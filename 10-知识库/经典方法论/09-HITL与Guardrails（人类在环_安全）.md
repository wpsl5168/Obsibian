---
title: "09-HITL与Guardrails（人类在环_安全）"
created: 2026-03-28
updated: 2026-06-16
type: methodology
tags: [hitl, guardrails, safety, security, llm]
status: active
date: 2026-04-08
category: Notes
---

# 09-HITL与Guardrails（人类在环_安全）

## 1. 核心概念

### Human-in-the-Loop (HITL / 人类在环)

**HITL** 是一种架构模式：AI Agent 在关键决策点**暂停执行**，等待人类审核和反馈后再继续。自动化的目标不是完全移除人类，而是让人类监督模糊决策边界。

**核心价值**：
- **精确性**：人类修正 Agent 的错误推理
- **安全性**：高风险操作必须人工审批
- **可问责性**：关键决策留痕，可追溯责任人

> [!tip] .NET 类比
> 把 HITL 想象成 **Workflow Foundation 的 BookmarkActivity**：
> - 工作流执行到 Bookmark 时暂停
> - 系统等待外部事件（`ResumeBookmark`）
> - 恢复后带着人类输入继续执行
>
> 或者类比 SQL Server 的 **WAITFOR**：
> ```sql
> -- Agent 执行到此处挂起
> WAITFOR (RECEIVE message FROM HumanApprovalQueue)
> -- 收到人类消息后继续
> ```

### Guardrails（安全护栏）

**Guardrails** 是运行时控制层，在请求到达模型前和响应返回用户前，**强制执行安全、合规和质量策略**。

| 类型 | 检查时机 | 作用 |
|------|---------|------|
| **Input Validation** | 模型调用前 | 阻止恶意 Prompt、越狱攻击、PII 泄露 |
| **Output Filtering** | 模型返回后 | 检测幻觉、过滤有毒内容、脱敏敏感信息 |
| **Content Filters** | 双向 | 限制话题范围（如客服拒绝政治讨论） |
| **PII Detection** | 双向 | 扫描并自动脱敏身份证、信用卡号等 |
| **Prompt Injection Defense** | 输入侧 | 识别试图覆盖系统指令的攻击 |

**与 HITL 的区别**：
- HITL = 人类主动审核（Approval Gate）
- Guardrails = 自动化策略执行（Policy Engine）

## 2. 解决的问题

### HITL 解决的核心问题

| 场景 | 无 HITL 风险 | HITL 方案 |
|------|-------------|----------|
| **金融交易** | Agent 直接执行 $10,000 转账 | 暂停并展示交易详情，等人类批准 |
| **法律文档** | 自动生成合同条款可能有瑕疵 | 律师在最终签署前审查 AI 草案 |
| **医疗诊断** | AI 误诊导致错误治疗 | 医生确认诊断和用药建议 |
| **代码部署** | Agent 直接 push 到 production | PR 创建后等待人工 Code Review |

**2026 现实**：完全自主的 Agent 仍是科幻。生产系统的标准模式是 **80% AI 执行 + 20% 人类决策**。

### Guardrails 防御的威胁

| 威胁 | 统计数据 | 后果 |
|------|---------|------|
| **Prompt Injection** | 无防护成功率 >50% | 窃取系统提示词、数据渗漏、劫持对话 |
| **PII 泄露** | 3 大泄露向量：训练记忆、推理重建、RAG 未过滤 | 违反 GDPR/HIPAA、用户隐私侵犯 |
| **Toxic 内容** | 生成歧视/攻击性语言 | 品牌声誉受损、用户流失 |
| **Hallucination** | 生成不存在的事实 | 客户信任崩塌、法律风险 |

**市场规模**：Guardrails 市场从 2024 年的 $0.7B 预计增长到 2034 年的 **$109.9B**。

## 3. 代表项目/论文/框架（链接）

### HITL 主流实现

| 框架 | HITL 支持 | 实现方式 | 文档 |
|------|----------|---------|------|
| **LangGraph** | ✅ 原生支持 | Static/Dynamic Interrupts + Checkpointer | [IBM HITL Tutorial](https://www.ibm.com/think/tutorials/human-in-the-loop-ai-agent-langraph-watsonx-ai) |
| **OpenAI Agents SDK** | ✅ 内置 | `wait_for_approval()` 工具 | [OpenAI Docs](https://platform.openai.com/docs/agents) |
| **CopilotKit** | ✅ React 组件 | `useHumanInTheLoop` hook | [CopilotKit HITL Demo](https://docs.showcase.copilotkit.ai/langgraph-python/human-in-the-loop) |
| **CrewAI** | ✅ Human Task | `human_input=True` 参数 | [CrewAI Tasks](https://docs.crewai.com/) |

#### LangGraph HITL 两种模式

**1. Static Interrupts（静态中断）**
```python
# 在指定节点前/后暂停
graph = builder.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["tools"],  # 工具调用前暂停
    interrupt_after=["assistant"]  # LLM 输出后暂停
)
```
**适用**：固定检查点，如每次工具调用前人工审核

**2. Dynamic Interrupts（动态中断）**
```python
from langgraph.types import interrupt

def risky_action(state):
    if state["amount"] > 10000:
        # 金额大时动态触发中断
        human_decision = interrupt("高额转账需审批")
        if human_decision != "approve":
            return {"status": "cancelled"}
    # 继续执行...
```
**适用**：基于运行时条件决定是否暂停

### Guardrails 主流框架

| 框架 | 类型 | 特性 | GitHub Stars | 文档 |
|------|------|------|-------------|------|
| **NeMo Guardrails** (NVIDIA) | 开源 | Colang DSL，5 种 Rail 类型 | 5.6K | [NeMo Docs](https://github.com/NVIDIA/NeMo-Guardrails) |
| **Guardrails AI** | 开源+商业 | 声明式验证，Pydantic 集成 | 4.3K | [Guardrails AI](https://www.guardrailsai.com/) |
| **Llama Guard** (Meta) | 开源模型 | 13B/70B 分类器 | - | [Llama Guard Paper](https://ai.meta.com/research/publications/llama-guard/) |
| **AWS Bedrock Guardrails** | 托管服务 | 云原生，PII/Toxic 检测 | - | [AWS Docs](https://aws.amazon.com/bedrock/guardrails/) |
| **Lakera Guard** | API 服务 | Prompt Injection 防御专家 | - | [Lakera](https://www.lakera.ai/) |
| **OpenAI Moderation API** | API 服务 | Toxic/NSFW 分类 | - | [OpenAI Docs](https://platform.openai.com/docs/guides/moderation) |

#### NeMo Guardrails 五种 Rail

```yaml
# Colang DSL 示例
define flow
  # 1. Input Rails: 检查用户输入
  user said something
    when input contains pii
      bot say "请不要提供个人信息"
      stop
  
  # 2. Dialog Rails: 控制对话流
  user ask about politics
    bot refuse politely
  
  # 3. Retrieval Rails: 过滤知识库结果
  search knowledge base
    filter out documents with classification >= confidential
  
  # 4. Execution Rails: 门控工具调用
  bot execute transfer_money
    if amount > $1000
      require human approval
  
  # 5. Output Rails: 验证响应
  bot say something
    when output contains hallucination
      regenerate with grounding
```

## 4. 工程落地清单（Checklist）

### 4.1 HITL 架构设计

#### 决策树：何时需要 HITL？

```
是否涉及不可逆操作？（删除数据、金钱转移、合同签署）
├─ 是 → 强制 HITL
└─ 否
    └─ 是否有合规要求？（医疗、金融、法律）
        ├─ 是 → 强制 HITL
        └─ 否
            └─ Agent 准确率 < 95%？
                ├─ 是 → 建议 HITL
                └─ 否 → 可选 HITL（用于用户信任建立）
```

#### LangGraph 实战：异步审批工作流

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class ApprovalState(TypedDict):
    messages: Annotated[list, add_messages]
    pending_action: dict | None
    approval_status: str | None  # "pending" | "approved" | "rejected"

def create_approval_workflow():
    builder = StateGraph(ApprovalState)
    
    # 1. Agent 节点：生成待审核操作
    def agent_node(state):
        action = {"type": "transfer", "amount": 5000, "to": "vendor@example.com"}
        return {
            "pending_action": action,
            "approval_status": "pending",
            "messages": [AIMessage(content=f"准备执行: {action}")]
        }
    
    # 2. 审批节点：等待人类输入
    def approval_gate(state):
        # 这里会触发 interrupt
        pass  # LangGraph 自动处理
    
    # 3. 执行节点：根据审批结果决定
    def execute_or_cancel(state):
        if state["approval_status"] == "approved":
            # 执行实际操作
            return {"messages": [SystemMessage(content="✅ 操作已执行")]}
        else:
            return {"messages": [SystemMessage(content="❌ 操作已取消")]}
    
    builder.add_node("agent", agent_node)
    builder.add_node("approval", approval_gate)
    builder.add_node("execute", execute_or_cancel)
    
    builder.add_edge(START, "agent")
    builder.add_edge("agent", "approval")
    builder.add_edge("approval", "execute")
    builder.add_edge("execute", END)
    
    # 关键：在审批节点前中断
    return builder.compile(
        checkpointer=MemorySaver(),
        interrupt_before=["execute"]
    )

# 使用示例
graph = create_approval_workflow()
config = {"configurable": {"thread_id": "approval-123"}}

# 第一次调用：Agent 执行到审批点暂停
for event in graph.stream({"messages": []}, config):
    print(event)

# 人类审核（异步，可能几小时后）
current_state = graph.get_state(config)
print(f"待审批操作: {current_state.values['pending_action']}")

# 人类批准后更新状态并恢复
graph.update_state(config, {"approval_status": "approved"})
for event in graph.stream(None, config):  # None 表示从断点恢复
    print(event)
```

#### 上下文保留最佳实践

```python
# ✅ 好的做法：人类审批时看到完整上下文
def format_approval_request(state):
    return {
        "request_id": uuid4(),
        "action": state["pending_action"],
        "reasoning": state["agent_reasoning"],  # Agent 的思考过程
        "related_messages": state["messages"][-5:],  # 最近 5 轮对话
        "timestamp": datetime.now(),
        "timeout": timedelta(hours=24)  # 24 小时未审批自动拒绝
    }

# ❌ 坏的做法：只告诉人类"请批准"
def bad_approval_request(state):
    return {"action": "approve or reject"}  # 人类不知道批准什么
```

### 4.2 Guardrails 部署策略

#### 分层防御架构

```
┌─────────────────────────────────────────┐
│  User Input                              │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Layer 1: Input Validation               │
│  - Prompt Injection Detection (Lakera)   │
│  - PII Scanner (AWS Comprehend)          │
│  - Length/Format Checks                  │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Layer 2: LLM Call                       │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Layer 3: Output Filtering               │
│  - Hallucination Detection (Guardrails AI)│
│  - Toxic Content Filter (OpenAI Mod API) │
│  - PII Redaction                         │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  User Response                           │
└─────────────────────────────────────────┘
```

#### NeMo Guardrails 快速启动

```python
from nemoguardrails import RailsConfig, LLMRails

config = RailsConfig.from_path("./config")  # 加载 Colang 配置
rails = LLMRails(config)

# 包装 LLM 调用
response = rails.generate(
    messages=[{"role": "user", "content": "帮我转账 $5000"}]
)

# NeMo 自动应用所有 Rails
print(response)  # 可能被 Execution Rail 拦截并要求审批
```

#### Guardrails AI 声明式验证

```python
from guardrails import Guard
from guardrails.validators import ValidLength, ToxicLanguage, PIIFilter

guard = Guard.from_string(
    validators=[
        ValidLength(min=10, max=500),  # 输出长度限制
        ToxicLanguage(threshold=0.8, on_fail="filter"),  # 过滤有毒内容
        PIIFilter(pii_types=["EMAIL", "PHONE", "SSN"], on_fail="fix")  # 脱敏 PII
    ],
    description="客服回复生成"
)

# 包装 LLM 调用
raw_output = llm.invoke(prompt)
validated_output = guard.validate(raw_output)  # 自动修正/过滤
```

### 4.3 监控与告警

| 指标 | 告警阈值 | 处理 |
|------|---------|------|
| **HITL 审批率** | >30% | Agent 过于保守，需调整暂停逻辑 |
| **HITL 平均等待时间** | >4 小时 | 增加审批人员或降低优先级任务的暂停 |
| **Guardrail 拦截率** | >10% | 输入质量差或 Guardrail 过严 |
| **Prompt Injection 检出** | >1/天 | 可能遭受攻击，升级安全措施 |
| **PII 泄露次数** | >0 | 立即调查并通知法务/合规团队 |

## 5. 更新记录

- **2026-06-16**：完整补充内容（HITL 架构、Guardrails 框架对比、工程落地清单）
  - 数据来源：IBM Watson HITL 教程、Openlayer Guardrails Guide、NeMo/Guardrails AI 官方文档
  - 框架覆盖：LangGraph、OpenAI SDK、NeMo Guardrails、Guardrails AI、AWS Bedrock、Lakera
  - 市场数据：Guardrails 市场规模 $0.7B→$109.9B（2024-2034），Prompt Injection 成功率 >50%
- **2026-04-20**：创建骨架文件
- **2026-03-28**：初始化
