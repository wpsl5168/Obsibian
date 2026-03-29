# Claude Code CLI Cheatsheet（速查）

来源（官方）：<https://code.claude.com/docs/en/cli-reference>

## 常用
- `claude`：进入交互模式
- `claude "query"`：带初始 prompt 进入交互
- `claude -p "query"`：跑完就退出（适合脚本化）
- `claude -c`：继续当前目录最近一次对话
- `claude -r "<session>" "query"`：按 session id/name 恢复继续
- `claude update`：更新
- `claude auth login` / `logout` / `status`

## 建议的企业开发用法
- 把 repo 的 build/test/lint 命令写进 CLAUDE.md，让它少问你“怎么跑测试”。
