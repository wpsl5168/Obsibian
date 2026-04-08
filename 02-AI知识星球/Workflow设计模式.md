---
title: Workflow 设计模式
date: 2026-04-08
tags:
  - Workflow
  - StateMachine
  - SystemDesign
---

> [!note] Workflow 设计模式
> 单纯的 [[AI-Agent 架构]] 往往不可控，因此在企业级落地时，我们通常采用 **Workflow （工作流）** 来约束 LLM 的行为。

## 状态机与工作流引擎

在 C# 中，我们有经典的 `Windows Workflow Foundation (WF)` 或者基于无服务器架构的 `Durable Functions`。
AI 的 Workflow 也是类似的：

- **节点流转**：每个节点就像是 .NET 里的一个 `Activity`，有着明确的输入和输出参数。
- **状态持久化 (Event Sourcing)**：整个流程的执行历史就像是插入到 SQL Server Event Store 中的记录。如果某个节点出错，我们可以像数据库事务一样进行重试或回滚。
- **分支条件**：利用 LLM 的判别能力作为网关，类似于 C# 里的 `switch` 表达式或 `if-else` 树，决定下一步走向哪个节点处理。

为了让 Workflow 更加灵活，节点往往会利用 [[MCP 规范]] 引入外部工具。高级的研发流甚至可以演变为 [[SWE-Agent 实战]] 的形式。