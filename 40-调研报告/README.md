---
title: 40-调研报告
created: 2026-01-01
updated: 2026-09-08
type: meta
tags: [research]
status: stable
---

# 40-调研报告

深度调研、对比分析、决策报告。**完成后只读**，新版本另开文件。
受 [[SCHEMA]] 约束。完整索引见 [[index]]。

## 系列报告

- **`2026-04-中美AI模型与Agent全景/`** (7篇) — 中美大模型、开源Agent、编码Agent、国产Agent、趋势对比
  - 入口：[[2026-04-中美AI模型与Agent全景/INDEX|系列总览]]

## 单篇报告

- [[40-调研报告/2026-09-22-赣东北五日亲子行程|赣东北五日亲子行程（交互HTML）]] — 中秋错峰、连锁酒店、6岁120cm儿童规则与离线地图，含五日卡片/雨天切换。
- [[40-调研报告/2026-09-08-全账户条件单与仓位整理草案|全账户条件单与仓位整理草案]] — 覆盖10只持仓的建议额度、约80%仓位测算与条件单使用边界，未启用委托。
- [[40-调研报告/2026-09-08-股票交易接入技术方案|股票交易接入技术方案]] — 条件单、官方接口、RPA对比；人审、独立风控及程序化报告边界。
- [[40-调研报告/2026-09-08-十只持仓综合研究|十只持仓综合研究]] — 四股半年报、六只ETF穿透、复权量价与条件化风险建议。

| 文件 | 主题 | tag |
|------|------|-----|
| [[AI-Agent-Memory架构借鉴分析]] | Mem0/Letta/Zep 等记忆系统架构对比 | `#memory` `#research` |
| [[Memory-Agent-架构设计推演]] | 记忆Agent的角色与边界推演 | `#memory` `#architecture` |
| [[Hermes上下文管理优化方案]] | Hermes三层上下文优化设计 | `#hermes` `#architecture` |
| [[Claude-Opus-4.7-vs-4.6]] | Claude Opus 模型版本对比 | `#comparison` `#llm` |
| [[40-调研报告/agent/2026-06-AI-Agent优质信息源盘点|AI Agent 优质信息源盘点]] | B站/公众号/抖音讲 Agent 干货的大V盘点+订阅建议 | `#agent` `#research` |

## 调研页规范

- 类型 `type: research` 或 `type: comparison`
- 必须有 `created` 日期，反映报告时效性
- 时效性内容（"截至XXXX-XX"）必须明确标注
- 新报告生成后必须由 `research-to-kb` skill 自动注册到 [[index]] 与 [[log]]
