---
title: "Claude Code 概览（落地导向）"
created: 2026-03-29
updated: 2026-04-20
type: concept
tags: [vibe-coding, agent]
status: draft
date: 2026-04-07
---

# Claude Code 概览（落地导向）

> 深度架构分析见 20260402-Claude Code架构分析 · MCP 协议见 [[3.2-Model_Context_Protocol规范解析]]

> 你关心的是：vibe coding 到底能做什么、怎么评估、怎么快速落地。

## 一句话定位
Claude Code 是一个 **agentic coding 环境**：它不只是回答问题，而是能在你的项目里读文件、改文件、跑命令，按“探索→计划→实现→验证”的循环完成任务。

## 官方截图（用于快速建立直觉）
![Claude Code Auto mode（官方截图，来源见下）](../assets/claude-code/auto-mode.png)

来源：Claude Code Docs（Week 13 · March 23–27, 2026）
- 页面：https://code.claude.com/docs/en/whats-new/2026-w13
- 图片原址：https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/auto-mode.png
- 访问日期：2026-04-07

## 最小落地路径（MVP）
1) 选一个小目标：修一个 bug / 加一个小功能（最好有测试）
2) 让 Claude Code 先“读代码+计划”（Plan Mode），再让它动手改
3) 让它跑测试/脚本自证（verify），你只做验收
4) 产物：一个可合并的 commit/PR（这是最容易衡量的）

## 关键能力（你会频繁用到）
- **Plan Mode**：先分析不改代码，避免“上来就写错方向”。
- **Checkpointing**：随时 rewind（注意：bash 改文件不在 checkpoint 里）。
- **CLI**：支持 `claude` 交互、`claude -p` 一次性、`claude -c` 继续、`claude -r` 恢复。
- **.claude/ 目录**：把“项目约定/规则/技能/工具接入”外置成配置。
- **Channels（研究预览）**：把外部事件推到运行中的 session（适合 CI/告警/聊天桥）。

## 适合 vs 不适合（企业软件/银行视角）
适合：
- 读老代码、定位问题、写修复补丁
- 写脚手架/重复性改造（重命名、抽取、补齐测试）
- 快速做 PoC

不适合（或必须加护栏）：
- 直接在生产环境执行有破坏性的命令
- 未经审计/审批就改关键业务逻辑

## 官方一手入口
- Overview：<https://code.claude.com/docs/en/overview>
- Best Practices：<https://code.claude.com/docs/en/best-practices>
- CLI reference：<https://code.claude.com/docs/en/cli-reference>
- Checkpointing：<https://code.claude.com/docs/en/checkpointing>
- Explore .claude directory：<https://code.claude.com/docs/en/claude-directory>
- Channels：<https://code.claude.com/docs/en/channels>

## 时间线（演进史速览）
- 2021→：Copilot 把“补全范式”推到主流
- 2024→：coding agent 进入“读仓库/改文件/跑命令”的端到端阶段
- 2026→：Claude Code 产品化 + 工程化（checkpointing / rules / plugins / channels）
