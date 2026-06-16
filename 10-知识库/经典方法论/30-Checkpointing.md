---
title: "30-Checkpointing"
created: 2026-03-29
updated: 2026-06-16
type: methodology
tags: [agent, methodology]
status: stable
date: 2026-04-08
category: Notes
---

# Checkpointing（检查点 / 回退回放机制）

来源（官方）：<https://code.claude.com/docs/en/checkpointing>

## 1. 核心概念

**Checkpointing** 是 AI Agent 在执行长时任务时，将**完整执行状态序列化到持久存储**的机制。目的是在中断、失败或需要人工审核时，能够**从断点恢复**而不是从头重跑。

> [!note] 定义
> Checkpoint = 某个时间点的完整状态快照（变量、消息历史、工具输出、当前节点位置）  
> Checkpointing = 周期性保存 Checkpoint 的过程

### 与传统状态管理的区别

| 概念 | 作用域 | 目的 | .NET 类比 |
|------|-------|------|----------|
| **State Management** | 运行时内存状态 | 节点间传递数据 | `HttpContext.Items` |
| **Persistence** | 跨会话存储 | 长期记忆 | `DbContext.SaveChanges()` |
| **Checkpointing** | 可恢复的执行点 | 故障恢复 + 回放 | `TransactionScope` + SQL Savepoint |

> [!tip] SQL Server 类比
> ```sql
> BEGIN TRANSACTION
> SAVE TRANSACTION Checkpoint1;  -- 保存点
> UPDATE Accounts SET Balance = Balance - 100 WHERE ID = 1;
> SAVE TRANSACTION Checkpoint2;
> -- 出错了！
> ROLLBACK TRANSACTION Checkpoint2;  -- 回滚到 Checkpoint2
> COMMIT;
> ```
> LangGraph 的 Checkpoint 允许你"回滚"到任意历史节点。

### LangGraph 中的 Checkpointing

**自动保存时机**：每个 "super-step"（一轮完整的节点执行）后  
**存储结构**：Thread（线程）→ Checkpoint 序列

```python
from langgraph.checkpoint.memory import MemorySaver

# 编译时指定 Checkpointer
graph = builder.compile(checkpointer=MemorySaver())

# 每次调用自动保存 Checkpoint
config = {"configurable": {"thread_id": "thread-123"}}
result = graph.invoke({"messages": [...]}, config)

# 随时回溯历史状态
history = graph.get_state_history(config)
for checkpoint in history:
    print(checkpoint.values, checkpoint.next_nodes)
```

## 2. 解决的问题

### 长时任务的脆弱性

**无 Checkpointing 的代价**：
```
30 分钟工作流 → 第 29 分钟崩溃 → 从头重跑 → 成本翻倍
```

| 场景 | 无 Checkpoint 后果 | 有 Checkpoint 后果 |
|------|------------------|------------------|
| **API 超时** | 所有工作丢失，重新调用所有 API | 从断点恢复，仅重试失败步骤 |
| **人工审核** | 无法暂停等待，或强制重启 | 持久化状态，人类审批后精确恢复 |
| **多步推理** | 每次推理从头思考，Token 浪费 | 保存中间推理链，逐步深化 |
| **并行任务** | 一个子任务失败拖累全局 | 子任务独立 Checkpoint，失败仅影响自己 |

### 2026 生产案例

**LangChain 官方报告**：60% 的生产事故源于状态管理问题（State of Agent Engineering 2026）

**AWS Well-Architected Agentic AI Lens** (2026.03)：
> 没有 Checkpoint 的长时工作流，中断后需要支付完整的重启成本。在自然边界处设置 Checkpoint 并设计幂等步骤，让 Agent 从最后完成的检查点恢复，而不是重做工作。

## 3. 代表项目/论文/框架（链接）

### 主流 Checkpointing 实现

| 框架 | Checkpointer 类型 | 存储后端 | 特性 |
|------|-----------------|---------|------|
| **LangGraph** | 内置 + 可扩展 | Memory / Postgres / Redis / SQLite | Thread 隔离、时间旅行调试 |
| **Temporal** | Event Sourcing | 自托管 / Temporal Cloud | 事件重放、活动级 Checkpoint |
| **AWS Step Functions** | 托管服务 | DynamoDB | 每个状态转换自动持久化 |
| **CrewAI** | 内置 | 文件系统 / 数据库 | 任务级断点保存 |
| **Claude Code** | 编辑历史 | 本地文件系统 | 代码变更可回退，但不含 bash 操作 |

#### LangGraph Checkpointer 生态

**官方 Checkpointer**：
- `MemorySaver`：内存（开发测试）
- `SqliteSaver`：本地 SQLite（单机生产）
- `PostgresSaver`：生产级分布式存储
- `RedisSaver`（第三方）：高性能 KV 存储

**第三方集成**：
- **ScyllaDB**：10x Cassandra 性能，支持十亿级 Checkpoint
- **Supabase**：Postgres + Real-time + Auth 一体化
- **MongoDB**：文档存储，灵活 Schema

**参考资料**：
- [LangGraph State Management (EastonDev 2026)](https://eastondev.com/blog/en/posts/ai/20260424-langgraph-agent-architecture)
- [ScyllaDB + LangGraph Agentic AI](https://www.scylladb.com/2026/04/08/agentic-ai-state-management-with-scylladb-and-langgraph)
- [Medium: Mastering Persistence in LangGraph](https://medium.com/@vinodkrane/mastering-persistence-in-langgraph-checkpoints-threads-and-beyond-21e412aaed60)

### Temporal 的持久化执行模型

**核心思想**：不保存状态快照，而是保存**事件历史**（Event History），失败后通过重放事件重建内存状态。

```python
# Temporal Workflow 示例
@workflow.defn
class DataProcessingWorkflow:
    @workflow.run
    async def run(self, data_id: str):
        # Activity 1: 下载数据（可能失败）
        data = await workflow.execute_activity(
            download_data,
            data_id,
            start_to_close_timeout=timedelta(minutes=5)
        )
        # Activity 2: 处理数据
        result = await workflow.execute_activity(
            process_data,
            data,
            start_to_close_timeout=timedelta(minutes=30)
        )
        # Activity 3: 上传结果
        await workflow.execute_activity(
            upload_result,
            result,
            start_to_close_timeout=timedelta(minutes=5)
        )
        return result

# 如果 process_data 崩溃：
# 1. Temporal 记录了 Activity 1 成功完成的事件
# 2. 重启后重放历史，跳过 Activity 1，直接重试 Activity 2
# 3. 无需重新下载数据
```

**优势**：精确到 Activity 粒度，不浪费已完成的工作  
**代价**：需要所有 Activity 幂等（重复执行结果一致）

## 4. 工程落地清单（Checklist）

### 4.1 什么时候需要 Checkpointing？

**决策矩阵**：

| 场景 | 是否需要 | 推荐方案 |
|------|---------|---------|
| 单轮对话（<5 秒完成） | ❌ | 无需 Checkpoint |
| 多轮对话（需要跨会话记忆） | ✅ | LangGraph MemorySaver（开发）/ PostgresSaver（生产） |
| 长时任务（>5 分钟） | ✅✅ | 必须 Checkpoint，建议 PostgresSaver 或 ScyllaDB |
| 需要人工审核 (HITL) | ✅✅ | 必须 Checkpoint + `interrupt_before/after` |
| 涉及外部副作用（支付、邮件、数据库写入） | ✅✅ | Checkpoint + 幂等性保证 |

### 4.2 LangGraph Checkpointing 实战

#### 基础配置

```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.postgres import PostgresSaver

# 生产环境：Postgres Checkpointer
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost:5432/checkpoints"
)

graph = builder.compile(checkpointer=checkpointer)

# Thread ID 隔离不同会话
config1 = {"configurable": {"thread_id": "user-alice-session-1"}}
config2 = {"configurable": {"thread_id": "user-bob-session-1"}}

# 两个用户的状态完全隔离
graph.invoke({"messages": [...]}, config1)
graph.invoke({"messages": [...]}, config2)
```

#### 时间旅行调试

```python
# 回溯历史所有 Checkpoint
history = graph.get_state_history(config)

print("历史 Checkpoint:")
for i, checkpoint in enumerate(history):
    print(f"[{i}] Step: {checkpoint.metadata['step']}")
    print(f"    State: {checkpoint.values}")
    print(f"    Next Nodes: {checkpoint.next_nodes}")

# 从历史某个点重新执行
target_checkpoint = list(history)[3]  # 回到第 3 个 Checkpoint
graph.update_state(
    config,
    target_checkpoint.values,
    as_node="some_node"  # 指定从哪个节点恢复
)
```

#### 手动触发 Checkpoint

```python
from langgraph.checkpoint import Checkpoint

def custom_node(state):
    # 做一些工作...
    intermediate_result = expensive_computation(state)
    
    # 手动触发 Checkpoint（虽然 LangGraph 自动做，但你可以强制）
    # 注意：LangGraph 的 Checkpointer 接口不支持显式调用
    # 实际上每个节点执行后自动保存
    
    return {"result": intermediate_result}
```

**注意**：LangGraph 的 Checkpointing 是自动的，你不需要（也不能）手动调用 `save_checkpoint()`。每个节点执行后框架会自动保存。

### 4.3 幂等性设计

**核心原则**：同一个 Checkpoint 恢复后重跑，不应产生重复副作用。

```python
# ❌ 不幂等：每次重跑都发邮件
def send_notification(state):
    send_email(state["user_email"], "订单确认")
    return {"status": "notified"}

# ✅ 幂等：检查是否已发送
def send_notification_idempotent(state):
    if state.get("notification_sent"):
        return state  # 已发送，跳过
    
    send_email(state["user_email"], "订单确认")
    return {"status": "notified", "notification_sent": True}

# ✅✅ 最佳实践：使用幂等键
def send_notification_with_key(state):
    idempotency_key = f"order-{state['order_id']}-notification"
    
    # 邮件服务检查该 key 是否已处理
    send_email_idempotent(
        to=state["user_email"],
        subject="订单确认",
        idempotency_key=idempotency_key
    )
    return {"status": "notified"}
```

### 4.4 Checkpoint 生命周期管理

```python
# PostgresSaver 配置示例
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://...",
    # Checkpoint 保留策略
    max_checkpoints_per_thread=100,  # 每个 Thread 最多保留 100 个
    ttl_seconds=7 * 24 * 3600,       # 7 天后自动清理
)

# 手动清理过期 Thread
async def cleanup_old_threads():
    cutoff_date = datetime.now() - timedelta(days=30)
    await checkpointer.delete_threads_before(cutoff_date)
```

### 4.5 监控指标

| 指标 | 告警阈值 | 原因分析 |
|------|---------|---------|
| **Checkpoint 写入延迟** | >500ms | 数据库性能瓶颈，考虑切换 ScyllaDB |
| **Checkpoint 大小** | >1MB | State 膨胀，考虑压缩或裁剪历史消息 |
| **恢复失败率** | >1% | Checkpoint 数据损坏或 Schema 变更不兼容 |
| **Thread 数量** | >100 万 | 需要清理策略，防止存储爆炸 |

### 4.6 Claude Code 特定限制

**你需要记住的点**：
- Claude Code 会在**每次编辑前**自动做 Checkpoint，可通过 `/rewind` 回退。
- 支持：
  - 只回退代码 / 只回退对话 / 两者都回退
  - 从某个点开始 summarize（压缩上下文，避免 context window 爆掉）

**最重要的限制（务必记住）**：
- **bash 命令改动不在 Checkpoint 里**。
  - 比如 `rm/mv/cp` 或脚本生成文件，rewind 不会帮你恢复。
  - 所以：重要变更一定要用 Git（commit/branch）兜底。

**企业落地建议**：
- 对关键模块：让 Claude 在改之前先创建分支或 worktree（隔离）。
- 形成固定节奏：小步提交（每完成一个子任务就 commit）。

## 5. 七种持久化策略对比

来源：[Indium Tech: 7 State Persistence Strategies (2026)](https://www.indium.tech/blog/7-state-persistence-strategies-ai-agents-2026)

| 策略 | 何时使用 | 优点 | 缺点 |
|------|---------|------|------|
| **1. Checkpoint-Restore** | 长时任务，需要故障恢复 | 简单直接，精确恢复 | Checkpoint 间隔内的工作可能丢失 |
| **2. Event Sourcing** | 需要完整审计日志 | 精确重放，无信息丢失 | 存储成本高，重放慢 |
| **3. Incremental State** | 高频小更新 | 低延迟，增量写入 | 复杂度高，难调试 |
| **4. Snapshot + Delta** | 大状态 + 小变更 | 平衡存储和恢复速度 | 需要合并逻辑 |
| **5. Lazy Loading** | 状态很大但只用部分 | 节省内存 | 网络往返增加延迟 |
| **6. Versioned State** | 需要回滚到历史版本 | 支持时间旅行 | 存储爆炸风险 |
| **7. Hybrid（混合）** | 复杂生产系统 | 针对不同数据选最优策略 | 架构复杂 |

**推荐组合**：LangGraph（Checkpoint-Restore）+ Temporal（Event Sourcing）+ Redis（Incremental State for real-time）

## 6. 更新记录

- **2026-06-16**：完整补充内容（核心概念深化、7 种持久化策略、LangGraph 实战、幂等性设计、监控指标）
  - 数据来源：LangChain/LangGraph 官方文档、AWS Well-Architected Agentic AI Lens、ScyllaDB/Temporal 技术博客
  - 框架覆盖：LangGraph、Temporal、AWS Step Functions、CrewAI、Claude Code
  - 新增章节：幂等性设计、Checkpoint 生命周期管理、七种持久化策略对比
- **2026-04-20**：添加 Claude Code 特定限制和企业落地建议
- **2026-03-29**：初始化骨架文件
