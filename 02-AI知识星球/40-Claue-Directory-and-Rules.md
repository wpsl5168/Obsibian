---
title: "40-Claue-Directory-and-Rules"
date: 2026-04-08
category: AI-Architecture
tags: [ai, architecture]
---

# .claude 目录与项目规则（怎么把 Claude 变成“懂你项目的人”）

来源（官方）：<https://code.claude.com/docs/en/claude-directory>

## 核心思想
把“项目约定”写成 Claude 每次都会读的文件，让它像团队成员一样遵守规范。

## 你最该先写的：CLAUDE.md
- 放在项目根目录（或 `.claude/CLAUDE.md`）
- 内容建议控制在 200 行内，写清：
  - build/test/lint 命令
  - 目录结构
  - coding style（命名/导出/日志/异常）
  - 安全/合规红线（比如不要读某些路径/不要执行某类命令）

## [[MCP]] 配置提示
- `.mcp.json`：项目级 [[MCP]] servers（团队共享）
- `~/.claude.json`：用户级 [[MCP]] servers（个人私有）
- secrets 推荐用环境变量引用（避免落盘）

> 我们后面做“银行业场景落地”时，CLAUDE.md 会是你最值钱的资产：它把隐性团队经验显性化。
