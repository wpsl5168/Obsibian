---
title: PRD 九·十｜环境与里程碑
created: 2026-04-21
updated: 2026-04-21
type: entity
tags: [openhippo]
status: draft
sources: [20-项目/海马体/项目需求文档(PRD).md]
---

# PRD 九·十｜环境与里程碑

> 本页是 [[../项目需求文档(PRD)|海马体PRD]] 的分卷之一：**环境要求 + 里程碑规划**
> 完整目录见 [[../项目需求文档(PRD)|PRD索引]]

---

## 九、环境要求

| 项目 | 最低 | 推荐 |
|------|------|------|
| OS | Linux/macOS/Windows(WSL2) | Linux |
| Python | 3.10+ | 3.11+ |
| RAM | 2GB（规则引擎） | 8GB+ |
| 磁盘 | 500MB | SSD 10GB+ |
| 网络 | 安装时需要 | 运行时完全离线 |

核心依赖：SQLite 3.35+, sqlite-vec, FastAPI, Uvicorn
可选依赖：外部LLM API(OpenAI/Anthropic), jieba(中文分词), tiktoken(token计算)

---

## 十、里程碑规划

### M0: Dogfood迁移（第1-2周）

**目标**：通过Hook管道实现Hermes记忆双写同步到海马体

**交付物**
- [x] MemoryEngine核心类（add/search/replace/remove/archive/promote/stats）
- [x] SQLite + FTS5 + sqlite-vec混合检索引擎
- [x] REST API（FastAPI，/v1/*端点）
- [x] MEMORY.md/USER.md/state.db → 海马体迁移（含embedding backfill）
- [x] Hermes Plugin Hook管道（F27三个Hook）
- [ ] 写入去重（F1精确+语义去重）
- [ ] post_llm_call规则层提取（F18，替代全量存储）
- [ ] WAL重试机制（F1写入可靠性）
- [ ] 记忆审查REST API（GET/PUT/DELETE by ID + timeline）

**验收准则**
1. ✅ Hermes对话中 memory add → Hook自动镜像到海马体DB → search可检索
2. ✅ 原MEMORY.md中所有记忆可通过search命中
3. ✅ 迁移脚本幂等：运行两次记忆数不翻倍（去重保证）
4. ✅ Hook管道对Hermes完全透明（Agent无感知）
5. ✅ 海马体不可用时Hermes正常工作（优雅降级）
6. ⬜ 写入去重：重复内容不产生冗余记忆
7. ⬜ 规则层提取：只存有价值记忆，噪声率<30%
8. ⬜ 用户可通过REST API审查所有历史记忆

**涉及功能**：F1(写入+去重), F2(检索), F18(规则提取), F20(审查API), F26(迁移), F27(Hook管道)

---

### M1: 核心引擎（第3-4周）

**目标**：完整的记忆CRUD + 热冷分层 + 混合检索

**交付物**
- [ ] 完整REST API（F6）
- [ ] FTS5 + sqlite-vec混合检索
- [ ] 热冷三级温度管理（F4）
- [ ] CLI工具基础命令（F8）
- [ ] 单元测试覆盖>80%

**验收准则**
1. ✅ `POST /v1/memories` 写入延迟<50ms
2. ✅ `POST /v1/memories/search` 混合检索P@5≥0.8（50组测试集）
3. ✅ 1万条记忆规模search<100ms
4. ✅ Hot记忆注入延迟<5ms
5. ✅ `hippocampus add/search/stats` CLI可用
6. ✅ Swagger UI (`/docs`) 可交互
7. ✅ 所有API返回统一 `{data, error, meta}` 格式

**涉及功能**：F1-F5, F6, F8, F9

---

### M2: 多Agent隔离共享（第5-6周）

**目标**：Agent注册/认证 + 记忆库权限 + 共享机制

**交付物**
- [ ] Agent注册+Token认证体系（F11）
- [ ] 记忆库权限（F12）+ Session隔离（F13）
- [ ] 共享记忆库（F14）+ 广播（F15）
- [ ] 审计日志（F16）

**验收准则**
1. ✅ 无Token请求→401，scope不足→403，private不存在→404
2. ✅ Agent-A private记忆对Agent-B不可见
3. ✅ shared repo授权后Agent立即可检索（<1秒）
4. ✅ urgent广播在子Agent search时自动出现在结果首位
5. ✅ 审计日志记录完整，按维度可过滤
6. ✅ Session结束后临时记忆24h内清除

**涉及功能**：F11-F16

---

### M3: 智能引擎（第7-8周）

**目标**：智能整合 + 自动提取 + PII检测 + 上下文注入

**交付物**
- [ ] 整合引擎（F5规则层+可选模型层）
- [ ] 自动记忆提取（F18规则层）
- [ ] PII检测管道（F17）
- [ ] 上下文注入接口（F19）
- [ ] Auto-Dream定时任务

**验收准则**
1. ✅ 整合后有重复时记忆数减少≥20%
2. ✅ 自动提取准确率≥70%（规则层，50组测试）
3. ✅ PII标准格式识别率≥95%，误报<5%
4. ✅ inject输出不超过token_budget，误差<5%
5. ✅ Auto-Dream每天凌晨自动运行，有完整日志
6. ✅ 规则层零API费用可独立运行

**涉及功能**：F5, F17, F18, F19

---

### M4: 运维与集成（第9-10周）

**目标**：备份恢复 + Webhook + 知识库 + Review UI + 监控

**交付物**
- [ ] 备份恢复（F22）+ 自动备份定时任务
- [ ] Webhook事件推送（F21）
- [ ] Obsidian知识库索引（F24）
- [ ] 记忆审查Web UI（F20）
- [ ] 健康检查+监控（F25）
- [ ] 导入导出迁移（F23）5种格式 + 一键导出

**验收准则**
1. ✅ 备份→恢复round-trip零数据丢失
2. ✅ Webhook推送延迟<500ms，HMAC可验证
3. ✅ 1000个MD文件索引<30秒，watch模式5秒内重索引
4. ✅ Review UI 1万条加载<2秒，移动端可用
5. ✅ /health响应<50ms，DB不可用时返回unhealthy
6. ✅ 5种导入格式各通过round-trip测试

**涉及功能**：F20-F25, F10(版本)

---

### M5: 发布（第11-12周）

**目标**：打包发布 + 文档 + 开源

**交付物**
- [ ] PyPI包 (`pip install hippocampus`)
- [ ] Docker镜像 (`hippocampus/hippocampus:latest`)
- [ ] GitHub README（功能介绍+快速开始+架构图）
- [ ] API文档（自动生成+手写Guide）
- [ ] 集成指南（Hermes/Claude Code/Cursor）
- [ ] CHANGELOG + CONTRIBUTING

**验收准则**
1. ✅ `pip install hippocampus && hippocampus serve` 5分钟内可用
2. ✅ Docker一行命令启动
3. ✅ README含Quick Start可照做成功
4. ✅ 至少3个Agent框架集成指南
5. ✅ 全部F1-F26功能通过集成测试
6. ✅ 无已知Critical/High级别bug

**涉及功能**：全部

---


---

## 相关链接

- 上级索引：[[../项目需求文档(PRD)]]
- 项目主页：[[../README]]
- 知识库索引：[[../../../index]]
