---
title: "10-Best-Practices-Extract"
date: 2026-04-08
category: Notes
tags: [daily]
---

# Claude Code Best Practices（摘录 + 落地解读）

来源（官方）：<https://code.claude.com/docs/en/best-practices>

## 我提炼的 3 条“最值钱”原则
1) **给它一个自证方式（verify）**：测试/脚本/截图/预期输出。
2) **先探索再计划再实现**：用 Plan Mode 把“读代码”和“改代码”分开。
3) **把 context window 当资源管理**：长会话会退化，必要时 summarize/compact。

## 落地写法（你可以直接复制粘贴给 Claude Code）
- 让它自证：
  - “实现 X。完成后运行 `...`，把输出贴出来。如果失败，继续修到通过。”
- 强制先计划：
  - “先进入 Plan Mode：读 `...`，给出改动方案（文件列表+理由），我确认后再改。”

## 风险提醒
- Claude 很强，但只要没有“可验证的成功标准”，它就容易写出看似合理但不可用的代码。
