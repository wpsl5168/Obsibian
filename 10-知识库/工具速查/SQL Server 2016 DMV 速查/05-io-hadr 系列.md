---
title: SQL Server 2016 DMV - io/hadr 系列
created: 2026-05-23
updated: 2026-05-23
type: entity
tags: [tooling, methodology]
status: stable
---

# 05 - IO + HADR + 扩展事件

> 文件 IO 延迟、AlwaysOn 副本健康、XE 监控。

---

## sys.dm_io_virtual_file_stats(database_id, file_id)

**用途**：TVF，每个数据文件 / 日志文件的 IO 统计（**累计**，自实例启动）。**找慢盘的标准入口**。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-io-virtual-file-stats-transact-sql?view=sql-server-2016

**11 列**：

| 列 | 类型 | 含义 |
|---|---|---|
| `database_id` | smallint | 哪个库（NULL=所有） |
| `file_id` | smallint | 文件 ID（NULL=所有） |
| `sample_ms` | int | 自启动至今的采样窗口毫秒 |
| `num_of_reads` | bigint | 读次数 |
| `num_of_bytes_read` | bigint | 读字节 |
| `io_stall_read_ms` | bigint | **读等待累计毫秒**（关键） |
| `num_of_writes` | bigint | 写次数 |
| `num_of_bytes_written` | bigint | 写字节 |
| `io_stall_write_ms` | bigint | **写等待累计毫秒**（关键） |
| `io_stall` | bigint | 读+写等待 |
| `size_on_disk_bytes` | bigint | 磁盘上大小 |

**实战（平均读写延迟，> 20ms 算慢）**：
```sql
SELECT DB_NAME(vfs.database_id) AS db, mf.physical_name,
       vfs.num_of_reads, vfs.num_of_writes,
       vfs.io_stall_read_ms / NULLIF(vfs.num_of_reads, 0) AS avg_read_ms,
       vfs.io_stall_write_ms / NULLIF(vfs.num_of_writes, 0) AS avg_write_ms,
       vfs.size_on_disk_bytes / 1024 / 1024 AS file_mb
FROM sys.dm_io_virtual_file_stats(NULL, NULL) vfs
JOIN sys.master_files mf ON vfs.database_id = mf.database_id AND vfs.file_id = mf.file_id
ORDER BY vfs.io_stall DESC;
```

**经验阈值**：
- 数据文件读写 < 10ms 优秀，10-20ms 可接受，> 20ms 慢
- 日志文件写 < 5ms 优秀，> 15ms 该换盘了

---

## sys.dm_hadr_database_replica_states（⚠️ 列名陷阱）

**用途**：AlwaysOn 可用性组里每个数据库副本的状态。**判断同步健康度**。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-hadr-database-replica-states-transact-sql?view=sql-server-2016

**20 列，关键 11 个**：

| 列 | 类型 | 含义 |
|---|---|---|
| `database_id` | int | ⚠️ **只有 database_id，没有 database_name**，要 `DB_NAME(database_id)` |
| `replica_id` | uniqueidentifier | JOIN sys.availability_replicas |
| `group_database_id` | uniqueidentifier | AG 全局数据库 ID |
| `is_local` | bit | 1 = 本机的副本 |
| `is_primary_replica` | bit | 1 = 主副本 |
| `synchronization_state_desc` | nvarchar(60) | NOT SYNCHRONIZING / SYNCHRONIZING / SYNCHRONIZED / REVERTING / INITIALIZING |
| `synchronization_health_desc` | nvarchar(60) | NOT_HEALTHY / PARTIALLY_HEALTHY / HEALTHY |
| `log_send_queue_size` | bigint | **主→辅 待发送日志 KB**（积压关键指标） |
| `log_send_rate` | bigint | 发送速率 KB/s |
| `redo_queue_size` | bigint | **辅→已收到但未重做 KB**（重做积压） |
| `redo_rate` | bigint | 重做速率 KB/s |
| `last_sent_time` | datetime | 最后发送 |
| `last_received_time` | datetime | 最后接收 |
| `last_hardened_time` | datetime | 最后刷盘 |
| `last_redone_time` | datetime | 最后重做 |
| `last_commit_time` | datetime | 最后提交 |

**⚠️ v9 修复**（15_备份与高可用检查.sql 第 112 行）：
```sql
-- ❌ 不存在 database_name 列
SELECT drs.database_name, ...

-- ✅ 用 DB_NAME 转
SELECT DB_NAME(drs.database_id) AS database_name, ...
```

**实战（健康检查）**：
```sql
SELECT
    ar.replica_server_name,
    DB_NAME(drs.database_id) AS db_name,
    drs.synchronization_state_desc, drs.synchronization_health_desc,
    drs.log_send_queue_size AS send_queue_kb,
    drs.redo_queue_size AS redo_queue_kb,
    DATEDIFF(second, drs.last_commit_time, GETDATE()) AS commit_lag_sec
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON drs.replica_id = ar.replica_id
WHERE drs.is_local = 0  -- 看远程副本
ORDER BY drs.log_send_queue_size DESC;
```

**故障转移决策**：
- `synchronization_state_desc = SYNCHRONIZED` + `synchronization_health_desc = HEALTHY` → 可无损同步切
- 否则只能异步切，会丢数据

---

## sys.dm_xe_sessions

**用途**：扩展事件会话列表。检查 `system_health` / `AlwaysOn_health` 等是否在跑。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-xe-sessions-transact-sql?view=sql-server-2016

**关键列**：
| 列 | 含义 |
|---|---|
| `name` | 会话名 |
| `create_time` | 启动时间 |
| `total_buffer_size_kb` | 缓冲区大小 |
| `dropped_event_count` | 丢失事件数（> 0 说明压力大） |

**实战**：
```sql
SELECT name, create_time, dropped_event_count, dropped_buffer_count
FROM sys.dm_xe_sessions
WHERE name IN ('system_health', 'AlwaysOn_health', 'telemetry_xevents');
```

**配套查死锁（从 system_health 拉死锁图）**：
```sql
SELECT XEvent.value('@timestamp', 'datetime') AS deadlock_time,
       XEvent.query('.') AS deadlock_graph
FROM (
    SELECT CAST(target_data AS XML) AS target_data
    FROM sys.dm_xe_session_targets st
    JOIN sys.dm_xe_sessions s ON s.address = st.event_session_address
    WHERE s.name = 'system_health' AND st.target_name = 'ring_buffer'
) AS data
CROSS APPLY target_data.nodes('//RingBufferTarget/event[@name="xml_deadlock_report"]') AS XEventData(XEvent);
```
