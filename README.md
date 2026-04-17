---
title: "老王的知识库 (Obsidian Vault)"
date: 2026-04-17
tags: [索引, 知识库, AI-Agent]
---

# 老王的知识库 (Obsidian Vault)

本知识库采用结构化与双向链接体系，旨在沉淀成完整的知识图谱，而非碎片化信息。

> 最后审计：2026-04-17 · 维护人：小贝（二秘/知识库整理员）

---

## 目录索引结构

### 📥 0. 收件箱 (`00-Inbox/`)
- **定位**：待整理的原始素材、研究报告草稿。
- **内容**：
  - [[2026-04-12-AI-Agent-研究报告]] — AI Agent 10大主题研究报告（工程落地向）

### 📰 1. 新闻与动态 (`01-新闻与动态/`)
- **定位**：AI 及 AI Agent 领域新闻、每日动态追踪、重要事件里程碑。
- **内容**：行业新闻速递 + AI Agent Daily（OpenClaw Release、Claude Code、MCP 生态、顶流博主原创）。

### 🌐 2. AI知识星球 (`02-AI知识星球/`)
- **定位**：体系化 AI 知识图谱（非碎片知识）。
- **维度**：架构 → 模块功能 → 处理方式 → 技术路径 → 产品对比。
- **子目录**：
  - `01-基础架构与模型底座/` — [[1.1-大模型演进与主流架构体系|大模型演进]] · [[1.2-上下文窗口与Token机制|Token机制]] · [[1.3-多模态能力原理与应用|多模态]] · [[1.4-Embeddings与向量表示|Embeddings]]
  - `02-提示词工程与输出规范/` — [[2.1-系统提示词与角色设定|角色设定]] · [[2.2-高阶推理策略|推理策略]] · [[2.3-结构化数据输出|结构化输出]]
  - `03-工具调用与上下文协议/` — [[3.1-函数调用底层机制|函数调用]] · [[3.2-Model_Context_Protocol规范解析|MCP规范]] · [[3.3-RAG系统架构与演进|RAG系统]]
  - `04-智能体架构与工作流设计/` — [[4.1-AI_Agent核心心智模型|心智模型]] · [[4.2-工作流编排模式|工作流编排]] · [[4.3-记忆机制设计|记忆机制]] · [[4.4-Human-in-the-loop交接机制|HITL交接]]
  - `05-评测监控与安全防护/` — [[5.1-模型评测基准与Evals驱动开发|Evals评测]] · [[5.2-可观测性与链路追踪|可观测性]] · [[5.3-AI安全护栏与防御机制|安全护栏]]
  - `06-工程落地与Vibe_Coding实战/` — [[6.1-终端IDE形态深度对比|IDE对比]] · [[6.2-CLI原生Agent实战|CLI Agent]] · [[6.3-SWE-Agent端到端闭环开发|SWE-Agent]]
  - 独立专题：[[AI-Agent架构]] · [[MCP规范]] · [[Workflow设计模式]] · [[SWE-Agent实战]]

### 💡 3. 笔记与灵感 (`03-笔记与灵感/`)
- **定位**：日常学习笔记、技术灵感、随笔心得。
- **SQL Server 加密系列**：
  - [[SQLServer_存储过程加密方案_WITH_ENCRYPTION|WITH ENCRYPTION 基础方案]]
  - [[SQLServer_高级加密方案_CLR_混淆|CLR + 代码混淆高级方案]]
  - [[SQLServer_Dacpac包加密与自动化部署|Dacpac 包加密与自动化部署]]
- **OpenAI Agent SDK 系列**：
  - [[00-Global-Rules]] · [[01-Session-Management]] · [[01-工作流编排（Graphs & Workflows）]]
  - [[02-异步消息与事件驱动（Event-driven Messaging）]] · [[03-平台化框架（DevUI_OTel_多语言）]]
  - [[05-Handoff与Triage（交接_分诊）]] · [[07-AI Dev产品化（CLI_GUI_Cloud）]]
  - [[08-Observability与Evals（可观测_评测）]] · [[09-HITL与Guardrails（人类在环_安全）]]
  - [[10-经典方法论（ReAct_Reflexion_ToT_MetaGPT）]] · [[10-Best-Practices-Extract]]
  - [[20-CLI-Cheatsheet]] · [[30-Checkpointing]] · [[Diagram-Style]]
- **Claude Code 工具系列**：
  - [[ClaudeCode-工具/00-Overview|Claude Code 概览]]
- **DeepLearning.AI 学习**：
  - [[DeepLearning.AI-学习路径]]

### 🏗️ 4. 项目开发 (`04-项目开发/`)
- **定位**：实战项目管理与 Vibe Coding 试水。
- **BrickHub 项目**：
  - [[4.5-BrickHub_Architecture_Vision|总体架构与愿景]]
  - [[4.6-BrickHub_Technical_Research|进阶技术研究蓝图]]
  - [[4.7-BrickHub_LDraw_Standard_Assets|LDraw 标准测试素材库]]
  - [[4.8-BrickHub_Interactive_Engine_Architecture|互动拼搭引擎架构白皮书]]
  - [[4.9-BrickHub_Engineering_Principles_and_Lessons|工程原则与血泪教训]]
  - [[Gemini提示词|Gemini/Copilot 提示词模板]]

### 🤖 5. AI Agent 专题 (`05-AI-Agent专题/`)
- **定位**：AI Agent 架构研究、模型对比、实践经验。
- **内容**：
  - [[AI-Agent-Memory架构借鉴分析]]
  - [[Hermes上下文管理优化方案]]
  - [[Claude-Opus-4.7-vs-4.6]]

### 📚 7. 专题学习 (`10-Topics/`)
- **DeepLearning.AI 课程追踪**：
  - `updates/` — 每日课程变更监测
  - `digests/` — 每日总结与学习建议

### ⚙️ 8. 治理与记忆 (`99-Governance/`)
- **定位**：Agent 运行记忆与日志存档。
- **内容**：[[OpenClaw-迁移摘要]]（压缩后的关键决策摘要）、Agent 心跳状态、[[00-写作与排版规范|写作与排版规范]]。
- ⚠️ 注意：此目录为自动生成的 Agent Memory，非人工笔记。

### 📁 9. 其他
- `assets/` — 配图资源库（截图、架构图等）
- `scripts/` — 知识库维护脚本

---

## 标签体系

| 标签 | 覆盖范围 |
|------|----------|
| `AI-Agent` | Agent 架构、编排、多Agent协作 |
| `LLM` | 大模型基础、Token、多模态 |
| `MCP` | Model Context Protocol 协议 |
| `RAG` | 检索增强生成系统 |
| `BrickHub` | 乐高项目开发 |
| `SQL-Server` | SQL Server 加密、部署、性能优化 |
| `DevOps` | CI/CD、自动化部署 |
| `Claude-Code` | Claude Code 工具使用与架构 |
| `Vibe-Coding` | AI辅助编程实战 |
| `DeepLearning-AI` | DeepLearning.AI 课程学习 |

---

## 维护规范

1. **每篇笔记必须有 Frontmatter**（title, date, tags）
2. **内容之间用双向链接 `[[]]` 关联**，构建知识网络
3. **拒绝纯搬运**，每篇笔记要有结构化价值和个人理解
4. **中文为主，英文术语保留原文**
5. 详见 [[00-写作与排版规范]]
