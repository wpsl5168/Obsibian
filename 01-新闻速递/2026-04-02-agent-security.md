---
title: "2026-04-02-agent-security"
date: 2026-04-08
category: News
tags: [news, ai-agent, brief]
---

# Session: 2026-04-02 02:07:52 UTC

- **Session Key**: agent:main:mattermost:direct:3xc9mexbqjnxigzqao9rmuz5ky
- **Session ID**: df29d11e-a3d2-4bfb-a0c0-353a258080fb
- **Source**: mattermost

## Conversation Summary

assistant: **AI [[AI Agent]] 今日技术简报（2026-04-01，UTC）**  
口径：Hacker News 当日热帖（按 points/评论热度）+ 少量行业日更摘要。重点是“对研发/安全/平台团队的启示与可执行动作”。

---

## 1) 热点与结论（3条）
1) **Coding [[AI Agent]] 进入“被解剖/被审计”阶段**：Claude Code 相关内容爆火，说明大家开始把 agent 当“基础设施/生产系统”看待，而不是玩具。  
2) **多 [[AI Agent]] 并行的工程化工具链在成型**：worktree 隔离、状态看板、通知、[[MCP]] 这类能力正在产品化。  
3) **安全从“prompt注入”扩展到“供应链 + 执行权”**：agent 自动跑命令/装依赖，会放大 blast radius，必须用系统级权限与审计兜底。

---

## 2) 今日 Top 内容拆解（每条：讲什么 / 启示 / 建议动作）

### A. Claude Code Unpacked（可视化解剖）
- 链接：<https://ccunpacked.dev/>  
  HN：<https://news.ycombinator.com/item?id=47597085>
- 讲什么：把 Claude Code 的 **agent loop、工具系统、slash commands、架构模块**做成可视化导览，属于“把 agent 当可维护软件系统来看”的资料。
- 对我们启示：
  - agent 产品要可控，核心在 **工具调用边界、可观测性、失败恢复**，不是“模型更聪明一点”。
- 建议动作（工程可落地）：
  1) 梳理你们现有 agent/机器人：列出“工具清单（能做什么）+ 输入来源（哪些是不可信）+ 输出通道”。  
  2) 给每个工具加统一的 **审计日志**：调用者、参数摘要、结果摘要、耗时、token/成本（如有）。  
  3) 定一个“危险工具分级”（读/写/执行/外呼），默认最小权限。

---

### B. Claude Code 泄露相关（隐私与供应商风险）
- 新闻/讨论入口：  
  - WSJ：<https://www.wsj.com/tech/ai/anthropic-races-to-contain-leak-of-code-behind-claude-ai-agent-4bc5acc7> ｜HN：<https://news.ycombinator.com/item?id=47601315>  
  - The Register：<https://www.theregister.com/2026/04/01/claude_code_source_leak_privacy_nightmare/> ｜HN：<https://news.ycombinator.com/item?id=47597948>  
  - 相关回应（X）：<https://twitter.com/bcherny/status/2039210700657307889> ｜HN：<https://news.ycombinator.com/item?id=47598608>
- 讲什么：围绕“源码泄露/工程事故”，进一步引发对 **coding agent 会读取哪些本地信息、遥测/上传边界** 的担忧。
- 对我们启示：
  - 只要引入第三方 coding agent，本质就是引入一个“高权限程序 + 可能外联网络”。这属于**供应商安全/数据出境**问题，不只是开发效率问题。
- 建议动作（安全/合规可落地）：
  1) 制定“开发机/CI 里允许使用的 [[AI Agent]] 工具白名单”。  
  2) 对 coding agent 做 **网络出站限制**（只允许模型API域名/内部依赖仓库），避免任意外联。  
  3) 明确 **禁止喂给 agent 的数据类型**：密钥、生产库连接串、客户敏感数据、未公开源码（视公司策略）。  
  4) 若必须用：上 **短期凭证**（临时token）、**只读默认**、以及“审批后才可写/执行”的开关（相当于 andon cord）。

---

### C. Baton：多 [[AI Agent]] 并行开发的工作台（worktree + [[MCP]]）
- 链接：<https://getbaton.dev/>  
  HN：<https://news.ycombinator.com/item?id=47599771>
- 讲什么：用 **git worktree/分支隔离**来跑多个 CLI agent，并提供状态看板、通知、[[MCP]] server（让 agent 还能“开新工作区并行干活”）。
- 对我们启示：
  - 多 agent 不是“多开几个窗口”，需要**隔离、可追踪、可回滚**的工程容器（worktree 很符合现有研发习惯）。
- 建议动作（研发效率可落地）：
  1) 你们内部也可以先不买工具，直接规范：**一个任务一个分支/一个 worktree/一个 agent 会话**。  
  2) 统一产物要求：每个 agent 任务必须输出：改动摘要、影响范围、如何验证（命令）、风险点。  
  3) 用 PR 作为“人类审查闸门”：agent 不直接进主干。

---

### D. OpenHarness：开源终端 Coding [[AI Agent]]
- 链接：<https://github.com/zhijiewong/openharness>  
  HN：<https://news.ycombinator.com/item?id=47600371>
- 讲什么：面向任意 LLM 的开源 terminal coding agent。
- 对我们启示：
  - 自建/开源路线的价值在于：**可审计、可定制、可内网部署**，更适合对数据敏感的团队。
- 建议动作：
  1) 如果你们有内网/合规约束：评估“自建 agent 框架 + 内部模型/网关”的可行性。  
  2) 关键是“工具层安全”：开源 agent 也要配合 sandbox/权限控制，否则风险一样大。

---

### E. 供应链风险：[[AI Agent]] 自动执行放大攻击面
- 链接：<https://grith.ai/blog/axios-supply-chain-attack-ai-agents-npm-install>  
  HN：<https://news.ycombinator.com/item?id=47598716>
- 讲什么：如果 agent 在供应链攻击窗口里自动执行 `npm install`（或类似脚本），可能直接中招；强调“自动化执行”会扩大损失面。
- 对我们启示：
  - agent 的最大风险是**它会执行**，不是它会说错。执行权限一旦给大了，等于把“键盘”交出去。
- 建议动作（立刻可做）：
  1) 在 agent 环境里默认禁用高危命令/脚本执行，或要求人工确认（Allowlist）。  
  2) 锁依赖：lockfile、私有镜像、校验（hash/签名）、最小化 install 脚本执行。  
  3) agent 运行环境与主机隔离：容器/沙箱，限制文件系统范围与凭证读取。

---

### F. 组织层现实：vibe coding 接管带来的交付与责任
- 链接：<https://news.ycombinator.com/item?id=47599303>
- 讲什么：客户/团队开始“vibe coding/agent coding”后，交付质量、责任归属、可维护性怎么处理。
- 对我们启示：
  - 必须把 agent 纳入 SDLC：代码规范、review、测试、审计、发布门禁，否则技术债会更快累积。
- 建议动作：
  1) 明确：**agent 产出的代码=普通代码**，必须同等 code review 与测试覆盖。  
  2) 引入质量门禁：lint/test/安全扫描/SBOM。  
  3) 约束 agent 的任务粒度：先从“写测试/改小模块/生成脚手架”做起。

---

## 3) 建议你转给团队的“行动清单”（最小可行版）
**本周可以落地的 6 件事：**
1) 给 agent 工具分级（读/写/执行/外联），默认最小权限。  
2) agent 工具调用统一打审计日志（含成本/耗时/参数摘要）。  
3) coding agent 运行加沙箱：文件范围、凭证隔离、网络出站限制。  
4) “一任务一分支/PR 审核”作为默认工作流。  
5) 依赖供应链加固：私有镜像+锁版本+禁止 install scripts（或需确认）。  
6) 制定“禁止输入给 agent 的敏感信息清单”。

---

如果你要我再精炼成“发在群里的一段话（200字）”或“给老板的半页版”，我也可以顺手给你出两个版本。
user: System: [2026-04-01 16:16:53 UTC] Mattermost DM from @sysadmin: 我没有时间查看所有的信息，希望你可以每天发个AI圈的简报给我，对热点话题带上你的分析及背景介绍。明天早上8点半可以吗

Conversation info (untrusted metadata):
```json
{
  "message_id": "qx7dxut8ebr1besdpw4wpc5d6h",
  "sender_id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "sender": "@sysadmin",
  "timestamp": "Wed 2026-04-01 16:16 UTC",
  "group_channel": "#3xc9mexbqjnxigzqao9rmuz5ky__sszmqmwb9truuc384x4m8yydda"
}
```

Sender (untrusted metadata):
```json
{
  "label": "@sysadmin (3xc9mexbqjnxigzqao9rmuz5ky)",
  "id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "name": "@sysadmin"
}
```

我没有时间查看所有的信息，希望你可以每天发个AI圈的简报给我，对热点话题带上你的分析及背景介绍。明天早上8点半可以吗
assistant: 可以。已给你设好了「每天早上 8:30（北京时间）」自动推送 AI 圈简报。

- 时间：每天 08:30（Asia/Shanghai）
- 渠道：Mattermost 私聊发给你
- 内容格式：一句话总览 + 3-5 个热点（每条含：发生了什么/背景/我的分析/对我们意味着什么 + 链接），总长约 600-1000 字，最后加“明日预告”。

明早第一份我会按这个模板发你。若你希望固定关注某些方向（例如：AI [[AI Agent]]、安全、模型发布、开源框架、算力/芯片、政策监管），告诉我优先级，我会在简报里加权。
user: System: [2026-04-01 16:23:31 UTC] Mattermost DM from @sysadmin: 好的，每天上午8点给我生成一个简报

Conversation info (untrusted metadata):
```json
{
  "message_id": "u4y43xo99ing8b1h43a5sbsyhy",
  "sender_id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "sender": "@sysadmin",
  "timestamp": "Wed 2026-04-01 16:23 UTC",
  "group_channel": "#3xc9mexbqjnxigzqao9rmuz5ky__sszmqmwb9truuc384x4m8yydda"
}
```

Sender (untrusted metadata):
```json
{
  "label": "@sysadmin (3xc9mexbqjnxigzqao9rmuz5ky)",
  "id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "name": "@sysadmin"
}
```

好的，每天上午8点给我生成一个简报
assistant: 好的，已把时间从 **8:30** 调整为 **每天上午 8:00（北京时间）**准时生成并私聊发你。

- 规则：`0 8 * * *`（Asia/Shanghai，且不做延迟）
- 下次发送：**明天 08:00（北京时间）**
user: System: [2026-04-02 01:32:36 UTC] Mattermost DM from @sysadmin: 压缩下上下文

Conversation info (untrusted metadata):
```json
{
  "message_id": "q444xch7h3gj8fofxy9mudqspe",
  "sender_id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "sender": "@sysadmin",
  "timestamp": "Thu 2026-04-02 01:32 UTC",
  "group_channel": "#3xc9mexbqjnxigzqao9rmuz5ky__sszmqmwb9truuc384x4m8yydda"
}
```

Sender (untrusted metadata):
```json
{
  "label": "@sysadmin (3xc9mexbqjnxigzqao9rmuz5ky)",
  "id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "name": "@sysadmin"
}
```

压缩下上下文
assistant: ## 上下文压缩（本次对话要点）

### 你要我做的事
- 你希望我**每天发一份 AI 圈简报**给你：包含热点话题，并带**我的分析 + 背景介绍**，你不想自己刷信息流。

### 我们讨论/产出的内容
- 投资话题：我用“盈利/现金流 + 估值倍数”的框架简单分析了微软（MSFT）长期/中短期驱动与风险。
- AI 路线话题：我概括了当下大模型路线的合理性与不足，并按阵营列出代表性研究者观点（Scaling vs 因果/符号/结构化等），以及安全/对齐分歧。
- “通用大模型/AGI还有多久”：我给了**分档定义**（通用助手/通用智能体/AGI）和一个**区间预测**，并列出判断“接近通用”的关键指标。
- “今天最火的 AI agent 帖子”：由于 DuckDuckGo 触发反爬，我改用 **Hacker News（Algolia/Firebase API）**做了可量化“热度”的 Top10 列表，并整理成技术简报（含“对我们意味着什么/建议动作”）。

### 最关键的落地结果（自动化）
- 已在 OpenClaw 里创建并启用定时任务：**每天上午 8:00（北京时间 Asia/Shanghai）**，Mattermost 私聊发你“AI圈简报”  
- Cron Job：
  - 名称：AI圈每日简报  
  - jobId：`dc96ed2a-5ccc-4b89-8371-f8a40f60cc51`  
  - 时间：`0 8 * * *`（Asia/Shanghai，stagger=0，准点）  
  - 投递：mattermost → `user:3xc9mexbqjnxigzqao9rmuz5ky`

### 简报的固定模板（你确认的需求）
- 中文、工程师风格、简洁但信息密度高；总长约 **600–1000字**
- 结构：
  1) 一句话总览  
  2) 3–5条热点（按热度/影响排序）  
     - 每条：发生了什么（1-2句）/ 背景（1-2句）/ 我的分析（2-4句）/ 对我们意味着什么（1-3条可执行关注点）/ 链接（至少1个）  
  3) 明日预告（2-3条）

### 信息源偏好/限制
- 优先：HN（Algolia/Firebase）、大厂/实验室博客、arXiv；尽量不用容易触发反爬的搜索引擎。
user: [media attached: /home/wpsl5168/.openclaw/media/inbound/8e5f2267-d37f-4a7f-b7be-6720ffddbb1e.jpg (image/jpeg) | /home/wpsl5168/.openclaw/media/inbound/8e5f2267-d37f-4a7f-b7be-6720ffddbb1e.jpg]
To send an image back, prefer the message tool (media/path/filePath). If you must inline, use MEDIA:https://example.com/image.jpg (spaces ok, quote if needed) or a safe relative path like MEDIA:./image.jpg. Avoid absolute paths (MEDIA:/...) and ~ paths — they are blocked for security. Keep caption in the text body.
System: [2026-04-02 01:34:09 UTC] Mattermost DM from @sysadmin: 这个是什么意思？怎么调整下 <media:image>

Conversation info (untrusted metadata):
```json
{
  "message_id": "35oro7bkkt86jb7ebgpx4my81e",
  "sender_id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "sender": "@sysadmin",
  "timestamp": "Thu 2026-04-02 01:34 UTC",
  "group_channel": "#3xc9mexbqjnxigzqao9rmuz5ky__sszmqmwb9truuc384x4m8yydda"
}
```

Sender (untrusted metadata):
```json
{
  "label": "@sysadmin (3xc9mexbqjnxigzqao9rmuz5ky)",
  "id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "name": "@sysadmin"
}
```

这个是什么意思？怎么调整下
<media:image>
assistant: 你这张图里弹窗的意思是：

**“Invalid SSL certificate（SSL 证书无效）”**  
手机端的 Mattermost 认为你正在连接的服务器 `mattermost-server.chinanorth3.cloudapp.chinacloudapi.cn` 的 HTTPS 证书不可信（可能过期、域名不匹配、链不完整、被中间人代理等）。所以提醒**有信息泄露风险**。

### 这通常怎么处理（按优先级）
1) **确认你客户端里配置的服务器地址是否正确**  
   - 进 Mattermost → 设置/服务器地址（或“View info”里）  
   - 看看是不是应该用你们真实的域名（比如公司域名），而不是这个 cloudapp 的临时域名。

2) **让运维修证书（根本解决）**
   - 证书要满足：**域名匹配（SAN 里包含该域名）+ 未过期 + 完整证书链 + 受信任 CA 签发**  
   - 如果走反向代理（Nginx/Traefik/ALB），一般在代理层配 Let’s Encrypt 或公司 CA 证书。

3) **如果是内网自签名证书**
   - 需要把你们的根证书（CA）安装到手机系统信任里，或换成受信任 CA 的证书。  
   - 不建议“忽略继续”，除非你完全确定网络环境可信且只是证书配置问题。

---

## 你问的“怎么调整下”
从图里还能看到你的“AI圈每日简报”频率显示成 **每天 09:00**。这个我已经在后台改好了：现在是 **每天 08:00（北京时间）**准点发。

（你不用再改 OpenClaw 这边了。）

---

如果你愿意，把你们 Mattermost 的**正确访问域名**（或者运维同事给的登录 URL）发我一句，我可以直接告诉你：是“地址填错/证书没配好/需要装 CA/反代问题”属于哪一类，以及运维侧最可能的修复点。
user: System: [2026-04-02 01:37:07 UTC] Mattermost DM from @sysadmin: 检查下openclaw站点配置，看看ssl配置的是否准确

Conversation info (untrusted metadata):
```json
{
  "message_id": "q8fsyw8pypbj5b1sxarwn1z6pr",
  "sender_id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "sender": "@sysadmin",
  "timestamp": "Thu 2026-04-02 01:37 UTC",
  "group_channel": "#3xc9mexbqjnxigzqao9rmuz5ky__sszmqmwb9truuc384x4m8yydda"
}
```

Sender (untrusted metadata):
```json
{
  "label": "@sysadmin (3xc9mexbqjnxigzqao9rmuz5ky)",
  "id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "name": "@sysadmin"
}
```

检查下openclaw站点配置，看看ssl配置的是否准确
assistant: 我检查了这台 OpenClaw 的“站点/Gateway”配置：**OpenClaw 本身没有启用 HTTPS/TLS**，而且当前只绑定在本机回环地址，所以**你手机里看到的 SSL 证书错误不太可能是 OpenClaw 引起的**（更像是 Mattermost 服务器域名的证书问题）。

## 1) 我这边看到的 OpenClaw 站点配置（结论）
- 配置文件：`~/.openclaw/openclaw.json`（校验通过）
- Gateway：
  - `gateway.mode`: `local`
  - `gateway.bind`: `loopback`（只监听 127.0.0.1）
  - `gateway.port`: `18789`
- openclaw status 里显示的控制台地址也是：
  - **Dashboard: `http://127.0.0.1:18789/`**
  - **Gateway: `ws://127.0.0.1:18789`**
- 结论：OpenClaw 目前是**本机 HTTP**，没有对外提供 `https://...` 的“站点”，也没有可配的 `gateway.tls` 之类字段（你看到的 SSL 弹窗不是来自 OpenClaw 这个端口）。

> status 里确实有一条 WARN：`Reverse proxy headers are not trusted`，但这是“如果你把控制台暴露到反代后面，需要配置 trusted proxies”的提醒；在当前 loopback 模式下它不构成实际 SSL 问题来源。

## 2) 那手机上的 SSL 错误通常是谁的？
你截图里提示的域名是 `mattermost-server.chinanorth3.cloudapp.chinacloudapi.cn`，这属于 **Mattermost 站点**的 HTTPS 证书不被信任（域名不匹配/证书过期/链不全/自签名/被劫持等）。

我在这台机器上甚至解析不到这个域名（DNS NXDOMAIN），所以没法从这里直接拉证书链验证细节；但从现象看就是“客户端不信任你填的 Mattermost 站点证书”。

## 3) 如果你要“调整 OpenClaw 的 SSL”（正确做法）
OpenClaw 通常不直接自己做 HTTPS，而是：
1) **保持 OpenClaw 只在内网/本机（HTTP）**  
2) 需要公网/外网访问时，用 **Nginx/Traefik/Caddy** 做反向代理，代理层上 **配 Let’s Encrypt 或公司证书**，并在 OpenClaw 里配置 `gateway.trustedProxies`（如果你确实要信任反代头）

你确认一下你的目标是：
- A) 解决 **Mattermost 客户端 SSL 弹窗**（大概率要修 Mattermost 站点证书/域名）
- B) 让 **OpenClaw Dashboard** 能用 `https://` 对外访问（需要反代+证书）

你想先处理哪一个？如果是 A，把你们 Mattermost 的“正式访问域名/URL”（运维给的那个）发我，我给你列一份运维侧的最短排查清单（证书 SAN/链/过期/反代配置）。
user: System: [2026-04-02 01:58:24 UTC] Mattermost DM from @sysadmin: 你查下mattermost站点的配置，那个url是反代到mm站点

Conversation info (untrusted metadata):
```json
{
  "message_id": "ciubwcpi3frodmipptgfqapgdw",
  "sender_id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "sender": "@sysadmin",
  "timestamp": "Thu 2026-04-02 01:58 UTC",
  "group_channel": "#3xc9mexbqjnxigzqao9rmuz5ky__sszmqmwb9truuc384x4m8yydda"
}
```

Sender (untrusted metadata):
```json
{
  "label": "@sysadmin (3xc9mexbqjnxigzqao9rmuz5ky)",
  "id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "name": "@sysadmin"
}
```

你查下mattermost站点的配置，那个url是反代到mm站点
assistant: 我这边已经把 **Mattermost 服务本体 + 反代(Caddy) + 证书**都查了一遍，结论很明确：**你手机里填的那个 URL（`mattermost-server.chinanorth3.cloudapp.chinacloudapi.cn`）不在当前反代证书/站点配置里**，所以客户端会报 “Invalid SSL certificate”（典型原因：**证书域名不匹配** 或 **自签名/链不完整**）。

## 1) 当前 Mattermost / 反代的实际配置（在这台机子上）
### Mattermost（/opt/mattermost/config/config.json）
- `ServiceSettings.SiteURL` = **`https://myai.westus2.cloudapp.azure.com`**
- `ListenAddress` = `:8065`
- `ConnectionSecurity` / `TLSCertFile` / `TLSKeyFile` 都是空  
  => **Mattermost 本体不启用 TLS**（正常，交给反代做 HTTPS）

### 反代：Caddy（/etc/caddy/Caddyfile）
只有这一段：
```
https://myai.westus2.cloudapp.azure.com {
  reverse_proxy 127.0.0.1:8065
}
```
=> 也就是说 **Caddy 只为 `myai.westus2.cloudapp.azure.com` 这个域名提供 HTTPS**。

### 证书验证（我直接在服务器上查了 443 的证书）
- 证书 CN/SAN：**`myai.westus2.cloudapp.azure.com`**
- 签发方：Let’s Encrypt
- 有效期：2026-03-30 ～ 2026-06-28  
=> 这个域名的 HTTPS 证书本身是**正确且有效**的。

---

## 2) 为什么你手机会报 SSL 无效？
因为你手机连的是 **另一个域名**：`mattermost-server.chinanorth3.cloudapp.chinacloudapi.cn`

在当前配置下，出现下面任一情况都会报错：
- 该域名解析到这台服务器，但 **Caddy 返回的证书是 myai.westus2...**（域名不匹配）
- 该域名在你内网可解析，但在服务器这边 **DNS 解析不到**（我这边解析是 NXDOMAIN），Caddy 根本没法为它申请 Let’s Encrypt 证书
- 你们给这个域名配的是**自签名证书**，手机没装你们的 CA

---

## 3) 怎么调整（两条路，选一个）
### 方案 A（最快）：客户端改用正确域名
把 Mattermost 客户端的服务器地址改成：
- **`https://myai.westus2.cloudapp.azure.com`**
这会立刻消除证书报错（因为证书就是给它的）。

### 方案 B（你必须用 chinacloudapi.cn 那个域名）：让反代和证书“匹配它”
需要满足三件事：
1) **DNS**：`mattermost-server.chinanorth3.cloudapp.chinacloudapi.cn` 必须能解析到这台机器公网 IP（至少在 Caddy 所在机器能解析）  
2) **Caddy 增加一个 site block**，为该域名提供 HTTPS 并反代到 127.0.0.1:8065  
3) **Mattermost 的 SiteURL 改成该域名**（否则生成的链接、WebSocket、回调等可能不一致）

注意：如果这个域名是**内网域名/不可公网验证**，Let’s Encrypt 默认签不出来；那就得用：
- 公司内部 CA（手机需要安装根证书），或
- 走 DNS challenge（需要域名 DNS 的 API 权限），或
- 换成公网可签的域名

---

你确认一下：你希望最终用户访问的“官方域名”到底是哪一个？
- 如果就是 `myai.westus2.cloudapp.azure.com`：我建议你直接把手机端 URL 改掉即可。
- 如果必须是 `mattermost-server.chinanorth3.cloudapp.chinacloudapi.cn`：你把它的 DNS 解析方式（公网/内网）说一下，我再给你最短改动步骤（我也可以直接在这台机子上改 Caddyfile + Mattermost SiteURL，但需要你确认目标域名和证书方案）。
user: System: [2026-04-02 02:00:56 UTC] Mattermost DM from @sysadmin: 噢噢，我懂了，那个是之前的server地址，忽略吧

Conversation info (untrusted metadata):
```json
{
  "message_id": "ija83cteqiyzbj4secdkp4exrw",
  "sender_id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "sender": "@sysadmin",
  "timestamp": "Thu 2026-04-02 02:00 UTC",
  "group_channel": "#3xc9mexbqjnxigzqao9rmuz5ky__sszmqmwb9truuc384x4m8yydda"
}
```

Sender (untrusted metadata):
```json
{
  "label": "@sysadmin (3xc9mexbqjnxigzqao9rmuz5ky)",
  "id": "3xc9mexbqjnxigzqao9rmuz5ky",
  "name": "@sysadmin"
}
```

噢噢，我懂了，那个是之前的server地址，忽略吧
assistant: 行，那就对上了：你手机里还留着旧的 server 地址，所以才会报证书无效。

你把客户端的服务器地址改成现在这台的正式入口就行：
- `https://myai.westus2.cloudapp.azure.com`

改完如果还弹证书问题，再跟我说，我再帮你看是不是缓存/代理/证书链导致的。
