---
title: Wiki Schema
created: 2026-04-21
updated: 2026-04-21
type: meta
---

# 知识库 Schema（治理宪法）

> 本Schema约束 `10-知识库/`、`20-项目/`、`30-调研报告/` 三个目录下的所有页面。
> 其他目录（00-收件箱、40-日报、90-治理）保持自由，不受本Schema约束。
> 受 [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 启发。

---

## 1. 域定义

**Wiki范围**（受治理）：
- `10-知识库/` — 概念页（concepts），AI/Agent/工程领域的稳定知识
- `20-项目/` — 实体页（entities），每个项目一组主索引+子页
- `30-调研报告/` — 调研/对比/综合分析（research/comparison）

**Wiki外**（自由区）：
- `00-收件箱/` — 草稿、待整理（不索引、不lint）
- `40-日报与动态/` — 时序记录（不索引、不lint）
- `90-治理/` — 元数据（迁移记录、周报）

---

## 2. 文件命名规范

- 中文/英文均可，避免空格（用连字符或下划线）
- 同一系列页用 `<编号>-<主题>.md`（例：`4.1-AI_Agent核心心智模型.md`）
- README.md 作为目录入口，必须存在并保持最新

---

## 3. Frontmatter 规范（强制）

每个wiki页面**必须**有YAML frontmatter：

```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept | entity | research | comparison | methodology | meta
tags: [taxonomy中的标签]
status: draft | stable | archived
sources: [可选，源材料路径或URL]
---
```

**字段说明**：
- `type` 必须是上述6种之一
- `tags` 至少1个，必须来自下文Tag Taxonomy
- `status`：`draft`(草稿)、`stable`(已成稿)、`archived`(归档)
- 修改页面时**必须**bump `updated` 日期

---

## 4. Tag Taxonomy（强约束，新tag必须先在此注册）

### 领域核心 (domain)
- `#agent` — AI Agent架构、心智模型、设计模式
- `#llm` — 大模型基础原理、架构演进
- `#memory` — 记忆系统、上下文管理、向量检索
- `#prompt` — 提示词工程、角色设定、输出控制
- `#tooling` — Function Calling、MCP、工具调用
- `#workflow` — 编排、流程图、HITL交接
- `#multimodal` — 多模态能力
- `#evaluation` — 评测、Evals、可观测性
- `#security` — 安全护栏、防注入

### 工程实践 (practice)
- `#vibe-coding` — Claude Code、Codex等终端Agent实战
- `#methodology` — 经典方法论（ReAct/CoT/Reflexion等）
- `#architecture` — 系统架构设计、架构对比
- `#research` — 调研报告、综述
- `#comparison` — 横向对比

### 项目维度 (project)
- `#brickhub` — BrickHub项目相关
- `#hermes` — Hermes Agent相关
- `#openhippo` — 海马体项目相关

### 状态维度 (lifecycle)
- `#draft` — 草稿（与frontmatter status=draft同义，可选）
- `#legacy` — 旧笔记归档区

> **新tag流程**：先PR到本Schema，再使用。禁止野生tag。

---

## 5. 页面阈值规则

| 场景 | 决策 |
|---|---|
| 一个实体/概念在2+源材料中出现，或在1个源中是核心 | **创建专页** |
| 已有页面提到的内容 | **更新已有页**，不要重建 |
| 仅一处提及的次要细节 | **不创建**，写在已有页的"相关"小节 |
| 页面超过200行 | **拆页**，按章节分子页，主页保留索引 |
| 内容已被新页面完全替代 | **归档**，移到 `_archive/`，更新index |

---

## 6. 链接规范

- 每个wiki页面**至少2个出站 `[[wikilinks]]`**（孤儿页是债务）
- 项目专页（`20-项目/<X>/`）必须有1个README作为枢纽，链向该项目所有子页
- 跨目录链接用相对路径：`[[../../10-知识库/AI模型与Agent/4.3-记忆机制设计]]`

---

## 7. 矛盾处理

- 新源与已有内容冲突时：**不要静默覆盖**
- 在页面顶部添加 `> ⚠️ Note: 本页与 [[other-page]] 在 X 点存在分歧（YYYY-MM-DD）`
- frontmatter加 `contradictions: [page-name]`
- 在下次lint报告中由人工裁决

---

## 8. 维护操作（由Agent执行）

| 操作 | 触发 | 必做 |
|---|---|---|
| **ingest** | 用户提供源材料 | 创建/更新页 + 加wikilinks + 更新index + 写log |
| **update** | 修改已有页 | bump updated日期 + 写log |
| **lint** | 周期性（建议每周） | 检查孤儿/坏链/缺frontmatter/超长页/野生tag → 报告 |
| **archive** | 内容过时 | 移到_archive/ + 更新index + 写log |

---

## 9. 索引与日志

- `index.md` — 所有wiki页的分类索引，每页一行摘要。**新增/重命名/归档页必须同步更新**
- `log.md` — 所有wiki操作的append-only日志。**每次ingest/update/lint/archive必须写入**
- 当 `log.md` 超过500条，rotate为 `log-YYYY.md`

---

## 10. 与Skill的协同

本Schema是以下skill的强约束：
- `kb-maintenance` — 周期审计必须按本Schema检查
- `research-to-kb` — 新调研报告入库必须遵守frontmatter+tag+index更新
- `dreaming` — Auto Dream生成的内容必须符合本Schema

如果skill与本Schema冲突，**以本Schema为准**，并提交skill的修订PR。
