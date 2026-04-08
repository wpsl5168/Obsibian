---
title: LLM Architecture（索引）
updated_at: 2026-03-31
---

# LLM Architecture（索引）

> 维护者：小虾

## 入门必读（推荐顺序）
1) [[LLM-Parameters-Explained]] — 从“用户输入流程”讲透参数：推理怎么用、训练怎么更新、RAG/记忆/微调差异
2) [[MoE-vs-Dense-DB-Analogy]] — 用 SQL Server vs TiDB 的直觉理解 Dense vs MoE
3) [[MoE-vs-Dense-Diagrams]] — 两张 ASCII 图：分布式 SQL 执行流 & MoE 路由流
4) [[MoE-vs-Dense]] — 更完整的对比：差异、演化史、性能口径、选型建议

## 关键词速查
- 参数（Parameters）：模型可学习权重；推理只读，训练才会更新
- 总参数 vs 激活参数：MoE 必须区分 total vs active
- Router/Gate：MoE 的“分诊台/路由层”
- Experts：被路由到的“专家 FFN”，像分布式节点/分片
- 热点专家：类似热点分片，导致吞吐下降、p95/p99 变差

## 后续可扩展主题（待补）
- KV Cache / Prefill vs Decode（推理性能关键）
- 并行策略：TP/PP/DP/EP（Dense vs MoE 的差异）
- 量化：INT8/INT4、KV cache 量化
- 推理引擎：vLLM/TensorRT-LLM
