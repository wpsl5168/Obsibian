---
title: "01-工作流编排（Graphs & Workflows）"
created: 2026-03-28
updated: 2026-06-02
type: methodology
tags: [workflow, methodology, agent]
status: draft
date: 2026-04-08
category: Notes
---

# 01-工作流编排（Graphs & Workflows）

## 1. 核心概念

工作流编排是AI Agent系统中**定义执行顺序、状态传递、失败恢复**的架构模式。相比单Agent的线性ReAct循环，复杂任务需要显式的流程图来协调多个步骤。

三种主流架构模式：

| 模式 | 类比（.NET/SQL） | 特点 | 适用场景 |
|------|-----------------|------|---------|
| **DAG（有向无环图）** | SSIS数据流管道 | 显式依赖关系，确定性执行顺序 | ETL、多Agent顺序协作、审批流 |
| **状态机（State Machine）** | WF（Windows Workflow）状态机 | 明确定义状态转移条件，显式guard条件 | 订单流程、HITL交接、有明确阶段的任务 |
| **事件驱动（Event-driven）** | Azure Service Bus + Event Grid | 异步pub/sub，Agent作为事件消费者 | 微服务解耦、实时响应、长时任务 |

**为什么需要编排？** ReAct单Agent面对复杂任务时会：
- 无限循环（没有终止条件）
- 状态丢失（上下文超长被截断）
- 成本失控（每次重新规划都调LLM）

显式编排通过**预定义DAG节点**固化确定性部分，只让LLM负责不确定的决策点。

## 2. 解决的问题

| 生产痛点 | 编排方案 |
|---------|---------|
| **死锁与循环依赖** | DAG拓扑排序保证无环，状态机显式guard防止非法转移 |
| **状态腐败** | 每个节点typed state + snapshot checkpoint（类似SQL Server快照隔离级别） |
| **HITL卡住** | 状态机的wait_for_human状态，超时自动降级或escalate |
| **部分失败恢复** | Checkpoint + replay，类似Kafka offset commit机制 |
| **可观测性盲区** | 每个节点emit trace span（OpenTelemetry），DAG执行图可视化 |

## 3. 代表项目/论文/框架（链接）

### 生产级框架（2026排名）

| 框架 | 编排模式 | 适用场景 | 市场占有率 |
|------|---------|---------|-----------|
| **[LangGraph](https://langchain-ai.github.io/langgraph/)** | 状态机 + DAG混合 | 复杂stateful workflow，月搜索量27.1K | #1 |
| **[CrewAI](https://crewai.com/)** | 角色编排（role-based） | 多Agent协作，角色分工明确 | #2（月搜索14.8K） |
| **[Claude Agent SDK](https://docs.anthropic.com/claude/docs/agents-sdk)** | 内置MCP编排 | Anthropic原生生产Agent（Claude Code底层） | 官方推荐 |
| **[AutoGen v0.4](https://microsoft.github.io/autogen/)** | Actor模型 | 对话式研究Agent，消息传递 | 学术界主流 |
| **[Temporal](https://temporal.io/)** | DAG + durable execution | 长时任务、分布式重试、金融级可靠性 | 企业级 |
| **[Dagster](https://dagster.io/)** | 数据编排DAG | 数据管道 + ML Ops | 数据工程主流 |

**选型指南**（Alice Labs 18次生产部署总结）：
- **控制力优先** → LangGraph（显式状态管理，调试友好）
- **团队速度** → CrewAI（角色分工直观，快速原型）
- **Anthropic生态** → Claude Agent SDK（MCP原生集成）
- **.NET栈** → [Semantic Kernel](https://learn.microsoft.com/semantic-kernel/)（微软官方，C#一等公民）
- **金融/合规** → Temporal（ACID级别durability）

### 经典论文与模式

- **Plan-and-Execute**：先用LLM生成DAG执行计划，再按图执行（Yao et al., 2023 ReAct）
- **Hierarchical Agent**：上层Agent生成子任务DAG，下层专家Agent执行叶节点（Google SIMA, 2025）
- **Human-in-the-Loop Orchestration**：状态机中插入`approval_gate`状态，等待人类审批后继续

## 4. 工程落地清单（Checklist）

### 4.1 架构选型决策树

```
任务类型？
├─ 确定性流程（审批/ETL）        → DAG（LangGraph/Temporal）
├─ 多角色协作（研究/写作）        → CrewAI
├─ 长时任务（>1天/需断点续传）    → Temporal + durable execution
├─ 实时事件响应（监控/告警）      → Event-driven（Kafka + Agent消费者）
└─ 对话式研究（多Agent辩论）      → AutoGen/AG2
```

### 4.2 状态管理规范

| 要点 | 实现 |
|------|------|
| **Typed State** | 用Pydantic定义状态schema，禁止`dict[str, Any]` |
| **Immutability** | 每个节点返回new state，不直接修改（类似Redux reducer） |
| **Checkpoint策略** | 关键节点snapshot到Redis/Postgres，5min checkpoint间隔 |
| **State TTL** | 超过7天未更新的state自动归档到冷存储 |

### 4.3 失败恢复机制

```python
# 示例：LangGraph checkpoint恢复
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
graph = builder.compile(checkpointer=checkpointer)

# 失败后从断点续传
result = graph.invoke(
    input, 
    config={"configurable": {"thread_id": "task_123"}},
    resume_from_checkpoint=True  # 从最后成功节点继续
)
```

**重试策略**（避免成本爆炸）：
- 前3次重试：原节点重试，间隔2/4/8秒（exponential backoff）
- 第4-5次：降级到更便宜模型（GPT-4→3.5，Claude Opus→Sonnet）
- 第6次：HITL escalate，人工接管

### 4.4 成本控制门禁

| 门禁 | 阈值 | 触发动作 |
|------|------|---------|
| **单任务token上限** | 500K tokens | 强制终止 + 拆分任务建议 |
| **单节点重试次数** | 5次 | 标记为failed + 人工审查 |
| **并行度** | 8个Agent | 超过则排队（防止API rate limit） |
| **执行时长** | 5分钟 | 超时自动checkpoint + 异步继续 |

### 4.5 可观测性埋点

```python
# OpenTelemetry span追踪每个节点
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def my_node(state):
    with tracer.start_as_current_span("node:my_node") as span:
        span.set_attribute("input_length", len(state["input"]))
        # ... 节点逻辑
        span.set_attribute("output_length", len(result))
        return result
```

**监控指标**：
- **节点级延迟分布**（P50/P95/P99）→ 找到瓶颈节点
- **状态转移热力图**（state_a→state_b频率）→ 发现异常跳转
- **Checkpoint频率**（每小时checkpoint次数）→ 判断任务复杂度

### 4.6 调试与测试

| 工具 | 用途 |
|------|------|
| **LangGraph Studio** | 可视化状态机执行图，单步调试 |
| **Replay测试** | 用生产checkpoint数据在本地重放 |
| **Chaos Engineering** | 随机kill节点，测试恢复能力 |

**单元测试模式**：
```python
# 测试单个节点的状态转换
def test_approval_node():
    input_state = {"status": "pending", "content": "xxx"}
    output_state = approval_node(input_state)
    assert output_state["status"] == "approved"
    assert "timestamp" in output_state
```

## 5. 更新记录

| 日期 | 更新内容 |
|------|---------|
| 2026-06-02 | 补充核心概念、三种编排模式对比、2026框架排名（LangGraph/CrewAI/Claude SDK）、工程落地清单（状态管理/失败恢复/成本控制/可观测性） |
| 2026-04-08 | 初始版本（空骨架） |
