# 03 AIP Bootcamp 五日模式

> 2023 年发明的 5 天压缩交付模式,把 FDE 方法论变成销售飞轮。直接拉动 ARR 翻倍、股价 $15→$80。

---

## 1. 官方定义

来自 palantir.com/platforms/aip/bootcamp:

> **"From 0 to use case in 5 days."**

5 天 immersive、hands-on-keyboard session,产出 3 个目标:
1. **Understand** 怎么把 AI 用到 mission-critical 业务
2. **Develop** 第一批 use case in software(直接跑客户自家数据,不是 demo 数据)
3. **Onboard & Train** 用户准备 rollout

官方提的 6 条 "Why it works":
1. Solving real business problems immediately
2. Defining your architecture empirically
3. Moving from chat to automation(不止 LLM 对话,要落到 workflow 自动化)
4. Driving change across industries & functions
5. Making AI your own
6. Lowering the floor, raising the ceiling

---

## 2. 发明者与初衷

**发明人**:**Ted Mabrey**(Palantir 全球商业负责人)在 2023 年 AIPCon 上正式宣布并主推。

> "In 2023, Palantir pioneered the bootcamp wave. Now, everyone is surfing. That's a good thing. Redefining the software procurement process …"
> "2023 年 Palantir 开创了 bootcamp 浪潮。现在所有人都在冲浪——这是好事。它重新定义了软件采购流程……"
> — Ted Mabrey, LinkedIn

**初衷原话**:
> "The value of getting started is so important, and you will move so much more quickly if we can reduce the friction to allow you to get started."
> "'开始'这件事本身价值巨大——如果我们能把启动摩擦降下来,你就会快得多。"
> — Ted Mabrey, AIPCon 宣布 AIP Bootcamps

**底层逻辑**:绕过传统 RFP / POC 销售流程——把 FDE 方法论压缩到 5 天工作坊里。

---

## 3. 5 天的具体跑法

综合 GTM Foundry + Bloomberg + Karp earnings call 的描述:

| Day | 活动 | 关键动作 |
|---|---|---|
| **Day 0 (准备)** | 客户带自家真实数据来 | 不是 demo 数据,是脱敏的生产数据;客户高管+业务方+IT 全到场 |
| **Day 1** | Problem framing | Palantir FDE + 客户 Echo 共同梳理 3-5 个候选 use case |
| **Day 2** | Ontology 建模 | 把客户业务对象映射到 Foundry Ontology |
| **Day 3** | AIP workflow 搭建 | LLM + tools + workflow 自动化,FDE 现场 hands-on |
| **Day 4** | 完成可跑通的 PoC | 客户高管参与验收,要求是"真的能用",不是 slide |
| **Day 5** | 投产路线图 | 输出 MVP + roadmap,商务团队跟进合同 |

Karp 在 Q4'23 earnings 的描述:
> 挑战客户拿"他们内部花再多资源/再多年也做不出来的问题",对比 10 小时的 AIP 结果。

---

## 4. 规模数据(可考证)

| 时间 | 累计 Bootcamp 场次 | 覆盖组织数 |
|---|---|---|
| 2022 年末 | 92 场 | — |
| 2023 年末 | **500+** 场 | **465+** organizations |
| 2024+ | 持续放量,具体未公开 | — |

**一年 5 倍增长**,这是 Palantir 历史上销售周期最短的产品形态。

来源:Karp 2023 Q4 earnings call

---

## 5. 商业飞轮:为什么管用

**传统企业 AI 销售**:
- 客户调研 → RFP → 多家投标 → POC(3-6 个月) → 合同 → 部署(6-12 个月) → 看到结果
- 总周期 1-2 年,客户高管早就换人,项目大概率烂尾

**AIP Bootcamp 模式**:
- 5 天 PoC = 直接看到能用的结果
- 销售周期从 12 个月压缩到 2-4 周
- 客户决策门槛大幅降低(没花大钱前已看到价值)

**Karp 公开案例**(Q4'23 earnings):
- 一个 outbound 起的 $3M 合同
- 经 bootcamp 后**同季度扩成 enterprise-wide deal**(数千万级)
- 这种"5 天定下来,当季扩单"是过去企业软件销售里不可能的

**财务效果**(可量化):
- 2023-2024 商业 ARR 翻倍
- 股价从 ~$15(2023 初)涨到 ~$80(2024 末)
- AIP 成为 PLTR 股价叙事的核心

---

## 6. 主交付角色就是 FDE

> "Palantir's AIP 5-day bootcamp where Forward Deployed [engineers] …"
> — Rohit Kelapure (Accenture), LinkedIn

Bootcamp = FDE 工作的销售化压缩版。这是 **FDE 工作产生最直接商业杠杆的场景**。

部分由生态合作伙伴(Accenture、KPMG 等)跑,但**主基调和方法论都是 FDE 模式**。

---

## 7. 给老王的启示:个人版 Bootcamp 可能性

如果你要做"老王 FDE Bootcamp",拆解如下:

| 维度 | Palantir 版 | 老王个人版(假设) |
|---|---|---|
| **周期** | 5 天 | 3-5 天 (1-2 天调研 + 2-3 天交付) |
| **客户** | 央企/政府/大型企业 | 中型民营企业、SMB、个体 |
| **平台** | Foundry + AIP | Hermes Agent + 客户已有工具 |
| **交付物** | 可跑通的 use case PoC | 可跑通的 Agent workflow + cron 任务 |
| **价格** | 数十万美金 + 后续年费 | ¥5-20万一次性 + 月度运维 |
| **复利** | 回流到 Ontology | 回流到 skill 库 |

可行性、定价、获客 — 这是 [[07-移植到个人咨询]] 要详细 workshop 的。

---

## 8. 模仿者(已开始抄)

a16z 称 FDE 为 "the hottest job in tech",2025 年 FDE 招聘增长 **800%**(a16z Joe Schmidt IV, a16z.com/services-led-growth)。

抄 Bootcamp 模式的:
- Anthropic Applied AI(私下叫 Bootcamp 不公开)
- OpenAI Solutions
- Glean
- Distyl(ex-Palantir 创立,刻意复制)
- Sierra(Bret Taylor 创业项目,有类似交付模式)

但 Barry 警告:**没有 Palantir 的 Ontology 平台底子,5 天交付出来的 PoC 没有复利,只是高级 PoC 工厂**。

---

## 参考

- palantir.com/platforms/aip/bootcamp(官方页)
- Bloomberg (2024-04-23) *Inside Palantir's AI Sales Secret Weapon: Software Boot Camp*
- Karp Q4 2023 earnings call transcript
- Ted Mabrey LinkedIn posts (AIPCon announcement)
- GTM Foundry deep dive
- a16z *Services-Led Growth* (Joe Schmidt IV)
