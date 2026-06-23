---
title: Global Rules - Hermes Agent 使用规范
created: 2026-06-23
updated: 2026-06-24
type: methodology
tags: [hermes, workflow]
status: stable
---

# Global Rules — Hermes Agent 使用规范

> 通用规则与最佳实践 — 适用于所有 Hermes 会话的基本准则

## 核心原则

### 1. 明确的请求 = 高效的响应

**差**：
```
帮我处理下那个文件
```

**好**：
```
读取 src/main.py，找出所有未使用的 import，并移除它们
```

**最佳实践**：
- 提供文件路径、错误信息、具体期望
- 一次说清楚上下文，减少来回追问
- 复杂任务拆解成多个明确步骤

### 2. 信任 Agent 的工具能力

Hermes 有完整工具链（文件操作、搜索、终端、浏览器），**不需要你手动复制粘贴内容**。

**差**：
```
[粘贴 500 行代码]
帮我分析这段代码
```

**好**：
```
分析 src/auth/jwt.py 的安全问题
```

Hermes 会自动 `read_file()`，节省 token 和时间。

### 3. 使用 AGENTS.md 固化项目规则

项目根目录创建 `AGENTS.md`，Hermes 会自动加载：

```markdown
# 项目规则

## 技术栈
- Python 3.11
- FastAPI + SQLAlchemy
- PostgreSQL

## 代码风格
- 使用 ruff 格式化
- 所有函数必须有 docstring
- 测试覆盖率 > 80%

## 工作流
- 修改前先运行测试
- Git commit 用常规提交格式（Conventional Commits）
```

Hermes 会遵守这些规则，不用每次重复说明。

### 4. 技能（Skills）是可复用的操作手册

**何时创建 Skill**：
- 操作步骤 ≥ 5 步
- 需要重复执行
- 有明确的前置条件和验证步骤

**示例**：
```bash
# 让 Hermes 保存为 skill
"请把刚才的 Docker 部署流程保存为 skill"
```

之后直接：
```bash
/skill deploy-docker
```

### 5. Memory 管理 — 记住重要的，遗忘琐碎的

**应该记住**：
- 用户偏好（"我喜欢简洁的回复"）
- 项目约定（"后端用 Python，前端用 TypeScript"）
- 工具特性（"这个 API 有速率限制，每分钟 10 次"）

**不应该记住**：
- 任务进度（"已完成 PR #123"）→ 用 `/title` 或 session
- 临时数据（"今天天气 28°C"）
- 代码细节 → 用文件或技能

**清理 Memory**：
```bash
"清理记忆中的过期信息"
```

## 会话管理规范

### 何时开新会话

| 场景 | 操作 |
|------|------|
| 切换不同项目 | `/new <project-name>` |
| 上下文混乱了 | `/new` |
| 长任务告一段落 | `/compress` + `/new` |

### 何时压缩上下文

- 会话超过 50 轮对话
- 包含大量工具输出（日志、diff）
- 感觉响应变慢

```bash
/compress
```

### 会话命名习惯

**差**：
- `test`
- `asdf`
- `new project`

**好**：
- `backend-api-refactor`
- `debug-payment-gateway`
- `research-rust-async`

## 提问技巧

### 调试问题

**差**：
```
代码报错了
```

**好**：
```
运行 pytest tests/test_auth.py 时报 ImportError: cannot import name 'verify_token'
文件路径: src/auth/jwt.py
Python 版本: 3.11
```

### 代码审查

**差**：
```
看看这个 PR
```

**好**：
```
审查 PR #123 (git diff main..feature/auth)
重点关注:
1. 安全性（JWT 验证）
2. 性能（数据库查询）
3. 测试覆盖率
```

### 学习/调研

**差**：
```
Rust 怎么样
```

**好**：
```
对比 Rust 和 Go 在以下场景的优劣：
- Web 后端开发（框架、ORM、生态）
- 并发模型
- 学习曲线
- 生产案例
```

## 工具使用指南

### 文件操作

```bash
# 读取文件（Hermes 自动处理）
"读取 README.md 并总结"

# 批量操作
"把 src/ 下所有 .py 文件的 print() 换成 logging.info()"

# 搜索
"在项目中搜索所有 TODO 注释"
```

### 终端命令

```bash
# 让 Hermes 执行
"运行 pytest 并显示覆盖率"

# 复杂脚本
"写一个脚本：
1. 检查 Docker 是否运行
2. 启动 PostgreSQL 容器
3. 等待数据库就绪
4. 运行迁移
然后执行它"
```

### Web 搜索

```bash
# 实时信息
"搜索 Python 3.13 最新特性"

# 对比调研
"对比 2026 年主流 CI/CD 工具（GitHub Actions、GitLab CI、Jenkins）"
```

## 安全最佳实践

### 1. 敏感操作确认

危险操作（删除文件、执行 sudo、修改数据库）Hermes 会请求确认。

**跳过确认（仅限安全环境）**：
```bash
hermes --yolo
```

### 2. 不信任的代码隔离

```bash
# 使用 Docker 隔离环境
hermes chat --docker

# 或独立 worktree
hermes --worktree
```

### 3. 消息平台白名单

Gateway 部署时设置白名单，避免未授权用户访问：

```yaml
# config.yaml
telegram:
  allowlist:
    - 123456789    # 你的 Telegram user ID
```

## 平台特定规范

### Telegram / Discord / Slack

- `/title` 设置会话名称
- 跨平台切换：CLI → `/handoff telegram` → Telegram 继续 → `/resume` 回 CLI
- 图片直接发送，Hermes 自动识别

### CLI / TUI

- `Ctrl+C` 中断（双击强制退出）
- `Alt+Enter` 多行输入
- `Tab` 自动补全
- `/help` 查看所有命令

## 性能优化

### 减少 Token 消耗

1. **用工具读取，不要粘贴**
   ```
   # 差：粘贴 1000 行日志
   # 好："分析 logs/error.log 的最后 50 行"
   ```

2. **用摘要，不要全文**
   ```
   "总结 docs/ 下的所有 markdown 文件（15 个）"
   # 而不是让 Hermes 读取并返回所有内容
   ```

3. **定期压缩上下文**
   ```bash
   /compress
   ```

### 加快响应速度

1. **选对模型**
   - 简单任务：`gpt-4o-mini` / `claude-haiku`
   - 复杂推理：`claude-opus` / `gpt-5.5`

2. **预加载技能**
   ```bash
   hermes chat -s docker-deploy,pytest-workflow
   ```

3. **批量操作合并**
   ```
   # 差：分 10 次问
   # 好："分析 src/ 下所有 Python 文件，生成统一的代码质量报告"
   ```

## 故障排查

### Hermes 不响应

```bash
# 检查进程
ps aux | grep hermes

# 查看日志
hermes logs

# 重启 gateway
hermes gateway restart
```

### 会话恢复失败

```bash
# 列出所有会话
hermes sessions list

# 检查数据库
sqlite3 ~/.hermes/state.db "SELECT * FROM sessions ORDER BY updated_at DESC LIMIT 10;"
```

### 配置问题

```bash
# 查看当前配置
hermes config list

# 重置配置（小心！）
hermes config reset

# 或手动编辑
vim ~/.hermes/config.yaml
```

---

## 更新日志

| 日期 | 内容 |
|------|------|
| 2026-06-23 | 根据 Hermes 最佳实践和社区经验整理全局使用规范 |
