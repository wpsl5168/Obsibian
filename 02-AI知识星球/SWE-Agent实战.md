---
title: SWE-Agent 实战指南
date: 2026-04-08
tags:
  - SWE-Agent
  - CodeGen
  - Practice
---

# SWE-Agent 实战指南

**SWE-Agent** (Software Engineering Agent) 是将 [[AI-Agent架构]] 专门应用于软件工程领域的实践。它能够自主阅读代码、定位 bug、修改文件并提交 PR。

## 深入类比

- **代码环境沙箱**：就像给 Agent 分配了一个隔离的 **AppDomain** 或者是带有特定只读/读写权限的 SQL Server 登录账户，防止越权操作。
- **Terminal 交互**：SWE-Agent 通过类似 SSH 或伪终端操作，不断下发命令。这有点像在 SQL Server Management Studio (SSMS) 里面执行一段段 `T-SQL`，根据查出来的表结构（目录结构）再写下一段查询。
- **工具链集成**：它重度依赖 [[MCP规范]]。比如通过 MCP 接入 `git` 命令行工具或者 `msbuild` 编译工具。一旦编译失败，它会像 C# 捕获异常 (`try-catch`) 一样，将错误日志反馈给 LLM，触发新一轮的思考。

通过将 SWE-Agent 节点编排进标准的 [[Workflow设计模式]]，我们可以打造自动化的 Code Review 流水线。