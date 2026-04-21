---
title: 知识库操作日志
created: 2026-04-21
updated: 2026-04-21
type: meta
---

# 📜 知识库操作日志

> Append-only。所有wiki治理操作必须记录。
> 格式：`## [YYYY-MM-DD] action | subject`
> Actions: `init` `ingest` `update` `lint` `archive` `delete` `restructure`
> 当本文件超过500条，rotate为 `log-YYYY.md`，新建空log。

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
