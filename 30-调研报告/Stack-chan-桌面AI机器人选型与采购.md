---
title: Stack-chan 桌面 AI 机器人选型与采购指南
date: 2026-05-14
tags: [硬件, 机器人, M5Stack, Stack-chan, AI-Agent, Hermes]
status: 调研完成
---

# Stack-chan 桌面 AI 机器人选型与采购指南

## 背景与目标

老王想在桌上养一个**可接入 Hermes Agent 的 AI 机器人**，能听话、说话、显示表情、转头看人，进阶版还能在桌面跑动避障。

**Stack-chan** 是日本工程师ししかわ (Shishikawa) 基于 M5Stack 开发的开源桌面机器人项目，社区活跃、扩展性强、价格亲民，是当前性价比最高的"可玩 AI 机器人"平台。

GitHub: <https://github.com/stack-chan/stack-chan>

---

## 候选品类对比（为什么选 Stack-chan）

| 类型 | 代表 | 价格 | 可装 Agent | 评价 |
|---|---|---|---|---|
| 开源 DIY | **Stack-chan (M5Stack)** ⭐ | ¥600-1300 | ✅ 完全开放 | **首选**：社区活跃、文档全、能折腾 |
| 开发者平台 | Reachy Mini (HuggingFace) | ¥2200+ | ✅ Python SDK | 工业级精致，贵 3 倍 |
| 半开放 | Looi Robot | ¥600-900 | ⚠️ 接 ChatGPT | 手机当大脑，封闭 |
| 情感陪伴 | Eilik / EMO / Ropet | ¥500-2000 | ❌ 不可编程 | 只能卖萌 |

---

## 主机选型

### 推荐：M5Stack CoreS3（¥350）

| 型号 | 价格 | 摄像头 | 麦 | 喇叭 | Stack-chan 适配度 |
|---|---|---|---|---|---|
| **CoreS3** ✅ | ¥350 | ✅ | ✅ | ✅ | 当前事实标准，固件/外壳全 |
| CoreS3 SE | ¥250 | ❌ | ✅ | ✅ | 砍摄像头，影响未来视觉 |
| CoreS3 Lite | ¥200 | ❌ | ❌ | ❌ | 不推荐做 Stack-chan |
| Core2 v1.1（老款）| ¥280 | ❌ | ✅ | ✅ | 教程多但被 CoreS3 取代 |
| Tab5（最新顶配）| ¥1200+ | ✅ | ✅ 阵列 | ✅ | 太新没适配，外壳少 |

**结论**：CoreS3 是当前甜蜜点，事实标准，多花 ¥100 比 SE 多个摄像头位，未来想做"看到人就打招呼"不会傻眼。

---

## 完整 BOM（按用途分层）

### 🧠 1. 主板（必需，1 个）
- **M5Stack CoreS3** ¥350

### 🎭 2. 舵机（必需，2 个，控头部 2 自由度）
- 入门：SG90 塑料齿 ¥10×2（抖、易坏）
- **推荐：MG90S 金属齿 ¥25×2**
- 顶配：FEETECH SCS0009 ¥80×2（串行总线、丝滑无声，但外壳孔位不同）

### 🔌 3. 舵机驱动（必需，1 个）
- **M5Stack Servo 2 Hat ¥80**（堆叠式，最干净）
- 备选：PCA9685 16 路驱动板 ¥20（要焊接）
- SCS0009 专用：FEETECH 总线驱动板 ¥50

### 🏠 4. 外壳（必需，1 套，3D 打印件）
- 自打印：¥0（GitHub 下 STL）
- 淘宝代打 PLA：¥50-80
- **推荐：套件包（含舵机座+螺丝）¥120-200**
- 顶配：树脂上色 ¥150-250

### 🔋 5. 电源（必需）
- CoreS3 内置 500mAh（30-60 min）
- **推荐外挂：Atomic Battery Base ¥80**（+200mAh）
- 桌面长跑：DinBase 5V 电源模块 ¥150

### 🔌 6. 线材（必需）
- USB-C 数据线（带数据，刷固件）¥15
- Grove 4Pin 线 20cm × 2-3 ¥10
- 杜邦线母对母 20cm × 1 包 ¥10

### 🛠 7. 工具（一次性，按需）
- PH00/PH0 螺丝刀 ¥20
- 镊子 ¥15
- 3M 双面胶 / 热熔胶枪 ¥30

---

## 套餐推荐

### 💎 标准 Stack-chan（¥660）— 桌面摆件 + AI 对话

```
M5Stack CoreS3              ¥350
MG90S 舵机 ×2               ¥50
Servo 2 Hat                 ¥80
外壳套件（含螺丝）          ¥150
USB-C 线 + Grove 线         ¥30
─────────────────────────────────
合计                        ¥660
```

能做：摆桌上转头、显示表情、说话、Hermes Agent 对话

### 🚗 可移动 AI 小车（¥1370）— Stack-chan + 桌面跑动

在标准版基础上加：

```
M5Stack RoverC Pro 底盘     ¥400  ← 麦克纳姆轮全向移动
Unit ToF 避障传感器         ¥80   ← 必加，否则会摔下桌
Atomic Joystick 遥控        ¥150  ← 调试时手动遥控比改代码快
额外电池模块                ¥80
─────────────────────────────────
追加 ¥710，总计 ¥1370
```

### 🎨 选配（按兴趣加）

| 配件 | 价格 | 用途 |
|---|---|---|
| Unit IR | ¥30 | 红外遥控家电 |
| Unit ENV III | ¥60 | 温湿度传感（"今天热不热"） |
| LED 灯环 | ¥40 | 装基座当氛围灯 |
| Unit 9DOF IMU | ¥120 | 姿态感知，"原地 90 度"更准 |
| UnitV2 AI 摄像头 | ¥350 | 跟随人脸/识别物体 |
| 激光雷达 LD06/LD19 | ¥400 | SLAM 建图（已超 ESP32 范畴） |

---

## 购买渠道

### 主机 + 官方配件：M5Stack 官方天猫旗舰店
- **店名：M5Stack 企业店**（认准卖家"深圳明栈信息科技有限公司"，M5Stack 母公司）
- 搜索：`M5Stack企业店` 或直接搜 `M5Stack CoreS3`
- ✅ 原厂正品 / 售后保障 / 顺丰发货
- ✅ 一站买齐：CoreS3 + Servo Hat + RoverC + Unit + 线材

### 备选官方渠道
- 立创商城（嘉立创旗下）：搜 M5Stack
- 京东：自营少，多是第三方，谨慎

### 外壳套件：淘宝
搜索词（按推荐度排）：
1. `stackchan 套件`
2. `stack chan diy`
3. `M5Stack 桌面机器人`

**挑店三看**：
- 销量 ≥ 50，评价 ≥ 4.9
- 有买家秀实物（避开只挂渲染图的）
- 备注里写明 **CoreS3 兼容**（不是只支持 Core2）

### 顶配舵机：飞特舵机
- 淘宝搜：`FEETECH SCS0009` 或 `飞特舵机 SCS0009`
- 官方店：飞特舵机（深圳飞特模型）

---

## 可移动 AI 小车搜索清单（下单照抄）

```
①  M5Stack CoreS3              → 「M5Stack企业店」
②  MG90S 舵机 9g 金属齿        → 销量高的随便买
③  M5Stack Servo 2 Hat         → 「M5Stack企业店」
④  stackchan 外壳 套件 CoreS3   → 销量 ≥ 50 + 评价 4.9 + 标 CoreS3 适配
⑤  M5Stack RoverC Pro          → 「M5Stack企业店」
⑥  M5Stack Unit ToF            → 「M5Stack企业店」
⑦  M5Stack Atomic Joystick     → 「M5Stack企业店」
⑧  M5Stack Atomic Battery Base → 「M5Stack企业店」
⑨  USB-C 数据线 带数据 1m       → 有数据传输标识的
⑩  Grove 4Pin 线 20cm 3根       → 「M5Stack企业店」
```

**省事策略**：①③⑤⑥⑦⑧⑩ 全在 M5Stack 企业店一单买齐凑单包邮；④ 单独淘宝搜套件包；②大头去官方店免去匹配麻烦。

**总订单数**：2 单（M5 官方 + 外壳店）

---

## 接入 Hermes Agent 方案

### 链路
```
Stack-chan(麦) → STT → HTTP/WS → Hermes API → TTS → Stack-chan(喇叭+表情+转头+轮子)
```

### 三种实施路径

#### 路径 ① 最快（1-2 天）：劫持 robo8080 固件
- 刷 robo8080 的 ChatGPT 固件
- 把 OpenAI endpoint 改成 Hermes `api_server`（已兼容 OpenAI API）
- STT/TTS 仍走 OpenAI 或换百度
- ✅ 不写代码，改 URL 即用
- ❌ 表情/转头是固件预设，不能由 agent 主动控制

#### 路径 ② 中等（3-5 天）：自写 M5Stack 固件
- PlatformIO Arduino 工程
- 录音→base64→POST `/v1/chat/completions` (multimodal)
- 解析返回的 TTS 音频流播放
- agent 回复里塞控制 token（如 `[head:left][face:happy][move:fwd:10]`），固件解析驱动舵机/表情/小车
- ✅ 完全 agent 驱动，能调所有 skill/记忆
- ❌ 要写 C++，调音频 buffer 烦

#### 路径 ③ 终极（1 周+）：瘦客户端
- Stack-chan 只做 IO（麦/喇叭/舵机/屏幕/轮子）
- WebSocket 长连到 Hermes gateway 的 `/stackchan` 端点（走 plugin，不改 hermes 源码）
- Hermes 端 plugin：管表情状态机、舵机动作库、TTS 流式推送、小车控制
- ✅ 最优雅，未来加视觉/多机器人都好扩
- ❌ 工作量最大

### 推荐路径
**先 ① 验证链路（2 天玩起来），再跳到 ③ 长期形态。**  
③ 走 plugin 不改 hermes fork，符合"不改 hermes 源码"红线。

### Agent 决策示例
```
你说话 → Stack-chan 麦
       → Hermes (LLM 决策)
       → 返回 JSON: {"action":"move","dir":"forward","dist":10,"face":"happy"}
       → CoreS3 解析
         ├─ 驱动 RoverC 走 10cm
         ├─ 屏幕显示开心脸
         └─ 转头看说话方向
```

---

## 关键避坑

1. **CoreS3 vs Core2**：教程很多基于 Core2，下单前确认外壳/固件**支持 CoreS3**
2. **舵机选型**：SG90/MG90S 用 PWM，SCS0009 用串口，**外壳孔位不同**，混用要重新打印
3. **电源**：舵机吃电凶，CoreS3 内置电池跑不了多久，**建议外挂 Atomic Battery Base**
4. **USB-C 线**：山寨线常缺数据线芯，刷固件失败必查这里
5. **可移动版避障**：必加 ToF，否则桌面机器人会摔下桌（不是开玩笑）
6. **Tab5 别上**：太新无社区适配，第一台机器人先选踩坑少的

---

## 参考链接

- Stack-chan 主仓库：<https://github.com/stack-chan/stack-chan>
- robo8080 ChatGPT 固件分支（社区最火）：<https://github.com/robo8080>（搜 stack-chan-AI 等仓库）
- M5Stack 官方店：<https://shop.m5stack.com>
- M5Stack CoreS3 产品页：<https://docs.m5stack.com/en/core/CoreS3>
- M5Stack RoverC Pro：<https://docs.m5stack.com/en/app/roverc_pro>

---

## 后续 TODO

- [ ] 标准版下单（¥660）→ 收货
- [ ] 路径 ① 跑通：固件刷写 + Hermes API endpoint 替换
- [ ] 路径 ③ 设计：Hermes plugin 架构图 + WebSocket 协议
- [ ] 升级可移动版（¥710 追加）
- [ ] 视觉扩展：UnitV2 或 CoreS3 自带摄像头做人脸跟随
