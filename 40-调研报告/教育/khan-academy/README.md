---
title: Khan Academy 可汗学院调研索引
created: 2026-05-26
updated: 2026-05-26
type: research
tags: [research, family]
status: stable
sources:
  - https://www.khanacademy.org
  - https://khanmigo.ai
  - https://blog.khanacademy.org
  - https://en.wikipedia.org/wiki/Khan_Academy
---

# Khan Academy 可汗学院调研

> 2026-05-26 系统化整理。基于官方年报、Wikipedia、SRI/Oreopoulos 等学术 RCT、Reddit/知乎口碑、EdWeek/Vice 批评、Common Sense Media 评测、Sal Khan TED + 著作，跨 15+ 一手与二手来源交叉验证。

## 一句话概括

非营利 K-12 教育平台，**起家于一段 YouTube 视频，长成全球 1.89 亿注册用户的标杆**；Khanmigo 是它押注下一个十年的 AI 老师产品。**优点是免费 + mastery learning 路径 + SAT 官方合作；缺点是"重程序轻概念、视频陈旧、中文版残缺"**；对中国家长**只能当辅助不能当主线**。

## 文件索引

| 文件 | 内容 |
|---|---|
| [[01-历史与里程碑]] | 2004 远程辅导表妹 → 2026 Gemini 整合的全时间线 |
| [[02-组织与财务]] | 501(c)(3) 结构、捐助方、年度收入、Sal Khan 薪酬争议 |
| [[03-产品矩阵与内容规模]] | 主站 / Kids / Khanmigo / SAT 备考四产品、842 门课、80M 活跃 |
| [[04-用户口碑与学术效果]] | 四个用户段真实口碑、SRI/RCT 学术研究、5 个主要争议 |
| [[05-Khanmigo专题]] | 三角色定位、苏格拉底交互、技术栈、定价、效果数据 |
| [[06-竞品对比与启示]] | vs IXL/Brilliant/猿辅导/学而思；做中文版的 5 条启示 |

## 核心结论速查（8 条）

1. **创业故事经典**：1 人录视频起步（2006）→ 2008 注册非盈利 → 2010 Gates + Google 200 万背书 → 2023 Khanmigo 与 GPT-4 同日发布，22 年走到全球教育 OS 候选位。
2. **财务模式独特**：全靠捐赠，2023 年收入约 \$107M，主要金主是 Gates 基金会、Google、AT&T、Musk Foundation、微软（算力赞助）。**不依赖订阅，反而是道护城河**。
3. **规模真实但增长靠 B 端**：累计 1.89 亿注册，但 Districts Partnerships（795 学区）模式效率比草根用户**高 8-14 倍**——B2B2C 比纯 C 端跑得快。
4. **教学法争议从未停过**：被批"程序操作多，概念推导少"，r/math、EdWeek、Vice 都有长文骂。Cathy Duffy 评测说**只适合中学（6-8）作主线**，K-5 太浅，高中以上不够深。
5. **学术 RCT 证据有限**：Oreopoulos 2024 美国 RCT 显示提升 0.12-0.22 SD；印度 RCT 0.44-0.47 SD。但**核心结论是"必须配教师引导"**，纯放任效果不显著。
6. **Khanmigo 是真正的标杆产品**：苏格拉底式引导、永不直接给答案、安全护栏完整、数据不喂回 OpenAI 训练——**目前 K-12 AI tutor 设计最系统的一家**。
7. **Khanmigo 定价聪明**：教师免费（微软买单）、家长/学生 \$4/月、学区 SSO 单独报价。**仅限美国账单地址**——海外用户被挡。
8. **对中国老王家娃判断**：Khan Kids 可作零成本英语 + 数学启蒙试水；**主线坚持人教/北师大体系**；3-4 年级后用 Khan 英文版做双语数学拓展。**不要当万能解药**。

## 给做"中文版 Khanmigo"的 5 条启示

1. **苏格拉底"不给答案"是灵魂，但要给中国家长做"双模式"**——考前救急模式可以给答案，平时学习模式坚持引导
2. **B2B2C 是 Khanmigo 验证过的最优路径**：教师免费 → 学校渠道 → 家长付费。中国校内 AI 受双减限制，**家长 C 端 + 教培机构 B 端** 更现实
3. **Prompt 即产品**：Khanmigo 没做 fine-tune，纯靠 system prompt + 内容 grounding。中文版基于 DeepSeek/Qwen/GLM 同样玩法可行
4. **内容库是护城河**：没有 KA 那种 842 门课，就找强教材合作（人教社、北师大、五三、黄冈密卷）
5. **A/B 测试 + 安全护栏 + 家长 Dashboard 是合规底线**，做 toC 教育产品这三件少一个都活不下去

## 关联

- Khanmigo MVP决策（待补充到00-收件箱）
- [[05-个人/家庭与孩子教育|家庭与孩子教育]]（待补 Khan Kids 试水方案）
- [[../../20-项目/hermespet/README]]（HermesPet 可借鉴 Khanmigo 角色化交互）
