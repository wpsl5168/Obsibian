# 海马体（Hippocampus）— 项目需求文档（PRD）

> 版本：v1.1 | 日期：2026-04-18 | 作者：小虾 | 状态：初稿待评审

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
| **处理逻辑** | ① 聚类相似记忆（余弦>0.85） ② 合并/摘要（规则层：模板拼接；模型层：调用外部API） ③ 检测矛盾记忆（"用户喜欢A" vs "用户不喜欢A"）保留最新 ④ 生成整合报告 |
| **验收标准** | ① 整合后记忆数量减少≥20%（有重复时） ② 矛盾检测准确率≥80% ③ 整合不丢失关键信息（人工抽检） ④ 默认每天凌晨自动运行一次 |

---

### 6.2 记忆管理（Lifecycle Management）

#### F11: 自动温度调控

| 项目 | 说明 |
|------|------|
| **功能描述** | 基于访问模式自动调整记忆温度（Hot/Warm/Cold），无需人工干预 |
| **升温规则** | Warm→Hot: `access_count ≥ 5 AND last_accessed within 7d`; Cold→Warm: 被检索命中时自动升温 |
| **降温规则** | Hot→Warm: `last_accessed > 7d`; Warm→Cold: `last_accessed > 30d AND access_count < 3` |
| **遗忘公式** | `score = α × recency(t) + β × relevance(query) + γ × frequency(n)` 其中 α=0.4, β=0.35, γ=0.25; `recency(t) = exp(-λt)`, λ=0.05/天; score < 0.1 且非pinned → 标记待清除 |
| **接口** | `POST /v1/maintenance/sweep` (手动触发), `GET /v1/maintenance/schedule` (查看自动任务) |
| **参数** | sweep: `dry_run: bool`, `threshold: float` (遗忘阈值, 默认0.1) |
| **验收标准** | ① 温度调控每小时自动运行一次 ② 升降温有日志记录（consolidation_log） ③ pinned记忆永不降温/遗忘 ④ 用户可通过config.yaml自定义α/β/γ和时间窗口 |

#### F12: 记忆版本与冲突处理

| 项目 | 说明 |
|------|------|
| **功能描述** | 记忆更新时保留历史版本，矛盾记忆自动检测并标记 |
| **接口** | `GET /v1/memories/{id}/history`, `POST /v1/memories/conflicts` |
| **存储** | 表 `memory_versions`(memory_id, version, content, updated_at); 表 `conflicts`(id, memory_a_id, memory_b_id, type, resolved) |
| **矛盾检测** | 同scope+同主题的记忆，语义相似度>0.8但情感/意图相反 → 标记为conflict |
| **解决策略** | 默认保留最新; 可配置为`ask`(标记待人工决策)或`merge`(调用本地模型合并) |
| **验收标准** | ① 每次update自动创建版本记录 ② 最多保留10个历史版本（可配置） ③ conflicts接口返回未解决冲突列表 ④ 冲突解决后自动清理旧版本 |

#### F13: 记忆导入导出与迁移

| 项目 | 说明 |
|------|------|
| **功能描述** | 支持记忆批量导入导出，兼容Mem0/CLAUDE.md等格式 |
| **接口** | `POST /v1/memories/export`, `POST /v1/memories/import` |
| **参数** | export: `format: enum(json\|markdown\|mem0)`, `scope: str`, `agent_id: str`; import: `file: UploadFile`, `format: enum(json\|markdown\|mem0\|claudemd)`, `target_repo: str` |
| **支持格式** | JSON(原生), Markdown(MEMORY.md风格), Mem0 JSON, CLAUDE.md(Claude Code记忆) |
| **验收标准** | ① export→import round-trip零数据丢失 ② 导入Mem0格式自动映射字段 ③ 导入CLAUDE.md自动拆分为独立记忆条目 ④ 大批量(10K条)导入<60秒 |

---

### 6.3 隔离模式（Isolation Model）

> 设计理念：借鉴GitHub的 Organization → Repository → Branch 模型

#### F14: 三级隔离架构

| 层级 | 概念 | 类比GitHub | 说明 |
|------|------|-----------|------|
| **L1: Tenant（租户）** | 部署实例 | GitHub Organization | 一个海马体实例 = 一个租户，物理隔离（独立DB文件） |
| **L2: Agent（代理）** | 注册的AI Agent | GitHub User | 每个Agent有唯一ID+Token，拥有私有记忆空间 |
| **L3: Session（会话）** | 单次对话上下文 | GitHub Branch | 会话级临时记忆，会话结束后决定保留/丢弃 |

#### F15: 记忆库权限体系

| 项目 | 说明 |
|------|------|
| **功能描述** | Agent通过PAT(Personal Access Token)认证，记忆库分public/private，权限精细控制 |
| **Token机制** | 注册Agent时生成PAT，格式`hpc_xxxxxxxxxxxx`，SHA-256哈希存储，支持多Token（如只读Token、全权Token） |
| **Token Scope** | `memory:read` — 读取记忆; `memory:write` — 写入记忆; `repo:admin` — 管理记忆库; `consolidate` — 触发整合 |
| **记忆库类型** | `private` — 仅owner和被授权Agent可访问; `public` — 同租户下所有Agent可读（写仍需授权） |

**权限矩阵：**

| 角色 | 自己的private repo | 他人的private repo | public repo | 共享repo(被授权) |
|------|-------------------|-------------------|-------------|-----------------|
| **主Agent (owner)** | 读写删 | ❌ | 读 | 按授权(read/write/admin) |
| **子Agent** | 读写删(自己的) | ❌ | 读 | 按授权(通常只读) |
| **未注册Agent** | ❌ | ❌ | ❌ | ❌ |

**典型场景：**

```
场景1: Hermes主Agent + 子Agent协作
├── hermes-private (private)     ← 主Agent独占，存用户偏好/敏感信息
├── hermes-shared (public)       ← 所有子Agent可读，存项目上下文/技术约定
└── sub-agent-001-private (private) ← 子Agent独占，存临时推理中间结果

场景2: 多Agent团队
├── team-knowledge (public)      ← 团队共享知识库
├── agent-alice-private (private) ← Alice的个人记忆
├── agent-bob-private (private)   ← Bob的个人记忆
└── project-x (private)          ← 项目专属，Alice=admin, Bob=read
```

| **接口** | 说明 |
|---------|------|
| `POST /v1/agents` | 注册Agent，返回PAT |
| `POST /v1/agents/{id}/tokens` | 生成额外Token（指定scope） |
| `DELETE /v1/agents/{id}/tokens/{token_id}` | 吊销Token |
| `POST /v1/repos` | 创建记忆库 |
| `PUT /v1/repos/{id}` | 修改记忆库（名称/可见性） |
| `POST /v1/repos/{id}/grant` | 授权Agent访问 |
| `DELETE /v1/repos/{id}/grant/{agent_id}` | 撤销授权 |
| `GET /v1/repos/{id}/grants` | 查看授权列表 |

| **验收标准** |
|-------------|
| ① 无Token请求返回401 |
| ② Token scope不足返回403 |
| ③ 访问无权限的private repo返回404（不暴露存在性） |
| ④ public repo未授权写入返回403 |
| ⑤ Token吊销后立即生效（<1秒） |
| ⑥ 支持同时100+个Agent注册 |

#### F16: Session级记忆隔离

| 项目 | 说明 |
|------|------|
| **功能描述** | 会话级临时记忆空间，会话内自动可见，会话结束时由Agent决定哪些提升为持久记忆 |
| **接口** | `POST /v1/sessions` (开始会话), `DELETE /v1/sessions/{id}` (结束会话), `POST /v1/sessions/{id}/promote` (提升记忆) |
| **参数** | 开始: `agent_id, session_id(可选，默认生成)`, 结束: `promote_strategy: enum(all\|none\|auto)` — auto由本地模型判断哪些值得保留 |
| **存储** | 表 `session_memories`(session_id, memory_id) 关联表，会话结束且不提升时清除 |
| **验收标准** | ① 会话记忆对其他会话不可见 ② promote=auto时，模型判断保留率在30-70%之间（非全保留/全丢弃） ③ 会话结束后临时记忆在24h内自动清除 |

---

### 6.4 记忆共享（Memory Sharing）

> 设计理念：**隔离是默认，共享是显式授权的动作。** 像发GitHub Collaborator邀请一样精确控制谁能看到什么。

#### F17: 共享记忆库（Shared Repos）

| 项目 | 说明 |
|------|------|
| **功能描述** | Agent创建共享记忆库，邀请其他Agent加入，实现跨Agent知识传递 |
| **接口** | `POST /v1/repos` (创建), `POST /v1/repos/{id}/grant` (邀请), `GET /v1/repos/{id}/feed` (共享动态) |
| **共享粒度** | **repo级** — 整个记忆库共享; **tag级** — 只共享指定tag的记忆（如 `grant(agent_id, permission, tags=["project-context"])` ） |
| **写入冲突** | 多Agent同时写入同一repo时，采用 last-write-wins + 自动版本记录（F12），不做分布式锁 |
| **验收标准** | ① 授权后Agent立即可检索共享记忆（<1秒生效） ② tag级共享过滤准确率100% ③ 共享记忆的修改对所有被授权Agent实时可见 ④ feed接口返回最近的共享记忆变更流（分页） |

#### F18: 记忆广播（Memory Broadcast）

| 项目 | 说明 |
|------|------|
| **功能描述** | 主Agent向所有子Agent单向推送关键上下文（如用户偏好变更、项目决策），子Agent无需主动拉取 |
| **接口** | `POST /v1/broadcast` |
| **参数** | `content: str`, `from_agent: str`, `to_agents: list[str]` (空=所有已注册Agent), `priority: enum(normal\|urgent)`, `ttl: int` |
| **机制** | 写入各目标Agent的收件队列表 `inbox`; Agent下次search时自动注入urgent广播; normal广播在Agent显式调用 `GET /v1/inbox` 时返回 |
| **验收标准** | ① urgent广播在下次search时自动出现在结果最前 ② 广播有已读状态追踪 ③ TTL到期自动清除 ④ 单次广播支持最多1000个目标Agent |

**典型共享场景：**

```
场景1: 用户偏好同步
  用户对Hermes说"我喜欢简洁风格" 
  → Hermes写入自己的private repo
  → Hermes通过broadcast推送给所有子Agent
  → 子Agent下次工作时自动获得该偏好

场景2: 项目知识共享
  主Agent创建 "brickhub-context" shared repo (public)
  → 主Agent写入项目架构、技术栈、设计规范
  → Claude Code子Agent被授权read
  → Claude Code检索时自动搜索shared repo + 自己的private repo

场景3: 跨Agent学习
  Agent-A完成了一个复杂debug，提炼出经验
  → Agent-A写入shared repo "team-learnings" (tag: "debugging")
  → Agent-B下次遇到类似问题，search命中该经验
  → 避免重复踩坑

场景4: 敏感信息隔离
  主Agent持有用户API keys、个人信息
  → 存在private repo，不共享
  → 子Agent只能访问脱敏后的共享上下文
  → 即使子Agent被注入恶意prompt，也无法获取敏感信息
```

#### F19: 共享审计日志（Sharing Audit Trail）

| 项目 | 说明 |
|------|------|
| **功能描述** | 记录所有共享相关操作，便于安全审计和问题追踪 |
| **接口** | `GET /v1/audit/sharing` |
| **参数** | `agent_id: str`, `repo_id: str`, `action: enum(grant\|revoke\|read\|write\|broadcast)`, `since: datetime`, `limit: int` |
| **存储** | 表 `sharing_audit`(id, timestamp, actor_agent_id, target_agent_id, repo_id, action, detail) |
| **验收标准** | ① 每次grant/revoke/broadcast自动记录 ② 每次跨Agent读取记录（可配置关闭以降低写入量） ③ 日志保留90天（可配置） ④ 支持按Agent/Repo/Action维度过滤 |

---

### 6.5 安全与自动化

#### F20: 敏感信息识别（PII Detection）

| 项目 | 说明 |
|------|------|
| **功能描述** | 写入记忆时自动检测敏感信息（API Key、邮箱、手机号、身份证号等），标记或脱敏，防止跨Agent共享时泄露 |
| **接口** | 写入流程自动触发；`POST /v1/memories/scan` 可手动扫描存量 |
| **实现** | 纯规则引擎，零模型依赖：正则匹配（API key模式、邮箱、手机号、身份证、信用卡号）+ 关键词黑名单（password、secret、token） |
| **行为** | 检测到PII后：① 自动添加 `pii:true` 标签 ② `scope` 强制为 `private`（不可共享） ③ 可选脱敏模式：用 `***` 替换敏感值后存储 |
| **配置** | `pii_detection: enabled/disabled`，`pii_action: tag_only/redact/reject`，`pii_patterns: list`（可扩展自定义正则） |
| **验收标准** | ① 识别率≥95%（标准格式PII） ② 误报率<5% ③ 检测延迟<5ms ④ 共享接口自动拦截含PII的private记忆 ⑤ scan接口可扫描存量并生成报告 |

#### F21: 自动记忆提取（Auto Memory Extraction）

| 项目 | 说明 |
|------|------|
| **功能描述** | 从Agent对话流中自动提取值得记住的内容，无需Agent显式调用add。这是核心用户体验——Agent不需要"知道"自己在存记忆 |
| **接口** | `POST /v1/extract` |
| **参数** | `messages: list[{role, content}]`（对话片段），`agent_id: str`，`mode: enum(rules\|model\|hybrid)` |
| **规则层（无模型）** | ① 用户纠正Agent时 → 提取偏好（"我喜欢X不喜欢Y"模式匹配） ② 用户自述信息 → 提取事实（"我是/我在/我的"模式） ③ Agent发现环境信息 → 提取（"OS is/Python version"等） ④ 重复出现的关键词/实体 → 提取 |
| **模型层（可选）** | 调用外部LLM API对对话做摘要提取，识别隐含偏好和上下文 |
| **输出** | `extracted: list[{content, confidence, source_turn, suggested_scope, suggested_tags}]`，需Agent确认或配置自动写入阈值 |
| **验收标准** | ① 规则层可独立运行（零API费用） ② 提取准确率≥70%（规则层）/≥90%（模型层） ③ 支持auto_commit阈值：confidence>0.8自动写入 ④ 提取不阻塞对话（异步处理） ⑤ 防重复：提取结果与已有记忆去重 |

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
│  │              智能处理层（分级策略）                      │   │
│  │  无模型层：温度调控/TTL遗忘/正则PII/余弦去重（MVP）     │   │
│  │  可选模型层：整合/摘要/矛盾检测（外部API或本地大模型）   │   │
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
| **RAM** | 2GB（规则引擎模式）/ 4GB+（含embedding生成） |
| **磁盘** | 500MB（引擎） + 可选embedding模型缓存 |
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
| 外部LLM API | 整合/摘要/矛盾检测（OpenAI/Anthropic/本地Ollama均可） | ⚠️ 可选（无则仅用规则引擎，MVP够用） |
| jieba | 中文分词 | ⚠️ 可选（无则中文FTS降级） |

---

## 十、里程碑与排期

| 阶段 | 周期 | 目标 | 交付物 |
|------|------|------|--------|
| **M0: Dogfood** | W1-2 | 从Hermes现有记忆迁移 | ① 解析~/memory-mcp/memory_server.py的4个MCP tools → 抽象为hippocampus核心API ② 迁移MEMORY.md/USER.md→SQLite ③ Hermes config改接hippocampus MCP ④ 验证：Hermes记忆读写无感切换 |
| **M1: Core** | W3-4 | 记忆CRUD + 热冷分层 + 检索 | F1-F4完成，单元测试覆盖>80% |
| **M2: Protocol** | W5-6 | MCP + REST + CLI | F7-F9完成，可对接Claude Desktop/Hermes |
| **M3: Smart** | W7-8 | 智能整合 + 自动提取 + PII检测 | F5+F20+F21完成，Auto-Dream+规则引擎可运行 |
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
| POST | `/v1/memories/scan` | PII扫描存量 |
| POST | `/v1/extract` | 自动记忆提取 |

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
