---
title: 05-behavior-tree-llm
created: 2026-04-23
updated: 2026-04-23
type: concept
tags: [pi-rover]
status: draft
---
# 模式05：行为树 + LLM 架构

## 一句话
任务流程用行为树(Behavior Tree)做骨架，LLM动态填充叶子节点的"思考"。

## 灵感
- 游戏AI: Halo/Unreal Engine NPC 30年用法
- ROS 2 Nav2: 默认导航栈用BehaviorTree.CPP
- 学界2024-2025热点: "LLM-Based Behavior Tree Generation"

## 架构图

```
                ┌────────────────────┐
                │   任务输入         │
                │ "巡逻并报告异常"   │
                └──────────┬─────────┘
                           ↓
        ┌──────────────────────────────────────┐
        │  LLM (一次性生成BT XML)               │
        │  Claude/Qwen → 行为树定义             │
        └──────────────────┬───────────────────┘
                           ↓
┌──────────────────────────────────────────────────┐
│           Behavior Tree Engine                    │
│           (BehaviorTree.CPP / py_trees)           │
│                                                   │
│              [Sequence: 巡逻]                     │
│                  ├── [GoTo: 客厅]                 │
│                  ├── [Scan: 360°]                 │
│                  ├── [Fallback: 异常处理]         │
│                  │     ├── [HasAnomaly?]          │
│                  │     │     └── [LLM: 描述异常]  │ ← LLM在叶子
│                  │     └── [Continue]             │
│                  └── [GoTo: 厨房] ...             │
└──────────────────────────┬───────────────────────┘
                           ↓
              ┌─────────────────────────┐
              │   原子动作 (Skills)     │
              │   Move/Scan/Detect/Say  │
              └─────────────────────────┘
```

## 两种LLM参与方式

### 方式A: LLM生成行为树 (设计时)

```python
prompt = "为'巡逻并报告异常'生成BT XML"
xml = llm.generate(prompt)
tree = BehaviorTree.from_xml(xml)
tree.tick_loop()  # 之后纯BT执行
```

- LLM只在任务开始时调用一次
- 执行时不依赖LLM，超快超稳
- 适合任务结构相对固定

### 方式B: LLM嵌入叶子节点 (运行时)

```xml
<Sequence>
  <GoTo target="kitchen"/>
  <LLMReason prompt="看到的物品有异常吗？" 
             input="{vision_output}"
             output="{anomaly_desc}"/>
  <Condition test="{anomaly_desc} != null"/>
  <SayOut text="{anomaly_desc}"/>
</Sequence>
```

- LLM作为"智能叶子"，处理需要理解的环节
- 其余节点纯规则，确定性强
- 适合任务结构清晰但局部需要智能

### 方式C (推荐): A+B混合
- 启动时LLM生成BT骨架
- 关键叶子节点也是LLM (动态判断)
- 失败时LLM重新生成子树

## BT vs 状态机 vs LLM Agent

| 维度 | 状态机 (FSM) | 行为树 (BT) | 纯LLM Agent |
|---|---|---|---|
| 表达力 | 弱 (状态爆炸) | 强 (组合性好) | 极强 |
| 可读性 | 中 | 高 (树形清晰) | 低 (黑盒) |
| 可调试 | 易 | 易 (可视化) | 难 |
| 实时性 | 好 | 好 (~10ms tick) | 差 (秒级) |
| 灵活性 | 差 | 中 | 极强 |
| 安全性 | 高 | 高 | 中 |

**BT是FSM的进化版**：解决了"状态爆炸"和"修改困难"两大痛点。

## 工作流程示例

### 场景: "把水杯送到客厅给妈妈"

LLM生成的BT (设计时):
```xml
<Sequence name="送水任务">
  <Subtree name="找水杯">
    <Fallback>
      <CheckMemory key="cup_location"/>
      <Sequence>
        <GoTo target="kitchen"/>
        <ScanForObject obj="cup"/>
      </Sequence>
    </Fallback>
  </Subtree>
  
  <Subtree name="抓取">
    <PrecisionMove distance="0.3"/>
    <CloseGripper/>
    <CheckGrasp/>  <!-- 失败则重试 -->
  </Subtree>
  
  <Subtree name="送达">
    <GoTo target="living_room"/>
    <DetectFace name="妈妈"/>  <!-- LLM叶子 -->
    <Approach distance="0.8"/>
    <Say text="妈，水来了"/>
    <OpenGripper/>
  </Subtree>
</Sequence>
```

执行时BT每50ms tick一次，遇到异常自动走Fallback分支。

## 优势

- **可解释**：每一步执行都看得见，调试可视化
- **确定性强**：树结构 + 优先级清晰
- **实时友好**：不需要每步都LLM (vs 纯Agent)
- **复用性高**：子树可复用 (送水/送药/送遥控器都是"送物品")
- **失败处理优雅**：Fallback节点天然支持重试/降级
- **成熟生态**：BehaviorTree.CPP, py_trees, Groot可视化编辑器

## 缺陷

- **结构化任务才适用**：开放式对话不适合
- **BT本身有学习成本**：Sequence/Fallback/Decorator概念
- **LLM生成BT不稳定**：可能生成无效XML，需要校验+重试
- **动态性受限**：树生成后修改难，需要重生成
- **过度结构化**：简单任务杀鸡用牛刀

## 适用场景

✅ 任务流程相对清晰可枚举
✅ 已经在用ROS 2 (Nav2自带)
✅ 需要严格可调试性
✅ 工业巡检/服务机器人

❌ 开放式对话/陪伴型机器人
❌ 完全不可预测的探索任务

## 实现要点

```bash
# Python版 (适合快速原型)
pip install py_trees py_trees_ros

# C++版 (Nav2集成)
sudo apt install ros-jazzy-behaviortree-cpp
sudo apt install ros-jazzy-groot2  # 可视化编辑器
```

```python
# py_trees 简单示例
import py_trees

class LLMReason(py_trees.behaviour.Behaviour):
    def update(self):
        result = ollama.chat("qwen2.5:3b", self.prompt)
        self.blackboard.set("llm_output", result)
        return py_trees.common.Status.SUCCESS

root = py_trees.composites.Sequence("Patrol", memory=True)
root.add_children([GoTo("kitchen"), LLMReason("describe scene"), GoTo("base")])
tree = py_trees.trees.BehaviourTree(root)
tree.tick_tock(period_ms=100)
```

## 与其他模式的关系

- **可作为模式03(混合脑)的L2行为层** ★ 推荐组合
- **替代模式04的L2** 是BT的本职工作
- **可与模式06 ROS 2** 无缝集成 (Nav2原生支持)

## 一句话评价

**BT是工业界对"如何驯服LLM"的最佳答案。** 用结构化骨架兜住LLM的不确定性。

## 与本项目匹配度

⭐⭐⭐⭐ (4/5) — 强烈推荐作为L2层实现方式。但完整BT生态学习成本不低，Phase 1可先用Python状态机过渡。
