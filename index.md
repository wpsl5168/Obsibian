---
title: 知识库索引
created: 2026-04-21
updated: 2026-05-28
type: meta
tags: [meta]
status: stable
---

# 📚 知识库索引

> 覆盖 7 个顶层目录（00/10个人/10知识库/20/40/50/90） · 总页数 **341** · 最近更新 2026-05-28
> Schema 约束见 [[SCHEMA]] ｜ 操作日志 [[log]] ｜ 各区入口 [[README]]

---

## 📥 收件箱（00-收件箱）  *(3)*

- [[00-收件箱/2026-04-12-AI-Agent-研究报告.md|AI Agent 研究报告（10大主题）副本]] — 2024–2026 的 Agent 热点正在从“能跑的 demo”转向“可控、可观测、可复现、可部署”的工程体系。主线可以概括为三句话： 🔴
- [[00-收件箱/2026-05-01-五一回家携带清单.md|五一回家携带清单]]
- [[00-收件箱/README.md|00-收件箱]] — 临时草稿与待整理素材的暂存区。不过夜原则：每日整理。

## 👤 个人（05-个人）  *(1)*

- [[05-个人/家庭与孩子教育.md|家庭与孩子教育]] — 1. 下载Khan Kids App（iOS/Android）

## 🤖 知识库 · AI模型与Agent  *(32)*

- [[10-知识库/AI模型与Agent/01-基础架构与模型底座/1.1-大模型演进与主流架构体系.md|大模型演进与主流架构体系]] — 大语言模型（Large Language Model, LLM）本质上是一个超大规模的概率函数——给定一串 Token 序列，输出下一个 Token 的概率分布。如果用 .NET 类比：`Func<T 🟡
- [[10-知识库/AI模型与Agent/01-基础架构与模型底座/1.2-上下文窗口与Token机制.md|上下文窗口与 Token 机制]] — Token 不等于字符，也不等于单词。它是模型 Tokenizer 切分后的最小语义单元。 🟡
- [[10-知识库/AI模型与Agent/01-基础架构与模型底座/1.3-多模态能力原理与应用.md|多模态能力原理与应用]] — 多模态（Multimodal）指模型能处理和生成多种数据模态——文本、图像、音频、视频。 🟡
- [[10-知识库/AI模型与Agent/01-基础架构与模型底座/1.4-Embeddings与向量表示.md|Embeddings 与向量表示]] — Embedding（嵌入/向量表示）本质上就是把人类语言"翻译"成计算机能做数学运算的高维浮点数组。如果你熟悉 SQL Server，可以这样理解：一张表的每一行是一个文本，Embedding 就是给 🔴
- [[10-知识库/AI模型与Agent/02-提示词工程与输出规范/2.1-系统提示词与角色设定.md|系统提示词与角色设定]] — System Prompt（系统提示词）是 LLM 对话的"宪法"——它在每轮对话之前注入，定义模型的行为边界、人格、输出格式和能力范围。如果把 LLM 比作一个 C# 类，System Prompt 🔴
- [[10-知识库/AI模型与Agent/02-提示词工程与输出规范/2.2-高阶推理策略.md|高阶推理策略]] — 高阶推理策略就是让 LLM "想清楚再说话"的各种套路。如果说基础 Prompt 是 `Console.WriteLine("答案")`，高阶推理就是在输出前先跑一遍 `Debug.Assert()` 🔴
- [[10-知识库/AI模型与Agent/02-提示词工程与输出规范/2.2.1-推理模型工程化进阶.md|推理模型工程化进阶]] — 本文剥离自父页 §10-13，覆盖 2026 年推理模型的训练范式、Inference Scaling 技术栈与生产部署考量。 🔴
- [[10-知识库/AI模型与Agent/02-提示词工程与输出规范/2.3-结构化数据输出.md|结构化数据输出]] — 结构化输出（Structured Output）就是让 LLM 不再"自由发挥"，而是严格按照预定义的 Schema 输出 JSON、XML 等机器可解析的数据格式。如果把 LLM 比作一个 C# 方 🟡
- [[10-知识库/AI模型与Agent/02-提示词工程与输出规范/2.3.1-结构化输出-厂商能力对比.md|结构化输出 — 各大模型厂商能力对比]] — OpenAI 在 2024 年 8 月推出 Structured Outputs，到 2025-2026 年已经是最成熟的方案： 🟡
- [[10-知识库/AI模型与Agent/02-提示词工程与输出规范/2.3.2-结构化输出-工程实战.md|结构化输出 — 工程实战与最佳实践]] — Python 生态中，Pydantic 已经成为定义 LLM 输出 Schema 的事实标准： 🟡
- [[10-知识库/AI模型与Agent/03-工具调用与上下文协议/3.1-函数调用底层机制.md|函数调用底层机制]] — 用户消息 ──→ LLM（含 tools 定义） 🟡
- [[10-知识库/AI模型与Agent/03-工具调用与上下文协议/3.2-Model_Context_Protocol规范解析.md|Model Context Protocol 规范解析]] — 在没有 ADO.NET 之前，访问 SQL Server 用一套 API，访问 Oracle 用另一套，访问 MySQL 又是一套。ADO.NET 统一了接口：`IDbConnection`、`IDb 🟡
- [[10-知识库/AI模型与Agent/03-工具调用与上下文协议/3.2.1-MCP-Server生态系统.md|MCP Server 生态系统]] — 截至 2026 年初，MCP 生态已爆发式增长，社区已有 1000+ MCP Server 实现。
- [[10-知识库/AI模型与Agent/03-工具调用与上下文协议/3.2.2-MCP-SDK开发实战.md|MCP SDK 与开发实战]] — 官方提供 Python 和 TypeScript 两个 SDK。 🟡
- [[10-知识库/AI模型与Agent/03-工具调用与上下文协议/3.2.3-MCP协议架构与传输层.md|MCP 协议架构与传输层]] — 本文剥离自父页"协议架构详解"+"协议传输层"两节，覆盖 MCP 三大原语、JSON-RPC 消息格式、生命周期管理、stdio/HTTP+SSE 传输实现细节。 🔴
- [[10-知识库/AI模型与Agent/03-工具调用与上下文协议/3.3-RAG系统架构与演进.md|RAG 系统架构与演进]] — Indexing (离线)              Retrieval (在线)          Generation (在线) 🔴
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.1-AI_Agent核心心智模型.md|AI Agent 核心心智模型]] — 相较于传统的静态 Prompt 问答，Agent 的核心特征在于闭环的行动与反馈机制。它能够根据环境返回的真实数据动态调整后续策略。 🔴
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.1.1-Agent认知架构与主流框架2026.md|Agent 认知架构与主流框架 (2026)]] — 本文剥离自父页两节： 🔴
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.2-工作流编排模式.md|工作流编排模式]] — Anthropic 在 2025 年的研究报告中明确建议：能用 Workflow 解决的就不要用 Agent。Agent 的自主性带来的灵活性也意味着不可预测性。 🔴
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.2.1-LangGraph深度实操.md|LangGraph 深度实操]] — LangGraph 的 State 是一个 TypedDict，所有节点共享和修改同一个状态对象。 🟡
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.2.2-工作流工程最佳实践.md|工作流工程最佳实践]] — Agent 工作流的可观测性是工程落地的关键痛点。主流方案： 🟡
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.3-记忆机制设计.md|记忆机制设计]] — LLM 的上下文窗口本身就是最基础的记忆形式——所有的 messages 历史都在这个窗口中。 🔴
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.4-Human-in-the-loop交接机制.md|Human-in-the-loop 交接机制]] — 在 Agent 调用特定工具前，暂停执行等待人类确认。 🔴
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.5-AI-Agent架构开源学习指南.md|AI Agent 架构开源学习指南]] — 在深入源码之前，先把 5 个核心概念对齐。这些概念贯穿所有框架，只是实现方式不同。 🔴
- [[10-知识库/AI模型与Agent/05-评测监控与安全防护/5.1-模型评测基准与Evals驱动开发.md|模型评测基准与 Evals 驱动开发]] — LLM Evaluation（大模型评测）是对语言模型能力的系统化度量。类比 .NET 工程中的单元测试 + 集成测试 + 性能基准测试： 🔴
- [[10-知识库/AI模型与Agent/05-评测监控与安全防护/5.2-可观测性与链路追踪.md|可观测性与链路追踪]] — 传统微服务可观测性（Metrics / Logs / Traces 三支柱）在 LLM 应用场景下严重不足： 🔴
- [[10-知识库/AI模型与Agent/05-评测监控与安全防护/5.3-AI安全护栏与防御机制.md|AI 安全护栏与防御机制]] — LLM 应用面临的安全威胁与传统 Web 应用截然不同： 🔴
- [[10-知识库/AI模型与Agent/06-工程落地与Vibe_Coding实战/6.1-终端IDE形态深度对比.md|终端 IDE 形态深度对比]] — 2025 年以来，AI 编码工具已分化为三个明确的形态： 🔴
- [[10-知识库/AI模型与Agent/06-工程落地与Vibe_Coding实战/6.2-CLI原生Agent实战.md|6.2 CLI原生Agent实战：Aider / Claude Code / Codex CLI 三剑客]] — 在 6.1-终端IDE形态深度对比 中我们提到 Vibe Coding 的核心是"意图驱动"。但 VS Code 插件（Copilot / Cursor）本质上是 IDE-first，Agent 能力 🔴
- [[10-知识库/AI模型与Agent/06-工程落地与Vibe_Coding实战/6.3-SWE-Agent端到端闭环开发.md|6.3 SWE-Agent端到端闭环开发：从Benchmark到生产级自主编程]] — SWE-Agent 由 Princeton 和 Stanford 联合推出（1.0 版本），核心贡献是提出了 ACI（Agent-Computer Interface） 的概念——一套专门为 LLM  🔴
- [[10-知识库/AI模型与Agent/06-工程落地与Vibe_Coding实战/6.3.1-SWE-Agent生产化与CICD.md|SWE-Agent 生产化与 CI/CD 闭环]] — SWE-Agent 类工具的终极形态是完全集成到 CI/CD 管线中： 🔴
- [[10-知识库/AI模型与Agent/README.md|02-AI知识星球 索引]]

## 🎓 知识库 · DeepLearning.AI学习路径  *(3)*

- [[10-知识库/DeepLearning.AI学习路径/DeepLearning.AI-全量目录.md|DeepLearning.AI 全量课程目录]] — https://www.deeplearning.ai/courses/build-with-andrew 🔴
- [[10-知识库/DeepLearning.AI学习路径/DeepLearning.AI-学习路径.md|DeepLearning.AI 学习路径（工程师向）]] — 数据抓取来源：DeepLearning.AI 课程索引（Algolia index: courses_date_desc） 🟡
- [[10-知识库/DeepLearning.AI学习路径/DeepLearning.AI-按主题索引.md|DeepLearning.AI 按主题快速索引]] — https://www.deeplearning.ai/short-courses/agent-memory-building-memory-aware-agents 🔴

## 🛠️ 知识库 · 工具速查  *(6)*

- [[10-知识库/工具速查/00-Global-Rules.md|00-Global-Rules]]
- [[10-知识库/工具速查/01-Session-Management.md|01-Session-Management]] — 目的：避免长会话导致上下文膨胀（模型变笨/忘前文），同时保证关键信息不丢。
- [[10-知识库/工具速查/10-Best-Practices-Extract.md|10-Best-Practices-Extract]] — 来源（官方）：<https://code.claude.com/docs/en/best-practices>
- [[10-知识库/工具速查/20-CLI-Cheatsheet.md|20-CLI-Cheatsheet]] — 来源（官方）：<https://code.claude.com/docs/en/cli-reference>
- [[10-知识库/工具速查/ClaudeCode工具/00-Overview.md|Claude Code 概览（落地导向）]] — Claude Code 是一个 agentic coding 环境：它不只是回答问题，而是能在你的项目里读文件、改文件、跑命令，按“探索→计划→实现→验证”的循环完成任务。
- [[10-知识库/工具速查/Diagram-Style.md|Diagram-Style]] — 1) 必须基于文章内容严谨生成：图里每个实体、关系、层级，都要能在正文中找到对应依据。

## 📜 知识库 · 经典方法论  *(9)*

- [[10-知识库/经典方法论/01-工作流编排（Graphs & Workflows）.md|01-工作流编排（Graphs & Workflows）]]
- [[10-知识库/经典方法论/02-异步消息与事件驱动（Event-driven Messaging）.md|02-异步消息与事件驱动（Event-driven Messaging）]]
- [[10-知识库/经典方法论/03-平台化框架（DevUI_OTel_多语言）.md|03-平台化框架（DevUI_OTel_多语言）]]
- [[10-知识库/经典方法论/05-Handoff与Triage（交接_分诊）.md|05-Handoff与Triage（交接_分诊）]]
- [[10-知识库/经典方法论/07-AI Dev产品化（CLI_GUI_Cloud）.md|07-AI Dev产品化（CLI_GUI_Cloud）]]
- [[10-知识库/经典方法论/08-Observability与Evals（可观测_评测）.md|08-Observability与Evals（可观测_评测）]]
- [[10-知识库/经典方法论/09-HITL与Guardrails（人类在环_安全）.md|09-HITL与Guardrails（人类在环_安全）]]
- [[10-知识库/经典方法论/10-经典方法论（ReAct_Reflexion_ToT_MetaGPT）.md|10-经典方法论（ReAct_Reflexion_ToT_MetaGPT）]]
- [[10-知识库/经典方法论/30-Checkpointing.md|30-Checkpointing]] — 来源（官方）：<https://code.claude.com/docs/en/checkpointing>

## 👪 知识库 · 家庭教育  *(1)*

- [[10-知识库/家庭教育/初一英语学习方案.md|初一男孩英语学习启动方案（游戏切入）]] — 📦 初一英语 🟡

## 🗄️ 知识库 · 旧笔记归档 / Topics-archive  *(47)*

- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/digests/2026-04-24-digest.md|DeepLearning.AI Daily Digest — 2026-04-24]] — 3 门 Amazon Bedrock 相关课程被移除：
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/digests/2026-04-25-digest.md|DeepLearning.AI 课程监控日报 — 2026-04-25]] — 既然目录稳定，推荐本周复习/补课方向：
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/digests/2026-04-26-digest.md|DeepLearning.AI 课程监控日报 — 2026-04-26]] — 既然目录稳定，建议本周末巩固核心技能：
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/digests/2026-04-27-digest.md|DeepLearning.AI 每日摘要 — 2026-04-27]] — 既然课程库进入稳定期，正好时机回顾基础能力建设：
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/digests/2026-04-28-digest.md|DeepLearning.AI 日报 — 2026-04-28]] — 1. 全民级提示工程入门 — 这是一门面向非技术人群的提示工程课程，但对工程师同样有价值，可以学习如何向业务团队解释和推广提示工程最佳实践
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/digests/2026-04-29-digest.md|DeepLearning.AI 日报 — 2026-04-29]] — 本日课程目录与昨日快照完全一致，课程总数保持在 122 门（Short Courses: 97, Specializations: 14, Courses: 11）。
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/digests/2026-04-30-digest.md|DeepLearning.AI 日报 — 2026-04-30]] — 本日课程目录与昨日快照完全一致，课程总数保持在 122 门（Short Courses: 97, Specializations: 14, Courses: 11）。已连续两日无更新。
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/digests/2026-05-01-digest.md|DeepLearning.AI 每日简报 — 2026-05-01]] — 由于今日无新增课程，建议本周可以：
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/digests/2026-05-02-digest.md|DeepLearning.AI 每日资讯简报 — 2026-05-02]] — 既然今日无新增，正是复习巩固的好时机。推荐本周重点关注：
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/digests/2026-05-03-digest.md|DeepLearning.AI 每日资讯简报 — 2026-05-03]] — 连续稳定期正是深度学习的黄金时间。推荐本周重点关注：
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/digests/2026-05-04-digest.md|DeepLearning.AI 日报 — 2026-05-04]] — 既然课程库稳定，正是深度学习的好时机：
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/digests/2026-05-05-digest.md|DeepLearning.AI 日报 — 2026-05-05]] — 由于今日无新增课程，建议重点进行知识巩固和实战练习：
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/digests/2026-05-06-digest.md|DeepLearning.AI 日报 — 2026-05-06]] — 由于今日无新增课程，建议重点进行技能深化和项目实战：
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-04-20-deeplearningai-update.md|DeepLearning.AI 课程更新 — 2026-04-20]] — _无_ 🟡
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-04-21-deeplearningai-update.md|DeepLearning.AI 课程更新 — 2026-04-21]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-04-22-deeplearningai-update.md|DeepLearning.AI Update — 2026-04-22]] — 对比基准：`2026-04-21`
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-04-24-deeplearningai-update.md|DeepLearning.AI Course Sync — 2026-04-24]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-04-25-deeplearningai-update.md|DeepLearning.AI 课程更新 — 2026-04-25]] — _无_
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-04-26-deeplearningai-update.md|DeepLearning.AI 课程更新 — 2026-04-26]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-04-27-deeplearningai-update.md|DeepLearning.AI 课程同步 — 2026-04-27]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-04-28-deeplearningai-update.md|DeepLearning.AI Course Update — 2026-04-28]] — _None_
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-04-29-deeplearningai-update.md|DeepLearning.AI 课程更新 — 2026-04-29]] — 本日课程目录与上次快照一致。
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-04-30-deeplearningai-update.md|DeepLearning.AI 课程索引更新 — 2026-04-30]] — 今日无变更。
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-01-deeplearningai-update.md|DeepLearning.AI 课程更新 — 2026-05-01]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-02-deeplearningai-update.md|DeepLearning.AI 课程更新 — 2026-05-02]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-03-deeplearningai-update.md|DeepLearning.AI 课程变更报告 — 2026-05-03]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-04-deeplearningai-update.md|DeepLearning.AI 课程更新 — 2026-05-04]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-05-deeplearningai-update.md|DeepLearning.AI 课程变更 — 2026-05-05]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-06-deeplearningai-update.md|DeepLearning.AI 课程更新 — 2026-05-06]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-07-deeplearningai-update.md|DeepLearning.AI 课程索引更新 — 2026-05-07]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-08-deeplearningai-update.md|DeepLearning.AI 课程更新 — 2026-05-08]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-09-deeplearningai-update.md|DeepLearning.AI Course Catalog Update - 2026-05-09]] — The catalog remains stable at 123 courses.
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-10-deeplearningai-update.md|DeepLearning.AI Course Catalog Update]] 🔴
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-11-deeplearningai-update.md|DeepLearning.AI 课程索引变更 — 2026-05-11]] — ✅ 与 `2026-05-09` 基线完全一致 — 无新增、无移除、无字段修改。123 门课程的 slug、标题、类型、难度、主题、发布日期、URL 全部稳定。
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-12-deeplearningai-update.md|DeepLearning.AI 课程索引更新 — 2026-05-12]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-13-deeplearningai-update.md|DeepLearning.AI 课程更新 — 2026-05-13]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-14-deeplearningai-update.md|DeepLearning.AI 课程目录变更 — 2026-05-14]] — （无）
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-15-deeplearningai-update.md|DeepLearning.AI 课程更新 — 2026-05-15]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-16-deeplearningai-update.md|DeepLearning.AI 课程索引更新 — 2026-05-16]] — 今日课程目录与昨日完全一致。
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-17-deeplearningai-update.md|DeepLearning.AI 课程更新 — 2026-05-17]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-18-deeplearningai-update.md|DeepLearning.AI 课程目录变更 — 2026-05-18]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-19-deeplearningai-update.md|DeepLearning.AI 课程变更 — 2026-05-19]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-20-deeplearningai-update.md|DeepLearning.AI 课程索引更新 — 2026-05-20]]
- [[10-知识库/Topics-archive/Learning/DeepLearning.AI/updates/2026-05-27-deeplearningai-update.md|DeepLearning.AI 课程同步 — 2026-05-27]]
- [[10-知识库/旧笔记归档/SQLServer_Dacpac包加密与自动化部署.md|SQLServer_Dacpac包加密与自动化部署]] — 微软原生的 `.dacpac` 包本质上是一个 ZIP 压缩包，解压后可以通过 `model.xml` 等文件直接查看完全明文的数据库架构定义（包括表结构、视图、存储过程的 T-SQL 源码等）。 🟡
- [[10-知识库/旧笔记归档/SQLServer_存储过程加密方案_WITH_ENCRYPTION.md|SQLServer_存储过程加密方案_WITH_ENCRYPTION]] — 为了防止拥有高级权限（如 `sa`）的人员轻易窥探和窃取核心业务存储过程源码，SQL Server 提供了原生的 `WITH ENCRYPTION` 选项。 🟡
- [[10-知识库/旧笔记归档/SQLServer_高级加密方案_CLR_混淆.md|SQLServer_高级加密方案_CLR_混淆]] — 原生 T-SQL 的 `WITH ENCRYPTION` 仅是一种可逆的代码混淆（文本异或），面对掌握专用工具的高级 DBA（具备 `sa` 或 `sysadmin` 权限），源码仍有被提取和还原的风

## 🧱 项目 · BrickHub  *(6)*

- [[20-项目/BrickHub/4.5-BrickHub_Architecture_Vision.md|BrickHub 项目总体架构与愿景]] — BrickHub 项目目前的核心架构主要分为以下几个层次，旨在实现从自然语言到高质量 3D 乐高模型的生成与展示：
- [[20-项目/BrickHub/4.6-BrickHub_Technical_Research.md|BrickHub 进阶技术研究蓝图]] — 本报告旨在为 BrickHub 的下一阶段核心功能（高级渲染与动态图纸生成）提供底层技术资料与实现路径，作为后续开发的架构参考书。 🟡
- [[20-项目/BrickHub/4.7-BrickHub_LDraw_Standard_Assets.md|BrickHub 标准 LDraw 测试素材库]] — 本素材库由二秘小贝整理，收录了四秘（小牛）在测试渲染引擎 `components/BrickRenderer.js` 及其核心解析逻辑 `parseLDraw` 时所采用的 4 个官方标准分类 LDr 🟡
- [[20-项目/BrickHub/4.8-BrickHub_Interactive_Engine_Architecture.md|BrickHub 2.0 互动拼搭引擎架构白皮书]] — BrickHub 2.0 的核心目标是打造对标 Mecabricks 的“可互动拖拽、可动态拆解的在线拼搭工厂”。为实现数万级零件的高性能渲染与丝滑的拼搭交互，本白皮书针对四大核心技术难题进行了深度调 🟡
- [[20-项目/BrickHub/4.9-BrickHub_Engineering_Principles_and_Lessons.md|BrickHub 工程原则与血泪教训总结]] — 今天早期我们将大段黑盒 `parse` 逻辑直接塞进 `useEffect` 中，导致了灾难性的面条代码。经过外部专家指导，我们确立了“保时捷图纸”最佳实践：
- [[20-项目/BrickHub/Gemini提示词.md|BrickHub Gemini/Copilot 提示词模板]] — 太棒了，我们这就开始 BrickHub 的第一步：实现一个标准 2x6 乐高积木的 3D 渲染。 🟡

## ⚡ 项目 · Hermes Agent  *(2)*

- [[20-项目/Hermes/README.md|Hermes 项目]]
- [[20-项目/Hermes/memory-system-upgrade.md|Hermes Memory System Upgrade]] — Hermes记忆系统存在三个核心问题： 🔴

## 🦛 项目 · 海马体 OpenHippo  *(33)*

- [[20-项目/海马体/F5-Dream设计-v0.1.md|F5 Dream（记忆整合）设计 v0.1]] — PRD F5 标 P0，但市面上的记忆系统（Mem0/Letta/Zep）几乎都没真正做这件事——它们停在"存"和"检索"，而 Dream 是整理 + 遗忘。这是项目需求文档(PRD)相对它们的护城河 🔴
- [[20-项目/海马体/PRD分卷/prd-01-目的与痛点.md|PRD 一·二｜项目目的与解决痛点]] — 为AI Agent提供本地优先、隐私第一的持久化记忆引擎。让任何Agent框架通过标准协议（REST API / CLI / Hook Plugin）即插即用地获得跨会话记忆能力，数据永远不离开用户的
- [[20-项目/海马体/PRD分卷/prd-02-用户与开源形态.md|PRD 三·四｜目标用户与开源形态]]
- [[20-项目/海马体/PRD分卷/prd-03-部署形式.md|PRD 五｜部署形式]] — pip install hippocampus && hippocampus serve
- [[20-项目/海马体/PRD分卷/prd-04-1-核心记忆操作.md|PRD 6.1｜核心记忆操作 (F1)]] — 将结构化或自然语言记忆写入存储，支持自动去重和合并。单条写入和批量写入（最多100条/次）。
- [[20-项目/海马体/PRD分卷/prd-04-2-协议与接入.md|PRD 6.2｜协议与接入 (F6-F8)]] — 标准RESTful HTTP API，FastAPI实现，OpenAPI 3.0自动文档。所有功能的统一HTTP入口。 🟡
- [[20-项目/海马体/PRD分卷/prd-04-3-生命周期管理.md|PRD 6.3｜记忆生命周期管理 (F9-F10)]] — 基于访问模式自动调整记忆温度，无需人工干预。高频访问自动升Hot，长期不用自动降Cold。 🟡
- [[20-项目/海马体/PRD分卷/prd-04-4-隔离与共享.md|PRD 6.4｜隔离与共享 (F11-F16)]] — Tenant→Agent→Session三级隔离，借鉴GitHub的Organization→User→Branch模型。物理隔离（独立DB）+ 逻辑隔离（Agent/Session维度）。 🔴
- [[20-项目/海马体/PRD分卷/prd-04-5-安全与智能.md|PRD 6.5｜安全与智能 (F17-F20)]] — 写入记忆时自动检测敏感信息（API Key、邮箱、手机号、身份证号等），标记或脱敏，防止跨Agent共享时泄露。 🔴
- [[20-项目/海马体/PRD分卷/prd-04-6-运维与集成.md|PRD 6.6｜运维与集成 (F21-F25)]] — 记忆变更时主动推送通知到外部系统，HMAC签名保证安全，指数退避重试保证可靠。 🔴
- [[20-项目/海马体/PRD分卷/prd-04-7-Dogfood迁移.md|PRD 6.7｜Dogfood迁移 (F26-F27)]] — 从现有Hermes内嵌记忆系统迁移到海马体，采用Hook管道双写架构。Hermes内置memory保留作为热缓存，海马体作为持久化冷存储+语义搜索引擎。这是Dogfood第一步。 🟡
- [[20-项目/海马体/PRD分卷/prd-05-操作流程与架构.md|PRD 七·八｜操作流程与架构]] — pip install hippocampus → hippocampus init → hippocampus serve → 配置Agent Hook/REST → 开始使用 🟡
- [[20-项目/海马体/PRD分卷/prd-06-环境与里程碑.md|PRD 九·十｜环境与里程碑]] — 核心依赖：SQLite 3.35+, sqlite-vec, FastAPI, Uvicorn 🟡
- [[20-项目/海马体/PRD分卷/prd-07-附录.md|PRD 附录｜API/Schema/ADR]] — prd-07-附录A-API接口汇总
- [[20-项目/海马体/PRD分卷/prd-07-附录A-API接口汇总.md|PRD 附录 A：API 接口汇总]]
- [[20-项目/海马体/PRD分卷/prd-07-附录B-数据库Schema.md|PRD 附录 B：数据库 Schema]] — CREATE TABLE memories ( 🔴
- [[20-项目/海马体/PRD分卷/prd-07-附录C-Hermes集成架构决策.md|PRD 附录 C：Hermes Agent 集成架构决策]] — 海马体的首个dogfooding场景是替代Hermes Agent的记忆后端。Hermes内置memory系统使用MEMORY.md/USER.md（热记忆）+ state.db FTS5（冷记忆），
- [[20-项目/海马体/session-storage-unification.md|Session Storage Unification]] — 1|# Session 存储统一方案 v1（已落地） 🟡
- [[20-项目/海马体/审查日志-v0.3-2026-04-20.md|OpenHippo 架构审查 v0.3 实施日志]] — ALTER TABLE cold_memory ADD COLUMN agent_id TEXT DEFAULT 'default'; 🟡
- [[20-项目/海马体/开发进度.md|OpenHippo 开发进度]] — ✅ F5 Dream — 三个PR全部完成 + observability 🟡
- [[20-项目/海马体/架构审查v0.2.md|OpenHippo 架构审查 v0.2]] — 1. 并发不安全 — 单 connection 跨线程 + WAL 解决不了写事务交叉 🟡
- [[20-项目/海马体/架构方案-v0.4-多agent共享池.md|海马体 v0.4 架构定稿 — 多 Agent 共享池 + 切片治理]] — 2026-04-21 修复了两个致命 bug 后做架构师复盘，结论：当前形态不是"独立无破坏"，而是"低耦合可插拔"。 🔴
- [[20-项目/海马体/测试方案-报告与缺陷追踪.md|海马体测试报告与缺陷追踪]] — （无 / 列表）
- [[20-项目/海马体/测试方案与用例.md|OpenHippo 记忆系统测试方案与用例]] — 作为 Agent 记忆系统，OpenHippo 需满足以下行业标准： 🟡
- [[20-项目/海马体/测试用例-D1-D5-功能与性能.md|海马体测试用例 D1-D5（功能正确性/去重/搜索/性能/数据完整性）]] 🔴
- [[20-项目/海马体/测试用例-D6-D8-容量与异常.md|海马体测试用例 D6-D8（容量/生命周期/异常恢复）]] — 创建 → 替换 → 归档 → Cold搜索 → 提升 → 删除 → 验证清除
- [[20-项目/海马体/竞品调研与商业计划书.md|海马体 — 竞品调研与商业计划书]] — 1. Mem0单季186M API调用（Q3 2025）— 证明记忆是高频需求 🔴
- [[20-项目/海马体/设计/F5-统一软删除管线-v0.1.md|F5 统一软删除管线设计 v0.1]] — 当前 OpenHippo 所有"删除"语义（用户 remove、测试 teardown、dream consolidate）都是物理 DELETE： 🔴
- [[20-项目/海马体/设计/F5-统一软删除管线-v0.2.md|F5 统一软删除管线设计 v0.2]] — 8 个开放问题决策见 §7。 🔴
- [[20-项目/海马体/设计/F5-统一软删除管线-v0.3.md|F5 统一软删除管线设计 v0.3]] — OpenHippo 当前所有"删除"语义走物理 DELETE。F5 零信任铁律：never hard delete, only mark dormant。三处现存物理删点： 🔴
- [[20-项目/海马体/访问凭证.md|海马体 访问凭证]] — 1. 改 `~/.hippocampus/config.yaml` → `auth.enabled: true`
- [[20-项目/海马体/重构方案-事件总线v1.md|海马体重构方案 v1.0 — 事件总线架构]] — ┌──────────────────────────────────────────────────────────────┐ 🔴
- [[20-项目/海马体/项目需求文档(PRD).md|海马体（Hippocampus）PRD - 索引]]

## 🐾 项目 · Pets  *(4)*

- [[20-项目/Pets/PRD.md|Pets PRD]] — 1|# HermesPet · PRD
- [[20-项目/Pets/README.md|Pets README]] — 1|# HermesPet · 我的 AI 分身
- [[20-项目/Pets/架构.md|Pets 架构]] — 1|# HermesPet · 架构 🟡
- [[20-项目/Pets/进度.md|Pets 进度]] — 当前无 🟡

## 🤖 项目 · Pi-Rover  *(14)*

- [[20-项目/Pi-Rover/INDEX.md|INDEX]] — 待补充至 `决策/` 子目录。
- [[20-项目/Pi-Rover/README.md|README]] — docs/kb/
- [[20-项目/Pi-Rover/架构模式/00-overview.md|00-overview]] — 你的小车是？
- [[20-项目/Pi-Rover/架构模式/01-pure-cloud.md|01-pure-cloud]] — 车上只跑驱动和传感器读取，所有"思考"通过网络上传到云端LLM。 🟡
- [[20-项目/Pi-Rover/架构模式/02-pure-local.md|02-pure-local]] — 所有大脑跑在Pi上，永不上云，断网照常工作。 🟡
- [[20-项目/Pi-Rover/架构模式/03-hybrid-brain.md|03-hybrid-brain]] — 本地脑做日常+云端脑做专家，路由器智能分发——默认本地兜底，复杂任务上云。 🔴
- [[20-项目/Pi-Rover/架构模式/04-hierarchical.md|04-hierarchical]] — 仿生脑科学，分L0-L4五层，反射越快的层级越底层、越简单、越不可中断。 🔴
- [[20-项目/Pi-Rover/架构模式/05-behavior-tree-llm.md|05-behavior-tree-llm]] — 任务流程用行为树(Behavior Tree)做骨架，LLM动态填充叶子节点的"思考"。 🔴
- [[20-项目/Pi-Rover/架构模式/06-ros2-agent.md|06-ros2-agent]] — LLM作为ROS 2节点，与导航/感知/控制等成熟节点平等通信，享受整个ROS生态。 🟡
- [[20-项目/Pi-Rover/架构模式/07-multi-agent.md|07-multi-agent]] — 不是一个全能Agent，而是多个专精Agent (感知/规划/执行/批判) 协作完成任务。 🟡
- [[20-项目/Pi-Rover/架构模式/08-federated-swarm.md|08-federated-swarm]] — N台小车 + 1个云端"集群大脑"，车之间共享地图/记忆/技能，集体学习。 🟡
- [[20-项目/Pi-Rover/架构模式/99-decision-matrix.md|99-decision-matrix]] — 权重: Agent能力(30%) · 本地优先(25%) · 延迟(15%) · 成本(10%) · 复杂度(10%) · 扩展性(10%) 🟡
- [[20-项目/Pi-Rover/硬件/01-hailo-deep-dive.md|Hailo 加速器详解]] — 不做训练，不做云端，只做端侧推理——这是它便宜+省电+小巧的根本原因。 🔴
- [[20-项目/Pi-Rover/软件栈/01-pi-deployment-forms.md|Pi 5 本地部署形式详解]] — sudo raspi-config 🔴

## 🛡️ 项目 · Safety  *(6)*

- [[20-项目/Safety/01-产品方案-客户版.md|Safety AI · 工程安全检查系统 产品方案]] — 私有化部署，数据不出客户域；通用内核 + 行业模板，开箱即用。 🔴
- [[20-项目/Safety/02-系统架构-内部版.md|Safety AI 系统架构（内部版）]] — 技术栈一览： 🔴
- [[20-项目/Safety/03-分期路线-内部版.md|Safety AI 分期路线（内部版）]] 🟡
- [[20-项目/Safety/04-行业模板规划.md|Safety AI 行业模板规划]] — template_id: power_2026 🟡
- [[20-项目/Safety/99-决策记录.md|Safety AI 关键决策记录]]
- [[20-项目/Safety/README.md|Safety AI 工程安全检查系统]]

## 🌙 项目 · Dreaming（自主预研）  *(35)*

- [[20-项目/Dreaming/2026-04-17-research.md|BrickHub预研+质检 2026-04-17]] — 首次Dream B执行，选择最核心的渲染组件进行深度审查。
- [[20-项目/Dreaming/2026-04-18-research.md|BrickHub预研+质检 2026-04-18]] — DSL编译器负责将LLM输出的JSON DSL编译为LDraw文本，是AI生成管线的核心环节。代码整体质量较高，防御性编程到位（readNum fallback、warning收集），但发现以下问题：
- [[20-项目/Dreaming/2026-04-19-research.md|BrickHub预研+质检 2026-04-19]] — ldrawParser.js是纯逻辑层，无UI代码，无不符项。
- [[20-项目/Dreaming/2026-04-20-research.md|BrickHub预研+质检 2026-04-20]] — 后果：调用方（`lib/pipeline/index.js:100`）在 DSL 回退路径下拿到的 system prompt 里混入了本该是 JS 源码/文档的内容：
- [[20-项目/Dreaming/2026-04-21-research.md|BrickHub预研+质检 2026-04-21]] — Phase 3 沙盒核心两文件——零件抽屉与场景容器。配合 `npm test` 全量回归。
- [[20-项目/Dreaming/2026-04-22-research.md|BrickHub预研+质检 2026-04-22]] — 模型详情页是 Phase 1/2/3 入口枢纽，与生成管线 `lib/pipeline/index.js` 一起审查能完整覆盖"用户加载已有模型 → 浏览/放映/沙盒"和"AI 生成"两条主链路。 🟡
- [[20-项目/Dreaming/2026-04-23-research.md|BrickHub预研+质检 2026-04-23]]
- [[20-项目/Dreaming/2026-04-24-research.md|BrickHub Dream B 2026-04-24]] — PR: https://github.com/wpsl5168/brickhub/pull/1
- [[20-项目/Dreaming/2026-04-25-research.md|BrickHub Dream B 2026-04-25]] — LDraw 解析器 + 几何约束校验（碰撞/悬空检测），是 AI 生成内容落地到 3D 渲染前的最后闸门。
- [[20-项目/Dreaming/2026-04-26-research.md|BrickHub Dream B 2026-04-26]]
- [[20-项目/Dreaming/2026-04-27-research.md|BrickHub Dream B 2026-04-27]] — DSL → LDraw 编译器，把 LLM 输出的结构化 JSON 转为 LDraw 文本。包含组件展开器（RECT_FILL / LINE / STACK / WALL_FRAME / WHEEL_
- [[20-项目/Dreaming/2026-04-28-research.md|BrickHub Dream B 2026-04-28]] — 抽屉式零件库组件（FAB → peek → open 三态），含分类切换、颜色选择、零件网格、触摸手势。
- [[20-项目/Dreaming/2026-04-29-research.md|BrickHub Dream B 2026-04-29]] — PR：https://github.com/wpsl5168/brickhub/pull/7
- [[20-项目/Dreaming/2026-04-30-research.md|BrickHub Dream B 2026-04-30]] — 详情/截屏模式两用的模型详情页：动态加载 LDraw 源码 → 解析零件清单 / 逐步指南 → 切换"清单/放映/沙盒"三种交互。
- [[20-项目/Dreaming/2026-05-01-research.md|BrickHub Dream B 2026-05-01]] — PR：https://github.com/wpsl5168/brickhub/pull/9
- [[20-项目/Dreaming/2026-05-02-research.md|BrickHub Dream B 2026-05-02]] — 零件托盘展示组件（拼搭面板底部黄色条），4025字节，65行。
- [[20-项目/Dreaming/2026-05-03-research.md|BrickHub Dream B 2026-05-03]] — Web Speech API toggle 按钮组件，被 `components/home/PromptDock.js` 使用。
- [[20-项目/Dreaming/2026-05-04-research.md|BrickHub Dream B 2026-05-04]] — 模块职责：LDraw 生成主管线，DSL 优先 + LDraw 兜底 + 离线兜底，含遥测、重试、几何校验。
- [[20-项目/Dreaming/2026-05-05-research.md|BrickHub Dream B 2026-05-05]] — （无 — 该文件按规则仅报告）
- [[20-项目/Dreaming/2026-05-06-research.md|BrickHub Dream B 2026-05-06]] — 129 LOC，纯函数模块（LDraw 文本提取/去重/正交矩阵校验/离线兜底素材）。被 `lib/pipeline/index.js` 调用，是 LLM 输出后处理管线的关键节点。
- [[20-项目/Dreaming/2026-05-07-research.md|BrickHub Dream B 2026-05-07]] — 模块职责：把 brick 列表按材质/几何特征聚合成 InstancedMesh 分组、生成入场动画时间线、以 ease-in-out 采样位置。
- [[20-项目/Dreaming/2026-05-08-research.md|BrickHub Dream B 2026-05-08]] — PR：https://github.com/wpsl5168/brickhub/pull/14
- [[20-项目/Dreaming/2026-05-09-research.md|BrickHub Dream B 2026-05-09]] — 无
- [[20-项目/Dreaming/2026-05-10-research.md|BrickHub Dream B 2026-05-10]] — 无发现。
- [[20-项目/Dreaming/2026-05-11-research.md|BrickHub Dream B 2026-05-11]] — DSL JSON → LDraw 文本编译器。LLM 输出结构化 JSON，编译器负责坐标转换、9 位旋转矩阵生成、组件宏展开（CHASSIS/BODY_SHELL/RECT_FILL/LINE/ST
- [[20-项目/Dreaming/2026-05-12-research.md|BrickHub Dream B 2026-05-12]] — 模块职责：LDraw 颜色表 + 零件别名表 + `parseLDraw()` 字符串→bricks + `validateGeometry()` 碰撞/悬空检测。
- [[20-项目/Dreaming/2026-05-13-research.md|BrickHub Dream B 2026-05-13]] — 上次审查：2026-04-28（当时刚做过命名/aria-label清理，commit 06262421）。15天后复审。
- [[20-项目/Dreaming/2026-05-14-research.md|BrickHub Dream B 2026-05-14]] — 上次审查 04-29，距今 15 天，rotation 中最早的未近审条目。文件 lint clean，22/22 测试全过 (baseline 22 pass)。
- [[20-项目/Dreaming/2026-05-15-research.md|BrickHub Dream B 2026-05-15]] — 文件 lint clean、modelDetail.test.js 2/2 通过、近期无 git 改动 (febe1246, 2 周前)。
- [[20-项目/Dreaming/2026-05-16-research.md|BrickHub Dream B 2026-05-16]] — 文件小而稳定（最近一次修改在 ~3 周前的 glassmorphism 升级），ESLint clean。深扫发现 1 个真 bug + 1 个冗余。
- [[20-项目/Dreaming/2026-05-17-research.md|BrickHub Dream B 2026-05-17]] — 首次审查（home/ 子目录最大未审组件）。文件职责：浮层 banner + 可展开的"处理过程详情"模态。
- [[20-项目/Dreaming/2026-05-18-research.md|BrickHub Dream B 2026-05-18]] — 选择理由：rotation.json 里未审过；属于 modal/弹窗类组件，按 Pitfall #28，a11y 三件套高产；同期 home/ 子目录最大未审文件。
- [[20-项目/Dreaming/2026-05-19-research.md|BrickHub Dream B 2026-05-19]] — 选取理由：rotation.json 中未审过的核心组件（候选池里仅剩 LDrawModal / LDrawEditorPanel / FloatingControls / MenuPanel / H
- [[20-项目/Dreaming/2026-05-20-research.md|BrickHub Dream B 2026-05-20]] — AI 生成提示输入栏 + 语音入口 + 提交按钮组合组件。VoiceInput / Submit / 文本输入三件套布局。
- [[20-项目/Dreaming/2026-05-27-research.md|BrickHub Dream B 2026-05-27]] — 129 LOC，LDraw 文本处理工具集（extract/dedup/normalize/fallback），被 `lib/pipeline/index.js` 5 处调用。无直接单测，依赖 `ge

## 💼 项目 · AI风口/盈利方案  *(3)*

- [[20-项目/AI风口调研/2026-AI风口-张雪峰视角.md|2026 AI 风口 · 张雪峰视角终稿]] — 1. 抖音本地生活服务商（10 万押金 + 签 20 达人门槛）—— 单年流水千万级 🔴
- [[20-项目/README.md|20-项目]] — 正在进行的项目笔记。每个子目录=一个独立项目。
- [[20-项目/盈利方案-2026Q2.md|AI Agent 个人盈利路径方案 (老王 2026Q2)]] — 国内能拿到银行AI预算的人不多，能同时讲清Agent技术细节的更少。 🔴

## 🌏 调研 · 2026-04 中美AI模型与Agent全景  *(7)*

- [[40-调研报告/2026-04-中美AI模型与Agent全景/01-美国大模型.md|美国五大家旗舰大模型 2026]]
- [[40-调研报告/2026-04-中美AI模型与Agent全景/02-中国大模型.md|中国八大家旗舰大模型 2026]] — 1. 全面拥抱国产算力（DeepSeek V4 + 昇腾、阿里平头哥 47 万片、阶跃 StepMesh） 🟡
- [[40-调研报告/2026-04-中美AI模型与Agent全景/03-开源Agent框架.md|开源 Agent 框架 6 强 2026]] — 你需要什么？
- [[40-调研报告/2026-04-中美AI模型与Agent全景/04-编码Agent.md|编码 Agent 6 强 2026]]
- [[40-调研报告/2026-04-中美AI模型与Agent全景/05-国产Agent产品.md|国产 Agent 产品 4 强 2026]] — 1. 通用 Agent 路线被普遍押注（Manus、AutoGLM、扣子操作电脑）— 与美国"编码 Agent 一枝独秀"形成鲜明对比
- [[40-调研报告/2026-04-中美AI模型与Agent全景/06-中美对比与趋势.md|中美 AI 全景对比与 2026 趋势研判]] — 1. 海马体定位：本地优先 + 用户可审查，正好抓住"自主可控"+"开源"两大风口 🟡
- [[40-调研报告/2026-04-中美AI模型与Agent全景/INDEX.md|2026 中美 AI 模型与 Agent 全景报告]]

## 🏦 调研 · 银行业AI转型  *(8)*

- [[40-调研报告/银行业AI转型/00-行业全景与大行案例对标.md|行业全景与 12 家大行 AI 案例对标（2025）]] — 1. 大模型 + 小模型双引擎 —— 大模型搞复杂语义/生成，小模型搞精准风控/识别 🟡
- [[40-调研报告/银行业AI转型/01-企业级AI架构六层蓝图.md|企业级 AI 架构六层蓝图]] — ┌─────────────────────────────────────────────────────────────────────┐ 🟡
- [[40-调研报告/银行业AI转型/02-老系统改造路径-CLI化与MCP包壳.md|老系统改造路径 — CLI 化与 MCP 包壳]] — 1. 发起前：草拟申请材料（如客户经理发起授信申请，AI 帮写理由）
- [[40-调研报告/银行业AI转型/03-数据授权与权限控制四维矩阵.md|数据授权与权限控制四维矩阵]] — PostgreSQL（Hive / Greenplum 同理）： 🟡
- [[40-调研报告/银行业AI转型/04-角色赋能-RM副驾驶到行领导驾驶舱.md|角色赋能 — RM 副驾驶到行领导驾驶舱]] — 行领导    →  战略驾驶舱（聚合 + 趋势 + 跨条线 + 行业对标） 🟡
- [[40-调研报告/银行业AI转型/05-12-18个月落地路径与POC选型.md|12-18 个月落地路径与 POC 选型]] — M0  摸底盘点（4 周） 🟡
- [[40-调研报告/银行业AI转型/06-国有大行企业级大模型落地专题.md|国有大行企业级大模型落地专题 — 案例·进展·场景·趋势·要求]] — 1. 六大行都已建成企业级大模型平台——不是单点应用，是平台级 🟡
- [[40-调研报告/银行业AI转型/README.md|银行业 AI 转型调研（对公客户管理系统视角）]] — 1. 不要重写，要"包壳" — 老系统暴露 MCP/OpenAPI 工具层，AI 在上层调用；20+ 年历史数据迁移风险 > 收益

## 🏛️ 调研 · Palantir-FDE  *(10)*

- [[40-调研报告/Palantir-FDE/00-FDE-是什么.md|00 FDE 是什么]] — Palantir 官方 careers 页把所有工程岗划分为三类,内部用希腊字母代号: 🟡
- [[40-调研报告/Palantir-FDE/01-起源与方法论.md|01 起源与方法论]] — Sankar 反复阐述的两条原则,在多个播客里几乎逐字重复: 🟡
- [[40-调研报告/Palantir-FDE/02-Ontology与产品哲学.md|02 Ontology 与产品哲学]] — 举个具体例子: 🟡
- [[40-调研报告/Palantir-FDE/03-AIP-Bootcamp-五日模式.md|03 AIP Bootcamp 五日模式]] — 来自 palantir.com/platforms/aip/bootcamp: 🟡
- [[40-调研报告/Palantir-FDE/04-组织与招聘.md|04 组织与招聘]] — Palantir 把所有 FDE 岗位分到 两个独立 division,从招聘到 clearance 流程完全独立: 🟡
- [[40-调研报告/Palantir-FDE/05-对标与模仿者.md|05 对标与模仿者]] — Barry (ex-Palantir) 在 *Understanding Forward Deployed Engineering* 中归纳: 🟡
- [[40-调研报告/Palantir-FDE/06-阴暗面与批评.md|06 阴暗面与批评]] — 帖标题:"Over 33% of my customers NEVER needed FDEs" 🟡
- [[40-调研报告/Palantir-FDE/07-移植到个人咨询.md|07 移植到个人咨询(占位)]] — 参考 06-阴暗面与批评#6 给老王的诚实判断:
- [[40-调研报告/Palantir-FDE/08-市场认可与国内实操.md|08 市场认可与国内实操]] — 国内客户以"人天/项目制"为绝对主流。投中网/53AI/肖仰华论坛多名嘉宾反复强调: 🔴
- [[40-调研报告/Palantir-FDE/README.md|Palantir FDE 深度调研]] — 1. FDE 不是单一岗位 title,是工程家族。核心是 FDSE(=Delta),还有 FDAIE、FD-Infra、FD-Reliability、FD-Security 等子岗。官方招聘页把工程

## 🏠 调研 · 房产  *(5)*

- [[40-调研报告/房产/2026-05-丰台学区与房价综合评估.md|丰台学区房价综合评估·全区视角(2026-05)]] — 直接对口/直升十二中、十八中、钱学森系： 🟡
- [[40-调研报告/房产/2026-05-丰台科技园区周边小区对标.md|北京丰台科技园区周边小区房价对标(2026-05)]] — _生成时间: 2026-05-05_ 🟡
- [[40-调研报告/房产/2026-05-北京16区房价13月走势.md|北京16区二手房挂牌均价13月走势(2025-04 ~ 2026-03)]] — 1. 核心区抗跌、远郊承压：西城/东城/海淀同比跌幅 < 10%，房山/门头沟/平谷 > 13% 🟡
- [[40-调研报告/房产/2026-05-怡海花园真实成交价.md|怡海花园（丰台科技园）真实成交价调研]] — 1. 用本人账号登录链家提供 cookie；或 🟡
- [[40-调研报告/房产/README.md|房产调研索引]] — 北京个人置业相关的小区成交价、市场行情、政策追踪。

## 🎓 调研 · 教育  *(13)*

- [[40-调研报告/教育/ai-startup.md|AI 启蒙资源调研（娃 + 自己）]] — 1. 4-5 岁：ScratchJr + 《Hello Ruby》绘本 + 和爸爸一起玩 Teachable Machine"认玩具"游戏。每周 1-2 次每次 15 分钟，重点是好玩不是学会 🟡
- [[40-调研报告/教育/bluey.md|Bluey 布鲁伊 调研]] — 每个配角是一种狗品种（拉布拉多、松狮、贵宾、斑点狗、阿富汗猎犬……），是个隐藏的"狗品种百科"。 🟡
- [[40-调研报告/教育/cool-math-games.md|Cool Math Games 调研]] — 1. 教育性被夸大：本质是"附带数学标签的小游戏站"，真正训练数学能力的游戏占比小，Common Sense Media 也只说"some" educational value 🟡
- [[40-调研报告/教育/english-startup.md|孩子英语启蒙资源调研]] 🟡
- [[40-调研报告/教育/khan-academy/01-历史与里程碑.md|Khan Academy 历史与里程碑]] — Sal 录视频是为了让表妹反复看（活人辅导没耐心讲十遍同一个东西）。这个偶然决定了 Khan Academy "短视频 + 自学" 的产品 DNA——后来抖音/B 站的知识区都吃这个红利。
- [[40-调研报告/教育/khan-academy/02-组织与财务.md|Khan Academy 组织与财务]] — 1. Sal Khan 薪酬 \$839K（2019）vs 非营利伦理
- [[40-调研报告/教育/khan-academy/03-产品矩阵与内容规模.md|Khan Academy 产品矩阵与内容规模]]
- [[40-调研报告/教育/khan-academy/04-用户口碑与学术效果.md|Khan Academy 用户口碑与学术效果]] — ✅ Khan Academy Kids 获普遍好评：App Store 18 万+ 5 星，Educational App Store 评 "无广告、无内购、对 2-8 岁 phonics 与早期数学 🟡
- [[40-调研报告/教育/khan-academy/05-Khanmigo专题.md|Khanmigo AI Tutor 专题]] — Khanmigo 不是单一聊天机器人，而是按角色拆三套体验： 🟡
- [[40-调研报告/教育/khan-academy/06-竞品对比与启示.md|Khan Academy 竞品对比与做中文版的启示]] — 中国家长/学生普遍要"快、准、直接给"——苏格拉底法在中国可能水土不服。 🟡
- [[40-调研报告/教育/khan-academy/README.md|Khan Academy 可汗学院调研索引]] — 非营利 K-12 教育平台，起家于一段 YouTube 视频，长成全球 1.89 亿注册用户的标杆；Khanmigo 是它押注下一个十年的 AI 老师产品。优点是免费 + mastery learni
- [[40-调研报告/教育/math-startup.md|孩子数学启蒙资源调研]] — 1. 现在（4 岁中班，2026 春-夏）：B 站 Numberblocks 中文版 + 古氏积木/Numicon + 新加坡数学《思维启蒙 4-5 岁》。每天 15-20 分钟，重数感不重计算。先不 🟡
- [[40-调研报告/教育/教育路线图.md|老王娃教育路线图（4 岁中班 → 小学 3 年级）]] — 1. 每天屏幕时间 ≤ 30 分钟（4-5 岁），≤ 45 分钟（6 岁后），分散到多个时段 🟡

## 📈 调研 · 量化方向  *(7)*

- [[40-调研报告/量化方向/00-入门-基础概念与技术体系.md|A股量化交易：基础概念与核心技术体系]] — 关键边界澄清（业内常混淆）： 🔴
- [[40-调研报告/量化方向/01-平台全景.md|A股量化交易平台全景 (2024-2025)]] — 2022年起证监会对程序化交易加强监管,2024年5月《程序化交易管理规定》 落地:所有量化交易须向券商报备、券商再报交易所。直接后果: 🟡
- [[40-调研报告/量化方向/02-数据源与券商接入.md|A股量化交易：数据源与券商接入技术]] — 机构级数据商还有 聚源、恒生聚源、巨潮、Reuters Eikon、Bloomberg——以"数据库直连+多年历史 PIT (point-in-time) 数据"卖给私募/公募，单一接入合同通常 10 🟡
- [[40-调研报告/量化方向/03-MiniQMT-实战playbook.md|MiniQMT 散户实盘 Playbook (2024-2025)]] — 2024-2025 多家券商已把 MiniQMT 门槛从官方50万降到 1万元: 🟡
- [[40-调研报告/量化方向/04-中国量化生死录-2023-2025.md|中国量化生死录 (2023-2025)]] — 雪球结构敲入 🟡
- [[40-调研报告/量化方向/05-Qlib实战pipeline.md|Qlib 实战 Pipeline (微软 AI 量化框架)]] — ┌─────────────────────────────────────────────┐ 🔴
- [[40-调研报告/量化方向/README.md|量化方向调研报告 - 索引]] — 1. 散户合规实盘只剩两条路:MiniQMT(国金/华鑫等可1万开)、Ptrade(中信建投等)

## 📊 调研 · 单篇报告（根目录）  *(9)*

- [[40-调研报告/2026高考志愿全行业评估.md|2026高考志愿全行业评估报告]] — 1. AI+新能源+集成电路把传统工科拽出泥潭：电气、车辆、机械电子、能源动力四个老牌专业重回绿牌；微电子连续5年绿牌、起薪7282元仅次信息安全。 🟡
- [[40-调研报告/AI-Agent-Memory架构借鉴分析.md|AI Agent Memory 架构借鉴分析]] — Memory 是 AI Agent 从"无状态工具"进化为"持续协作伙伴"的关键能力。当前业界的 memory 架构呈现以下趋势： 🔴
- [[40-调研报告/AI-Agent个人盈利赛道扫描-2026Q2.md|AI Agent 个人盈利赛道扫描 (2026Q2)]] — ┌─────────────────────────────────────────────┐ 🔴
- [[40-调研报告/Claude-Opus-4.7-vs-4.6.md|Claude Opus 4.7 vs 4.6 对比]] — 1. Extended Thinking移除 → 只能用 adaptive 模式 + effort 参数控制
- [[40-调研报告/Hermes上下文管理优化方案.md|Hermes 上下文管理优化方案]] — ../20-项目/Hermes/README 在通过 Copilot provider 接入 Claude 模型时，存在严重的上下文空间不足问题，直接影响长对话场景下的任务执行质量。 🔴
- [[40-调研报告/McKinsey-2026-AI报告与5岁AI启蒙.md|McKinsey 2026 AI 报告解读 & 5岁儿童 AI 启蒙路径]] — 这是高低绩效公司的分水岭。把 AI 装进旧流程的，无利润提升；重设计工作流的，EBIT ≥5% 来自 AI。 🔴
- [[40-调研报告/Memory-Agent-架构设计推演.md|Memory Agent 架构设计推演]] — 1. 合并重复记忆 🟡
- [[40-调研报告/README.md|40-调研报告]] — 深度调研、对比分析、决策报告。完成后只读，新版本另开文件。
- [[40-调研报告/Stack-chan-桌面AI机器人选型与采购.md|Stack-chan 桌面 AI 机器人选型与采购指南]] — 老王想在桌上养一个可接入 Hermes Agent 的 AI 机器人，能听话、说话、显示表情、转头看人，进阶版还能在桌面跑动避障。 🔴

## 📰 日报与动态 · AI日报  *(42)*

- [[50-日报与动态/AI日报/2026-04-09.md|AI Agent Daily Brief 2026-04-09]] — 我的理解：OpenClaw 在把 agent 的‘副作用能力’（exec/写文件/外部调用）纳入统一的审批与可审计链路，这对生产化很关键。
- [[50-日报与动态/AI日报/2026-04-10.md|AI Agent Daily Brief 2026-04-10]] — 我的理解：OpenClaw 在把 agent 的‘副作用能力’（exec/写文件/外部调用）纳入统一的审批与可审计链路，这对生产化很关键。
- [[50-日报与动态/AI日报/2026-04-11.md|AI Agent Daily Brief 2026-04-11]] — 我的理解：OpenClaw 在把 agent 的‘副作用能力’（exec/写文件/外部调用）纳入统一的审批与可审计链路，这对生产化很关键。
- [[50-日报与动态/AI日报/2026-04-12.md|AI Agent Daily Brief 2026-04-12]] — 我的理解：OpenClaw 在把 agent 的‘副作用能力’（exec/写文件/外部调用）纳入统一的审批与可审计链路，这对生产化很关键。
- [[50-日报与动态/AI日报/2026-04-13.md|AI Agent Daily Brief 2026-04-13]] — 我的理解：OpenClaw 在把 agent 的‘副作用能力’（exec/写文件/外部调用）纳入统一的审批与可审计链路，这对生产化很关键。
- [[50-日报与动态/AI日报/2026-04-14-知识库全量更新.md|2026-04-14 知识库全量更新日志]] — 本次对 `02-AI知识星球` 知识库进行了从零到一的全量内容建设，覆盖 6 大模块共 24 篇文章。所有文章均已完成 Frontmatter 标注、双向链接织网、Mermaid 架构图绘制，形成完整 🟡
- [[50-日报与动态/AI日报/2026-04-15-AI-Daily.md|AI Daily - 2026-04-15]] — 本周AI圈持续高密度输出：Google发布Gemini Robotics-ER 1.6进军具身智能，Anthropic以Project Glasswing联合12家巨头限量发布Claude Mytho 🟡
- [[50-日报与动态/AI日报/2026-04-16-AI-Daily.md|AI Daily - 2026-04-16]] — Claude Code 生态全面爆发霸占 GitHub Trending，OpenAI 发布 GPT-5.4-Cyber 网安专用模型，美国法院裁定 AI 对话不受律师-客户特权保护，本地推理方案持续
- [[50-日报与动态/AI日报/2026-04-17-AI-Daily.md|AI Daily - 2026-04-17]] — OpenAI Codex 大更新加入计算机操作能力，Claude Opus 4.7 发布引爆 HN，Google 开源 Gemma 4，Qwen3.6 小模型搅局 agentic coding——AI
- [[50-日报与动态/AI日报/2026-04-18-AI-Daily.md|AI Daily - 2026-04-18]] — Anthropic 连发两弹——Claude Opus 4.7 与 Claude Design，GitHub Trending 被 AI Agent 框架刷屏，RL+推理仍是学术主旋律。
- [[50-日报与动态/AI日报/2026-04-19-AI-Daily.md|AI Daily - 2026-04-19]] — 周末节奏放缓，但本周余波仍强：GPT-6落地发酵、Anthropic连发Claude Design+Opus 4.7双更新、开源阵营GLM-5.1/Gemma 4持续冲击闭源壁垒，GitHub趋势被A
- [[50-日报与动态/AI日报/2026-04-20-AI-Daily.md|AI Daily - 2026-04-20]] — 本周 AI 圈主线是「Agent 全面落地 + 开源模型逼宫闭源」：OpenAI Codex 把 agent 推向桌面与多应用、Anthropic Opus 4.7 系统提示集中体现"少问多做"的 a
- [[50-日报与动态/AI日报/2026-04-21-AI-Daily.md|AI Daily - 2026-04-21]] — 本周「编码 Agent + 模型迭代」双线推进：Anthropic 发布 Claude Opus 4.7（更换 tokenizer，新增 xhigh effort 档），OpenAI 把 Codex 
- [[50-日报与动态/AI日报/2026-04-22-AI-Daily.md|AI Daily - 2026-04-22]] — OpenAI 发布 ChatGPT Images 2.0、Claude Opus 4.7 落地后续发酵（tokenizer 变更引发约 40% 隐性涨价）、Qwen3.6-Max-Preview 登顶
- [[50-日报与动态/AI日报/2026-04-23-AI-Daily.md|AI Daily - 2026-04-23]] — OpenAI 今日正式发布 GPT‑5.5（主打"真实工作流"长任务执行），叠加昨日 ChatGPT Workspace Agents 落地与 GitHub Copilot 个人版收紧 / Claud
- [[50-日报与动态/AI日报/2026-04-25-AI-Daily.md|AI Daily - 2026-04-25]] — GPT-5.5 全量上线（API 于 4-24 开放）与 Claude Opus 4.7 + Claude Code 质量回归事件并列本周双主线，工程师圈对 Claude 订阅价值的不满情绪显著升温。
- [[50-日报与动态/AI日报/2026-04-26-AI-Daily.md|AI Daily - 2026-04-26]] — 本周前端模型集体迭代——OpenAI GPT-5.5（Apr 23）与 Anthropic Claude Opus 4.7（Apr 16）相继 GA，主线全面押注「可托付的长程 agentic 编码」
- [[50-日报与动态/AI日报/2026-04-27-AI-Daily.md|AI Daily - 2026-04-27]] — 本周 AI 圈"基础设施 + 安全"双线齐进：OpenAI 完成史上最大 $122B 融资把战线推向 AI Superapp，Anthropic 用 Opus 4.7 把高危能力主动"阉割"上线、把 
- [[50-日报与动态/AI日报/2026-04-28-AI-Daily.md|AI Daily - 2026-04-28]] — 微软-OpenAI 排他协议正式终结、OpenAI 可上任意云、Anthropic 与 Amazon 再加 5GW 算力——AI 基础设施版图在今天进入「多云+多甲方」的新阶段；同时开源侧 Codex
- [[50-日报与动态/AI日报/2026-04-29-AI-Daily.md|AI Daily - 2026-04-29]] — Anthropic 把 Claude 推进创意工作流（Blender/Adobe/Autodesk/Ableton/Splice 全家桶 connector），同日 Claude.ai 经历 78 分
- [[50-日报与动态/AI日报/2026-04-30-AI-Daily.md|AI Daily - 2026-04-30]] — Mistral 用 Medium 3.5 + Vibe 远程 Agent 把"云端并行编码代理"打到了 SWE-Bench 77.6%，同时社区今天密集讨论的几件事——Claude Code 的 HE
- [[50-日报与动态/AI日报/2026-05-01-AI-Daily.md|AI Daily - 2026-05-01]] — xAI 用 Grok 4.3（1M 上下文 + $1.25/$2.50 极致定价）正面冲击 GPT-5.5 / Claude Opus 4.7 的性价比阵地；与此同时 PyPI `lightning`
- [[50-日报与动态/AI日报/2026-05-02-AI-Daily.md|AI Daily - 2026-05-02]] — Grok 4.3 与 DeepSeek V4 两端发力压价（百万 context + 长尾推理成本下行），Uber 四个月烧光全年 AI 预算成为 Claude Code 经济性"反例"，OpenAI
- [[50-日报与动态/AI日报/2026-05-03-AI-Daily.md|AI Daily - 2026-05-03]] — 开源权重模型 Kimi K2.6 在第三方编程竞赛中力压 GPT-5.5/Claude Opus 4.7/Gemini Pro 3.1 拿下冠军；同日 xAI 放出 Grok 4.3、IBM 开源 G
- [[50-日报与动态/AI日报/2026-05-04-AI-Daily.md|AI Daily - 2026-05-04]] — 五一假期周一，三大厂的"代理工程化"叙事进一步收敛：OpenAI 推 Symphony 编排开源规范并把 Codex/Managed Agents 接入 AWS；Anthropic 强化 Claude
- [[50-日报与动态/AI日报/2026-05-05-AI-Daily.md|AI Daily - 2026-05-05]] — 今日两大主线：基础设施侧 OpenAI 公开了支撑 9 亿周活语音 AI 的 WebRTC 重构方案；用户权益侧 Chrome 被曝静默下载 4GB Gemini Nano 模型引发 GDPR/ePr
- [[50-日报与动态/AI日报/2026-05-06-AI-Daily.md|AI Daily - 2026-05-06]] — Google 用 MTP drafter 给 Gemma 4 加速 3 倍，OpenAI 公开 9 亿周活背后的 WebRTC 重构；与此同时 Chrome 被曝静默下载 4GB Gemini Nan
- [[50-日报与动态/AI日报/2026-05-07-AI-Daily.md|AI Daily - 2026-05-07]] — 今天的 AI 圈主轴是「Agent 真的开始花钱办事 + 算力合纵连横」：Cloudflare/Stripe 让 Agent 自助开账号买域名上线、Anthropic 一边把 Claude 配额拉高一 🟡
- [[50-日报与动态/AI日报/2026-05-08-AI-Daily.md|AI Daily - 2026-05-08]] — "算力 + 工程范式"双主线日：Anthropic 拿下 SpaceX Colossus 1（22 万 GPU、300+ MW）并全线提额；Simon Willison 公开承认 vibe codin
- [[50-日报与动态/AI日报/2026-05-09-AI-Daily.md|AI Daily - 2026-05-09]] — AI工程赛道今天呈现"双核"爆发态势：Anthropic凭Claude Opus 4.5首破SWE-bench 80%关口+300亿美元G轮融资(估值3800亿美元)稳坐coding AI头把交椅；O
- [[50-日报与动态/AI日报/2026-05-10-AI-Daily.md|AI Daily - 2026-05-10]] — Anthropic 携 Claude Opus 4.7 和金融Agent生态强势突围,与 SpaceX/Google/Amazon 锁定吉瓦级算力;OpenAI 推广告自助平台瞄准年入千亿;DeepS 🟡
- [[50-日报与动态/AI日报/2026-05-11-AI-Daily.md|AI Daily - 2026-05-11]] — Anthropic 在 Code w/ Claude 上拿下 xAI Colossus 数据中心全量算力的"敌营借兵"协议，Mozilla 用 Claude Mythos 单月修复 423 个 Fir
- [[50-日报与动态/AI日报/2026-05-12-AI-Daily.md|AI Daily - 2026-05-12]] — Thinking Machines Lab 抛出"交互模型"新范式直击 agent 自动化叙事的盲区；Google 首次披露真实世界中 AI 驱动的 0-day 漏洞利用被拦截，攻防侧 AI 化正式落
- [[50-日报与动态/AI日报/2026-05-13-AI-Daily.md|AI Daily - 2026-05-13]] — 今日AI圈三条主线：DeepMind把"鼠标指针"重新发明成AI入口；OpenAI Realtime API升级到GPT-5级语音推理；Anthropic拿到SpaceX的300MW算力，Claude
- [[50-日报与动态/AI日报/2026-05-14-AI-Daily.md|AI Daily - 2026-05-14]] — Anthropic 把 Claude 推进美国 SMB 市场（15 个开箱即用 agentic workflow + QuickBooks/PayPal/HubSpot 等集成）、Cactus 开源 
- [[50-日报与动态/AI日报/2026-05-15-AI-Daily.md|AI Daily - 2026-05-15]] — Codex 攻入 ChatGPT 移动端把"agent 随身"变成主流叙事，Anthropic 同步把 Claude 推向 SMB 长尾，与此同时业内开始严肃讨论"前沿模型访问权将被经济与安全两道门槛
- [[50-日报与动态/AI日报/2026-05-16-AI-Daily.md|AI Daily - 2026-05-16]] — 今日 AI 圈的主旋律是「Agent 时代的副作用账单开始到期」：Mitchell Hashimoto 警示「AI psychosis」式的工程文化、CTF 圈宣告被前沿模型攻破、OpenAI/Ant
- [[50-日报与动态/AI日报/2026-05-17-AI-Daily.md|AI Daily - 2026-05-17]] — NVIDIA 开源 SANA-WM 把"分钟级世界模型"塞进单卡 H100；Frontier AI 已经把开放式 CTF 比赛玩坏了；OpenAI 与马耳他政府直接给"全国国民"配 ChatGPT P
- [[50-日报与动态/AI日报/2026-05-18-AI-Daily.md|AI Daily - 2026-05-18]] — Google 放出 Gemini 3.1 全家桶 + Gemma 4 + Nano Banana 2 + Veo 3.1 一周连发，正面挤压 OpenAI/Anthropic；DeepSeek-V4-
- [[50-日报与动态/AI日报/2026-05-19-AI-Daily.md|AI Daily - 2026-05-19]] — Musk 起诉 OpenAI 一审败诉、Anthropic 出手收 Stainless 打通 MCP/SDK、Cursor Composer 2.5 押注 Kimi K2.5 + 与 SpaceXAI
- [[50-日报与动态/AI日报/2026-05-20-AI-Daily.md|AI Daily - 2026-05-20]] — Karpathy 离开教育全职加盟 Anthropic，叠加 Gemini 3.5 Flash GA、Google 把 Gemini CLI 砍掉换 Antigravity CLI、OpenAI 接入
- [[50-日报与动态/AI日报/README.md|50-日报与动态/AI日报 索引]]

## 📚 日报与动态 · DeepLearning.AI  *(16)*

- [[50-日报与动态/DeepLearning.AI/digests/2026-04-09-digest.md|DeepLearning.AI 每日简报 2026-04-09]] — 今日无新课发布。建议本周复习大模型应用开发的基石—— RAG (Retrieval Augmented Generation) 和基本 Agents 原理，打好基础应对后续新工具。可以抽空温习《Bui
- [[50-日报与动态/DeepLearning.AI/digests/2026-04-10-digest.md|DeepLearning.AI 每日观察 2026-04-10]] — 本周建议复习 Agents 及 RAG 相关的核心基础概念，巩固 LLMOps 实践链路。
- [[50-日报与动态/DeepLearning.AI/digests/2026-04-11-digest.md|DeepLearning.AI 每日解读 2026-04-11]] — 考虑到近期暂无新课程，建议优先巩固 Agents 和 RAG 相关的基础理论与实践，这两者在当前 LLM 应用落地中最为关键。可以抽空复习之前的核心课程或尝试动手写一个小型的 Agent Demo 练
- [[50-日报与动态/DeepLearning.AI/digests/2026-04-12-digest.md|DeepLearning.AI 每日简报 2026-04-12]] — 今日课程库无变化，一切如常。
- [[50-日报与动态/DeepLearning.AI/digests/2026-04-13-digest.md|DeepLearning.AI 每日总结 2026-04-13]]
- [[50-日报与动态/DeepLearning.AI/digests/2026-04-15-digest.md|DeepLearning.AI 每日简报 2026-04-15]] — 与上次快照（2026-04-13）相比无任何变化，课程库稳定在 122 门。
- [[50-日报与动态/DeepLearning.AI/updates/2026-04-09-deeplearningai-update.md|DeepLearning.AI 每日更新 2026-04-09]]
- [[50-日报与动态/DeepLearning.AI/updates/2026-04-10-deeplearningai-update.md|DeepLearning.AI 每日更新 2026-04-10]]
- [[50-日报与动态/DeepLearning.AI/updates/2026-04-11-deeplearningai-update.md|DeepLearning.AI 每日更新 2026-04-11]]
- [[50-日报与动态/DeepLearning.AI/updates/2026-04-12-deeplearningai-update.md|DeepLearning.AI 每日更新 2026-04-12]]
- [[50-日报与动态/DeepLearning.AI/updates/2026-04-13-deeplearningai-update.md|DeepLearning.AI 每日更新 2026-04-13]]
- [[50-日报与动态/DeepLearning.AI/updates/2026-04-15-deeplearningai-update.md|DeepLearning.AI 课程索引更新 2026-04-15]] — 与上次快照（2026-04-13）相比无任何变化。
- [[50-日报与动态/DeepLearning.AI/updates/2026-04-16-deeplearningai-update.md|DeepLearning.AI 课程同步 — 2026-04-16]]
- [[50-日报与动态/DeepLearning.AI/updates/2026-04-17-deeplearningai-update.md|DeepLearning.AI 课程同步 — 2026-04-17]] — 与上次快照 (2026-04-16) 相比无变化。
- [[50-日报与动态/DeepLearning.AI/updates/2026-04-18-deeplearningai-update.md|DeepLearning.AI 课程同步 2026-04-18]] — 无变更 — 本次同步未检测到课程变化。
- [[50-日报与动态/DeepLearning.AI/updates/2026-04-19-deeplearningai-update.md|DeepLearning.AI 课程同步 2026-04-19]] — 课程列表与上次快照一致。

## 🌐 日报与动态 · 其他  *(1)*

- [[50-日报与动态/README.md|50-日报与动态]] — 时序型内容：每日订阅、外部信息流、定期更新的快照。

## 📅 治理 · 周报 / 周聚合  *(13)*

- [[90-治理/weekly-digest/2026-04-28-daily.md|Dream A 日报 2026-04-28]]
- [[90-治理/weekly-digest/2026-05-02-daily.md|Dream A 日报 2026-05-02]] — cron 环境 memory() 不可用，仅审计未修改。
- [[90-治理/weekly-digest/2026-05-08-daily.md|Dream A 日报 2026-05-08]] — ⚠️ ce283ced880e (DeepLearning.AI每日摘要-小贝):
- [[90-治理/weekly-digest/2026-05-16-daily.md|Dream A 日报 2026-05-16]] — W20 周报昨日刚出（覆盖 5/11-15），今日仅 +1 天，全为 cron session（无人工对话），增量极少。
- [[90-治理/weekly-digest/2026-05-17-daily.md|Dream A 日增量 2026-05-17 (W20收官)]] — USER.md 已连续两周 >93%，下次新增前需老王手动 review 取舍（cron 无 memory 工具）。
- [[90-治理/weekly-digest/2026-05-20-daily.md|Dream A 每日简报 2026-05-20]] — USER.md 已 94% 占用率连续多日，cron 环境 `memory()` 不可用，无法清理。建议老王在正常 session 中：将"语音交互参考标杆豆包App"、"HermesPet改码红线"
- [[90-治理/weekly-digest/2026-W17.md|周报 2026-W17]] — 预期释放 ~300-500 字符，恢复到 80% 占用率。
- [[90-治理/weekly-digest/2026-W18.md|周报 2026-W18]]
- [[90-治理/weekly-digest/2026-W19.md|周报 2026-W19]] — 1. USER.md容量管理：当前98%（2700/2750字符），需要合并重复内容（第15/17行表格规则重复）
- [[90-治理/weekly-digest/2026-W20.md|周报 2026-W20]]
- [[90-治理/weekly-digest/2026-W21.md|周报 2026-W21]]
- [[90-治理/weekly-digest/2026-W22.md|周报 2026-W22]] — 🔴 严重:微信交付链路全面 rate limited
- [[90-治理/周报/2026-W16.md|周报 2026-W16]]

## 🗂️ 治理 · 迁移记录 & 元  *(4)*

- [[90-治理/README-old-90.md|90-治理]] — 知识库元规范与治理记录。
- [[90-治理/写作规范.md|写作与排版规范]] — 为了对标 Google AI、Anthropic (Claude) 等官方文档的专业水准，本知识库的所有内容生成必须严格遵循以下 Markdown 排版规范。小贝 (second-secretary)
- [[90-治理/迁移记录/OpenClaw-Memory/Daily/README.md|OpenClaw Memory 索引]]
- [[90-治理/迁移记录/OpenClaw-Memory/OpenClaw-迁移摘要.md|OpenClaw 迁移摘要（2026-03-28 ~ 2026-04-12）]] — 1. 工具分级（读/写/执行/外联），默认最小权限

---

## 📈 健康度

- 总页数：**341**
- 🔴 超长页 (>200行)：**53** 个
- 🟡 中等长度 (100-200行)：**79** 个
- 详细健康检查：`python3 ~/.hermes/skills/note-taking/kb-maintenance/scripts/wiki_lint.py`

---

## 📂 目录入口

- [[00-收件箱/README|00-收件箱]]
- [[05-个人/README|05-个人]]
- [[10-知识库/README|10-知识库]]
- [[20-项目/README|20-项目]]
- [[40-调研报告/README|40-调研报告]]
- [[50-日报与动态/README|50-日报与动态]]
- [[90-治理/README|90-治理]]
