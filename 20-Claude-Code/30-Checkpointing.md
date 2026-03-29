# Checkpointing（回退/回放机制）

来源（官方）：<https://code.claude.com/docs/en/checkpointing>

## 你需要记住的点
- Claude Code 会在**每次编辑前**自动做 checkpoint，可通过 `/rewind` 回退。
- 支持：
  - 只回退代码 / 只回退对话 / 两者都回退
  - 从某个点开始 summarize（压缩上下文，避免 context window 爆掉）

## 最重要的限制（务必记住）
- **bash 命令改动不在 checkpoint 里**。
  - 比如 `rm/mv/cp` 或脚本生成文件，rewind 不会帮你恢复。
  - 所以：重要变更一定要用 Git（commit/branch）兜底。

## 企业落地建议
- 对关键模块：让 Claude 在改之前先创建分支或 worktree（隔离）。
- 形成固定节奏：小步提交（每完成一个子任务就 commit）。
