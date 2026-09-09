---
title: The AI-Native SDLC Playbook：摘要与裁决
created: 2026-09-05
updated: 2026-09-09
type: research
tags: [agent, methodology, research, workflow]
status: stable
---

# The AI-Native SDLC Playbook：摘要与裁决

> [打开交互式流程页](../../agent/AI-Native-SDLC%E4%BA%A4%E4%BA%92%E6%B5%81%E7%A8%8B.html)  
> HTML 为单文件，可离线打开；Markdown 正文用于 Obsidian 检索与双链。

## 一句话裁决

这不是一篇“怎样让 AI 多写代码”的教程，而是一套 **artifact-driven control plane**：把需求、设计、实施、验证、审批、生产反馈都变成 Agent 可读、Git 可审计、规则可强制的连续闭环。方向对，机制也够具体；但它仍是 Anthropic 的厂商 playbook，不是已被数据证明有效的通用方法论。[1]

## 原文主张

文章判断：Agent 已显著压缩 Build 时间，因此瓶颈转移到 Plan、Review/Test、Deploy；如果这些阶段仍靠人工交接和委员会节奏，AI 写码的收益会被吞掉。[1]

它把六阶段串成一条版本化 artifact 链：

- Plan：原始想法经追问形成 `intent.md`，Product Owner 审批。
- Design：Agent 结合品牌、安全、合规、UX skills 生成 `spec.md`。
- Build：先在 plan mode 形成 `plan.md`，再实施；`CLAUDE.md` 保存 repo 知识，skills 提供规则，hooks 提供硬约束。
- Test：Agent 在交人前自行运行 build/test/视觉验证；Agent 配置本身用 continuous evals 回归测试。
- Deploy：按 `REVIEW.md` 做多轮 AI review，人只聚焦 intent、risk 和高风险审批；managed settings、sandbox、hooks、branch protection 构成边界。
- Maintain：确定性监控发现 control-band breach 后触发 Agent；Agent 诊断并写回新的 `intent.md`，重新进入循环。[1]

## 核心判断

文章最有价值的不是“六阶段”，而是三个控制原则：

1. **交接靠 artifact，不靠聊天上下文。** 每阶段的输出既是下阶段输入，也是审计记录。
2. **软规则与硬控制分层。** Prompt/skill 只能引导；必须遵守的策略交给 hook、sandbox、权限和 branch protection。
3. **Human-in-the-loop 改为 Human-on-the-gate。** 人不逐行陪跑，而在意图、风险、生产发布等判断点签字。

这比单纯部署 Coding Agent 成熟得多：真正需要改造的是组织的“控制面”，不是再加一个代码生成器。

## 论证与证据

原文提供了可执行模板、依赖关系、治理责任和 leading/lagging indicators，因此比概念文章具体；但没有客户基线、样本、对照组或上线后的 defect/cycle-time 数据。故“可以这样实施”有较强支持，“这样实施一定更快且同样安全”仍未被证明。[1]

外部证据本身也是 mixed：DORA 2024 观察到 AI adoption 与文档质量、代码质量和 review speed 改善相关，但同时与 delivery throughput、stability 下降相关，说明局部提速不会自动转化为端到端收益。[5] METR 的 early-2025 RCT 曾测得资深开源开发者慢 19%，但 METR 已明确标注该结果过时；其 2026 更新认为现在更可能提速，却因参与者和任务选择偏差，无法可靠估算幅度。[6] 所以文章前提在 2026 年是合理假设，不是普遍事实。

## 最强反方

- **Plan/Design 压得过薄。** 多方 stakeholder 冲突、领域模型、NFR、requirement→test traceability，不能都缩成一次对话和两份 prose Markdown；小 feature 可用，复杂系统不足。[2]
- **闭环缺 measurement plane。** 原文列了每阶段指标，却没有解决 Git、PR、CI、incident 等数据如何关联、如何先建立 baseline。没有 instrumentation，control band 和 ROI 都可能只是口号。[3]
- **企业级运行缺 platform context。** 跨 repo 依赖、服务 owner、blast radius、审批路由和 adoption visibility，不是 repo 内的 skills/hooks 自动拥有的能力。[4]
- **同源模型审查存在相关性风险。** 同一模型家族写 spec、code、test、review，错误假设可能层层继承；独立 verifier、异构模型和确定性测试不可省。

后面三篇批评也都在销售自己的 requirements/process、engineering intelligence 或 developer portal 产品，所以应把它们视为有效缺口提示，而非中立结论。[2][3][4]

## 决策更新

对小团队，别照抄成新的文档官僚制。建议采用 80/20 版：

1. Issue/Kanban 卡直接充当 `intent`，避免重复录入。
2. 中高风险任务才生成 `spec.md + plan.md`；小修只保留 acceptance criteria。
3. 强制“可运行验证 + 独立 reviewer + 高风险人工 gate”。
4. 生产异常自动回流成卡片，但自动修复只允许走预批准 runbook/PR。
5. 先量四个指标：端到端 cycle time、首次验证通过率、review 等待时间、escaped defect rate。

## 置信度与待验证

置信度：中高。对架构原则判断较强；对规模化收益判断有限，因为原文缺实证。

会提高判断的证据：跨团队上线前后数据同时显示 cycle time 下降、escaped defects 不升、review queue 不积压。会降低判断的证据：Markdown/skill 数量增长，但 requirement rework、PR 等待和生产事故同步上升。

## Sources

[1] https://claude.com/blog/the-ai-native-sdlc-playbook — The AI-Native SDLC playbook
[2] https://martinelli.ch/code-is-no-longer-the-bottleneck-requirements-are — Code Is No Longer the Bottleneck. Requirements Are.
[3] https://waydev.co/anthropics-ai-native-sdlc-playbook-has-a-missing-layer-measurement — Anthropic's AI-Native SDLC playbook has a missing layer: measurement
[4] https://www.port.io/blog/anthropic-ai-native-sdlc-playbook — Implementing the Anthropic AI-Native SDLC Playbook
[5] https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report — Highlights from the 10th DORA report
[6] https://metr.org/blog/2026-02-24-uplift-update — We are Changing our Developer Productivity Experiment Design
