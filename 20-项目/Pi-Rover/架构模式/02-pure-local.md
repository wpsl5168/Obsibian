---
title: 02-pure-local
created: 2026-04-23
updated: 2026-04-23
type: concept
tags: [pi-rover]
status: draft
---
# 模式02：纯本地架构

## 一句话
所有大脑跑在Pi上，永不上云，断网照常工作。

## 架构图

```
┌─────────────────────────────────────┐
│  🤖 Pi 5 8GB + Hailo-8L AI HAT+     │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  本地Agent Runtime            │  │
│  │  ├─ Hermes (本地实例)         │  │
│  │  ├─ Ollama: Qwen2.5:7B (Q4)   │  │
│  │  ├─ Hailo: YOLOv8 视觉        │  │
│  │  ├─ Whisper.cpp small         │  │
│  │  └─ Piper TTS                 │  │
│  └───────────────────────────────┘  │
│                                     │
│  Skills (本地):                     │
│   GPIO / Camera / Motor / KB        │
│                                     │
│  存储: SQLite + 本地RAG (Chroma)    │
└─────────────────────────────────────┘
        ↓ GPIO/CSI/I2C
   电机 摄像头 雷达 IMU
```

## 工作流程

```
用户: "找我的水杯"
  ↓ 本地Whisper.cpp识别 (~300ms)
  ↓ 本地Qwen2.5:7B规划 (~2s, 流式)
  ↓ 调用本地Skills:
    - vision_skill (Hailo YOLOv8 30fps)
    - move_skill (GPIO直控)
  ↓ 全程<5秒，全程在车内
  ↓ 本地Piper语音回复
```

## 优势

- **隐私无敌**：摄像头画面永远不出车
- **零API成本**：跑多少都不花钱
- **离线工作**：山里露营、停电、断网照样用
- **延迟可控**：本地推理100ms-2s，无网络抖动
- **数据安全**：符合GDPR等隐私法规
- **抗封锁**：完全不依赖海外API

## 致命缺陷

- **能力天花板低**：7B模型 vs Claude Sonnet差距巨大
  - 复杂推理：差
  - 长上下文：差（8K vs 200K）
  - 视觉理解：YOLO能识别物体，但"这是莫奈风格"做不到
- **算力捉襟见肘**：
  - Pi 5 CPU: Qwen 7B约 3-5 token/s
  - Hailo-8L: 13 TOPS仅够实时YOLO，跑不了大VLM
  - 8GB RAM上限：大模型+视觉+ROS同时跑会OOM
- **冷启动慢**：模型加载30-60s
- **更新复杂**：模型升级要进每台车
- **散热挑战**：满载时Pi 5会节流，需主动散热

## 适用场景

✅ 隐私强需求（家庭监控、医疗）
✅ 工业离线环境（矿井、远洋船）
✅ 已有强本地AI HAT且任务相对固定
✅ 教学/科研验证"边缘LLM"可行性

❌ 需要复杂推理/长对话
❌ 需要视觉深度理解（艺术、医学影像）
❌ 任务边界不确定，能力要持续扩展

## 实现要点

```bash
# Pi 5装机清单
sudo apt install -y ros-jazzy-ros-base
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:7b-instruct-q4_K_M  # 4.4GB
pip install whisper-cpp-python piper-tts

# Hailo运行时 (官方仓库)
sudo apt install hailo-all
# YOLOv8模型转换为.hef格式
```

```python
# 本地Skill示例
class LocalVisionSkill:
    def __init__(self):
        self.hailo = HailoInference("yolov8s.hef")
    
    def detect(self, frame):
        return self.hailo.run(frame)  # 33ms/帧
```

## 性能基准 (Pi 5 8GB实测，参考byteiota & Arm Learning Path)

| 模型 | 量化 | 内存 | 速度 | 体验 |
|---|---|---|---|---|
| Qwen2.5:1.5B | Q4 | 1.2GB | 12 t/s | 流畅，能力弱 |
| Qwen2.5:3B | Q4 | 2.5GB | 7 t/s | 可用 |
| Qwen2.5:7B | Q4 | 4.8GB | 3-5 t/s | 慢但能用 |
| Llama3.1:8B | Q4 | 5.5GB | 2-4 t/s | 边缘 |
| **YOLOv8s on Hailo** | INT8 | - | **30 fps** | 实时 |
| Whisper small | - | 1GB | 0.3x实时 | 可用 |
| Piper TTS | - | 200MB | 实时 | 自然 |

## 成本估算 (月)

| 项 | 月成本 |
|---|---|
| API调用 | ¥0 |
| 网络流量 | ¥0 |
| 电费 (Pi+Hailo约15W满载) | ~¥10 |
| **合计** | **¥10/月** |

一次性硬件成本: +¥450 (Hailo HAT) ≈ 半年回本 vs 纯云端

## 故障模式

| 故障 | 现象 | 缓解 |
|---|---|---|
| 模型OOM | swap爆，系统卡死 | 限制并发，分时调度 |
| 推理太慢 | 用户等10秒还没回 | 流式输出+预生成话术 |
| Hailo驱动崩 | 视觉失能 | CPU OpenCV兜底 |
| SD卡损坏 | 模型丢失 | NVMe SSD + 镜像备份 |

## 一句话评价

**纯本地是隐私神器，但能力天花板硬伤。** 适合特定垂直场景，但通用Agent小车跑不动复杂任务。

## 与本项目匹配度

⭐⭐⭐ (3/5) — 满足"本地优先"，但放弃"Agent级"能力。最佳用法是作为混合脑的"L2本地脑"基座。
