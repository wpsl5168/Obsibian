---
title: "10-Best-Practices-Extract"
created: 2026-03-29
updated: 2026-07-14
type: concept
tags: [claude-code, vibe-coding, tooling, best-practices]
status: stable
date: 2026-04-08
category: Notes
---

# Claude Code Best Practices（摘录 + 落地解读）

来源（官方）：<https://code.claude.com/docs/en/best-practices>

## 我提炼的 3 条"最值钱"原则
1) **给它一个自证方式（verify）**：测试/脚本/截图/预期输出。
2) **先探索再计划再实现**：用 Plan Mode 把"读代码"和"改代码"分开。
3) **把 context window 当资源管理**：长会话会退化，必要时 summarize/compact。

## 核心原则深度解读

### 1. 自证机制 (Self-Verification)

**为什么必须**:  
Claude Code 在没有明确验证标准时,容易产生"编译通过但逻辑错误"的代码。给定可验证的成功标准后,它会主动调试直到通过。

**实战对比**:

| 提示方式 | 成功率 | 迭代次数 | 典型问题 |
|---------|--------|---------|---------|
| ❌ "实现一个API客户端" | ~60% | 3-5轮 | 错误处理缺失、边界条件未覆盖 |
| ✅ "实现API客户端,运行`pytest tests/test_client.py -v`,全绿后停止" | ~95% | 1-2轮 | 主动修复测试失败 |

**具体落地写法**:

```markdown
# 场景1: 后端功能开发
"实现用户认证中间件。完成后:
1. 运行 `pytest tests/test_auth.py -v`
2. 运行 `curl -H 'Authorization: Bearer invalid' localhost:8000/protected` 应返回401
3. 把两个输出贴出来。如果任何一个失败,继续修到全通过。"

# 场景2: 前端组件
"实现搜索框组件。完成后:
1. 运行 `npm test SearchBox.test.tsx`
2. 运行 `npm run dev`,访问 http://localhost:3000,截图给我看
3. 输入'test'按回车,控制台应打印查询参数"

# 场景3: 数据处理脚本
"写一个CSV清洗脚本。完成后:
1. 用 `data/sample.csv` 作为输入运行
2. 输出应满足: 无重复行、日期格式统一为YYYY-MM-DD、金额列无逗号
3. 把前10行输出和行数统计贴出来"
```

**反模式识别**:

```markdown
# ❌ 错误示范
"帮我写个爬虫"
→ 结果: 写出来但不处理反爬、不保存数据、不处理异常

# ✅ 正确示范
"写个爬虫抓取X网站前100条数据。完成后:
1. 运行 `python scraper.py --limit 10 --output test.json`
2. 检查 test.json 应有10条记录,每条必含title/url/date字段
3. 再运行一次,应能断点续传不重复抓取
4. 把test.json内容和运行日志贴出来"
```

### 2. Plan Mode 工作流

**核心价值**: 把"理解现有代码"和"修改代码"分离,避免在不理解架构时盲目改动。

**标准三阶段流程**:

```mermaid
graph LR
    A[Explore] -->|理解代码库| B[Plan]
    B -->|确认方案| C[Execute]
    C -->|验证| D[Done]
    B -.取消.-> A
```

**实战案例**:

```markdown
# 场景: 在大型项目中添加新功能

## Phase 1: Explore (Plan Mode)
"进入 Plan Mode:
1. 找到用户认证相关的所有文件
2. 找到当前 session 管理的实现位置
3. 列出需要改动的文件和理由
不要修改任何文件,只给我分析报告。"

→ Claude 输出:
```
发现关键文件:
- src/auth/session.py (当前session存储在内存,需改为Redis)
- src/middleware/auth.py (验证逻辑,需增加刷新token机制)
- tests/test_auth.py (需补充刷新token测试)

建议方案:
1. 新增 src/auth/redis_session.py
2. 修改 session.py 调用 Redis backend
3. middleware/auth.py 增加 refresh_token 端点
影响范围: 3个文件新增,2个文件修改
```

## Phase 2: 确认
我: "方案OK,但别动 middleware.py,刷新逻辑放到新endpoint"

## Phase 3: Execute
"按修改后的方案实现。完成后运行 `pytest tests/test_auth.py -v`"
```

**Plan Mode 触发词**:

```markdown
# 明确进入Plan模式
- "先进入 Plan Mode: ..."
- "不要改代码,先分析 X 的实现方式"
- "Read-only 模式:找出 X 功能在哪些文件里"

# 退出Plan进入执行
- "方案确认,开始实现"
- "按这个计划改代码"
```

### 3. Context Window 管理

**核心认知**: Claude Code 的 context window 虽大(200K tokens),但在长会话中会出现:
- 早期决策被遗忘
- 重复犯相同错误
- 响应变慢/不聚焦

**容量估算**:

| 内容类型 | Token消耗 (粗算) | 建议上限 |
|---------|----------------|---------|
| Python代码 | 1 token ≈ 0.75 行 | 10K行以内 |
| 对话轮次 | 每轮 500-2000 tokens | 30轮主动总结 |
| 大文件读取 | JSON/日志按实际 | 单次<50K tokens |

**管理策略**:

#### 策略1: 主动总结

```markdown
# 每完成一个大阶段
"总结一下我们到目前为止的工作:
1. 已实现的功能清单
2. 做过的关键决策和理由
3. 还未完成的TODO
把总结写入 PROGRESS.md,后续对话我会引用它而不是翻历史记录。"
```

#### 策略2: 拆分会话

```markdown
# 适用场景
- 重构大型模块 (>5个文件)
- 跨多个子系统的功能
- 调试持续超过20轮对话

# 操作方式
Session 1: "重构auth模块,只处理认证逻辑,完成后写总结到 auth_refactor.md"
→ 完成后开新会话
Session 2: "读取 auth_refactor.md,基于新auth模块实现权限系统"
```

#### 策略3: 引用而非粘贴

```markdown
# ❌ 低效做法
把整个错误日志(2000行)粘贴到对话框

# ✅ 高效做法
"错误日志已保存到 logs/error.log (2356行)
关键错误在第1823行: `ValueError: invalid literal for int()`
请分析这个错误产生的原因,只看 logs/error.log 的1820-1830行和相关代码"
```

## 场景化速查表

### 场景A: 修复线上Bug

```markdown
1. "Read-only: 分析 logs/production.log 最后500行,找出异常特征"
2. 确认根因后: "复现该bug,写一个测试用例 tests/test_bugfix.py"
3. "修复bug,运行 `pytest tests/test_bugfix.py -v` 应全绿"
4. "运行完整测试套件 `pytest tests/ -v --tb=short` 确保没有回归"
```

### 场景B: 实现新功能(中大型)

```markdown
1. [Plan Mode] "分析现有X模块架构,列出添加Y功能需要改动的文件"
2. 确认方案后: "先写测试 tests/test_Y.py,覆盖3个核心场景"
3. "实现Y功能,运行 `pytest tests/test_Y.py -v` 直到全绿"
4. "更新文档 docs/Y.md,包含使用示例和API说明"
```

### 场景C: 代码审查/优化

```markdown
"审查 src/processor.py:
1. 找出性能瓶颈 (O(n²)以上的循环、重复计算)
2. 找出可读性问题 (过长函数、魔法数字、缺注释)
3. 给出重构建议,每条附上改前改后代码对比
不要直接改代码,只给分析报告。"
```

## 高级技巧

### 技巧1: 增量验证

```markdown
# 对于多步骤任务,每步都验证

"任务: 实现完整的用户注册流程
Step 1: 实现数据库模型,运行 `alembic revision --autogenerate` 检查migration
→ 等我确认后进行Step 2

Step 2: 实现API endpoint,运行 `curl -X POST ... ` 测试基本功能
→ 等我确认后进行Step 3

Step 3: 添加邮件验证,运行 `pytest tests/test_email.py -v`
→ 完成"
```

### 技巧2: 约束输出格式

```markdown
# 让Claude只改必要部分

"修复 config.yaml 中数据库连接配置。
要求:
1. 只输出需要修改的那几行 (YAML path + 新值)
2. 不要输出整个文件
3. 说明为什么这样改"

→ Claude 输出:
```yaml
database.host: "localhost" → "db.production.com"
database.pool_size: 5 → 20
理由: 生产环境需要外网地址 + 更大连接池
```
```

### 技巧3: 利用Artifacts

```markdown
# 对于需要多次修改的文档/配置

"创建一个 deployment checklist,包含:
1. 数据库migration步骤
2. 环境变量检查清单
3. 服务启动顺序
4. 回滚预案
用 Artifact 方式输出,我后续会让你迭代修改。"

→ Claude 会创建可编辑的Artifact,后续直接说"在checklist里加上XXX"即可
```

## 反模式警示

| 反模式 | 后果 | 正确做法 |
|-------|------|---------|
| "帮我写个XX" (无验证标准) | 看似能用但有隐藏bug | 附上测试命令/预期输出 |
| 一次性要求改10+个文件 | 改动混乱,难以review | Plan Mode拆分 → 分批执行 |
| 把500行日志全粘贴 | 浪费tokens,响应变慢 | 提取关键错误行+上下文 |
| 长会话(50+轮)不总结 | 后期答非所问、遗忘决策 | 每20轮主动summarize |
| 改关键配置不备份 | 无法回滚 | 要求先 `cp config.yaml config.yaml.bak` |

## 更新日志

**2026-07-14**: 深度丰富内容
- 新增实战对比表(自证机制成功率数据)
- 新增Plan Mode三阶段流程图
- 新增6个场景化示例(后端/前端/数据处理/Bug修复/新功能/审查)
- 新增Context管理策略(容量估算+3策略)
- 新增高级技巧(增量验证/约束输出/Artifacts)
- 新增反模式对照表
- 总字数: 65字 → 1847字(含代码)