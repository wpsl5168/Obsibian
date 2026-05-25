# 50-日报与动态

**定位**: 所有自动/手动生成的"日频/周频"动态。

**子目录**:
- `AI日报/` — AI Daily(原 01-新闻速递)
- `DeepLearning.AI/snapshots/` — DLAI 课程快照(JSON)
- `DeepLearning.AI/digests/` — DLAI 日摘要
- `DeepLearning.AI/updates/` — DLAI 增量更新

**自动清理规则**(每周一周报扫描时执行):
- 超过 **2 周** 的 daily(`YYYY-MM-DD-*.md`、`*-daily.md`、`courses-*.json`)归档到 `.trash/archive-YYYY-MM-DD/`
- 周报(`YYYY-WXX.md`)保留,不清理

**典型生成源**: cron(daily-brief、blogwatcher)、手动整理。
