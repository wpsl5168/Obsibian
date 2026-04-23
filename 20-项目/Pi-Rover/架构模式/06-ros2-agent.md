# 模式06：ROS 2 + LLM Agent 架构

## 一句话
LLM作为ROS 2节点，与导航/感知/控制等成熟节点平等通信，享受整个ROS生态。

## 架构图

```
┌──────────────────────────────────────────────────────┐
│              ROS 2 Jazzy (DDS Middleware)             │
│  ┌────────────────────────────────────────────────┐  │
│  │  Topic / Service / Action / Parameter Bus      │  │
│  └────────────────────────────────────────────────┘  │
│   ↑↓        ↑↓         ↑↓         ↑↓        ↑↓     │
│ ┌──────┐ ┌──────┐ ┌──────────┐ ┌──────┐ ┌────────┐ │
│ │Camera│ │ LiDAR│ │Nav2      │ │Motor │ │LLM Agent│ │
│ │Node  │ │ Node │ │(BT-based)│ │Ctrl  │ │ Node   │ │
│ └──────┘ └──────┘ └──────────┘ └──────┘ └────────┘ │
│                                              ↑      │
│                                         Hermes/Ollama│
└──────────────────────────────────────────────────────┘
```

## 核心: LLM作为ROS节点

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from nav2_msgs.action import NavigateToPose

class LLMAgentNode(Node):
    def __init__(self):
        super().__init__('llm_agent')
        # 订阅用户语音/文本
        self.sub = self.create_subscription(String, '/user_input', self.cb, 10)
        # 调用Nav2 Action
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        # 订阅感知结果
        self.create_subscription(DetectionArray, '/detections', self.on_detect, 10)
    
    def cb(self, msg):
        # LLM决策
        plan = ollama.chat("qwen2.5:7b", f"用户说: {msg.data}, 你应该: ")
        # 执行Action
        self.nav_client.send_goal_async(parse_goal(plan))
```

## ROS 2带来什么

- **Nav2**: 工业级SLAM+路径规划+导航 (Behavior Tree based)
- **MoveIt 2**: 机械臂运动规划
- **TF2**: 多坐标系自动转换 (机器人/世界/相机)
- **rosbag2**: 完整任务回放，调试神器
- **rqt/Foxglove**: 可视化调试
- **Gazebo/Isaac Sim**: 仿真测试

## 优势

- **生态最全**: 30+年机器人工程沉淀
- **工业标准**: 业内通用，简历/合作友好
- **真SLAM**: Nav2开箱即用，不用造轮子
- **多语言**: C++/Python/Rust混编
- **仿真先行**: Gazebo里跑通再上车

## 致命缺陷

- **学习曲线极陡**: 概念多 (Topic/Service/Action/TF/QoS/Lifecycle...)
- **重**: 安装包GB级，启动复杂
- **过度工程化**: 玩具车用ROS像螺蛳壳里做道场
- **Pi 5吃力**: ROS+LLM+视觉同时跑，可能不够
- **调试痛苦**: 节点崩溃链式反应

## 适用场景

✅ 你打算长期搞机器人 (职业方向)
✅ 需要SLAM+导航+机械臂等复杂能力
✅ 团队/科研，要标准化协作
✅ 想用现成的Nav2省2个月

❌ 个人快速原型
❌ 任务简单 (只是遥控+对话)
❌ 想最小化运维

## 与其他模式的关系

- **可作为模式03/04的"运动控制底座"** — Nav2提供L1/L2能力
- **与模式05 BT原生集成** — Nav2的BT就是BehaviorTree.CPP

## 实现复杂度

| 阶段 | 周期 |
|---|---|
| ROS 2基础 | 2周 |
| Nav2配置+SLAM | 3-4周 |
| LLM节点集成 | 2周 |
| 调试稳定 | 持续 |

## 与本项目匹配度

⭐⭐⭐ (3/5) — Phase 4(SLAM/自动归位)再考虑引入。前期用Hermes+Skills即可，避免过早ROS化。

## 决策建议

**分两条路径**:
- **A路径**: 不用ROS，Hermes Skills直接GPIO控车 (Phase 1-3)
- **B路径**: 上ROS，用Nav2做导航 (Phase 4+)

老王这个项目，**先A后B**最划算。
