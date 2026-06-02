---
title: "10-经典方法论（ReAct_Reflexion_ToT_MetaGPT）"
created: 2026-03-28
updated: 2026-06-02
type: methodology
tags: [methodology, agent, prompt]
status: draft
date: 2026-04-08
category: Notes
---

# 10-经典方法论（ReAct_Reflexion_ToT_MetaGPT）

## 1. 核心概念

AI Agent推理方法论是**结构化思考框架**，定义Agent如何分析、决策和自适应。相比原始的"给个Prompt就跑"，这些方法论通过**显式推理步骤**大幅提升任务完成率。

四大经典方法论：

| 方法论 | 核心机制 | 适用场景 |
|-------|---------|---------|
| **ReAct** | Reasoning（推理）+ Action（行动）循环 | 需要工具调用的任务（搜索/计算/API） |
| **Reflexion** | Self-Reflection（自我反思）+ 经验记忆 | 多次尝试可优化的任务（代码生成/规划） |
| **Tree-of-Thoughts (ToT)** | 并行探索多条推理路径，剪枝劣解 | 策略性决策（游戏/数学证明） |
| **MetaGPT** | 软件公司角色模拟（PM/Dev/QA） | 端到端软件开发 |

**类比**（.NET/SQL）：
- **ReAct** = SSRS报表设计器的"预览→调参→重新预览"循环
- **Reflexion** = SQL Server Profiler抓trace→分析→优化索引→重跑查询的性能调优循环
- **ToT** = SQL优化器的执行计划并行探索（评估cost后选最优）
- **MetaGPT** = TFS/Azure DevOps的角色工作流自动化

## 2. 解决的问题

| 朴素Prompt痛点 | 方法论方案 |
|---------------|----------|
| **幻觉与错误推理** | 单次生成无法纠错 | ReAct: Observation反馈修正推理；Reflexion: 自我批判+重试 |
| **工具调用失序** | 不知何时该调工具 | ReAct: Thought → Action → Observation显式步骤 |
| **局部最优解** | 只探索一条路径 | ToT: 并行探索N条分支，剪枝+回溯 |
| **复杂任务无结构** | 长任务一锅炖 | MetaGPT: 按软件公司流程拆解（PRD→设计→代码→测试） |
| **无法从失败学习** | 每次重跑从头来 | Reflexion: 存储失败经验到记忆，避免重蹈覆辙 |

**实际案例**（HumanEval代码生成）：
- 朴素Prompt: 65% pass@1
- ReAct: 71%（工具调用+观察修正）
- Reflexion: 91%（3次迭代，每次反思优化）

## 3. 代表项目/论文/框架（链接）

### 3.1 ReAct（Reason + Act）

**论文**：[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)（Yao et al., 2023）

**核心思想**：交替进行**推理（Thought）→ 行动（Action）→ 观察（Observation）**循环。

**Prompt模板**：
```
Question: What is the elevation of the highest peak in the Himalayas?

Thought 1: I need to find which peak is highest in the Himalayas.
Action 1: Search[highest peak Himalayas]
Observation 1: Mount Everest is the highest peak at 8,849 meters.

Thought 2: Now I need to confirm the exact elevation.
Action 2: Lookup[Mount Everest elevation]
Observation 2: 8,849 meters (29,032 feet).

Thought 3: I have the answer.
Action 3: Finish[8,849 meters]
```

**框架实现**：
- [LangChain ReAct Agent](https://python.langchain.com/docs/modules/agents/agent_types/react)
- [Claude Code](https://docs.anthropic.com/claude/docs/agents-sdk)（底层用ReAct循环）
- [OpenAI Agents SDK](https://platform.openai.com/docs/agents)

**落地要点**：
- **Action要幂等**：重复调用同一工具结果应一致
- **循环上限**：15-20步强制终止，避免无限循环
- **Observation截断**：工具返回超过2K tokens需摘要，防止context爆炸

### 3.2 Reflexion（Self-Reflection）

**论文**：[Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)（Shinn et al., 2023）

**核心思想**：任务失败后**自我批判（Self-Reflection）**，生成教训存入记忆，下次尝试时利用。

**三步循环**：
1. **Actor**：尝试完成任务（如生成代码）
2. **Evaluator**：执行测试，判断成功/失败
3. **Reflector**：失败时生成反思（"哪里错了，下次怎么改"），存入短期记忆

**Prompt模板**（代码生成场景）：
```
Attempt 1:
Code: def fibonacci(n): return n + 1
Test Result: Failed (expected [0,1,1,2,3,5], got [1,2,3,4,5,6])

Reflection: My implementation was completely wrong. I added 1 instead of computing the actual Fibonacci sequence. Next time, I should:
1. Remember base cases: fib(0)=0, fib(1)=1
2. Use recursion or iteration: fib(n) = fib(n-1) + fib(n-2)

Attempt 2 (with reflection memory):
Code: def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)
Test Result: Success
```

**框架支持**：
- [ReflexionAgent](https://github.com/noahshinn/reflexion)（原论文实现）
- LangChain + [MemGPT](https://memgpt.ai/)（长期记忆管理）

**落地要点**：
- **记忆TTL**：反思存Redis，72小时过期（避免过时经验误导）
- **相似性检索**：新任务时向量搜索历史反思，找最相关的教训
- **迭代上限**：最多3次重试，否则escalate给人类

### 3.3 Tree-of-Thoughts (ToT)

**论文**：[Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601)（Yao et al., 2023）

**核心思想**：LLM生成**多条候选推理路径**（树的分支），每步评估质量，剪枝差的，保留好的，最终回溯找最优解。

**类比**：SQL优化器的执行计划探索（生成多个plan → cost估算 → 选cost最小的）

**四步流程**：
1. **Thought Generation**：每步生成k个候选思路（如k=3）
2. **State Evaluation**：LLM自评或外部评估器打分
3. **Pruning**：保留top-b个最佳分支（如b=2）
4. **Backtracking**：死路时回到上一步选次优分支

**示例**（24点游戏：用4个数字组合算出24）：
```
Input: 4, 9, 10, 13

Thought Tree:
├─ Branch 1: (13-9) * (10-4) = 4*6 = 24 ✅
├─ Branch 2: (10-4) * (13-9) = 6*4 = 24 ✅
└─ Branch 3: 13*4 - 10*9 = 52-90 = -38 ❌ (pruned)

Best Path: Branch 1 or 2 (both valid)
```

**框架实现**：
- [tree-of-thought-llm](https://github.com/princeton-nlp/tree-of-thought-llm)（原论文代码）
- [LangChain ToT](https://python.langchain.com/docs/use_cases/more/agents/tree_of_thought)

**落地要点**：
- **评估函数关键**：可用LLM打分（"这个思路可行吗？0-10分"）或规则（通过单测得分）
- **BFS vs DFS**：广度优先适合短路径，深度优先适合深层探索
- **成本控制**：k=5，深度=3 → 5³=125次LLM调用，必须设预算上限

### 3.4 MetaGPT（Multi-Agent Software Company）

**论文**：[MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352)（Hong et al., 2023）

**核心思想**：模拟**软件公司角色分工**（PM写PRD → 架构师设计 → 工程师编码 → QA测试），每个角色是一个专家Agent。

**角色与SOP**（Standard Operating Procedure）：

| 角色 | 输入 | 输出 | 类比 |
|------|------|------|------|
| **Product Manager** | 用户需求 | PRD（Product Requirement Document） | Azure DevOps User Story |
| **Architect** | PRD | 系统设计文档（架构图/API设计） | .NET Solution架构 |
| **Engineer** | 设计文档 | 代码实现 | Visual Studio开发 |
| **QA Engineer** | 代码 | 测试用例 + Bug报告 | xUnit/NUnit测试 |

**工作流**：
```
用户需求 → PM Agent → PRD
         → Architect Agent → 设计文档
         → Engineer Agent → 代码
         → QA Agent → 测试报告
         → （如有bug）→ Engineer修复 → 重测
```

**框架**：[MetaGPT GitHub](https://github.com/geekan/MetaGPT)（8K+ stars，2026年活跃）

**示例命令**：
```bash
# 安装
pip install metagpt

# 运行
metagpt "Write a snake game with pygame"

# 输出：
# - docs/prd.md
# - docs/system_design.md
# - snake_game/main.py
# - snake_game/tests/test_main.py
```

**落地要点**：
- **适合绿地项目**：端到端生成新项目，不适合改既有代码库
- **需要人类审查**：生成的PRD/设计必须review，不可盲目执行
- **成本高**：一个任务调用4-5个Agent，每个Agent多轮对话，单次$1-5

### 3.5 混合模式（Plan-and-Execute + Hierarchical）

**Plan-and-Execute**：
- **规划阶段**：LLM生成任务DAG（"先搜索→再摘要→最后写报告"）
- **执行阶段**：按图执行，每个节点调ReAct Agent

**Hierarchical Agent**：
- **上层Manager Agent**：分解任务，派发给下层Worker Agent
- **下层Worker Agent**：专家（研究/写作/编码）
- 类比：TFS的Epic → Feature → Task层级

## 4. 工程落地清单（Checklist）

### 4.1 方法论选型决策树

```
任务类型？
├─ 需要调用外部工具（搜索/计算/API）   → ReAct
├─ 多次尝试可优化（代码/规划）         → Reflexion
├─ 策略性决策（游戏/数学证明）         → ToT
├─ 端到端软件开发                    → MetaGPT
└─ 复杂任务需分解                    → Plan-and-Execute
```

### 4.2 ReAct实现Checklist

```python
# LangChain ReAct Agent示例
from langchain.agents import create_react_agent
from langchain.tools import Tool

tools = [
    Tool(name="Search", func=search_api, description="Search the web"),
    Tool(name="Calculator", func=calculator, description="Do math")
]

agent = create_react_agent(
    llm=llm,
    tools=tools,
    max_iterations=15,  # 防无限循环
    early_stopping_method="generate"  # 超时生成结果而非报错
)

result = agent.invoke({"input": "What is 25% of the GDP of France?"})
```

**关键配置**：
- `max_iterations=15`：最多15步，超过强制终止
- `return_intermediate_steps=True`：调试时看每步Thought/Action
- 工具描述要精准：LLM通过description选工具，写错选不到

### 4.3 Reflexion记忆管理

```python
# 伪代码：Reflexion循环
memory = []  # 历史反思

for attempt in range(3):
    # Actor: 尝试任务（带上历史教训）
    code = llm.generate(task_prompt + "\n".join(memory))
    
    # Evaluator: 测试
    test_result = run_tests(code)
    
    if test_result.passed:
        break
    
    # Reflector: 反思
    reflection = llm.generate(f"""
    Task: {task_prompt}
    Code: {code}
    Test Failed: {test_result.error}
    
    What went wrong? How to fix next time?
    """)
    memory.append(reflection)
```

**存储方案**：
- **短期记忆**（当前任务）：Python list
- **长期记忆**（跨会话）：Redis + 向量数据库（Pinecone/Qdrant）
  - Key: `reflexion:{task_type}:{hash(task)}`
  - Embedding: 用`text-embedding-ada-002`向量化反思
  - 检索: 新任务时cosine相似度搜索top-3历史教训

### 4.4 ToT成本控制

| 参数 | 保守 | 平衡 | 激进 |
|------|------|------|------|
| **分支数k** | 2 | 3 | 5 |
| **深度d** | 2 | 3 | 4 |
| **保留b** | 1 | 2 | 3 |
| **LLM调用次数** | k^d = 4 | k^d = 27 | k^d = 625 |
| **成本（gpt-4）** | $0.08 | $0.54 | $12.50 |

**优化策略**：
- **早停**：某分支得10分（满分），立即返回，不再探索
- **启发式剪枝**：低于5分的分支直接丢弃
- **缓存**：相同子问题不重复计算

### 4.5 MetaGPT配置

```python
# MetaGPT配置文件示例
from metagpt.config import Config
from metagpt.team import Team

config = Config.default()
config.llm.api_type = "azure"  # 或 "openai"
config.llm.model = "gpt-4"

team = Team()
team.hire([
    ProductManager(),
    Architect(),
    Engineer(),
    QAEngineer()
])

team.invest(investment=5.0)  # 预算$5
team.run_project(idea="Build a CLI tool for git commit message generation")
```

**成本控制**：
- `investment`参数限制总花费
- 超预算自动降级模型（gpt-4 → gpt-3.5）
- 可禁用某些角色（如跳过QA直接出代码）

### 4.6 监控与调试

| 指标 | 工具 | 告警阈值 |
|------|------|---------|
| **平均迭代次数** | LangSmith Tracing | >10次（可能陷入循环） |
| **工具调用失败率** | OpenTelemetry | >20%（工具不稳定） |
| **Reflexion收敛率** | 自定义日志 | 3次尝试仍失败 → escalate |
| **ToT剪枝率** | 日志 | <30%（分支太少，探索不足） |

**调试技巧**：
- **可视化推理树**：用Graphviz画ToT的搜索树
- **Replay失败案例**：保存输入+中间步骤，本地重放调试
- **对比基线**：同任务跑朴素Prompt vs 方法论，量化提升

## 5. 更新记录

| 日期 | 更新内容 |
|------|---------|
| 2026-06-02 | 补充四大方法论（ReAct/Reflexion/ToT/MetaGPT）核心概念、论文链接、代码示例、HumanEval实际提升数据、工程落地清单（选型/成本控制/监控） |
| 2026-04-08 | 初始版本（空骨架） |
