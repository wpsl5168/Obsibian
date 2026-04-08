---
title: "Security"
date: 2026-04-08
category: AI-Architecture
tags: [ai, architecture]
---

# [[AI Agent]] Security（话题页）

> 目标：把 agent 的安全风险（prompt injection、工具滥用、数据泄漏）与可执行的工程防线沉淀下来。

## 官方/权威渠道
- Martin Fowler：[[AI Agent]]ic AI and Security
  - <https://martinfowler.com/articles/agentic-ai-security.html>

## 我认可的工程防线（简版）
- Treat all external content as untrusted input（网页/邮件/文档都是不可信输入）
- 最小权限：工具分级、写操作隔离
- 审批点：关键副作用（写库/发信/转账/删改）必须 requireApproval
- 沙箱：命令执行与文件读写都要可控边界
- 评测：上线前后用 evals 防回归

## 时间线（演进史速览）

- 2025-08：Bruce Schneier 强调“LLM prompt injection 仍无法被有效防御”（引用/讨论在业界广泛传播）。
  - 技术：prompt injection / tool abuse / data exfiltration
  - 关键人物：Bruce Schneier、Simon Willison 等
  - 行业背景：agent 工具化带来的系统性安全风险被放大

- 202x-xx：Martin Fowler 体系化总结 agentic AI 安全风险与工程应对。
  - 技术：威胁建模、最小权限、审批点、沙箱、可观测
  - 行业背景：coding agents 与企业 agent 从“可用”走向“可上线”

## 最近条目
- [[AI-[[AI Agent]]-Daily/2026-03-29]]
