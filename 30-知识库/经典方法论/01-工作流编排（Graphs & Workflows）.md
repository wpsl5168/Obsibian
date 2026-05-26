---
title: "01-工作流编排（Graphs & Workflows）"
created: 2026-03-28
updated: 2026-05-26
type: methodology
tags: [workflow, agent, methodology]
status: draft
---

# 01-工作流编排（Graphs & Workflows）

## 1. 核心概念

工作流编排（Workflow Orchestration）是将多个AI Agent、工具调用、人类交互组织成**有状态的执行图**的技术。与传统线性Pipeline不同，图结构支持：

- **条件分支**：根据运行时状态选择不同执行路径
- **循环与重试**：Agent可返回前序节点重新执行
- **并行执行**：多个节点同时运行并汇聚结果
- **持久化状态**：节点间共享上下文，支持长时运行任务

**核心组件**：
- **State（状态）**：所有节点共享的内存，通常用TypedDict定义Schema
- **Nodes（节点）**：独立的执行单元，可以是LLM调用、工具、人类输入
- **Edges（边）**：定义节点间的转移逻辑，支持静态边和动态路由
- **Checkpoints（检查点）**：自动保存状态快照，支持时间旅行调试和故障恢复

**与.NET类比**：
- State = WF4的WorkflowContext或TPL Dataflow的共享数据块
- Nodes = Activity或ActionBlock<T>
- Edges = Bookmark/Transition或DataflowLinkOptions
- LangGraph ≈ Durable Functions + Actor模型（像Orleans Grain的状态持久化）

## 2. 解决的问题

### 问题1：线性Pipeline的表达力瓶颈
**场景**：RAG系统需要"检索→判断质量→决策是否重新检索"，传统LCEL Chain无法回退。

**Graph解法**：
```python
# LangGraph伪代码
graph.add_node("retrieve", retrieve_docs)
graph.add_node("grade", grade_relevance)
graph.add_node("rewrite_query", rewrite)
graph.add_conditional_edges(
    "grade",
    lambda state: "rewrite" if state["score"] < 0.6 else "generate"
)
```

### 问题2：长时运行任务的容错性
**场景**：客服Agent处理多轮对话，中途服务重启会丢失上下文。

**Graph解法**：Checkpoint机制自动保存每个节点执行后的State到SQLite/Postgres，重启后从最后一个成功节点恢复。

### 问题3：多Agent协作的可观测性
**场景**：4个Agent并行工作（研究+写作+审校+发布），传统多线程难以追踪每个Agent的决策路径。

**Graph解法**：图拓扑天然可视化，每条边的触发条件、State变更都有完整日志。

## 3. 代表项目/框架

### LangGraph（LangChain官方，2026年主流）
- **定位**：企业级图编排框架，内置Checkpoint、人类在环、流式输出
- **优势**：与LangSmith深度集成（可观测性）、支持Async节点、社区最活跃
- **劣势**：学习曲线较陡，简单任务用LCEL Chain更快
- **典型场景**：需要条件分支的RAG、多轮交互客服、需要人类审批的审计流程
- **2026新特性**：DeepAgents（长时运行任务）、Sandboxes（安全执行Agent生成代码）
- **官方资源**：[LangGraph官网](https://www.langchain.com/langgraph) | [LangGraph Academy教程](https://academy.langchain.com/courses/intro-to-langgraph)

### CrewAI（角色导向，快速原型）
- **定位**：用"角色+任务"隐喻快速搭建多Agent协作
- **优势**：代码可读性强（`Agent(role="研究员", goal="...")`），内置常见工作流模板
- **劣势**：底层仍是顺序执行（Sequential/Hierarchical），缺乏LangGraph的动态路由能力
- **典型场景**：内容生成流水线（研究→写作→编辑）、DevOps自动化（监控→诊断→修复）
- **2026对比**：CrewAI适合"每个步骤都确定要做"的场景，LangGraph适合"根据中间结果决定下一步"

### AutoGen（微软，对话驱动）
- **定位**：通过对话协议让Agent相互通信，底层是Message Passing
- **优势**：支持人类在环（AssistantAgent + UserProxyAgent模式）、GroupChat多Agent讨论
- **劣势**：对话式编排的调试难度高，状态管理不如显式State Schema清晰
- **典型场景**：代码生成+执行反馈循环、需要多Agent辩论/投票的决策系统

### Temporal/Cadence（通用工作流引擎，非AI专用）
- **定位**：Uber的分布式工作流引擎，保证任务最终完成（Exactly-Once语义）
- **与AI Agent结合**：用Temporal编排LLM调用，利用其持久化Timer、重试策略、版本控制
- **典型场景**：需要跨天/跨周的长时任务（如定时生成周报）、金融级容错要求

### n8n/Zapier（无代码/低代码）
- **定位**：图形化工作流编排，节点拖拽连接
- **AI集成**：内置OpenAI/Anthropic节点，可视化搭建Prompt Chain
- **适用人群**：非程序员的运营/市场人员，快速验证想法
- **劣势**：复杂逻辑（如多层嵌套条件）的表达力不如代码

## 4. 工程落地清单

### 前期设计
- [ ] **State Schema设计**：用TypedDict或Pydantic定义所有节点共享的字段（如`messages`, `documents`, `score`）
- [ ] **节点粒度划分**：每个节点单一职责（Retrieve ≠ Retrieve+Grade），便于单测和复用
- [ ] **边的路由逻辑**：条件边（`add_conditional_edges`）的判断函数应简单清晰，避免复杂业务逻辑嵌入
- [ ] **失败模式设计**：哪些节点允许重试？重试几次？超时怎么办？是否需要降级路径？

### 开发阶段
- [ ] **本地Checkpoint测试**：用MemorySaver先验证流程，再切换到SqliteSaver/PostgresSaver
- [ ] **流式输出支持**：如需实时反馈（如打字机效果），确保节点支持`stream_mode="values"`
- [ ] **人类在环集成**：需要审批的节点用`interrupt_before`标记，前端轮询`get_state`拿到暂停点
- [ ] **幂等性保证**：节点被重试时不能产生副作用（如重复发送邮件），用Checkpoint的`metadata`记录"已执行"标记

### 可观测性
- [ ] **LangSmith集成**：自动记录每个节点的输入/输出、耗时、Token使用
- [ ] **图可视化**：用`graph.get_graph().draw_mermaid()`生成Mermaid图，嵌入文档
- [ ] **日志结构化**：记录每次State变更的Diff，便于回溯决策链
- [ ] **告警规则**：监控关键指标（如Retrieval召回率<0.5、某节点耗时>10s）触发告警

### 生产部署
- [ ] **Checkpoint持久化选型**：
  - SQLite：单机POC，<1000次/天调用
  - PostgreSQL：生产环境，支持并发、事务
  - Redis：需要TTL自动清理的临时任务
- [ ] **并发控制**：多个Worker同时处理不同用户请求，Checkpoint的`thread_id`必须隔离
- [ ] **版本管理**：Graph定义变更后，旧Checkpoint如何迁移？建议用`metadata["graph_version"]`标记
- [ ] **成本优化**：长时任务的Checkpoint体积膨胀问题（如存储100轮对话历史），定期归档或仅保留最近N条

### 调试与测试
- [ ] **单元测试**：每个节点函数独立测试，Mock掉LLM调用用固定响应
- [ ] **集成测试**：用固定Seed运行完整Graph，断言最终State
- [ ] **时间旅行调试**：从Checkpoint恢复到任意节点，修改State后重新执行后续节点
- [ ] **A/B测试支持**：相同输入分流到不同Graph版本（如实验新Prompt），对比成功率/延迟

## 5. 实战案例：Strava训练计划Agent（2026年示例）

**场景**：从Strava获取跑步记录 → 分析训练负荷 → 生成下周计划 → 发送邮件

**Graph设计**：
```python
from langgraph.graph import StateGraph
from typing import TypedDict, List

class TrainingState(TypedDict):
    user_id: str
    activities: List[dict]  # Strava数据
    summary: str            # 训练总结
    plan: str               # 下周计划
    email_sent: bool

def fetch_activities(state: TrainingState) -> TrainingState:
    # 调用Strava API
    state["activities"] = get_recent_runs(state["user_id"])
    return state

def analyze_training(state: TrainingState) -> TrainingState:
    # LLM分析训练负荷
    state["summary"] = llm.invoke(f"分析这些跑步数据: {state['activities']}")
    return state

def generate_plan(state: TrainingState) -> TrainingState:
    state["plan"] = llm.invoke(f"基于{state['summary']}生成下周计划")
    return state

def send_email(state: TrainingState) -> TrainingState:
    send_mail(to=state["user_id"], body=state["plan"])
    state["email_sent"] = True
    return state

# 构建Graph
workflow = StateGraph(TrainingState)
workflow.add_node("fetch", fetch_activities)
workflow.add_node("analyze", analyze_training)
workflow.add_node("generate", generate_plan)
workflow.add_node("send", send_email)

workflow.set_entry_point("fetch")
workflow.add_edge("fetch", "analyze")
workflow.add_edge("analyze", "generate")
workflow.add_edge("generate", "send")
workflow.set_finish_point("send")

app = workflow.compile(checkpointer=SqliteSaver("training.db"))
```

**运行**：
```python
result = app.invoke(
    {"user_id": "athlete123"},
    config={"configurable": {"thread_id": "weekly_run"}}
)
```

**关键点**：
- 每周定时触发（用Cron或Temporal）
- Checkpoint保证即使中途失败（如Strava API超时），下次重试从失败节点开始
- 可视化Graph：`workflow.get_graph().draw_mermaid()` 生成流程图供团队Review

## 6. 2026年最佳实践

### 选型决策树
```
需要条件分支/循环？
├─ 是 → LangGraph（复杂场景）或CrewAI（角色明确的简单场景）
└─ 否 → LCEL Chain（线性Pipeline更简单）

需要人类审批？
├─ 是 → LangGraph（interrupt_before）或Temporal（Human Task）
└─ 否 → 任意框架

需要跨天/跨周运行？
├─ 是 → Temporal（原生Timer）或LangGraph + Cron
└─ 否 → LangGraph

团队主要是非程序员？
├─ 是 → n8n/Zapier（拖拽式）
└─ 否 → 代码框架
```

### 反模式警告
- ❌ **过度设计**：3步线性流程不要上Graph，LCEL Chain够用
- ❌ **State过载**：把所有数据都塞State里（如完整文档内容），应该存ID用时再查
- ❌ **隐式依赖**：节点A悄悄依赖State中节点B写入的字段，应该显式声明（用Pydantic的Field描述）
- ❌ **边的副作用**：路由函数（`conditional_edges`的判断函数）不应修改State，仅返回下一个节点名

### 可观测性标准
- 每个Graph运行必须有唯一`run_id`（关联到用户请求）
- 关键节点的输入/输出必须记录到LangSmith或自建日志系统
- 生产环境必须监控：平均执行时长、P95延迟、失败率、Checkpoint存储用量

## 7. 更新记录

| 日期 | 更新内容 |
|------|---------|
| 2026-05-26 | 补充LangGraph 2026特性、CrewAI/AutoGen对比、Strava实战案例、工程落地清单 |
| 2026-04-20 | 创建骨架 |
