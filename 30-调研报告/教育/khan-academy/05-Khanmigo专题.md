---
title: Khanmigo AI Tutor 专题
created: 2026-05-26
updated: 2026-05-26
type: research
tags: [research, agent, prompt, family]
status: stable
---

# Khanmigo AI Tutor 专题

> Khan Academy 的 AI 老师产品，2023.03.14 与 GPT-4 同日发布。**目前 K-12 领域用户规模最大、设计最系统的 AI 教育产品**。本文是做"中文版 Khanmigo"的产品参考。

## 1. 产品定位 — 三种角色

Khanmigo 不是单一聊天机器人，而是按角色拆三套体验：

| 角色 | 核心价值 | 形态 |
|---|---|---|
| **Student Tutor** | 苏格拉底式辅导，**不直接给答案** | 嵌在每道 Khan Academy 习题/视频旁的侧边栏 chat |
| **Teacher Assistant** | 备课、出题、rubric、学情摘要、差异化教学 | 独立 dashboard，20+ Teacher Activities（Plan/Create/Differentiate/Support/Learn 五类） |
| **Parent Companion** | 看孩子聊天历史 + moderation alerts，大学申请辅导 | 家长账号下挂最多 10 个孩子 |

设计哲学源自 Bloom 1984 年的 **"2 Sigma Problem"**：一对一辅导能让学生提升 2 SD，但人力不可规模化——AI 是解 2 Sigma 的"廉价老师"路径（Sal Khan TED 演讲和《Brave New Words》全书主线）。

## 2. 核心交互设计（产品最关键的部分）

### 2.1 苏格拉底法 — "永不直接给答案"
- 学生写 "求 x" → Khanmigo 反问 "你觉得第一步应该做什么？"
- 学生答错 → 不说错，而是 "让我们看看 3×4 等于多少"，引导发现
- **与 ChatGPT/Photomath 最大的差异**：后者默认给完整解，Khanmigo 默认 **withhold**

### 2.2 角色扮演（Roleplay with historical/literary figures）
- 学生可以跟 **Jay Gatsby、Hamlet、富兰克林、居里夫人** 等对话
- prompt 模板锁定人物背景知识 + 时代语言风格 + 不出戏（refuse to break character）
- 写作课特色：让学生跟自己写的小说人物对话，深化人物塑造

### 2.3 写作辅导（Writing Coach）
- **不改作文**，而是 ask probing questions："你这段的论点是什么？""有什么证据支持？"
- 提供 **debate mode**：AI 扮演反方，逼学生论证

### 2.4 数学步骤引导
- 2025 年专门做了 **math computation enhancements**——之前 GPT-4 算数易错，现在调用外部计算工具
- 每步只引导一步（chunking），符合 cognitive load 理论

### 2.5 趣味元素
- 学习时长解锁 **hats**（Khanmigo 头像换帽子），轻度 gamification
- 但在严肃话题（核战、抑郁等）prompt 中**禁用 emoji**——这是真实迭代出来的（早期用户反馈 emoji 在沉重话题下不合适）

## 3. 技术栈

| 层 | 实现 |
|---|---|
| **Base Model** | OpenAI **GPT-4**（2023 首发）→ 现在通过 **Microsoft Azure OpenAI Service** 提供（教师版） |
| **是否 Fine-tune** | **没有传统意义的 fine-tune**，主要靠 **system prompt + 内容 grounding**。Sal Khan 公开说过：他们更依赖 prompt engineering 而不是 weight 微调 |
| **Grounding / 防幻觉** | 接入 Khan Academy 内容库（**429 门课程、43 种语言**），回答时引用知识库降低幻觉 |
| **个性化上下文** | 注入学生 profile：当前所学课程、技能掌握度、兴趣标签、首选语言 |
| **安全护栏** | 多层 moderation：① OpenAI Moderation API ② 自研敏感话题分类器 ③ 触发后通知家长/老师 ④ 对话日志全保留 |
| **数据隐私** | **Khan Academy 不允许 OpenAI 用学生/教师数据训练模型**（Common Sense Media 确认） |
| **反馈环** | 每条回答都有 👍/👎，按钮直接喂回 prompt 迭代；老师/家长可查任意对话 |

### Khan Academy 公开的 7-Step Prompt Engineering Framework

1. 理解理想师生关系
2. 引入学习科学（meet learners where they are / Goldilocks zone / immediate feedback / self-explanation）
3. 接入内容库做个性化
4. 设计 tutor 口吻、问题类型、安全护栏
5. 多 persona 用户测试
6. NIST 标准安全实践
7. 真实用户反馈持续迭代

A/B 测试驱动：Khan Academy 工程负责人 Kristen DiCerbo 公开过一项实验——**新版 prompt 让学生下一题正确率提升 3.4%**（LinkedIn）。

## 4. 定价与地区

| 用户 | 价格 | 备注 |
|---|---|---|
| **教师** | **完全免费** | 由 Microsoft 出钱（Azure OpenAI 算力赞助），**180+ 国家、30+ 种实验语言**（2025-12 数据） |
| **个人学习者** | **\$4/月 或 \$44/年** | **仅限美国账单地址** |
| **家庭** | **\$4/月 或 \$44/年** | 1 个家长账号可挂 10 个孩子 |
| **学区版（District Tools）** | 自定义报价 | Clever / ClassLink SSO、自动 rostering、学区数据看板、专属 CSM |

**学生侧地区限制**：**仅限美国**——因为未成年数据合规（COPPA、各州学校 AI 政策）尚未在海外打通。教师版已全球（除古巴、伊朗、朝鲜、叙利亚、俄占乌克兰地区）。

## 5. 实际效果数据

### 5.1 用户规模
- **2023-24 pilot**: 68,000 用户
- **2024-25**: **700,000+ 用户**（**一年增长 ~10×**）
- 整个 Khan Academy 生态：年触达 100M+ 学习者

### 5.2 学习提升
- Khan Academy 总平台数据：每周用 30+ 分钟 → MAP Growth 测试预期外提升 ~20%（不直接归因 Khanmigo，但平台叠加效应）
- 学术研究（EKU 大学物理课对照实验，Khanmigo vs Google Search）：两组都有显著学习收益，但**组间差异不显著**——说明 AI tutor 不一定碾压传统搜索，**关键在使用方式**
- TC Columbia 用 Chapelle CALL 框架评 Khanmigo 作语言学习工具：**对初学者法语作用有限**（语音、对话深度不足）
- A/B 测试：新版苏格拉底 prompt **下一题正确率 +3.4%**

### 5.3 老师反馈
- 备课时间下降（教师工作量 50%+ 在备课，Khanmigo 主打砍这部分）
- Rick Hess（AEI 教育研究员）实测：**好的对话非常像理想 tutor，但学生也会试图 game system 套答案**

## 6. 未来路线图与愿景

### Sal Khan 公开口径（TED 2023 + Brave New Words 2024 + 60 Minutes）

1. **"给每个孩子一个 AI personal tutor，给每个老师一个 AI teaching assistant"** — 直接对标古希腊亚里士多德教亚历山大的体验
2. **Voice mode 优先**：尤其低龄段，已经在做语音对话版（GPT-4o 后顺势接入）
3. **写作未来**：AI 实时陪写，"Process > Product"，看过程不只看成品（反作弊新范式）
4. **多模态**：摄像头识别学生在作业本上的草稿（手写识别 + 步骤反馈）
5. **班级整体感知**：老师 dashboard 能看到整个班的实时困惑点，做精准教学
6. **AI Native School**：Khan Lab School + Khan World School 已经把 AI 嵌入日常课程作为试点
7. **降到完全免费**：长期目标是学生版也免费（依赖捐赠 + 微软算力）

## 7. 主要争议

1. **数学准确性问题**（2024.02 WSJ 实测）：早期 Khanmigo 在基础计算上犯错，后通过外部计算工具修复
2. **学生 game system**：学生会试图套答案（Rick Hess 实测）
3. **效果难以独立归因**：EKU 大学物理 RCT 显示与 Google 搜索差异不显著
4. **付费墙偏离非营利初心**

## 主要来源

- khanmigo.ai / khanmigo.ai/pricing
- blog.khanacademy.org（7-Step Prompt Engineering、Microsoft 180 国扩展、2024 efficacy results）
- aka.ms/khanmigoforteachersexpansion（微软合作公告）
- Common Sense Media 2024-08 评测
- OpenAI Khan Academy case study（GPT-4 启动）
- Sal Khan TED 2023《How AI could save (not destroy) education》
- 《Brave New Words》Salman Khan, Viking 2024
- 学术：IRRODL Vol.26 No.4（2025）、Journal of Teaching and Learning（EKU 物理课实验）、ERIC EJ1435677（TC Columbia 法语评估）
- LinkedIn Kristen DiCerbo（A/B 3.4% 提升）
- 60 Minutes 2024 报道

## 关联

- [[06-竞品对比与启示]]
- [[../../10-知识库/AI模型与Agent/4.1-AI_Agent核心心智模型]]（待关联）
