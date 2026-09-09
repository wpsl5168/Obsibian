---
title: 多Agent SDLC闭环与并行开发流程设计(细化版)
created: 2026-06-14
updated: 2026-06-14
type: research
tags: [research, workflow]
status: draft
---

# 多 Agent SDLC 闭环 + 并行 + 依赖检测(源码级细化)

> 第二版。所有命令/行为均经本机 kanban 源码与 `--help` 实测验证,标注「✅实测」的可直接敲。

## 0. 核心认知更新(读完源码后的关键发现)

**最重要的一条**:你之前担心的「依赖检测」「门禁」**不是靠 agent 自觉遵守 SOP,而是 kanban 内核在数据库事务层强制的硬约束**。这彻底改变方案性质——不是"约定流程",是"机制保证"。

3 个内核级硬保证(源码定位):
1. **父依赖门禁是结构性不变量**(`kanban_db.py:2988` 注释原文:"single enforcement point")。任何卡要从 `ready→running`,只要有一个父卡没 `done/archived`,内核**直接拒绝认领并把它打回 todo**,记 `claim_rejected / parents_not_done` 事件。手动 SQL 也绕不过。
2. **建依赖边自动检测环**(`kanban_db.py:2420` `_would_cycle`)。`kanban link A B` 若 B 已是 A 的祖先,直接报错 "would create a cycle"。**你不可能手撸出环**。
3. **ready 自动重算**(`recompute_ready`)。父卡一旦 `done`,内核自动把满足条件的子卡 `todo→ready`,dispatcher(嵌在 gateway,60s tick)随即派发。**不需要手动 unblock**。

结论:**你的 kanban 本质就是一个带强制依赖 DAG 的工作流引擎**,Spec-Kit/BMAD 那套规格驱动 + 门禁 + 并行,它原生支持。缺的只是「把闭环写成标准动作」。

---

## 1. 全流程闭环(每个功能项,源码级精确)

### 阶段总览
```
[1]SPECIFY → [2]DECOMPOSE+DAG → [3]并行IMPLEMENT(内核依赖门禁)
  → [4]REVIEW(architect+qa) → [5]FIX → [4']复评 → [6]SMOKE → [7]MERGE&PUSH → 下一项
```

### [1] SPECIFY —— 规格化(architect)
**命令(✅实测)**：`hermes kanban specify <task_id>`
**真实行为**(源码 `kanban_specify.py:142`)：
- 仅对 **triage 列**的卡生效(`status='triage'` 才行,否则报错)。
- 调辅助 LLM 把粗想法 → 收紧的规格化描述(含验收标准)。
- 把卡 `triage → todo`,**不建子卡**(单卡原地升级)。
**DoR 门禁**(architect 人工签字,checklist 注入卡描述)：
- 验收标准(AC)明确且**可自动化验证**
- 依赖已识别
- 技术方案定(2-3 候选对比,符合老王红线:钱/数据/不可逆请示)

### [2] DECOMPOSE —— 拆分 + 自动建 DAG(architect)
**命令(✅实测)**：`hermes kanban decompose <task_id>`
**真实行为**(源码 `kanban_decompose.py` 头注释)：
- 读你的 **profile 花名册(name+description)**,调 LLM 返回任务图 JSON。
- **原子地**:建所有子卡 → `link` 到 root 下 → root `triage→todo`。
- **root 不死**:它成为所有叶子的父,全图完成后 root 唤醒,其 assignee(编排 profile)判定是否真完成、可追加任务。← 这就是你要的"做完一项继续下一项"的内核机制。
- `fanout=false` 时退化成 specify(不建子卡)。
- LLM 选了不存在的 profile → 自动改写成 `default_assignee`,**子卡绝不会 assignee=None**(避免你 kanban 第②坑:unassigned 永远 skip)。
**依赖检测**:decompose 自动建父子边;跨子任务的额外依赖用 `kanban link <前置> <后继>` 手补,**内核自动查环**。

### [3] IMPLEMENT —— 并行执行(developer / copilot 并行,内核管依赖)
**并行机制(内核原生,无需手动调度)**:
- 入度=0 的子卡 → 内核自动置 `ready` → dispatcher 60s tick 派给对应 profile worker → 多 worker **天然并行**。
- 有前置的子卡 → 内核保持 `todo`(因父未 done)。父 `done` 瞬间 → 自动 `ready`。**你什么都不用做**。
- 每个 worker 在**独立 workspace**(`claim` 原子认领)隔离跑,TDD:先测→实现→自测。
**两个执行手分工**:
- `developer`(opus):核心逻辑、需深推理的模块。
- `copilot`(Copilot CLI,已装登录):`delegate_task(acp_command='copilot')`,样板/CRUD/测试脚手架,分担并行度。
**重度并行也可一键 swarm**(✅实测语法)：
```bash
hermes kanban swarm "实现用户认证模块" \
  --worker developer:"登录API:auth-login" \
  --worker copilot:"JWT中间件:auth-jwt" \
  --verifier qa --synthesizer architect
```
⚠️ 前提:worker 间真无依赖。若 login 依赖 jwt,**必须 jwt 先单独跑完**,否则并行=冲突。

### [4] ARCHITECT REVIEW —— 质量门禁(architect + qa 小贝 8 维度)
- 子卡完成 → qa profile 8 维度评审 + architect 终审。
- **Quality Gate checklist**(固化,不再每次重定义):
  - [ ] 逐条对照 AC
  - [ ] 测试覆盖核心路径,全绿
  - [ ] 无新增 lint/类型错误
  - [ ] 符合现风格(老王:最小改动)
  - [ ] 安全(注入/越权,如涉及)
  - [ ] 性能无回退
  - [ ] 文档充分 + **交付去 AI 化**
  - [ ] 未破坏依赖项
- **失败处理**:`hermes kanban block <子卡> "评审未过:<清单>"` → 卡进 blocked,产出 fix 清单。

### [5] FIX REVIEW —— 修评审结果(developer)
- developer 按 block 时记的清单逐条修。
- 修完 `hermes kanban unblock <子卡> --reason "已修:<项>"` → 回 [4'] 复评。
- **轮次上限 2**(建议):超 2 轮 fix→review 仍不过 → 升级老王拍板,别死循环烧 credits。

### [6] SMOKE TEST —— 冒烟门禁(独立 gate,developer/qa)
- 所有子卡 done、root 唤醒后,做**集成级冒烟**(非单元):
  - [ ] 服务起得来(pm2 reload / 健康检查端点 200)
  - [ ] 核心用户路径端到端跑通
  - [ ] 关键断言通过(真实环境,非 mock)
- 失败 → 定位是哪个子卡的锅 → `block` 对应卡回 [3]/[5]。

### [7] MERGE & PUSH —— 收口(developer)
- 冒烟过 → 合并 → `git commit + push`,**看 SHA 确认**(老王红线:远程完成=看到 SHA)。
- root 卡 done → 编排者(小虾)judge:本 feature 真完成 → 取下一个 triage 卡,回 [1]。

---

## 2. 依赖检测与并行——机制细节

### DAG 怎么建
1. `decompose` 自动建 root→子 的父子边。
2. 子任务间的横向依赖,手补:`hermes kanban link <前置id> <后继id>`(✅实测,自动查环)。
3. 查看依赖与状态:`hermes kanban show <id> --json` / `hermes kanban list`。

### 并行批次怎么定(其实内核自动,但你要会读)
- 内核按「父全 done 才 ready」自动分层放行 ≈ 拓扑排序。
- 第 0 层(无父)= 首批并行;父 done 后下一层自动 ready = 第二批。
- **你只需建对 link,批次内核自己算**。

### 想"预演"依赖是否卡得对
`hermes kanban promote <id> --dry-run`(✅实测)：不改状态,验证这卡能否放行;`--force` 可强制越过未完成父依赖(慎用,等于手动拆门禁)。

### 老王 kanban 三坑(memory + 源码双重确认,务必避开)
1. **禁起独立 `kanban daemon`**:dispatcher 已嵌 gateway(`dispatch_in_gateway:true`,60s tick),独立 daemon 会抢 claim。
2. **notify-subscribe 必须在卡 done 之前建**:notifier 只在状态变化触发,已 done 订阅是 no-op。手撸 spawn:先订阅再 spawn。
3. **卡不流转**真因常是 `unassigned` 或 `workspace=scratch`:gateway 轮询但永远 skip。decompose 已自动保证非 None assignee,手建卡要自己盯。

---

## 3. 落地物:`wp-sdlc-loop` 编排 skill

主 agent(小虾)加载即按标准编排,内容:
1. 七阶段的**精确命令序列**(本文 §1,可直接复制执行)。
2. 三道门禁 **checklist 模板**(DoR / Quality Gate / Smoke)。
3. DAG 建立 + dry-run 预演 + 三坑规避**标准动作**。
4. 失败回退矩阵(哪个 gate 挂 → 回哪阶段)+ 2 轮升级老王触发条件。
5. 与现有 `kanban-orchestrator` / `role-*` / `team-sop` 心法衔接(不重复,只补闭环骨架)。

### 候选方案对比(选型,老王拍板)
| 方案 | 做法 | 优 | 缺 | 适用 |
|---|---|---|---|---|
| **A 纯SOP skill** | 闭环写 skill,小虾按本文命令编排 | 零新依赖,内核已强制依赖/门禁,完全符合不改源码红线 | 阶段衔接靠编排者执行 | **强烈推荐** |
| B swarm重度 | 每feature一条swarm打包 | 一键fan-out | 固定 worker→verify→synth,门禁/多轮回退表达弱 | 子任务纯并行无依赖时点用 |
| C 引入Conductor | YAML声明workflow | 路由可视化 | 新外部依赖,与kanban重叠,违背最小改动 | 暂不 |

---

## 4. 待老王拍板(5 项)
1. **选型**:A(推荐)/ B / C。
2. **冒烟边界**:独立 gate(建议)vs developer 顺手。
3. **评审轮次上限**:建议 2 轮升级你。
4. **Copilot CLI 入列**:是否当第 2 并行执行手分担 worker(提并行度,qa 把关质量)。
5. **是否落地**:拍板后我写 `wp-sdlc-loop` skill + 在 openhippo 板跑一个真实小 feature 走完整闭环验证。

---

## 5. 行业共识对标(Anthropic vs Cognition vs LangChain)—— 关键修正

### 三方一手立场
| 来源 | 立场 | 核心论据 |
|---|---|---|
| **Anthropic**(多agent research) | 多agent有效,**但限读不限写** | orchestrator-worker,90.2%↑;但原文红线:"需要所有agent共享同一上下文、或agent间多依赖的领域,不适合多agent" |
| **Cognition/Devin**(Don't Build Multi-Agents) | 写代码**默认单线程** | 并行写会乱:两subagent各写一半,风格/假设冲突(Flappy Bird例:鸟和背景两种画风)。跨agent上下文传递是**未解难题** |
| **LangChain**(调和) | **读密集 vs 写密集是分水岭** | 读可并行;写并行=双重难题(传上下文+合并冲突)。"actions carry implicit decisions, conflicting decisions carry bad results" |

### 铁打的行业共识(三方一致)
1. **Context Engineering 是第一工程**:不是模型笨,是上下文没喂对。
2. **读可并行,写要谨慎并行**:Anthropic 自己的 research 系统——研究(读)多agent并行,但**写报告(synthesis)故意用单个agent一次性完成**。
3. **写密集任务默认单线程**;要并行,前提是子任务**完全独立**(Cognition 几乎反对一切多写agent)。

### 老王踩的坑 = 教科书级失败模式(有论文背书,不是你操作问题)
> 两个 VSCode session 并行写同一项目 → 正中 Cognition/LangChain 警告:**write-heavy 并行 + 上下文不共享**。两个 session 互相看不见对方改了啥,基于冲突的隐含假设各写各的 → 必乱。这是**行业公认当前做不好**的事。

### 本方案是否行业共识?—— 分两半
**✅ 对齐共识的部分**:
- orchestrator-worker(小虾编排+worker)= Anthropic 蓝图。
- 规格先行 `specify` / DoR 门禁 = Context Engineering 落地。
- **kanban 内核强制依赖 DAG = 恰好解决 Cognition 最担心的"冲突"**——只有依赖切干净的卡才放行并行,这是你相对裸 VSCode 多开的**结构性优势**。
- 评审/冒烟由 architect 单点收口 = Anthropic 的 synthesis 单agent 模式。

**⚠️ 需修正的部分(原方案 [3] 偏激进)**:
- 原方案让 developer+copilot **并行写代码**——若两卡碰同一文件/同一模块,就是 Cognition 反对的 write-heavy 并行。
- **修正铁律**:并行的必须是**文件级不重叠的独立模块**;同文件/同模块**永远串行**。依赖 link 要切到文件粒度,不只是逻辑粒度。
- **能并行的典型**:auth模块 vs 支付模块 vs 前端组件(物理隔离)。**不能并行的**:同一个 service 的不同方法、同一个组件的样式+逻辑。
- copilot 入列价值降级:不是"加并行写手",而是当**探索/读 worker**(查代码、写测试脚手架、出初稿)更安全;核心写仍 developer 单线程为主。

### 修正后的稳态架构(对齐三方共识)
```
并行层 = 读/探索/独立模块(安全并行)
  ├─ 多 worker 查代码、调研、写测试、独立模块初稿
串行层 = 核心写(单 agent 主线,Cognition 派)
  └─ 同模块/同文件改动,developer 单线程顺序做
收口层 = 单 agent synthesis(Anthropic 派)
  └─ architect 评审 + 集成 + 冒烟,一个脑子收口避免冲突
```
**一句话**:并行用在"读和物理隔离的写",串行用在"耦合的写",收口永远单agent。kanban 依赖门禁是你执行这条线的内核保障。

---

## 6. 待老王拍板(更新)
1. **架构定调**:接受"并行限于独立模块 + 耦合写串行 + 单agent收口"的修正版?(我强烈建议,对齐三方共识)
2. **选型**:A 纯SOP skill(推荐)/ B / C。
3. **冒烟边界**:独立 gate(建议)。
4. **评审轮次上限**:2 轮升级你。
5. **copilot 定位**:降级为读/探索/初稿 worker(建议),非并行写手。
6. **是否落地**:写 `wp-sdlc-loop` skill + openhippo 板跑真实小feature验证。

---

## 信源
- 本机源码:`hermes_cli/kanban_specify.py` / `kanban_decompose.py` / `kanban_db.py`(依赖门禁 2988、查环 2420、ready重算 2884)
- Anthropic《How we built our multi-agent research system》(orchestrator-worker,90.2%,多依赖不适合多agent)
- Cognition《Don't Build Multi-Agents》(context engineering,并行写会乱,默认单线程)
- LangChain《How and when to build multi-agent systems》(读密集 vs 写密集分水岭,调和两派)
- GitHub Spec-Kit / BMAD Method / MS Conductor 2026-05
