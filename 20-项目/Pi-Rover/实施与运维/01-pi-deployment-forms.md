---
title: Pi 5 本地部署形式详解
created: 2026-04-23
updated: 2026-09-09
type: entity
tags: [pi-rover]
status: draft
oversized_ok: true
date: 2026-04-23
---

> 上游: [[20-项目/Pi-Rover/INDEX.md|Pi-Rover项目首页]] · [[20-项目/Pi-Rover/调研/设计模式/03-hybrid-brain.md|混合脑架构]]
> 关联: [[20-项目/Pi-Rover/决策/99-decision-matrix.md|决策矩阵]]

# 本地部署形式：Pi 5 完整方案

> 锁定方案: 混合脑(03) + 分层反射(04) — 本地脑放Pi 5 8GB
> 本文回答: Pi 5上"操作系统/启动介质/运行时/服务管理/目录结构"五大问题
> 信息源: Pi官方/Arm Learning/Hailo官方/Reddit r/ROS 2025年实测

---

## 一、操作系统选型 (5选1)

| 系统 | 内核 | 包管理 | Pi 5支持 | ROS 2支持 | Hailo驱动 | 适用 |
|---|---|---|---|---|---|---|
| **Raspberry Pi OS Lite (Bookworm 64-bit)** ★ | Linux 6.6 | apt | 官方一等公民 | 需手动 | ✅ 官方包`hailo-all` | **本项目主推** |
| Raspberry Pi OS Full (有桌面) | 同上 | apt | 同上 | 同上 | 同上 | 调试期/偶尔需要GUI |
| Ubuntu Server 24.04 LTS | Linux 6.8 | apt | 官方支持 | ✅ Jazzy原生apt | ⚠️ 需手动编译 | 后期上ROS 2可考虑 |
| DietPi | 同Pi OS | apt | 良好 | 需手动 | 需手动 | 极致省资源(~150MB空闲) |
| Ubuntu Core 24 | snap-only | snap | 实验性 | snap版 | 难 | 不推荐 |

### 决策建议

**Phase 1-3 用 Raspberry Pi OS Lite (Bookworm 64-bit)**
- 理由1: Hailo官方驱动 `apt install hailo-all` 一行装好
- 理由2: GPIO/I2C/SPI/CSI 全部out-of-box，零配置
- 理由3: 社区生态最大，遇坑能搜到答案
- 理由4: 官方维护，长期兼容性最好

**Phase 4+ 引入ROS 2时**:
- 选项A: 留在Pi OS，从源码编译ROS 2 Jazzy (麻烦但OS不动)
- 选项B: 切到Ubuntu 24.04 (ROS 2 Jazzy原生支持，但Hailo驱动要自己来)
- **推荐A**: 不要为ROS 2换OS，Hailo驱动太重要

### 为什么不用桌面版

- 桌面环境吃 ~500MB RAM，跑LLM很吃亏
- 服务器型机器人不需要GUI，远程SSH+Web仪表盘就够
- 调试时临时 `apt install lxde-core` 装个轻量桌面也行

---

## 二、启动介质 (3选1)

| 介质 | 速度 | 寿命 | 价格 | 推荐 |
|---|---|---|---|---|
| microSD (A2 U3) | ~100 MB/s | ⚠️ 频繁写易坏 | ¥50-100 | 应急/不推荐主用 |
| **NVMe SSD (M.2 HAT)** ★ | 800 MB/s+ | 高 | ¥150 (256GB) + ¥150 (HAT) | **强烈推荐** |
| USB 3 SSD | 400 MB/s | 高 | ¥200 | 备选，占USB口 |

### 主推: NVMe SSD

**硬件**:
- Pimoroni NVMe Base 或 Pi官方M.2 HAT+ (¥150)
- Kioxia/西数 256GB NVMe (¥150)

**注意Hailo HAT和NVMe HAT会冲一个PCIe口**！
- 解法1: **AI HAT+ (Pi官方双HAT)** 已集成 Hailo + NVMe，省心 (¥600-900)
- 解法2: 双层叠装 (M.2 HAT在下，Hailo在上) — 需要分PCIe lane
- 解法3: NVMe走 USB-to-NVMe 转接 (略慢但解耦)

**Phase 1可以先用SD卡**:
- microSD跑通基础流程
- 确定方案后再花¥300升级NVMe
- SD卡作冷备份镜像

### 启动顺序设置

```bash
sudo raspi-config
# Advanced Options → Boot Order → NVMe/USB Boot
# 或: sudo rpi-eeprom-config --edit
# 改: BOOT_ORDER=0xf416  (NVMe优先, SD兜底)
```

---

## 三、运行时形态 (4选1)

这是部署形式的核心选择：**裸机 / systemd / Docker / k3s**

### 形式A: 裸机 (Bare-metal)
**直接在OS上 `python rover.py` 跑**

```bash
# 极简，适合首日调试
cd ~/rover && python -m rover.main
```

✅ 优势: 启动快、调试直接、零overhead
❌ 缺陷: 不能开机自启、崩了不重启、依赖污染主系统、回滚困难

**适用**: 开发调试期 (Phase 1前2周)

---

### 形式B: systemd Service ★ 主推

**为每个长期进程写systemd unit，让OS看护**

典型服务拓扑（推荐）：
```
rover-safety.service    L0安全反射 (永不停)
rover-ollama.service    本地LLM后端
rover-agent.service     Hermes Agent主进程
rover-vision.service    Hailo视觉推理 (按需)
rover-bridge.service    硬件桥(GPIO/Camera) 
rover-dashboard.service Web仪表盘
```

示例 unit:
```ini
# /etc/systemd/system/rover-agent.service
[Unit]
Description=Pi-Rover Hermes Agent
After=network.target rover-ollama.service
Requires=rover-ollama.service

[Service]
Type=simple
User=pi
WorkingDirectory=/opt/rover
Environment="HERMES_HOME=/opt/rover/.hermes"
ExecStart=/opt/rover/.venv/bin/python -m rover.agent
Restart=always
RestartSec=5
# 资源限制 (防LLM吃爆内存)
MemoryMax=4G
CPUQuota=300%
# 日志走journald
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now rover-agent
journalctl -u rover-agent -f  # 看实时日志
```

✅ **优势**:
- 开机自启
- 崩溃自动拉起
- 资源限制 (MemoryMax/CPUQuota)
- 启动顺序 (After/Requires)
- 统一日志 (journald)
- Pi社区/Hailo官方都用这个方式 (HAILO论坛实测)

❌ **缺陷**:
- 依赖直接装在主机，污染系统
- 多版本切换难
- 跨机迁移要重装

**适用**: **本项目Phase 1-3主力部署形式**

---

### 形式C: Docker Compose

**每个服务一个容器，docker-compose编排**

```yaml
# /opt/rover/docker-compose.yml
version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    ports: ["11434:11434"]
    volumes: ["./ollama:/root/.ollama"]
    deploy:
      resources:
        limits: { memory: 5G }
    restart: unless-stopped
  
  agent:
    build: ./agent
    depends_on: [ollama]
    devices:  # 关键: 透传硬件
      - /dev/gpiomem:/dev/gpiomem
      - /dev/i2c-1:/dev/i2c-1
      - /dev/video0:/dev/video0
      - /dev/hailo0:/dev/hailo0   # Hailo设备
    volumes:
      - ./data:/app/data
      - /sys/class/gpio:/sys/class/gpio
    privileged: false  # 尽量不要全特权
    restart: unless-stopped
  
  dashboard:
    image: rover/dashboard:latest
    ports: ["8080:8080"]
    restart: unless-stopped
```

✅ **优势**:
- 依赖隔离，不污染主机
- 跨Pi复制 = `docker compose up -d`
- 版本管理 (image tag)
- Towards AI 的Hailo+YOLO教程就是Docker方案

❌ **缺陷**:
- 硬件透传配置繁琐（GPIO/I2C/Camera/Hailo都要单独传）
- Hailo驱动主机仍要先装 (容器内装不了内核模块)
- 启动比systemd慢
- 内存overhead ~200MB
- ARM64镜像生态比x86小

**Hailo Docker实测注意**:
- 主机必须先 `apt install hailo-all` 装内核模块
- 容器再装 `hailo-rt` Python包
- `/dev/hailo0` 必须透传

**适用**: 跨车批量部署、需要严格依赖隔离时 (Phase 4+ 多车规模)

---

### 形式D: k3s (轻量Kubernetes)

```bash
curl -sfL https://get.k3s.io | sh -
```

✅ 多车集群编排、滚动升级
❌ 单车杀鸡用牛刀，吃 ~500MB RAM

**适用**: Phase 5+ 多车 (>3台) 才考虑

---

### 部署形式对比矩阵

| 维度 | 裸机 | **systemd** | Docker | k3s |
|---|---|---|---|---|
| 启动速度 | 即时 | 即时 | 5-15s | 30s+ |
| 内存overhead | 0 | 0 | ~200MB | ~500MB |
| 开机自启 | ❌ | ✅ | ✅ | ✅ |
| 崩溃重启 | ❌ | ✅ | ✅ | ✅ |
| 硬件访问 | 原生 | 原生 | 需透传 | 需透传 |
| 依赖隔离 | ❌ | 中(venv) | ✅ | ✅ |
| 跨机复制 | 难 | 中 | ✅ | ✅ |
| 学习曲线 | 0 | 低 | 中 | 高 |
| 社区案例 | 多 | 极多 | 多 | 少 |

**本项目结论**: **Phase 1-3 用 systemd**，Phase 4+ 视情况引入Docker for可移植性。

---

## 四、Python环境管理

### 方案: uv + venv (强烈推荐)

```bash
# 装 uv (Astral, 比pip快10x)
curl -LsSf https://astral.sh/uv/install.sh | sh

cd /opt/rover
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt

# pyproject.toml 锁版本
uv pip compile requirements.in -o requirements.txt
```

**为什么uv**:
- 比pip安装快10-20x，Pi上CPU慢，节省时间显著
- 原生支持lockfile
- 兼容pip生态

### 关键依赖列表

```text
# requirements.in
hermes-agent          # 你的Agent runtime
ollama                # 本地LLM客户端
openai                # 兼容Ollama的OpenAI SDK
httpx                 # 异步HTTP
fastapi               # Web仪表盘后端
uvicorn               # ASGI server
sqlalchemy            # SQLite ORM (events表)
gpiozero              # Pi GPIO高级API
picamera2             # Pi Camera Module
opencv-python-headless # 图像处理(无GUI)
hailo-rt              # Hailo Python运行时 (从.whl装)
sounddevice           # 麦克风采集
pvporcupine           # 关键词唤醒 (Picovoice)
piper-tts             # 离线TTS
faster-whisper        # 比openai-whisper快
paho-mqtt             # MQTT (远程控制可选)
```

---

## 五、目录结构 (FHS规范)

```
/opt/rover/                  ← 主代码 (用/opt而非/home)
├── .venv/                    Python虚拟环境
├── pyproject.toml
├── rover/
│   ├── __init__.py
│   ├── agent.py             Hermes Agent入口
│   ├── safety/              L0反射层
│   │   └── daemon.py
│   ├── router/              路由器(本地vs云端)
│   ├── skills/              本地Skills
│   │   ├── motor.py
│   │   ├── camera.py
│   │   ├── vision_hailo.py
│   │   └── speech.py
│   └── bridge/              硬件抽象层
├── models/                  本地LLM模型 (软链到/var/lib/ollama)
├── hef/                     Hailo .hef模型文件
└── tests/

/etc/rover/                   ← 配置 (可被apt-conf管理)
├── rover.toml               主配置
└── secrets.env              API key等

/var/lib/rover/               ← 运行时数据 (可备份)
├── events.db                SQLite事件流
├── memory.db                短期记忆
└── kb.db                    长期知识库

/var/log/rover/               ← 日志 (logrotate管理)
└── (主要走journalctl, 这里只放特殊日志)

/etc/systemd/system/          ← Service unit
├── rover-safety.service
├── rover-ollama.service
├── rover-agent.service
└── ...
```

**为什么用 /opt 而不是 /home/pi**:
- 系统级服务的标准位置
- 升级Pi OS不会动到
- 多用户场景清晰
- systemd User= 可指定运行身份

---

## 六、网络与远程访问

### 推荐三件套

1. **Tailscale** (最强组合): 零配置WireGuard，给Pi一个固定虚拟IP，全球可达
   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   sudo tailscale up
   ```

2. **MQTT Broker** (可选): Mosquitto做远程控制总线
   ```bash
   sudo apt install mosquitto mosquitto-clients
   ```

3. **mDNS** (本地网络): `rover.local` 直接访问
   ```bash
   sudo apt install avahi-daemon
   sudo hostnamectl set-hostname rover
   ```

### Web仪表盘
- FastAPI后端 + Vue/Svelte前端
- WebSocket推实时摄像头/状态
- 端口8080，Tailscale下任意设备可看

---

## 七、模型管理

### Ollama (本地LLM)

```bash
curl -fsSL https://ollama.com/install.sh | sh

# 模型放在SSD
sudo mkdir -p /var/lib/ollama
sudo systemctl edit ollama
# 加: Environment="OLLAMA_MODELS=/var/lib/ollama"

# 拉模型
ollama pull qwen2.5:1.5b-instruct-q4_K_M  # 路由器, 1GB
ollama pull qwen2.5:3b-instruct-q4_K_M    # 主对话, 2.5GB

# 预热(避免冷启动)
ollama run qwen2.5:3b "你好" 

# 设置常驻 (防被卸载)
# OLLAMA_KEEP_ALIVE=24h 写入service
```

### Hailo模型管理

```
/opt/rover/hef/
├── yolov8s.hef         物体检测 (~10MB, INT8)
├── yolov8n_pose.hef    姿态识别
└── face_recognition.hef
```

模型通过 `hailo_model_zoo` 编译，或直接下载预编译.hef。

### Whisper (语音识别)
```
/opt/rover/models/whisper/
└── ggml-small.bin      466MB, faster-whisper SMALL足够
```

### Piper (TTS)
```
/opt/rover/models/piper/
├── zh_CN-huayan-medium.onnx  60MB 中文女声
└── en_US-amy-medium.onnx     英文备用
```

---

## 八、典型部署流程 (Day 1 实操)

```bash
# 1. 烧录Pi OS Lite 64-bit到SD/NVMe
#    (Raspberry Pi Imager → 设置好用户/SSH/WiFi)

# 2. 首次SSH登录后基础设置
sudo apt update && sudo apt full-upgrade -y
sudo raspi-config  # 启用SSH/I2C/SPI/Camera, 扩展文件系统

# 3. 装关键驱动
sudo apt install -y git python3-venv python3-pip                     i2c-tools libcamera-tools                     hailo-all  # Hailo整套
sudo reboot

# 4. 验证Hailo
hailortcli scan  # 应输出 Device 0000:01:00.0

# 5. 装Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 6. 装uv + 项目代码
curl -LsSf https://astral.sh/uv/install.sh | sh
sudo mkdir -p /opt/rover && sudo chown $USER /opt/rover
cd /opt/rover
git clone https://github.com/wpsl5168/pi-rover.git .
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# 7. 装systemd services
sudo cp deploy/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now rover-safety rover-ollama rover-agent

# 8. 验证
systemctl status rover-agent
curl http://rover.local:8080/health
```

---

## 九、本项目最终选定栈

| 层 | 选型 | 理由 |
|---|---|---|
| OS | **Raspberry Pi OS Lite Bookworm 64-bit** | Hailo一等支持 |
| 启动 | **NVMe SSD 256GB (Phase 2换)** | 速度+寿命 |
| 运行时 | **systemd services** | 简单可靠社区主流 |
| Python | **uv + venv** | 快+lockfile |
| LLM后端 | **Ollama** | 现成API兼容 |
| 视觉 | **Hailo-8L + YOLOv8s.hef** | 30fps实时 |
| 语音入 | **faster-whisper small** | 0.3x实时 |
| 语音出 | **Piper TTS 中文** | 离线自然 |
| 唤醒词 | **Picovoice Porcupine** | 低功耗 |
| 状态库 | **SQLite (WAL mode)** | 单机最优 |
| 远程 | **Tailscale** | 零配置全球可达 |
| 仪表盘 | **FastAPI + 简单SPA** | 轻量+你熟悉 |

---

## 十、常见踩坑 (前人血泪)

| 坑 | 现象 | 解法 |
|---|---|---|
| Hailo驱动版本错配 | `hailortcli scan` 找不到设备 | 必须主机`hailo-all`+容器`hailo-rt`版本对齐 |
| Pi 5 PCIe默认Gen2 | Hailo性能打折 | dtoverlay=pcie-32bit-dma + force-pcie-gen=3 |
| Ollama首次加载慢 | 用户等30s | 设OLLAMA_KEEP_ALIVE=24h常驻 |
| systemd权限问题 | GPIO访问拒绝 | User=pi + adm gpio i2c组授权 |
| picamera2与OpenCV冲突 | import错乱 | 用picamera2采集→numpy→opencv处理，不混用VideoCapture |
| 散热降频 | 满载10分钟性能砍半 | 主动风扇 + 大金属外壳 |
| SD卡写崩 | 几个月后系统挂 | 日志走tmpfs或直接NVMe |
| Hailo+NVMe抢PCIe | 只能用一个HAT | 上Pi官方AI HAT+ (集成版) |

---

## 下一步

- [ ] 老王拍板硬件清单（NVMe + Hailo方案）
- [ ] Phase 1启动: 先SD卡跑通基础流程
- [ ] 写 `deploy/systemd/*.service` 模板
- [ ] 写 `~/workspace/pi-rover/PROJECT_VISION.md` 把架构定下来
