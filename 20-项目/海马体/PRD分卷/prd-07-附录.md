---
title: PRD 附录｜API/Schema/ADR
created: 2026-04-21
updated: 2026-04-21
type: entity
tags: [openhippo]
status: draft
sources: [20-项目/海马体/项目需求文档(PRD).md]
---

# PRD 附录｜API/Schema/ADR

> 本页是 [[../项目需求文档(PRD)|海马体PRD]] 的分卷之一：**API接口汇总 + DB Schema + ADR**
> 完整目录见 [[../项目需求文档(PRD)|PRD索引]]

---

## 附录A: API接口汇总

| 方法 | 路径 | 功能 | 里程碑 |
|------|------|------|--------|
| POST | `/v1/memories` | 写入记忆(F1) | M0 |
| POST | `/v1/memories/search` | 检索记忆(F2) | M0 |
| DELETE | `/v1/memories/{id}` | 删除记忆(F3) | M0 |
| GET | `/v1/memories/{id}` | 获取单条 | M1 |
| PUT | `/v1/memories/{id}` | 更新记忆 | M1 |
| POST | `/v1/memories/batch` | 批量写入(F1) | M1 |
| POST | `/v1/memories/forget` | 批量遗忘(F3) | M1 |
| POST | `/v1/memories/{id}/promote` | 升温(F4) | M1 |
| POST | `/v1/memories/{id}/archive` | 降温(F4) | M1 |
| GET | `/v1/memories/stats` | 统计(F4) | M1 |
| POST | `/v1/maintenance/sweep` | 温度调控(F9) | M1 |
| POST | `/v1/consolidate` | 触发整合(F5) | M3 |
| POST | `/v1/agents` | 注册Agent(F11) | M2 |
| POST | `/v1/agents/{id}/tokens` | 生成Token(F12) | M2 |
| POST | `/v1/repos` | 创建记忆库(F11) | M2 |
| POST | `/v1/repos/{id}/grant` | 授权(F12) | M2 |
| DELETE | `/v1/repos/{id}/grant/{agent_id}` | 撤销授权(F12) | M2 |
| GET | `/v1/repos/{id}/grants` | 授权列表(F12) | M2 |
| POST | `/v1/sessions` | 开始会话(F13) | M2 |
| DELETE | `/v1/sessions/{id}` | 结束会话(F13) | M2 |
| POST | `/v1/broadcast` | 广播(F15) | M2 |
| GET | `/v1/inbox` | 收件箱(F15) | M2 |
| GET | `/v1/audit/sharing` | 审计日志(F16) | M2 |
| POST | `/v1/memories/scan` | PII扫描(F17) | M3 |
| POST | `/v1/extract` | 自动提取(F18) | M3 |
| POST | `/v1/inject` | 上下文注入(F19) | M3 |
| GET | `/v1/memories/timeline` | 时间轴(F20) | M4 |
| POST | `/v1/webhooks` | 注册webhook(F21) | M4 |
| GET | `/v1/webhooks` | 列表webhook(F21) | M4 |
| DELETE | `/v1/webhooks/{id}` | 删除webhook(F21) | M4 |
| POST | `/v1/backup` | 备份(F22) | M4 |
| POST | `/v1/restore` | 恢复(F22) | M4 |
| POST | `/v1/import` | 导入(F23) | M4 |
| POST | `/v1/knowledge/index` | 索引知识库(F24) | M4 |
| POST | `/v1/knowledge/search` | 搜索知识库(F24) | M4 |
| GET | `/v1/health` | 健康检查(F25) | M0 |
| GET | `/v1/metrics` | 监控指标(F25) | M4 |
| GET | `/v1/memories/{id}/history` | 版本历史(F10) | M4 |
| POST | `/v1/memories/{id}/rollback` | 回滚(F10) | M4 |
| POST | `/v1/memories/conflicts` | 冲突列表(F10) | M4 |

---

## 附录B: 数据库Schema

```sql
-- 记忆主表
CREATE TABLE memories (
    id TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
    content TEXT NOT NULL,
    embedding BLOB,
    agent_id TEXT NOT NULL,
    repo_id TEXT NOT NULL,
    scope TEXT CHECK(scope IN ('user','agent','session','shared')) DEFAULT 'agent',
    tags TEXT DEFAULT '[]',
    metadata TEXT DEFAULT '{}',
    temperature TEXT CHECK(temperature IN ('hot','warm','cold')) DEFAULT 'warm',
    access_count INTEGER DEFAULT 0,
    ttl INTEGER DEFAULT 0,
    pinned BOOLEAN DEFAULT FALSE,
    created_at REAL DEFAULT (unixepoch('subsec')),
    updated_at REAL DEFAULT (unixepoch('subsec')),
    last_accessed REAL DEFAULT (unixepoch('subsec'))
);

-- FTS5全文索引
CREATE VIRTUAL TABLE memories_fts USING fts5(content, tags, tokenize='unicode61');

-- 向量索引
CREATE VIRTUAL TABLE memories_vec USING vec0(embedding float[768]);

-- Agent表
CREATE TABLE agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    token_hash TEXT NOT NULL,
    created_at REAL DEFAULT (unixepoch('subsec'))
);

-- Agent Token表
CREATE TABLE agent_tokens (
    id TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
    agent_id TEXT REFERENCES agents(id),
    token_hash TEXT NOT NULL,
    scopes TEXT DEFAULT '[]',
    created_at REAL DEFAULT (unixepoch('subsec')),
    revoked_at REAL
);

-- 记忆库表
CREATE TABLE repos (
    id TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
    name TEXT NOT NULL,
    owner_agent_id TEXT REFERENCES agents(id),
    visibility TEXT CHECK(visibility IN ('public','private')) DEFAULT 'private',
    created_at REAL DEFAULT (unixepoch('subsec'))
);

-- 授权表
CREATE TABLE repo_grants (
    repo_id TEXT REFERENCES repos(id),
    agent_id TEXT REFERENCES agents(id),
    permission TEXT CHECK(permission IN ('read','write','admin')),
    tags TEXT,
    PRIMARY KEY (repo_id, agent_id)
);

-- Session表
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    agent_id TEXT REFERENCES agents(id),
    created_at REAL DEFAULT (unixepoch('subsec')),
    ended_at REAL
);

-- Session记忆关联
CREATE TABLE session_memories (
    session_id TEXT REFERENCES sessions(id),
    memory_id TEXT REFERENCES memories(id),
    PRIMARY KEY (session_id, memory_id)
);

-- 收件箱（广播）
CREATE TABLE inbox (
    id TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
    agent_id TEXT REFERENCES agents(id),
    content TEXT NOT NULL,
    from_agent TEXT,
    priority TEXT CHECK(priority IN ('normal','urgent')) DEFAULT 'normal',
    read BOOLEAN DEFAULT FALSE,
    ttl INTEGER DEFAULT 0,
    created_at REAL DEFAULT (unixepoch('subsec'))
);

-- 知识库表
CREATE TABLE knowledge (
    id TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
    content TEXT NOT NULL,
    embedding BLOB,
    source_path TEXT NOT NULL,
    file_hash TEXT NOT NULL,
    metadata TEXT DEFAULT '{}',
    created_at REAL DEFAULT (unixepoch('subsec')),
    updated_at REAL DEFAULT (unixepoch('subsec'))
);

-- 整合日志
CREATE TABLE consolidation_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT,
    affected_ids TEXT,
    detail TEXT,
    created_at REAL DEFAULT (unixepoch('subsec'))
);

-- 记忆版本历史
CREATE TABLE memory_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_id TEXT REFERENCES memories(id) ON DELETE CASCADE,
    version INTEGER NOT NULL,
    content TEXT NOT NULL,
    changed_by TEXT,
    change_type TEXT CHECK(change_type IN ('manual','consolidation','auto_extract','import','rollback')),
    created_at REAL DEFAULT (unixepoch('subsec'))
);
CREATE INDEX idx_mv_memory ON memory_versions(memory_id, version);

-- Webhook表
CREATE TABLE webhooks (
    id TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
    url TEXT NOT NULL,
    events TEXT DEFAULT '[]',
    agent_filter TEXT,
    secret TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    failure_count INTEGER DEFAULT 0,
    created_at REAL DEFAULT (unixepoch('subsec'))
);

-- 共享审计日志
CREATE TABLE sharing_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL DEFAULT (unixepoch('subsec')),
    actor_agent_id TEXT,
    target_agent_id TEXT,
    repo_id TEXT,
    action TEXT,
    detail TEXT
);
CREATE INDEX idx_audit_time ON sharing_audit(timestamp);
CREATE INDEX idx_audit_agent ON sharing_audit(actor_agent_id);
```

---

#### F2: 记忆检索（Search/Recall）

**需求描述**
混合检索引擎：FTS5全文搜索 + 向量语义搜索 + 标签过滤，加权融合返回排序结果。

**解决的问题**
精确关键词搜索漏召回（语义不同但意思相近），纯向量搜索不精确（关键词完全匹配却排名低）。混合方案兼顾。

**操作步骤**
1. Agent调用 `POST /v1/memories/search`，传入query
2. 并行执行FTS5全文搜索 + 向量近邻搜索
3. 按配置权重融合两路结果（默认FTS 0.4 + Vec 0.6）
4. 应用scope/tags/agent_id过滤
5. 按融合分数排序，截取top-N返回
6. 更新命中记忆的access_count和last_accessed

**输入参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | str | ✅ | 搜索词/语句 |
| agent_id | str | ❌ | 限定Agent |
| scope | list[str] | ❌ | 限定scope |
| tags | list[str] | ❌ | 标签过滤 |
| limit | int | ❌ | 返回条数，默认10，最大100 |
| threshold | float | ❌ | 相关性阈值，默认0.5 |
| mode | enum | ❌ | hybrid/fts/vector，默认hybrid |

**输出参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| results | list | [{id, content, score, tags, scope, temperature, created_at, access_count}] |
| total_count | int | 命中总数（不受limit限制） |

**技术方案**
- FTS5：`memories_fts` 虚表，unicode61 tokenizer + jieba中文分词（可选）
- 向量：sqlite-vec `memories_vec` 虚表，768维float向量
- 融合：RRF (Reciprocal Rank Fusion) — `score = Σ 1/(k+rank_i)`，k=60
- 权限：自动过滤无权限repo的记忆

**验收标准**
1. 混合检索P@5 ≥ 0.8（人工标注测试集）
2. 1万条记忆规模下响应<100ms
3. FTS5支持中英文混合查询
4. 检索自动更新access_count和last_accessed
5. mode=fts/vector可单独使用

**验证手段**
- 准确率测试：构建50组query+标注，计算P@5
- 性能测试：插入1万条后bench search延迟
- 中文测试：纯中文/中英混合查询验证分词
- 回归测试：每次改动后跑完整测试集

---

#### F3: 记忆删除/遗忘（Delete/Forget）

**需求描述**
手动删除指定记忆，或按策略批量自动遗忘低价值记忆。支持dry_run预览和"永不遗忘"标记。

**解决的问题**
记忆只增不减导致膨胀、检索噪音增大、存储无限增长。

**操作步骤**
1. 手动删除：`DELETE /v1/memories/{id}` → 从memories表+FTS5+vec0删除
2. 批量遗忘：`POST /v1/memories/forget` → 按策略筛选候选 → dry_run预览或执行删除
3. 遗忘评分公式：`score = 0.4×recency + 0.35×relevance + 0.25×frequency`
4. score < threshold 且 pinned=false → 标记待清除
5. 执行删除前自动记录到consolidation_log

**输入参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | str | ✅(删除) | 记忆ID |
| strategy | enum | ✅(遗忘) | ttl/cold/unused/score |
| dry_run | bool | ❌ | 预览不执行，默认false |
| before | datetime | ❌ | 只处理此时间之前的记忆 |
| threshold | float | ❌ | 遗忘分数阈值，默认0.1 |

**输出参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| deleted_count | int | 实际/将删除的条数 |
| deleted_ids | list[str] | 删除的记忆ID列表 |
| skipped_pinned | int | 跳过的pinned记忆数 |

**技术方案**
- 删除：SQLite事务，同步清理memories + memories_fts + memories_vec三表
- 遗忘公式：`recency(t) = exp(-0.05×天数)`，`frequency(n) = min(n/20, 1.0)`
- 日志：每次遗忘写入consolidation_log（action=forget）

**验收标准**
1. 删除后search不再返回该条目
2. dry_run返回候选列表但不执行删除
3. pinned=true的记忆永不被自动遗忘
4. 批量遗忘1000条<5秒
5. 删除操作记录在consolidation_log中可审计

**验证手段**
- 功能测试：删除→搜索验证不存在
- dry_run测试：dry_run后再搜索，验证数据仍在
- pinned测试：pinned记忆在遗忘策略下不被删除
- 日志测试：遗忘后查consolidation_log验证记录完整

---

#### F4: 热冷分层（Temperature Management）

**需求描述**
三级温度体系：Hot(内存LRU+MD文件) → Warm(SQLite主表) → Cold(SQLite归档)。高频记忆常驻内存极速访问，低频记忆降级节省资源。

**解决的问题**
所有记忆平等对待导致：高频记忆访问慢（每次查DB），低频记忆占用热资源。

**操作步骤**
1. 新记忆写入默认Warm（SQLite主表）
2. 手动升温：`POST /v1/memories/{id}/promote` → 加载到LRU缓存+同步MEMORY.md
3. 手动降温：`POST /v1/memories/{id}/archive` → 移至归档表+压缩embedding
4. 自动调控由F11定时任务处理
5. `GET /v1/memories/stats` 查看各层统计

**输入参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | str | ✅ | 记忆ID |
| target | enum | ❌ | hot/warm（promote时），默认hot |

**输出参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | str | 记忆ID |
| temperature | str | 变更后的温度 |
| stats | dict | {hot_count, warm_count, cold_count, hot_size_bytes, total_size_bytes} |

**技术方案**
- Hot：Python LRU缓存（默认500条上限）+ MEMORY.md文件实时同步
- Warm：SQLite memories主表，FTS5+vec0索引齐全
- Cold：SQLite `memories_archive` 表，embedding压缩50%存储
- 升降温：UPDATE temperature字段 + 移动/复制数据

**验收标准**
1. Hot记忆注入延迟<5ms（内存直读）
2. Warm检索延迟<100ms
3. stats接口返回各层准确数量和大小
4. MEMORY.md与Hot缓存内容一致
5. Cold记忆被检索命中时自动升温到Warm

**验证手段**
- 延迟测试：Hot vs Warm检索延迟对比bench
- 一致性测试：升温后检查LRU缓存+MEMORY.md内容
- stats测试：写入已知数量后验证stats返回值
- 自动升温测试：搜索命中Cold记忆后验证温度变为Warm

---

#### F5: 记忆智能整合（Consolidation / Auto-Dream）

**需求描述**
定期整合记忆：聚类去重、合并矛盾、提炼摘要，类似人脑REM睡眠。分两层——规则层（零模型依赖，MVP）和模型层（可选外部API）。

**解决的问题**
记忆随时间积累大量重复/矛盾/碎片化内容，降低检索质量和存储效率。

**操作步骤**
1. 手动触发 `POST /v1/consolidate` 或定时任务自动运行（默认每天凌晨）
2. 规则层：按余弦相似度>0.85聚类 → 模板拼接合并
3. 矛盾检测：同scope同主题但情感/意图相反的记忆对，标记conflict
4. 模型层（可选）：调用外部LLM对聚类做摘要提炼
5. 生成整合报告写入consolidation_log
6. 被合并的旧记忆创建版本历史（F27）后删除

**输入参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| scope | str | ❌ | 限定整合范围 |
| agent_id | str | ❌ | 限定Agent |
| dry_run | bool | ❌ | 预览不执行 |
| use_model | bool | ❌ | 是否启用模型层，默认false |

**输出参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| merged | int | 合并的记忆组数 |
| deduplicated | int | 去重删除条数 |
| conflicts_found | int | 发现的矛盾对数 |
| report | str | 人可读的整合报告 |

**技术方案**
- 聚类：sqlite-vec批量计算余弦矩阵，>0.85归为一组
- 合并（规则层）：取最新content为主体，附加其余条目的差异信息
- 合并（模型层）：prompt = "合并以下记忆为一条摘要：{cluster}"
- 矛盾检测（规则层）：关键词对立模式匹配（喜欢/不喜欢，是/不是）
- 定时：APScheduler CronTrigger，默认 `0 3 * * *`

**验收标准**
1. 整合后有重复时记忆数量减少≥20%
2. 矛盾检测准确率≥80%（规则层）
3. 整合不丢失关键信息（人工抽检10组）
4. dry_run返回报告但不修改数据
5. 规则层零API费用可独立运行
6. 整合日志完整记录每个操作

**验证手段**
- 去重测试：插入20条近义记忆，整合后验证数量和内容
- 矛盾测试：插入"用户喜欢A"和"用户不喜欢A"，验证检测到conflict
- 幂等测试：连续运行两次整合，第二次应无变更
- 日志测试：整合后查consolidation_log验证记录完整
- 无损测试：人工抽检整合前后关键信息完整性

---

## 附录A：Hermes Agent集成架构决策记录

> 日期：2026-04-19 | 决策人：老王 | 状态：已实施

### 背景

海马体的首个dogfooding场景是替代Hermes Agent的记忆后端。Hermes内置memory系统使用MEMORY.md/USER.md（热记忆）+ state.db FTS5（冷记忆），需要将持久化冷存储切换到OpenHippo。

### 方案对比

| 维度 | 方案A：MCP Server代理 | 方案B：Hook管道（✅ 采纳） |
|------|---------------------|------------------------|
| 原理 | 改造memory MCP Server，所有memory tool调用代理到OpenHippo REST API | Gateway plugin的pre/post hook自动拦截，管道级同步 |
| 触发可靠性 | ❌ 依赖大模型"选择调用"MCP tool，不保证每次触发 | ✅ Hook是管道级拦截，每次LLM调用必触发，零遗漏 |
| 架构角色 | OpenHippo替代Hermes内置memory成为唯一系统 | Hermes内置memory=热缓存（注入system prompt），OpenHippo=持久化冷存储+语义搜索 |
| 改动范围 | 需重写memory_server.py | 仅维护plugin代码（~180行Python） |
| 符合设计理念 | ❌ Agent需要"知道"自己在存记忆 | ✅ 全自动无感知，像人脑记忆一样自动运行 |

### 决策

**采纳方案B：Hook管道**。核心原因：
1. **MCP不可靠** — 大模型并不会每次都调用MCP tool，记忆写入会有遗漏
2. **无感知是核心UX** — PRD F18明确要求"Agent不需要知道自己在存记忆"，Hook天然满足
3. **双层架构更健壮** — 热缓存（Hermes内置，token级快）+ 冷存储（OpenHippo，语义搜索），各司其职

### 实现架构

```
用户消息 → Hermes Gateway
              │
              ├─ pre_llm_call hook → OpenHippo语义搜索 → 注入相关冷记忆到context
              │
              ├─ LLM推理（system prompt含Hermes热记忆 + OpenHippo注入的冷记忆）
              │
              ├─ post_llm_call hook → 对话自动存入OpenHippo冷存储
              │
              └─ post_tool_call hook → 镜像memory操作（add/replace/remove/archive/promote）
```

### Hook覆盖矩阵

| Hermes memory操作 | Hook镜像 | OpenHippo API |
|-------------------|----------|---------------|
| add | ✅ post_tool_call | POST /v1/memories |
| replace | ✅ post_tool_call | POST /v1/memories |
| remove | ✅ post_tool_call | POST /v1/memories/remove |
| archive | ✅ post_tool_call | POST /v1/memories/archive |
| promote | ✅ post_tool_call | POST /v1/memories/promote |
| search（冷搜索）| ✅ pre_llm_call | POST /v1/memories/search |
| 对话自动提取 | ✅ post_llm_call | POST /v1/memories |

### 数据迁移

初始迁移已完成（2026-04-19）：
- Hermes cold memory（state.db memory_entries）→ OpenHippo cold_memory：14条，含embedding
- Hermes hot memory（MEMORY.md 11条 + USER.md 11条）→ OpenHippo hot_memory：22条
- 向量索引backfill完成，语义搜索可用

---

## 相关链接

- 上级索引：[[../项目需求文档(PRD)]]
- 项目主页：[[../README]]
- 知识库索引：[[../../../index]]
