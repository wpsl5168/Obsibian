# OpenClaw（话题页）

> 目标：沉淀 OpenClaw 的官方更新、关键能力、最佳实践，以及我对产品走向的判断。

## 官方渠道
- 官网文档：<https://docs.openclaw.ai>
- GitHub repo：<https://github.com/openclaw/openclaw>
- Releases：<https://github.com/openclaw/openclaw/releases>

## 我关注的主线（长期）
- 多渠道触达（Telegram/Discord/飞书/…）与统一消息路由
- 工具调用的权限/审批/审计（HITL/requireApproval/沙箱）
- ACP：把“外部编码执行器”（Claude Code/Codex/Gemini）纳入统一编排
- 可维护的 Skills 生态（安装、版本、更新、治理）

## 时间线（演进史速览）

> 目的：按时间把“技术/关键贡献者/生态与行业背景”串起来，方便系统理解。

- 2026-03（OpenClaw v2026.3.x）：插件审批能力增强（requireApproval）、CLI backend 统一、ACP 会话绑定能力加强。
  - 技术：approval hooks / ACP / CLI backends
  - 关键贡献者：openclaw/openclaw 维护者与核心贡献者（以 release/PR 为准）
  - 行业背景：多渠道 agent + 工具副作用治理成为生产化刚需

- 2026-04-03（OpenClaw v2026.4.2）：插件配置迁移 + Task Flow 基座回归（更偏“可运维的后台编排”）。
  - 技术：plugins config boundary / openclaw doctor --fix / Task Flow（durable state、revision、inspection/recovery、child task spawning）
  - 我关心的含义：把 agent 的“副作用能力”（exec/写文件/外部调用）纳入统一审批与可审计链路；同时让后台任务的编排状态可恢复、可运维。

## 最近条目
- [[AI-Agent-Daily/2026-03-29]]（含 v2026.3.28 release 摘要）
- [[AI-Agent-Daily/2026-04-03]]（含 v2026.4.2 release 摘要与我的解读）
