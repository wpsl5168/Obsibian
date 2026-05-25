---
title: SQL Server 2016 DMV 速查手册
created: 2026-05-23
updated: 2026-05-23
type: entity
tags: [tooling, methodology]
status: stable
---

# SQL Server 2016 SP2 DMV 速查手册

> 基于 dba-toolkit v9 文档驱动审计沉淀（2026-05-22）。每个 DMV 的列定义、版本陷阱、实战踩坑均对照 Microsoft Learn 2016 官方文档原文整理。
>
> **目标受众**：在 SQL Server 2016/2017 上做性能巡检、应急排障的 DBA / Dev。
>
> **核心价值**：避免凭印象写 SQL → 跑到客户现场报错 → 来回返工。

---

## 📚 分类索引

| 文件 | 覆盖 DMV | 用途 |
|---|---|---|
| [[01-exec 系列|01-exec 系列（执行与会话）]] | dm_exec_requests/sessions/sql_text/connections/cached_plans/query_plan/query_memory_grants | 当前会话、运行中请求、SQL 文本、执行计划 |
| [[02-os 系列|02-os 系列（操作系统层）]] | dm_os_wait_stats/waiting_tasks/sys_info/windows_info/memory_clerks/buffer_descriptors/performance_counters/workers/threads/ring_buffers | 等待统计、CPU/内存/IO 系统级指标 |
| [[03-db 系列|03-db 系列（数据库与索引）]] | dm_db_index_usage_stats/index_physical_stats/stats_properties/file_space_usage/session_space_usage/missing_index_* | 索引使用、碎片、缺失索引、空间 |
| [[04-tran 系列|04-tran 系列（事务与锁）]] | dm_tran_active_transactions/locks/session_transactions | 活动事务、锁等待、长事务排查 |
| [[05-io-hadr 系列|05-io-hadr 系列（IO + AlwaysOn）]] | dm_io_virtual_file_stats/hadr_database_replica_states/xe_sessions | 文件 IO 延迟、副本健康度、扩展事件 |

---

## ⚠️ 2016 → 2017+ 版本陷阱速查表（最易踩坑）

这些列在 2016 上**不存在**，凭印象写就报 `Invalid column name`：

| DMV | 2017+ 才有的列 | 2016 替代方案 |
|---|---|---|
| `sys.dm_exec_query_stats` | `total_compile_time` / `last_compile_time` / `min_compile_time` / `max_compile_time` | 用 `plan_generation_num` + `creation_time` 推断 |
| `sys.dm_exec_query_stats` | `total_columnstore_segment_reads` / `total_columnstore_segment_skips` | 无替代，跳过列存指标 |
| `sys.dm_db_index_physical_stats` | `version_ghost_record_count`（2019+） | 用 `ghost_record_count` |
| `sys.dm_os_sys_info` | `socket_count`（2017+ 才稳定） | 用 `cpu_count / hyperthread_ratio` 推算 |
| `sys.dm_exec_session_wait_stats` | 2016 SP1+ 才有，旧 SP 没有 | 先 `SELECT @@VERSION` 看 SP 等级 |

---

## 🔥 v9 审计踩过的 5 个 Critical 坑（值得永远记住）

| # | 错误写法 | 正确写法 | 根因 |
|---|---|---|---|
| 1 | `dm_os_workers.kernel_time` | `JOIN dm_os_threads ON ... THEN t.kernel_time` | `kernel_time / usermode_time` 在 **threads** DMV，不在 workers |
| 2 | `dm_exec_requests.database_id`（误以为在 requests） | `dm_exec_sessions.database_id` | `database_id` 在 sessions，**不在 requests**（requests 有 database_id 但 2016 容易混） |
| 3 | `dm_exec_query_stats.total_compile_time` | 删列，改用 `plan_generation_num + creation_time` | 2017+ 才有 |
| 4 | `dm_hadr_database_replica_states.database_name` | `DB_NAME(drs.database_id)` | AlwaysOn DMV 只有 `database_id bigint`，无 name 列 |
| 5 | `DATEADD(ms, -1 * ms_ticks, GETDATE())` 算术溢出 | `DATEADD(ms, timestamp - tk.ms_ticks, GETDATE())` 或分段 | `ms_ticks` 是 bigint，服务器跑 > 24.8 天就爆 int |

---

## 🛠️ 调试套路（出错了怎么排）

1. **报 `Invalid column name`** → 先 `SELECT * FROM 该DMV` 看实际列，再对照 Microsoft Learn 官方文档（搜 `sys.dm_xxx` + `2016`）
2. **报 `Arithmetic overflow`** → 99% 是 bigint 被隐式转 int，找 DATEADD/SUM 处分段算
3. **报 `权限不足`** → 大多数 DMV 要 `VIEW SERVER STATE`，`USE master; GRANT VIEW SERVER STATE TO [login]`
4. **结果是空** → 检查 `WHERE` 是否过滤太严，或该功能未启用（如 AlwaysOn / Query Store）

---

## 📖 引用约定

每个分类文件里，每个 DMV 按这个模板：

```
### sys.dm_xxx_yyy
**用途**：一句话说清做什么
**官方文档**：链接
**关键列**：列名 + 类型 + 含义
**实战用法**：典型查询片段
**坑**：版本/类型/JOIN 陷阱
```

---

## 🔗 关联

- 工具集源码：`~/workspace/dba-toolkit-sqlserver-2016/`
- 当前交付包：`/tmp/dba-toolkit-sqlserver-2016-v9.tar.gz`
- Microsoft Learn 入口：https://learn.microsoft.com/sql/relational-databases/system-dynamic-management-views/system-dynamic-management-views?view=sql-server-2016
