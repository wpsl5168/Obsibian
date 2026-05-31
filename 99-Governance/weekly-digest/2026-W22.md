---
title: "周报 2026-W22"
date: 2026-05-31
tags: [weekly, dreaming, governance]
---

# 周报 2026-W22 (Dream A 自主维护)

## 健康概览
- **Memory**: MEMORY.md 2568/4400 (58%) ✓ / USER.md 2437/2750 (**89%**) ⚠️ 接近上限
- **Cold memory (state.db)**: 14 条 / 3007 字符 ✓
- **Cron**: 全部 last_status=ok (15+ jobs);Dream A/B、wiki_lint、proginn 系列、丰台学区监控、AI简报、小贝周整理均健康
- **Skills**: 224 个,分类稳定,无新增孤儿

## 记忆变更
- 本轮未做清理(MEMORY.md 内容均为高频引用、USER.md 89% 但每条都活跃,保守不删)
- 建议:下次满 90% 时考虑把"GitHub PAT/gh 细节"(USER L9) demote 到 cold,日常少用

## 健康告警
- **P2** USER.md 占用 89%,逼近 2750 上限,再加 1 条容易静默溢出 (Pitfall #17)
- **P2** Hermes状态备份 cron 的微信投递偶发 rate limited (ret=-2),不影响备份本身,可考虑改邮件或延后档期
- **P0/P1** 无

## 近期 session 关键决策 (2026-05-25 ~ 05-31)
- 5-30 老王明确:cron auto-fix `git add -A` 会带 untracked 噪音,改用精确 `git add <file>` (写入 dreaming skill #36)
- 5-28 Dream A/B 报错铁律入库:出错当场修禁拖,先查 dream_runs + agent.log + cron list 三件套
- 5-28 输出极简协议正式入 skill:简报 ≤600 字符,无新动态=[SILENT]
- 5-27 纯工具/解析器文件 4 项检查模板入 skill #33
- 5-26 HTTP/LLM provider wrapper 的 5 项 P1 清单入 skill #32

## 下周关注
- USER.md 占用持续上升时主动 demote
- BrickHub: Dream B rotation 继续扫 `components/home/` 残余文件
- 微信投递 rate limit 频率,如成常态考虑分散 cron 时段
