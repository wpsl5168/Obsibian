# Palantir FDE 深度调研

> 系列入口。Forward Deployed Engineer 模式的定义、起源、方法论、组织结构、商业飞轮、批评与移植可能性。
> 调研时间:2026-05-19。资料源:Palantir 官方 (careers/blog/IR)、Sankar/Karp 公开演讲与播客、Levels.fyi、a16z、Bloomberg、SEC 财报、Reddit/Blind 一手员工反馈。
> Schema 合规留 TODO,下次维护时补 frontmatter。

---

## 核心结论速查

1. **FDE 不是单一岗位 title,是工程家族**。核心是 FDSE(=Delta),还有 FDAIE、FD-Infra、FD-Reliability、FD-Security 等子岗。官方招聘页把工程类分三大类:Deltas(FDSE)、Echos(Deployment Strategist)、Devs(总部产品工程师)。
2. **三条不可妥协的判据**(真 FDE vs 假 FDE):
   - deployment 成本计入 R&D 而不是 COGS
   - 极端 field autonomy(Sankar 称之为 Auftragstaktik 任务式指挥)
   - VC 式风险容忍(允许低毛利甚至负毛利期换长期复利)
3. **Ontology 才是护城河,不是 FDE 本身**。FDE 是把客户痛点抽象成可复用 Ontology primitive 的"采矿工",真正的资产是中心化的知识图谱。
4. **没有传统 PM 是结构性选择**。Echo(领域专家)+ Delta(工程师)合并承担 PM 职责,绕开"PM-工程师"分工税。一个 Delta 是"多个能力服务一个客户",一个 Dev 是"一个能力服务多个客户"。
5. **AIP Bootcamp 是 FDE 的销售化压缩版**。5 天产出可投产 PoC,2023 一年从 92 场→500+ 场,直接拉动 ARR 翻倍、股价 $15→$80。
6. **财务复利证据**:86.8% 毛利率(Q1 2026)+ 139% NDR(Q4 FY25)+ $2.1B FCF(FY2025)。服务工作若按传统 COGS 算毛利不可能这么高,意味着 FDE 工作被实质资本化为 R&D。
7. **模仿者排行**:Anthropic / OpenAI / Glean / Distyl 是真 FDE;Scale AI / Hebbia / Sierra 名字像但机制证据弱;**国内大模型公司目前无公开证据存在真 FDE**,都还是 SA + 交付混合。
8. **阴暗面真实**:a16z 数据 FDE 招聘 2025 涨 800%,但 33% 客户事后承认根本不需要;burn-out 高,转岗到主流大厂被视为"半咨询";ICE/以色列军方合同持续受抗议。

---

## 文件索引

| # | 文件 | 内容 | 状态 |
|---|---|---|---|
| 00 | [[00-FDE-是什么]] | 官方定义、岗位家族(FDSE/FDAIE/…)、Echo+Delta 结构、不是 PFE 升级版 | ✅ |
| 01 | [[01-起源与方法论]] | Sankar 第 13 号员工故事、CIA 帐篷、bottom-up/outside-in、Sankar/Karp 原话引用 | ✅ |
| 02 | [[02-Ontology与产品哲学]] | 为什么 Ontology 是护城河、为什么没传统 PM、deployment-as-R&D 财务把戏 | ✅ |
| 03 | [[03-AIP-Bootcamp-五日模式]] | Ted Mabrey 发明、5 天产出 PoC、规模数据、商业飞轮机制 | ✅ |
| 04 | [[04-组织与招聘]] | Commercial vs USG 双线、14% 通过率、面试 4 轮(含 Problem Decomposition)、薪资水位 | ✅ |
| 05 | [[05-对标与模仿者]] | vs MS PFE / 咨询 / Snowflake / Anthropic / OpenAI / Glean / Distyl / 国内 SA,真假 FDE 三大判据 | ✅ |
| 06 | [[06-阴暗面与批评]] | ICE/以色列争议、员工 burn-out、客户不需要 FDE、学术批评、依赖陷阱 | ✅ |
| 07 | [[07-移植到个人咨询]] | 老王 FDE Bootcamp 产品定义、Hermes 作为 Ontology 等价物的可能性 | ⏳ 占位,待 workshop |
| 08 | [[08-市场认可与国内实操]] | 国外国内认可度、客户接受度、国内大模型厂商实操、中数睿智等"准 FDE"案例 | ✅ |

---

## 学习路径

- **快速理解(20 分钟)**:README + 00 + 03
- **方法论深读(1 小时)**:01 + 02,看 Sankar/Karp 原话和 Ontology 哲学
- **商业模式分析(45 分钟)**:03 + 04 + 06,理解 Bootcamp 飞轮与真实代价
- **判断模仿者(30 分钟)**:05,带"三大判据"扫描身边任何宣称 FDE 的公司
- **个人移植(workshop)**:07,要跟老王一起对话产出

---

## 关联阅读

- [[../../00-个人/简历/README]] — 老王 PFE 背景与 FDE 的能力交集
- [[../../10-知识库/AI Agent]] — Hermes Agent 作为个人 Ontology 等价物的潜力
- 外部:Barry (ex-Palantir) *Understanding Forward Deployed Engineering* — barry.ooo/posts/fde-culture
- 外部:Diogo Silva Santos *A Comprehensive Analysis of Palantir's FDE Model* (Medium, Apr 2026)
- 外部:PostHog *WTF is a Forward Deployed Engineer* — posthog.com/blog/forward-deployed-engineer
- 外部:a16z *Services-Led Growth* — a16z.com/services-led-growth (FDE 招聘 800% 增长数据)

---

## 调研缺口(后续可补)

- Karp 历季股东信(Q-letter)逐字原文 — 当前依赖 Fortune/Sherwood/BI 二手转述
- FDE 内部 leveling(L3/L4/L5)— Palantir 不公开,levels.fyi 只有合并 "Software Engineer"
- EU/亚太精确薪资分位 — 样本太少
- AIP Bootcamp 是否对客户收费 vs Palantir 自吸 — GTM Foundry 作者也称不公开
- FDE 流失率定量数据 — 财报不单独披露
- 国内大模型公司是否有真 FDE — 需访谈一手员工
