---
title: AI Agent架构
date: 2026-04-14
tags:
  - AI-Agent
  - 架构
  - LLM
  - 入门
---

# AI Agent架构

> 如果你是.NET开发者，这篇文章用你熟悉的概念帮你快速建立AI Agent的心智模型。
> 相关深入章节：[[4.1-AI_Agent核心心智模型]] | [[4.2-Agent框架对比]]

---

## 一、核心类比：Agent就是一个.NET应用程序

在.NET世界里，一个应用程序由运行时(CLR)、数据存储(SQL Server)、依赖注入(DI)的服务接口组成。AI Agent的架构惊人地相似：

| .NET概念 | Agent对应概念 | 职责 |
|---|---|---|
| CLR（公共语言运行时） | LLM（大语言模型） | 核心推理引擎，负责"思考" |
| SQL Server / MemoryCache | Memory（记忆系统） | 长期持久化 / 短期上下文缓存 |
| DI注册的接口(IService) | Tools（工具集） | 外部能力的标准化接入点 |
| ASP.NET管道中间件 | Workflow（工作流） | 控制请求处理的流转顺序 |
| AppDomain / 进程隔离 | Sandbox（沙箱） | 隔离执行不受信任的代码 |

### 1.1 LLM = CLR

CLR负责把IL编译成机器码并执行。LLM负责把自然语言"编译"成推理步骤并执行。

关键区别：CLR是确定性的——同样的IL永远产生同样的结果。LLM是概率性的——同样的Prompt可能产生不同输出。这是Agent工程中大量"防御性编程"的根源。

```
// .NET: CLR执行IL
var result = MyMethod(input);  // 确定性

// Agent: LLM执行Prompt
var result = await llm.Complete(prompt);  // 概率性，需要验证
```

### 1.2 Memory = SQL Server + MemoryCache

Agent的记忆分两层，和.NET应用的数据架构一模一样：

**短期记忆 = MemoryCache / Session State**
- 当前对话的上下文窗口（Context Window）
- 类似HttpContext.Session，请求结束就没了
- 受限于token上限（相当于内存上限）

**长期记忆 = SQL Server / 向量数据库**
- 历史对话、知识文档持久化存储
- 通过RAG（检索增强生成）按需加载
- 类似EF Core查询数据库，只拉需要的数据到内存

```csharp
// .NET类比
var cached = _memoryCache.Get<string>("current_context");  // 短期
var history = await _dbContext.Conversations
    .Where(c => c.UserId == userId)
    .OrderByDescending(c => c.Time)
    .Take(10).ToListAsync();  // 长期
```

### 1.3 Tools = DI接口

在.NET中，你通过DI注册`IEmailService`、`IPaymentGateway`等接口，业务代码不关心实现细节。

Agent的Tools完全一样——LLM只看到工具的"接口声明"（名称、描述、参数Schema），不关心背后是调API还是查数据库。

```csharp
// .NET DI注册
services.AddScoped<IWeatherService, OpenWeatherService>();

// Agent工具声明（JSON Schema）
{
  "name": "get_weather",
  "description": "查询指定城市的天气",
  "parameters": {
    "type": "object",
    "properties": {
      "city": { "type": "string", "description": "城市名称" }
    }
  }
}
```

LLM看到工具声明后，就像你的Controller通过构造函数注入拿到接口一样——它知道能调什么、怎么调、参数是什么。

工具声明的质量直接决定Agent表现。把它当成API文档来写，参数尽量用enum约束。

---

## 二、Agent的三大关键能力

### 2.1 思考规划（Reasoning & Planning）

这是Agent区别于普通ChatBot的核心能力。

**ReAct模式（2022, Yao et al.）**

至今仍是主流范式。核心循环：Thought → Action → Observation → Thought → ...

```
用户：帮我查一下北京明天天气，如果下雨就提醒我带伞

Thought: 需要先查北京明天的天气
Action: get_weather(city="北京", date="明天")
Observation: 多云转小雨，气温15-22°C

Thought: 明天有小雨，需要提醒用户带伞
Action: send_reminder(message="明天北京有小雨，记得带伞！")
Observation: 提醒已发送

Thought: 任务完成
Final Answer: 已查询到北京明天多云转小雨(15-22°C)，已发送带伞提醒。
```

类比.NET：这就像一个`while`循环里不断调用service方法，每次根据返回值决定下一步。

ReAct的演进版本：
- **ReWOO**：先一次性规划所有步骤，再批量执行，减少LLM调用次数（类似批量SQL vs 逐条查询）
- **Reflexion**：执行失败后自我反思并重试（类似Polly重试策略+日志分析）

**Plan-and-Execute模式**

2025年复杂任务的首选。先生成完整计划，再逐步执行，执行中可动态调整计划。

```
// 类比：这像是先写了一个详细的技术方案文档，再按方案逐步实施
Plan:
  1. 分析用户需求 → 确定查天气+条件提醒
  2. 调用天气API
  3. 判断是否下雨
  4. 如果是，发送提醒
  5. 汇总结果

Execute: 逐步执行，每步完成后评估是否需要调整计划
```

LangGraph v0.2+ 原生支持Plan-and-Execute，内置`PlanExecute`图模板。

### 2.2 工具调用（Tool Use）

工具调用是Agent的"手脚"。没有工具的Agent就像一个只能说不能做的顾问。

**调用流程：**

```
用户输入 → LLM分析 → 决定调用哪个工具 → 生成参数JSON
    → 框架执行工具 → 返回结果 → LLM整合结果 → 回复用户
```

关键点：
- LLM**不执行**工具，它只**生成**调用指令（像Controller只调Service接口，不管实现）
- 框架负责实际执行（像DI容器负责解析和实例化）
- 工具返回值回到LLM的上下文中，供后续推理使用

工具标准化协议：**[[MCP规范]]**（Model Context Protocol）正在成为行业标准，详见专题文章。

### 2.3 工作流控制（Workflow Orchestration）

单步工具调用只是基础。真正的Agent需要编排复杂的多步骤流程。

Anthropic在2025年1月发布的*Building Effective Agents*中定义了5种核心模式：

| 模式 | .NET类比 | 适用场景 |
|---|---|---|
| Prompt Chaining | 中间件管道(Pipeline) | 顺序处理，前一步输出是后一步输入 |
| Routing | MVC路由/策略模式 | 根据输入类型分发到不同处理器 |
| Parallelization | Task.WhenAll | 多个独立子任务并行执行 |
| Orchestrator-Workers | 主从架构/Hangfire Job | 主Agent分解任务，Worker Agent分头执行 |
| Evaluator-Optimizer | 单元测试+重构循环 | 一个Agent生成，另一个评估，迭代优化 |

详细模式解析见 **[[Workflow设计模式]]**。

---

## 三、主流Agent框架（2025-2026）

### 3.1 LangGraph v0.2+

LangChain团队出品，有状态循环Agent图。

核心思想：把Agent建模为**有向图**——节点是函数或子Agent，边是条件路由，状态在节点间流转。

```python
from langgraph.graph import StateGraph

graph = StateGraph(AgentState)
graph.add_node("planner", plan_step)
graph.add_node("executor", execute_step)
graph.add_node("reviewer", review_step)
graph.add_conditional_edges("reviewer", should_continue,
    {"continue": "executor", "end": END})
```

.NET类比：这就像用Durable Functions编排工作流，每个Activity Function是一个节点。

### 3.2 OpenAI Agents SDK（2025.3）

替代之前实验性的Swarm项目。三个核心抽象：

- **Agent**：带指令和工具的LLM配置（类似一个配置好的Controller）
- **Handoffs**：Agent之间的任务交接（类似请求转发/路由）
- **Guardrails**：输入输出校验（类似FluentValidation）

同期发布的Responses API支持内置工具：`web_search`、`file_search`、`computer_use`。

### 3.3 CrewAI v0.100+

20k+ GitHub Stars。特色是**角色化多Agent**——你定义Agent的角色(Role)、目标(Goal)、背景(Backstory)，它们像一个团队协作完成任务。

```python
researcher = Agent(
    role="高级研究员",
    goal="找到关于AI Agent的最新技术趋势",
    backstory="你是一个有10年经验的AI研究员...",
    tools=[search_tool, wiki_tool]
)
```

.NET类比：每个Agent像一个微服务，有自己的职责边界，通过消息通信协作。

### 3.4 AutoGen v0.5

微软出品，核心是AgentChat API，支持异步多Agent对话。

特色：Agent之间可以像群聊一样交流，支持人类参与(Human-in-the-Loop)。

### 3.5 Claude生态

- **Claude computer_use**：GUI-Agent，能操作鼠标键盘控制桌面应用
- **Claude Code**：CLI Agent，2025年初发布，直接在终端中进行代码开发

---

## 四、从Augmented LLM到Agent的渐进路径

Anthropic的建议（也是实践中验证有效的）：**不要一上来就搞复杂Agent，从增强型LLM开始。**

```
Level 0: 纯LLM对话（ChatBot）
    ↓ 加检索
Level 1: RAG增强（LLM + 知识库检索）
    ↓ 加工具
Level 2: Tool-Augmented LLM（LLM + 工具调用）
    ↓ 加循环
Level 3: ReAct Agent（LLM + 工具 + 思考循环）
    ↓ 加规划
Level 4: Plan-and-Execute Agent（规划 + 执行 + 反思）
    ↓ 加协作
Level 5: Multi-Agent系统（多Agent协作/竞争）
```

这和.NET开发一样——不要一开始就上微服务，先单体跑通，再按需拆分。

---

## 五、Agent开发的"防御性编程"

LLM的概率性意味着你需要更多防护措施：

| 风险 | 防护手段 | .NET类比 |
|---|---|---|
| LLM输出格式错误 | 结构化输出(JSON Mode) + 重试 | 强类型 + try-catch |
| 工具调用参数错误 | JSON Schema验证 + 参数约束 | FluentValidation |
| 无限循环 | max_iterations限制 | CancellationToken + Timeout |
| Token爆炸 | 上下文窗口管理 + 摘要压缩 | 内存池 + GC |
| 幻觉/错误推理 | RAG事实锚定 + 人工审核 | 集成测试 + Code Review |
| 成本失控 | 小模型routing + 大模型推理 | 缓存策略 + 读写分离 |

---

## 六、快速上手建议

1. **选一个框架**：入门推荐LangGraph（文档好、社区大），企业场景考虑OpenAI Agents SDK
2. **从单Agent开始**：一个ReAct Agent + 2-3个工具，解决一个具体问题
3. **工具声明花心思**：描述写清楚，参数用enum，像写好的API文档
4. **加监控**：OpenAI Agents SDK内置Tracing，LangGraph用LangSmith，这是你的Application Insights
5. **控制成本**：设token上限，用小模型做路由分发，大模型只处理核心推理
6. **看实战案例**：[[SWE-Agent实战]] 是一个完整的Agent应用分析

---

## 相关文章

- [[MCP规范]] - Agent工具调用的标准化协议
- [[Workflow设计模式]] - Agent工作流编排的5种核心模式
- [[SWE-Agent实战]] - 软件工程Agent的实际应用与Benchmark
- [[4.1-AI_Agent核心心智模型]] - 更深入的Agent理论模型
- [[4.2-Agent框架对比]] - LangGraph/CrewAI/AutoGen详细对比

---

## 更新日志

| 日期 | 内容 |
|---|---|
| 2026-04-08 | 初始骨架：核心类比、关键能力、双链结构 |
| 2026-04-14 | 填充完整内容：ReAct/Plan-and-Execute模式、5种Anthropic模式、主流框架对比、防御性编程、渐进路径 |
