---
title: Hermes Memory System Upgrade
created: 2026-04-15
updated: 2026-04-21
type: entity
tags: [hermes, memory, architecture]
status: stable
oversized_ok: true
---

# Hermes Memory System Upgrade

> Created: 2026-04-15
> Updated: 2026-04-15
> Status: P1 Complete, P2 Complete
> Tags: #hermes #architecture #memory #vector-search #ollama

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
│  │ 4400 chars  │  │ 2750 chars                │  │
│  │ (hot memory)│  │ (user profile)            │  │
│  └─────────────┘  └───────────────────────────┘  │
└─────────────────────────────────────────────────┘
         ↕ archive/promote                    
┌─────────────────────────────────────────────────┐
│           Cold Memory (SQLite FTS5)              │
│  memory_entries table + FTS5 full-text search    │
│  unlimited capacity, keyword search              │
└─────────────────────────────────────────────────┘
         ↕ Ollama local embedding              
┌─────────────────────────────────────────────────┐
│         Vector Store (sqlite-vec)                │
│  embeddings table + vec0 virtual table (768维)    │
│  session summaries + memory entries              │
│  语义搜索 via cosine similarity                    │
│  Ollama nomic-embed-text (本地, 零成本)            │
└─────────────────────────────────────────────────┘
         ↕ auto-trigger (OR门控)                
┌─────────────────────────────────────────────────┐
│           Auto Dream (智能触发+日频保底)             │
│  代码触发: >=24h OR >=5sessions (满足任一即触发)     │
│  Cron保底: 每日0:00 UTC                           │
│  合并重复、删矛盾、归档低频、日期规范化               │
└─────────────────────────────────────────────────┘
```

## 技术选型

### 向量数据库: sqlite-vec
- **选择理由**: 163KB安装，零依赖，直接在现有state.db内建virtual table
- **替代方案评估**: ChromaDB(500MB+依赖地狱)、Qdrant(100MB+)、LanceDB(300MB+ pyarrow)、纯numpy(性能够但无SQL集成)
- **性能**: 1K向量查询<1ms（brute-force），我们的规模完全够用

### Embedding模型: Ollama nomic-embed-text (最终选型)
- **成本**: 零（本地推理，无API调用）
- **维度**: 768
- **速度**: ~0.8s per embedding
- **内存**: 274MB模型 + ~346MB运行时
- **运行方式**: systemd user service, 开机自启
- **降级方案**: OpenRouter text-embedding-3-small (1536维) 作为fallback
- **选型理由**: 对比mxbai-embed-large(670MB)，nomic更轻量，768维对我们的规模足够

### 行业对比
| Agent | 记忆整理机制 | 向量检索 | Embedding |
|-------|------------|---------|-----------|
| Claude Code | Auto Dream (24h+5sessions AND) | 无(grep) | 无 |
| Cursor | 无(社区Memory Bank) | 无 | 无 |
| Windsurf | 自动生成，无整理 | 无 | 无 |
| Cline | Context Handoff(反应式) | 无 | 无 |
| Aider | Session内递归摘要 | 无 | 无 |
| **Hermes(升级后)** | **Auto Dream + OR门控 + 日频保底** | **sqlite-vec 768维** | **Ollama本地** |

## 实施记录

### P0: Gateway重启Session丢失 ✅
- **改动**: `run_agent.py` — shutdown时一律写`.clean_shutdown`
- **效果**: 重启gateway后session正常延续

### P1a: Embedding基础设施 ✅
- 安装sqlite-vec (`pip install sqlite-vec`)
- `hermes_state.py` 新增 `embeddings` 表 + `embeddings_vec` 虚拟表 + `system_meta` 表
- `SCHEMA_SQL` 更新，确保新建DB也有完整表结构
- vec0维度从hardcoded改为动态读取 `embedding_client.EMBEDDING_DIM`

### P1b: Session Search向量化 ✅
- `session_search_tool.py` — 使用 `get_query_embedding()` 做语义搜索
- 搜索流程: query → embedding → KNN → 返回预生成summary（不调LLM）
- FTS5作为fallback
- 实测语义匹配效果良好

### P1c: Memory向量化 ✅
- `memory_tool.py` — cold memory search增加向量路径
- 使用 `get_query_embedding()` 加 "search_query:" 前缀优化检索质量
- 与FTS5结果合并去重

### P1d: 扩容Hot Memory ✅
- memory: 2200→4400 chars
- user: 1375→2750 chars
- 总~7150 chars ≈ 2000 tokens（原方案6000+3000太激进，按实际需求调整）

### P2: Auto Dream双触发器 ✅
- `run_agent.py` 的 `shutdown_memory_provider()` 中添加 `_check_auto_dream()` 调用
- **触发逻辑**: OR门控 — >=24h 或 >=5sessions 满足任一即触发（优于Claude Code的AND门控）
- **状态存储**: `system_meta` 表存 `last_dream_at` 和 `sessions_since_dream`
- **触发方式**: 通过 `trigger_job()` 轻量级触发现有Dream A cron job
- **保底机制**: Dream A cron schedule改为每日0:00 UTC
- 触发后重置计数器和时间戳

### Ollama本地Embedding部署 ✅
- **安装**: Ollama v0.20.7 → ~/ollama/bin/ (用户级安装，无sudo)
- **模型**: nomic-embed-text (274MB)
- **服务**: systemd user service (`~/.config/systemd/user/ollama.service`), enabled, auto-start
- **环境**: OLLAMA_HOST=127.0.0.1:11434, PATH加入~/.bashrc

### embedding_client.py 重写 ✅
- 双后端架构: Ollama primary → OpenRouter fallback
- `_detect_backend()`: 启动时探测Ollama(3s timeout)，失败降级OpenRouter
- `EMBEDDING_DIM`: 动态检测(768 for Ollama, 1536 for OpenRouter)
- `get_embedding(text)`: 通用embedding
- `get_query_embedding(text)`: 搜索专用，自动加 "search_query:" 前缀
- 从255行重写到323行

### 历史数据Backfill ✅
- `scripts/backfill_all_embeddings.py`: 295行迁移脚本
- 3阶段: session摘要生成 → session embedding → cold memory embedding
- 使用copilot provider(gpt-4o-mini)生成摘要，Ollama做embedding
- 完成34个embedding (30 sessions + 4 cold memory)

### Git提交与合并 ✅
- 7个开发commit squash合并为1条: `ca5540be feat: memory system upgrade - Ollama embedding, hybrid search, Auto Dream`
- PR #1 → wpsl5168/hermes-agent main (squash merge + delete branch)
- 清理所有feature分支(本地+远程): feat/auto-session-context, feat/elastic-hot-cold-memory, feature/auto-session-summary

## 测试结果

| 测试集 | 结果 |
|--------|------|
| hermes_state (137 tests) | 全部通过 |
| 完整test suite (11654 tests) | 11535 passed, 109 failed (全部pre-existing, 零回归) |
| session_search 语义搜索 | 手动验证OK |

## 变更文件清单

| 文件 | 变更 |
|------|------|
| `agent/embedding_client.py` | 完全重写 — Ollama+OpenRouter双后端 |
| `hermes_state.py` | vec0表维度动态化 + SCHEMA_SQL补全 |
| `tools/memory_tool.py` | get_embedding → get_query_embedding |
| `tools/session_search_tool.py` | 同上 |
| `scripts/backfill_all_embeddings.py` | 新增 — 历史数据迁移脚本 |
| `run_agent.py` | Auto Dream触发器 |

## 备份

| 备份项 | 路径 | 时间 |
|--------|------|------|
| 项目tar | ~/.hermes/hermes-agent-backup-20260415_094022.tar.gz | 2026-04-15 |
| Git tag | pre-memory-upgrade-20260415_094022 | 2026-04-15 |
| Memory文件 | ~/.hermes/memories_backup_20260415_094022/ | 2026-04-15 |
| State DB | ~/.hermes/state_backup_20260415_094022.db | 2026-04-15 |

## 后续可做（未排期）

1. **P1d扩容到更大** — 当前4400/2750，如果实际使用中hot memory经常满，可以继续扩
2. **Embedding维度自适应** — 如果切换模型导致维度变化，需要rebuild vec0表
3. **向量搜索质量调优** — 可以尝试hybrid scoring (BM25 + cosine)
4. **Ollama模型升级** — 关注nomic-embed-text v2或更好的小模型
5. **Auto Dream效果监控** — 观察触发频率和整理质量

## Claude Code Auto Dream详细机制

来源: 泄露源码分析 + 官方文档

### 触发条件
- 时间门: >= 24h since last dream
- Session门: >= 5 new sessions
- 双门控同时满足才触发（AND逻辑，Hermes改为OR更积极）
- 文件锁防并发

### 四阶段流程
1. **Orient**: ls memory目录，读MEMORY.md(master index)，浏览topic文件
2. **Gather Signal**: grep session transcripts（窄搜索，不全量读）
3. **Consolidate**: 合并重复、删矛盾、相对→绝对日期、去stale引用
4. **Prune & Index**: MEMORY.md控制在200行/25KB，超限demote到topic文件

### 关键约束
- 独立子进程运行（不中断工作）
- 只有memory目录写权限
- 用grep检索（非向量，这是Hermes已经超越的地方 ✅）
- 每条index entry < 150字符

## 相关文件

- Dream A Skill: `~/.hermes/skills/note-taking/dreaming/SKILL.md`
- Memory Tool: `~/.hermes/hermes-agent/tools/memory_tool.py`
- Session Search: `~/.hermes/hermes-agent/tools/session_search_tool.py`
- State DB: `~/.hermes/hermes-agent/hermes_state.py`
- Embedding Client: `~/.hermes/hermes-agent/agent/embedding_client.py`
- Backfill Script: `~/.hermes/hermes-agent/scripts/backfill_all_embeddings.py`
- Ollama Service: `~/.config/systemd/user/ollama.service`
- Gateway Session: `~/.hermes/hermes-agent/gateway/session.py`
