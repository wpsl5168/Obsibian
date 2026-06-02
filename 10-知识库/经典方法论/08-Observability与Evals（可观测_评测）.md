---
title: "08-Observability与Evals（可观测_评测）"
created: 2026-03-28
updated: 2026-06-02
type: methodology
tags: [methodology, evaluation, architecture]
status: draft
date: 2026-04-08
category: Notes
---

# 08-Observability与Evals（可观测_评测）

## 1. 核心概念

Observability(可观测性)是**看清Agent做了什么**,Evals(评测)是**判断Agent做得对不对**。两者是生产AI系统的双引擎:没有Observability调不了bug,没有Evals量化不了进步。

**核心区别**:

| 维度 | Observability(观测) | Evals(评测) |
|------|-------------------|------------|
| **时机** | 运行时/生产环境 | 开发时/预发布 |
| **目的** | 调试、监控、根因分析 | 质量门禁、回归测试、优化方向 |
| **输出** | Trace、日志、指标 | 分数、Pass/Fail、对比报告 |
| **类比(.NET/SQL)** | SQL Profiler + Application Insights | 单元测试 + 性能基准测试 |

**为什么需要?** 传统软件栈的observability(APM/日志)对Agent无效:
- **无法溯源决策**: 看到结果是错的,但不知道Agent哪步推理偏了
- **多步黑盒**: Agent调用10个工具,每个工具返回不同内容,传统日志只能看到HTTP 200
- **评测缺失**: 单元测试验证函数输出,但怎么测Agent"推理质量"?

## 2. 解决的问题

| 生产痛点 | Observability方案 | Evals方案 |
|---------|------------------|-----------|
| **Agent调试难** | 结构化trace记录每步Thought/Action/Observation | N/A |
| **性能瓶颈定位** | 每个节点延迟分布(P50/P95/P99) | N/A |
| **成本爆炸** | 实时token消耗监控,按Agent分组 | Prompt优化前后cost对比 |
| **回归风险** | N/A | 100+测试case,新版本vs旧版本 |
| **质量无量化** | N/A | Correctness/Relevance/Hallucination评分 |
| **工具误调** | Trace显示工具名、参数、返回值 | Tool selection accuracy指标 |

**实际案例**(客服Agent):
- **观测**: 发现P95延迟15秒 → trace定位到"知识库检索"节点占9秒 → 优化索引后降到2秒
- **评测**: 100个真实对话回放 → 发现新版本hallucination从3%升到12% → 回滚prompt改动

## 3. 代表项目/论文/框架(链接)

### 3.1 Observability平台(2026生产级)

| 平台 | 核心能力 | 适用场景 | 定价 |
|------|---------|---------|------|
| **[Braintrust](https://braintrust.dev/)** | Agent trace + 生产评分 + CI/CD | 全栈(观测+评测一体) | $99/月起 |
| **[LangSmith](https://smith.langchain.com/)** | LangChain原生trace,调试友好 | LangChain/LangGraph用户 | $39/月起 |
| **[W&B Weave](https://wandb.ai/site/weave)** | Agent trace + 实验对比 | 研究团队、模型迭代 | 免费tier / $50/月 |
| **[Arize Phoenix](https://phoenix.arize.com/)** | 开源、OTel原生、自托管 | 隐私要求高、自建平台 | 免费开源 |
| **[Helicone](https://helicone.ai/)** | 轻量代理、成本追踪 | 小团队、快速上手 | $29/月起 |

**选型实战**(Alice Labs经验):
- **LangChain栈** → LangSmith(原生集成、调试体验最佳)
- **多框架混用** → Braintrust(框架无关、评测能力强)
- **自托管需求** → Arize Phoenix(开源、OTel标准)
- **预算有限** → Helicone(最便宜、功能够用)

### 3.2 Evals框架

| 框架 | 评测类型 | 特点 |
|------|---------|------|
| **[Truesight](https://truesight.ai/)** | 领域专家grounded评测 | 专家标注,高质量ground truth |
| **[DeepEval](https://deepeval.ai/)** | 指标库(30+) | 开源、预置评测器(G-Eval/RAGAS等) |
| **[Promptfoo](https://promptfoo.dev/)** | Prompt对比 | 多版本prompt并行测试 |
| **[RAGAS](https://ragas.io/)** | RAG专项评测 | Faithfulness/Context Recall/Precision |

**评测指标金字塔**(从简单到复杂):
1. **精确匹配**(Exact Match): 答案是否完全一致 → 适用于事实性QA
2. **语义相似度**(Semantic Similarity): 用embedding计算cos距离 → 适用于paraphrase
3. **LLM-as-Judge**: 用GPT-4评分0-10 → 适用于开放式生成
4. **人类标注**(Human Eval): 专家打分 → 金标准但昂贵

### 3.3 工具链整合

**标准栈**(2026推荐):
```
生产流量
   ↓
[LangSmith/Braintrust] ← 记录trace
   ↓
[Trace → Dataset] ← 转换成测试集
   ↓
[DeepEval/RAGAS] ← 批量评测
   ↓
[CI/CD质量门禁] ← 分数<80%拒绝部署
```

**OpenTelemetry标准**(互操作性):
- Trace导出到Jaeger/Tempo → 统一可视化
- Span属性标准化 → 跨平台对比
- 自定义exporter → 写入自建系统

## 4. 工程落地清单(Checklist)

### 4.1 Observability埋点标准

**Agent Span属性**(必需字段):
```python
{
  "agent.id": "customer-service-agent-v2",
  "agent.session_id": "sess_20260602_abc123",
  "agent.step": 3,  # 第几步
  "agent.thought": "用户询问退款政策,需查询知识库",
  "agent.action": "search_knowledge_base",
  "agent.action_input": '{"query": "退款政策"}',
  "agent.observation": "找到3条相关文档...",
  "llm.model": "claude-sonnet-4.5",
  "llm.input_tokens": 1234,
  "llm.output_tokens": 567,
  "llm.cost_usd": 0.012,
  "tool.name": "search_knowledge_base",
  "tool.args": '{"query": "退款政策", "top_k": 5}',
  "tool.result": "[doc1, doc2, doc3]",
  "tool.latency_ms": 450
}
```

**Trace结构**(嵌套span):
```
agent.session [总span]
  ├─ agent.step.1
  │   ├─ llm.call (推理)
  │   └─ tool.search (工具调用)
  ├─ agent.step.2
  │   ├─ llm.call
  │   └─ tool.fetch_policy
  └─ agent.step.3 (最终答复)
      └─ llm.call
```

### 4.2 关键指标监控

**三类指标**(SLI体系):

| 类别 | 指标 | 阈值示例 |
|------|------|---------|
| **性能** | P95 latency | <5秒 |
| | Token throughput | >1000 tok/s |
| **质量** | Hallucination rate | <5% |
| | Tool selection accuracy | >90% |
| | Task success rate | >85% |
| **成本** | Cost per session | <$0.50 |
| | Daily budget burn | <$500 |

**Dashboard模板**(Grafana):
```
[Agent健康度总览]
├─ 成功率(24h): 87.3% ↑2.1%
├─ P95延迟: 4.2s ↓0.3s
├─ 成本/请求: $0.32 ↓$0.05
└─ 活跃Agent: 12个

[Top故障原因]
1. 工具超时 (23%)
2. LLM rate limit (18%)
3. 上下文溢出 (15%)
```

### 4.3 Evals测试套件设计

**三层测试金字塔**:
```
E2E场景测试(10个case)
   ↑ 复杂业务流程,端到端
Agent行为测试(50个case)
   ↑ 工具选择、推理路径
单元测试(200个case)
   ↑ Prompt输出格式、工具函数
```

**Regression测试模板**:
```python
import deepeval
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

# 从生产trace生成测试case
def test_customer_refund_policy():
    test_case = LLMTestCase(
        input="如何申请退款?",
        actual_output=agent.run("如何申请退款?"),
        expected_output="根据退款政策,您可以在购买后7天内...",
        retrieval_context=["退款政策文档v3.2"]
    )
    
    metric = AnswerRelevancyMetric(threshold=0.8)
    assert metric.measure(test_case) > 0.8
```

### 4.4 CI/CD质量门禁

**Pre-merge检查**(GitHub Actions):
```yaml
name: Agent Quality Gate
on: [pull_request]
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - name: Run eval suite
        run: pytest tests/evals/
      
      - name: Compare with baseline
        run: |
          # 新版本vs main分支
          python compare_evals.py \
            --baseline main \
            --current ${{ github.sha }}
      
      - name: Quality gate
        run: |
          # 分数下降>5%则失败
          if [ $SCORE_DROP -gt 5 ]; then
            echo "Quality regression detected!"
            exit 1
          fi
```

**部署门禁**:
- ✅ Eval分数 ≥ baseline
- ✅ P95延迟 ≤ baseline + 20%
- ✅ 成本 ≤ baseline + 10%
- ✅ 无CRITICAL级别trace error

### 4.5 Trace → Dataset转换

**生产数据利用**(黄金闭环):
```python
# 1. 从生产trace提取case
def extract_test_cases_from_traces():
    traces = langsmith_client.list_runs(
        project="prod-agent",
        filter="status='success' AND user_rating>=4"  # 只要好评case
    )
    
    test_cases = []
    for trace in traces:
        test_cases.append({
            "input": trace.inputs["query"],
            "expected_output": trace.outputs["response"],
            "context": trace.extra["retrieved_docs"]
        })
    
    return test_cases

# 2. 写入eval数据集
dataset = deepeval.Dataset(test_cases)
dataset.save("prod_golden_set_20260602.json")

# 3. 每周更新回归测试
# cron: 0 0 * * 0 (周日更新)
```

### 4.6 成本归因分析

**成本拆解**(按维度):
```sql
-- 假设trace存在ClickHouse
SELECT
  agent_id,
  DATE(timestamp) as date,
  SUM(llm_input_tokens + llm_output_tokens) as total_tokens,
  SUM(llm_cost_usd) as total_cost,
  COUNT(*) as num_sessions,
  AVG(llm_cost_usd) as avg_cost_per_session
FROM agent_traces
WHERE date >= '2026-06-01'
GROUP BY agent_id, date
ORDER BY total_cost DESC
```

**优化策略**(ROI排序):
1. **最贵Agent先优化** → 80/20法则,top 3 Agent占60%成本
2. **Prompt缓存收益** → 重复上下文场景(客服FAQ)收益>50%
3. **模型降级** → 简单query用Haiku,复杂才上Opus
4. **上下文裁剪** → RAG结果只取top-3,不要塞10条

### 4.7 告警与SLO

**告警规则**(分级):
```yaml
alerts:
  - name: Agent延迟异常
    condition: p95_latency > 10s for 5min
    severity: warning
    action: slack通知
  
  - name: 成功率暴跌
    condition: success_rate < 70% for 2min
    severity: critical
    action: PagerDuty唤醒oncall
  
  - name: 成本超支
    condition: daily_cost > $500
    severity: critical
    action: 自动暂停Agent + 通知财务
```

**SLO定义**(99.9%可用性 = 月43.8分钟downtime):
- **可用性SLO**: 99.0% (月7.2小时downtime可接受)
- **延迟SLO**: 95%请求 <5秒
- **质量SLO**: 90%会话用户满意(4星+)

## 5. 更新记录

| 日期 | 更新内容 |
|------|---------|
| 2026-06-02 | 补充完整内容: Observability vs Evals核心区别、2026平台排名(Braintrust/LangSmith/W&B/Phoenix)、落地清单(埋点标准/三类指标/Evals金字塔/CI门禁/成本归因/告警SLO) |
| 2026-04-08 | 初始版本(空骨架) |
