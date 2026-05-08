---
title: Session Storage Unification
created: 2026-05-08
updated: 2026-05-08
type: meta
tags:
  - 项目/海马体
  - 架构
---

     1|# Session 存储统一方案 v1（已落地）
     2|
     3|**状态**: ✅ 已实施 2026-05-08
     4|**作者**: 小虾
     5|**关联**: hermes-agent fork (wpsl5168/hermes-agent), OpenHippo v0.4
     6|
     7|## 背景
     8|
     9|Hermes 历史 session 数据原本分散：
    10|- `~/.hermes/state.db`：原始 messages、title、summary 列（部分填充）
    11|- `session_search` 工具：直接查 state.db，必要时现场跑 LLM 生成摘要 → **慢、不语义、与 memory 检索两套体系**
    12|
    13|OpenHippo 已经是 memory + chat_log + skills 的统一向量后端，session summary 也应进同一空间。
    14|
    15|## 设计
    16|
    17|### 数据流
    18|
    19|```
    20|┌─────────────────────────────────────────────────────────────┐
    21|│ session 运行中                                              │
    22|│   messages → state.db (sessions, messages 表)               │
    23|│   end_session() 写 ended_at（upstream 行为，不动）          │
    24|└──────────────────────┬──────────────────────────────────────┘
    25|                       │
    26|                       ▼ 每 5 分钟 systemd timer
    27|┌─────────────────────────────────────────────────────────────┐
    28|│ session_summary_backfill.py --ended-only --needs-summary-only │
    29|│   1. SELECT id FROM sessions WHERE ended_at IS NOT NULL     │
    30|│        AND (summary IS NULL OR summary='')                  │
    31|│   2. concat messages → LLM (auxiliary task, copilot)        │
    32|│   3. UPDATE sessions SET summary, title                     │
    33|│   4. POST /v1/cold/memories                                 │
    34|│        source=session_summary, session_id=<id>              │
    35|└──────────────────────┬──────────────────────────────────────┘
    36|                       ▼
    37|┌─────────────────────────────────────────────────────────────┐
    38|│ OpenHippo cold tier (~/.hippocampus/memory.db)              │
    39|│   会被 vec 索引器自动 embed                                 │
    40|└──────────────────────┬──────────────────────────────────────┘
    41|                       ▼
    42|┌─────────────────────────────────────────────────────────────┐
    43|│ session_search 工具（fork 注入）                            │
    44|│   - 有 query：POST /v1/memories/search → 返 hot+cold        │
    45|│   - 无 query：state.db ORDER BY started_at DESC（最近列表） │
    46|└─────────────────────────────────────────────────────────────┘
    47|```
    48|
    49|### 关键决策
    50|
    51|| 项 | 决策 | 理由 |
    52||----|------|------|
    53|| 触发方式 | systemd --user timer 5min | 不改 upstream 的 end_session/run_agent，merge 干净 |
    54|| 实时性 | ≤5 分钟延迟 | 对 search 场景足够；live session 不污染索引 |
    55|| 单 tick 上限 | 20 sessions | concurrency=5 时 wall time ~60s，绝不卡 |
    56|| 幂等 | `--needs-summary-only` SQL 过滤 + `_already_in_hippo` 双层 | 重复跑不会重写 |
    57|| source 标识 | `session_summary` | 与 chat_log（原始消息）区分 |
    58|| namespace | 默认 namespace（agent scope） | 与 memory 共享检索；session_id 字段做关联 |
    59|
    60|### 文件清单
    61|
    62|```
    63|~/.hermes/hermes-agent/
    64|├── tools/session_summary_backfill.py   # +2 flag (ended-only, needs-summary-only)
    65|├── tools/session_search_tool.py        # fork 注入：先查 hippo，state.db fallback
    66|└── FORK.md                             # 改动登记
    67|
    68|~/.config/systemd/user/
    69|├── hermes-session-summary.service      # oneshot, 调上面那条命令
    70|└── hermes-session-summary.timer        # OnUnitActiveSec=5min
    71|
    72|~/.hermes/logs/
    73|└── session-summary-backfill.log        # 运行日志
    74|```
    75|
    76|## 验证
    77|
    78|✅ 首批 20 条已回填，平均 ~6.8s/session（含 copilot LLM 生成）
    79|✅ `/v1/memories/all?source=session_summary` 能列出
    80|✅ `/v1/memories/search` 能命中（hot+cold）
    81|✅ Timer 启用，下次 5 分钟后自动跑
    82|✅ live session（ended_at IS NULL）不被处理
    83|
    84|## 后续
    85|
    86|- [ ] 跑满全部 493 条候选（约需 25 个 tick = ~2 小时）
    87|- [ ] 观察 1 周，看是否有 session 卡在"已结束但永远不被回填"
    88|- [ ] 评估是否给 BadCase / 用户高频检索的 session 单独标 priority
    89|- [ ] OpenHippo 增加 `session_id` 维度的检索 filter（目前只能 source filter）
    90|
    91|## 回滚
    92|
    93|```bash
    94|systemctl --user disable --now hermes-session-summary.timer
    95|rm ~/.config/systemd/user/hermes-session-summary.{service,timer}
    96|cd ~/.hermes/hermes-agent && git checkout tools/session_summary_backfill.py tools/session_search_tool.py
    97|rm FORK.md
    98|```
    99|
   100|state.db 数据不动，hippo 里的 `source=session_summary` 数据可保留（无害）或删：
   101|```bash
   102|curl -X DELETE 'http://localhost:8200/v1/memories/remove?source=session_summary'
   103|```
   104|