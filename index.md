---
title: 知识库索引
created: 2026-04-21
updated: 2026-04-21
type: meta
---

# 📚 知识库索引

> 覆盖 `10-知识库/`、`20-项目/`、`30-调研报告/` 治理目录。
> 总页数：**88** | 最近更新：2026-04-21
> Schema约束见 [[SCHEMA]]｜操作日志 [[log]]


## 🤖 AI模型与Agent（核心知识）

- [[10-知识库/AI模型与Agent/01-基础架构与模型底座/1.1-大模型演进与主流架构体系.md|大模型演进与主流架构体系]] — 大语言模型（Large Language Model, LLM）本质上是一个**超大规模的概率函数**——给定一串 Token 序列，输出下一个 Token 的概率分布。如果用 .NET 类比：`Func<Token[], Probabil  🟡
- [[10-知识库/AI模型与Agent/01-基础架构与模型底座/1.2-上下文窗口与Token机制.md|上下文窗口与 Token 机制]] — Token 不等于字符，也不等于单词。它是模型 Tokenizer 切分后的最小语义单元。  🟡
- [[10-知识库/AI模型与Agent/01-基础架构与模型底座/1.3-多模态能力原理与应用.md|多模态能力原理与应用]] — 多模态（Multimodal）指模型能处理和生成**多种数据模态**——文本、图像、音频、视频。  🟡
- [[10-知识库/AI模型与Agent/01-基础架构与模型底座/1.4-Embeddings与向量表示.md|Embeddings 与向量表示]] — Embedding（嵌入/向量表示）本质上就是把人类语言"翻译"成计算机能做数学运算的高维浮点数组。如果你熟悉 SQL Server，可以这样理解：**一张表的每一行是一个文本，Embedding 就是给每行算出一个固定长度的 `VARBI  🔴
- [[10-知识库/AI模型与Agent/02-提示词工程与输出规范/2.1-系统提示词与角色设定.md|系统提示词与角色设定]] — System Prompt（系统提示词）是 LLM 对话的"宪法"——它在每轮对话之前注入，定义模型的行为边界、人格、输出格式和能力范围。如果把 LLM 比作一个 C# 类，**System Prompt 就是构造函数里的初始化配置，Use  🔴
- [[10-知识库/AI模型与Agent/02-提示词工程与输出规范/2.2-高阶推理策略.md|高阶推理策略]] — 高阶推理策略就是让 LLM "想清楚再说话"的各种套路。如果说基础 Prompt 是 `Console.WriteLine("答案")`，**高阶推理就是在输出前先跑一遍 `Debug.Assert()` + 单元测试 + 代码审查**。  🔴
- [[10-知识库/AI模型与Agent/02-提示词工程与输出规范/2.3-结构化数据输出.md|结构化数据输出]] — 结构化输出（Structured Output）就是让 LLM 不再"自由发挥"，而是严格按照预定义的 Schema 输出 JSON、XML 等机器可解析的数据格式。如果把 LLM 比作一个 C# 方法，**普通对话是返回 `string`  🔴
- [[10-知识库/AI模型与Agent/03-工具调用与上下文协议/3.1-函数调用底层机制.md|函数调用底层机制]] — **Function Calling**（函数调用）是 LLM 厂商提供的一种结构化输出能力：模型在推理过程中不直接返回自然语言，而是生成一个符合预定义 JSON Schema 的函数调用请求，由客户端执行后将结果回传给模型继续推理。  🟡
- [[10-知识库/AI模型与Agent/03-工具调用与上下文协议/3.2-Model_Context_Protocol规范解析.md|Model Context Protocol 规范解析]] — **MCP 之于 AI Agent，就像 ADO.NET 之于 .NET 应用——一套标准化的数据访问协议。**  🔴
- [[10-知识库/AI模型与Agent/03-工具调用与上下文协议/3.3-RAG系统架构与演进.md|RAG 系统架构与演进]] — **RAG（Retrieval-Augmented Generation，检索增强生成）** 是一种将外部知识检索与 LLM 生成相结合的架构模式。其核心思想：不要指望模型"记住"所有知识，而是在推理时动态检索相关上下文，注入到 promp  🔴
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.1-AI_Agent核心心智模型.md|AI Agent 核心心智模型]] — 相较于传统的静态 Prompt 问答，Agent 的核心特征在于**闭环的行动与反馈机制**。它能够根据环境返回的真实数据动态调整后续策略。  🔴
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.2-工作流编排模式.md|工作流编排模式]] — **工作流编排（Workflow Orchestration）** 是指将多个 LLM 调用、工具调用、条件判断等步骤按照一定的逻辑拓扑组织起来，形成可执行、可观测、可恢复的自动化流程。  🔴
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.3-记忆机制设计.md|记忆机制设计]] — **记忆（Memory）** 是 Agent 区别于一次性 LLM 调用的关键特征。没有记忆的 Agent 就像患了健忘症的员工——每次汇报都要从头解释背景。记忆系统让 Agent 能够跨会话积累经验、持久化关键信息、动态调整行为策略。  🔴
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.4-Human-in-the-loop交接机制.md|Human-in-the-loop 交接机制]] — **Human-in-the-loop (HITL)** 是指在 AI Agent 的自主执行循环中，在关键决策点引入人类审核、确认或介入的机制。它是 Agent 从实验环境走向生产环境的**必要安全网**。  🔴
- [[10-知识库/AI模型与Agent/04-智能体架构与工作流设计/4.5-AI-Agent架构开源学习指南.md|AI Agent 架构开源学习指南]] — ---  🔴
- [[10-知识库/AI模型与Agent/05-评测监控与安全防护/5.1-模型评测基准与Evals驱动开发.md|模型评测基准与 Evals 驱动开发]] — LLM Evaluation（大模型评测）是对语言模型能力的系统化度量。类比 .NET 工程中的单元测试 + 集成测试 + 性能基准测试：  🔴
- [[10-知识库/AI模型与Agent/05-评测监控与安全防护/5.2-可观测性与链路追踪.md|可观测性与链路追踪]] — 传统微服务可观测性（Metrics / Logs / Traces 三支柱）在 LLM 应用场景下严重不足：  🔴
- [[10-知识库/AI模型与Agent/05-评测监控与安全防护/5.3-AI安全护栏与防御机制.md|AI 安全护栏与防御机制]] — LLM 应用面临的安全威胁与传统 Web 应用截然不同：  🔴
- [[10-知识库/AI模型与Agent/06-工程落地与Vibe_Coding实战/6.1-终端IDE形态深度对比.md|终端 IDE 形态深度对比]] — 2025 年以来，AI 编码工具已分化为三个明确的形态：  🔴
- [[10-知识库/AI模型与Agent/06-工程落地与Vibe_Coding实战/6.2-CLI原生Agent实战.md|6.2 CLI原生Agent实战]] — 在 [[6.1-Vibe_Coding核心理念]] 中我们提到 Vibe Coding 的核心是"意图驱动"。但 VS Code 插件（Copilot / Cursor）本质上是 **IDE-first**，Agent 能力受限于编辑器沙箱  🔴
- [[10-知识库/AI模型与Agent/06-工程落地与Vibe_Coding实战/6.3-SWE-Agent端到端闭环开发.md|6.3 SWE-Agent 端到端闭环开发]] — SWE-Agent 由 Princeton 和 Stanford 联合推出（1.0 版本），核心贡献是提出了 **ACI（Agent-Computer Interface）** 的概念——一套专门为 LLM Agent 设计的"计算机操作接  🔴
- [[10-知识库/AI模型与Agent/README.md|02-AI知识星球]] — ---


## 🛠️ 工具速查

- [[10-知识库/工具速查/00-Global-Rules.md|全局规则（大秘/二秘统一遵守）]] — - 任何“有意义的产物”都要落到 GitHub（Obsidian 仓库）并可检索。 - 不允许只存在于聊天里。
- [[10-知识库/工具速查/01-Session-Management.md|会话管理（压缩/切会话策略）]] — 目的：避免长会话导致上下文膨胀（模型变笨/忘前文），同时保证关键信息不丢。
- [[10-知识库/工具速查/10-Best-Practices-Extract.md|Claude Code Best Practices（摘录 + 落地解读）]] — 来源（官方）：<https://code.claude.com/docs/en/best-practices>
- [[10-知识库/工具速查/20-CLI-Cheatsheet.md|Claude Code CLI Cheatsheet（速查）]] — 来源（官方）：<https://code.claude.com/docs/en/cli-reference>
- [[10-知识库/工具速查/ClaudeCode工具/00-Overview.md|Claude Code 概览（落地导向）]] — Claude Code 是一个 **agentic coding 环境**：它不只是回答问题，而是能在你的项目里读文件、改文件、跑命令，按“探索→计划→实现→验证”的循环完成任务。
- [[10-知识库/工具速查/Diagram-Style.md|配图标准（强约束：禁止 AI 生图）]] — 1) **必须基于文章内容严谨生成**：图里每个实体、关系、层级，都要能在正文中找到对应依据。 2) **禁止随意发散与脑补**：正文没提到的模块/流程/术语，不得擅自补全。 3) **统一风格**：高级、极简、学术白板风（参考 Googl


## 📜 经典方法论

- [[10-知识库/经典方法论/01-工作流编排（Graphs & Workflows）.md|01-工作流编排（Graphs & Workflows）]] — 
- [[10-知识库/经典方法论/02-异步消息与事件驱动（Event-driven Messaging）.md|02-异步消息与事件驱动（Event-driven Messaging）]] — 
- [[10-知识库/经典方法论/03-平台化框架（DevUI_OTel_多语言）.md|03-平台化框架（DevUI_OTel_多语言）]] — 
- [[10-知识库/经典方法论/05-Handoff与Triage（交接_分诊）.md|05-Handoff与Triage（交接_分诊）]] — 
- [[10-知识库/经典方法论/07-AI Dev产品化（CLI_GUI_Cloud）.md|07-AI Dev产品化（CLI_GUI_Cloud）]] — 
- [[10-知识库/经典方法论/08-Observability与Evals（可观测_评测）.md|08-Observability与Evals（可观测_评测）]] — 
- [[10-知识库/经典方法论/09-HITL与Guardrails（人类在环_安全）.md|09-HITL与Guardrails（人类在环_安全）]] — 
- [[10-知识库/经典方法论/10-经典方法论（ReAct_Reflexion_ToT_MetaGPT）.md|10-经典方法论（ReAct_Reflexion_ToT_MetaGPT）]] — 
- [[10-知识库/经典方法论/30-Checkpointing.md|Checkpointing（回退/回放机制）]] — 来源（官方）：<https://code.claude.com/docs/en/checkpointing>


## 🎓 DeepLearning.AI学习路径

- [[10-知识库/DeepLearning.AI学习路径/DeepLearning.AI-学习路径.md|DeepLearning.AI 学习资料（面向工程师）]] — 数据抓取来源：DeepLearning.AI 课程索引（Algolia index: courses_date_desc）  🔴


## 🗄️ 旧笔记归档

- [[10-知识库/旧笔记归档/SQLServer_Dacpac包加密与自动化部署.md|SQLServer_Dacpac包加密与自动化部署 (PowerShell+AES256)]] — **日期**: 2026-04-08 **关联**: 基于 2026-04-07 讨论的 [[SQL Server]] 存储过程加密方案 (防代码泄露) 的进一步延伸 (防介质泄漏)。  🟡
- [[10-知识库/旧笔记归档/SQLServer_存储过程加密方案_WITH_ENCRYPTION.md|[[SQL Server]] 存储过程加密方案 (WITH ENCRYPTION)]] — 为了防止拥有高级权限（如 `sa`）的人员轻易窥探和窃取核心业务存储过程源码，[[SQL Server]] 提供了原生的 `WITH ENCRYPTION` 选项。 - **作用**：通过对系统表中存储的源码进行内部混淆（异或算法），使 `  🟡
- [[10-知识库/旧笔记归档/SQLServer_高级加密方案_CLR_混淆.md|[[SQL Server]] 存储过程高级加密方案：CLR + 代码混淆]] — 原生 T-SQL 的 `WITH ENCRYPTION` 仅是一种可逆的代码混淆（文本异或），面对掌握专用工具的高级 DBA（具备 `sa` 或 `sysadmin` 权限），源码仍有被提取和还原的风险。


## 🧱 项目：BrickHub

- [[20-项目/BrickHub/4.5-BrickHub_Architecture_Vision.md|BrickHub 项目总体架构与愿景]] — BrickHub 项目目前的核心架构主要分为以下几个层次，旨在实现从自然语言到高质量 3D 乐高模型的生成与展示：
- [[20-项目/BrickHub/4.6-BrickHub_Technical_Research.md|BrickHub 进阶技术研究蓝图]] — **撰写：** 二秘小贝 🗂️（需求调研与知识库专员） **面向对象：** 三秘小马（研发）、老王（项目赞助人）、小虾（项目经理）  🟡
- [[20-项目/BrickHub/4.7-BrickHub_LDraw_Standard_Assets.md|BrickHub 标准 LDraw 测试素材库]] — 本素材库由二秘小贝整理，收录了四秘（小牛）在测试渲染引擎 `components/BrickRenderer.js` 及其核心解析逻辑 `parseLDraw` 时所采用的 4 个官方标准分类 LDraw 示例素材。这些素材能够为后续的渲染  🟡
- [[20-项目/BrickHub/4.8-BrickHub_Interactive_Engine_Architecture.md|BrickHub 2.0 互动拼搭引擎架构选型与技术白皮书 (TDD)]] — BrickHub 2.0 的核心目标是打造对标 Mecabricks 的**“可互动拖拽、可动态拆解的在线拼搭工厂”**。为实现数万级零件的高性能渲染与丝滑的拼搭交互，本白皮书针对四大核心技术难题进行了深度调研，并给出了明确的架构选型与代码  🟡
- [[20-项目/BrickHub/4.9-BrickHub_Engineering_Principles_and_Lessons.md|BrickHub 工程原则与血泪教训总结 (4.9)]] — **老王原话：“代码一定要优雅，一定要有结构性，架构化，哪怕多用点时间。不要写屎一样的代码。”**
- [[20-项目/BrickHub/Gemini提示词.md|Gemini提示词]] — 太棒了，我们这就开始 BrickHub 的第一步：实现**一个标准 2x6 乐高积木的 3D 渲染**。  🟡


## 🦛 项目：海马体（OpenHippo）

- [[20-项目/海马体/F5-Dream设计-v0.1.md|F5 Dream（记忆整合）设计 — v0.1 草案]] — ---  🔴
- [[20-项目/海马体/PRD分卷/prd-01-目的与痛点.md|PRD 一·二｜项目目的与解决痛点]] — ---
- [[20-项目/海马体/PRD分卷/prd-02-用户与开源形态.md|PRD 三·四｜目标用户与开源形态]] — ---
- [[20-项目/海马体/PRD分卷/prd-03-部署形式.md|PRD 五｜部署形式]] — ---
- [[20-项目/海马体/PRD分卷/prd-04-1-核心记忆操作.md|PRD 6.1｜核心记忆操作 (F1)]] — ---
- [[20-项目/海马体/PRD分卷/prd-04-2-协议与接入.md|PRD 6.2｜协议与接入 (F6-F8)]] — ---  🟡
- [[20-项目/海马体/PRD分卷/prd-04-3-生命周期管理.md|PRD 6.3｜记忆生命周期管理 (F9-F10)]] — ---  🟡
- [[20-项目/海马体/PRD分卷/prd-04-4-隔离与共享.md|PRD 6.4｜隔离与共享 (F11-F16)]] — ---  🔴
- [[20-项目/海马体/PRD分卷/prd-04-5-安全与智能.md|PRD 6.5｜安全与智能 (F17-F20)]] — ---  🔴
- [[20-项目/海马体/PRD分卷/prd-04-6-运维与集成.md|PRD 6.6｜运维与集成 (F21-F25)]] — ---  🔴
- [[20-项目/海马体/PRD分卷/prd-04-7-Dogfood迁移.md|PRD 6.7｜Dogfood迁移 (F26-F27)]] — ---  🟡
- [[20-项目/海马体/PRD分卷/prd-05-操作流程与架构.md|PRD 七·八｜操作流程与架构]] — ---  🟡
- [[20-项目/海马体/PRD分卷/prd-06-环境与里程碑.md|PRD 九·十｜环境与里程碑]] — ---  🟡
- [[20-项目/海马体/PRD分卷/prd-07-附录.md|PRD 附录｜API/Schema/ADR]] — ---  🔴
- [[20-项目/海马体/审查日志-v0.3-2026-04-20.md|OpenHippo 架构审查 v0.2 — 实施日志]] — ---  🟡
- [[20-项目/海马体/开发进度.md|[[项目需求文档(PRD)|OpenHippo]] 开发进度报告]] — ---  🟡
- [[20-项目/海马体/架构审查v0.2.md|[[项目需求文档(PRD)|OpenHippo]] 架构审查 v0.2]] — ---  🟡
- [[20-项目/海马体/测试方案与用例.md|🦛 OpenHippo 记忆系统测试方案与用例]] — 作为 Agent 记忆系统，OpenHippo 需满足以下行业标准：  🔴
- [[20-项目/海马体/竞品调研与商业计划书.md|海马体（Hippocampus）— 竞品调研与商业计划书]] — ---  🔴
- [[20-项目/海马体/访问凭证.md|海马体 访问凭证]] — - URL: https://hippo.brickhub.cc/ui/ - **鉴权**: Cloudflare Access (Email OTP, 仅 wang.pei@live.com，session 1 个月) - 内层 Bear
- [[20-项目/海马体/项目需求文档(PRD).md|🦛 海马体（Hippocampus）— PRD 索引]] — - [[竞品调研与商业计划书]] — Mem0/Letta/Zep等竞品分析 - [[F5-Dream设计-v0.1]] — F5 Dream（记忆整合）专项设计 - [[架构审查v0.2]] — 架构审查记录 - [[审查日志-v0.3-


## ⚡ 项目：Hermes Agent

- [[20-项目/Hermes/memory-system-upgrade.md|Hermes Memory System Upgrade]] — Hermes记忆系统存在三个核心问题： 1. **Gateway重启丢对话** — 重启无clean_shutdown标记→session被标记suspended→下次消息auto-reset 2. **session_search超时**  🔴


## 💭 项目：Dreaming（自主预研）

- [[20-项目/Dreaming/2026-04-17-research.md|BrickHub 每日报告 — 2026-04-17]] — 首次Dream B执行，选择最核心的渲染组件进行深度审查。
- [[20-项目/Dreaming/2026-04-18-research.md|BrickHub 每日报告]] — DSL编译器负责将LLM输出的JSON DSL编译为LDraw文本，是AI生成管线的核心环节。代码整体质量较高，防御性编程到位（readNum fallback、warning收集），但发现以下问题：
- [[20-项目/Dreaming/2026-04-19-research.md|BrickHub 每日报告]] — ldrawParser.js是纯逻辑层，无UI代码，无不符项。
- [[20-项目/Dreaming/2026-04-20-research.md|BrickHub 每日报告 — 2026-04-20]] — **现象**：`node -e` 调用 `buildSystemPrompt()`，返回字符串长度 **18,873 字符**（预期约 3.6KB）。 **根因**：`lib/llmPrompt.js:123` 的本意关闭符 `` `; `
- [[20-项目/Dreaming/2026-04-21-research.md|BrickHub 每日报告 — 2026-04-21]] — Phase 3 沙盒核心两文件——零件抽屉与场景容器。配合 `npm test` 全量回归。


## 🌏 调研：2026-04 中美AI模型与Agent全景

- [[30-调研报告/2026-04-中美AI模型与Agent全景/01-美国大模型.md|🇺🇸 美国五大家旗舰大模型（2026-04）]] — ---
- [[30-调研报告/2026-04-中美AI模型与Agent全景/02-中国大模型.md|🇨🇳 中国八大家旗舰大模型（2026-04）]] — ---  🟡
- [[30-调研报告/2026-04-中美AI模型与Agent全景/03-开源Agent框架.md|🛠️ 开源 Agent 框架 6 强（2026-04）]] — ---
- [[30-调研报告/2026-04-中美AI模型与Agent全景/04-编码Agent.md|💻 编码 Agent 6 强（2026-04）]] — ---
- [[30-调研报告/2026-04-中美AI模型与Agent全景/05-国产Agent产品.md|🇨🇳 国产 Agent 产品 4 强（2026-04）]] — ---
- [[30-调研报告/2026-04-中美AI模型与Agent全景/06-中美对比与趋势.md|⚖️ 中美对比 & 2026 趋势研判]] — ---  🟡
- [[30-调研报告/2026-04-中美AI模型与Agent全景/INDEX.md|2026 中美 AI 模型与 Agent 全景报告]] — ---


## 📊 调研：单篇报告

- [[30-调研报告/AI-Agent-Memory架构借鉴分析.md|AI Agent Memory 架构借鉴分析]] — ---  🔴
- [[30-调研报告/Claude-Opus-4.7-vs-4.6.md|Claude Opus 4.7 vs 4.6 对比]] — 1. **Extended Thinking移除** → 只能用 adaptive 模式 + effort 参数控制 2. **Sampling参数移除** → temperature / top_p / top_k 直接报400错误 3.
- [[30-调研报告/Hermes上下文管理优化方案.md|Hermes 上下文管理优化方案]] — ---  🔴
- [[30-调研报告/Memory-Agent-架构设计推演.md|Memory Agent 架构设计推演]] — ---  🟡
- [[30-调研报告/README.md|30-调研报告]] — 深度调研、对比分析、决策报告。**完成后只读**，新版本另开文件。 受 [[SCHEMA]] 约束。完整索引见 [[index]]。


## 📂 目录入口

- [[10-知识库/README.md|10-知识库]]
- [[20-项目/README.md|20-项目]]
- [[30-调研报告/README.md|30-调研报告]]


---

## 📈 健康度

- 总页数：**88**
- Frontmatter覆盖：**88/88** (100%)
- 超长页(>200行)：**28** 个 — 1.4-Embeddings与向量表示.md, 2.1-系统提示词与角色设定.md, 2.2-高阶推理策略.md, 2.3-结构化数据输出.md, 3.2-Model_Context_Protocol规范解析.md…
- 图标：🔴=>200行 🟡=100-200行

详细健康检查请运行 `kb-maintenance` skill。
