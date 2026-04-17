---
title: DeepLearning.AI 学习路径（工程师向）
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

### GenAI / Prompt / Agents（110）
- [Short Courses] **Agent Memory: Building Memory-Aware Agents** — Agents  
  https://www.deeplearning.ai/short-courses/agent-memory-building-memory-aware-agents
- [Short Courses] **Build and Train an LLM with JAX** — GenAI Applications  
  https://www.deeplearning.ai/short-courses/build-and-train-an-llm-with-jax
- [Short Courses] **A2A: The Agent2Agent Protocol** — Agents  
  https://www.deeplearning.ai/short-courses/a2a-the-agent2agent-protocol
- [Short Courses] **Agent Skills with Anthropic** — Agents  
  https://www.deeplearning.ai/short-courses/agent-skills-with-anthropic
- [Short Courses] **Gemini CLI: Code & Create with an Open-Source Agent** — AI Coding, Task Automation  
  https://www.deeplearning.ai/short-courses/gemini-cli-code-and-create-with-an-open-source-agent
- [Courses] **Build with Andrew** — AI Coding  
  https://www.deeplearning.ai/courses/build-with-andrew
- [Short Courses] **Nvidia's NeMo Agent Toolkit: Making Agents Reliable** — Agents  
  https://www.deeplearning.ai/short-courses/nvidia-nat-making-agents-reliable
- [Short Courses] **Multi-Vector Image Retrieval** — AI Coding, Search and Retrieval  
  https://www.deeplearning.ai/short-courses/multi-vector-image-retrieval
- [Short Courses] **Building Coding Agents with Tool Execution** — Agents  
  https://www.deeplearning.ai/short-courses/building-coding-agents-with-tool-execution
- [Short Courses] **Semantic Caching for AI Agents** — Agents  
  https://www.deeplearning.ai/short-courses/semantic-caching-for-ai-agents
- [Courses] **Design, Develop, and Deploy Multi-Agent Systems with CrewAI** — Agents  
  https://www.deeplearning.ai/courses/design-develop-and-deploy-multi-agent-systems-with-crewai
- [Short Courses] **Jupyter AI: AI Coding in Notebooks** — AI Coding  
  https://www.deeplearning.ai/short-courses/jupyter-ai-coding-in-notebooks
- [Courses] **Fine-tuning and Reinforcement Learning for LLMs: Intro to Post-Training** — Fine-Tuning  
  https://www.deeplearning.ai/courses/fine-tuning-and-reinforcement-learning-for-llms-intro-to-post-training
- [Short Courses] **Governing AI Agents** — Agents  
  https://www.deeplearning.ai/short-courses/governing-ai-agents
- [Short Courses] **Building Live Voice Agents with Google’s ADK** — Agents  
  https://www.deeplearning.ai/short-courses/building-live-voice-agents-with-googles-adk
- [Courses] **Agentic AI** — Agents  
  https://www.deeplearning.ai/courses/agentic-ai
- [Short Courses] **Building and Evaluating Data Agents** — Agents  
  https://www.deeplearning.ai/short-courses/building-and-evaluating-data-agents
- [Short Courses] **Build AI Apps with MCP Servers: Working with Box Files** — AI Frameworks, Agents, Data Processing, Document Processing  
  https://www.deeplearning.ai/short-courses/build-ai-apps-with-mcp-server-working-with-box-files
- [Short Courses] **Knowledge Graphs for AI Agent API Discovery ** — Agents, Embeddings, Search and Retrieval, Vector Databases  
  https://www.deeplearning.ai/short-courses/knowledge-graphs-for-ai-agent-api-discovery
- [Short Courses] **Agentic Knowledge Graph Construction** — AI Frameworks, Agents, Data Engineering, Data Processing  
  https://www.deeplearning.ai/short-courses/agentic-knowledge-graph-construction
- [Courses] **Fast Prototyping of GenAI Apps with Streamlit** — Chatbots, GenAI Applications, Prompt Engineering, RAG  
  https://www.deeplearning.ai/courses/fast-prototyping-of-genai-apps-with-streamlit
- [Short Courses] **Claude Code: A Highly Agentic Coding Assistant** — AI Coding, AI in Software Development, Agents, Chatbots  
  https://www.deeplearning.ai/short-courses/claude-code-a-highly-agentic-coding-assistant
- [Short Courses] **Pydantic for LLM Workflows** — Evaluation and Monitoring, Fine-Tuning, Generative Models, LLMOps  
  https://www.deeplearning.ai/short-courses/pydantic-for-llm-workflows
- [Courses] **Retrieval Augmented Generation (RAG)** — Data Processing, Document Processing, RAG  
  https://www.deeplearning.ai/courses/retrieval-augmented-generation-rag
- [Short Courses] **Post-training of LLMs** — Evaluation and Monitoring, Fine-Tuning, Generative Models, LLMOps  
  https://www.deeplearning.ai/short-courses/post-training-of-llms
- [Short Courses] **Building with Llama 4** — Chatbots, GenAI Applications, Generative Models, MultiModal  
  https://www.deeplearning.ai/short-courses/building-with-llama-4
- [Short Courses] **Orchestrating Workflows for GenAI Applications** — Data Engineering, Data Processing, Embeddings, Evaluation and Monitoring  
  https://www.deeplearning.ai/short-courses/orchestrating-workflows-for-genai-applications
- [Short Courses] **DSPy: Build and Optimize Agentic Apps** — AI Frameworks, Agents, Evaluation and Monitoring, GenAI Applications  
  https://www.deeplearning.ai/short-courses/dspy-build-optimize-agentic-apps
- [Short Courses] **Reinforcement Fine-Tuning LLMs with GRPO** — Evaluation and Monitoring, Fine-Tuning, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/reinforcement-fine-tuning-llms-grpo
- [Short Courses] **MCP: Build Rich-Context AI Apps with Anthropic** — AI Coding, AI Frameworks, Agents, Chatbots  
  https://www.deeplearning.ai/short-courses/mcp-build-rich-context-ai-apps-with-anthropic
- [Short Courses] **Building AI Voice Agents for Production** — Agents, Evaluation and Monitoring, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/building-ai-voice-agents-for-production
- [Short Courses] **LLMs as Operating Systems: Agent Memory** — Agents, LLMOps, Prompt Engineering, RAG  
  https://www.deeplearning.ai/short-courses/llms-as-operating-systems-agent-memory
- [Short Courses] **Building Code Agents with Hugging Face smolagents** — AI Safety, Evaluation and Monitoring, GenAI Applications, Prompt Engineering  
  https://www.deeplearning.ai/short-courses/building-code-agents-with-hugging-face-smolagents
- [Short Courses] **Building AI Browser Agents** — AI Frameworks, Agents, Evaluation and Monitoring, Fine-Tuning  
  https://www.deeplearning.ai/short-courses/building-ai-browser-agents
- [Short Courses] **Getting Structured LLM Output** — AI in Software Development, GenAI Applications, LLMOps, Prompt Engineering  
  https://www.deeplearning.ai/short-courses/getting-structured-llm-output
- [Short Courses] **Vibe Coding 101 with Replit** — AI Coding, AI in Software Development, Agents, GenAI Applications  
  https://www.deeplearning.ai/short-courses/vibe-coding-101-with-replit
- [Short Courses] **Long-Term Agentic Memory with LangGraph** — Agents, Chatbots, Embeddings, Evaluation and Monitoring  
  https://www.deeplearning.ai/short-courses/long-term-agentic-memory-with-langgraph
- [Short Courses] **Event-Driven Agentic Document Workflows** — Agents, Document Processing, Embeddings, Event-Driven AI  
  https://www.deeplearning.ai/short-courses/event-driven-agentic-document-workflows
- [Short Courses] **Build Apps with Windsurf’s AI Coding Agents** — AI Coding, AI in Software Development, Agents, GenAI Applications  
  https://www.deeplearning.ai/short-courses/build-apps-with-windsurfs-ai-coding-agents
- [Short Courses] **Evaluating AI Agents** — Agents, Evaluation and Monitoring, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/evaluating-ai-agents
- …（略）该组共 110 门，详见 JSON 全量目录文件。

### ML / DL 基础（36）
- [Specializations] **PyTorch for Deep Learning Professional Certificate** — Deep Learning  
  https://www.deeplearning.ai/courses/pytorch-for-deep-learning-professional-certificate
- [Short Courses] **Pydantic for LLM Workflows** — Evaluation and Monitoring, Fine-Tuning, Generative Models, LLMOps  
  https://www.deeplearning.ai/short-courses/pydantic-for-llm-workflows
- [Short Courses] **Post-training of LLMs** — Evaluation and Monitoring, Fine-Tuning, Generative Models, LLMOps  
  https://www.deeplearning.ai/short-courses/post-training-of-llms
- [Short Courses] **Building with Llama 4** — Chatbots, GenAI Applications, Generative Models, MultiModal  
  https://www.deeplearning.ai/short-courses/building-with-llama-4
- [Short Courses] **Reinforcement Fine-Tuning LLMs with GRPO** — Evaluation and Monitoring, Fine-Tuning, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/reinforcement-fine-tuning-llms-grpo
- [Short Courses] **Building AI Voice Agents for Production** — Agents, Evaluation and Monitoring, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/building-ai-voice-agents-for-production
- [Short Courses] **Attention in Transformers: Concepts and Code in PyTorch** — Deep Learning, Embeddings, GenAI Applications, Machine Learning  
  https://www.deeplearning.ai/short-courses/attention-in-transformers-concepts-and-code-in-pytorch
- [Short Courses] **How Transformer LLMs Work** — Deep Learning, Embeddings, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/how-transformer-llms-work
- [Short Courses] **Build Long-Context AI Apps with Jamba** — Document Processing, GenAI Applications, Generative Models, NLP  
  https://www.deeplearning.ai/short-courses/build-long-context-ai-apps-with-jamba
- [Short Courses] **Reasoning with o1** — Agents, GenAI Applications, MultiModal, NLP  
  https://www.deeplearning.ai/short-courses/reasoning-with-o1
- [Short Courses] **Collaborative Writing and Coding with OpenAI Canvas** — AI Coding, Agents, GenAI Applications, MultiModal  
  https://www.deeplearning.ai/short-courses/collaborative-writing-and-coding-with-openai-canvas
- [Short Courses] **Safe and Reliable AI via Guardrails** — AI Safety, Chatbots, Evaluation and Monitoring, GenAI Applications  
  https://www.deeplearning.ai/short-courses/safe-and-reliable-ai-via-guardrails
- [Short Courses] **Introducing Multimodal Llama 3.2** — Agents, Chatbots, Computer Vision, Fine-Tuning  
  https://www.deeplearning.ai/short-courses/introducing-multimodal-llama-3-2
- [Specializations] **Generative AI for Software Development** — AI Coding, AI Frameworks, AI in Software Development, Chatbots  
  https://www.deeplearning.ai/courses/generative-ai-for-software-development
- [Specializations] **Data Engineering** — Data Engineering, Data Processing, Deep Learning, Search and Retrieval  
  https://www.deeplearning.ai/courses/data-engineering
- [Short Courses] **Improving Accuracy of LLM Applications** — AI Frameworks, Agents, Evaluation and Monitoring, Fine-Tuning  
  https://www.deeplearning.ai/short-courses/improving-accuracy-of-llm-applications
- [Short Courses] **Pretraining LLMs** — Deep Learning, Evaluation and Monitoring, Fine-Tuning, GenAI Applications  
  https://www.deeplearning.ai/short-courses/pretraining-llms
- [Short Courses] **Introduction to On-Device AI** — Data Processing, Deep Learning, Compression and Quantization, On-Device AI  
  https://www.deeplearning.ai/short-courses/introduction-to-on-device-ai
- [Courses] **Machine Learning in Production** — Data Engineering, Deep Learning, MLOps  
  https://www.deeplearning.ai/courses/machine-learning-in-production
- [Short Courses] **Prompt Engineering for Vision Models** — Computer Vision, Diffusion Models, Fine-Tuning, Generative Models  
  https://www.deeplearning.ai/short-courses/prompt-engineering-for-vision-models
- [Short Courses] **Preprocessing Unstructured Data for LLM Applications** — Computer Vision, Document Processing, GenAI Applications, RAG  
  https://www.deeplearning.ai/short-courses/preprocessing-unstructured-data-for-llm-applications
- [Short Courses] **Open Source Models with Hugging Face** — Chatbots, Generative Models, MultiModal, NLP  
  https://www.deeplearning.ai/short-courses/open-source-models-hugging-face
- [Short Courses] **Understanding and Applying Text Embeddings** — Embeddings, GenAI Applications, NLP, RAG  
  https://www.deeplearning.ai/short-courses/google-cloud-vertex-ai
- [Short Courses] **Finetuning Large Language Models** — Deep Learning, Fine-Tuning, Transformers  
  https://www.deeplearning.ai/short-courses/finetuning-large-language-models
- [Short Courses] **Large Language Models with Semantic Search** — Embeddings, NLP, RAG, Search and Retrieval  
  https://www.deeplearning.ai/short-courses/large-language-models-semantic-search
- [Short Courses] **LangChain: Chat with Your Data** — Computer Vision, Document Processing, Embeddings, RAG  
  https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data
- [Short Courses] **How Diffusion Models Work** — Deep Learning, Diffusion Models, GenAI Applications, Generative Models  
  https://www.deeplearning.ai/short-courses/how-diffusion-models-work
- [Specializations] **AI for Good** — Computer Vision, Data Processing, GenAI Applications, NLP  
  https://www.deeplearning.ai/courses/ai-for-good
- [Specializations] **Mathematics for Machine Learning and Data Science** — Deep Learning, Mathematical Foundations, Supervised Learning  
  https://www.deeplearning.ai/courses/mathematics-for-machine-learning-and-data-science-specialization
- [Specializations] **Machine Learning Specialization** — Anomaly Detection, Deep Learning, Machine Learning, Supervised Learning  
  https://www.deeplearning.ai/courses/machine-learning-specialization
- [Specializations] **Generative Adversarial Networks (GANs)** — Computer Vision, Deep Learning, Generative Models  
  https://www.deeplearning.ai/courses/generative-adversarial-networks-gans-specialization
- [Specializations] **TensorFlow Developer Professional Certificate** — AI Frameworks, Computer Vision, Deep Learning, NLP  
  https://www.deeplearning.ai/courses/tensorflow-developer-professional-certificate
- [Specializations] **Natural Language Processing** — Chatbots, Embeddings, NLP, Transformers  
  https://www.deeplearning.ai/courses/natural-language-processing-specialization
- [Specializations] **Deep Learning Specialization** — Computer Vision, Deep Learning, NLP, Supervised Learning  
  https://www.deeplearning.ai/courses/deep-learning-specialization
- [Specializations] **AI for Medicine ** — Computer Vision, Deep Learning, Evaluation and Monitoring, Generative Models  
  https://www.deeplearning.ai/courses/ai-for-medicine-specialization
- [Courses] **AI for Everyone** — Deep Learning, Machine Learning  
  https://www.deeplearning.ai/courses/ai-for-everyone

### MLOps / LLMOps / 部署（41）
- [Short Courses] **Agentic Knowledge Graph Construction** — AI Frameworks, Agents, Data Engineering, Data Processing  
  https://www.deeplearning.ai/short-courses/agentic-knowledge-graph-construction
- [Short Courses] **Claude Code: A Highly Agentic Coding Assistant** — AI Coding, AI in Software Development, Agents, Chatbots  
  https://www.deeplearning.ai/short-courses/claude-code-a-highly-agentic-coding-assistant
- [Short Courses] **Pydantic for LLM Workflows** — Evaluation and Monitoring, Fine-Tuning, Generative Models, LLMOps  
  https://www.deeplearning.ai/short-courses/pydantic-for-llm-workflows
- [Short Courses] **Post-training of LLMs** — Evaluation and Monitoring, Fine-Tuning, Generative Models, LLMOps  
  https://www.deeplearning.ai/short-courses/post-training-of-llms
- [Short Courses] **Orchestrating Workflows for GenAI Applications** — Data Engineering, Data Processing, Embeddings, Evaluation and Monitoring  
  https://www.deeplearning.ai/short-courses/orchestrating-workflows-for-genai-applications
- [Short Courses] **DSPy: Build and Optimize Agentic Apps** — AI Frameworks, Agents, Evaluation and Monitoring, GenAI Applications  
  https://www.deeplearning.ai/short-courses/dspy-build-optimize-agentic-apps
- [Short Courses] **Reinforcement Fine-Tuning LLMs with GRPO** — Evaluation and Monitoring, Fine-Tuning, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/reinforcement-fine-tuning-llms-grpo
- [Short Courses] **MCP: Build Rich-Context AI Apps with Anthropic** — AI Coding, AI Frameworks, Agents, Chatbots  
  https://www.deeplearning.ai/short-courses/mcp-build-rich-context-ai-apps-with-anthropic
- [Short Courses] **Building AI Voice Agents for Production** — Agents, Evaluation and Monitoring, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/building-ai-voice-agents-for-production
- [Short Courses] **LLMs as Operating Systems: Agent Memory** — Agents, LLMOps, Prompt Engineering, RAG  
  https://www.deeplearning.ai/short-courses/llms-as-operating-systems-agent-memory
- [Short Courses] **Building Code Agents with Hugging Face smolagents** — AI Safety, Evaluation and Monitoring, GenAI Applications, Prompt Engineering  
  https://www.deeplearning.ai/short-courses/building-code-agents-with-hugging-face-smolagents
- [Short Courses] **Building AI Browser Agents** — AI Frameworks, Agents, Evaluation and Monitoring, Fine-Tuning  
  https://www.deeplearning.ai/short-courses/building-ai-browser-agents
- [Short Courses] **Getting Structured LLM Output** — AI in Software Development, GenAI Applications, LLMOps, Prompt Engineering  
  https://www.deeplearning.ai/short-courses/getting-structured-llm-output
- [Short Courses] **Long-Term Agentic Memory with LangGraph** — Agents, Chatbots, Embeddings, Evaluation and Monitoring  
  https://www.deeplearning.ai/short-courses/long-term-agentic-memory-with-langgraph
- [Short Courses] **Event-Driven Agentic Document Workflows** — Agents, Document Processing, Embeddings, Event-Driven AI  
  https://www.deeplearning.ai/short-courses/event-driven-agentic-document-workflows
- [Short Courses] **Evaluating AI Agents** — Agents, Evaluation and Monitoring, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/evaluating-ai-agents
- [Short Courses] **How Transformer LLMs Work** — Deep Learning, Embeddings, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/how-transformer-llms-work
- [Short Courses] **Building Towards Computer Use with Anthropic** — AI Coding, AI Safety, Agents, Chatbots  
  https://www.deeplearning.ai/short-courses/building-towards-computer-use-with-anthropic
- [Short Courses] **Building an AI-Powered Game** — AI Safety, AI in Software Development, GenAI Applications, Generative Models  
  https://www.deeplearning.ai/short-courses/building-an-ai-powered-game
- [Short Courses] **Safe and Reliable AI via Guardrails** — AI Safety, Chatbots, Evaluation and Monitoring, GenAI Applications  
  https://www.deeplearning.ai/short-courses/safe-and-reliable-ai-via-guardrails
- [Short Courses] **Improving Accuracy of LLM Applications** — AI Frameworks, Agents, Evaluation and Monitoring, Fine-Tuning  
  https://www.deeplearning.ai/short-courses/improving-accuracy-of-llm-applications
- [Short Courses] **Pretraining LLMs** — Deep Learning, Evaluation and Monitoring, Fine-Tuning, GenAI Applications  
  https://www.deeplearning.ai/short-courses/pretraining-llms
- [Short Courses] **Prompt Compression and Query Optimization** — Data Processing, GenAI Applications, LLMOps, Prompt Engineering  
  https://www.deeplearning.ai/short-courses/prompt-compression-and-query-optimization
- [Short Courses] **Carbon Aware Computing for GenAI Developers** — GenAI Applications, LLMOps, LLM Serving  
  https://www.deeplearning.ai/short-courses/carbon-aware-computing-for-genai-developers
- [Short Courses] **Building Your Own Database Agent** — Agents, Data Processing, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/building-your-own-database-agent
- [Short Courses] **Introduction to On-Device AI** — Data Processing, Deep Learning, Compression and Quantization, On-Device AI  
  https://www.deeplearning.ai/short-courses/introduction-to-on-device-ai
- [Courses] **Machine Learning in Production** — Data Engineering, Deep Learning, MLOps  
  https://www.deeplearning.ai/courses/machine-learning-in-production
- [Short Courses] **Quantization in Depth** — Compression and Quantization  
  https://www.deeplearning.ai/short-courses/quantization-in-depth
- [Short Courses] **Quantization Fundamentals with Hugging Face** — Generative Models, Compression and Quantization, MultiModal, Transformers  
  https://www.deeplearning.ai/short-courses/quantization-fundamentals-with-hugging-face
- [Short Courses] **Red Teaming LLM Applications** — AI Safety, Chatbots, Generative Models, LLMOps  
  https://www.deeplearning.ai/short-courses/red-teaming-llm-applications
- [Short Courses] **Efficiently Serving LLMs** — Fine-Tuning, Generative Models, LLMOps, LLM Serving  
  https://www.deeplearning.ai/short-courses/efficiently-serving-llms
- [Short Courses] **Prompt Engineering with Llama 2 & 3** — AI Safety, GenAI Applications, Generative Models, Prompt Engineering  
  https://www.deeplearning.ai/short-courses/prompt-engineering-with-llama-2
- [Short Courses] **Serverless LLM Apps with Amazon Bedrock** — Event-Driven AI, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/serverless-llm-apps-amazon-bedrock
- [Short Courses] **Automated Testing for LLMOps** — Evaluation and Monitoring, LLMOps, MLOps, Prompt Engineering  
  https://www.deeplearning.ai/short-courses/automated-testing-llmops
- [Short Courses] **LLMOps** — AI Safety, Chatbots, Data Processing, Evaluation and Monitoring  
  https://www.deeplearning.ai/short-courses/llmops
- [Short Courses] **Reinforcement Learning from Human Feedback** — Fine-Tuning, Generative Models, LLMOps, Transformers  
  https://www.deeplearning.ai/short-courses/reinforcement-learning-from-human-feedback
- [Short Courses] **Building and Evaluating Advanced RAG Applications** — AI Frameworks, Evaluation and Monitoring, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag
- [Short Courses] **Evaluating and Debugging Generative AI Models Using Weights and Biases** — Evaluation and Monitoring, Fine-Tuning, Generative Models, LLMOps  
  https://www.deeplearning.ai/short-courses/evaluating-debugging-generative-ai
- [Short Courses] **Building Systems with the ChatGPT API** — AI Safety, Chatbots, GenAI Applications, Generative Models  
  https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt
- [Specializations] **TensorFlow: Data and Deployment** — Data Processing, MLOps, On-Device AI  
  https://www.deeplearning.ai/courses/tensorflow-data-and-deployment-specialization
- …（略）该组共 41 门，详见 JSON 全量目录文件。

### 数据分析 / 数据工程基础（24）
- [Short Courses] **Document AI: From OCR to Agentic Doc Extraction** — Document Processing  
  https://www.deeplearning.ai/short-courses/document-ai-from-ocr-to-agentic-doc-extraction
- [Short Courses] **Build AI Apps with MCP Servers: Working with Box Files** — AI Frameworks, Agents, Data Processing, Document Processing  
  https://www.deeplearning.ai/short-courses/build-ai-apps-with-mcp-server-working-with-box-files
- [Short Courses] **Agentic Knowledge Graph Construction** — AI Frameworks, Agents, Data Engineering, Data Processing  
  https://www.deeplearning.ai/short-courses/agentic-knowledge-graph-construction
- [Short Courses] **Claude Code: A Highly Agentic Coding Assistant** — AI Coding, AI in Software Development, Agents, Chatbots  
  https://www.deeplearning.ai/short-courses/claude-code-a-highly-agentic-coding-assistant
- [Courses] **Retrieval Augmented Generation (RAG)** — Data Processing, Document Processing, RAG  
  https://www.deeplearning.ai/courses/retrieval-augmented-generation-rag
- [Specializations] **Data Analytics Professional Certificate** — Data Engineering, Data Processing, Synthetic Data  
  https://www.deeplearning.ai/courses/data-analytics
- [Short Courses] **Orchestrating Workflows for GenAI Applications** — Data Engineering, Data Processing, Embeddings, Evaluation and Monitoring  
  https://www.deeplearning.ai/short-courses/orchestrating-workflows-for-genai-applications
- [Short Courses] **Event-Driven Agentic Document Workflows** — Agents, Document Processing, Embeddings, Event-Driven AI  
  https://www.deeplearning.ai/short-courses/event-driven-agentic-document-workflows
- [Short Courses] **Build Long-Context AI Apps with Jamba** — Document Processing, GenAI Applications, Generative Models, NLP  
  https://www.deeplearning.ai/short-courses/build-long-context-ai-apps-with-jamba
- [Specializations] **Generative AI for Software Development** — AI Coding, AI Frameworks, AI in Software Development, Chatbots  
  https://www.deeplearning.ai/courses/generative-ai-for-software-development
- [Specializations] **Data Engineering** — Data Engineering, Data Processing, Deep Learning, Search and Retrieval  
  https://www.deeplearning.ai/courses/data-engineering
- [Short Courses] **Building AI Applications with Haystack** — AI Frameworks, AI in Software Development, Agents, Document Processing  
  https://www.deeplearning.ai/short-courses/building-ai-applications-with-haystack
- [Short Courses] **Prompt Compression and Query Optimization** — Data Processing, GenAI Applications, LLMOps, Prompt Engineering  
  https://www.deeplearning.ai/short-courses/prompt-compression-and-query-optimization
- [Short Courses] **Building Your Own Database Agent** — Agents, Data Processing, GenAI Applications, LLMOps  
  https://www.deeplearning.ai/short-courses/building-your-own-database-agent
- [Short Courses] **AI Agents in LangGraph** — AI Frameworks, Agents, Chatbots, Document Processing  
  https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph
- [Short Courses] **Introduction to On-Device AI** — Data Processing, Deep Learning, Compression and Quantization, On-Device AI  
  https://www.deeplearning.ai/short-courses/introduction-to-on-device-ai
- [Courses] **Machine Learning in Production** — Data Engineering, Deep Learning, MLOps  
  https://www.deeplearning.ai/courses/machine-learning-in-production
- [Short Courses] **Preprocessing Unstructured Data for LLM Applications** — Computer Vision, Document Processing, GenAI Applications, RAG  
  https://www.deeplearning.ai/short-courses/preprocessing-unstructured-data-for-llm-applications
- [Short Courses] **Building Applications with Vector Databases** — Anomaly Detection, Embeddings, MultiModal, Vector Databases  
  https://www.deeplearning.ai/short-courses/building-applications-vector-databases
- [Short Courses] **LLMOps** — AI Safety, Chatbots, Data Processing, Evaluation and Monitoring  
  https://www.deeplearning.ai/short-courses/llmops
- [Short Courses] **LangChain: Chat with Your Data** — Computer Vision, Document Processing, Embeddings, RAG  
  https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data
- [Specializations] **AI for Good** — Computer Vision, Data Processing, GenAI Applications, NLP  
  https://www.deeplearning.ai/courses/ai-for-good
- [Specializations] **Machine Learning Specialization** — Anomaly Detection, Deep Learning, Machine Learning, Supervised Learning  
  https://www.deeplearning.ai/courses/machine-learning-specialization
- [Specializations] **TensorFlow: Data and Deployment** — Data Processing, MLOps, On-Device AI  
  https://www.deeplearning.ai/courses/tensorflow-data-and-deployment-specialization

## 4) 全量目录（按课程类型）

### Courses（10）
- **Build with Andrew**  
  https://www.deeplearning.ai/courses/build-with-andrew
- **Design, Develop, and Deploy Multi-Agent Systems with CrewAI**  
  https://www.deeplearning.ai/courses/design-develop-and-deploy-multi-agent-systems-with-crewai
- **Fine-tuning and Reinforcement Learning for LLMs: Intro to Post-Training**  
  https://www.deeplearning.ai/courses/fine-tuning-and-reinforcement-learning-for-llms-intro-to-post-training
- **Agentic AI**  
  https://www.deeplearning.ai/courses/agentic-ai
- **Fast Prototyping of GenAI Apps with Streamlit**  
  https://www.deeplearning.ai/courses/fast-prototyping-of-genai-apps-with-streamlit
- **Retrieval Augmented Generation (RAG)**  
  https://www.deeplearning.ai/courses/retrieval-augmented-generation-rag
- **Machine Learning in Production**  
  https://www.deeplearning.ai/courses/machine-learning-in-production
- **Generative AI for Everyone**  
  https://www.deeplearning.ai/courses/generative-ai-for-everyone
- **Generative AI with LLMs**  
  https://www.deeplearning.ai/courses/generative-ai-with-llms
- **AI for Everyone**  
  https://www.deeplearning.ai/courses/ai-for-everyone

### Short Courses（97）
- **Agent Memory: Building Memory-Aware Agents**  
  https://www.deeplearning.ai/short-courses/agent-memory-building-memory-aware-agents
- **Build and Train an LLM with JAX**  
  https://www.deeplearning.ai/short-courses/build-and-train-an-llm-with-jax
- **A2A: The Agent2Agent Protocol**  
  https://www.deeplearning.ai/short-courses/a2a-the-agent2agent-protocol
- **Agent Skills with Anthropic**  
  https://www.deeplearning.ai/short-courses/agent-skills-with-anthropic
- **Gemini CLI: Code & Create with an Open-Source Agent**  
  https://www.deeplearning.ai/short-courses/gemini-cli-code-and-create-with-an-open-source-agent
- **Document AI: From OCR to Agentic Doc Extraction**  
  https://www.deeplearning.ai/short-courses/document-ai-from-ocr-to-agentic-doc-extraction
- **Nvidia's NeMo Agent Toolkit: Making Agents Reliable**  
  https://www.deeplearning.ai/short-courses/nvidia-nat-making-agents-reliable
- **Multi-Vector Image Retrieval**  
  https://www.deeplearning.ai/short-courses/multi-vector-image-retrieval
- **Building Coding Agents with Tool Execution**  
  https://www.deeplearning.ai/short-courses/building-coding-agents-with-tool-execution
- **Semantic Caching for AI Agents**  
  https://www.deeplearning.ai/short-courses/semantic-caching-for-ai-agents
- **Jupyter AI: AI Coding in Notebooks**  
  https://www.deeplearning.ai/short-courses/jupyter-ai-coding-in-notebooks
- **Governing AI Agents**  
  https://www.deeplearning.ai/short-courses/governing-ai-agents
- **Building Live Voice Agents with Google’s ADK**  
  https://www.deeplearning.ai/short-courses/building-live-voice-agents-with-googles-adk
- **Building and Evaluating Data Agents**  
  https://www.deeplearning.ai/short-courses/building-and-evaluating-data-agents
- **Build AI Apps with MCP Servers: Working with Box Files**  
  https://www.deeplearning.ai/short-courses/build-ai-apps-with-mcp-server-working-with-box-files
- **Knowledge Graphs for AI Agent API Discovery **  
  https://www.deeplearning.ai/short-courses/knowledge-graphs-for-ai-agent-api-discovery
- **Agentic Knowledge Graph Construction**  
  https://www.deeplearning.ai/short-courses/agentic-knowledge-graph-construction
- **Claude Code: A Highly Agentic Coding Assistant**  
  https://www.deeplearning.ai/short-courses/claude-code-a-highly-agentic-coding-assistant
- **Pydantic for LLM Workflows**  
  https://www.deeplearning.ai/short-courses/pydantic-for-llm-workflows
- **Post-training of LLMs**  
  https://www.deeplearning.ai/short-courses/post-training-of-llms
- **Building with Llama 4**  
  https://www.deeplearning.ai/short-courses/building-with-llama-4
- **Orchestrating Workflows for GenAI Applications**  
  https://www.deeplearning.ai/short-courses/orchestrating-workflows-for-genai-applications
- **DSPy: Build and Optimize Agentic Apps**  
  https://www.deeplearning.ai/short-courses/dspy-build-optimize-agentic-apps
- **Reinforcement Fine-Tuning LLMs with GRPO**  
  https://www.deeplearning.ai/short-courses/reinforcement-fine-tuning-llms-grpo
- **MCP: Build Rich-Context AI Apps with Anthropic**  
  https://www.deeplearning.ai/short-courses/mcp-build-rich-context-ai-apps-with-anthropic
- **Building AI Voice Agents for Production**  
  https://www.deeplearning.ai/short-courses/building-ai-voice-agents-for-production
- **LLMs as Operating Systems: Agent Memory**  
  https://www.deeplearning.ai/short-courses/llms-as-operating-systems-agent-memory
- **Building Code Agents with Hugging Face smolagents**  
  https://www.deeplearning.ai/short-courses/building-code-agents-with-hugging-face-smolagents
- **Building AI Browser Agents**  
  https://www.deeplearning.ai/short-courses/building-ai-browser-agents
- **Getting Structured LLM Output**  
  https://www.deeplearning.ai/short-courses/getting-structured-llm-output
- **Vibe Coding 101 with Replit**  
  https://www.deeplearning.ai/short-courses/vibe-coding-101-with-replit
- **Long-Term Agentic Memory with LangGraph**  
  https://www.deeplearning.ai/short-courses/long-term-agentic-memory-with-langgraph
- **Event-Driven Agentic Document Workflows**  
  https://www.deeplearning.ai/short-courses/event-driven-agentic-document-workflows
- **Build Apps with Windsurf’s AI Coding Agents**  
  https://www.deeplearning.ai/short-courses/build-apps-with-windsurfs-ai-coding-agents
- **Evaluating AI Agents**  
  https://www.deeplearning.ai/short-courses/evaluating-ai-agents
- **Attention in Transformers: Concepts and Code in PyTorch**  
  https://www.deeplearning.ai/short-courses/attention-in-transformers-concepts-and-code-in-pytorch
- **How Transformer LLMs Work**  
  https://www.deeplearning.ai/short-courses/how-transformer-llms-work
- **Building Towards Computer Use with Anthropic**  
  https://www.deeplearning.ai/short-courses/building-towards-computer-use-with-anthropic
- **Build Long-Context AI Apps with Jamba**  
  https://www.deeplearning.ai/short-courses/build-long-context-ai-apps-with-jamba
- **Reasoning with o1**  
  https://www.deeplearning.ai/short-courses/reasoning-with-o1
- **Collaborative Writing and Coding with OpenAI Canvas**  
  https://www.deeplearning.ai/short-courses/collaborative-writing-and-coding-with-openai-canvas
- **Building an AI-Powered Game**  
  https://www.deeplearning.ai/short-courses/building-an-ai-powered-game
- **Safe and Reliable AI via Guardrails**  
  https://www.deeplearning.ai/short-courses/safe-and-reliable-ai-via-guardrails
- **Practical Multi AI Agents and Advanced Use Cases with crewAI**  
  https://www.deeplearning.ai/short-courses/practical-multi-ai-agents-and-advanced-use-cases-with-crewai
- **Serverless Agentic Workflows with Amazon Bedrock**  
  https://www.deeplearning.ai/short-courses/serverless-agentic-workflows-with-amazon-bedrock
- **Introducing Multimodal Llama 3.2**  
  https://www.deeplearning.ai/short-courses/introducing-multimodal-llama-3-2
- **Retrieval Optimization: From Tokenization to Vector Quantization**  
  https://www.deeplearning.ai/short-courses/retrieval-optimization-from-tokenization-to-vector-quantization
- **AI Python for Beginners**  
  https://www.deeplearning.ai/short-courses/ai-python-for-beginners
- **Large Multimodal Model Prompting with Gemini**  
  https://www.deeplearning.ai/short-courses/large-multimodal-model-prompting-with-gemini
- **Building AI Applications with Haystack**  
  https://www.deeplearning.ai/short-courses/building-ai-applications-with-haystack
- **Improving Accuracy of LLM Applications**  
  https://www.deeplearning.ai/short-courses/improving-accuracy-of-llm-applications
- **Embedding Models: From Architecture to Implementation**  
  https://www.deeplearning.ai/short-courses/embedding-models-from-architecture-to-implementation
- **Federated Learning**  
  https://www.deeplearning.ai/short-courses/intro-to-federated-learning
- **Pretraining LLMs**  
  https://www.deeplearning.ai/short-courses/pretraining-llms
- **Prompt Compression and Query Optimization**  
  https://www.deeplearning.ai/short-courses/prompt-compression-and-query-optimization
- **Carbon Aware Computing for GenAI Developers**  
  https://www.deeplearning.ai/short-courses/carbon-aware-computing-for-genai-developers
- **Function-Calling and Data Extraction with LLMs**  
  https://www.deeplearning.ai/short-courses/function-calling-and-data-extraction-with-llms
- **Building Your Own Database Agent**  
  https://www.deeplearning.ai/short-courses/building-your-own-database-agent
- **AI Agents in LangGraph**  
  https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph
- **AI Agentic Design Patterns with AutoGen **  
  https://www.deeplearning.ai/short-courses/ai-agentic-design-patterns-with-autogen
- **Introduction to On-Device AI**  
  https://www.deeplearning.ai/short-courses/introduction-to-on-device-ai
- **Multi AI Agent Systems with crewAI**  
  https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai
- **Building Multimodal Search and RAG**  
  https://www.deeplearning.ai/short-courses/building-multimodal-search-and-rag
- **Building Agentic RAG with LlamaIndex**  
  https://www.deeplearning.ai/short-courses/building-agentic-rag-with-llamaindex
- **Quantization in Depth**  
  https://www.deeplearning.ai/short-courses/quantization-in-depth
- **Prompt Engineering for Vision Models**  
  https://www.deeplearning.ai/short-courses/prompt-engineering-for-vision-models
- **Getting Started With Mistral**  
  https://www.deeplearning.ai/short-courses/getting-started-with-mistral
- **Quantization Fundamentals with Hugging Face**  
  https://www.deeplearning.ai/short-courses/quantization-fundamentals-with-hugging-face
- **Preprocessing Unstructured Data for LLM Applications**  
  https://www.deeplearning.ai/short-courses/preprocessing-unstructured-data-for-llm-applications
- **Red Teaming LLM Applications**  
  https://www.deeplearning.ai/short-courses/red-teaming-llm-applications
- **JavaScript RAG Web Apps with LlamaIndex**  
  https://www.deeplearning.ai/short-courses/javascript-rag-web-apps-with-llamaindex
- **Efficiently Serving LLMs**  
  https://www.deeplearning.ai/short-courses/efficiently-serving-llms
- **Knowledge Graphs for RAG**  
  https://www.deeplearning.ai/short-courses/knowledge-graphs-rag
- **Open Source Models with Hugging Face**  
  https://www.deeplearning.ai/short-courses/open-source-models-hugging-face
- **Prompt Engineering with Llama 2 & 3**  
  https://www.deeplearning.ai/short-courses/prompt-engineering-with-llama-2
- **Serverless LLM Apps with Amazon Bedrock**  
  https://www.deeplearning.ai/short-courses/serverless-llm-apps-amazon-bedrock
- **Building Applications with Vector Databases**  
  https://www.deeplearning.ai/short-courses/building-applications-vector-databases
- **Automated Testing for LLMOps**  
  https://www.deeplearning.ai/short-courses/automated-testing-llmops
- **LLMOps**  
  https://www.deeplearning.ai/short-courses/llmops
- **Build LLM Apps with LangChain.js**  
  https://www.deeplearning.ai/short-courses/build-llm-apps-with-langchain-js
- **Advanced Retrieval for AI with Chroma**  
  https://www.deeplearning.ai/short-courses/advanced-retrieval-for-ai
- **Reinforcement Learning from Human Feedback**  
  https://www.deeplearning.ai/short-courses/reinforcement-learning-from-human-feedback
- **Building and Evaluating Advanced RAG Applications**  
  https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag
- **Vector Databases: from Embeddings to Applications**  
  https://www.deeplearning.ai/short-courses/vector-databases-embeddings-applications
- **Functions, Tools and Agents with LangChain**  
  https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain
- **Pair Programming with a Large Language Model**  
  https://www.deeplearning.ai/short-courses/pair-programming-llm
- **Understanding and Applying Text Embeddings**  
  https://www.deeplearning.ai/short-courses/google-cloud-vertex-ai
- **How Business Thinkers Can Start Building AI Plugins With Semantic Kernel**  
  https://www.deeplearning.ai/short-courses/microsoft-semantic-kernel
- **Finetuning Large Language Models**  
  https://www.deeplearning.ai/short-courses/finetuning-large-language-models
- **Large Language Models with Semantic Search**  
  https://www.deeplearning.ai/short-courses/large-language-models-semantic-search
- **Evaluating and Debugging Generative AI Models Using Weights and Biases**  
  https://www.deeplearning.ai/short-courses/evaluating-debugging-generative-ai
- **Building Generative AI Applications with Gradio**  
  https://www.deeplearning.ai/short-courses/building-generative-ai-applications-with-gradio
- **LangChain: Chat with Your Data**  
  https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data
- **How Diffusion Models Work**  
  https://www.deeplearning.ai/short-courses/how-diffusion-models-work
- **LangChain for LLM Application Development**  
  https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development
- **Building Systems with the ChatGPT API**  
  https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt
- **ChatGPT Prompt Engineering for Developers**  
  https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers

### Specializations（14）
- **PyTorch for Deep Learning Professional Certificate**  
  https://www.deeplearning.ai/courses/pytorch-for-deep-learning-professional-certificate
- **Data Analytics Professional Certificate**  
  https://www.deeplearning.ai/courses/data-analytics
- **Generative AI for Software Development**  
  https://www.deeplearning.ai/courses/generative-ai-for-software-development
- **Data Engineering**  
  https://www.deeplearning.ai/courses/data-engineering
- **AI for Good**  
  https://www.deeplearning.ai/courses/ai-for-good
- **Mathematics for Machine Learning and Data Science**  
  https://www.deeplearning.ai/courses/mathematics-for-machine-learning-and-data-science-specialization
- **Machine Learning Specialization**  
  https://www.deeplearning.ai/courses/machine-learning-specialization
- **TensorFlow: Advanced Techniques**  
  https://www.deeplearning.ai/courses/tensorflow-advanced-techniques-specialization
- **Generative Adversarial Networks (GANs)**  
  https://www.deeplearning.ai/courses/generative-adversarial-networks-gans-specialization
- **TensorFlow: Data and Deployment**  
  https://www.deeplearning.ai/courses/tensorflow-data-and-deployment-specialization
- **TensorFlow Developer Professional Certificate**  
  https://www.deeplearning.ai/courses/tensorflow-developer-professional-certificate
- **Natural Language Processing**  
  https://www.deeplearning.ai/courses/natural-language-processing-specialization
- **Deep Learning Specialization**  
  https://www.deeplearning.ai/courses/deep-learning-specialization
- **AI for Medicine **  
  https://www.deeplearning.ai/courses/ai-for-medicine-specialization

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
