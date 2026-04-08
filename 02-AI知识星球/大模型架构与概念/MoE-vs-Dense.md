---
title: MoE vs Dense：大模型架构差异、演化史、参数与性能比较
updated_at: 2026-03-31
---

# 一句话结论
- **Dense（稠密）模型**：每个 token 都会“用到全部（或几乎全部）参数”，**训练/推理实现简单、稳定**，但**算力成本随参数线性增长**。
- **MoE（Mixture-of-Experts，专家混合/稀疏激活）模型**：每个 token 只激活少数几个专家（例如 top-1 / top-2），所以能做到 **“总参数很大，但每 token 计算量接近小模型”**；代价是 **路由/通信/负载均衡/稳定性/工程复杂度**显著上升。

---

# 1) Dense 与 MoE 的核心差异（从计算图角度）

## 1.1 Dense（稠密）Transformer（典型）
对任意输入 token：
- Attention 层：计算 Q/K/V、注意力、输出投影（对所有 token 共享同一套权重）
- FFN/MLP 层：同一套 MLP 权重对所有 token 生效

**特点**：
- 每个 token 都会走同样的层与权重 ⇒ **每 token 激活参数≈总参数（同一层权重全部参与计算）**
- 训练稳定、并行模式成熟（DP/TP/PP）
- 模型变大 ⇒ **FLOPs/token 基本随参数线性增加**

## 1.2 MoE（稀疏专家）Transformer（典型：把 FFN 替换为 MoE-FFN）
对任意输入 token：
1) Router/Gate（路由器）先根据 token 表征算一组分数
2) 选择 top-k 个专家（k 很小，比如 1 或 2）
3) 只对选中的专家 FFN 做前向（其余专家不算）
4) 将专家输出按 gate 权重合并

**特点**：
- **总参数（Total params）很大**：有很多专家，每个专家是一套独立 FFN
- **激活参数（Active params / per-token params）较小**：每 token 只用 k 个专家
- 但要付出：
  - token 需要按专家“分桶/重排/All-to-All 通信”（专家并行）
  - 需要 load balancing（负载均衡）避免少数专家过载
  - 训练更容易出现不稳定（路由崩塌、专家失活等）

---

# 2) 什么是「参数」（以及 MoE 为什么会让“参数”概念变复杂）

## 2.1 参数（Parameters）
在神经网络里，“参数”通常指 **可学习的权重**（weights/biases），例如：
- token embedding 矩阵
- Attention 的 Wq/Wk/Wv/Wo
- FFN 的 W1/W2（以及可能的门控/激活相关矩阵）
- LayerNorm 的缩放/偏置（如果可学习）

> 直觉：参数是模型“存储知识/能力”的载体；训练就是在数据上优化这些参数。

## 2.2 Dense vs MoE 下参数的两个口径
MoE 场景里经常同时谈两个指标：
- **总参数（Total Parameters）**：把所有专家的参数都算上（非常大）
- **激活参数（Active Parameters）**：每个 token 实际参与计算的那部分参数（小很多）

因此出现一个常见现象：
- MoE 宣称“几百 B / 1T 参数”，但每 token 的 FLOPs/token 接近一个更小的 dense 模型。

---

# 3) 性能比较：该怎么比才公平？

对比 Dense vs MoE，至少要把指标拆开：

## 3.1 质量（Quality）
- 困惑度（Perplexity）、下游任务指标（MMLU、MGSM、HumanEval…）
- 对齐/安全性（RLHF 后的表现）

**经验**：在相同训练算力预算下，MoE 往往能用更高的“容量（total params）”换取更好的质量；但增益依赖路由与训练稳定性。

## 3.2 推理算力与吞吐（Compute / Throughput）
- **FLOPs/token**（或等价的计算量）
- tokens/s（吞吐）
- 真实延迟（p50/p95 latency）

**经验**：
- MoE 的 **理论 FLOPs/token** 很划算（只算 top-k 专家）
- 但 **真实延迟**未必更低：All-to-All、kernel 启动、路由开销、batch 太小等都会抵消优势

## 3.3 显存/内存（Memory）
- Dense：显存大多随参数增长（权重常驻）
- MoE：
  - 总权重更大 ⇒ **权重常驻的压力更大**（尤其是专家多）
  - 但每 token 激活参数少 ⇒ activation 可能更小
  - 工程上常见：需要更复杂的并行/分片/缓存策略

## 3.4 成本（Cost）
- 训练成本：MoE 可能以更低的 FLOPs 获得更高质量，但工程投入更大
- 部署成本：MoE 权重总量大，可能增加加载时间、冷启动、弹性伸缩复杂度

---

# 4) MoE 的主要收益与主要坑

## 4.1 主要收益
1) **条件计算（Conditional Computation）**：每个 token 用不同子网络，提升容量
2) **更好的“质量/算力比”潜力**：在给定 FLOPs/token 下做更大容量
3) **专家分工**：不同专家可能专注不同模式/领域（并非总能自动出现，但常见）

## 4.2 主要坑（工程与训练）
1) **负载不均（load imbalance）**：少数专家被大量 token 选择 ⇒ 变慢/溢出
2) **路由不稳定（routing collapse）**：训练早期或不当正则导致专家失活
3) **通信成本高**：All-to-All 是大头，集群网络与拓扑很关键
4) **小 batch / 低并发推理困难**：batch 小时路由重排开销占比更大
5) **推理服务复杂**：权重更大、分片更多、热身与缓存策略更复杂

---

# 5) 演化历史（里程碑时间线）

> 这里列“MoE 在大模型/Transformer 规模化”脉络；更早期 MoE（90 年代）属于传统 NN 时代的混合专家思想。

- **2017 — Sparsely-Gated MoE**：提出稀疏门控 MoE 层，强调“容量↑↑，计算近似不变”的条件计算。
  - 论文：*Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer* (arXiv:1701.06538)
  - https://arxiv.org/abs/1701.06538

- **2020 — GShard**：把“条件计算 + 自动分片/编译器支持”体系化，展示超大 MoE（600B+）在大规模 TPU 上训练可行。
  - 论文：*Scaling Giant Models with Conditional Computation and Automatic Sharding* (arXiv:2006.16668)
  - https://arxiv.org/abs/2006.16668

- **2021/2022 — Switch Transformer**：把路由简化为 Switch（常见 top-1），重点解决 MoE 的复杂度/通信成本/稳定性问题，并推动到“trillion 参数级”。
  - 论文：*Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity* (arXiv:2101.03961)
  - https://arxiv.org/abs/2101.03961

- **2021/2022 — GLaM（MoE LLM）**：代表性 MoE 大语言模型工作，强调在训练效率与质量上的收益。
  - 论文：*Efficient Scaling of Language Models with Mixture-of-Experts* (arXiv:2112.06905)
  - https://arxiv.org/abs/2112.06905

- **2023~2024（工程落地阶段）**：MoE 思路被更多开源/工业模型采用（典型做法：在 Transformer 的 FFN 用 MoE，推理用高效专家并行）。
  - 这一阶段常见关键词：更稳定的路由、更好的 load balancing、专家并行优化、推理低延迟化。

---

# 6) Dense vs MoE：典型选型建议

## 6.1 什么时候选 Dense
- 你更在意：**工程简单、稳定、可预测的延迟**
- 部署场景：低并发/小 batch，或者对 p95 延迟极敏感
- 你希望复用成熟生态（量化、KV cache、推理引擎）并减少通信复杂度

## 6.2 什么时候选 MoE
- 你更在意：**训练阶段的质量/算力比**，并且有能力做大规模并行与通信优化
- 推理场景：高吞吐（大 batch/高并发），能摊薄路由/通信开销
- 你希望在“相对可控的 FLOPs/token”下提升容量/知识量

---

# 7) 常见误区澄清
- **“MoE 一定比 Dense 快”**：不一定。理论 FLOPs 少，但通信/重排/小 batch 可能拖慢。
- **“MoE 参数更多就一定更强”**：不一定。路由、数据、训练稳定性决定是否把容量转化为质量。
- **“参数=算力”**：Dense 更接近；MoE 需要区分 total vs active params。

---

# 8) 你如果要更“量化”的性能对比
给我你关心的具体场景，我可以按这个模板帮你对比（并补上估算公式/数据口径）：
- 目标：离线推理（批量）还是在线服务（低延迟）？
- 模型规模：大概是 7B/70B/百 B/万亿？
- 硬件：A100/H100/TPU？网络带宽？
- 主要指标：tokens/s、p95 延迟、$ / 1M tokens、质量指标（MMLU/业务指标）
