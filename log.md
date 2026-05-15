---
title: 知识库操作日志
created: 2026-04-21
updated: 2026-04-22
type: meta
---

# 📜 知识库操作日志

> Append-only。所有wiki治理操作必须记录。
> 格式：`## [YYYY-MM-DD] action | subject`
> Actions: `init` `ingest` `update` `lint` `archive` `delete` `restructure`
> 当本文件超过500条，rotate为 `log-YYYY.md`，新建空log。

---

## [2026-05-05] weekly maintenance | Automated by cron — COMPLETE

**审计结果**: CRITICAL:0, WARN:10 → 0, INFO:53 → 49 ✅ **全绿达成**

**修复动作**:
- 房产调研文件缺字段：补齐 created/updated/type 字段，野生tag归并为规范tag  
- 孤儿页面收编：AI风口调研 → 项目/Hermes分类，英语学习方案 → 新增家庭教育分类
- index.md同步更新：新增"👪家庭教育"分类，收编2个孤儿页面
- 审计脚本更新：补齐缺失的 family/realestate 标签到 VALID_TAGS

**治理效果**: 
- ✅ 10个WARN问题全部修复
- ✅ 2个孤儿页面成功入库  
- ✅ 7个野生标签全部规范化
- ✅ 知识库达到全绿状态 (仅49个INFO级超长页提醒)
- ✅ 143个页面，100% frontmatter覆盖

**下周重点**: 内容质量提升 — 重点检查🔴标记的空洞文件

---

## [2026-04-29] weekly maintenance | Automated by cron

**审计结果**: CRITICAL:0 → 0, WARN:4 → 0, INFO:63 → 40

**问题修复**:
- 🔧 **野生标签清理**: 修复 `30-调研报告/2026高考志愿全行业评估.md` 的4个野生标签 (`#高考`, `#志愿填报`, `#行业分析`, `#张雪峰视角`) → 规范化为 `[research]`
- 📄 **索引更新**: 在 `index.md` 补充14个缺失条目:
  - Pi-Rover项目: 12个架构模式+硬件+软件栈文档
  - Dreaming项目: 1个研究报告
  - 调研报告: 1个高考志愿评估报告
- ✅ **全绿状态**: WARN级问题从4个清零，CRITICAL级问题保持0

**剩余事项**: 40个INFO级超长页（>200行），建议考虑添加 `oversized_ok: true` 豁免标记，因为多数为技术深度文档和调研报告，拆分会影响阅读体验。

---

## [2026-04-21] init | 知识库治理体系建立

按 Karpathy LLM Wiki 模式为 obsidian-vault 建立治理骨架：

**新增文件**：
- `SCHEMA.md` — 治理宪法，定义tag taxonomy、frontmatter规范、页面阈值规则
- `index.md` — 75页全分类索引，每页一句话摘要
- `log.md` — 本文件，操作日志

**治理范围**：
- ✅ 受Schema约束：`10-知识库/`、`20-项目/`、`30-调研报告/`
- ⏭️ 自由区：`00-收件箱/`、`40-日报与动态/`、`90-治理/`

**当前健康度**：
- 总页数：75
- Frontmatter覆盖：62/75 (82%)
- 超长页(>200行)：16个，其中海马体PRD达2085行（待拆）
- Tag体系：基本空白，需要按SCHEMA重新打tag

**下一步（第2波待执行）**：
1. 拆分海马体PRD（2085行 → 5-8个子页）
2. 给13个无frontmatter页面补元数据
3. 建立第一批跨页 `[[wikilinks]]`

**第3波**：升级 kb-maintenance / research-to-kb / dreaming skill 强制走Schema。

---

## [2026-04-21] restructure | 第2波：拆PRD + 补frontmatter + 注入wikilinks

### 拆分海马体PRD（2085行 → 13个分卷）
原 `20-项目/海马体/项目需求文档(PRD).md` 改写为索引页（46行）。
新建 `20-项目/海马体/PRD分卷/` 目录，13个分卷文件：
- prd-01-目的与痛点 (23行)
- prd-02-用户与开源形态 (31行)
- prd-03-部署形式 (19行)
- prd-04-1-核心记忆操作 (67行) — F1
- prd-04-2-协议与接入 (136行) — F6-F8
- prd-04-3-生命周期管理 (104行) — F9-F10
- prd-04-4-隔离与共享 (303行) — F11-F16 🔴
- prd-04-5-安全与智能 (240行) — F17-F20 🔴
- prd-04-6-运维与集成 (310行) — F21-F25 🔴
- prd-04-7-Dogfood迁移 (110行) — F26-F27
- prd-05-操作流程与架构 (93行)
- prd-06-环境与里程碑 (163行)
- prd-07-附录 (474行) 🔴

### 补frontmatter（9个无元数据页面）
- 20-项目/Hermes/memory-system-upgrade.md
- 20-项目/海马体/{开发进度,访问凭证,架构审查v0.2,审查日志-v0.3-2026-04-20,竞品调研与商业计划书,F5-Dream设计-v0.1}.md
- 30-调研报告/{AI-Agent-Memory架构借鉴分析,Hermes上下文管理优化方案}.md

### 注入跨页wikilinks（6处保守注入）
- 调研↔项目互链：AI-Agent-Memory架构借鉴分析、Hermes上下文管理优化方案、竞品调研、F5-Dream设计、开发进度、架构审查v0.2

### 健康度变化
| 指标 | 第1波后 | 第2波后 |
|---|---|---|
| 总页数 | 75 | **88** (+13 PRD分卷) |
| Frontmatter覆盖 | 82% | **100%** ✅ |
| 超长页(>200行) | 16 | 待重新审计 |

### 重写 index.md
反映新的88页结构与100% FM覆盖。

---

## [2026-04-21] tool-release | wiki_lint.py 上线 | 治理体系第3波完成
- 新工具：`~/.hermes/skills/note-taking/kb-maintenance/scripts/wiki_lint.py`（~330行Python，零依赖）
- 检查项：frontmatter完整性 / tag taxonomy合规 / 坏链 / 孤儿页 / 超长页 / stale / index对账
- 退出码：0=clean / 1=warnings / 2=errors（可串CI/cron）
- Skill升级：kb-maintenance + research-to-kb 均已注入Schema约束段落
  - kb-maintenance：审计流程改为一键跑lint，标签体系更新为17-tag taxonomy
  - research-to-kb：入库子Agent context 强制要求frontmatter规范+更新index+追加log+lint自检
- 首跑基线：88页 / 100% frontmatter覆盖 / 0 CRITICAL / 463 WARN（66坏链、205野生tag、183缺字段、其余孤儿页/超长页）
- 这些 WARN 是真实存量债务，留待后续按主题分批清理

## [2026-04-21] mass-cleanup | 第4波债务清理 | 451 WARN已修复
**工具**: 新增 `~/.hermes/skills/note-taking/kb-maintenance/scripts/wiki_fix.py`
**模式**: dry-run → apply → re-lint → 幂等验证

### 治理数据 BEFORE → AFTER
| 指标 | BEFORE | AFTER | Δ |
|---|---|---|---|
| CRITICAL | 0 | 0 | — |
| WARN     | 463 | **7** | -451 (-97.4%) |
| 坏链      | 66  | **0** | 全清 |
| 野生tag   | 205 | **0** | 全清 |
| 缺字段    | 183 | **0** | 全清 |
| 非法status | 2  | **0** | 全清 |
| 超长页    | 7   | 7  | 留待拆文波 |

### 4A 坏链修复（66处）
- 13× [[SQL Server]] → 删除（旧笔记目标已不在治理区）
- 7× [[Model_Context_Protocol 规范解析]] → [[3.2-Model_Context_Protocol规范解析]]
- 7× [[AI_Agent 核心心智模型]] → [[4.1-AI_Agent核心心智模型]]
- 7× [[工作流编排模式]] → [[4.2-工作流编排模式]]
- 4× [[1.1-LLM基础与模型选型]] → [[1.1-大模型演进与主流架构体系]]
- 其余按映射表批量替换

### 4B 标签归一（205处 → 17-tag taxonomy）
- 大小写归一: #AI/#LLM → #llm | #BrickHub → #brickhub | #Agent → #agent
- 分类归并: #Cursor/#Copilot/#Devin/#OpenHands/#GeminiCLI/#Windsurf → #vibe-coding
- 厂商映射: #OpenAI/#Google/#Meta/#xAI/#DeepSeek/#Qwen/#Kimi → #llm
- 语义归并: #MemGPT/#长期记忆/#向量数据库 → #memory | #ReAct/#TDD → #methodology
- 章节中文tag: #基础架构与模型底座 等 → 删除（章节本身就是目录）
- 杂项: #daily/#qa/#dreaming/#sql/#database → 删除
- Schema扩展: 新增 #meta（README/index/说明文档专用）

### 4C frontmatter补字段（62文件 / 183字段）
- created: 62处（git log --diff-filter=A 取首次提交日期）
- updated: 58处（git log -1 取最近提交日期）
- type:    62处（按目录推断: 10-/AI模型→concept, 30-/→research, 20-/→entity）
- status:  60处（30-调研→stable, 其余→draft）
- tags:    1处

### 验证闭环
- ✅ wiki_fix.py 幂等性测试通过（第二次执行0变更）
- ✅ wiki_lint.py 复跑确认 451 WARN 已清
- ✅ 抽查 1.1-大模型演进 / Memory架构借鉴分析 frontmatter 符合规范

### 留待清理
- 7处 oversized 长文需拆分（独立的"拆长文波"，工作量大）
- 55处 orphan + 17处 not_in_index 是 INFO 级，不影响主体质量


## 2026-04-21 第5波：拆长文 + lint修缺陷 + 索引补全

**拆长文（7个超长页）**
- 3.2-MCP规范解析 (520→376) → 拆出 3.2.1 / 3.2.2
- 4.2-工作流编排模式 (551→367) → 拆出 4.2.1 / 4.2.2
- 6.3-SWE-Agent (484→272) → 拆出 6.3.1 生产化与CICD
- DL.AI学习路径 (641→114) → 拆出 按主题索引 / 全量目录
- prd-07-附录 (500→43) → 拆出 附录A/B/C
- 测试方案与用例 (433→144) → 拆出 D1-D5 / D6-D8 / 报告与缺陷追踪
- 2.3-结构化输出 (425→133) → 拆出 厂商对比 / 工程实战
- 共生成 **15 个子页**，每页带回链 + 父页留 stub

**lint工具修复2个隐性bug**
- 修 `Path("2.3.1-x").stem == "2.3"` 误判 → 加 `link_stem()` 工具函数（误报97%孤儿页）
- 入链来源补全：根级 `index.md/log.md/README.md` 也算入链来源

**lint增强**
- 加 `oversized_ok: true` frontmatter豁免（用于Schema/参考文档结构性长文）

**索引/孤儿补全**
- index.md 新增"📑 拆分子页索引"块（15子页）
- 创建 20-项目/Hermes/README.md，挂入 memory-system-upgrade

**最终状态**
- CRITICAL=0, WARN=0, INFO=29 (均为 200-400 行"略长但合理"档)
- vault总页数：88 → 103
- 100% frontmatter / 100% tag合规 / 0坏链 / 0孤儿


## 2026-04-21 调研产出
- 30-调研报告/AI-Agent个人盈利赛道扫描-2026Q2.md (新增)
- 9个赛道完整评分 + 三层组合策略

## [2026-04-22] research-ingest | McKinsey-2026-AI报告与5岁AI启蒙 | 整合 McKinsey 2026 三份核心报告（State of Organizations/State of AI/MGI Agents-Robots-Us）+ 儿童AI教育研究，输出AI现状+5岁娃三层启蒙路径+12月节奏，~12KB。

## [2026-04-22] weekly-maintenance | 知识库维护 | 修复4个CRITICAL问题（缺frontmatter）+ 1个WARN（invalid type）+ 6个新文档加入index.md。丰富AI知识库内容：大模型演进补充Claude 4.5/GPT-5/Gemini 3.0，MCP更新2026生态数据，终端IDE新增Continue/Claude Code，Agent架构/评测基准/推理策略补充最新进展。621行新增，107行删除。

## [2026-04-23] lint-fix | 拆长文+加豁免 | 处理wiki_lint 5个oversized WARN：海马体两文档加 oversized_ok: true 豁免（架构方案-v0.4 437行 / F5-软删除-v0.3 424行，结构性长文不拆）；三篇知识库综述按H2拆分：2.2-高阶推理策略 534→329行（剥离§10-13到 2.2.1-推理模型工程化进阶 237行）、3.2-MCP规范 424→173行（剥离协议架构+传输层到 3.2.3-MCP协议架构与传输层 274行）、4.1-Agent心智模型 453→253行（剥离2026新进展+主流框架到 4.1.1-Agent认知架构与主流框架2026 232行）。同步更新index.md添加3个新子页索引。WARN结构性oversized 5→0。

## [2026-05-05] research-ingest | 怡海花园真实成交价调研 | 房天下网签数据，3 个分园近期成交单价区间 3.5~4.6 万/㎡，链家参考价偏高 10~20%。放 00-收件箱/。

## [2026-05-05] schema-update | 新增 #realestate / #family tags + 30-调研报告/房产/ 子分类，迁入怡海花园调研。
