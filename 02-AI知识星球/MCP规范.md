---
title: MCP规范（Model Context Protocol）
date: 2026-04-14
tags:
  - MCP
  - 协议
  - Tool-Use
  - 入门
---

# MCP规范（Model Context Protocol）

> 用SQL Server存储过程和ADO.NET的概念来理解MCP——AI世界的"USB-C接口"。
> 相关深入章节：[[4.3-MCP协议详解]] | [[AI-Agent架构]]

---

## 一、一句话理解MCP

**MCP之于AI Agent，就像ADO.NET之于.NET应用——一套标准化的数据访问协议。**

在没有ADO.NET之前，访问SQL Server用一套API，访问Oracle用另一套，访问MySQL又是一套。ADO.NET统一了接口：`IDbConnection`、`IDbCommand`、`IDataReader`，不管底层是什么数据库，上层代码写法一样。

MCP做的是同一件事：在没有MCP之前，接Claude用Anthropic的Tool API，接GPT用OpenAI的Function Calling，接Gemini用Google的Tool格式。每家LLM平台的工具接入方式都不同。MCP统一了这一切。

Anthropic在2024年11月发布MCP，称之为**"AI的USB-C接口"**。到2025年，OpenAI（2025.3）和Google（2025.4）相继宣布支持，MCP正在成为事实上的行业标准。

---

## 二、核心架构：Client-Server模型

### 2.1 三个角色

```
┌─────────────────────────────────────────┐
│                 Host                     │
│  (Claude Desktop / VS Code / IDE)       │
│                                          │
│  ┌──────────┐  ┌──────────┐             │
│  │ MCP      │  │ MCP      │             │
│  │ Client 1 │  │ Client 2 │  ...        │
│  └────┬─────┘  └────┬─────┘             │
└───────┼──────────────┼──────────────────┘
        │              │
   ┌────▼─────┐  ┌────▼─────┐
   │ MCP      │  │ MCP      │
   │ Server A │  │ Server B │
   │ (GitHub) │  │ (数据库)  │
   └──────────┘  └──────────┘
```

| 角色 | .NET类比 | 职责 |
|---|---|---|
| Host | ASP.NET宿主进程 | 运行环境，管理生命周期 |
| Client | ADO.NET的SqlConnection | 维护与单个Server的连接，1:1关系 |
| Server | SQL Server实例 | 暴露能力（工具/资源/提示），处理请求 |

.NET类比展开：
- **Host** = IIS/Kestrel宿主，你的Claude Desktop或VS Code就是Host
- **Client** = 每个`SqlConnection`对象，Host内部为每个Server维护一个Client实例
- **Server** = 一个SQL Server实例，暴露存储过程(Tools)、表/视图(Resources)、查询模板(Prompts)

### 2.2 三大原语（Server暴露的能力）

MCP Server对外暴露三种原语，用SQL Server的概念来类比：

| MCP原语 | SQL Server类比 | 说明 |
|---|---|---|
| **Tools** | 存储过程(Stored Procedure) | 可执行的操作，有输入参数和返回值 |
| **Resources** | 表/视图(Table/View) | 只读数据源，Agent可以读取 |
| **Prompts** | 查询模板(SQL Template) | 预定义的Prompt模板，带参数槽位 |

#### Tools（工具）= 存储过程

这是MCP最核心的原语。每个Tool就像一个存储过程——有名称、描述、参数Schema、返回值。

```json
// MCP Tool声明，类似存储过程签名
{
  "name": "query_database",
  "description": "执行SQL查询并返回结果（只读）",
  "inputSchema": {
    "type": "object",
    "properties": {
      "sql": {
        "type": "string",
        "description": "SELECT查询语句，禁止DDL/DML"
      },
      "database": {
        "type": "string",
        "enum": ["production_readonly", "analytics"],
        "description": "目标数据库"
      }
    },
    "required": ["sql", "database"]
  }
}
```

```sql
-- SQL Server类比：这就是一个存储过程签名
CREATE PROCEDURE [dbo].[query_database]
    @sql NVARCHAR(MAX),
    @database NVARCHAR(50)  -- 约束: 'production_readonly' | 'analytics'
AS
```

**2025.3新增：Tool Annotations（工具注解）**

类似.NET的Attribute标注，给工具加元数据：

```json
{
  "name": "delete_file",
  "annotations": {
    "destructive": true,      // 破坏性操作
    "requiresConfirmation": true,  // 需要人工确认
    "readOnly": false,
    "idempotent": false
  }
}
```

这让Host可以在执行破坏性操作前弹出确认对话框——像SQL Server Management Studio执行DELETE前的警告。

#### Resources（资源）= 表/视图

只读数据暴露。Agent可以读取但不能修改。

```json
{
  "uri": "file:///project/src/main.py",
  "name": "主程序源码",
  "mimeType": "text/x-python"
}
```

类比：就像给Agent开了一个只读的数据库视图权限。

#### Prompts（提示模板）= 查询模板

预定义的Prompt模板，用户或Agent可以填参数使用。

```json
{
  "name": "code_review",
  "description": "代码审查提示模板",
  "arguments": [
    { "name": "language", "description": "编程语言", "required": true },
    { "name": "code", "description": "待审查代码", "required": true }
  ]
}
```

类比：就像团队共享的SQL查询模板，参数化后复用。

---

## 三、协议交互：JSON-RPC 2.0

MCP的通信协议基于**JSON-RPC 2.0**，这对.NET开发者应该很熟悉——和WCF/gRPC的RPC调用模式一样。

### 3.1 生命周期

```
Client                          Server
  │                                │
  │──── initialize ───────────────>│  握手：交换能力声明
  │<─── initialize result ─────── │  (类似TLS握手/连接协商)
  │                                │
  │──── initialized ──────────────>│  确认就绪
  │                                │
  │──── tools/list ───────────────>│  获取工具列表
  │<─── tools ────────────────────│  (类似sp_helptext查看存储过程)
  │                                │
  │──── tools/call ───────────────>│  调用工具
  │<─── result ───────────────────│  (类似EXEC stored_procedure)
  │                                │
  │──── shutdown ─────────────────>│  关闭连接
  │                                │  (类似SqlConnection.Close)
```

### 3.2 请求/响应格式

```json
// 请求：调用工具（类似 EXEC sp_get_weather @city='北京'）
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": { "city": "北京" }
  }
}

// 响应
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "北京：多云转小雨，15-22°C"
      }
    ]
  }
}
```

**2025.3新增：JSON-RPC批处理**

可以一次发送多个请求，减少网络往返——就像SQL Server的批量查询。

```json
[
  {"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_weather","arguments":{"city":"北京"}}},
  {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_weather","arguments":{"city":"上海"}}}
]
```

---

## 四、传输层

### 4.1 stdio（本地传输）

Server作为子进程运行，通过标准输入/输出通信。

```
Host进程
  └── MCP Client
        └── 子进程: MCP Server (stdin/stdout)
```

.NET类比：就像`Process.Start()`启动一个控制台应用，通过`StandardInput`/`StandardOutput`通信。

```csharp
// .NET类比
var process = new Process();
process.StartInfo.FileName = "mcp-server-sqlite";
process.StartInfo.RedirectStandardInput = true;
process.StartInfo.RedirectStandardOutput = true;
process.Start();

// 发送JSON-RPC请求
await process.StandardInput.WriteLineAsync(jsonRpcRequest);
// 读取响应
var response = await process.StandardOutput.ReadLineAsync();
```

适用场景：本地工具，如文件系统、本地数据库、Git操作。

### 4.2 Streamable HTTP（远程传输，2025.3新增）

替代之前的HTTP+SSE方案（SSE已deprecated）。

```
Client ──── HTTP POST/GET ────> Server (远程)
       <─── Streaming Response ─
```

.NET类比：从早期的Long Polling升级到SignalR，Streamable HTTP就是MCP世界的"协议升级"。

支持OAuth 2.1认证，适用于远程/云端MCP Server。

### 4.3 传输选择指南

| 场景 | 传输方式 | 类比 |
|---|---|---|
| 本地IDE插件 | stdio | 进程间通信(IPC) |
| 云端服务集成 | Streamable HTTP | REST API / SignalR |
| 已有SSE实现 | SSE（deprecated，迁移中） | 旧版WebSocket polyfill |

---

## 五、MCP Server生态

截至2026年初，社区已有**1000+** MCP Server实现，覆盖主要场景：

### 5.1 常见Server分类

| 类别 | 示例Server | 暴露的工具 |
|---|---|---|
| 数据库 | mcp-server-sqlite, mcp-server-postgres | 查询、Schema查看 |
| 开发工具 | mcp-server-github, mcp-server-git | Issue操作、PR管理、提交历史 |
| 云服务 | mcp-server-aws, mcp-server-gcp | 资源管理、部署操作 |
| 通信 | mcp-server-slack, mcp-server-email | 发消息、读邮件 |
| 文件系统 | mcp-server-filesystem | 文件读写、目录遍历 |
| 搜索 | mcp-server-brave-search | Web搜索 |
| 知识库 | mcp-server-notion, mcp-server-confluence | 文档读写 |

### 5.2 配置示例（Claude Desktop）

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/path/to/db.sqlite"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx"
      }
    }
  }
}
```

.NET类比：这就是`appsettings.json`里的连接字符串配置。

---

## 六、SDK与开发

官方提供Python和TypeScript两个SDK。

### 6.1 用Python写一个MCP Server

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("my-tool-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="calculate",
            description="计算数学表达式",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '2+3*4'"
                    }
                },
                "required": ["expression"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "calculate":
        result = eval(arguments["expression"])  # 生产环境请用安全的解析器
        return [TextContent(type="text", text=str(result))]

# 启动：stdio传输
if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    asyncio.run(stdio_server(server))
```

.NET类比：这和写一个ASP.NET Minimal API的体验几乎一样——定义路由(list_tools)、处理请求(call_tool)、启动服务。

### 6.2 .NET社区SDK

社区有非官方的.NET MCP SDK实现 [待验证]，基本思路：

```csharp
// 概念性示例
public class WeatherMcpServer : McpServerBase
{
    [McpTool("get_weather", "查询城市天气")]
    public async Task<string> GetWeather(
        [McpParam("城市名称")] string city)
    {
        var weather = await _weatherService.GetAsync(city);
        return JsonSerializer.Serialize(weather);
    }
}
```

---

## 七、当前缺口与展望

MCP虽然势头强劲，但仍有明显短板：

| 缺口 | 现状 | 期望 |
|---|---|---|
| 安全认证 | OAuth 2.1刚加入，实践不足 | 需要成熟的认证最佳实践 |
| Server发现 | 手动配置，无注册中心 | 需要类似NuGet/npm的Server Registry |
| 权限粒度 | 粗粒度：全部工具或不连 | 需要细粒度的Tool级权限控制 |
| 版本管理 | 无版本协商机制 | 需要类似API版本控制的方案 |
| 监控审计 | 缺少标准化的日志/审计方案 | 需要类似Application Insights的集成 |

.NET类比：MCP现在的阶段类似早期的NuGet——核心功能可用，生态快速增长，但治理和安全机制还在完善中。

---

## 八、快速上手路径

1. **体验**：安装Claude Desktop，配置一个mcp-server-filesystem，让Claude读写你的文件
2. **理解**：抓包看JSON-RPC交互（stdio模式下可以看stdin/stdout日志）
3. **开发**：用Python SDK写一个自定义Server，暴露你常用的内部工具
4. **集成**：把MCP Server接入你的Agent框架（LangGraph/OpenAI Agents SDK都支持）

---

## 相关文章

- [[AI-Agent架构]] - Agent的整体架构，MCP在其中的定位
- [[Workflow设计模式]] - 工具调用如何嵌入工作流
- [[SWE-Agent实战]] - SWE-Agent如何使用工具链
- [[4.3-MCP协议详解]] - MCP规范的完整技术细节

---

## 更新日志

| 日期 | 内容 |
|---|---|
| 2026-04-08 | 初始骨架：SQL Server/ADO.NET类比、工具声明、协议交互 |
| 2026-04-14 | 填充完整内容：2025.3规范更新、三大原语详解、传输层对比、Server生态、SDK示例、缺口分析 |
