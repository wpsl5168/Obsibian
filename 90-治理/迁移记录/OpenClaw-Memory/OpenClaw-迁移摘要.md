---
title: "OpenClaw 迁移摘要（2026-03-28 ~ 2026-04-12）"
date: 2026-04-14
tags: [OpenClaw, Memory, 摘要, 治理]
---

# OpenClaw 迁移摘要

> 本文件由小贝（二秘/知识库整理员）于 2026-04-14 从 Daily 日志中提炼合并。
> 原始日志已归档至 git 历史，可通过 `git log -- 90-治理/OpenClaw-Memory/Daily/` 查阅。

---

## 一、基础设施搭建（03-28 ~ 03-30）

### 关键决策
- **GitHub 仓库创建**：建立 `wpsl5168/Obsidian` 作为知识库远端存储。
- **用户画像确立**：老王（北京，UTC+8），微软顾问，服务中国银行客户，擅长 SharePoint 和 SQL Server。兴趣方向：Claude Code + vibe coding，AI Agent 个人知识库。
- **知识库需求定调**：系统化目录索引、每主题历史+最新整合、技术演进叙事、深度领域专题。语言偏好中文为主，英文术语保留。
- **Mattermost 部署**：VM 主机 myAI 上运行，Caddy 反代，Let's Encrypt HTTPS 证书（`myai.westus2.cloudapp.azure.com`）。
- **自动备份体系**：`mattermost-backup.sh` + systemd timer，每日 02:30 UTC 备份 Postgres + 配置。
- **Agent 体系初始化**：两个 Agent — main（小虾/大秘）和 second-secretary（小贝/二秘）。通过 Mattermost 接入。
- **OpenClaw 配对**：sysadmin 账号配对完成（code UHH74G74）。

---

## 二、日常简报与安全策略（04-01 ~ 04-02）

### 关键决策
- **每日 AI 简报建立**：Cron Job `0 8 * * *`（Asia/Shanghai），Mattermost 私聊推送。模板：一句话总览 + 3-5 热点（背景/分析/行动建议）+ 明日预告。
- **Agent 安全六条行动清单**：
  1. 工具分级（读/写/执行/外联），默认最小权限
  2. 工具调用统一审计日志
  3. coding agent 运行加沙箱
  4. 一任务一分支/PR 审核
  5. 依赖供应链加固
  6. 制定敏感信息禁入清单
- **小红书账号共建计划**：硬核冷静专业的技术博主定调，老王碳基构思+手动发布，小虾硅基全包文案与视觉卡片。
- **NotebookLM 调研结论**：个人版无官方 API，建议走 Gemini API + Drive API 替代方案。
- **Mattermost SSL 排查**：手机端旧域名证书不匹配，改用正确域名 `myai.westus2.cloudapp.azure.com` 即可。

---

## 三、出差与系统排错（04-03 ~ 04-04）

### 关键事件
- **雄安出差**：通过飞书提供亲子游推荐（商务服务中心、金湖公园、悦容公园、自动驾驶公交体验）。
- **Mattermost 回复 Bug**：发现 `Invalid RootId parameter` 错误，原因是回复已不存在的帖子。解决：发新消息而非回复旧帖。

---

## 四、核心能力建设（04-07 ~ 04-08）

### 关键决策
- **邮件附件发送修复**：Himalaya 邮件工具带附件发送语法修复，改用 Python MIME 方案成功。
- **命令免 Approve**：老王要求取消逐条审批，配置网关全量命令自动执行。
- **Web 端配对**：配置 `openclaw.brickhub.cc` 反向代理，支持公网访问 OpenClaw Dashboard。
- **记忆检索切换**：切换至本地 Ollama + `nomic-embed-text`，提升隐私与稳定性。
- **双轨制生态**：大秘（小虾）主外排错跑脚本；二秘（小贝）主内，隔离容器维护知识库。
- **二秘 Git 推送**：配置专用 GitHub PAT（仅 Obsidian 仓库权限）注入小贝环境。
- **灾备方案落地**：24h Cron 自动打包配置/向量库/记忆文件到 `wpsl5168/OpenClaw` 私有仓库。

### SQL Server 加密系列输出
- **方案一（WITH ENCRYPTION）**：原生加密 + PowerShell 批量脚本（含注释剥离）→ `03-日常灵感/SQLServer_存储过程加密方案_WITH_ENCRYPTION.md`
- **方案二（CLR + 混淆）**：C# CLR + ConfuserEx/Dotfuscator → `03-日常灵感/SQLServer_高级加密方案_CLR_混淆.md`
- **方案三（Dacpac 加密）**：AES-256 加密 .dacpac + 阅后即焚部署 → `03-日常灵感/SQLServer_Dacpac包加密与自动化部署.md`

### 知识库重大重构（04-08）
- 废弃旧 `Obsidian/` 目录，启用 `obsidian-vault/`
- 建立 [[90-治理/写作规范.md]]（Callout 语法、盘古之白、Frontmatter、双链强制）
- AI 知识星球 6 大结构定型
- 小贝模型升级为 `claude-3.5-sonnet`
- 全量文件清洗、迁移、合并，推送 GitHub

### Daily Brief 流水线
- 简报改为直接归档到 `06-AI-Agent-Daily/` 目录并 Push
- 心跳补偿机制：断电重启后自动补跑简报和备份

---

## 五、BrickHub 项目攻坚（04-08 ~ 04-09）

### 关键决策
- **BrickHub 部署**：Next.js 项目 `~/brickhub`，PM2 守护端口 3005，域名 `news.brickhub.cc`（Caddy 反代）。
- **四秘分工固化**：小虾(PM/大秘)、小贝(知识库/竞品)、小马(前端/渲染)、小牛(QA)。
- **测试数据纠偏**：禁止使用 AI 编造的 LDraw 示例，改用官方纯人类构建标准测试件。
- **渲染引擎重大修复**：旋转矩阵 Bug、原点对齐穿模、PBR 材质升级。
- **文档沉淀**：Architecture Vision、Technical Research、LDraw Standard Assets 三份核心文档归档。

---

## 六、Pipeline 稳定运行（04-10 ~ 04-12）

### 关键事件
- 04-10：AI Daily Brief pipeline 正常执行
- 04-11：简报与记忆备份正常运行
- 04-12：系统备份完成、Obsidian 备份同步、飞书通知触发、二秘审计满分（100分）
