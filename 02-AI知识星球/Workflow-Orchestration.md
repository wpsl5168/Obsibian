---
title: "Workflow-Orchestration"
date: 2026-04-08
category: AI-Architecture
tags: [ai, architecture]
---

# Workflow & Orchestration（话题页）

> 目标：沉淀 agent 的控制流工程：graph/workflow、重试、checkpoint、HITL、预算。

## 我关注的主线（长期）
- 显式控制流：分支/循环/重试/超时/幂等
- 状态模型：state schema、持久化、checkpoint、可回放
- HITL：关键节点审批/复核
- 预算：token/cost/tool-call ceiling + stop condition

## 时间线（演进史速览）

- 2023→：[[AI Agent]] 从 prompt 驱动转向显式 workflow/graph（分支/循环/重试/checkpoint/HITL）。
  - 行业背景：长任务与工具链复杂度提升，必须可回放、可恢复、可审计

- 2024→：LangGraph 等 graph 编排框架兴起（以 release/文档为准）。
  - 技术：graph-based orchestration
  - 企业/生态：LangChain

- 2026-02：Microsoft [[AI Agent]] Framework RC：提供 graph-based workflows + streaming + checkpointing + HITL。
  - <https://devblogs.microsoft.com/foundry/microsoft-agent-framework-reaches-release-candidate/>

## 一手入口
- LangGraph（官方）：<https://www.langchain.com/langgraph>
- LangGraph releases：<https://github.com/langchain-ai/langgraph/releases>
- Microsoft [[AI Agent]] Framework：<https://devblogs.microsoft.com/foundry/microsoft-agent-framework-reaches-release-candidate/>
