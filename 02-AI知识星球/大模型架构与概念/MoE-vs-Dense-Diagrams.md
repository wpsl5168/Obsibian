---
title: Dense vs MoE 图解（数据库执行流 & MoE 路由流）
updated_at: 2026-03-31
---

# 1) TiDB 类分布式 SQL：拆解 → 下推 → 局部聚合 → 汇总

```
(1) Client
    |
    |  SQL: JOIN + WHERE + GROUP BY + ORDER BY + LIMIT
    v
+------------------------+
| SQL Layer / Coordinator|
|  - Parse / Optimize    |
|  - Decide shards       |
|  - Build exec plan     |
+-----------+------------+
            |
            |  (2) Scatter tasks by shard/region
            v
   +--------+--------+--------+--------+
   |                 |                 |
   v                 v                 v
+--------+       +--------+       +--------+
| TiKV   |       | TiKV   |       | TiKV   |   ... (many nodes)
| shardA |       | shardB |       | shardC |
+---+----+       +---+----+       +---+----+
    |                |                |
    | (3) Pushdown:  | (3) Pushdown:  | (3) Pushdown:
    |  filter/scan   |  filter/scan   |  filter/scan
    |  partial agg   |  partial agg   |  partial agg
    v                v                v
  partial           partial          partial
 results            results          results
 (city->cnt,sum)    (city->cnt,sum)  (city->cnt,sum)
    \                |                /
     \               |               /
      \              |              /
       \             |             /
        v            v            v
     +------------------------------+
     | Coordinator / SQL Layer      |
     | (4) Gather + Merge           |
     |  - Final GROUP BY aggregation|
     |  - ORDER BY gmv DESC         |
     |  - LIMIT 10 (TopN)           |
     +---------------+--------------+
                     |
                     v
               (5) Result rows
```

---

# 2) MoE（单层）：路由 → 分发 → 专家计算 → 聚合

```
 token hidden states (batch of tokens)
            |
            v
     +----------------+
     | Router / Gate  |   (像 TiDB 的路由层)
     | score each exp |
     +-------+--------+
             |
             | choose top-k experts per token
             v
      (scatter / dispatch tokens)
     +----+----+----+----+----+
     |    |    |    |    |    |
     v    v    v    v    v    v
  +----+ +----+ +----+ +----+ +----+
  |E1  | |E2  | |E3  | |E4  | |E5  |  ... many experts
  |FFN | |FFN | |FFN | |FFN | |FFN |
  +--+-+ +--+-+ +--+-+ +--+-+ +--+-+
     |      |      |      |      |
     |  (each expert computes only its tokens)
     v      v      v      v      v
   out1   out2   out3   out4   out5
     \      |      |      |     /
      \     |      |      |    /
       v    v      v      v   v
     +--------------------------+
     | Gather + Combine         |  (像 SQL 层汇总聚合)
     | weighted sum by gate     |
     +------------+-------------+
                  |
                  v
        output hidden states (to next layer)
```
