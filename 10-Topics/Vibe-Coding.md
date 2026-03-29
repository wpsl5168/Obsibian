# Vibe Coding（话题页）

> 目标：用 Claude Code 为主线，系统梳理“vibe coding（氛围编程）”的工作方式、边界、最佳实践，以及它与传统开发（尤其企业软件/银行系统）的差异。

## 定义（工作口径）
- 不是“随便写”，而是：
  - 人用自然语言描述目标/约束
  - Agent 在受控环境里读代码、改文件、跑命令、提交变更
  - 人负责把控方向、验收质量与风险

## 为什么你会关心（结合你的背景）
- 银行业系统的特点：强合规、强审计、强稳定、长生命周期、复杂集成。
- vibe coding 的价值点往往在：
  - 读旧系统、定位问题、生成改动建议
  - 自动化脚手架与重复性改造
  - 快速做 PoC / 原型验证
- 风险点往往在：
  - prompt injection（把“内容”当“指令”）
  - 变更不可解释、不可回放、不可审计
  - 依赖与环境差异导致“看似能跑，实际不可部署”

## 官方渠道（一手）
- Claude Code overview：<https://code.claude.com/docs/en/overview>
- Claude Code Changelog：<https://code.claude.com/docs/en/changelog>
- Best Practices：<https://code.claude.com/docs/en/best-practices>
- Checkpointing：<https://code.claude.com/docs/en/checkpointing>
- Explore .claude directory：<https://code.claude.com/docs/en/claude-directory>

## 与传统开发对比（建议的评估维度）
- 交付速度：从需求到 PR 的时间
- 可控性：审批点、权限、可回滚
- 可观测：tracing / 日志 / 失败可复现
- 质量保障：测试、review、静态分析、evals
- 合规：数据访问边界、敏感信息处理、审计记录

## 后续我会怎么写这个话题
- 形成一条“技术演变史”主线：从 Copilot 到 coding agent 到 MCP/协议化工具，到工作流/审批/审计
- 每次日报只写增量；这里沉淀结构化结论与最佳实践
