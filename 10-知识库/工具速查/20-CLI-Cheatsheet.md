---
title: "20-CLI-Cheatsheet"
created: 2026-03-29
updated: 2026-04-20
type: concept
tags: []
status: draft
date: 2026-04-08
category: Notes
---

# Claude Code CLI Cheatsheet（速查）

来源（官方）：<https://code.claude.com/docs/en/cli-reference>

## 常用
- `claude`：进入交互模式
- `claude "query"`：带初始 prompt 进入交互
- `claude -p "query"`：跑完就退出（适合脚本化）
- `claude -c`：继续当前目录最近一次对话
- `claude -r "<session>" "query"`：按 session id/name 恢复继续
- `claude update`：更新
- `claude auth login` / `logout` / `status`

## 建议的企业开发用法
- 把 repo 的 build/test/lint 命令写进 CLAUDE.md，让它少问你“怎么跑测试”。
