---
title: F5 Dream（记忆整合）设计 v0.1
created: 2026-04-15
updated: 2026-09-09
type: entity
tags: [openhippo, memory, architecture]
status: draft
oversized_ok: true
---

# F5 Dream（记忆整合）设计 — v0.1 草案

> 作者：小虾  
> 日期：2026-04-20  
> 状态：**待老王 review**（先设计后编码红线）

---

## 一、为什么 Dream 是核心差异化

PRD F5 标 P0，但市面上的记忆系统（Mem0/Letta/Zep）几乎都没真正做这件事——它们停在"存"和"检索"，而 Dream 是**整理 + 遗忘**。这是[[20-项目/海马体/需求/项目需求文档(PRD).md|海马体]]相对它们的护城河，也是和老王世界观最契合的一块：

> "全自动无感知运行（像人脑记忆），工作 Agent 只管热记忆，热转冷时通过管道输送给记忆 Agent 做归档整理遗忘。"

Dream 不是一个 API，是一个**后台进程**。

---

## 二、设计目标 vs 非目标

### 目标（v0.4 MVP）
- ✅ **后台异步触发**，对工作 Agent 无感知（不阻塞写）
- ✅ **去重整合**：把 cold 里语义近似的记忆合并成一条，保留 provenance
- ✅ **遗忘衰减**：低访问、低重要度、过期的记忆被边缘化（不必硬删）
- ✅ **可审查**：每次 Dream 产出报告，老王可以看哪些记忆被合并/降权
- ✅ **可关闭**：不信任时一键关掉，hot/cold 仍正常工作

### 非目标（v0.4 不做）
- ❌ LLM 重写记忆内容（会改变语义，先不碰；v0.5 再考虑）
- ❌ 跨 agent 的记忆共识（多租户落地后再说）
- ❌ 实时整合（Dream 必须**离线**，不进写入热路径）

---

## 三、核心机制：四阶段 Dream Cycle

借鉴神经科学的睡眠分期，Dream 也分四个阶段，依次执行：

### Stage 1: **Recall**（召回扫描）
- 扫描 cold_memory，按 target 分组
- 输出：候选记忆集（默认最近 7 天 OR 从未被 Dream 过的全量）
- 实现：SQL 查询，纯读，不动数据
- 性能：100k 条 < 1s

### Stage 2: **Cluster**（聚类）
- 对候选集做**语义聚类**：复用现有 vec0 表，每条记忆找 top-K 相似邻居
- 阈值：L2 distance < 0.6（比写入去重的 0.4 宽，因为 Dream 是宽松整合）
- 输出：簇列表 `[(seed_id, [member_ids], avg_distance), ...]`
- 算法：贪心连接（避免做完整聚类的复杂度）

### Stage 3: **Consolidate**（整合）
对每个簇执行：
- **保留种子**：选 importance 最高 OR 创建最早的为代表
- **合并 metadata**：成员的访问次数、最后访问时间、tags 累加到种子
- **建立 alias 关系**：成员标记为 `consolidated_into=<seed_id>`，**不删除原记录**（可审查、可回滚）
- **重算 importance**：种子的 importance += sum(成员 importance) * 0.3（衰减加权）
- **provenance**：种子记录 `merged_from=[id1, id2, ...]`

### Stage 4: **Forget**（遗忘衰减）
不做硬删除，做**软衰减**：
- 计算每条 cold 记忆的 `decay_score`：
  ```
  decay_score = age_days / 30 - access_count * 0.5 - importance * 2
  ```
- decay_score > THRESHOLD 的记忆：标记 `archived_at=now, status='dormant'`
- dormant 记忆**不参与默认搜索**（除非 `include_dormant=true`）
- 不动 vec 表（保留以便老王回头查）

---

## 四、Schema 改动（migration 006-008）

### Migration 006: dream_runs 表
```sql
CREATE TABLE dream_runs (
    id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL,  -- 'running' / 'completed' / 'failed'
    candidates_count INTEGER,
    clusters_count INTEGER,
    consolidated_count INTEGER,
    forgotten_count INTEGER,
    config_snapshot TEXT,   -- JSON: 当时的阈值
    error TEXT
);
```

### Migration 007: cold_memory 加 Dream 相关列
```sql
ALTER TABLE cold_memory ADD COLUMN consolidated_into TEXT;  -- 指向种子 id
ALTER TABLE cold_memory ADD COLUMN merged_from TEXT;         -- JSON array
ALTER TABLE cold_memory ADD COLUMN access_count INTEGER DEFAULT 0;
ALTER TABLE cold_memory ADD COLUMN last_accessed_at TEXT;
ALTER TABLE cold_memory ADD COLUMN importance REAL DEFAULT 0.5;  -- 0~1
ALTER TABLE cold_memory ADD COLUMN dream_status TEXT DEFAULT 'active';  
-- 'active' | 'dormant' | 'consolidated'
ALTER TABLE cold_memory ADD COLUMN last_dream_at TEXT;

CREATE INDEX idx_cold_dream_status ON cold_memory(dream_status, last_dream_at);
CREATE INDEX idx_cold_consolidated ON cold_memory(consolidated_into);
```

### Migration 008: dream_actions 审计表
```sql
CREATE TABLE dream_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dream_run_id TEXT NOT NULL,
    action TEXT NOT NULL,  -- 'consolidate' / 'forget' / 'restore'
    memory_id TEXT NOT NULL,
    details TEXT,  -- JSON
    created_at TEXT NOT NULL,
    FOREIGN KEY (dream_run_id) REFERENCES dream_runs(id)
);
```

---

## 五、触发机制

### 三种触发方式（默认开 #2）

1. **手动**：`POST /v1/dream/run` — 立即执行一次（同步返回 dream_run_id）
2. **自动**（默认）：每 6 小时一次，由后台 `asyncio.create_task` 在 lifespan 启动
3. **事件驱动**：cold_memory 累计新增 ≥ 100 条时触发一次

配置：
```yaml
dream:
  enabled: true
  auto_interval_hours: 6
  consolidate_threshold: 0.6  # L2 distance
  forget_threshold: 1.0       # decay_score
  min_age_days: 1             # 新记忆不参与
```

---

## 六、API 设计

| Endpoint | 方法 | 用途 |
|---|---|---|
| `POST /v1/dream/run` | POST | 手动触发一次 dream（异步，立返 run_id） |
| `GET /v1/dream/runs` | GET | 列出历史 dream runs（分页） |
| `GET /v1/dream/runs/{id}` | GET | 单个 run 详情 + actions 列表 |
| `POST /v1/dream/restore/{memory_id}` | POST | 把 dormant/consolidated 的记忆恢复成 active |
| `GET /v1/dream/preview` | GET | 干跑：返回如果现在 dream 会动哪些记忆，**不实际执行** |

`/dream/preview` 是关键 —— 老王要求"用户可通过海马体审查所有历史记忆"，先看再做。

---

## 七、风险与权衡

| 风险 | 缓解 |
|---|---|
| 误整合：把不该合并的记忆合一起 | (1) 阈值保守 0.6 (2) 不删原记录，可 restore (3) preview 干跑 |
| 性能爆炸：cold 增长后每次 dream 全扫 | 增量：只扫 `last_dream_at IS NULL OR < (now-1d)` |
| 后台任务挂了无感知 | dream_runs 表 status='failed' + health 暴露 last_dream_status |
| 老王不信任自动遗忘 | 默认 `forget_threshold` 高，几乎只整合不遗忘；保留手动开关 |

---

## 八、MVP 拆分（建议 3 个 PR）

### PR-1: Schema + 干跑（无副作用）
- migration 006/007/008
- `dream/preview` API
- 单元测试：聚类正确性、decay_score 计算
- **目标：能看，不能改**

### PR-2: Consolidate（整合）
- Stage 1+2+3 完整实现
- `/dream/run` API
- 测试：合并后 search 仍能找到原内容（通过种子）
- **目标：能合，不能忘**

### PR-3: Forget + 自动调度
- Stage 4 + lifespan 后台任务
- `/dream/restore` 回滚 API
- 测试：dormant 记忆默认不出现，include_dormant=true 时出现
- **目标：完整闭环**

每个 PR 独立可发布、独立可回滚。

---

## 九、与老王世界观的对照检查

| 老王观点 | 设计是否对齐 |
|---|---|
| "记忆 Agent 全自动无感知" | ✅ 后台 task，工作 Agent 看不见 |
| "热转冷时通过管道输送" | ✅ Dream 处理的是已经冷下来的记忆 |
| "用户可审查所有历史记忆" | ✅ preview + dream_actions 表 + restore API |
| "记忆透明度零容忍" | ✅ 不删除，只标 dormant；所有动作可追溯 |
| "对标 Mem0 走隐私+轻量路线" | ✅ 纯本地 SQL，无 LLM 重写，无外发 |

---

## 十、给老王的决策点

请明确回答以下 5 点，我按你的拍板再写代码：

1. **MVP 范围**：按 PR-1/2/3 拆三步走，还是一次到位？
2. **遗忘默认行为**：v0.4 MVP **默认开** forget 还是只做 consolidate？（我倾向后者，老王语义更保守）
3. **整合阈值**：L2=0.6 偏宽，要不要紧到 0.5？
4. **自动间隔**：6h 还是 24h？（cron 资源 vs 整合及时性）
5. **审计粒度**：dream_actions 每条记一行 OK，还是希望更详细的 diff 快照？

---

> 上面写完才动手编码。等老王回复后再开 PR-1。
