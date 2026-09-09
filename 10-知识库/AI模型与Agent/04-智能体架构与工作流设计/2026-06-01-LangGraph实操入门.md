---
title: LangGraph 实操入门 — 从零到能跑的多 Agent
created: 2026-06-02
updated: 2026-09-09
type: methodology
tags: [agent, methodology]
status: stable
sources: [https://langchain-ai.github.io/langgraph, "本机实测 langgraph 1.2.2"]
---

# LangGraph 实操入门 — 从零到能跑的多 Agent

> 配套概念页：[[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/2026-06-00-Agent编排入门-由浅入深.md|Agent 编排入门（由浅入深）]]。
> **本页所有结构代码在本机 langgraph 1.2.2 实测跑通**（mock 节点验证图骨架）。涉及真实 LLM 的部分已标注「需 API key」，未在本机实跑。

---

## 为什么第一个框架学 LangGraph

- 生态最完整（LangChain 组件 + LangSmith 运维），资料最多
- 图范式是"复杂有状态编排"的事实标准，学会迁移到 MAF Workflows 也快
- 心智模型清晰：**Node 干活，Edge 决定下一步去哪**

代价：图的概念比"对话式"稍抽象。但跨过这道坎，后面所有生产级能力（循环、断点、HITL、持久化）都顺。

---

## 第 1 步：环境搭建

```bash
python3 -m venv lg-venv
source lg-venv/bin/activate          # Windows: lg-venv\Scripts\activate
pip install langgraph                 # 本页实测版本 1.2.2
# 用真实 LLM 时再装：pip install langchain-openai
```

> 只学图骨架不需要任何 API key——这正是 LangGraph 适合初学者的地方：**先把控制流跑通，再接模型**。

---

## 第 2 步：理解三个核心概念

1. **State（状态）** — 一个 `TypedDict`，贯穿整个图，所有节点读写它。
   - 每个字段可配 **reducer** 控制"更新方式"：`operator.add` = 追加/累加（不覆盖）；默认 = 覆盖。
2. **Node（节点）** — 一个普通函数：收 state → 干活 → 返回要更新的字段（dict）。
3. **Edge（边）** — 决定下一步去哪。
   - 普通 edge：A 做完固定去 B
   - **conditional edge**：按运行时 state 动态决定去哪（实现分支/循环）

> 一句话：**Nodes do the work, edges tell what to do next.**

---

## 第 3 步：第一个多 Agent 图（已实测跑通）

场景：研究员 → 文案 → 审核，审核不通过就打回重写（**循环 + 条件分支**）。

```python
from typing import TypedDict, Annotated, Literal
import operator
from langgraph.graph import StateGraph, START, END

# 1) 共享状态:messages 用 reducer 追加,steps_done 累加
class State(TypedDict):
    task: str
    messages: Annotated[list[str], operator.add]
    steps_done: Annotated[int, operator.add]
    route: str

# 2) 三个专职 agent 节点(mock:演示控制流,不调真 LLM)
def researcher(state: State) -> dict:
    return {"messages": [f"[研究员] 查到关于 '{state['task']}' 的资料"], "steps_done": 1}

def writer(state: State) -> dict:
    return {"messages": ["[文案] 基于资料写了初稿"], "steps_done": 1}

def reviewer(state: State) -> dict:
    # 模拟:前两步不够分就打回,够了就通过(演示循环)
    if state["steps_done"] < 4:
        return {"messages": ["[审核] 不合格,打回重写"], "route": "rewrite", "steps_done": 1}
    return {"messages": ["[审核] 通过"], "route": "done", "steps_done": 1}

# 3) supervisor:conditional edge 的判定函数
def route_after_review(state: State) -> Literal["writer", "__end__"]:
    return "writer" if state["route"] == "rewrite" else END

# 4) 组图
g = StateGraph(State)
g.add_node("researcher", researcher)
g.add_node("writer", writer)
g.add_node("reviewer", reviewer)
g.add_edge(START, "researcher")
g.add_edge("researcher", "writer")
g.add_edge("writer", "reviewer")
g.add_conditional_edges("reviewer", route_after_review, {"writer": "writer", END: END})
app = g.compile()

# 5) 执行
result = app.invoke({"task": "AI Agent 编排框架", "messages": [], "steps_done": 0, "route": ""})
for m in result["messages"]:
    print(" ", m)
print(f"总步数: {result['steps_done']} | 最终路由: {result['route']}")
```

**本机实际输出：**
```
  [研究员] 查到关于 'AI Agent 编排框架' 的资料
  [文案] 基于资料写了初稿
  [审核] 不合格,打回重写
  [文案] 基于资料写了初稿
  [审核] 通过
总步数: 5 | 最终路由: done
```

→ 注意第 3-4 行：审核打回后**真的绕回去重写了**。这就是图范式相对旧 AgentExecutor 的核心优势——**循环和分支是你显式定义的，可控可复现**。

---

## 第 4 步：持久化 + 人工介入（HITL，生产级门槛，已实测）

让流程跑到某步**停下等人确认**，再恢复。靠两个东西：**checkpointer**（存状态）+ **interrupt_before**（断点）。

```python
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    counter: Annotated[int, operator.add]
    log: Annotated[list[str], operator.add]

def step_a(state): return {"counter": 1, "log": ["step_a 执行"]}
def step_b(state): return {"counter": 1, "log": ["step_b 执行"]}

g = StateGraph(State)
g.add_node("a", step_a); g.add_node("b", step_b)
g.add_edge(START, "a"); g.add_edge("a", "b"); g.add_edge("b", END)

# 关键:挂 checkpointer + 在 b 前设断点(模拟"等人工确认")
checkpointer = InMemorySaver()
app = g.compile(checkpointer=checkpointer, interrupt_before=["b"])

cfg = {"configurable": {"thread_id": "demo-1"}}   # thread_id 标识一次会话

# 第一次:跑到 b 之前停下
r1 = app.invoke({"counter": 0, "log": []}, cfg)
print("中断时:", r1["counter"], r1["log"])          # b 还没跑

snap = app.get_state(cfg)
print("下一步将执行:", snap.next)                    # 证明状态被存下来了

# 恢复:传 None = 从断点继续
r2 = app.invoke(None, cfg)
print("恢复后:", r2["counter"], r2["log"])
```

**本机实际输出：**
```
中断时: 1 ['step_a 执行']
下一步将执行: ('b',)
恢复后: 2 ['step_a 执行', 'step_b 执行']
```

→ 流程在 `b` 前**真的停住了**（counter 还是 1），`get_state` 能读到"下一步是 b"，传 `None` 后**从断点继续**而不是重头跑。生产里这一停就可以插入"等人工审批""等用户补充信息"。

---

## 第 5 步：接真实 LLM（需 API key，本机未实跑）

把 mock 节点换成真模型调用即可，图结构不变：

```python
# pip install langchain-openai;  export OPENAI_API_KEY=sk-...
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")

def researcher(state: State) -> dict:
    resp = llm.invoke(f"查找关于 {state['task']} 的关键资料,列 3 条")
    return {"messages": [f"[研究员] {resp.content}"], "steps_done": 1}
```

> 换模型只动节点内部，**图骨架（node/edge/state）一行不用改**——这就是"先跑通控制流再接模型"的好处。国内可换成兼容 OpenAI 接口的模型服务（改 `base_url` + `api_key`）。

---

## 第 6 步：进阶方向（学完上面再看）

- **预制多 agent 库**：`langgraph-supervisor`（中心调度）、`langgraph-swarm`（无中心 handoff）——不用手写路由
- **Streaming**：`app.stream(...)` 流式看每步中间结果
- **LangSmith**：设 `LANGSMITH_API_KEY`，自动 trace 每个 agent 怎么想的，调试神器
- **持久化升级**：`InMemorySaver` 换成 SQLite/Postgres checkpointer，状态落库

---

## 常见坑

1. **state 字段不加 reducer 会被覆盖**：想累积消息/列表，必须 `Annotated[list, operator.add]`，否则后一个节点的返回会冲掉前面的。
2. **conditional edge 的返回值要和映射字典对上**：`route_after_review` 返回的字符串/END 必须是 `add_conditional_edges` 第三个参数 dict 的 key。
3. **忘记 compile()**：`StateGraph` 定义完必须 `.compile()` 才能 invoke。
4. **HITL 必须挂 checkpointer**：`interrupt_before` 不配 checkpointer 不生效——状态没地方存就没法恢复。
5. **thread_id 要固定**：恢复执行时 config 的 `thread_id` 必须和中断时一致，否则找不到之前的状态。

---

## 关联阅读
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/2026-06-00-Agent编排入门-由浅入深.md|Agent 编排入门（由浅入深）]] — 先读这篇懂概念
- [[40-调研报告/AI技术与产品/Agent与研发流程/2026-06-Agent编排框架横评-SK-MAF-LangChain.md|Agent 编排框架横评]] — 横向对比 8 个框架
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.2.1-LangGraph深度实操.md|LangGraph 深度实操]] — 库内已有的进阶笔记
