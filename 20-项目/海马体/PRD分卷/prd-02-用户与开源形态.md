---
title: PRD 三·四｜目标用户与开源形态
created: 2026-04-21
updated: 2026-04-21
type: entity
tags: [openhippo]
status: draft
sources: [20-项目/海马体/项目需求文档(PRD).md]
---

# PRD 三·四｜目标用户与开源形态

> 本页是 [[../项目需求文档(PRD)|海马体PRD]] 的分卷之一：**目标用户群体 + 开源形态**
> 完整目录见 [[../项目需求文档(PRD)|PRD索引]]

---

## 三、目标用户群体

| 画像 | 规模 | 使用场景 | 付费意愿 |
|------|------|---------|---------|
| **独立开发者/Hacker** | 数十万 | 个人AI助手、Side Project | 低（用免费版） |
| **AI Agent框架作者** | 数千 | 为框架集成记忆能力 | 中（愿意赞助/Pro） |
| **企业AI团队** | 数千家 | 内网Agent部署，数据合规要求 | 高（Enterprise） |
| **多Agent玩家** | 数万 | Claude Code/Cursor/Hermes等多Agent协作 | 中 |
| 知识工作者 | — | Obsidian/笔记系统+AI联动 | 低 |

---

## 四、开源形态

| 项目 | 说明 |
|------|------|
| **License** | Apache 2.0 |
| **仓库** | `github.com/hippocampus-ai/hippocampus`（待注册） |
| **模式** | Open-Core：核心引擎完全开源，高级功能付费 |
| **语言** | Python 3.10+ |
| **包管理** | PyPI (`pip install hippocampus`) + Docker |

| 开源（Community） | 付费（Pro/Enterprise） |
|-------------------|----------------------|
| 完整记忆引擎 | 跨设备E2E加密同步 |
| REST API + CLI + Hook Plugin | Web Dashboard |
| 热冷分层 + FTS5 + 向量搜索 | 记忆分析报告 |
| 单机多Agent隔离共享 | 团队共享（RBAC）/ SSO / 审计 |

---


---

## 相关链接

- 上级索引：[[../项目需求文档(PRD)]]
- 项目主页：[[../项目需求文档(PRD)]]
- 知识库索引：[[../../../index]]
