# 模式07：多Agent协作架构

## 一句话
不是一个全能Agent，而是多个专精Agent (感知/规划/执行/批判) 协作完成任务。

## 灵感
- AutoGen / CrewAI / LangGraph 的多Agent模式
- 你Hermes已有的 delegate_task + 子Agent生态
- 大型企业的"小队作战"心智

## 架构图

```
                ┌──────────────────────┐
                │  👨 用户输入         │
                └──────────┬───────────┘
                           ↓
            ┌──────────────────────────────┐
            │  🎩 Coordinator Agent        │
            │  (主Agent，任务分解/调度)    │
            └──────┬──────────┬─────┬─────┘
                   ↓          ↓     ↓
        ┌──────────┐  ┌──────────┐ ┌──────────┐
        │ 👁️ 感知    │  │ 🧠 规划    │ │ ✋ 执行    │
        │ Perception│  │ Planning  │ │ Action   │
        │ Agent    │  │ Agent     │ │ Agent    │
        │          │  │           │ │          │
        │ Vision/  │  │ Path/Task │ │ Motor/   │
        │ ASR/IMU  │  │ Decompose │ │ Speech   │
        └──────────┘  └──────────┘ └──────────┘
                   ↑          ↑     ↑
                   └──────────┴─────┘
                              ↓
                    ┌──────────────────┐
                    │  🔍 Critic Agent │
                    │  (质量评审/纠错) │
                    └──────────────────┘
```

## 典型Agent分工

| Agent | 模型 | 职责 |
|---|---|---|
| **Coordinator** | Qwen3B/Claude | 接需求、分任务、汇总结果 |
| **Perception** | YOLOv8 + Qwen3B | 处理视觉/听觉，输出结构化感知 |
| **Planning** | Claude (云) | 复杂规划、长程推理 |
| **Memory** | Qwen1.5B + RAG | 检索历史、维护KB |
| **Action** | 规则引擎 | 把意图转电机指令 |
| **Critic** | Claude/Qwen | 评审决策、防幻觉 |
| **Safety** | 纯规则 | 否决危险动作 |

## 工作流程

```
用户: "帮我找猫"
  ↓
Coordinator: "需要 感知+规划+执行"
  ├→ Perception: 扫描画面 → "看到客厅有沙发，无猫"
  ├→ Memory: "猫常去阳台" 
  ↓
Planning: "去阳台扫描"
  ├→ Action: 移动到阳台
  ├→ Perception: "找到一只橘猫"
  ├→ Critic: "确认是猫，置信度0.94" ✓
  ↓
Coordinator: "找到了" → 用户
```

## 多Agent vs 单Agent

| 维度 | 单Agent (模式03) | 多Agent |
|---|---|---|
| 上下文管理 | 一锅炖 | 各管各的，干净 |
| Token消耗 | 高 (一个长context) | 中 (各短context) |
| 可解释性 | 中 | 高 (每Agent输出可见) |
| 并行性 | 弱 | 强 (感知+规划并行) |
| 调试 | 难 | 中 (问题定位到Agent) |
| 复杂度 | 中 | 高 (Agent间协议) |
| 失败恢复 | 整体重来 | 局部重试 |

## 关键设计：Agent间通信

### 方案A: 消息总线 (推荐)
```python
# 共享Blackboard (SQLite/Redis)
bus.publish("perception/detection", {"objects": [...]})
bus.subscribe("planning/replan_request", planner.handle)
```

### 方案B: 直接调用 (Hermes现成)
```python
result = delegate_task(
    goal="规划路径", 
    context={"map": ..., "target": ...},
    tools=["nav"]
)
```

### 方案C: LangGraph状态图
```python
graph = StateGraph(RoverState)
graph.add_node("perceive", perception_agent)
graph.add_node("plan", planning_agent)
graph.add_node("act", action_agent)
graph.add_edge("perceive", "plan")
graph.add_conditional_edges("plan", route_decision)
```

## 优势

- **专精度高**: 每Agent只用必要的工具/Prompt
- **可解释强**: 每步决策来源清晰
- **故障隔离**: 一个Agent崩不影响全局
- **并行加速**: 感知/规划可同时跑
- **上下文清洁**: 避免"context污染"
- **复用Hermes生态**: delegate_task + 子Agent天生支持

## 缺陷

- **延迟累加**: 多Agent串行 → 总延迟变长
- **协议复杂**: Agent间消息格式要约定好
- **资源消耗**: 多个LLM实例，内存/算力压力大
- **调试更难**: 问题可能在Agent间交互
- **过度设计风险**: 简单任务多Agent反而慢

## 适用场景

✅ 任务复杂、能明确分工
✅ 需要可解释性 (医疗/工业)
✅ 已有Hermes多Agent能力 (你的情况)
✅ 团队多人协作 (每人维护一个Agent)

❌ 简单任务 (单Agent就够)
❌ 极致延迟要求
❌ 资源紧张 (Pi上跑5个LLM不现实)

## Pi上的可行性

**直接跑5个本地LLM不现实** (8GB内存撑不住)。

可行方案:
- **轻Agent本地，重Agent云端** (混合)
- **同一模型多角色** (Qwen3B扮演不同Agent，靠system prompt切换)
- **Agent调度复用** (热加载，按需启动)

## 与其他模式的关系

- **可包在模式03外面** — 把混合脑做成"多Agent + 路由"
- **模式06的ROS节点天然就是多Agent**
- **模式05的BT可以编排多Agent**

## 一句话评价

**多Agent是大型项目的组织哲学**，但小车单兵作战可能用力过猛。建议Phase 5+引入。

## 与本项目匹配度

⭐⭐⭐ (3/5) — 现阶段用单Agent (模式03)更高效。等Skills生态丰富后，可演进为多Agent。
