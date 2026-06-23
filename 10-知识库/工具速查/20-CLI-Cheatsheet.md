---
title: Hermes CLI Command Cheatsheet
created: 2026-06-23
updated: 2026-06-23
type: reference
tags: [hermes, cli, cheatsheet]
status: active
---

# Hermes CLI Command Cheatsheet

> 快速参考 — Hermes Agent 命令行核心用法

## 启动会话

```bash
# 基础启动
hermes
hermes chat

# 单次查询（one-shot）
hermes chat -q "总结最新的 PR"
hermes -z "巴黎的首都是哪里？"   # 纯脚本模式，只输出答案

# 指定模型和工具集
hermes chat --model anthropic/claude-sonnet-4.6 --toolsets web,terminal,skills

# 恢复会话
hermes -c                        # 继续最近会话
hermes -c "project name"        # 按名称恢复
hermes -r <session-id>          # 按 ID 恢复
```

## 全局选项

| 选项 | 说明 |
|------|------|
| `--version`, `-V` | 显示版本 |
| `--profile <name>`, `-p` | 选择 profile |
| `--resume <session>`, `-r` | 恢复指定会话 |
| `--continue`, `-c` | 恢复最近会话 |
| `--worktree`, `-w` | 在独立 git worktree 中启动 |
| `--yolo` | 跳过危险命令确认 |
| `--tui` | 使用新 TUI 界面 |
| `--cli` | 强制经典 CLI |
| `--ignore-rules` | 跳过 AGENTS.md / memory / skills 自动注入 |
| `--safe-mode` | 完全干净环境（调试用） |

## 会话内命令（Slash Commands）

### 基础操作
```bash
/help                  # 帮助
/new                   # 开新会话
/new <title>          # 开新会话并指定标题
/title <new-title>    # 重命名当前会话
/compress             # 压缩上下文
/resume <name>        # 恢复另一会话
/sessions             # 浏览所有会话
```

### 模型切换
```bash
/model                              # 查看当前模型
/model claude-sonnet-4             # 切换模型
/model openrouter:gpt-5.5          # 指定提供商和模型
/model custom:qwen-2.5             # 使用自定义端点
/model claude-sonnet-4 --global    # 切换并持久化到配置
```

### 工具集控制
```bash
/toolsets                          # 查看当前工具集
/toolsets web,terminal,browser     # 启用指定工具集
/toolsets +search                  # 添加工具集
/toolsets -terminal                # 移除工具集
```

### 技能管理
```bash
/skills                            # 列出可用技能
/skills list                       # 同上
/skills load <skill-name>         # 加载技能
/skills unload <skill-name>       # 卸载技能
/skill <name>                     # 快捷加载技能
```

### 记忆管理
```bash
/memory                            # 查看当前记忆
/memory add "用户偏好: 简洁回复"    # 添加记忆
/memory clear                      # 清空记忆
```

### 高级操作
```bash
/handoff telegram                  # 切换到 Telegram
/checkpoint                        # 创建 checkpoint
/undo                             # 撤销上一步
/retry                            # 重试上一次请求
/interrupt                        # 中断当前任务
```

## 模型配置

```bash
# 交互式配置（推荐）
hermes model

# 设置默认模型
hermes config set inference.model "anthropic/claude-sonnet-4.6"
hermes config set inference.provider "openrouter"

# 查看配置
hermes config get inference.model
hermes config list
```

## 会话管理

```bash
# 列出所有会话
hermes sessions list
hermes sessions browse              # 交互式浏览

# 重命名会话
hermes sessions rename <id> "new title"

# 删除会话
hermes sessions delete <id>
hermes sessions prune               # 清理旧会话
```

## 技能管理

```bash
# 列出技能
hermes skills list
hermes skills list --category devops

# 查看技能详情
hermes skills view <skill-name>

# 刷新技能索引
hermes skills sync
```

## Gateway（消息平台）

```bash
# 前台运行（推荐 Docker/WSL/Termux）
hermes gateway run

# 后台服务（systemd/launchd）
hermes gateway start
hermes gateway stop
hermes gateway restart
hermes gateway status

# 查看所有 profile 的 gateway 状态
hermes gateway list

# 安装/卸载系统服务
hermes gateway install
hermes gateway uninstall

# 配置消息平台
hermes gateway setup
```

## Profile 管理

```bash
# 列出 profile
hermes profile list

# 创建/切换 profile
hermes profile create work
hermes profile switch work

# 当前 profile
hermes profile current

# 删除 profile
hermes profile delete personal
```

## 配置管理

```bash
# 查看配置
hermes config list
hermes config get <key>

# 修改配置
hermes config set <key> <value>
hermes config unset <key>

# 编辑配置文件
hermes config edit

# 配置文件位置
# ~/.hermes/config.yaml            (全局)
# ~/.hermes/profiles/<name>/config.yaml   (profile 级)
```

## 快捷操作

### 脚本模式
```bash
# 纯输出，无 banner/spinner
result=$(hermes -z "计算 2+3")
echo $result    # 5

# 带环境变量覆盖
HERMES_INFERENCE_MODEL=gpt-5.5 hermes -z "hello"
```

### 批量处理
```bash
# 处理多个文件
for file in *.md; do
  hermes -z "总结文件" < "$file" > "${file%.md}-summary.txt"
done
```

### 快速修改
```bash
# 单次查询模式（不保存会话）
hermes chat -q "修复这个 bug" --quiet
```

## 调试技巧

```bash
# 详细日志
hermes chat -v                     # verbose
hermes chat --debug                # debug 模式

# 干净环境测试
hermes chat --safe-mode -q "测试问题"

# 忽略用户配置
hermes chat --ignore-user-config

# 禁用自动注入
hermes chat --ignore-rules
```

## 快捷键（TUI 模式）

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+C` | 中断（双击强制退出） |
| `Ctrl+D` | 退出 |
| `Ctrl+L` | 清屏 |
| `Tab` | 自动补全 |
| `Up/Down` | 历史记录 |
| `Alt+Enter` | 多行输入（Windows 用 `Ctrl+Enter`） |

## 常见场景

### 项目协作
```bash
# 工作 profile + 特定项目会话
hermes -p work -c "backend-refactor"
```

### 快速调研
```bash
# 启用 web 工具，one-shot 查询
hermes chat --toolsets web -q "最新的 Rust 2026 版本特性"
```

### 代码审查
```bash
# 启用 worktree，独立分支工作
hermes --worktree -q "Review this PR and suggest improvements"
```

### 长任务续传
```bash
# 任务做到一半，上下文太长
/compress              # 压缩并创建续集
# 或直接退出，稍后恢复
hermes -c              # 自动找到最新会话
```

---

## 更新日志

| 日期 | 内容 |
|------|------|
| 2026-06-23 | 根据 Hermes 官方文档整理 CLI 命令速查表 |
