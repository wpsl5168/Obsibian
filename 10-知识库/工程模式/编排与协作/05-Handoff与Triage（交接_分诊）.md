---
title: "05-Handoff与Triage（交接_分诊）"
created: 2026-03-28
updated: 2026-06-16
type: methodology
tags: [agent, workflow, methodology]
status: stable
date: 2026-04-08
category: Notes
---

# 05-Handoff与Triage（交接_分诊）

## 1. 核心概念

**Handoff（交接）**与 **Triage（分诊）**是多 Agent 协作中的核心动态路由模式。

### Handoff（交接）

Agent 之间通过工具调用或状态更新实现**控制权转移**。与静态流程图不同，Handoff 模式通过状态变量（如 `current_step` 或 `active_agent`）动态决定由哪个 Agent 处理后续请求。

**核心机制**：
- 工具调用返回 `Command` 更新状态变量
- 状态持久化跨对话轮次
- Middleware 或路由器根据状态动态调整系统提示词和可用工具

> [!tip] .NET 类比
> 把 Handoff 想象成 **Workflow Foundation 状态机**：
> - 每个 Agent = 一个 State
> - Handoff 工具 = Transition Activity
> - 状态变量 = Workflow Context
> - 中间件 = `WorkflowRuntime.WorkflowIdled` 事件处理器，动态改变可执行 Activities

### Triage（分诊）

一个专门的 Agent（Triage Agent）负责**分类用户意图并路由到专业 Agent**。类比医院分诊台：根据症状决定去心内科还是骨科。

**与 Handoff 的区别**：
- **Triage 是 Handoff 的特化形式**：专门用于入口路由
- Triage Agent 通常不执行实际业务逻辑，只做分类+路由
- 常见于客服、呼叫中心、多领域应用的冷启动阶段

## 2. 解决的问题

### 单 Agent 的天花板
| 问题 | Handoff/Triage 解决方案 |
|------|------------------------|
| **上下文混乱** | 每个 Agent 专注单一领域，Prompt 简化 |
| **工具爆炸** | 分阶段暴露工具，避免一次性加载 50+ 工具导致模型混乱 |
| **安全边界** | 不同 Agent 绑定不同权限（如财务 Agent 只能调用财务 API） |
| **流程约束** | 强制按顺序完成步骤（如先验证身份再操作账户） |
| **成本优化** | Triage 用 GPT-4o-mini，专业 Agent 用 Claude Opus，节省 60-80% Token |

### 实际案例

**客户支持系统** (Reddit 分享的真实数据)：
```
Triage Agent → 分类意图
  ├── Technical Agent → 解决技术问题
  ├── Billing Agent → 处理账单查询
  └── Response Agent → 生成最终回复

结果：89% 查询自动处理，满意度超过纯人工客服
```

## 3. 代表项目/论文/框架（链接）

### 官方实现

| 框架 | Handoff 支持 | 实现方式 | 文档 |
|------|-------------|---------|------|
| **LangGraph** | ✅ 原生支持 | Command 机制 + Middleware | [LangChain Handoffs Docs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs) |
| **OpenAI Agents SDK** | ✅ 首创术语 | `transfer_to_<agent>` 工具模式 | [OpenAI Handoffs](https://openai.github.io/openai-agents-python/handoffs/) |
| **CrewAI** | ✅ 角色交接 | Task delegation + Role routing | [CrewAI Docs](https://docs.crewai.com/) |
| **AutoGen / AG2** | ✅ 群聊模式 | GroupChat with Speaker Selection | [AutoGen Multi-Agent](https://microsoft.github.io/autogen/) |

### 架构模式参考

**微软 Azure Architecture Center**：[AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- Sequential（顺序）、Concurrent（并行）、**Handoff**（交接）、Group Chat（群聊）、Magentic（磁铁）五大模式对比

**Databricks 生产实践**（2026.04 AI Engineer Summit）：
- 视频：[From Chaos to Choreography: Multi-Agent Orchestration Patterns That Actually Work](https://www.youtube.com/watch?v=2czYyrTzILg)
- 核心观点：Agent handoffs 的核心痛点是**状态管理**和**数据合约**，而非 LLM 本身

**LiveKit Voice Agent Pattern**：
- 语音场景下的 Handoff 实现（替代传统 IVR 菜单）
- 支持 Agent→Agent（路由）和 Agent→Human（升级）两种转移

## 4. 工程落地清单（Checklist）

### 4.1 架构选择

#### 单 Agent + Middleware（推荐）
```python
# LangGraph 单 Agent 模式
@wrap_model_call
def apply_step_config(request, handler):
    step = request.state.get("current_step", "triage")
    configs = {
        "triage": {
            "prompt": "Collect warranty info...",
            "tools": [record_warranty]
        },
        "specialist": {
            "prompt": "Provide solution for warranty={warranty_status}",
            "tools": [solve_issue, escalate]
        }
    }
    config = configs[step]
    request = request.override(
        system_prompt=config["prompt"].format(**request.state),
        tools=config["tools"]
    )
    return handler(request)
```

**优点**：消息历史自然流转，状态管理简单  
**适用**：大多数场景，除非需要严格隔离 Agent 运行环境

#### 多 Agent 子图模式
```python
# LangGraph 子图模式
@tool
def transfer_to_specialist(runtime) -> Command:
    return Command(
        goto="specialist_node",  # 跳转到另一个 Agent 节点
        update={
            "messages": [ToolMessage(...)],
            "context": extract_context(runtime.state)
        }
    )
```

**优点**：Agent 完全隔离（模型、知识库、权限）  
**代价**：需要精心设计**上下文传递**（哪些信息跨 Agent 传递）

### 4.2 Triage Agent 设计

**关键原则**：描述要当 API 文档写

```json
// ❌ 糟糕的 Triage 工具描述
{ "name": "route", "description": "选择目标 Agent" }

// ✅ 好的 Triage 工具描述
{
  "name": "route_to_specialist",
  "description": "根据用户问题分类路由到专业 Agent。\n可选目标：\n- billing: 账单、发票、支付问题\n- technical: 产品使用、bug、集成问题\n- sales: 定价、升级、新功能咨询\n返回值包含目标 Agent ID 和提取的关键信息。",
  "parameters": {
    "target_agent": {
      "type": "string",
      "enum": ["billing", "technical", "sales"],
      "description": "目标专业 Agent"
    },
    "extracted_context": {
      "type": "object",
      "description": "从用户输入提取的结构化信息（订单号、产品版本等）"
    }
  }
}
```

### 4.3 状态管理

| 状态类型 | 存储方案 | 适用场景 | .NET 类比 |
|---------|---------|---------|----------|
| **对话状态** | LangGraph Checkpointer | 需要跨轮次暂停/恢复 | `SessionState` |
| **用户档案** | 外部数据库 | 长期记忆、个性化 | `UserManager` |
| **临时上下文** | 工具返回值 | 单次 Handoff 传递的信息 | 方法参数 |

**示例：客服 Handoff 状态设计**
```python
class SupportState(AgentState):
    current_step: str = "triage"          # 当前所在 Agent
    user_tier: str | None = None          # 客户等级（影响路由决策）
    ticket_id: str | None = None          # 工单 ID
    warranty_status: str | None = None    # 保修状态
    escalation_reason: str | None = None  # 升级原因（给人类客服的上下文）
```

### 4.4 错误处理

```python
# 1. Handoff 失败回退
@tool
def transfer_with_fallback(target: str, runtime) -> Command:
    if target not in VALID_AGENTS:
        return Command(update={
            "messages": [ToolMessage(
                content=f"⚠️ 无效目标 {target}，回退到 Triage",
                tool_call_id=runtime.tool_call_id
            )],
            "current_step": "triage"  # 回到分诊
        })
    # 正常转移逻辑...

# 2. 最大跳转次数限制（防无限循环）
MAX_HANDOFFS = 5

def validate_handoff_count(state):
    count = state.get("handoff_count", 0)
    if count >= MAX_HANDOFFS:
        raise ValueError("超过最大 Handoff 次数，可能存在路由死循环")
```

### 4.5 可观测性

**必须记录的指标**：
1. **Handoff 路径**：用户请求经过了哪些 Agent（如 `triage → billing → escalation`）
2. **每个 Agent 的 Token 消耗**
3. **Handoff 触发原因**：工具调用了什么参数导致转移
4. **死循环检测**：是否在两个 Agent 之间反复跳转

**LangSmith Trace 示例**：
```
Trace ID: 5f3a2b...
├─ triage_agent (12 tokens)
│  └─ route_to_billing(reason="refund inquiry")
├─ billing_agent (340 tokens)
│  └─ transfer_to_manager(reason="amount > $1000")
└─ manager_agent (89 tokens)
   └─ approve_refund()

总耗时: 2.3s | 总 Token: 441
```

### 4.6 成本优化

| 优化策略 | 实现 | 节省比例 |
|---------|------|---------|
| **分级模型** | Triage 用 GPT-4o-mini，专家用 Claude Opus | 60-80% |
| **早停机制** | Triage Agent 发现问题过简单，直接回答不 Handoff | 20-40% |
| **上下文压缩** | 跨 Agent 传递时只传关键字段，不传完整历史 | 30-50% |

## 5. 更新记录

- **2026-06-16**：完整补充内容（核心概念、架构模式、工程落地清单、实战案例）
  - 数据来源：微软 Azure AI 架构指南、LangChain 官方文档、Reddit r/AI_Agents 社区分享、Databricks AI Engineer Summit 2026
  - 技术栈覆盖：LangGraph、OpenAI Agents SDK、CrewAI、AutoGen
- **2026-04-20**：创建骨架文件
- **2026-03-28**：初始化
