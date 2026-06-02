---
title: Agent 编排框架横评 — SK / Agent Framework / LangChain / 多 Agent 编排（2026-06）
created: 2026-06-02
updated: 2026-06-02
type: comparison
tags: [agent, research, comparison]
status: stable
sources: [https://learn.microsoft.com, https://microsoft.github.io/semantic-kernel, https://microsoft.github.io/autogen, https://langchain-ai.github.io/langgraph, https://docs.crewai.com, https://openai.github.io/openai-agents-python, https://github.com]
---

# Agent 编排框架横评（2026-06）

> 专题：多 Agent 编排框架的技术细节、点评与选型。覆盖微软系（Semantic Kernel / AutoGen / Microsoft Agent Framework）、LangChain 系（LangChain / LangGraph）、以及主流对照（CrewAI / OpenAI Agents SDK / LlamaIndex Workflows）。
> 配套阅读：[[40-调研报告/agent/2026-06-微软Agent全景与战略点评.md|微软 AI Agent 全景与战略点评]]
> Star 数为匿名 GitHub API 实时值（2026-06-02）。版本/发布日期为官方文档实测，标注「待确认」者为第三方源。

---

## 0. TL;DR — 一张表选型

按**编排范式**分四类，这是理解整个赛道的主轴：

- **Graph（状态图）**：LangGraph、MAF Workflows — 显式 node/edge/state，可控、可复现、支持循环/分支/断点续跑。复杂有状态编排的事实标准。
- **Conversation（对话驱动）**：AutoGen、OpenAI Agents SDK(handoff) — agent 用消息相互协商，灵活但确定性弱。
- **Role（角色扮演）**：CrewAI — Agent 配 role/goal/backstory，比喻贴近现实团队，上手最快。
- **Event（事件驱动）**：LlamaIndex Workflows — step 消费/发射 event，天然适配 RAG 流水线。

**一句话选型**：
- 微软栈/.NET 生产 → **MAF**（新项目）或 **SK**（已有系统、要 Java）
- 复杂有状态、要循环/HITL/断点 → **LangGraph**
- OpenAI 生态、要轻量快速原型 → **OpenAI Agents SDK**
- 多角色业务流程、团队式分工 → **CrewAI**
- RAG-heavy、文档密集 → **LlamaIndex Workflows**

---

## 1. Star 数与活跃度（2026-06-02 实测）

- langchain-ai/langchain — **138.3k** ★ / 22.9k fork（langchain-core 1.4.0）
- AutoGen `microsoft/autogen` — **58.6k** ★ / 8.9k fork（已进维护模式）
- CrewAI `crewAIInc/crewAI` — **52.7k** ★ / 7.3k fork
- LlamaIndex `run-llama/llama_index` — **49.8k** ★
- LangGraph `langchain-ai/langgraph` — **33.6k** ★ / 5.7k fork（v1.2.3）
- Semantic Kernel `microsoft/semantic-kernel` — **28.0k** ★ / 4.6k fork（维护模式，仍 push）
- OpenAI Agents SDK `openai/openai-agents-python` — **26.8k** ★ / 4.1k fork
- OpenAI Swarm `openai/swarm` — **21.6k** ★（教育性质，已被 Agents SDK 取代，停更）
- MAF `microsoft/agent-framework` — **11.0k** ★ / 1.8k fork（2025-04 开仓，增长最猛，今日仍 push）

> 解读：LangChain 体量断层第一（生态总入口）。AutoGen star 高但已停止主投入。MAF 开仓一年破万、增速最快，是微软的未来押注。

---

## 2. 微软系：SK → AutoGen → MAF 三代演进

### 时间线
```
2023-02  Semantic Kernel 开源（企业级 SDK，C#/Python/Java）
2023-08  AutoGen 开源（MS Research，研究导向多 agent）
2024     AutoGen v0.4 架构重写（event-driven actor runtime）
2025-04  agent-framework repo 创建
2025-10-01  MAF 公开 Public Preview —— SK + AutoGen 合并
            SK 与 AutoGen 同时进入 maintenance mode
~2026 Q1  MAF 目标 GA（社区信息，待官方确认）
```

### Semantic Kernel (SK)
- **定位**：轻量、企业级 SDK，把 LLM 集成进现有 App，强调 trust & stability（生产可信稳定）。
- **核心抽象**：Kernel（中央 DI 容器）/ Plugins（原 Skills，封装可被 LLM 调用的 native + prompt functions）/ Planners（让 LLM 自动编排 plugins，后期逐步被 function calling 取代）/ Memory（向量检索语义记忆）。
- **语言**：**C#/.NET（最成熟）、Python、Java** —— 唯一支持 Java 的微软框架。
- **现状**：**维护模式**。新投入转 MAF，但官方承诺继续支持。企业特性（session 管理、type safety、filters/middleware、telemetry）被 MAF 完整继承。

### AutoGen
- **定位**：MS Research 起家的**研究导向**多 agent 框架，社区驱动。
- **核心抽象**：ConversableAgent（可对话 agent 基类）/ GroupChat + GroupChatManager（多 agent 群聊，manager 决定发言顺序）/ Magentic-One（通用多 agent 系统：WebSurfer/FileSurfer/Coder/ComputerTerminal）。
- **v0.2 → v0.4**：彻底重写，转向**事件驱动 actor 模型 runtime**，异步、可扩展、可观测，分层（core/agentchat/extensions）。
- **AutoGen Studio**：低代码可视化 GUI，原型设计 + 调试。
- **现状**：与 SK 一同进入**维护模式**，能力被 MAF 吸收。

### Microsoft Agent Framework (MAF)
- **发布**：**2025-10-01 Public Preview**（repo 早于 2025-04 创建）。目前**仍是 Preview**（pip 需 `--pre`，.NET 需 `--prerelease`）。GA 目标 2026 Q1（第三方源，**官方未确认**）。
- **合并定位**（官方原话）：combines the agent abstractions from **AutoGen** with the enterprise features from **Semantic Kernel**。即：
  - 取 AutoGen → 简洁单/多 agent 抽象、动态编排
  - 取 SK → session 状态、type safety、middleware、telemetry、企业生产特性
  - 加 **Microsoft.Extensions.AI** 统一开发体验
  - **新增** → graph-based workflows + 长任务/HITL 的健壮状态管理
- **语言**：**Python 3.10+ / .NET 8.0+**（**无 Java** —— 这是与 SK 的关键差异，要 Java 留 SK）。MIT License。
- **核心抽象**：AI Agents（ChatAgent/AzureAIAgent/OpenAIAssistantAgent，支持 Foundry/OpenAI/Azure OpenAI/Anthropic/Ollama）/ Agent Threads（状态可持久化 Redis、Cosmos DB）/ Workflows（graph-based，type-safe routing、checkpointing、HITL）/ Context providers / Middleware / MCP clients。
- **开放标准**：原生 **MCP / A2A / OpenAPI**，深度集成 Azure AI Foundry。
- **五种内置编排**：Sequential（流水线）/ Concurrent（并行聚合）/ Group Chat（facilitator 选发言）/ Handoff（按上下文转交，适合客服分诊）/ Magentic-One（orchestrator + worker，维护 Task/Progress Ledger，适合开放式复杂问题，但协调开销大、不适合低延迟）。
- **迁移**：官方提供 from SK 和 from AutoGen 两份迁移指南，推荐新项目直接用 MAF。

**点评**：微软用 MAF 收编了自己分裂的两条线（研究派 AutoGen + 工程派 SK），战略清晰——把 AutoGen 的灵活编排装进 SK 的企业级外壳。代价是生态短期割裂（老项目迁移成本、Java 暂时掉队、Preview 期 API 不稳）。对微软栈用户是必然方向，但**现在压生产要掂量 Preview 风险**。

---

## 3. LangChain 系：组件 + 编排 + 运维三件套

### 分工（官方明确）
**LangChain 做组件（model/tool/retriever 抽象与集成），LangGraph 做编排，LangSmith 做可观测与部署。** LangChain 是"积木"，LangGraph 是"结构图"。

### LangChain
- **核心抽象**：Chains（LCEL/Runnable 串流水线）/ Tools（外部能力统一封装）/ Agents（LLM 自主选 tool）。langchain-core 已进 **1.x 稳定版**。
- **AgentExecutor 的历史局限**：旧 `AgentExecutor` 是封闭 while 循环（think→act→observe），控制流被框架硬编码，**难自定义分支/回退/循环/状态共享/人工介入**，可控性差。这正是 LangGraph 诞生的动因。

### LangGraph
- **核心抽象**：
  - **StateGraph**：主图类，用前必须 `compile()`（校验结构 + 注入 checkpointer/breakpoint）。
  - **State**：贯穿全图的共享数据，**首选 `TypedDict`**。每个 key 可配 **reducer**（如 `add_messages`、`operator.add`）控制更新是覆盖还是聚合。
  - **Node**：编码 agent 逻辑的函数，收 state → 算 → 返回 state 更新。
  - **Edge**：决定下一步。**conditional edge** 按运行时 state 动态路由。官方总结："Nodes do the work, edges tell what to do next."
  - **执行模型**：借鉴 Google **Pregel** message passing，按 super-step 离散推进。
- **为什么用图**：图天然表达 branching / cycle / retry / persistence / HITL —— 2026 生产级 agent 的刚需，primitives 一一对应（HITL = 一个 `interrupt` 节点 + 读 resume payload 的 conditional edge）。
- **关键能力**：Cycle 一等公民（旧 chain 做不到）/ Checkpointing 持久化（暂停-恢复，长跑+故障恢复）/ HITL（`interrupt` + breakpoint）/ Streaming。
- **多 agent 模式**：Supervisor（中心协调，最常用）/ Swarm（无中心 handoff）/ Hierarchical teams（supervisor 嵌套，复杂大任务）。官方另有 `langgraph-supervisor`、`langgraph-swarm` 预制库。

### 图 vs 对话（LangGraph vs AutoGen 本质区别）
- **LangGraph = 显式状态机**：控制流由开发者用 node/edge 精确定义，**可控、可复现、可调试**，状态在共享 TypedDict 流动。
- **AutoGen = 对话式**：agent 用自然语言消息协商，控制流隐式涌现，更灵活但**确定性弱**。
- 本质：LangGraph 把编排**外化为图结构**，AutoGen 把编排**内化为对话**。

### 商业化与采用
- **LangSmith**：可观测 + 调试 + 评估平台（tracing/eval/A-B/成本追踪）。2025 年底重定位为"agent engineering platform"，新增 **LangSmith Fleet**（无代码 agent 构建，2026-01 GA）。
- **LangGraph Platform → 现 LangSmith Deployment**：生产级托管部署，内置 persistence/task queue/cron/durability/HITL/memory/streaming/Studio，已 GA，上架 AWS Marketplace。
- **公司**：51–200 人，**2025-11 Series B 融资 1.25 亿美元**。
- **生产案例**：LinkedIn（SQL Bot）/ Uber（代码迁移 agent）/ Klarna（客服）/ Elastic（安全检测）。

**点评**：LangChain 系是目前生态最完整的栈——从原型（LangChain）到编排（LangGraph）到运维（LangSmith）闭环。LangGraph 的图范式在"复杂有状态编排"上是事实标准。槽点是早期 LangChain 抽象层层叠叠被诟病"过度封装"，但 1.x + LangGraph 已大幅收敛。

---

## 4. 主流对照：CrewAI / OpenAI Agents SDK / LlamaIndex Workflows

### CrewAI（role 范式）
- **核心抽象**：Crew（团队）/ Agent（带 role/goal/backstory）/ Task / Process。
- **Process 两模式**：Sequential（顺序，数据经 context 流转）/ Hierarchical（需 `manager_llm` 或 `manager_agent`，由 manager 自动委派调度，类 orchestrator-worker）。
- **核心卖点**：**完全独立于 LangChain**（"built from scratch, completely independent of LangChain"），主打无依赖、更快更轻。
- **商业**：OSS + CrewAI Enterprise（Control Plane / 托管 / 可观测）。
- **上手**：中偏低，角色比喻直观；但 hierarchical 调试、agent 委派不确定性较高。

### OpenAI Agents SDK（conversation/handoff 范式）
- **演进**：实验性 Swarm（教育框架）→ production-ready 正式 SDK。
- **核心抽象**：Agent（LLM+instructions+tools+handoffs+guardrails）/ handoffs（任务移交，也支持 agents-as-tools）/ guardrails（输入输出护栏）/ sessions（状态）/ Runner（管 turn 循环、工具、handoff、session）。
- **与 Responses API 关系**：SDK 对 OpenAI 模型**默认走 Responses API**，是其上的编排封装层。想自己掌控循环就直接用 Responses API。
- **定位**：lightweight，极简少抽象，学习曲线**最低**。内置原生 tracing。

### LlamaIndex Workflows（event 范式）
- **核心抽象**：step（步骤）消费并 emit event（事件），async 驱动，主打高速 + 易集成 FastAPI。
- **与 RAG 结合**：天然优势区——把 retrieval/rerank/synthesis 拆成独立 step 构建 event-driven RAG；配 LlamaParse 做 Agentic Document Workflows。
- **商业**：Workflows 完全开源，商业化靠 LlamaParse / LlamaCloud（文档解析企业平台）。

### 跨框架对比维度
- **编排范式**：CrewAI=role / OpenAI SDK=conversation+handoff / LlamaIndex=event / LangGraph=graph / MAF=graph+5模式 / AutoGen=conversation
- **语言**：CrewAI=Python(JS社区) / OpenAI SDK=Python(+JS/TS) / LlamaIndex=Python / LangGraph=Python+JS/TS / SK=C#/Py/Java / MAF=Py/.NET
- **学习曲线**：OpenAI SDK 最低 < CrewAI ≈ LlamaIndex < LangGraph ≈ MAF
- **生产就绪**：均高（各有 checkpoint/持久化/企业版/官方背书）
- **可观测**：CrewAI=telemetry+Enterprise / OpenAI=原生 tracing / LlamaIndex=可视化 / LangGraph=LangSmith / MAF=Dev UI
- **适用**：CrewAI=多角色业务流程 / OpenAI SDK=OpenAI 生态轻量 agent / LlamaIndex=RAG/文档密集 / LangGraph=复杂有状态控制流 / MAF=微软栈生产

---

## 5. 2026 赛道趋势判断

1. **标准化先于框架收敛**：MCP（工具/上下文标准）被各框架普遍内置（CrewAI 已设独立 MCP 章节，MAF 原生支持），从私有协议走向统一。A2A（agent 间互操作）推进中但成熟度低于 MCP。**协议层标准化跑在框架收敛前面。**

2. **框架未收敛，而是范式分化共存**：四大框架 star 都在 2.6万–5.3万量级，各锚定不同范式（role/conversation/event/graph）和生态，短期"分赛道共存"而非赢家通吃。

3. **graph 范式赢下"复杂有状态编排"细分**：LangGraph + MAF Workflows 代表的图/状态机范式在需要循环、分支、持久化、可恢复的复杂 agent 上是事实标准；但角色范式（CrewAI）、极简对话范式（OpenAI）在各自场景仍领先。**graph 赢的是细分，不是整个赛道。**

4. **隐性收敛点在底层 API 而非框架**：OpenAI Responses API 成为编排底座（Agents SDK 即其封装），收敛更可能发生在**模型 API/协议层**，框架层继续百花齐放。

---

## 关联阅读
- [[40-调研报告/agent/2026-06-微软Agent全景与战略点评.md|微软 AI Agent 全景与战略点评（2026-06）]] —— 微软 Copilot/Foundry/产品线全景
- [[40-调研报告/agent/2026-05-多Agent跨设备互联方案调研.md|多 Agent 跨设备互联方案调研]]
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.2.1-LangGraph深度实操.md|LangGraph 深度实操]]

---

> **可信度说明**：Star/版本/创建时间均为 GitHub API 实测。各框架核心抽象、定位、Process/handoff/step 机制来自官方文档。MAF GA 日期（2026 Q1）、CrewAI Enterprise 模块明细、A2A 成熟度为第三方/综合信息，标注待确认。趋势判断为分析推断。
