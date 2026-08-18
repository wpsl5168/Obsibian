---
title: PRD 五｜部署形式
created: 2026-04-21
updated: 2026-04-21
type: entity
tags: [openhippo]
status: draft
sources: [20-项目/海马体/项目需求文档(PRD).md]
---

# PRD 五｜部署形式

> 本页是 [[../项目需求文档(PRD)|海马体PRD]] 的分卷之一：**4种部署方式**
> 完整目录见 [[../项目需求文档(PRD)|PRD索引]]

---

## 五、部署形式

```bash
# 方式1: pip
pip install hippocampus && hippocampus serve

# 方式2: Docker
docker run -d -p 8200:8200 -v ~/.hippocampus:/data hippocampus/hippocampus:latest

# 方式3: 嵌入式
from hippocampus import MemoryEngine
engine = MemoryEngine(db_path="~/.hippocampus/memory.db")

# 方式4: Hook/Plugin接入（以Hermes Agent为例）
# 在Agent的plugin目录放置hook脚本，自动拦截对话并同步记忆
```

---


---

## 相关链接

- 上级索引：[[../项目需求文档(PRD)]]
- 项目主页：[[../项目需求文档(PRD)]]
- 知识库索引：[[../../../index]]
