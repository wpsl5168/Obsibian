---
title: 用数据库类比理解 MoE vs Dense（SQL Server vs TiDB）
updated_at: 2026-03-31
---

# 适用人群
- 主要做数据库/后端/平台，熟悉 **SQL Server（集中式）**，了解 **TiDB（分布式）**
- 想用“系统工程直觉”理解大模型里 **Dense vs MoE**，而不是从数学公式入手

---

# 0) 大模型最基本原理（一句话）
LLM 就是一个“超级自动补全器”：输入一段文字，模型不断预测下一个 token。

模型内部你可以粗略记两块：
- **Attention**：像在上下文里“查资料/找关联”
- **FFN/MLP**：像把信息“加工变换”的计算单元（MoE 通常就是替换这块）

---

# 1) 一张对照表（核心映射）

| 大模型概念 | Dense（稠密） | MoE（专家混合） | 数据库类比 |
|---|---|---|---|
| 整体形态 | 一套网络所有 token 都走 | 每 token 只走 top-k 专家 | SQL Server vs TiDB |
| Router/Gate | 无（或很弱） | 关键组件（决定去哪些专家） | TiDB SQL 层/协调者 + 路由 |
| Experts | 无 | 多个专家 FFN | TiKV 节点 / Region / 分片 |
| 通信 | 相对简单（并行主要为算力拆分） | All-to-All/重排开销明显 | 分布式 scatter-gather / shuffle |
| 主要风险 | 单体变大带来的成本 | 热点、尾延迟、负载均衡、训练稳定 | 热点分片、慢节点、网络抖动 |

一句话：
- **Dense 更像“单库引擎思路”**：路径统一、稳定、省心。
- **MoE 更像“分布式系统思路”**：容量/性价比潜力大，但复杂度更高。

> 校准一句：Dense 也常常多机多卡部署（像 AlwaysOn/读写分离/集群），但它更像“逻辑上单引擎”；MoE 则“逻辑上就需要路由到不同子系统”。

---

# 2) 关键词解释（用数据库语言翻译）

## 2.1 总参数 vs 激活参数
- **总参数（Total params）**：MoE 所有专家权重加起来（像“集群总数据量/总索引量”）
- **激活参数（Active params）**：一次请求/一个 token 实际命中的专家参数（像“一条 SQL 实际触达的 region 数据量”）

所以会出现：MoE “总量很大”，但单次计算量不一定按总量线性增长。

## 2.2 热点分片 / 热点专家
- **热点分片（DB）**：请求集中打到少数 region/store
- **热点专家（MoE）**：token 集中被路由到少数专家

现象：吞吐下降、排队增加、p95/p99 飙升。

## 2.3 尾延迟（p95/p99）
MoE 像分布式查询：总体耗时≈“最慢那个分片/专家 + 通信/聚合”。
任一环节抖动就会把 p99 拉高。

## 2.4 负载均衡（load balancing）
MoE 需要同时做到两件事：
1) 选“更擅长”的专家（质量）
2) 避免专家过载（系统稳定/吞吐）

这类似 TiDB 的热点调度 / region balance：既要正确，又要均衡。

---

# 3) 一条 SQL 在 TiDB 里的执行流程（拆解 → 下推 → 局部聚合 → 汇总）

以典型 Join + Group By + TopN 为例：

```sql
SELECT u.city, COUNT(*) AS cnt, SUM(o.amount) AS gmv
FROM orders o
JOIN users u ON o.user_id = u.user_id
WHERE o.created_at >= NOW() - INTERVAL 7 DAY
GROUP BY u.city
ORDER BY gmv DESC
LIMIT 10;
```

## 3.1 数据流图（TiDB 视角）

```
Client
  |
  v
SQL Layer / Coordinator
  - parse / optimize
  - decide shards
  |
  | scatter tasks (by region)
  v
TiKV shardA   TiKV shardB   TiKV shardC  ...
  |              |             |
  | pushdown: filter/scan/proj/partial agg
  v              v             v
partial results (city -> partial_cnt, partial_sum)
   \             |            /
    \            |           /
     v           v          v
SQL Layer / Coordinator
  - gather
  - final aggregation (merge partials)
  - order by + limit (TopN)
  |
  v
Result
```

## 3.2 每一步对应到 MoE（一层 MoE 的数据流）
你可以把“一层 MoE”理解成一次小型的 scatter-gather：

- Coordinator 选 region  → **Router 选专家**
- scatter tasks          → **dispatch tokens**
- TiKV 做局部计算        → **专家 FFN 本地计算**
- gather + final agg      → **合并专家输出（加权求和）**

---

# 4) MoE 为什么理论省 FLOPs，但线上未必更快？（对应 DB 的真实痛点）
- 理论：只算 top-k 专家 ⇒ 计算量更省
- 现实：
  - dispatch/重排/All-to-All（像分布式 shuffle）
  - 热点专家（像热点 region）
  - 小 batch/低并发时通信开销占比更大

所以：
- **低并发/强 SLA（p99）在线场景**：Dense 往往更稳
- **高吞吐/可摊薄通信成本**：MoE 更有潜力

---

# 5) 选型建议（用一句话落地）
- 要“SQL Server 那种省心/延迟稳/生态成熟” → **Dense**
- 要“TiDB 那种容量/性价比/吞吐潜力”，并且能搞定分布式工程 → **MoE**
