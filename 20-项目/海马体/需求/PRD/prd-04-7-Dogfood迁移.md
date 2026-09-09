---
title: PRD 6.7｜Dogfood迁移 (F26-F27)
created: 2026-04-21
updated: 2026-09-09
type: entity
tags: [openhippo]
status: draft
sources: [20-项目/海马体/项目需求文档(PRD).md]
---

# PRD 6.7｜Dogfood迁移 (F26-F27)

> 本页是 [[20-项目/海马体/需求/项目需求文档(PRD).md|海马体PRD]] 的分卷之一：**Hermes迁移 + Hook管道**
> 完整目录见 [[20-项目/海马体/需求/项目需求文档(PRD).md|PRD索引]]

---

### 6.7 Dogfood迁移

#### F26: Hermes记忆迁移

**需求描述**
从现有Hermes内嵌记忆系统迁移到海马体，采用**Hook管道双写**架构。Hermes内置memory保留作为热缓存，海马体作为持久化冷存储+语义搜索引擎。这是Dogfood第一步。

**解决的问题**
海马体的第一个用户就是Hermes Agent自己。通过Hook管道实现双写同步，而非替换Hermes内置memory，原因：
1. **早期曾考虑MCP方案但被否决**：大模型并不会每次都调用MCP tool，记忆同步不可靠
2. **Hook方案优势**：管道级自动拦截，每次memory操作100%被捕获，零遗漏
3. **保留Hermes热缓存**：Hermes内置memory注入system prompt的能力不可替代，海马体补充持久化+语义搜索

**操作步骤**
1. 部署OpenHippo Plugin到`~/.hermes/plugins/openhippo/`（见F27）
2. 导入MEMORY.md和USER.md到海马体hot_memory表
3. 迁移state.db中的冷记忆到海马体cold_memory表
4. 对所有cold记忆执行embedding backfill
5. 重启Hermes Gateway加载Plugin
6. 验证：三个Hook正常触发，双写同步无遗漏

**输入参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| hermes_state_db | str | ✅ | Hermes state.db路径（含cold memory） |
| memory_md | str | ✅ | MEMORY.md路径（hot memory - agent notes） |
| user_md | str | ✅ | USER.md路径（hot memory - user profile） |

**输出参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| migrated_hot | int | 迁移的热记忆条数 |
| migrated_cold | int | 迁移的冷记忆条数 |
| embeddings_generated | int | 生成的embedding数 |
| hooks_verified | bool | 三个Hook是否验证通过 |

**技术方案**
- MEMORY.md解析：§分隔符拆分→每段为一条hot记忆
- USER.md解析：§分隔符拆分→scope=user的hot记忆
- state.db解析：SQLite读取→mapping到hippocampus schema
- 迁移数据用metadata标记来源（`{"source": "hermes-migration"}`），不使用content前缀污染
- Hook Plugin部署：三文件（pre_llm_call/post_llm_call/post_tool_call）+ __init__.py

**验收标准**
1. 迁移后Hermes的memory add/replace/remove/search/archive/promote六个操作均同步到海马体
2. 原有MEMORY.md/USER.md内容可通过search检索
3. 迁移过程可回滚（保留原文件备份）
4. 迁移脚本幂等（重复运行不产生重复记忆）
5. 语义搜索验证通过（相关query命中迁移数据）

**验证手段**
- 端到端测试：迁移→Hermes对话→验证双写同步
- 完整性测试：对比迁移前后记忆条数和内容
- 回滚测试：迁移→回滚→验证原系统恢复
- 幂等测试：迁移两次→验证记忆数量不翻倍
- 语义搜索测试：用自然语言query验证embedding检索质量

---

#### F27: Hook管道集成（Pipeline Hook Integration）

**需求描述**
通过Hermes Plugin Hook机制实现海马体与Agent的自动集成。三个Hook覆盖记忆生命周期的全部入口，实现**全自动无感知**的记忆同步。

**解决的问题**
MCP依赖模型主动调用tool，不可靠（模型可能跳过、遗忘、选择不调用）。Hook在管道级拦截，100%捕获率，Agent完全无感知。

**架构概览**
```
用户消息 → [pre_llm_call Hook] → 语义搜索冷记忆 → 注入context
                                    ↓
         → LLM生成回复 → [post_llm_call Hook] → 规则提取 → 有价值则写入cold
                                    ↓
         → 工具调用 → [post_tool_call Hook] → 镜像memory操作到海马体
```

**三个Hook职责**

| Hook | 触发时机 | 职责 | 延迟要求 |
|------|----------|------|----------|
| pre_llm_call | 用户消息到达、LLM调用前 | 语义搜索冷记忆，注入相关上下文到system prompt | <2秒（阻塞） |
| post_llm_call | LLM回复生成后 | 规则层提取对话中有价值的记忆，写入cold存储 | 异步，不阻塞 |
| post_tool_call | 任何tool执行后 | 镜像memory工具的所有操作到海马体 | 异步，不阻塞 |

**技术方案**
- 通信：urllib.request同步HTTP调用海马体REST API
- 失败处理：所有写入操作best-effort + WAL重试（见F1写入可靠性）
- 搜索失败：静默降级，不影响对话
- Plugin注册：`register(ctx)`函数，ctx.register_hook()注册三个回调

**验收标准**
1. 三个Hook在Gateway启动时自动注册，日志可见
2. pre_llm_call：相关冷记忆注入到LLM上下文，搜索超时不阻塞对话
3. post_llm_call：只提取有价值的记忆（非全量对话），噪声率<30%
4. post_tool_call：memory的6种操作中写操作全部镜像
5. 海马体服务不可用时，Hermes对话完全不受影响（优雅降级）
6. WAL机制确保写入最终一致

**验证手段**
- Hook注册测试：重启Gateway→检查日志
- 注入测试：对话中提及历史话题→验证冷记忆出现在回复上下文
- 镜像测试：执行memory add→检查海马体DB中同步出现
- 降级测试：停止海马体→正常对话→验证无报错
- WAL测试：停止海马体→执行memory操作→重启→验证WAL回放


---


---

## 相关链接

- 上级索引：[[20-项目/海马体/需求/项目需求文档(PRD).md]]
- 项目主页：[[20-项目/海马体/需求/项目需求文档(PRD).md]]
- 知识库索引：[[index.md]]
