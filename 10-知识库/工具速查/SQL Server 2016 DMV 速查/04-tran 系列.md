# 04 - sys.dm_tran_* 系列（事务与锁）

> 阻塞、死锁、长事务的核心数据源。

---

## sys.dm_tran_active_transactions

**用途**：实例级所有活动事务。**找长事务的入口**。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-tran-active-transactions-transact-sql?view=sql-server-2016

**13 列，常用 5 个**：

| 列 | 类型 | 含义 |
|---|---|---|
| `transaction_id` | bigint | 事务 ID（JOIN 锁、session_transactions 都用这个） |
| `name` | nvarchar(32) | 事务名（BEGIN TRAN xxx 的 xxx） |
| `transaction_begin_time` | datetime | **开始时间**（找长事务用） |
| `transaction_type` | int | 1=读写 / 2=只读 / 3=系统 / 4=分布式 |
| `transaction_state` | int | 0=未初始化 / 1=已初始化未启动 / 2=活动 / 3=已结束(只读) / 4=已发送提交 / 5=已准备好 / 6=已提交 / 7=正在回滚 / 8=已回滚 |
| `dtc_state` | int | 分布式事务状态 |

**实战（找超过 1 分钟的事务）**：
```sql
SELECT at.transaction_id, at.name, at.transaction_begin_time,
       DATEDIFF(second, at.transaction_begin_time, GETDATE()) AS duration_sec,
       st.session_id, s.login_name, s.host_name, s.program_name,
       t.text AS current_sql
FROM sys.dm_tran_active_transactions at
JOIN sys.dm_tran_session_transactions st ON at.transaction_id = st.transaction_id
JOIN sys.dm_exec_sessions s ON st.session_id = s.session_id
LEFT JOIN sys.dm_exec_requests r ON s.session_id = r.session_id
OUTER APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE at.transaction_begin_time < DATEADD(minute, -1, GETDATE())
  AND at.transaction_state = 2
ORDER BY at.transaction_begin_time;
```

---

## sys.dm_tran_session_transactions

**用途**：session ↔ transaction 映射表。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-tran-session-transactions-transact-sql?view=sql-server-2016

| 列 | 含义 |
|---|---|
| `session_id` | session |
| `transaction_id` | 对应事务 |
| `transaction_descriptor` | 客户端事务描述符 |
| `enlist_count` | 加入分布式事务的次数 |
| `is_user_transaction` | 1 = BEGIN TRAN 显式开 |
| `is_local` | 1 = 本地事务 |
| `is_enlisted` | 1 = 已加入分布式 |
| `is_bound` | 1 = 绑定会话 |

---

## sys.dm_tran_locks

**用途**：当前所有锁。**阻塞链分析的核心**。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-tran-locks-transact-sql?view=sql-server-2016

**14 列，常用 10 个**：

| 列 | 类型 | 含义 |
|---|---|---|
| `request_session_id` | int | 谁持有/请求 |
| `resource_database_id` | int | 哪个库的资源 |
| `resource_type` | nvarchar(60) | DATABASE/OBJECT/PAGE/KEY/RID/EXTENT/HOBT/METADATA/APPLICATION 等 |
| `resource_subtype` | nvarchar(60) | 子类型 |
| `resource_description` | nvarchar(256) | 资源详情（如 PAGE 的 fileid:pageid） |
| `resource_associated_entity_id` | bigint | OBJECT → object_id，KEY/PAGE → hobt_id |
| `request_mode` | nvarchar(60) | S/X/U/IS/IX/IU/SIX/UIX/Sch-S/Sch-M/BU/RangeS-S/RangeS-U/RangeI-N/RangeX-X |
| `request_type` | nvarchar(60) | LOCK |
| `request_status` | nvarchar(60) | GRANT/WAIT/CONVERT |
| `request_owner_type` | nvarchar(60) | TRANSACTION/CURSOR/SESSION/SHARED_TRANSACTION_WORKSPACE 等 |

**实战（找阻塞链）**：
```sql
SELECT
    blocked.request_session_id AS blocked_sid,
    blocking.request_session_id AS blocking_sid,
    blocked.resource_type, blocked.request_mode AS blocked_mode,
    blocking.request_mode AS held_mode, blocked.resource_description,
    s_blocked.host_name AS blocked_host, s_blocking.host_name AS blocking_host
FROM sys.dm_tran_locks blocked
JOIN sys.dm_tran_locks blocking
     ON blocked.resource_associated_entity_id = blocking.resource_associated_entity_id
    AND blocked.request_status = 'WAIT'
    AND blocking.request_status = 'GRANT'
    AND blocked.request_session_id <> blocking.request_session_id
JOIN sys.dm_exec_sessions s_blocked ON blocked.request_session_id = s_blocked.session_id
JOIN sys.dm_exec_sessions s_blocking ON blocking.request_session_id = s_blocking.session_id;
```

**锁模式速记**：
- `S` 共享 / `X` 排他 / `U` 更新
- `IS/IX/IU` 意向（表级，表示子级有 S/X/U）
- `SIX` 共享+意向排他
- `Sch-S` 架构稳定 / `Sch-M` 架构修改
- `Range*` 序列化隔离用
