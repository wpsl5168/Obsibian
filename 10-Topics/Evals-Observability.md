# Evals & Observability（话题页）

> 目标：把“可观测 + 可评测”作为 agent 工程化的地基沉淀下来。

## 为什么这是地基
- 没 tracing：线上失败不可复现
- 没 evals：每次改 prompt/工具/模型都在赌博（质量回归不可控）

## 我关注的主线（长期）
- Tracing：OpenTelemetry 语义、span 结构、跨工具链关联（request_id/task_id）
- Evals：回归集、任务集、判分标准（自动+人工）、成本控制
- “产物驱动”：把 agent 的输出定义成 artifact（PR、文档、报表），评测围绕 artifact

## 一手/权威入口
- Microsoft Agent Framework（官方博客/RC，强调 workflow+OTel）：
  - <https://devblogs.microsoft.com/foundry/microsoft-agent-framework-reaches-release-candidate/>
-（后续补充你指定的 eval 平台官方入口：LangSmith/Braintrust/Weights&Biases/Arize/...）
