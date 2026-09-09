---
title: Hermes Session Management
created: 2026-06-23
updated: 2026-08-04
type: methodology
tags: [hermes, workflow]
status: stable
---

# Hermes Session Management

> 会话管理速查 — 恢复、切换、命名、清理会话的核心命令

## 核心命令

### 会话恢复

```bash
# 恢复最近的 CLI 会话
hermes -c
hermes --continue

# 按名称恢复（自动找最新的）
hermes -c "my project"
hermes chat --continue "refactoring"

# 按 session ID 恢复
hermes -r 20250305_091523_a1b2c3
hermes --resume 20250305_091523_a1b2c3d4

# 查看所有会话
hermes sessions list
hermes sessions browse    # 交互式浏览器
```

### 会话命名

```bash
# 会话中修改标题
/title my research project

# 命令行修改标题
hermes sessions rename <session-id> "new title"

# 创建新会话时指定标题
hermes chat
/new payments-refactor
```

**自动续号**：压缩上下文（`/compress`）会自动创建续集
- `"my project"` → `"my project #2"` → `"my project #3"`
- 按名称恢复时自动定位到最新的

### 会话内操作

```bash
/compress              # 压缩上下文（生成摘要，清理冗余）
/new                   # 开新会话（不关闭当前）
/new <title>          # 开新会话并指定标题
/resume <name>        # 在会话内恢复另一个会话
/sessions             # 浏览所有会话

# 跨平台切换（CLI → Telegram/Discord/Slack）
/handoff telegram     # 切到 telegram，CLI 会话暂停
                      # 之后用 /resume 切回 CLI
```

### 会话清理

```bash
# 删除已结束的旧会话
hermes sessions prune

# 删除指定会话
hermes sessions delete <session-id>

# 清理所有会话（危险！不可恢复）
rm ~/.hermes/state.db
```

## 会话存储机制

- **存储位置**：`~/.hermes/state.db`（SQLite）
- **跨平台共享**：CLI / Telegram / Discord / Slack / 微信 / WhatsApp 等所有对话共存一个库
- **上下文策略**：Hermes **不会**在每轮都重发全部历史，只注入：
  - 系统提示词
  - 当前对话窗口
  - 本轮显式注入的内容（技能、记忆等）

**媒体附件**（图片/文件）：仅在当前轮次可见，后续轮次只保留文字描述或缓存路径，不重传原文件。

### 上下文压缩机制（Context Compression）

Hermes 使用**两层压缩机制**防止上下文溢出：

| 压缩层 | 触发阈值 | 作用范围 | 行为 |
|:---|:---|:---|:---|
| **Agent 压缩器** | 50% 上下文窗口 | 对话历史 | 清理旧工具输出（替换为占位符），保留决策和文件路径 |
| **Gateway 安全网** | 85% 上下文窗口 | 完整注入内容 | 强制触发 `/compress`，生成续集会话 |

> [!warning] 配置陷阱：双层阈值不能相等
> 如果将 Agent 和 Gateway 压缩阈值都设为 50%，会导致**每轮都压缩**（Agent 层判断需要压缩 → 执行压缩 → Gateway 层仍然检测到 50% → 再次触发压缩）。**正确做法**：保持 35-40% 的间隔（如 50% 和 85%）。

**压缩过程**（`/compress` 或自动触发）：

1. **清理旧工具输出**：长文件内容（2000 行日志、大型 JSON）替换为 `[Old tool output cleared to save context space]`
2. **保留关键决策**：工作目标、技术决策、文件变更、待办事项、失败教训
3. **生成续集会话**：创建新会话，标题自动编号（`my project` → `my project #2`）
4. **注入 handoff 上下文**：将压缩后的上下文作为"前情提要"注入新会话首轮

**压缩后的 handoff 文档结构**：

```markdown
## Goal
[项目目标，一句话]

## In Progress
[当前正在做什么]

## Key Decisions
[重要技术决策和原因]

## Relevant Files
[读取/修改/创建的文件路径]

## Next Steps
[下一步操作]

## Critical Context
[关键值、错误信息、配置细节]
```

### 压缩策略选择

| 场景 | 操作 | 何时使用 |
|:---|:---|:---|
| **保持同一会话** | `/compress` | 上下文拥挤但工作连贯，需要清理旧输出继续 |
| **开新会话** | `/new` | 切换任务、上下文混乱、或需要干净起点 |
| **跨平台切换** | `/handoff telegram` | CLI → 移动端，保持上下文连续性 |

> [!info] 压缩 vs 开新会话
> - **压缩**（`/compress`）：保留会话 ID 和历史链接，清理冗余，适合长任务
> - **开新会话**（`/new`）：完全干净的上下文，适合切换项目或重置混乱状态
> - **自动续集**：压缩时自动创建 `#2`、`#3` 等续集，恢复时（`hermes -c "my project"`）自动定位最新续集

## Session ID 格式

| 来源 | 格式 | 示例 |
|------|------|------|
| CLI/TUI | `YYYYMMDD_HHMMSS_<6位hex>` | `20250305_091523_a1b2c3` |
| Gateway（消息平台） | `YYYYMMDD_HHMMSS_<8位hex>` | `20250305_091523_a1b2c3d4` |

恢复时可用完整 ID、唯一前缀或标题。

## 常见工作流

### 快速恢复最近工作
```bash
hermes -c
# 回到最近的 CLI 会话，继续上次对话
```

### 项目间切换
```bash
# 为不同项目使用不同标题
hermes -c "backend refactor"
hermes -c "frontend redesign"
```

### 长任务 checkpoint
```bash
# 任务做到一半，上下文太长
/compress              # 生成摘要，清理冗余
# 会自动创建续集会话，标题加 #2
```

### CLI ↔ 手机切换
```bash
# 在 CLI 中
/handoff telegram
# 在 Telegram 继续对话

# 稍后切回 CLI
hermes -c "my project"
```

### 会话 handoff 最佳实践（跨会话/跨 agent 交接）

当工作跨越多个会话、终端、或无人值守运行时，使用 **handoff 文档**确保下一个 agent/session 能无缝接力：

**Handoff 文档必须包含**：
1. **目标**（Goal）：一句话概括任务目的
2. **文件变更**（Files Changed）：已修改/创建的文件路径（含行号或提交 SHA）
3. **数据源头**（Source of Truth）：下一个会话应该信任的文件、URL、API
   - ✅ `Repo: /Users/antoine/work/agent-hermes`
   - ✅ `Evidence: /Users/antoine/.hermes/gsc-snapshots/latest.json`
   - ✅ `Report: research/2026-06-22/topic-opportunities.md`
4. **执行命令**（Commands Run）：关键命令 + 验证输出（成功/失败状态）
5. **未验证假设**（Unverified Assumptions）：推测但未确认的部分
6. **阻塞点**（Blockers）：需要人工决策或外部输入的地方
7. **下一步安全操作**（Next Safe Action）：新会话的第一个操作

**何时使用 handoff**：
- `/compress` 之前：将 handoff 文档粘贴到聊天，压缩后自动注入新会话
- `/new` 之后：在新会话中粘贴 handoff 文档，跳过重复探索
- Cron 任务结束时：将 handoff 写入文件，供下次运行读取

**常见错误**：
- ❌ 只说 "done"（下一个 agent 不知道做了什么）
- ❌ 粘贴全部聊天记录（新会话被旧假设污染）
- ❌ 不标注数据源头（agent 信任过时的聊天文字而非真实文件）

## Profile 隔离

不同 profile 的会话相互独立：

```bash
# 默认 profile
hermes -c

# 工作 profile
hermes --profile work -c

# 个人 profile
hermes -p personal -c
```

每个 profile 有独立的：
- `state.db`（会话历史）
- `config.yaml`（配置）
- `skills/`（技能库）
- `memories/`（记忆）

## 配置项

```yaml
# ~/.hermes/config.yaml
display:
  resume_display: full    # 恢复时显示详细回顾
  # 或 minimal              # 只显示一行提示

# 上下文压缩配置
compression:
  threshold: 0.5          # Agent 压缩器触发阈值（50% 上下文窗口）
  # Gateway 安全网固定在 85%，不可配置
  # 两者间隔必须 ≥35%，否则会导致每轮都压缩
```

> [!tip] 压缩阈值调优建议
> - **默认 50%**：适合大多数场景，给 Agent 和 Gateway 留足 35% 缓冲
> - **30-40%**：频繁长文件操作（日志分析、大代码库），提前清理旧输出
> - **60-70%**：短对话为主，减少不必要的压缩开销
> - **禁止设置 >85%**：会绕过 Agent 压缩器，直接触发 Gateway 强制压缩（失去渐进式清理的机会）

## 跨平台 handoff 限制

- **线程能力平台**（Telegram/Discord/Slack）：完整支持，切换无缝
- **非线程平台**（多人群组的微信/WhatsApp）：仅支持私聊，多人群中会混乱

---

## 更新日志

| 日期 | 内容 |
|------|------|
| 2026-06-23 | 根据 Hermes 官方文档整理核心会话管理命令 |
| 2026-08-04 | **周度深度丰富**：补充两层上下文压缩机制（Agent 50% + Gateway 85%）、压缩过程详解、handoff 文档结构与最佳实践、压缩 vs 开新会话决策表、配置项调优建议（compression.threshold） |
