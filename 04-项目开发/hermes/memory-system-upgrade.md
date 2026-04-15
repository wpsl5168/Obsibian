# Hermes Memory System Upgrade

> Created: 2026-04-15
> Status: In Progress
> Tags: #hermes #architecture #memory #vector-search

## 背景

Hermes记忆系统存在三个核心问题：
1. **Gateway重启丢对话** — 重启无clean_shutdown标记→session被标记suspended→下次消息auto-reset
2. **session_search超时** — 每次搜索实时调LLM生成摘要（3-5个并发调用，60s超时，35次timeout记录）
3. **Hot memory容量小** — memory 2200 chars / user 1375 chars，远低于Claude Code的25KB/200行

## 目标架构

对标Claude Code四层记忆模型，结合Hermes现有基础设施升级：

```
┌─────────────────────────────────────────────────┐
│              System Prompt (每轮注入)              │
│  ┌─────────────┐  ┌───────────────────────────┐  │
│  │ MEMORY.md   │  │ USER.md                   │  │
│  │ 6000 chars  │  │ 3000 chars                │  │
│  │ (hot memory)│  │ (user profile)            │  │
│  └─────────────┘  └───────────────────────────┘  │
└─────────────────────────────────────────────────┘
         ↕ archive/promote                    
┌─────────────────────────────────────────────────┐
│           Cold Memory (SQLite FTS5)              │
│  memory_entries table + FTS5 full-text search    │
│  unlimited capacity, keyword search              │
└─────────────────────────────────────────────────┘
         ↕ embedding                          
┌─────────────────────────────────────────────────┐
│         Vector Store (sqlite-vec)                │
│  embeddings table + vec0 virtual table           │
│  session summaries + memory entries              │
│  语义搜索 via cosine similarity                    │
└─────────────────────────────────────────────────┘
         ↕ auto-trigger                       
┌─────────────────────────────────────────────────┐
│           Auto Dream (定期整理)                    │
│  触发: 24h + 5 sessions 双门控                     │
│  合并重复、删矛盾、归档低频、日期规范化               │
└─────────────────────────────────────────────────┘
```

## 技术选型

### 向量数据库: sqlite-vec
- **选择理由**: 163KB安装，零依赖，直接在现有state.db内建virtual table
- **替代方案评估**: ChromaDB(500MB+依赖地狱)、Qdrant(100MB+)、LanceDB(300MB+ pyarrow)、纯numpy(性能够但无SQL集成)
- **性能**: 1K向量查询<1ms（brute-force），我们的规模完全够用
- **风险**: pre-v1(0.1.7)，但只用insert/search两个基本操作

### Embedding模型: OpenRouter text-embedding-3-small
- **成本**: $0.02/1M tokens，几百个session约几分钱
- **维度**: 1536
- **调用方式**: 通过已有的OPENROUTER_API_KEY，httpx直连

### 行业对比
| Agent | 记忆整理机制 | 向量检索 |
|-------|------------|---------|
| Claude Code | Auto Dream (24h+5sessions) | 无(grep) |
| Cursor | 无(社区Memory Bank) | 无 |
| Windsurf | 自动生成，无整理 | 无 |
| Cline | Context Handoff(反应式) | 无 |
| Aider | Session内递归摘要 | 无 |
| **Hermes(升级后)** | **Auto Dream + 向量辅助** | **sqlite-vec** |

## 实施计划

### P0: 修Gateway重启Session丢失 (30min)
- **改动**: `gateway/run.py:2340-2360`
- **方案**: graceful shutdown一律写.clean_shutdown，不管drain是否超时
- **验证**: 重启gateway后发消息，应继续现有session

### P1a: Embedding基础设施 (2h)
- 安装sqlite-vec (`pip install sqlite-vec`)
- state.db新增embeddings表 + embeddings_vec虚拟表
- 创建`agent/embedding_client.py` — OpenRouter embedding API封装
- SessionDB新增store_embedding/search_embeddings/delete_embeddings方法

### P1b: Session Search向量化 (2h)
- auto_summary后自动embedding session摘要
- 一次性backfill历史session摘要
- session_search新流程: query→embedding→KNN→返回预生成summary（不调LLM）
- FTS5作为fallback

### P1c: Memory向量化 (1h)
- memory add/replace/remove时自动维护embedding
- cold memory search加向量路径
- 与FTS5结果合并去重

### P1d: 扩容Hot Memory (10min)
- memory: 2200→6000 chars
- user: 1375→3000 chars
- 总9000 chars ≈ 2500 tokens

### P2-prep: Auto Dream地基 (30min)
- state.db新增system_meta表（key-value）
- session结束时递增sessions_since_dream计数
- dream_trigger.py: 24h+5sessions双门控检查

## 备份

| 备份项 | 路径 | 时间 |
|--------|------|------|
| 项目tar | ~/.hermes/hermes-agent-backup-20260415_094022.tar.gz | 2026-04-15 |
| Git tag | pre-memory-upgrade-20260415_094022 | 2026-04-15 |
| Memory文件 | ~/.hermes/memories_backup_20260415_094022/ | 2026-04-15 |
| State DB | ~/.hermes/state_backup_20260415_094022.db | 2026-04-15 |

## Claude Code Auto Dream详细机制

来源: 泄露源码分析 + 官方文档

### 触发条件
- 时间门: >= 24h since last dream
- Session门: >= 5 new sessions
- 双门控同时满足才触发
- 文件锁防并发

### 四阶段流程
1. **Orient**: ls memory目录，读MEMORY.md(master index)，浏览topic文件
2. **Gather Signal**: grep session transcripts（窄搜索，不全量读）
3. **Consolidate**: 合并重复、删矛盾、相对→绝对日期、去stale引用
4. **Prune & Index**: MEMORY.md控制在200行/25KB，超限demote到topic文件

### 关键约束
- 独立子进程运行（不中断工作）
- 只有memory目录写权限
- 用grep检索（非向量，这是Hermes可以超越的地方）
- 每条index entry < 150字符

## 相关文件

- 实施方案详细版: `~/.hermes/hermes-agent/docs/plans/2026-04-15-memory-upgrade.md`
- Dream A Skill: `~/.hermes/skills/note-taking/dreaming/SKILL.md`
- Memory Tool: `~/.hermes/hermes-agent/tools/memory_tool.py`
- Session Search: `~/.hermes/hermes-agent/tools/session_search_tool.py`
- State DB: `~/.hermes/hermes-agent/hermes_state.py`
- Gateway Session: `~/.hermes/hermes-agent/gateway/session.py`
