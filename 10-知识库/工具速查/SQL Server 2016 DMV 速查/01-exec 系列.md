# 01 - sys.dm_exec_* 系列（执行与会话）

> 排查"现在谁在跑什么、卡在哪、跑了啥 SQL"的核心 DMV 群。

---

## sys.dm_exec_requests

**用途**：当前正在执行的每个请求（含系统进程）。性能排查第一入口。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-requests-transact-sql?view=sql-server-2016

**31 个列，常用 21 个**：

| 列 | 类型 | 含义 |
|---|---|---|
| `session_id` | smallint | 会话 ID，**JOIN dm_exec_sessions 的键** |
| `request_id` | int | 同 session 下的请求序号（MARS 才 >0） |
| `status` | nvarchar(30) | running/runnable/suspended/background/sleeping |
| `command` | nvarchar(32) | SELECT/INSERT/BACKUP DATABASE/etc |
| `database_id` | smallint | ⚠️ **2016 有这列**，但语义偏弱，优先用 sessions 的 |
| `cpu_time` | int | 累计 CPU 毫秒 |
| `total_elapsed_time` | int | 累计运行毫秒 |
| `wait_type` | nvarchar(60) | 当前等待类型（NULL = 没在等） |
| `wait_time` | int | 当前等待已经持续多少毫秒 |
| `last_wait_type` | nvarchar(60) | 上一次的等待类型 |
| `blocking_session_id` | smallint | 阻塞我的 session（0 = 没被阻塞） |
| `sql_handle` | varbinary(64) | **CROSS APPLY sys.dm_exec_sql_text(sql_handle) 拿 SQL** |
| `plan_handle` | varbinary(64) | CROSS APPLY sys.dm_exec_query_plan(plan_handle) 拿计划 |
| `statement_start_offset` | int | SQL 中当前执行子句的起始字节偏移 |
| `statement_end_offset` | int | 结束偏移（-1 = 到末尾） |
| `granted_query_memory` | int | 已授予内存（页数 × 8KB） |
| `reads/writes/logical_reads` | bigint | 累计 IO |
| `open_transaction_count` | int | 未提交事务数 |
| `percent_complete` | real | 仅 BACKUP/RESTORE/DBCC/ROLLBACK 等系统命令有值 |

**实战用法（取 SQL 文本 + 等待）**：
```sql
SELECT r.session_id, r.status, r.command, r.wait_type, r.wait_time,
       r.blocking_session_id, r.cpu_time, r.total_elapsed_time,
       SUBSTRING(t.text, r.statement_start_offset/2 + 1,
                 CASE r.statement_end_offset WHEN -1 THEN DATALENGTH(t.text)
                      ELSE r.statement_end_offset - r.statement_start_offset END / 2 + 1) AS sql_text
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.session_id > 50;
```

**坑**：
- ⚠️ `statement_end_offset` = -1 时要用 `DATALENGTH(t.text)` 兜底，否则 `SUBSTRING` 报错
- 没在执行的会话**不会**出现在 requests 里，要看 dm_exec_sessions

---

## sys.dm_exec_sessions

**用途**：所有已连接会话（含睡眠中），48 列。常和 requests 配对用。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-sessions-transact-sql?view=sql-server-2016

**常用 13 列**：

| 列 | 类型 | 含义 |
|---|---|---|
| `session_id` | smallint | 主键 |
| `database_id` | smallint | ⭐ **当前数据库上下文**，比 requests 准 |
| `status` | nvarchar(30) | running/sleeping |
| `login_time` | datetime | 登录时间 |
| `host_name` | nvarchar(128) | 客户端机器名 |
| `program_name` | nvarchar(128) | 客户端程序（如 .Net SqlClient） |
| `login_name` | nvarchar(128) | 当前登录名 |
| `original_login_name` | nvarchar(128) | ⭐ 真实登录（impersonate 前的原始） |
| `cpu_time` | int | 累计 CPU |
| `memory_usage` | int | 已用内存（页数） |
| `total_scheduled_time` | int | 累计排队时长 |
| `last_request_start_time` | datetime | 最后一次请求开始时间 |
| `is_user_process` | bit | 1 = 用户会话，0 = 系统会话（spid ≤ 50） |

**坑**：
- ⚠️ v9 踩过：`dm_exec_requests` 也有 `database_id`，但**取 `dm_exec_sessions.database_id` 更可靠**（requests 有时为 0）

---

## sys.dm_exec_sql_text(sql_handle | plan_handle)

**用途**：TVF，从 handle 还原 SQL 文本。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-sql-text-transact-sql?view=sql-server-2016

**5 列全用**：

| 列 | 类型 | 含义 |
|---|---|---|
| `dbid` | smallint | 编译时的 DB（ad-hoc 为 NULL） |
| `objectid` | int | 存储过程/函数的 object_id（ad-hoc 为 NULL） |
| `number` | smallint | 编号过程的编号（已废弃用法） |
| `encrypted` | bit | 1 = 加密对象，text 为 NULL |
| `text` | nvarchar(max) | **SQL 原文** |

**实战**：永远用 `CROSS APPLY`（OUTER APPLY 当 sql_handle 可能为 NULL 时用）

---

## sys.dm_exec_connections

**用途**：客户端到 SQL Server 的物理连接信息。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-connections-transact-sql?view=sql-server-2016

**常用 10 列**：

| 列 | 类型 | 含义 |
|---|---|---|
| `session_id` | int | JOIN 键 |
| `connect_time` | datetime | 物理连接建立时间 |
| `net_transport` | nvarchar(40) | TCP/Named Pipes/Shared Memory |
| `protocol_type` | nvarchar(40) | TSQL/SOAP/Service Broker |
| `protocol_version` | int | TDS 版本 |
| `client_net_address` | varchar(48) | **客户端 IP** |
| `client_tcp_port` | int | 客户端端口 |
| `local_net_address` | varchar(48) | 服务端 IP（哪个网卡） |
| `local_tcp_port` | int | 服务端端口 |
| `most_recent_sql_handle` | varbinary(64) | 该连接最后跑的 SQL handle |

**实战**：排查"哪个 IP 在打死我的数据库"
```sql
SELECT c.client_net_address, COUNT(*) AS conn_count
FROM sys.dm_exec_connections c
GROUP BY c.client_net_address
ORDER BY conn_count DESC;
```

---

## sys.dm_exec_cached_plans

**用途**：plan cache 里所有计划，2 列在脚本里用。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-cached-plans-transact-sql?view=sql-server-2016

**常用 2 列（实际 9 列）**：

| 列 | 类型 | 含义 |
|---|---|---|
| `plan_handle` | varbinary(64) | APPLY 给 sql_text / query_plan |
| `usecounts` | int | 复用次数（=1 的说明没参数化，可能是性能瓶颈） |
| `size_in_bytes` | int | 计划占内存 |
| `cacheobjtype` | nvarchar(34) | Compiled Plan / Parse Tree / Extended Proc |
| `objtype` | nvarchar(16) | Adhoc / Prepared / Proc / Trigger / View |

**实战（找单次使用的 ad-hoc 计划，可能要开 forced parameterization）**：
```sql
SELECT TOP 100 cp.usecounts, cp.size_in_bytes, cp.objtype, t.text
FROM sys.dm_exec_cached_plans cp
CROSS APPLY sys.dm_exec_sql_text(cp.plan_handle) t
WHERE cp.objtype = 'Adhoc' AND cp.usecounts = 1
ORDER BY cp.size_in_bytes DESC;
```

---

## sys.dm_exec_query_plan(plan_handle)

**用途**：TVF，从 plan_handle 拿 **XML 格式执行计划**。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-query-plan-transact-sql?view=sql-server-2016

**关键列**：
- `query_plan` xml — 点开能在 SSMS 里看图形化计划

**坑**：超过 SSMS 内存阈值的大计划会返回 NULL，用 `sys.dm_exec_text_query_plan` 拿文本版

---

## sys.dm_exec_query_memory_grants

**用途**：当前所有内存授予请求，排查内存压力 / sort spill。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-query-memory-grants-transact-sql?view=sql-server-2016

**常用 13 列**：

| 列 | 含义 |
|---|---|
| `session_id` | JOIN 键 |
| `requested_memory_kb` | 请求的内存 |
| `granted_memory_kb` | 已授予 |
| `required_memory_kb` | 至少需要的（不给就跑不起来） |
| `used_memory_kb` | 实际用了多少 |
| `max_used_memory_kb` | 历史峰值 |
| `query_cost` | 优化器估算成本 |
| `timeout_sec` | 等待超时秒数 |
| `queue_id` | 在哪个 resource semaphore 队列 |
| `wait_order` | 队列里第几位 |
| `is_next_candidate` | 1 = 下一个能拿到内存 |
| `dop` | 并行度 |
| `wait_time_ms` | 已经等多久 |

**实战**：找内存大户
```sql
SELECT session_id, requested_memory_kb, granted_memory_kb, used_memory_kb, dop
FROM sys.dm_exec_query_memory_grants
WHERE granted_memory_kb IS NOT NULL
ORDER BY granted_memory_kb DESC;
```

---

## sys.dm_exec_query_stats（⚠️ 2016 版本陷阱集中地）

**用途**：每个查询计划的累计性能统计。Top N 慢查询的标准入口。

**官方文档**：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-query-stats-transact-sql?view=sql-server-2016

**⚠️ 2016 上不存在的列（2017+ 才加）**：
- `total_compile_time` / `last_compile_time` / `min_compile_time` / `max_compile_time`
- `total_columnstore_segment_reads` 系列

**2016 替代方案**：
- 编译次数代理：`plan_generation_num`
- 计划新旧：`creation_time`、`last_execution_time`

**v9 修复（07_慢查询分析.sql 第 118-134 行）**：原脚本用了 `total_compile_time` → 2016 报错，已删除并改用 `plan_generation_num + creation_time`。
