---
title: Hermes 上下文管理优化方案
created: 2026-04-15
updated: 2026-09-09
type: research
tags: [hermes, research, architecture]
status: stable
---

# Hermes 上下文管理优化方案

> 撰写日期：2026-04-15
> 状态：方案评审中
> 分类：#AI-Agent #Hermes #性能优化

---

## 1. 背景与问题

[[20-项目/Hermes/README.md|Hermes Agent]] 在通过 Copilot provider 接入 Claude 模型时，存在严重的上下文空间不足问题，直接影响长对话场景下的任务执行质量。

### 1.1 现象描述

在实际使用中，对话进行到中期阶段时频繁触发上下文压缩（context compression），导致：

- 早期对话历史被丢弃，agent 丢失任务上下文
- 压缩后仅保留约 14.4K chars 的 tail 内容，信息损失严重
- 多步骤复杂任务（如代码重构、跨文件分析）的完成质量显著下降

### 1.2 核心数据

| 指标 | 当前值 | 说明 |
|------|--------|------|
| Copilot context_length | 144K chars | 远低于 Claude 原生 1M |
| 压缩触发阈值 | 72K chars (50%) | 144K × 0.50 |
| 系统提示固定开销 | ~36K chars | 占总容量的 25% |
| 有效工作空间 | ~36K chars | 72K - 36K 系统开销 |
| 压缩后 tail 保留 | ~14.4K chars | 144K × 0.10 |

**关键结论：有效工作空间仅约 36K chars，对于涉及文件读取、工具调用的复杂任务而言严重不足。**

---

## 2. 根因分析

### 2.1 上下文容量瓶颈

```
原生 Claude context:  1,000,000 chars (1M)
Copilot provider 限制:  144,000 chars (144K)
                        ↓ 压缩率 85.6%
```

Copilot provider 在初始化时将 `context_length` 硬编码为 144K，这是整个问题链的根本起点。Claude 原生支持 1M context window，但经过 Copilot 平台中转后，可用容量缩水至原来的 14.4%。

### 2.2 系统提示开销过大

`prompt_builder.py` 中 `_build_system_prompt()` 负责组装系统提示，其固定开销约 36K chars，组成如下：

| 组件 | 估算大小 | 说明 |
|------|----------|------|
| Persona 定义 | ~4K | agent 角色、行为规范 |
| Memory 上下文 | ~8K | 持久化记忆内容 |
| Skills Index | ~10K | 全量工具 schema 定义 |
| AGENTS.md | ~6K | 多 agent 协作配置 |
| 其他元数据 | ~8K | 时间、环境、约束条件等 |

系统提示占据了总容量的 25%，且在每次对话轮次中都会完整携带，属于不可压缩的固定成本。

### 2.3 压缩机制分析

`context_compressor.py` 中的核心参数：

- **`threshold_percent`**：控制压缩触发阈值，当前为 0.50，即消息总长度达到 `context_length × 0.50` 时触发压缩
- **`target_ratio`**：压缩目标比例，当前为 0.20，压缩后保留消息量为 `context_length × 0.20`
- **`protect_last_n`**：保护最近 N 轮对话不被压缩，当前为 20

压缩流程：
```
消息增长 → 达到 72K (144K × 0.50) → 触发压缩
→ 压缩目标: 28.8K (144K × 0.20)
→ 保护最近 20 轮 → 压缩/丢弃早期消息
→ 实际保留 tail: ~14.4K
```

### 2.4 问题链总结

```
Copilot 144K 限制
    ↓
系统提示固定占 36K (25%)
    ↓
有效工作空间仅 ~36K
    ↓
文件读取/工具输出快速填满空间
    ↓
频繁触发压缩，丢失关键上下文
    ↓
任务质量下降、重复工作
```

---

## 3. 短期优化方案（Config 调优）

**目标：不改动代码，通过调整配置参数优化上下文利用效率。**
**预计收益：有效工作空间从 ~36K 提升至 ~65K，提升约 80%。**

### 3.1 降低单次文件读取消耗

```yaml
# config.yaml
file_read_max_chars: 50000  # 原值: 100000
```

**原理：** 单次 `read_file` 操作最大返回 50K chars（原 100K），避免一次文件读取就吃掉大部分工作空间。对于大文件，agent 需要通过 `offset` 和 `limit` 参数分段读取。

**影响评估：** 绝大多数代码文件远小于 50K，实际影响极小。对于超大文件（如 minified JS、大型 JSON），强制分段读取反而有助于 agent 聚焦关键部分。

### 3.2 延后压缩触发点

```yaml
# config.yaml
compression:
  threshold_percent: 0.70  # 原值: 0.50
```

**原理：** 将压缩触发阈值从 50% 提升到 70%，即消息总量达到 `144K × 0.70 = 100.8K` 时才触发压缩。

**收益计算：**
```
压缩前可用空间: 100.8K - 36K(系统提示) = 64.8K
对比原方案:      72K - 36K(系统提示) = 36K
提升幅度:        +80%
```

**风险：** 触发压缩时距离上下文上限更近，留给压缩操作本身的余量减小。但 70% 仍有 30% 的缓冲空间（43.2K），足够安全。

### 3.3 提高压缩后保留量

```yaml
# config.yaml
compression:
  target_ratio: 0.25  # 原值: 0.20
```

**原理：** 压缩后保留 `144K × 0.25 = 36K` 的消息内容（原 28.8K），多保留约 7.2K 的历史上下文。

### 3.4 保持对话保护

```yaml
# config.yaml
compression:
  protect_last_n: 20  # 保持不变
```

**原理：** 最近 20 轮对话包含当前任务的关键上下文，保护策略维持不变。

### 3.5 短期方案汇总

| 参数 | 原值 | 新值 | 效果 |
|------|------|------|------|
| file_read_max_chars | 100K | 50K | 降低单次读取开销 50% |
| threshold_percent | 0.50 | 0.70 | 延后压缩，有效空间 +80% |
| target_ratio | 0.20 | 0.25 | 压缩后多保留 7.2K |
| protect_last_n | 20 | 20 | 不变 |

---

## 4. 中期优化方案（代码级改造）

**目标：通过代码修改，从工具调用、schema 加载、系统提示三个维度压缩上下文开销。**
**预计收益：系统提示开销从 36K 降至 ~20K，释放约 16K 有效空间。**

### 4.1 工具输出强制截断

**改造点：** `registry.dispatch()` 方法

```python
# registry.py - dispatch() 方法
def dispatch(self, tool_name, params, max_result_size_chars=30000):
    result = self._execute_tool(tool_name, params)
    if len(result) > max_result_size_chars:
        truncated = result[:max_result_size_chars]
        truncated += f"\n\n[TRUNCATED: 原始输出 {len(result)} chars, 已截断至 {max_result_size_chars} chars]"
        return truncated
    return result
```

**原理：** 防止单个工具调用（如 `search_files` 返回大量匹配结果）吃掉大量上下文。设置 30K 硬上限，超出部分截断并提示。

### 4.2 动态工具 Schema 加载

**改造点：** `prompt_builder.py` 中工具 schema 注入逻辑

**当前问题：** 每次构建系统提示时，加载全量工具 schema（约 10K chars），但单次对话通常只使用 3-5 个工具。

**优化方案：**
1. 首轮对话仅加载核心工具 schema（read_file, write_file, search_files, patch）
2. 当 agent 请求未加载的工具时，动态注入该工具的 schema
3. 压缩触发时，移除本次会话未使用过的工具 schema

**预期收益：** 工具 schema 开销从 ~10K 降至 ~4K（核心工具集），节省 6K chars。

### 4.3 压缩联动系统提示瘦身

**改造点：** `context_compressor.py` 压缩触发回调

**优化方案：** 当压缩触发时，同步执行系统提示精简：

1. **Memory 精简：** 仅保留与当前任务相关的 memory 条目
2. **AGENTS.md 精简：** 如果当前为单 agent 模式，移除多 agent 协作配置
3. **Persona 精简：** 压缩后使用精简版 persona（保留核心行为规范，去除示例和详细说明）

```python
# context_compressor.py
def compress(self, messages, system_prompt):
    if self._should_compress(messages):
        compressed_messages = self._compress_messages(messages)
        slim_system_prompt = self._slim_system_prompt(system_prompt)
        return compressed_messages, slim_system_prompt
```

**预期收益：** 系统提示从 ~36K 降至 ~20K，释放 16K 有效空间。

---

## 5. 长期优化方案（架构级）

**目标：从根本上解决上下文容量限制，并建立可持续的上下文管理架构。**

### 5.1 切换原生 Anthropic Provider

**方案：** 绕过 Copilot 中转，直接使用 Anthropic API。

```yaml
# config.yaml
provider: anthropic
model: claude-sonnet-4-20250514
api_key: ${ANTHROPIC_API_KEY}
# context_length 自动获取为 1M
```

**收益：**
- context_length 从 144K 提升至 1M（+594%）
- 压缩触发阈值提升至 500K+（几乎不会在正常对话中触发）
- 系统提示 36K 开销占比从 25% 降至 3.6%

**代价：**
- 需要独立的 Anthropic API key 和计费
- 失去 Copilot 平台的统一管理和计费优势

### 5.2 手动覆盖 Context Length

**方案：** 在 config.yaml 中手动设置 context_length，覆盖 Copilot provider 的默认值。

```yaml
# config.yaml
provider: copilot
model: claude-sonnet-4-20250514
context_length: 500000  # 手动覆盖为 500K
```

**前提条件：** 需要验证 Copilot 平台实际是否支持更大的 context window。如果平台确实在 API 层面做了截断，则此方案无效。

**验证步骤：**
1. 设置 context_length 为 200K
2. 构造超过 144K 的对话
3. 观察是否出现 API 错误

### 5.3 分层上下文管理（热/温/冷）

**方案：** 实现三层上下文管理架构，按信息的时效性和重要性分层存储。

```
┌─────────────────────────────────────────┐
│           热层 (Hot Layer)               │
│   当前对话上下文，保留在 context window   │
│   容量: ~60K chars                       │
│   内容: 最近 N 轮对话、当前任务状态       │
├─────────────────────────────────────────┤
│           温层 (Warm Layer)              │
│   压缩摘要，保留在 context window 头部    │
│   容量: ~10K chars                       │
│   内容: 早期对话的结构化摘要              │
├─────────────────────────────────────────┤
│           冷层 (Cold Layer)              │
│   持久化存储，按需检索                    │
│   容量: 无限制                           │
│   内容: 完整对话历史、文件快照、工具输出   │
│   检索: 语义搜索 + 关键词匹配             │
└─────────────────────────────────────────┘
```

**工作流程：**
1. 新消息进入热层
2. 热层达到阈值时，最旧消息压缩为摘要移入温层，原文移入冷层
3. Agent 需要早期信息时，通过专用工具从冷层检索
4. 检索结果临时注入热层，用后释放

**实现复杂度：高。需要引入向量数据库或语义索引，改造消息管理流程。**

---

## 6. 实施计划

### Phase 1：短期 Config 调优（立即执行）

| 步骤 | 内容 | 耗时 |
|------|------|------|
| 1 | 备份当前 config.yaml | 5 min |
| 2 | 修改四项配置参数 | 10 min |
| 3 | 重启 Hermes，验证配置生效 | 5 min |
| 4 | 执行长对话压力测试，对比压缩触发时机 | 30 min |

**验收标准：** 有效工作空间从 ~36K 提升至 ~65K，长对话中压缩触发频率降低 40%+。

### Phase 2：中期代码改造（1-2 周）

| 步骤 | 内容 | 耗时 | 优先级 |
|------|------|------|--------|
| 1 | 实现 dispatch() 输出截断 | 2h | P0 |
| 2 | 实现动态 schema 加载 | 4h | P1 |
| 3 | 实现压缩联动系统提示瘦身 | 6h | P1 |
| 4 | 集成测试 + 回归测试 | 4h | P0 |

**验收标准：** 系统提示开销降至 ~20K，单工具输出不超过 30K。

### Phase 3：长期架构升级（1-2 月）

| 步骤 | 内容 | 耗时 | 优先级 |
|------|------|------|--------|
| 1 | 验证 Copilot 平台实际 context 上限 | 2h | P0 |
| 2 | 评估原生 Anthropic provider 切换成本 | 4h | P1 |
| 3 | 设计分层上下文管理 POC | 2w | P2 |
| 4 | 实现冷层存储与检索 | 2w | P2 |

**验收标准：** context_length 提升至 500K+ 或实现分层管理 POC。

---

## 7. 风险与注意事项

1. **threshold_percent 调高的风险：** 压缩触发点更接近上下文上限，极端情况下可能来不及压缩就超限。建议保留至少 25% 的安全缓冲（当前方案保留 30%）。

2. **工具输出截断的风险：** 截断可能丢失关键信息。建议在截断提示中包含原始长度和获取完整输出的方法。

3. **动态 schema 加载的复杂性：** 需要处理工具依赖关系（如 patch 依赖 read_file 的上下文），确保 agent 始终能发现可用工具。

4. **向后兼容性：** 中期方案的代码改造需要确保与现有 session 的兼容性，避免破坏正在进行的对话。

---

## 附录：关键代码位置

| 文件 | 关键函数/变量 | 作用 |
|------|--------------|------|
| `context_compressor.py` | `threshold_percent` | 压缩触发阈值 |
| `context_compressor.py` | `target_ratio` | 压缩目标比例 |
| `context_compressor.py` | `compress()` | 压缩主流程 |
| `prompt_builder.py` | `_build_system_prompt()` | 系统提示组装 |
| `registry.py` | `dispatch()` | 工具调用分发 |
| `config.yaml` | `compression.*` | 压缩相关配置 |
