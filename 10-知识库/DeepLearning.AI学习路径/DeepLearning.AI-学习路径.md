---
title: DeepLearning.AI 学习路径（工程师向）
created: 2026-03-31
updated: 2026-04-21
type: concept
tags: []
status: draft
source: https://www.deeplearning.ai/courses/
generated_at_utc: 2026-03-31
---

# DeepLearning.AI 学习资料（面向工程师）

数据抓取来源：DeepLearning.AI 课程索引（Algolia index: courses_date_desc）

抓取时间（UTC）：2026-03-31；总条目：121（本次拉取 121 条）

## 1) 课程/短课/证书/专题：可用的总目录入口

- 课程索引（包含 Short Courses / Courses / Specializations 等筛选）：https://www.deeplearning.ai/courses/
- Short Courses 入口（会重定向到 courses 索引）：https://www.deeplearning.ai/short-courses/

## 2) 推荐学习路径（入门 → 进阶 → 实战 → 专题）

### 第 0 章：学习环境与基线

- **学习目标**：搭建一套可复用的 LLM 应用开发与实验环境；掌握评估/记录习惯。
- **前置要求**：会基本 Python；能用 Git；能调用任意一家 LLM API（或本地模型）。
- **推荐顺序**：
  1) AI Python for Beginners（如果 Python 不熟）
  2) Jupyter AI: AI Coding in Notebooks（提升迭代效率）
- **关键知识点**：虚拟环境/依赖、notebook 工作流、提示与代码协作、实验记录。
- **练习/产出**：建立一个模板仓库：notebooks/、src/、eval/、prompts/、README，配好 lint/test。

### 第 1 章（入门）：Prompt Engineering + LLM 应用基本模式

- **学习目标**：掌握提示工程基础与常见 LLM 能力模式（总结/分类/改写/抽取/生成）。
- **前置要求**：会基础编程；了解 API 调用。
- **推荐顺序**：
  1) ChatGPT Prompt Engineering for Developers
  2) LangChain for LLM Application Development
  3) LangChain: Chat with Your Data（若想快速上手 RAG）
- **关键知识点**：指令/上下文/示例、输出约束（JSON/schema）、提示注入与安全、检索增强（chunking/embedding/检索/引用）。
- **练习/产出**：
  - 做一个“企业知识库问答”Demo：含检索、引用、答案结构化、拒答策略；
  - 建一个 prompts/ 目录：每个 prompt 配目标、输入输出 schema、失败案例与改进记录。

### 第 2 章（进阶）：Agents（规划-执行-反思）与工具调用

- **学习目标**：能设计多步任务的 agent；懂工具调用/沙箱执行/多 agent 协作；建立评估与可靠性手段。
- **前置要求**：熟悉第 1 章；有至少一个 RAG Demo。
- **推荐顺序**：
  1) Agentic AI
  2) Building Coding Agents with Tool Execution
  3) Multi AI Agent Systems with crewAI 或 Design, Develop, and Deploy Multi-Agent Systems with CrewAI
  4) Semantic Caching for AI Agents
  5) Agent Memory: Building Memory-Aware Agents
  6) A2A: The Agent2Agent Protocol（需要跨团队/框架互通时）
- **关键知识点**：
  - 规划（planner）/执行（executor）/验证（verifier）；
  - tool schema、权限与隔离、失败恢复与重试；
  - 多 agent 通信、角色分工、共享上下文；
  - 缓存、记忆（短期/长期/向量/结构化）、可观测性与评估。
- **练习/产出**：
  - 做一个“数据分析 agent”：能连接数据库/CSV，自动生成分析计划、执行查询、输出图表与报告；
  - 建一个 eval harness：用固定任务集跑回归，记录成功率/成本/延迟。

### 第 3 章（实战）：从 Demo 到可上线（LLMOps / Eval / Serving / 治理）

- **学习目标**：把 LLM/agent 系统做成可迭代的工程产品：可评估、可监控、可扩展、可治理。
- **前置要求**：做过至少一个 agent 或 RAG 项目。
- **推荐顺序（按痛点挑）**：
  - Evaluation and Monitoring 相关短课（以课程索引 topic 过滤：Evaluation and Monitoring / LLMOps）
  - Nvidia's NeMo Agent Toolkit: Making Agents Reliable（可靠性/可观测/部署视角）
  - Governing AI Agents（数据治理/合规）
- **关键知识点**：离线评估 vs 在线 A/B、日志与追踪、红队与安全测试、SLA/成本控制、版本管理。
- **练习/产出**：把你的 RAG/agent 服务化：Docker + API + 监控指标 + 评估流水线 + 回滚策略。

### 第 4 章（专题）：按领域深挖（按需选修）

- **GenAI 模型训练/后训练**：Build and Train an LLM with JAX；Fine-tuning and Reinforcement Learning for LLMs: Intro to Post-Training
- **开源模型与生态**：Open Source Models with Hugging Face
- **多模态与文档**：Document AI: From OCR to Agentic Doc Extraction；Multi-Vector Image Retrieval
- **深度学习体系化**：Deep Learning Specialization；PyTorch for Deep Learning Professional Certificate
- **ML 基础体系化**：Machine Learning Specialization
- **非技术同学/产品侧**：AI for Everyone；Generative AI for Everyone

## 3) 按主题快速索引（从抓取数据自动分组）

[[DeepLearning.AI-按主题索引|→ 详见独立子页]]

## 4) 全量目录（按课程类型）

[[DeepLearning.AI-全量目录|→ 详见独立子页]]

## 5) 维护方式（持续跟踪新增课程）

1) **定期拉取 Algolia index**（推荐每周/每月一次）：
   - Application ID: `Y5109WLMQW`
   - Index: `courses_date_desc`
   - 关键字段：`title/landing_page/course_type/topic/skill_level/date_timestamp`
2) 与上一版 JSON 做 diff：
   - 新增：按 `objectID` 或 `slug` 比对；
   - 变化：title/topic/course_type 变更要在大纲里同步。
3) 建议把 JSON 存到仓库/知识库：按日期归档，例如 `deeplearningai-courses-YYYY-MM-DD.json`，并生成一份“新增清单”。
4) 关注主页顶部 Announcement Banner（经常推新课），以及 The Batch 每周新闻。

---

## 📂 子页拆分

- [[DeepLearning.AI-按主题索引|DeepLearning.AI 按主题快速索引]]
- [[DeepLearning.AI-全量目录|DeepLearning.AI 全量课程目录]]
