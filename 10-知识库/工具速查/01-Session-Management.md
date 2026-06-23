---
title: Hermes Session Management
created: 2026-06-23
updated: 2026-06-23
type: reference
tags: [hermes, cli, session]
status: active
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
```

## 跨平台 handoff 限制

- **线程能力平台**（Telegram/Discord/Slack）：完整支持，切换无缝
- **非线程平台**（多人群组的微信/WhatsApp）：仅支持私聊，多人群中会混乱

---

## 更新日志

| 日期 | 内容 |
|------|------|
| 2026-06-23 | 根据 Hermes 官方文档整理核心会话管理命令 |
