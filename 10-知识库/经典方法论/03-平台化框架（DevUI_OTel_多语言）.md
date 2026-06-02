---
title: "03-平台化框架（DevUI_OTel_多语言）"
created: 2026-03-28
updated: 2026-06-02
type: methodology
tags: [methodology, architecture, tooling]
status: draft
date: 2026-04-08
category: Notes
---

# 03-平台化框架（DevUI_OTel_多语言）

## 1. 核心概念

平台化是将AI Agent能力**标准化、可复用、多语言支持**的工程模式。相比"每个项目从零写Agent代码",平台化通过**统一DevUI、OpenTelemetry可观测性、多语言SDK**让Agent成为基础设施。

**三大支柱**:

| 支柱 | 作用 | 类比(.NET/SQL) |
|------|------|---------------|
| **DevUI** | 开发者界面,可视化Agent执行流程 | Visual Studio调试器(断点/Watch/调用栈) |
| **OpenTelemetry** | 分布式追踪,Agent每步都emit span | SQL Server Profiler + Extended Events |
| **多语言SDK** | Python/C#/Java/Go统一接口 | .NET Standard跨运行时 |

**为什么需要平台化?** 散装Agent代码的痛点:
- **不可观测**: LLM调用是黑盒,出错不知道哪一步失败
- **语言锁定**: Python生态丰富但企业.NET栈无法复用
- **重复造轮**: 每个项目重写retry/checkpoint/state管理

平台化通过**抽象层**统一这些能力,让业务团队只需关注Agent逻辑。

## 2. 解决的问题

| 生产痛点 | 平台化方案 |
|---------|-----------|
| **Agent调试困难** | DevUI可视化执行图 + 单步调试 + 状态快照 |
| **多语言异构** | 统一SDK抽象(类似gRPC protobuf跨语言) |
| **监控盲区** | OTel自动埋点,每个Agent节点自动emit span |
| **无法重放** | Checkpoint + trace录制,可本地重放生产case |
| **跨团队协作** | 统一Agent Registry,版本管理,API约定 |

**实际案例**(银行贷款审批Agent):
- **改造前**: Python脚本跑在Lambda,C#后台看不到执行细节,出错只能看CloudWatch日志猜
- **改造后**: Agent注册到平台,C# dashboard通过OTel trace实时看到"征信查询→风控评分→人工复核"每步延迟,P95从3.2秒优化到1.1秒

## 3. 代表项目/论文/框架(链接)

### 3.1 平台级框架(2026生产主流)

| 框架 | 特点 | 适用场景 |
|------|------|---------|
| **[Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/)** | .NET原生,Azure集成,DevUI内置OTel | 企业级.NET栈,Azure客户 |
| **[Dapr](https://dapr.io/)** | 微服务抽象层,多语言SDK(8种) | 云中立,Kubernetes部署 |
| **[LangGraph Platform](https://langchain-ai.github.io/langgraph/cloud/)** | LangGraph Cloud托管,内置trace | Python团队,快速上线 |
| **[Temporal Cloud](https://temporal.io/)** | Durable execution,金融级可靠性 | 长时任务,合规要求高 |

**选型指南**:
- **.NET栈** → Microsoft Agent Framework(一等公民支持)
- **多云/云中立** → Dapr(K8s + 多语言SDK)
- **Python快速原型** → LangGraph Platform
- **金融/合规** → Temporal(ACID级durability)

### 3.2 DevUI工具

| 工具 | 能力 | 集成 |
|------|------|------|
| **LangGraph Studio** | 可视化状态机,单步调试,checkpoint查看 | LangGraph原生 |
| **Microsoft Agent DevUI** | OTel trace可视化,实时状态监控 | .NET Agent Framework |
| **Temporal Web UI** | 工作流历史,重放,失败分析 | Temporal |

### 3.3 OpenTelemetry生态

- **[OpenTelemetry Python SDK](https://opentelemetry.io/docs/languages/python/)**: Agent自动埋点
- **[Jaeger](https://www.jaegertracing.io/)**: 分布式追踪UI(开源)
- **[Grafana Tempo](https://grafana.com/oss/tempo/)**: 云原生trace存储
- **[Datadog APM](https://www.datadoghq.com/product/apm/)**: 商业SaaS,开箱即用

**OTel采纳度**(CNCF 2026调查):
- 67%生产AI系统已用OTel(2025年仅31%)
- 主要原因:Agent比传统API复杂10倍,没trace根本调不了

## 4. 工程落地清单(Checklist)

### 4.1 架构选型决策树

```
团队技术栈?
├─ .NET主导(C#/ASP.NET)        → Microsoft Agent Framework
├─ Python主导(Django/FastAPI)  → LangGraph Platform
├─ 多语言异构(Java+Python+Go)  → Dapr
├─ 合规/金融                   → Temporal
└─ 云中立(多云部署)             → Dapr + K8s
```

### 4.2 DevUI集成规范

**最小DevUI能力**(必需):
- **执行图可视化**: DAG/状态机的实时渲染
- **单步调试**: 暂停Agent,查看当前state
- **历史回放**: 从checkpoint重放任意时间点
- **性能剖析**: 每个节点的延迟分布(P50/P95/P99)

**实现示例**(LangGraph):
```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

# DevUI需要checkpoint才能回放
checkpointer = SqliteSaver.from_conn_string("agent_state.db")
builder = StateGraph(MyState)
# ... 添加节点
graph = builder.compile(checkpointer=checkpointer)

# 执行后可在LangGraph Studio可视化
```

### 4.3 OpenTelemetry埋点标准

**Agent span命名约定**(遵循semantic conventions):
```
agent.node.<node_name>          # Agent节点
agent.tool.<tool_name>          # 工具调用
agent.llm.<model_name>          # LLM推理
agent.memory.read / .write      # 记忆操作
```

**自动埋点示例**(Python):
```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# 配置OTel
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(
    endpoint="http://jaeger:4317"
))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# Agent节点自动埋点
def my_agent_node(state):
    with tracer.start_as_current_span("agent.node.my_node") as span:
        span.set_attribute("input_tokens", len(state["input"]))
        # ... 节点逻辑
        span.set_attribute("output_tokens", len(result))
        span.set_attribute("llm_model", "claude-sonnet-4.5")
        return result
```

**关键属性**(必须记录):
- `input_tokens` / `output_tokens`: 成本追踪
- `llm_model`: 多模型对比
- `tool_name` / `tool_args`: 调试工具调用
- `error`: 失败原因

### 4.4 多语言SDK设计

**接口统一原则**(类似.NET Standard):
```python
# Python SDK
class Agent:
    async def run(self, input: dict) -> dict: ...
    def add_tool(self, tool: Tool) -> None: ...
    def checkpoint(self) -> bytes: ...
```

```csharp
// C# SDK (同样接口)
public interface IAgent {
    Task<Dictionary<string, object>> RunAsync(Dictionary<string, object> input);
    void AddTool(ITool tool);
    byte[] Checkpoint();
}
```

**实际案例**(Dapr Actor模型):
- Python Agent发布到Dapr
- C#后台通过Dapr SDK调用,无需关心语言差异
- 序列化协议: JSON或Protobuf

### 4.5 成本控制门禁

| 门禁 | 阈值 | 触发动作 |
|------|------|---------|
| **单次运行token上限** | 500K tokens | 强制终止 + 告警 |
| **并发Agent数** | 50个 | 排队等待空闲slot |
| **每日预算** | $500 | 超过则暂停所有Agent |
| **单Agent延迟** | P95 > 30s | 自动降级到更快模型 |

**监控dashboard**(Grafana模板):
- 实时token消耗速率(tokens/min)
- 成本趋势($/day)
- 并发度热力图
- 失败率按Agent分组

### 4.6 测试与质量保证

**平台化测试金字塔**:
```
E2E集成测试(5%)
   ↑
 Agent行为测试(20%)
   ↑
 节点单元测试(75%)
```

**Replay测试**(关键能力):
```python
# 从生产trace重放,验证修复后行为
def test_agent_replay():
    checkpoint = load_checkpoint("prod_failure_20260602.pkl")
    agent = MyAgent()
    result = agent.replay(checkpoint)
    assert result["status"] == "success"
```

**CI/CD门禁**:
- 新Agent提交 → 自动跑100个回归case
- trace对比: 新版本vs旧版本的决策路径diff
- 成本回归: 新版本token消耗不能>旧版本20%

## 5. 更新记录

| 日期 | 更新内容 |
|------|---------|
| 2026-06-02 | 补充完整内容: 平台化三大支柱(DevUI/OTel/多语言SDK)、2026框架对比(Microsoft/Dapr/LangGraph/Temporal)、落地清单(架构决策树/OTel埋点标准/成本门禁/Replay测试) |
| 2026-04-08 | 初始版本(空骨架) |
