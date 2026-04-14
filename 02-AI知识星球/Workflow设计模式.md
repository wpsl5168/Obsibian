---
title: Workflow设计模式
date: 2026-04-14
tags:
  - Workflow
  - 设计模式
  - LangGraph
  - 入门
---

# Workflow设计模式

> 用Windows Workflow Foundation(WF)和Azure Durable Functions的概念来理解AI Agent工作流。
> 相关深入章节：[[4.4-Workflow编排实践]] | [[AI-Agent架构]]

---

## 一、为什么需要Workflow？

单个LLM调用就像一个简单的`Console.WriteLine("Hello")`——能用，但做不了复杂业务。

真实场景需要：
- **多步骤顺序执行**（先查数据，再分析，再生成报告）
- **条件分支**（如果是bug就修复，如果是feature就设计）
- **并行处理**（同时查3个数据源，汇总结果）
- **循环重试**（结果不满意就重做，最多3次）
- **人工审批**（关键操作需要人确认）

这和.NET世界里为什么需要Workflow引擎的原因一模一样。

### .NET类比全景

| AI Workflow概念 | .NET类比 |
|---|---|
| 工作流定义 | WF的.xaml / Durable Functions的Orchestrator |
| 节点(Node) | WF的Activity / Durable Functions的Activity Function |
| 状态传递 | WF的Variable / Orchestrator的输入输出 |
| 条件路由 | WF的FlowDecision / if-else in Orchestrator |
| 并行执行 | WF的Parallel / Task.WhenAll in Durable Functions |
| 持久化 | WF的InstanceStore / Durable Functions的Table Storage |
| Human-in-the-Loop | WF的Bookmark / Durable Functions的WaitForExternalEvent |

---

## 二、Anthropic五种核心模式

Anthropic在2025年1月发布的*Building Effective Agents*博客中系统总结了5种Workflow模式。这是目前最权威的分类框架。

### 2.1 Prompt Chaining（提示链）

**一句话：前一步的输出是后一步的输入，像流水线。**

```
[步骤1: 提取需求] → [步骤2: 生成代码] → [步骤3: 代码审查] → [步骤4: 生成测试]
```

.NET类比：ASP.NET中间件管道，每个中间件处理Request后传给下一个。

```csharp
// .NET中间件管道
app.UseAuthentication()    // 步骤1
   .UseAuthorization()     // 步骤2
   .UseRouting()           // 步骤3
   .UseEndpoints(...)      // 步骤4
```

```python
# LangGraph实现Prompt Chaining
graph = StateGraph(State)
graph.add_node("extract", extract_requirements)
graph.add_node("generate", generate_code)
graph.add_node("review", review_code)
graph.add_node("test", generate_tests)

graph.add_edge("extract", "generate")
graph.add_edge("generate", "review")
graph.add_edge("review", "test")
graph.add_edge("test", END)
graph.set_entry_point("extract")
```

**适用场景**：任务可以明确分解为固定顺序的步骤，每步都有清晰的输入输出。

**关键技巧**：步骤之间可以加"门控"(Gate)——检查上一步输出质量，不合格就重做或终止。就像中间件里的短路逻辑。

### 2.2 Routing（路由分发）

**一句话：根据输入类型，分发到不同处理器。**

```
              ┌─→ [技术问题处理器]
[输入分类] ──┼─→ [商务咨询处理器]
              └─→ [投诉处理器]
```

.NET类比：MVC的路由系统，或者策略模式(Strategy Pattern)。

```csharp
// .NET策略模式
public interface IQueryHandler { Task<string> Handle(string query); }

// 路由
var handler = query.Category switch
{
    "technical" => _techHandler,
    "business"  => _bizHandler,
    "complaint" => _complaintHandler,
    _ => _defaultHandler
};
return await handler.Handle(query);
```

```python
# LangGraph条件路由
def route_query(state):
    category = classify(state["query"])  # 用小模型分类
    return category  # 返回路由目标

graph.add_conditional_edges("classifier", route_query, {
    "technical": "tech_agent",
    "business": "biz_agent",
    "complaint": "complaint_agent"
})
```

**成本优化关键**：用小模型（如GPT-4o-mini）做路由分类，大模型（如Claude Opus）只处理核心推理。就像.NET里用Redis做缓存路由，SQL Server只处理必要查询。

### 2.3 Parallelization（并行化）

**一句话：多个独立子任务同时执行，汇总结果。**

两种变体：
- **Sectioning（分区）**：同一输入，不同角度并行处理
- **Voting（投票）**：同一任务，多个Agent独立执行，取多数结果

```
                ┌─→ [安全审查Agent] ──┐
[代码提交] ────┼─→ [性能审查Agent] ──┼──→ [汇总结果]
                └─→ [风格审查Agent] ──┘
```

.NET类比：`Task.WhenAll` + 结果聚合。

```csharp
// .NET并行
var securityTask = _securityReviewer.ReviewAsync(code);
var perfTask = _perfReviewer.ReviewAsync(code);
var styleTask = _styleReviewer.ReviewAsync(code);

await Task.WhenAll(securityTask, perfTask, styleTask);

var summary = Aggregate(
    securityTask.Result, perfTask.Result, styleTask.Result);
```

LangGraph原生支持**Map-Reduce并行**：对一个列表的每个元素并行执行同一节点，然后Reduce汇总。

```python
# LangGraph Map-Reduce（概念示例）
graph.add_node("review_file", review_single_file)  # 对每个文件并行执行
graph.add_node("aggregate", aggregate_reviews)       # 汇总所有审查结果
```

### 2.4 Orchestrator-Workers（编排者-工人）

**一句话：主Agent分解任务，Worker Agent分头执行，主Agent汇总。**

```
[用户需求] → [Orchestrator Agent]
                  │
                  ├─→ [Worker 1: 后端开发] → 结果
                  ├─→ [Worker 2: 前端开发] → 结果
                  └─→ [Worker 3: 测试编写] → 结果
                  │
              [Orchestrator汇总]
              → [最终交付]
```

.NET类比：Hangfire的Job编排，或者主从架构——一个Coordinator分配任务给多个Worker。

```csharp
// .NET类比：Hangfire批量Job
var batchId = BatchJob.StartNew(batch =>
{
    batch.Enqueue<BackendWorker>(w => w.Develop(spec));
    batch.Enqueue<FrontendWorker>(w => w.Develop(spec));
    batch.Enqueue<TestWorker>(w => w.WriteTests(spec));
});

BatchJob.ContinueBatchWith(batchId,
    batch => batch.Enqueue<Coordinator>(c => c.Integrate()));
```

与Parallelization的区别：Orchestrator-Workers中，**子任务是动态生成的**，主Agent根据具体问题决定需要几个Worker、做什么。Parallelization的分支是预定义的。

这是CrewAI的核心模式——定义角色化的Agent团队，Manager Agent动态分配任务。

### 2.5 Evaluator-Optimizer（评估者-优化者）

**一句话：一个Agent生成，另一个Agent评估，不合格就重做。**

```
[Generator Agent] ──→ [Evaluator Agent]
       ↑                     │
       │     不合格+反馈      │
       └─────────────────────┘
              合格 ↓
          [最终输出]
```

.NET类比：单元测试驱动的开发循环——写代码 → 跑测试 → 测试失败 → 改代码 → 再跑测试。

```csharp
// .NET类比
string code;
TestResult result;
int attempts = 0;

do
{
    code = await _generator.GenerateCode(spec, result?.Feedback);
    result = await _evaluator.RunTests(code);
    attempts++;
} while (!result.Passed && attempts < MAX_ATTEMPTS);
```

**关键**：必须设`max_iterations`防止无限循环。就像设置`CancellationToken`的Timeout一样重要。

---

## 三、LangGraph：Workflow的实现引擎

LangGraph（v0.2+）是目前最主流的Agent Workflow实现框架。核心抽象：**有向图（Directed Graph）**。

### 3.1 核心概念映射

| LangGraph | WF / Durable Functions | 说明 |
|---|---|---|
| StateGraph | WorkflowDefinition / Orchestrator | 工作流定义 |
| Node | Activity | 执行单元，一个函数或一个Agent |
| Edge | FlowStep.Next | 节点间的连接 |
| Conditional Edge | FlowDecision | 条件分支路由 |
| State | WorkflowVariable | 在节点间流转的状态对象 |
| Checkpointer | InstanceStore / Table Storage | 状态持久化 |
| Subgraph | 子工作流 / Sub-Orchestrator | 嵌套的子流程 |

### 3.2 状态管理

LangGraph的State是一个TypedDict，所有节点共享和修改同一个状态对象。

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # 消息列表，自动追加
    plan: str                                 # 当前计划
    iteration: int                            # 迭代次数
    final_answer: str                         # 最终答案
```

.NET类比：这就是Durable Functions中Orchestrator传递给每个Activity的上下文对象。

```csharp
// Durable Functions类比
[FunctionName("AgentOrchestrator")]
public async Task<AgentState> Run(
    [OrchestrationTrigger] IDurableOrchestrationContext context)
{
    var state = context.GetInput<AgentState>();
    state = await context.CallActivityAsync<AgentState>("Plan", state);
    state = await context.CallActivityAsync<AgentState>("Execute", state);
    state = await context.CallActivityAsync<AgentState>("Review", state);
    return state;
}
```

### 3.3 条件路由与循环

LangGraph原生支持循环——这是它相比简单DAG框架的核心优势。

```python
def should_continue(state: AgentState) -> str:
    if state["iteration"] >= 3:
        return "end"              # 达到最大迭代，强制结束
    if state["quality_score"] > 0.8:
        return "end"              # 质量达标，正常结束
    return "retry"                # 继续迭代

graph.add_conditional_edges("evaluator", should_continue, {
    "retry": "generator",         # 循环回去重新生成
    "end": "output"               # 输出最终结果
})
```

.NET类比：这就是`do-while`循环加退出条件，和Durable Functions的`ContinueAsNew`模式一样。

### 3.4 Subgraph嵌套

复杂Workflow可以拆分为多个子图，像.NET中的子工作流。

```python
# 子图：代码审查流程
review_subgraph = StateGraph(ReviewState)
review_subgraph.add_node("security_check", security_check)
review_subgraph.add_node("style_check", style_check)
# ... 构建子图

# 主图中引用子图
main_graph = StateGraph(MainState)
main_graph.add_node("develop", develop_code)
main_graph.add_node("review", review_subgraph.compile())  # 嵌入子图
main_graph.add_node("deploy", deploy)
```

### 3.5 Human-in-the-Loop（人在回路中）

关键操作需要人工确认。

```python
from langgraph.checkpoint.memory import MemorySaver

# 使用checkpointer持久化状态
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer, interrupt_before=["deploy"])

# 执行到deploy节点前会暂停，等待人工确认
# 人工确认后，从checkpoint恢复继续执行
```

.NET类比：WF的Bookmark机制——工作流执行到某个点暂停，等待外部事件触发后继续。和Durable Functions的`WaitForExternalEvent`完全对应。

### 3.6 Time Travel（时间旅行）

LangGraph的Checkpointer支持回到任意历史状态重新执行。调试神器。

```python
# 查看所有checkpoint
for state in app.get_state_history(config):
    print(state.values, state.config)

# 从某个历史checkpoint重新执行
app.update_state(old_config, new_values)
result = app.invoke(None, old_config)
```

.NET类比：就像数据库的Point-in-Time Recovery，或者Git的`git checkout <commit-hash>`。

---

## 四、多Agent通信模式

当Workflow中有多个Agent时，它们如何通信？

### 4.1 共享状态（Shared State）

所有Agent读写同一个State对象。简单直接，但要注意并发。

.NET类比：多个线程通过`ConcurrentDictionary`共享数据。

LangGraph默认采用这种模式——State就是共享的黑板(Blackboard)。

### 4.2 消息传递（Message Passing）

Agent之间通过消息通信，不共享内部状态。

.NET类比：微服务间的消息队列(RabbitMQ/Azure Service Bus)。

AutoGen v0.5的AgentChat API就是这种模式——Agent在"群聊"中发消息交流。

### 4.3 层级委托（Hierarchical Delegation）

上级Agent给下级Agent分配任务，下级完成后上报结果。

.NET类比：Hangfire的父子Job，或者分布式事务的Saga模式。

CrewAI和OpenAI Agents SDK的Handoffs机制都支持这种模式。

### 4.4 选择建议

| 通信模式 | 适用场景 | 复杂度 |
|---|---|---|
| 共享状态 | 2-3个紧耦合Agent | 低 |
| 消息传递 | 松耦合、需要审计日志 | 中 |
| 层级委托 | 复杂任务分解、团队协作 | 高 |

---

## 五、最佳实践

### 5.1 不要过度抽象

> "不要一上来就搞多Agent编排，先看一个augmented LLM能不能解决问题。" —— Anthropic

这和.NET界"不要过早微服务化"的建议一模一样。先单体，有明确需求再拆分。

### 5.2 工具描述当API文档写

```json
// ❌ 糟糕的工具描述
{ "name": "search", "description": "搜索" }

// ✅ 好的工具描述
{
  "name": "search_codebase",
  "description": "在代码仓库中搜索文件内容。支持正则表达式。返回匹配的文件路径和行号。最多返回50条结果。",
  "inputSchema": {
    "properties": {
      "pattern": { "type": "string", "description": "搜索模式，支持正则表达式" },
      "file_glob": {
        "type": "string",
        "description": "文件过滤，如 '*.py' 只搜Python文件",
        "default": "*"
      },
      "max_results": {
        "type": "integer",
        "description": "最大返回数",
        "default": 50,
        "enum": [10, 20, 50, 100]
      }
    }
  }
}
```

参数尽量用`enum`约束——减少LLM"自由发挥"出错的概率。

### 5.3 错误处理三板斧

```python
# 1. max_iterations 防无限循环
MAX_ITERATIONS = 5

# 2. 超时控制
import asyncio
result = await asyncio.wait_for(agent.run(task), timeout=120)

# 3. 异常兜底
try:
    result = await tool.execute(args)
except Exception as e:
    result = f"工具执行失败: {e}. 请尝试其他方法。"
    # 不要直接抛异常终止，给LLM机会自我修正
```

.NET类比：`CancellationToken` + `try-catch` + Polly重试。

### 5.4 成本控制策略

| 策略 | 实现 | 节省比例 |
|---|---|---|
| 路由用小模型 | GPT-4o-mini做分类，Opus做推理 | 50-70% |
| 缓存常见查询 | 语义相似度匹配历史结果 | 30-50% |
| 限制上下文长度 | 摘要压缩历史消息 | 20-40% |
| 早停机制 | 置信度达标就停止迭代 | 视场景而定 |

### 5.5 可观测性

LangGraph配合LangSmith提供完整的Trace可视化。OpenAI Agents SDK内置Tracing支持。

这是你的Application Insights——没有监控的Agent等于在裸奔。

---

## 六、LangGraph Cloud / Platform

LangGraph提供托管部署平台，类似Azure Functions的托管模式：

- 自动扩缩容
- 持久化Checkpoint存储
- HTTP API暴露Agent能力
- 监控和Trace集成

对团队来说，这意味着不用自己搭基础设施就能部署Agent Workflow。

---

## 七、从简单到复杂的推荐路径

```
Step 1: 单LLM + 工具调用（不需要Workflow框架）
    ↓
Step 2: Prompt Chaining（2-3步顺序流水线）
    ↓
Step 3: Routing（输入分类 + 专业化处理）
    ↓
Step 4: ReAct循环（LangGraph单Agent + 循环）
    ↓
Step 5: Orchestrator-Workers（多Agent协作）
    ↓
Step 6: 完整系统（Human-in-the-Loop + 持久化 + 监控）
```

每一步都要确认当前步骤真的不够用了，再往下走。过早复杂化是Agent开发的第一大坑。

---

## 相关文章

- [[AI-Agent架构]] - Agent的整体架构与框架对比
- [[MCP规范]] - 工具调用的标准化协议
- [[SWE-Agent实战]] - Workflow在软件工程Agent中的实际应用
- [[4.4-Workflow编排实践]] - LangGraph实战详细教程

---

## 更新日志

| 日期 | 内容 |
|---|---|
| 2026-04-08 | 初始骨架：WF/Durable Functions类比、节点流转、状态持久化、分支条件 |
| 2026-04-14 | 填充完整内容：Anthropic五种模式详解、LangGraph核心机制、多Agent通信、最佳实践、成本控制 |
