---
title: PRD 附录 A：API 接口汇总
created: 2026-04-21
updated: 2026-04-21
type: entity
tags: [openhippo]
status: draft
---

# PRD 附录 A：API 接口汇总

> 📚 上级页面：[[prd-07-附录]]

## 附录A: API接口汇总

| 方法 | 路径 | 功能 | 里程碑 |
|------|------|------|--------|
| POST | `/v1/memories` | 写入记忆(F1) | M0 |
| POST | `/v1/memories/search` | 检索记忆(F2) | M0 |
| DELETE | `/v1/memories/{id}` | 删除记忆(F3) | M0 |
| GET | `/v1/memories/{id}` | 获取单条 | M1 |
| PUT | `/v1/memories/{id}` | 更新记忆 | M1 |
| POST | `/v1/memories/batch` | 批量写入(F1) | M1 |
| POST | `/v1/memories/forget` | 批量遗忘(F3) | M1 |
| POST | `/v1/memories/{id}/promote` | 升温(F4) | M1 |
| POST | `/v1/memories/{id}/archive` | 降温(F4) | M1 |
| GET | `/v1/memories/stats` | 统计(F4) | M1 |
| POST | `/v1/maintenance/sweep` | 温度调控(F9) | M1 |
| POST | `/v1/consolidate` | 触发整合(F5) | M3 |
| POST | `/v1/agents` | 注册Agent(F11) | M2 |
| POST | `/v1/agents/{id}/tokens` | 生成Token(F12) | M2 |
| POST | `/v1/repos` | 创建记忆库(F11) | M2 |
| POST | `/v1/repos/{id}/grant` | 授权(F12) | M2 |
| DELETE | `/v1/repos/{id}/grant/{agent_id}` | 撤销授权(F12) | M2 |
| GET | `/v1/repos/{id}/grants` | 授权列表(F12) | M2 |
| POST | `/v1/sessions` | 开始会话(F13) | M2 |
| DELETE | `/v1/sessions/{id}` | 结束会话(F13) | M2 |
| POST | `/v1/broadcast` | 广播(F15) | M2 |
| GET | `/v1/inbox` | 收件箱(F15) | M2 |
| GET | `/v1/audit/sharing` | 审计日志(F16) | M2 |
| POST | `/v1/memories/scan` | PII扫描(F17) | M3 |
| POST | `/v1/extract` | 自动提取(F18) | M3 |
| POST | `/v1/inject` | 上下文注入(F19) | M3 |
| GET | `/v1/memories/timeline` | 时间轴(F20) | M4 |
| POST | `/v1/webhooks` | 注册webhook(F21) | M4 |
| GET | `/v1/webhooks` | 列表webhook(F21) | M4 |
| DELETE | `/v1/webhooks/{id}` | 删除webhook(F21) | M4 |
| POST | `/v1/backup` | 备份(F22) | M4 |
| POST | `/v1/restore` | 恢复(F22) | M4 |
| POST | `/v1/import` | 导入(F23) | M4 |
| POST | `/v1/knowledge/index` | 索引知识库(F24) | M4 |
| POST | `/v1/knowledge/search` | 搜索知识库(F24) | M4 |
| GET | `/v1/health` | 健康检查(F25) | M0 |
| GET | `/v1/metrics` | 监控指标(F25) | M4 |
| GET | `/v1/memories/{id}/history` | 版本历史(F10) | M4 |
| POST | `/v1/memories/{id}/rollback` | 回滚(F10) | M4 |
| POST | `/v1/memories/conflicts` | 冲突列表(F10) | M4 |

---
