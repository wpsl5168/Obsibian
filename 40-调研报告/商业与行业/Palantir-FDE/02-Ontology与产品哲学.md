---
title: 02 Ontology 与产品哲学
created: 2026-05-19
updated: 2026-09-09
type: research
tags: [research]
status: stable
---
# 02 Ontology 与产品哲学

> 为什么 Ontology 才是真正的护城河,FDE 只是采矿工。为什么 Palantir 没有传统 PM。deployment-as-R&D 的财务把戏怎么玩。

---

## 1. Ontology 是什么

**Ontology** 在 Palantir 语境里 = **客户业务对象的中心化知识图谱**。它不是数据库 schema,不是数据湖,是**业务概念 + 关系 + 操作 + 权限**的统一抽象层。

举个具体例子:
- 一家航空公司的 Ontology 里会有 `Aircraft`, `Flight`, `Crew`, `Maintenance Event`, `Fuel Order` 等对象,以及它们之间的关系(`Flight requires Crew`, `Aircraft has Maintenance Events` 等)
- 一旦 Ontology 建立,任何新应用(AI 助手、调度优化、合规报表)都基于同一组对象构建
- FDE 在每个项目里抽象出的"对象+关系",会被回流到一个跨客户的 Ontology 模式库

---

## 2. Karp 的护城河论断

> "All of the value in the market is going to go to chips and what we call ontology … The idea that chips and ontology is what you want to short is batsh*t crazy."
> "市场上所有的价值都将归于芯片和我们所说的本体(Ontology)……做空芯片和 Ontology 这个想法是疯到了家。"
> — Alex Karp, Q2 2025 股东信 / CNBC 采访(回应 Burry 做空)

Karp 把 Ontology 上升到与 NVIDIA 芯片同级的"AI 时代核心资产",这是个非常强的声明。

---

## 3. Palantir 官方对 Ontology 哲学的最系统阐述

Peter Wilczynski (Palantir Head of Product) 在 2024-01 博客 *Ontology-Oriented Software Development* 给出公司路线表述:

> "We've lost the plot by tricking ourselves into believing that because it's easier to build individual parts, someone else must be able to assemble them into something worthwhile."
> "我们已经迷失方向——自欺欺人地以为,因为造零件更容易,就一定有别人能把它们拼成有价值的东西。"

**核心论点**:
1. 现代软件世界过度迷信"乐高块组合"(microservices + API),但真正难的是组装
2. Ontology 把整合知识"中心化"一次,而不是每个新应用重复粘合
3. 这把"定制企业软件的边际成本推向零"

来源:blog.palantir.com/ontology-oriented-software-development-68d7353fdb12

---

## 4. 为什么 Palantir 没有传统 PM

直接说"我们没有 PM"的逐字原话**未找到**,但有强结构性证据。

**最接近的功能性解释**(Sankar 在 *Shawn Ryan Show* #190):
> "Military generals need to have a founder personality and a desire to understand the problems of the end-user – just like product managers in tech."
> "军队将领需要有创始人型的人格和理解终端用户问题的渴望——就像科技行业里的产品经理。"

**实际替代品**(fde.academy 总结):
> "You can think of a Dev's focus as one capability for many customers, while a Delta's focus is many capabilities for one customer."
> "Dev 的关注点是'一个能力服务很多客户',Delta 的关注点是'很多能力服务一个客户'。"

**为什么这样设计**(老王视角解读):
- 传统 PM 的核心痛点:产品规划脱离真实用户场景
- 传统咨询的核心痛点:交付不留资产(IP 归客户),无复利
- Echo + Delta 同时解决两个问题:既贴用户(Delta 在场),又产生平台资产(Echo 抽象出可复用 Ontology)
- 代价:对个体能力要求极高,招聘难度大,组织无法快速扩张

---

## 5. Deployment-as-R&D:财务把戏怎么玩

这是 FDE 模式最隐秘也最关键的一招。

**传统 SaaS 公司财务结构**:
- License 收入 → 高毛利(80%+)
- Professional Services 收入 → 低毛利(10-30%)
- Services 部分被分析师视为"低质量收入",拉低估值

**Palantir 的玩法**:
- 把大量 FDE 时间计入 **R&D 费用**,而不是 COGS(Cost of Goods Sold)
- 理由站得住:FDE 的代码会回流 Ontology/Foundry,本质是产品研发
- 财务效果:Gross Margin 86.8%(Q1 2026),Services Revenue 占比极低
- 资本市场效果:被估值为 SaaS(高 P/S)而非 SI(低 P/S)

**这是 Barry (ex-Palantir) 反复强调的"三大不可妥协条件"之一**:
> 真 FDE 要求 deployment 成本计为 R&D 而非 COGS。模仿者如果把 FDE 当 Sales Engineering 升级版,这条就守不住,毛利自然破不了 80%。

---

## 6. 给老王的关键启示

如果你要在个人咨询里复刻这套逻辑,需要回答:

1. **你的 Ontology 等价物是什么?** — Hermes Agent 的 skill 库?cron 模板?memory schema?这些资产能否跨客户复用,决定你是"按人天卖时间"还是"按资产卖复利"
2. **客户痛点抽象层是什么?** — 你解决的"中小企业 AI Agent 落地"问题,能不能抽出 5-10 个通用 primitive(知识库管理、对外触达、内部审批、客户服务、数据分析…)
3. **每个项目能不能 30% 时间回流到资产库?** — 如果不能,你就是高级外包;能,你就有了 Palantir 式的复利路径

这正是 [[40-调研报告/商业与行业/Palantir-FDE/07-移植到个人咨询.md]] 要 workshop 的核心问题。

---

## 参考

- Palantir Blog *Ontology-Oriented Software Development* (Wilczynski, 2024-01)
- Karp Q2 2025 股东信 + CNBC 采访(via Business Insider)
- Sankar *Shawn Ryan Show* #190
- Barry *Understanding Forward Deployed Engineering* (barry.ooo)