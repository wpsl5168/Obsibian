---
title: README
created: 2026-04-23
updated: 2026-04-23
type: meta
tags: [pi-rover]
status: stable
---
# Pi-Rover 知识库

> 项目：树莓派Agent级智能小车
> 核心问题：操作系统选什么？大脑放哪里？整体架构怎么搭？
> 维护人：小虾 · 决策人：老王

## 目录

```
docs/kb/
├── 01-architecture-patterns/   ← 当前焦点：架构模式系统分析
│   ├── 00-overview.md           8种模式总览+对比矩阵
│   ├── 01-pure-cloud.md         纯云端：所有大脑在云
│   ├── 02-pure-local.md         纯本地：完全离线
│   ├── 03-hybrid-brain.md       混合脑：本地+云端协作 ★推荐
│   ├── 04-hierarchical.md       分层反射：L0-L4分层
│   ├── 05-behavior-tree-llm.md  行为树+LLM：BT做骨架
│   ├── 06-ros2-agent.md         ROS 2 + Agent：工业派
│   ├── 07-multi-agent.md        多Agent协作：感知/决策/执行分离
│   ├── 08-federated-swarm.md    集群联邦：多车协同
│   └── 99-decision-matrix.md    选型决策矩阵
├── 02-hardware/                 (待填充)
├── 03-software-stack/           (待填充)
├── 04-case-studies/             (待填充)
└── 05-decisions/                (待填充)
```

## 阅读顺序建议

1. **先看** `01-architecture-patterns/00-overview.md` 拿全景图
2. **重点读** `03-hybrid-brain.md` + `04-hierarchical.md`（这两个会融合成最终方案）
3. **拍板用** `99-decision-matrix.md` 做最终选择
4. **避坑用** `01/02-pure-*.md` 看两个极端的优劣

## 信息源

- Arm官方Pi 5边缘LLM学习路径
- Hailo-8L AI HAT+ 实测数据 (byteiota 2025)
- ROS 2 Jazzy官方文档
- BehaviorTree.CPP集成指南
- LinkedIn: OpenClaw混合架构案例
- Reddit r/AI_Agents: 实际部署经验

## 核心结论预告

> **混合脑 + 分层反射** 的复合架构最适合本项目。
> 即 03 + 04 的融合：L0安全反射 + L1路由器 + L2本地脑 + L3云端脑 + L4执行层。
> 详见 `99-decision-matrix.md`。
