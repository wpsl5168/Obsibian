---
title: AI Agent 架构与核心思想
date: 2026-04-08
tags:
  - AIAgent
  - Architecture
  - AI
---

# AI Agent 架构与核心思想

AI Agent 可以看作是具备自主规划和执行能力的系统。如果我们用 .NET 生态来类比：
- **大模型 (LLM)** 就像是系统中的 **CLR (公共语言运行时)** 或核心计算引擎，负责理解指令并进行推理。
- **Memory (记忆)** 就像是 **SQL Server 数据库** 或者是内存中的 `MemoryCache`。长期记忆存储在数据库表中，短期记忆则是当前线程的 `HttpContext.Items`。
- **Tools (工具)** 就像是注入到系统中的各类 **服务接口 (Interfaces)** 或外部的 **Web API**。

## 关键能力
1. 思考与规划：类似于 .NET 中的 TPL (任务并行库)，将一个大 Task 拆解为多个子 Task。
2. 工具调用：就像通过反射或者依赖注入 (DI) 调用外部类的方法。详情参见 [[MCP规范]]。
3. 工作流控制：复杂的 Agent 流程需要清晰的状态管理，参考 [[Workflow设计模式]]。

## 进阶实践
如果想了解如何用 Agent 来写代码，请阅读 [[SWE-Agent实战]]。