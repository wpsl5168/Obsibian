---
title: MCP 规范与工具接入
date: 2026-04-08
tags:
  - MCP
  - Tools
  - Integration
---

> [!note] MCP 规范 (Model Context Protocol)
> [[AI-Agent 架构]] 中提到，工具调用是 Agent 与外部世界交互的桥梁。**MCP** (Model Context Protocol) 提供了一套标准化的工具定义和调用协议。

## .NET 与 SQL Server 类比

理解 MCP 规范，我们可以把它比作 **SQL Server 中的存储过程 (Stored Procedures)** 或者 **ADO.NET 中的 `SqlCommand`**。

- **工具声明 (Declaration)**：就像在 SQL Server 中定义 `CREATE PROCEDURE dbo.GetUserDetails (@UserId INT)`，你必须清楚地告诉调用者（ LLM ）这个工具有什么参数、什么类型、是否必填。
- **协议交互**： Agent 就像 ADO.NET 客户端，它知道如何构造一个带有参数的请求发送给服务器，服务器执行后返回结构化结果（如 JSON 或者 `DataTable`）。
- **MCP Server**：就是一个宿主程序，类似于挂载了多个 Web API 的 ASP.NET Core Kestrel 服务器，暴露出统一的终结点供 LLM 发现和调用。

## 与其他系统的联动
掌握了 MCP ，我们就能将各种企业内部系统无缝接入 [[Workflow 设计模式]]，并在 [[SWE-Agent 实战]] 中赋予代码生成工具更强大的能力。