---
title: AI 启蒙资源调研（娃 + 自己）
created: 2026-05-26
updated: 2026-05-26
type: research
tags: [research, family]
status: stable
---

# AI 启蒙资源调研

> 两层受众：(a) **4-12 岁孩子** AI 启蒙；(b) **老王自己** AI 入门到进阶（已是 Agent 重度用户，侧重原理深化与前沿跟踪）。

---

## 一、儿童 AI 启蒙资源（4-12 岁）

### 1. 可视化编程平台（AI 的"前置课"）

**ScratchJr** ⭐⭐⭐⭐⭐ **娃 4 岁中班正合适**
- iPad/安卓 App，图形拖拽无文字
- 5-7 岁，免费
- 先建立"指令→动作"因果直觉，后续一切 AI 课的基础

**Scratch 3.0（MIT）** ⭐⭐⭐⭐⭐
- 浏览器即用，可接 Google Teachable Machine、ML for Kids 扩展
- 7-12 岁，免费
- **最高性价比**，娃 6 岁起入门

**Code.org**（Hour of Code、CS Fundamentals）⭐⭐⭐⭐
- 课程体系完整，含 "AI for Oceans" 小课
- 6-15 岁，全免费

**Tynker** ⭐⭐⭐
- 商业版 Scratch，含 Minecraft/Roblox/无人机课程包
- 7-14 岁，$15/月。娃如果痴迷 Minecraft 再考虑

**micro:bit** ⭐⭐⭐⭐⭐ **软硬结合首选**
- 英国 BBC 出的口袋开发板，带传感器与 LED 阵列
- 8-14 岁，硬件 ¥150
- 便宜不锁生态

### 2. AI 玩具/机器人（警惕"已凉"产品）

**Anki Cozmo / Vector** ⚠️ **不建议**
- 曾经的"桌面 Pixar"
- Anki 2019 破产 → DDL 收购 → 2023.7 因未付 AWS 账单服务器全线下线 → 2024 才陆续部分恢复
- **现在买相当于赌运营寿命**

**Sphero（BOLT / indi）** ⭐⭐⭐⭐
- 球形机器人 + 块编程 + JavaScript
- 6-12 岁，¥800-1500
- 生态稳，学校用得多

**乐高 SPIKE Prime / Mindstorms** ⭐⭐⭐⭐
- ⚠️ Mindstorms EV3 已 2022 年停产；新线是 SPIKE Prime
- 8-14 岁，¥3000+
- **贵但保值**，配合 FLL 赛事路径清晰

**Makeblock mBot / Halocode** ⭐⭐⭐⭐
- 国产，含 AI 摄像头模块
- 8-14 岁，¥500-2000

**UBTech 优必选 Alpha Mini / JimuRobot** ⭐⭐
- ⚠️ 商业宣传重编程深度一般，售后与生态长期被吐槽
- 6-12 岁，¥2000+

### 3. AI 概念课与工具（真正"看见 AI"）

**Google Teachable Machine** ⭐⭐⭐⭐⭐ **强推**
- 浏览器训练图像/声音/姿态分类器，2 分钟出模型
- 8 岁+，免费
- **和娃一起"教电脑认猫狗"，理解"数据→模型"只需 5 分钟**

**Machine Learning for Kids**（Dale Lane，IBM 工程师公益项目）⭐⭐⭐⭐⭐
- 把 IBM Watson 接进 Scratch，做文本/图像/数字分类
- 配套书《Machine Learning for Kids》(No Starch, 2021)
- 9-14 岁，免费。教育圈口碑硬

**MIT App Inventor** ⭐⭐⭐⭐
- 拖拽做安卓 App，含 PersonalImageClassifier 等 AI 组件
- 10 岁+，免费

**Stable Diffusion / 文生图玩法** ⭐⭐⭐⭐
- 家长陪同下用 ComfyUI 或网页版"念咒造图"
- 6 岁+ 需家长陪
- **强推作为审美与提示词启蒙**，但要管控内容

### 4. 中文平台

**编程猫** ⭐⭐
- ⚠️ 长期被诟病"重营销重做题，自创积木与 Scratch 不通转出成本高"
- 可作启蒙体验，**不建议长期深绑**

**小码王** ⭐⭐⭐
- 线下+线上，主打信奥/NOIP 路径
- 8 岁+，几千到上万一年
- **适合走竞赛路线**

**核桃编程** ⭐⭐⭐
- 录播+AI 答疑，价格中等，体系比编程猫扎实

**CCtalk** ⭐⭐⭐
- 网易系直播课平台，大量个人老师开 Scratch/Python 课
- 质量参差，**需自己挑老师**

### 5. 绘本与书

**《Hello Ruby》系列**（Linda Liukas，芬兰）⭐⭐⭐⭐⭐ **强推娃 4 岁这阶段**
- 4-8 岁，不插电的计算思维绘本

**《Machine Learning for Kids》**（Dale Lane）：9 岁+ 项目书

**《动物园里的人工智能》《写给孩子的人工智能》**：国内绘本入门

---

## 二、成年人入门资源（老王自己用）

### 1. 系统课程

**吴恩达 DeepLearning.AI（Coursera）** ⭐⭐⭐⭐⭐
- 经典 ML / DL Specialization 仍是地基
- 新出短课《ChatGPT Prompt Eng for Devs》《LangChain》《Building Agentic RAG》**极适合老王**
- 每门 1-2 小时，全部免费旁听

**fast.ai《Practical Deep Learning for Coders》** ⭐⭐⭐⭐⭐
- Jeremy Howard，**自上而下**教学，先跑通再讲原理
- 免费，适合"工程师式"学法

**Hugging Face Learn** ⭐⭐⭐⭐⭐
- NLP / LLM / Audio / Agents 四套课全免费
- **老王最优解之一**——直接对应你在用的 Transformers/Datasets

**Andrej Karpathy《Neural Networks: Zero to Hero》YouTube** ⭐⭐⭐⭐⭐
- 从手撸 micrograd 到 GPT-2 复现到 Tokenizer 详解
- **全网最佳 LLM 原理课**，免费
- 配套 nanoGPT、llm.c 仓库
- **强推作为下一步核心投入**

### 2. 实践工具（每天用）

- **ChatGPT vs Claude vs Gemini 横向**：三家都开会员（合计约 $60/月）按任务分流——长文档与代码 Claude，多模态与搜索 Gemini，通用与生态 ChatGPT
- **Cursor / GitHub Copilot / Windsurf**：Cursor 目前体感最强 $20/月
- **Hermes Agent**（你已在用）：agentic 工作流本地化收口，配合 MCP
- **Ollama + LM Studio**：本地跑 Llama 3.x / Qwen / Mistral，理解部署与量化

### 3. 论文/博客（持续输入）

- **Lilian Weng**（lilianweng.github.io）："LLM Powered Autonomous Agents" 是 Agent 领域必读综述
- **Simon Willison**（simonwillison.net）：每天追 LLM 圈最实用英文博客，他写的 `llm` CLI 也好用
- **Andrej Karpathy** 推特/博客：思考密度极高
- **Sebastian Raschka**（magazine.sebastianraschka.com）：原理讲得清楚
- **Anthropic / OpenAI 官方 cookbook + research 页面**：跟踪能力边界

### 4. 中文资源

**李沐《动手学深度学习》（d2l-zh）** ⭐⭐⭐⭐⭐
- 第二版已稳定，PyTorch/MXNet/TF 三版本
- 免费在线书 + GitHub
- **中文最权威入门书**，习题完整

**B 站「跟李沐学 AI」** ⭐⭐⭐⭐⭐
- 李沐精读经典论文（Transformer/GPT/ResNet/AlphaFold）
- 每期 1 小时，**中文圈最高质量论文导读**

**B 站「3Blue1Brown」中文字幕**：神经网络与 Transformer 可视化，**和娃一起看反向传播那一集**

**机器之心 / 量子位 / PaperWeekly**：资讯类挑读，避免信息过载

---

## 三、两条路径建议

### 【娃 4 岁 → 10 岁 AI 启蒙路径】

1. **4-5 岁**：ScratchJr + 《Hello Ruby》绘本 + 和爸爸一起玩 Teachable Machine"认玩具"游戏。每周 1-2 次每次 15 分钟，**重点是好玩不是学会**
2. **6-7 岁**：Scratch 3.0 + Code.org "AI for Oceans" + Sphero/mBot 二选一。引入"训练数据"概念
3. **8-9 岁**：micro:bit 软硬结合做小项目（温湿度报警/计步器）+ Machine Learning for Kids 做"垃圾分类器""猜表情"项目
4. **10 岁**：Python 入门（codecombat 或 fast.ai kids 路径）+ MIT App Inventor 做带 AI 的小 App + 参加一次青少年 AI 挑战赛
5. **避坑**：不绑死编程猫这类封闭体系；机器人玩具选生态稳的（Sphero/乐高/micro:bit），不碰运营不稳的（Cozmo/Vector）

### 【老王 AI 进阶路径（已会用，下一步深化）】

1. **第 1 个月**：刷完 **Karpathy "Zero to Hero"** 全 8 集，跟着写 micrograd 与 nanoGPT，**真正理解 Transformer 与训练循环**
2. **第 2 个月**：Hugging Face **Agents Course + LLM Course**，把 Hermes Agent 工作流对照工业级框架（LangGraph/smolagents）重写一遍
3. **第 3 个月**：精读 Lilian Weng 的 Agent / Prompt / Hallucination 三篇综述，配 B 站李沐论文精读补 RLHF/DPO/MoE 背景
4. **持续**：Simon Willison 日更 + arXiv 周报 + Ollama 本地跑 Qwen3/Llama4 做隐私敏感任务
5. **副产出**：公司内部做一次"PFE 视角下的 LLM Agent 落地"分享——**输出倒逼输入**，老王这个段位最高效的学法

## 关联

- [[40-调研报告/教育/khan-academy/README|Khan Academy 调研]]
- [[40-调研报告/教育/math-startup|数学启蒙调研]]
- [[40-调研报告/教育/english-startup|英语启蒙调研]]
