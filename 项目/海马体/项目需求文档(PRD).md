# 海马体（Hippocampus）— 项目需求文档（PRD）

> 版本：v1.0 | 日期：2026-04-18 | 作者：小虾 | 状态：初稿待评审

---

## 一、项目目的

为AI Agent提供**本地优先、隐私第一**的持久化记忆引擎。让任何Agent框架通过标准协议（MCP/REST/CLI）即插即用地获得跨会话记忆能力，数据永远不离开用户的机器。

### 核心命题

> 现有AI Agent每次对话都是"失忆"的，记忆要么不存在，要么存在云端别人的服务器上。海马体让Agent像人一样记住重要的事，同时保证记忆完全属于你。

---

## 二、解决痛点

| # | 痛点 | 现状 | 海马体方案 |
|---|------|------|-----------|
| 1 | **Agent失忆** | 每次对话从零开始，用户反复重复偏好/上下文 | 自动提取、持久化、跨会话注入记忆 |
| 2 | **隐私泄露** | Mem0等方案数据上云，企业/个人敏感信息外泄 | 纯本地存储，零外部API调用（默认） |
| 3 | **部署复杂** | 竞品需3+容器、Neo4j、外部embedding API | `pip install hippocampus` 一行搞定 |
| 4 | **记忆割裂** | 多Agent各自为政，无法共享上下文 | GitHub-style记忆仓库，权限隔离+受控共享 |
| 5 | **记忆膨胀** | 只存不管，记忆越来越多越来越慢 | 热冷分层+自动遗忘+整合，模拟人脑记忆机制 |
| 6 | **集成成本高** | 每个框架对接方式不同 | MCP + REST + CLI三协议，5分钟集成 |

---

## 三、目标用户群体

### 主要用户

| 画像 | 规模 | 使用场景 | 付费意愿 |
|------|------|---------|---------|
| **独立开发者/Hacker** | 数十万 | 个人AI助手、Side Project | 低（用免费版） |
| **AI Agent框架作者** | 数千 | 为框架集成记忆能力 | 中（愿意赞助/Pro） |
| **企业AI团队** | 数千家 | 内网Agent部署，数据合规要求 | 高（Enterprise） |
| **多Agent玩家** | 数万 | Claude Code/Cursor/Hermes等多Agent协作 | 中 |

### 次要用户

| 画像 | 场景 |
|------|------|
| 知识工作者 | Obsidian/笔记系统+AI联动 |
| 教育/研究 | AI记忆研究、论文复现 |

---

## 四、开源形态

| 项目 | 说明 |
|------|------|
| **License** | Apache 2.0 |
| **仓库** | `github.com/hippocampus-ai/hippocampus`（待注册） |
| **模式** | Open-Core：核心引擎完全开源，高级功能付费 |
| **语言** | Python 3.10+ |
| **包管理** | PyPI (`pip install hippocampus`) + Docker |

### 开源范围

| 开源（Community） | 付费（Pro/Enterprise） |
|-------------------|----------------------|
| 完整记忆引擎 | 跨设备E2E加密同步 |
| MCP + REST + CLI | Web Dashboard |
| 热冷分层 + FTS5 + 向量搜索 | 记忆分析报告 |
| 本地模型推理 | 团队共享（RBAC） |
| 单机多Agent隔离共享 | SSO / 审计日志 |
| Obsidian整合 | SLA保障 |

---

## 五、部署形式

### 5.1 开发者本地部署（推荐）

```bash
pip install hippocampus
hippocampus serve          # 启动HTTP+MCP服务 (默认 localhost:8200)
hippocampus init           # 初始化记忆库
```

### 5.2 Docker部署

```bash
docker run -d -p 8200:8200 -v ~/.hippocampus:/data hippocampus/hippocampus:latest
```

### 5.3 嵌入式（Library模式）

```python
from hippocampus import MemoryEngine
engine = MemoryEngine(db_path="~/.hippocampus/memory.db")
engine.add("用户喜欢简洁直接的回复风格", agent="hermes", scope="user")
results = engine.search("用户偏好", limit=5)
```

### 5.4 MCP协议接入

```yaml
# claude_desktop_config.json / hermes config.yaml
mcp_servers:
  hippocampus:
    command: hippocampus
    args: ["mcp"]
```

---

## 六、功能清单

### 6.1 核心功能

#### F1: 记忆写入（Add/Update）

| 项目 | 说明 |
|------|------|
| **功能描述** | 将结构化或自然语言记忆写入存储，支持自动去重和合并 |
| **接口** | `POST /v1/memories` |
| **参数** | `content: str` (必填), `agent_id: str`, `scope: enum(user\|agent\|session\|shared)`, `tags: list[str]`, `metadata: dict`, `ttl: int` (秒，0=永不过期) |
| **存储** | SQLite表 `memories` — id, content, embedding(BLOB), agent_id, scope, tags(JSON), metadata(JSON), created_at, updated_at, access_count, last_accessed, temperature(hot/warm/cold), ttl |
| **验收标准** | ① 写入后立即可检索 ② 重复内容自动合并（余弦相似度>0.92触发） ③ 写入延迟<50ms（不含embedding） ④ 支持批量写入（最多100条/次） |

#### F2: 记忆检索（Search/Recall）

| 项目 | 说明 |
|------|------|
| **功能描述** | 混合检索：FTS5全文搜索 + 向量语义搜索 + 标签过滤，加权融合返回 |
| **接口** | `POST /v1/memories/search` |
| **参数** | `query: str` (必填), `agent_id: str`, `scope: list[str]`, `tags: list[str]`, `limit: int` (默认10, 最大100), `threshold: float` (相关性阈值, 默认0.5), `mode: enum(hybrid\|fts\|vector)` |
| **返回** | `results: list[{id, content, score, tags, created_at, access_count}]`, `total_count: int` |
| **验收标准** | ① 混合检索P@5 ≥ 0.8（人工标注测试集） ② 响应时间<100ms（1万条记忆规模） ③ FTS5支持中英文分词 ④ 检索自动更新access_count和last_accessed |

#### F3: 记忆删除/遗忘（Delete/Forget）

| 项目 | 说明 |
|------|------|
| **功能描述** | 手动删除指定记忆，或按策略自动遗忘 |
| **接口** | `DELETE /v1/memories/{id}`, `POST /v1/memories/forget` |
| **参数** | forget接口：`strategy: enum(ttl\|cold\|unused)`, `dry_run: bool` (预览不执行), `before: datetime` |
| **验收标准** | ① 删除后搜索不再返回 ② 自动遗忘按公式：`score = recency × relevance × frequency`，低于阈值降温/清除 ③ dry_run模式返回将被遗忘的列表但不执行 ④ 支持"永不遗忘"标记 |

#### F4: 热冷分层（Temperature Management）

| 项目 | 说明 |
|------|------|
| **功能描述** | 三级温度：Hot(内存+文件) → Warm(SQLite FTS5) → Cold(SQLite+向量归档) |
| **接口** | `POST /v1/memories/{id}/promote`, `POST /v1/memories/{id}/archive`, `GET /v1/memories/stats` |
| **参数** | promote: `target: enum(hot\|warm)`, archive: 无额外参数 |
| **存储** | Hot: 内存LRU缓存(默认500条) + MEMORY.md文件同步; Warm: SQLite主表; Cold: SQLite归档表+压缩embedding |
| **验收标准** | ① 新记忆默认Warm ② 访问频率>阈值自动升Hot ③ 30天未访问自动降Cold ④ Hot记忆注入延迟<5ms ⑤ stats接口返回各层数量和存储大小 |

#### F5: 记忆智能整合（Consolidation / Auto-Dream）

| 项目 | 说明 |
|------|------|
| **功能描述** | 定期用本地模型整合记忆：去重、合并矛盾、提炼摘要，类似人脑REM睡眠 |
| **接口** | `POST /v1/consolidate` (手动触发), 自动定时运行 |
| **参数** | `scope: str`, `dry_run: bool` |
| **处理逻辑** | ① 聚类相似记忆（余弦>0.85） ② 调用本地7B模型合并/摘要 ③ 检测矛盾记忆（"用户喜欢A" vs "用户不喜欢A"）保留最新 ④ 生成整合报告 |
| **验收标准** | ① 整合后记忆数量减少≥20%（有重复时） ② 矛盾检测准确率≥80% ③ 整合不丢失关键信息（人工抽检） ④ 默认每天凌晨自动运行一次 |

---

### 6.2 多Agent协作功能

#### F6: Agent隔离与共享（Multi-Agent Memory）

| 项目 | 说明 |
|------|------|
| **功能描述** | GitHub-style记忆仓库：每个Agent有私有记忆，可创建共享仓库 |
| **接口** | `POST /v1/agents` (注册), `POST /v1/repos` (创建记忆库), `POST /v1/repos/{id}/grant` (授权) |
| **参数** | agent注册: `agent_id, name, token`; repo创建: `name, visibility(public/private)`; grant: `agent_id, permission(read/write/admin)` |
| **存储** | 表 `agents`(id, name, token_hash, created_at), `repos`(id, name, owner_agent_id, visibility), `repo_grants`(repo_id, agent_id, permission) |
| **验收标准** | ① Agent只能访问有权限的记忆库 ② Token认证延迟<10ms ③ 支持最少100个Agent并发 ④ 权限变更实时生效 |

---

### 6.3 协议层

#### F7: REST API

| 项目 | 说明 |
|------|------|
| **功能描述** | 标准RESTful HTTP API，FastAPI实现 |
| **端口** | 默认 `localhost:8200` |
| **认证** | Bearer Token（Agent Token），本地模式可关闭 |
| **格式** | JSON，UTF-8 |
| **文档** | 自动生成OpenAPI 3.0 (Swagger UI at `/docs`) |
| **验收标准** | ① 所有F1-F6功能通过REST可调用 ② 响应格式统一 `{data, error, meta}` ③ 错误码遵循HTTP标准 ④ 支持CORS配置 |

#### F8: MCP协议

| 项目 | 说明 |
|------|------|
| **功能描述** | Model Context Protocol Server，供Claude Code/Hermes等MCP客户端直接调用 |
| **Tools** | `memory_add`, `memory_search`, `memory_delete`, `memory_stats`, `memory_consolidate` |
| **传输** | stdio (默认) / SSE |
| **验收标准** | ① Claude Desktop / Hermes配置后可直接调用 ② Tool参数与REST API一致 ③ 返回格式为MCP标准content block |

#### F9: CLI工具

| 项目 | 说明 |
|------|------|
| **功能描述** | 命令行界面，用于管理和调试 |
| **命令** | `hippocampus serve`, `init`, `add`, `search`, `forget`, `stats`, `consolidate`, `export`, `import` |
| **验收标准** | ① 所有命令支持 `--help` ② `search`支持交互式TUI（可选） ③ `export/import`支持JSON格式备份迁移 ④ 退出码遵循Unix惯例 |

---

### 6.4 知识库整合

#### F10: Obsidian/文件系统整合

| 项目 | 说明 |
|------|------|
| **功能描述** | 将Obsidian vault或指定目录下的Markdown文件索引为可检索的知识库 |
| **接口** | `POST /v1/knowledge/index`, `POST /v1/knowledge/search` |
| **参数** | index: `path: str, glob: str` (默认"*.md"), `recursive: bool`, `watch: bool` (文件变更自动重索引); search同F2 |
| **存储** | 独立表 `knowledge`，结构同memories但增加 `source_path, file_hash` |
| **验收标准** | ① 索引1000个MD文件<30秒 ② 文件变更后5秒内自动重索引（watch模式） ③ 搜索可跨memories+knowledge联合查询 ④ 支持frontmatter解析为metadata |

---

## 七、操作流程

### 7.1 首次安装流程

```
用户 → pip install hippocampus
     → hippocampus init (创建~/.hippocampus/目录和memory.db)
     → hippocampus serve (启动服务, localhost:8200)
     → 配置Agent的MCP/REST连接
     → 开始使用
```

### 7.2 记忆生命周期

```
Agent对话 → 记忆提取(自动/手动)
         → 写入Warm层(SQLite)
         → 生成embedding(本地模型)
         → 被检索时score++, 高频→升Hot
         → 长期未访问→降Cold
         → 整合任务→去重/合并/摘要
         → TTL到期或遗忘策略触发→删除
```

### 7.3 多Agent共享流程

```
Agent-A → 创建共享记忆库 "project-x"
       → 写入项目上下文记忆
Agent-B → 被授权read权限
       → 检索共享记忆 → 获得项目上下文
       → 写入自己的私有记忆库(分析结论等)
```

---

## 八、架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        客户端层                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │Claude Code│  │  Hermes  │  │  Cursor  │  │ 自定义Agent│  │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘  └─────┬─────┘  │
│        │MCP          │REST         │MCP          │REST     │
└────────┼─────────────┼─────────────┼─────────────┼─────────┘
         └─────────────┼─────────────┘             │
                       ▼                           │
┌──────────────────────────────────────────────────┼─────────┐
│                    协议网关层                       │         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┴───────┐ │
│  │  MCP Server   │  │  REST API    │  │    CLI Interface  │ │
│  │  (stdio/SSE)  │  │  (FastAPI)   │  │    (Click/Typer)  │ │
│  └───────┬──────┘  └───────┬──────┘  └───────┬──────────┘ │
│          └─────────────────┼─────────────────┘             │
│                            ▼                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  认证与权限层                          │   │
│  │   Agent Token验证 → Repo权限检查 → Scope过滤          │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   核心引擎层                           │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │   │
│  │  │记忆写入   │ │混合检索   │ │遗忘策略   │ │整合引擎│ │   │
│  │  │(去重/合并)│ │(FTS+Vec) │ │(评分/降温)│ │(Dream) │ │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └────────┘ │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   存储层                              │   │
│  │  ┌─────────┐  ┌─────────────┐  ┌─────────────────┐ │   │
│  │  │ Hot(L1) │  │  Warm(L2)   │  │    Cold(L3)     │ │   │
│  │  │ LRU缓存  │  │ SQLite+FTS5 │  │ SQLite归档+向量  │ │   │
│  │  │ +MD同步  │  │  主存储      │  │  压缩存储        │ │   │
│  │  └─────────┘  └─────────────┘  └─────────────────┘ │   │
│  │                     │                               │   │
│  │  ┌──────────────────┴──────────────────────────┐    │   │
│  │  │              知识库索引                        │    │   │
│  │  │  Obsidian vault / Markdown目录 / 自定义源      │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────┘   │
│                         ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 本地模型层                             │   │
│  │  Ollama / llama.cpp — 7B模型                         │   │
│  │  用途：embedding生成、记忆分类、摘要、遗忘决策、矛盾检测  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

数据文件:
~/.hippocampus/
├── memory.db          # SQLite主数据库(memories+knowledge+agents+repos)
├── memory.db-wal      # WAL日志
├── config.yaml        # 配置文件
├── hot/
│   └── MEMORY.md      # Hot记忆人可读镜像
└── models/
    └── nomic-embed/   # 本地embedding模型缓存
```

---

## 九、环境要求

### 最低配置

| 项目 | 要求 |
|------|------|
| **OS** | Linux / macOS / Windows (WSL2) |
| **Python** | 3.10+ |
| **RAM** | 2GB（无本地模型）/ 6GB（含7B模型推理） |
| **磁盘** | 500MB（引擎） + 4GB（本地模型，可选） |
| **网络** | 安装时需要（pip/docker pull），运行时完全离线 |

### 推荐配置

| 项目 | 要求 |
|------|------|
| **RAM** | 8GB+ |
| **磁盘** | SSD，10GB+ |
| **GPU** | 可选，CUDA/Metal加速embedding生成 |

### 依赖

| 依赖 | 用途 | 是否必须 |
|------|------|---------|
| SQLite 3.35+ | 存储（内置于Python） | ✅ 必须 |
| sqlite-vec | 向量搜索扩展 | ✅ 必须 |
| FastAPI + Uvicorn | REST API | ✅ 必须 |
| Ollama | 本地模型推理 | ⚠️ 可选（无则禁用智能功能） |
| jieba | 中文分词 | ⚠️ 可选（无则中文FTS降级） |

---

## 十、里程碑与排期

| 阶段 | 周期 | 目标 | 交付物 |
|------|------|------|--------|
| **M0: Dogfood** | W1-2 | 从Hermes记忆系统提炼核心 | 独立Python包骨架，通过现有memory_server.py验证 |
| **M1: Core** | W3-4 | 记忆CRUD + 热冷分层 + 检索 | F1-F4完成，单元测试覆盖>80% |
| **M2: Protocol** | W5-6 | MCP + REST + CLI | F7-F9完成，可对接Claude Desktop/Hermes |
| **M3: Smart** | W7-8 | 本地模型 + 整合 + 遗忘 | F5完成，Auto-Dream可运行 |
| **M4: Multi-Agent** | W9-10 | Agent隔离共享 + 知识库 | F6+F10完成 |
| **M5: Launch** | W11-12 | 打包 + 文档 + 开源发布 | PyPI包, Docker镜像, GitHub README, HN Post |

---

## 附录A: API接口汇总

| 方法 | 路径 | 功能 |
|------|------|------|
| POST | `/v1/memories` | 写入记忆 |
| POST | `/v1/memories/batch` | 批量写入 |
| POST | `/v1/memories/search` | 检索记忆 |
| GET | `/v1/memories/{id}` | 获取单条记忆 |
| PUT | `/v1/memories/{id}` | 更新记忆 |
| DELETE | `/v1/memories/{id}` | 删除记忆 |
| POST | `/v1/memories/forget` | 批量遗忘 |
| POST | `/v1/memories/{id}/promote` | 升温 |
| POST | `/v1/memories/{id}/archive` | 降温归档 |
| GET | `/v1/memories/stats` | 统计信息 |
| POST | `/v1/consolidate` | 触发整合 |
| POST | `/v1/agents` | 注册Agent |
| POST | `/v1/repos` | 创建记忆库 |
| POST | `/v1/repos/{id}/grant` | 授权 |
| POST | `/v1/knowledge/index` | 索引知识库 |
| POST | `/v1/knowledge/search` | 搜索知识库 |
| GET | `/v1/health` | 健康检查 |

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
    tags TEXT DEFAULT '[]',        -- JSON array
    metadata TEXT DEFAULT '{}',    -- JSON object
    temperature TEXT CHECK(temperature IN ('hot','warm','cold')) DEFAULT 'warm',
    access_count INTEGER DEFAULT 0,
    ttl INTEGER DEFAULT 0,         -- 0=永不过期
    pinned BOOLEAN DEFAULT FALSE,  -- 永不遗忘标记
    created_at REAL DEFAULT (unixepoch('subsec')),
    updated_at REAL DEFAULT (unixepoch('subsec')),
    last_accessed REAL DEFAULT (unixepoch('subsec'))
);

-- FTS5全文索引
CREATE VIRTUAL TABLE memories_fts USING fts5(content, tags, tokenize='unicode61');

-- 向量索引 (sqlite-vec)
CREATE VIRTUAL TABLE memories_vec USING vec0(embedding float[768]);

-- Agent表
CREATE TABLE agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    token_hash TEXT NOT NULL,
    created_at REAL DEFAULT (unixepoch('subsec'))
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
    PRIMARY KEY (repo_id, agent_id)
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
    action TEXT,          -- merge/dedupe/forget/summarize
    affected_ids TEXT,    -- JSON array of memory IDs
    detail TEXT,
    created_at REAL DEFAULT (unixepoch('subsec'))
);
```
