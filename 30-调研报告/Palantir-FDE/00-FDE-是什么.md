---
title: 00 FDE 是什么
created: 2026-05-19
updated: 2026-05-19
type: research
tags: [research]
status: stable
---
# 00 FDE 是什么

> 厘清概念边界:FDE 不是一个 title,是一个工程家族;不是 PFE 的升级版,是组织结构的反向重构。

---

## 1. 官方定义:三大工程类别

Palantir 官方 careers 页把所有工程岗划分为三类,内部用希腊字母代号:

| 内部代号 | 对外 title | 职责 |
|---|---|---|
| **Deltas** | **Forward Deployed Software Engineer (FDSE)** | 直接面对客户,把 Foundry/Gotham/AIP 部署到真实业务问题上,确保 outcome 落地 |
| **Echos** | **Deployment Strategist** | "Win" — 识别问题、拆解 workflow、对齐 stakeholder |
| **Devs** | **Product Development Engineer** | 在总部造产品本身(Foundry/AIP 内核) |

**FDSE 的端到端职责**(Palantir Blog *Who Wants to be a Delta?*, 2021):
1. 与客户初步讨论、scope 业务问题
2. 决定如何部署 Foundry/Gotham/AIP
3. 与 Product Development 协作请求新能力
4. go-live 时支持用户
5. 赋能客户 IT 团队独立在 Foundry 上自建

**核心隐喻**:传统软件公司是"接力赛"(PM → Eng → Sales → CSM),FDSE 是**一个人跑完全程**。

---

## 2. "FDE" 不是单一 title,是岗位前缀家族

口语里的 "FDE" 实际涵盖以下子岗(都以 Forward Deployed 开头):

- **Forward Deployed Software Engineer (FDSE)** — 最主流,做应用/数据集成
- **Forward Deployed AI Engineer (FDAIE)** — 2024 后新拆,专注 AIP/LLM 用例
- **Forward Deployed Infrastructure Engineer** — Baseline Team,管 fleet / 环境 / 部署自动化、跨 commercial 与 classified 网络
- **Forward Deployed Reliability Engineer** — SRE 方向
- **Forward Deployed Security Engineer** — USG 安全合规
- **Forward Deployed Enablement Engineer** — Customer Success 方向
- **Forward Deployed Engineer - Mixed Reality / Edge Autonomous Systems / Autonomous Systems C2** — Gotham 国防方向特化

FDSE 是其中**人数最多、最核心的子岗**。

---

## 3. Echo + Delta 双角色结构(替代传统 PM)

Palantir 的招牌组织设计:**没有传统 Product Manager**,由 Echo + Delta 联合承担 PM 职责。

| 角色 | 关注点 | 类比 |
|---|---|---|
| **Echo (Deployment Strategist)** | 客户业务/领域知识,识别值得做的问题 | 类似咨询公司 BA + 行业专家 |
| **Delta (FDSE)** | 多个能力服务一个客户(deep on customer) | 类似全栈工程师 + Solution Architect |
| **Dev (Product Eng)** | 一个能力服务多个客户(deep on product) | 类似传统 SaaS 产品工程师 |

**关键不同**:Echo 不是 PM,它没有产品 roadmap 决策权;Delta 也不是纯执行,它有权直接修改 Foundry/Ontology 来满足客户。这个组合**绕过了"PM 写需求 → Eng 实现"的分工税**,但代价是对个体能力要求极高。

---

## 4. FDE ≠ PFE 升级版(老王视角)

这一节是为有 Microsoft PFE 背景的老王特别加的对比。

| 维度 | Palantir FDE | Microsoft PFE |
|---|---|---|
| **介入时机** | 售前/共创,产品未定型时进场 | 售后,客户已购产品 |
| **核心动作** | Product discovery + 代码回流 | Proactive/reactive support,排障兜底 |
| **写产品代码?** | 是,代码常被吸收进 Foundry/Ontology | 否,做配置/排障/Workshop |
| **激励** | "做出可复用的 platform primitive" | 客户满意度 + 利用率 |
| **失败成本** | Palantir 自吸(R&D) | 客户已付费,SLA 兜底 |
| **典型背景** | 工程师 + 领域好奇心,愿意出差 | 资深工程师,深 Microsoft 技术栈 |
| **职业天花板** | FDE → Lead → Head → GM/COO (Sankar 路径) | PFE → CSM/TAM → Architect |

**老王能直接复用的能力**:
- 客户面对面沟通、多 stakeholder 协调
- 复杂系统调试和根因分析
- 在不完美环境下推动方案落地
- FSI/电信领域知识

**需要切换的思维模式**:
- troubleshoot 思维 → product discovery 思维
- "我帮客户用好产品" → "我帮客户共创产品"
- 服从 SLA → 容忍 R&D 失败率

---

## 5. 关键事实速记

- **创立时间**:2006 年 Sankar 加入后逐步成型
- **岗位数(2024)**:Palantir 全公司约 4000 人,FDE 系列估计 800-1200 人(占工程团队 30-40%,**官方不披露**)
- **薪资 median**(US):total comp ~$227K,base ~$154K + stock ~$60K + bonus ~$13K
- **通过率**:14%(Jointaro 样本)
- **核心 KPI**:不是 chargeable hours,是客户业务 outcome 和"代码是否回流 Ontology"

---

## 参考

- Palantir Blog *Who Wants to be a Delta?* (2021)
- Palantir UK Careers page
- fde.academy *How Palantir Invented the Forward Deployed Engineer Model*
- Barry (ex-Palantir) *Understanding Forward Deployed Engineering* — barry.ooo