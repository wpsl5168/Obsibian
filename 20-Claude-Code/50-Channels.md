# Channels（把外部事件推入运行中的 Claude Code Session）

来源（官方）：<https://code.claude.com/docs/en/channels>

## 一句话
Channels = 一个 MCP server，能把消息/告警/webhook 推到你正在运行的 Claude Code 会话里，让它“人在不在电脑前都能继续处理”。

## 适合场景
- CI 结果推送（失败日志自动分析）
- 监控告警（先分诊再建议处理）
- 聊天桥（Telegram/Discord/iMessage）

## 关键限制（官方）
- research preview
- 需要 claude.ai login（Console/API key 认证不支持）
- 事件只会在 session 打开时送达（想 always-on 需要后台跑）

## 安全要点（你做企业落地必须关心）
- sender allowlist（只允许特定来源推消息）
- pairing（配对）流程
- 对“能触发副作用”的动作要加审批/隔离
