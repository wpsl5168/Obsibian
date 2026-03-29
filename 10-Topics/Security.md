# Agent Security（话题页）

> 目标：把 agent 的安全风险（prompt injection、工具滥用、数据泄漏）与可执行的工程防线沉淀下来。

## 官方/权威渠道
- Martin Fowler：Agentic AI and Security
  - <https://martinfowler.com/articles/agentic-ai-security.html>

## 我认可的工程防线（简版）
- Treat all external content as untrusted input（网页/邮件/文档都是不可信输入）
- 最小权限：工具分级、写操作隔离
- 审批点：关键副作用（写库/发信/转账/删改）必须 requireApproval
- 沙箱：命令执行与文件读写都要可控边界
- 评测：上线前后用 evals 防回归

## 最近条目
- [[AI-Agent-Daily/2026-03-29]]
