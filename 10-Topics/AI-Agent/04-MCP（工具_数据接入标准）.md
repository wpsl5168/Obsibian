# MCP（工具 / 数据接入标准）（话题页）

> 这页对应 Topic Map 里的：Tools & Integration。

## 一句话结论
MCP（Model Context Protocol）正在成为 agent 工具接入的“USB-C”：**把工具/数据源接入协议化**，让竞争焦点从“谁接得多”转移到“谁更安全、更可治理、更好用”。

## 解决什么问题（落地场景）
- 你要把 agent 接入 N 个系统（GitHub、DB、Drive、内部 API、浏览器……），不想每个系统都写一套私有适配。
- 你要做企业落地：必须回答权限怎么控、审计怎么做、出事怎么回放。
- 你要做生态：希望工具提供方能独立发布/更新，而你的 agent 端接入成本可控。

## 最小可行实现（MVP）
1) 选 1 个真实业务闭环（例如：Issue → 查代码 → 给出 patch 或 PR 草案）。
2) 起一个 MCP Server（只暴露“读操作 + 少量低风险写操作”）：
   - 工具清单：search / get / list（先让 agent 能“找得到”）
   - 输出结构化：尽量返回 JSON（或至少可解析的字段）
3) 在 MCP Client（你的 agent/宿主）侧加 3 件事：
   - 权限/审批：哪些工具调用必须 requireApproval
   - 观测：每次调用记录 input/output/latency/error（便于回放）
   - 降级：超时/限流/失败后的 fallback（例如换检索源、改为只读模式）

## 常见坑（企业/银行视角）
- “协议化 ≠ 安全”：工具接入更容易后，**滥用与注入风险**也会放大；必须把权限/审批/审计做在宿主侧。
- 没有把工具按风险分级：导致要么全放开（风险大），要么全收紧（体验差）。
- 工具返回不结构化：最终 debug 成本暴涨，eval 也做不起来。

## 时间线（技术 / 人物 / 企业 / 背景）
- 2026-03-28：在《AI Agent 研究报告（10 大主题）》里把 MCP 作为“工具/数据接入标准化”的主线之一（对标 USB-C）。
- 2026-04-03：日报把 MCP 明确为生态焦点：工具协议化后，竞争点转移到权限/审计/评测/体验。

## 一手来源（官方 + 顶流原创）
- MCP Intro：<https://modelcontextprotocol.io/docs/getting-started/intro>
- Anthropic 官方发布：<https://www.anthropic.com/news/model-context-protocol>
- Simon Willison（MCP 相关文章聚合）：<https://simonwillison.net/tags/model-context-protocol/>

## 关联条目（本知识库）
- [[AI-Agent-Daily/2026-04-03]]（MCP 生态要点）
- [[10-Topics/AI-Agent/Research/2026-03-29-AI-Agent-研究报告]]（主题 4：MCP）

## 更新记录
- 2026-04-07：补齐“6 段固定结构”（一句话结论 / 场景 / MVP / 坑 / 时间线 / 一手来源），并挂接日报与研究报告。

