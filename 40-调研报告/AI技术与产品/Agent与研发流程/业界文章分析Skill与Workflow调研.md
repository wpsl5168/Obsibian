---
title: 业界优秀文章分析 Skill 与 Workflow 调研
created: 2026-08-20
updated: 2026-08-21
type: research
tags: [research, workflow, evaluation]
status: stable
---

# 业界优秀文章分析 Skill 与 Workflow 调研

## 结论

业界没有一套可以直接拿来、同时做好“忠实理解、证据核验、反方检验、原创判断”的单篇文章分析 Skill。

成熟产品和开源项目主要解决三件事：

1. 多轮检索与多源覆盖；
2. claim 与 citation 的可追溯；
3. 大量材料的去重、聚类和综合。

它们通常不擅长审计作者的隐含前提，也不强制形成可证伪的分析者 thesis。尤其通用 Deep Research 工作流常把“全面、详细、保留所有信息”作为目标，这正是摘要堆砌的来源。

对“每日深度文章推荐”最优解不是照抄某个产品，而是组合：

- STORM 的多视角提问；
- PaperQA2 的 claim-level 反证检索；
- Elicit 的 protocol、证据摘录和 dual review；
- Anthropic Knowledge Synthesis 的去重、冲突显式化和置信度；
- ODNI 的事实/假设/判断分离、替代假设与变化指标；
- Reuters / Full Fact 的主动证伪、原始来源和中心主张双源核验；
- DeepResearch Bench 的 claim-citation 与 insight 双轨验收。

推荐落地架构：**两个隔离审稿人并行工作，主编只负责裁决和成文**。不要让同一个模型先写观点再自我审查。

## 一、业界现状：真正成熟的是 Research，不是 Critique

### Anthropic Agent Skills

本次通过 GitHub tree 实查，`anthropics/skills` 主仓库共有 20 个 `SKILL.md`，没有专门的文章批判、文献评述或 argument analysis Skill；Anthropic 也明确把该仓库定位为示例和教育用途，要求关键任务自行测试。[1]

`knowledge-work-plugins` 中有更成熟的 synthesis 工作流，但仍主要面向企业知识、用户研究和业务材料：

- `knowledge-synthesis`：去重 → 聚类 → 排序 → 依据 freshness、authority、agreement 评估置信度 → 带来源成文；冲突必须显式展示，不能静默选择一方。[2]
- `synthesize-research`：先抽 observation、quote、behavior、context，再做 thematic analysis、frequency、impact、confidence；强调“观察不等于解释”和“矛盾是信号”。[3]

可借：证据原子化、冲突保留、置信度分级、观察/解释分离。

不能照抄：它们擅长从多条材料归纳主题，不会自动检查“证据为什么能推出作者结论”。

### OpenAI / Perplexity / LangChain Deep Research

这类系统采用：澄清问题 → 写 research brief → 多轮检索 → 根据缺口继续搜索 → 汇总引用 → 生成长报告。OpenAI 官方 API 还提供结构化 inline citation 与 source metadata，并建议记录完整工具轨迹。[13]

LangChain Open Deep Research 的源码最能说明其目标：中间压缩步骤要求保留“ALL relevant information”，最终写作要求 comprehensive、long、verbose，并鼓励尽可能纳入研究信息。[8]

这对市场调研和资料汇编合理，对单篇深度分析却是反模式：

- 优化 recall，不优化论证锋利度；
- 资料越多越容易把分析者 thesis 淹没；
- 引用多只能证明可追溯，不能证明推理成立；
- 多个 researcher 往往按主题分工，不会主动互相证伪。

可借：research brief、并行检索、搜索后反思、stop rule、统一 citation ledger。

不能照抄：保存全部信息、追求篇幅、按章节平行铺陈。

## 二、最值得借的项目

### 1. STORM：多视角提问优于直接列提纲

STORM 在写作前先从相似主题发现多个 perspective，让不同视角的“作者”与基于网页资料的“专家”多轮问答，再据此形成 outline。实验中，相比普通 outline-driven RAG，专家认为其文章组织性和覆盖面更好；论文也承认 source bias transfer 和把无关事实过度关联是风险。[4]

最有价值的不是生成 Wikipedia，而是这条原则：

> 深度问题不是从文章目录里长出来的，而是从不同角色的关注差异里长出来的。

迁移到单篇文章：

- 领域专家：作者的机制在专业上成立吗？
- 实际操作者：落地时依赖哪些未说出的条件？
- 利益相关者/反方：谁承担成本，谁获得收益，谁被叙事省略？

限制：STORM 追求 breadth，容易问出很多有趣但不承重的问题。每日任务最多保留 3 个 perspective，每个只问 1 个能改变结论的问题。

### 2. PaperQA2 / ContraCrow：从“找支持”升级为“主动找冲突”

PaperQA2 把 scientific RAG 拆成可迭代工具：搜索论文、收集证据、上下文摘要与重排、沿 citation graph 补资料、生成带引文答案。它允许返回 “insufficient information”，而不是强行作答。[5]

更适合文章分析的是 ContraCrow：

1. 从目标文章抽取独立 claims；
2. 每条 claim 单独检索其他文献；
3. 把证据评为 agreement、lack of evidence、nuanced contradiction、explicit contradiction 等等级；
4. 输出 claim、证据片段、来源和推理。

其论文在特定生物学任务中报告：随机 93 篇论文平均找到 2.34 个矛盾陈述，70% 经专家验证；这不能直接外推到商业文章，但证明了“逐 claim 搜反证”可以成为独立工作流，而不是一句 prompt 里的自我反思。[5]

迁移价值最高：对文章 2～3 个承重 claim 建 evidence ledger，支持证据和反证分开检索。

限制：科学论文有 DOI、稳定全文和相对明确的 claim；商业评论的概念和时间范围更模糊，需要先做 claim normalization。

### 3. Elicit：把严谨性做成状态机，而不是提醒语

Elicit 的 Systematic Review 明确分离 protocol、gather、abstract/full-text screening、extraction、report。每个筛选判断和数据单元都能跳回支持它的原文 quote；dual review 让两名 reviewer 独立判断，再集中处理冲突，并保留 override、exclusion reason 和 agreement audit trail。[6]

最值得借的三点：

- **先定 protocol 再搜索**：先写清研究问题、纳入/排除标准和抽取字段，避免看到材料后移动球门；
- **判断绑定 quote**：不能只给 URL，每个重要结论必须能跳回原文片段；
- **独立双审**：第二 reviewer 在看不到第一份结论时工作，减少锚定。

限制：完整 systematic review 对每天一篇文章过重。应借状态机和双审，不借论文规模。

### 4. NotebookLM / Consensus：source-grounding 是底座，不是深度

NotebookLM 的核心是把回答限定在用户提供的来源中，并允许从 citation 跳回原文 quote 和上下文。[7] Consensus 则在论文库中提供单篇 Study Snapshot、多篇 synthesis、Consensus Meter 和 citation graph traversal。[14]

可借：

- 原文与外部资料分库；
- 所有解释先链接原文 span；
- 先看研究设计、样本、结果，再看作者结论；
- 沿引用图找上游依据和后续反证。

不能照抄：grounded 只代表“来自资料”，不代表“资料可靠”或“推理有效”；Consensus Meter 也可能把研究异质性压成简单多数。

## 三、编辑部与情报分析比 AI 产品更接近“深度分析”

### Reuters / Full Fact

Reuters 要求尽量交叉核验、两源优于一源、检查匿名来源的 track record、position 和 motive，并明确要求 initiative reporting 同时尝试证明和证伪；AI 生成的事实、来源和 claims 必须独立核验。[10]

Full Fact 不只检查显式证据，还检查 underlying assumption，因为事实正确也可能推出误导结论；它优先原始数据、法律文件和 primary research，中心主张通常尽量两源核验，并在发布前由另一名 researcher review。[11]

迁移：

- 对中心 claim 至少寻找一个支持源和一个独立核验/反证源；
- 把作者提供的证据与外部证据分开；
- 分析“数据是否真实”和“数据是否支持结论”两个问题；
- 最终报告必须公开信息缺口。

### ODNI ICD 203

ODNI 将严谨分析制度化：客观、独立、及时、基于所有可用来源，并以统一 analytic tradecraft standards 评审产品。[12]

最适合文章分析的要求：

- 区分 underlying information、analyst assumptions 和 judgments；
- 说明来源、数据和方法的质量；
- 对主要判断表达 uncertainty；
- 分析 plausible alternatives；
- 指出哪些 indicators 出现时会提高或降低某个解释的可能性；
- 让结论与证据和逻辑链清晰对应。

这比笼统写“局限性”更有操作性：不是说“结论可能有偏差”，而是明确“如果出现 X 证据，我会从中置信降为低置信”。

## 四、评测方法比写作模板更重要

DeepResearch Bench 把评估拆成两部分：

- RACE：comprehensiveness、depth/insight、instruction following、readability；
- FACT：effective citations 与 citation accuracy，即有多少有价值信息被可靠来源真正支持。[9]

它的实验显示，基于高质量 reference report 和任务自适应 criteria 的评审，比一句通用 judge prompt 更接近人类专家判断；但它仍偏多源长报告，不直接测 argument reconstruction fidelity。[9]

为单篇分析，应改造成六项验收：

1. **原文忠实度**：有没有把作者实际论点改成方便批评的版本；
2. **claim-source 对齐**：引用是否真的支持紧邻 claim；
3. **反证质量**：是否主动找过替代解释和冲突证据；
4. **分析增量**：核心 thesis 是否原文没有直接说过；
5. **可证伪性**：是否写出改变判断所需的新证据；
6. **反摘要约束**：摘要是否 ≤20%，全文是否围绕一个 thesis 收口。

不能只用同一个 writer 给自己打分。至少一个独立 judge 只看原文、evidence ledger 和成品，不看 writer 的思考过程。

## 五、推荐给 Hermes 的 V2 Workflow

### 角色与隔离

#### Reviewer A：Text Mapper

输入：仅原文，不给外部搜索结果。

输出：

- 文章类型、目的、受众；
- 一句话主张；
- claim → grounds → warrant → qualifier → rebuttal；
- 2～3 个承重 claim；
- 原文 span/quote；
- 作者实际说法与 steelman 分栏；
- 文章内部矛盾和未解释跳跃。

目的：先忠实理解原文，防止外部资料污染对作者的重构。

#### Reviewer B：Evidence Auditor

输入：承重 claims，不给 Reviewer A 的评价。

输出 `claim_ledger.jsonl`：

```json
{"claim_id":"C1","claim":"...","type":"fact|inference|value","source_span":"...","support":[...],"contradict":[...],"status":"supported|mixed|unsupported|unverifiable","confidence":"high|medium|low","missing":"..."}
```

要求：

- 支持和反证分开检索；
- 优先原始来源；
- 每项证据保存 exact quote；
- 找不到就写 insufficient information；
- 同源转载只算一个来源；
- 区分“来源可信”和“来源支持该 claim”。

#### 主编：Synthesis Judge

输入：原文、A 的论证图、B 的 ledger。

任务：

1. 先列事实、假设、判断；
2. 对比作者解释与至少一个 alternative hypothesis；
3. 保留 Reviewer 冲突，不强行平均；
4. 写唯一分析者 thesis；
5. 给出 confidence 和 change indicators；
6. 围绕 thesis 成文，摘要 ≤20%。

Sakana AI Scientist 的 reviewer 实现提供了一个可借鉴的裁决模式：多个 reviewer 独立输出结构化 JSON，再由 Area Chair 式 meta-review 找共识、保留问题并给 reviewer confidence。[15] 但不应照抄其简单均分；文章分析里，少数 reviewer 指出的致命证据断点不能被多数票冲淡。

### 流程状态

```text
候选发现与去重
→ 全文可访问性门禁
→ Reviewer A 与 Reviewer B 独立并行
→ 主编冲突裁决
→ claim-citation verifier
→ 独立质量 judge
→ 通过才登记 dedup 和投递
```

### Research State 与审计产物

Dify 的公开 workflow 把 `findings`、`executed_queries`、`visited_urls`、`knowledge_gaps` 等做成循环状态，每轮只把当前 search query 交给研究 Agent，再把结果写回状态。[17] 这比让模型在长上下文里“记得自己查过什么”可靠。

每次运行应落盘：

```text
runs/YYYY-MM-DD/<slug>/
  source.md                 # 原文快照
  source.sha256             # 防网页更新后证据漂移
  protocol.json             # 分析问题、文章类型、优先源、版本
  text_map.json             # claim、warrant、原文 locator
  claim_ledger.jsonl        # 支持、反证、状态、置信度
  queries.log               # 已执行 query、访问 URL、失败来源
  unresolved_gaps.json      # 未解决缺口与停止原因
  draft.md
  eval.json                 # 六项 rubric 与失败项
```

检索粒度和引用粒度要分开：检索可使用较大段落保持语境，引用时再切成更小的、带编号 locator 的 citation chunks。LlamaIndex 的 Citation Workflow 就是先取 relevant nodes，再拆成更细 citation nodes，并要求无有用证据时明确说明。[16] 这能减少“引用指向整篇文章、实际找不到支撑句”的问题，但仍需额外做 claim–quote entailment 检查。

### Source Admission Gate

外部材料进入 evidence ledger 前先检查：

- 是否能访问正文，而非只有搜索摘要；
- 原始来源还是二手转述；
- 作者/机构是否具备直接知情或专业能力；
- 发布日期与 claim 的时间范围是否匹配；
- 是否与已有来源独立，还是同源转载；
- 是否直接讨论该 claim，而非只在主题上相关；
- 是否存在撤稿、更正、利益冲突或版本更新。

未过门禁的材料可作为检索线索，不能作为承重证据。

### Stop Rule

- 原文拿不全：不做深度分析；
- 找不到 2 个承重 claims：降级为短推荐；
- 没有独立 thesis：`[SILENT]`；
- claim ledger 中核心 claim 为 unsupported/unverifiable：可以发，但标题/裁决必须直说证据不足；
- 质量 judge 任一硬门禁失败：退回一次修订，仍失败则静默。

## 六、哪些业界做法不要抄

- **不要抄“越长越深”**：LangChain 的“保留全部相关信息、尽量 comprehensive”会直接复发摘要病。[8]
- **不要抄按章节并行写作**：适合百科报告，不适合围绕一个判断收口。
- **不要把 citation count 当质量**：引用多但错配，反而制造虚假可信度。DeepResearch Bench 已把 effective citation 与 citation accuracy 分开。[9]
- **不要只让同一模型自我批评**：它往往维护自己最初的 framing；独立上下文比一句“请反思”更有效。
- **不要强制每篇都有洞见**：PaperQA2 的 insufficient information 和 Elicit 的 exclusion，比硬凑“启示”更专业。[5][6]
- **不要把共识投票当真理**：来源可能同源、样本异质、时间条件不同；冲突应解释，不应被多数票抹平。

## 七、落地建议

把当前超长 Cron prompt 拆成一个 `wp-deep-article-analysis` Skill：

- `SKILL.md`：路由、角色、状态机、输出和硬门禁；
- `references/claim-ledger-schema.md`：claim/evidence 数据结构；
- `references/rubric.md`：六项质量 rubric；
- `templates/text-map.md`：Reviewer A 模板；
- `templates/evidence-audit.jsonl`：Reviewer B 模板；
- `scripts/verify_analysis.py`：检查摘要比例、核心 claim 是否有证据、引用编号、change indicator、唯一 thesis；
- Cron 只保留发现、去重、调用 Skill、投递四件事；启用 `delegation + web + terminal`。

这比继续扩写 Cron prompt 更容易测试、复用和迭代，也符合 Anthropic 对 Skill 的定位：重复使用的多步流程应从全局说明中拆成按需加载的 Skill，并通过 eval 迭代。[1]

### 回归评测，不靠感觉改 Prompt

建立 20～50 篇固定评测集，覆盖技术实验、商业评论、政策文、思想随笔、营销软文和证据不足文章。每篇人工标注：

- 作者真实核心 claim；
- 2～3 个承重证据与关键 warrant；
- 至少一个有效反证或替代解释；
- 可接受的适用边界；
- 哪些“原创洞见”其实是自由联想；
- 是否应该静默不推。

每次修改 Skill 后跑同一评测集，记录：论证重构忠实度、claim-citation accuracy、反证召回、原创增量、摘要占比、人工偏好、单篇成本和耗时。DeepResearch Bench 的经验也表明，和高质量 reference 及任务专属 criteria 对比，比一句通用“请评分”更接近专家判断。[9]

## Sources

[1] https://github.com/anthropics/skills — Anthropic Agent Skills Repository
[2] https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/enterprise-search/skills/knowledge-synthesis/SKILL.md — Anthropic Knowledge Synthesis Skill
[3] https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/product-management/skills/synthesize-research/SKILL.md — Anthropic Research Synthesis Skill
[4] https://arxiv.org/html/2402.14207 — STORM
[5] https://arxiv.org/html/2409.13740v2 — PaperQA2
[6] https://support.elicit.com/en/articles/7927169 — Elicit Systematic Review Workflow
[7] https://blog.google/technology/ai/notebooklm-new-features-availability — Google NotebookLM Source Grounding
[8] https://raw.githubusercontent.com/langchain-ai/open_deep_research/main/src/open_deep_research/prompts.py — LangChain Open Deep Research Prompts
[9] https://deepresearch-bench.github.io — DeepResearch Bench
[10] https://reutersagency.com/about/standards-values — Reuters Journalistic Standards
[11] https://fullfact.org/how-we-fact-check — Full Fact Methodology
[12] https://archive.dni.gov/index.php/how-we-work/objectivity — ODNI Analytic Standards Overview
[13] https://developers.openai.com/api/docs/guides/deep-research — OpenAI Deep Research API Guide
[14] https://consensus.app/home/blog/how-consensus-works — Consensus How It Works
[15] https://raw.githubusercontent.com/SakanaAI/AI-Scientist/main/ai_scientist/perform_review.py — Sakana AI Scientist Reviewer
[16] https://docs.llamaindex.ai/en/stable/examples/workflow/citation_query_engine — LlamaIndex Citation Query Workflow
[17] https://dify.ai/blog/deep-research-workflow-in-dify-a-step-by-step-guide — Dify Deep Research Workflow
