---
title: PRD 附录 C：Hermes Agent 集成架构决策
created: 2026-04-21
updated: 2026-04-21
type: entity
tags: [openhippo]
status: draft
---

# PRD 附录 C：Hermes Agent 集成架构决策

> 📚 上级页面：[[prd-07-附录]]

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
