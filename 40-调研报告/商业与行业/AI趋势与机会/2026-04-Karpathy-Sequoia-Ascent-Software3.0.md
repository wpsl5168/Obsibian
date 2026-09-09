---
title: Karpathy @ Sequoia Ascent 2026 · Software 3.0 / Agentic Engineering / Jagged Intelligence
created: 2026-06-09
updated: 2026-09-09
type: research
tags: [research, agent, llm, vibe-coding, evaluation]
status: stable
sources: ["https://karpathy.bearblog.dev/sequoia-ascent-2026", "https://www.youtube.com/watch?v=96jN2OCOfLs"]
---

# Karpathy @ Sequoia Ascent 2026

> 信源：karpathy.bearblog.dev/sequoia-ascent-2026（炉边谈话，对谈 Stephanie Zhan，2026-04-30 发布）
> 抓取：bearblog 反爬，走 jina reader 取全文（含 Karpathy 用 Codex 5.5 生成的 summary + cleaned transcript）
> 元层面彩蛋：这份总结本身是他把所有近期博客+推文喂给 LLM、再让它读 transcript 生成的——本身就是 Software 3.0 / LLM Wiki 的 dogfood

## 一句话定性

Karpathy 把"2025年12月是 agentic 拐点"系统化成一套世界观：**AI 正成为数字工作的新操作层**，稀缺性从"写代码"转移到"理解 / 品味 / 验证 / 编排"。

---

## 核心论点链

### ① 拐点 + 新范式
- "我从没像现在这样觉得自己作为程序员落后了"——不是编程变难，是默认工作流变了。2025年12月起代码块变大、连贯、可靠到他想不起上次纠错是什么时候。
- 编程单元：从"敲行"→"委派宏动作"（实现功能 / 重构子系统 / 调研库 / 建服务 / 写测试跑测试修 bug / 比较方案给计划）。**程序员 = agent 编排者。**
- Software 演进：1.0 写代码 → 2.0 训权重（造数据集+目标+架构）→ **3.0 用 context window 编程**（prompt / tools / memory / examples / instructions）。LLM 是解释器，context 是你的杠杆。

### ② 软件开始消失
- **MenuGen 时刻**：老版要 OCR + 图像生成 + 前端 + 部署 + auth + 支付一整套；新版 = 拍照丢给多模态模型（Gemini + Nano Banana），直接把菜品图渲染进菜单像素里。神经网络直接做 media→media 变换。
- 金句：**"有些 app 不该再以 app 形式存在。"** AI 不只是更快造旧应用，而是旧应用的脚手架整个该消失。
- 更大的机会不是"更快编程"，是**自动化了以前无法编程的信息处理**。该问的不是"什么流程能加速"，而是"什么信息变换以前不可能、现在变自然了"。
- 极限外推："neural computer"——设备把原始视频/音频喂进神经网，用 diffusion 实时渲染当下专属 UI；神经网从虚拟化在经典计算机上，翻转为 host process，CPU 沦为协处理器。

### ③ 可验证性（Verifiability）—— 全文理论内核
- **传统软件自动化你能"指定（specify）"的；LLM + RL 自动化你能"验证（verify）"的。** 有自动 reward 信号的任务（数学/代码/测试/游戏）进步飞快，因为可重置、可重复、可奖励。
- 这也是为什么 coding agent 体感远超 chatbot——代码有持续反馈（测试过没过、跑没跑崩、diff 可审、benchmark 可测）。

### ④ Jagged Intelligence（锯齿状智能）两轴
- **能力 ≈ 可验证性 × 训练关注度**（× 数据覆盖 × 经济价值）。模型没有说明书，是 pretraining 配比 + RL 环境 + benchmark 压力 + 商业激励的产物，某些点尖峰、某些点诡异地蠢。
- 棋力例子：GPT-3.5→GPT-4 下棋变强不是通用智能平滑提升，是有人往训练集塞了大量棋谱→局部能力尖峰。
- 新版"strawberry 几个字母"：问"50 米外洗车店该开车还是走路"，SOTA 模型可能答走路——但你是要**洗车**，车得开过去。能重构十万行代码、能找 0-day，却让你走路去洗车，这就是 jaggedness。
- 实操结论：**判断"你在不在模型的轨道上（on the rails）"**。在可验证+重训练区→模型起飞；在区外→基础失败，得靠更好的 context / tools / fine-tune / 自建 evals / 自建 RL 环境。

### ⑤ Vibe Coding vs Agentic Engineering
- Vibe coding **抬地板**（人人能描述即造软件，适合原型/个人工具）；Agentic engineering **抬天花板**（专业纪律：协调易错的 agent 同时守住正确性/安全/品味/可维护）。
- agentic engineer 不盲收生成代码：设计 spec、监督计划、审 diff、写测试、建 eval loop、管权限、隔离 worktree。
- **MenuGen 支付 bug**：agent 用 email 匹配 Stripe 购买和 Google 账户——但两个 email 可能不同，该用 persistent user ID。前沿技能不是记 API 细节（`dim` 还是 `axis`），是理解底层概念（存储/视图/不变量/身份/安全边界）。
- "10x 工程师"会被放大到**远超 10x**。

### ⑥ 创业者机会
- 找**有价值 + 可验证 + labs 还没重点训练**的领域。能造领域专属 RL 环境→自己 fine-tune 也能提升。数学/代码已被 labs 占满，但很多经济重要领域有未开发的潜在可验证结构。**这就是 startup wedge。**（详见 [[40-调研报告/商业与行业/AI趋势与机会/2026-盈利线索-可验证RL环境wedge.md]]）
- **Agent-native 基础设施**：为 agent 而非人构建。文档别再写"点这个按钮"——真正的用户是人的 agent。需要 markdown 文档 / CLI / API / MCP server / 结构化日志 / 可粘贴的 agent 指令 / 可审计动作 / headless 安装。框架 = **sensors**（世界状态→数字信息）+ **actuators**（让 agent 改变世界）。
- 招聘该变：别再出小 puzzle。让候选人用 agent 造个大项目+部署+加固，再放对抗 agent 去攻破（"造个 agent 版 Twitter 克隆，我放 10 个 Codex 来攻"）。

### ⑦ 两个心智模型
- **Ghosts, not animals**：LLM 不是动物，没有生物驱动/好奇心/具身生存压力，是人类产物的统计模拟。拟人化期待会误导你（冲它吼没用）。正确姿态：经验性熟悉，边用边摸清哪 work 哪 fail——既不轻视也不盲信。
- **教育**：金句 **"你能外包思考，但不能外包理解（outsource thinking, not understanding）。"** agent 干再多活，人仍是瓶颈——得知道什么值得造、什么问题重要、什么结果可疑、什么取舍可接受。microGPT（单文件无依赖 GPT 训练+推理）就是把教育产物压缩到人和 agent 都能审查。补充观察：他试图让 LLM 把 microGPT 简化"得心脏病"——模型做不到极简，因为"不在 RL 回路里"，像拔牙。

---

## 大图景：稀缺性转移

- **变便宜**：代码生成、API 记忆、样板、初稿、重复配置、简单变换
- **变稀缺**：理解、品味、eval 设计、安全、系统边界、agent 编排、领域反馈循环、**判断模型何时脱轨**

收尾公式：
```
定义 context → 定义 tools → 定义反馈循环 → 定义护栏 → 让 agent 干 → 守住人的理解
```

---

## 对老王体系的映射（高度重合）

- **LLM Wiki = Obsidian KB + 海马体记忆系统**。Karpathy 把"增量把杂乱文档编译成持久 Markdown 知识库（摘要/实体页/概念页/矛盾/交叉链接）"当杀手级模式背书——正是 research-to-kb / 记忆 Agent 在做的。他说"理解是瓶颈，KB 是增强理解的工具"，跟"剥离独立记忆 Agent"构想同源。本 vault 的 SCHEMA.md 本就注明受 Karpathy LLM Wiki 启发。
- **Skill = 该粘贴给 agent 的那段文字**。OpenClaw 安装例子（brittle shell script → 一段文字丢给 agent）直接印证 Hermes skill 设计哲学。`wp-` skills 体系就是 Software 3.0 的程序单元。
- **multi-role 班子（architect/dev/qa）= agentic engineering 实践**：spec→审 diff→对抗评审，"协调易错 agent 守住质量"已在跑。
- **盈利 wedge 聚焦**：从"全景扫描"收敛到三条筛选标准——高价值 + 可验证 + labs 未训练。

## 相关

- [[40-调研报告/商业与行业/AI趋势与机会/2026-盈利线索-可验证RL环境wedge.md]] — 本文 ⑥ 衍生的可执行盈利线索
- [[40-调研报告/商业与行业/AI趋势与机会/2026-AI风口-张雪峰视角.md]] — 另一视角的风口调研
- Karpathy 前作：[Verifiability](https://karpathy.bearblog.dev/verifiability/)、[Animals vs. Ghosts](https://karpathy.bearblog.dev/animals-vs-ghosts/)、[MenuGen](https://karpathy.bearblog.dev/vibe-coding-menugen/)
