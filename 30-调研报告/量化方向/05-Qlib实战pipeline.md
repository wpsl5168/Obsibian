# Qlib 实战 Pipeline(微软 AI 量化框架)

> 调研时间:2026-05 | Qlib v0.9+ | 43.1k★,2026-04 仍在更新

## 一、Qlib 是什么 & 不是什么

**是什么**
- 微软亚研院开源的 AI 量化研究框架,**重心是因子+ML+回测**
- 一个 `qrun config.yaml` 跑通"数据→特征→模型→回测→报告"全链路
- 数据层 + Alpha158/360 因子库 + 20+ ML/DL baseline 模型
- 配合 `microsoft/RD-Agent` 可做自动化 R&D(2024 新模块)

**不是什么**
- ❌ **不是实盘交易系统** — 没下单接口,要自接 MiniQMT/CTP
- ❌ 不是高频框架 — 设计是日频/分钟级
- ❌ 不是开箱即用的赚钱机器 — baseline 配置实际亏钱(见下文)

## 二、架构总览(7 大模块)

```
┌─────────────────────────────────────────────┐
│  Workflow (qrun + YAML)  ← 编排入口          │
└─────────────────────────────────────────────┘
       ↓
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Data    │→ │  Model   │→ │ Strategy │
│ Handler  │  │ (LGBM,   │  │ (Topk    │
│ Alpha158 │  │  GRU...) │  │  Dropout)│
└──────────┘  └──────────┘  └──────────┘
       ↓             ↓             ↓
┌──────────────────────────────────────┐
│  Backtest + Report  (回测+指标输出)   │
└──────────────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  RL Module  (订单执行,2022+ 新增)     │
└──────────────────────────────────────┘
```

**设计哲学**:配置即代码(YAML),所有组件可热替换(handler/model/strategy 都靠 `class+module_path+kwargs` 反射加载)。

## 三、安装与数据初始化

### 3.1 装包

```bash
# Python 3.8-3.11(3.12 有 numpy 兼容坑)
conda create -n qlib python=3.11 -y
conda activate qlib

pip install pyqlib                # 主包
pip install lightgbm xgboost      # GBDT 模型
pip install torch                 # 深度学习模型
```

### 3.2 拉 A股日线数据

```bash
# Qlib 官方维护的 A股数据(雅虎源,2008-至今,自动更新滞后约 1 周)
python -m qlib.run.get_data qlib_data \
  --target_dir ~/.qlib/qlib_data/cn_data \
  --region cn

# 美股
python -m qlib.run.get_data qlib_data \
  --target_dir ~/.qlib/qlib_data/us_data \
  --region us
```

数据格式:二进制 `.bin` + `instruments/csi300.txt`,加载速度比 pandas 快一个量级。

### 3.3 ⚠️ 数据坑 3 条

1. **官方数据是 Yahoo 源**,A股复权方式与国内不同(前复权 vs 后复权),做长周期回测前必须对齐
2. **数据滞后** — 官方仓库通常滞后 7-14 天,实盘必须接 Tushare Pro/AKShare 增量更新(`scripts/data_collector/yahoo/collector.py` 可改源)
3. **退市股缺失** — 默认数据集只含当前在市标的,**回测会有幸存者偏差**,跑长周期 alpha 失真严重

### 3.4 自建数据导入

```bash
# 把 CSV 转 qlib 二进制格式
python scripts/dump_bin.py dump_all \
  --csv_path ~/my_data/csv \
  --qlib_dir ~/.qlib/qlib_data/my_data \
  --include_fields open,close,high,low,volume,factor \
  --symbol_field_name symbol \
  --date_field_name date
```

## 四、Alpha158 因子库实战

### 4.1 Alpha158 包含什么

158 个因子分 5 类(都基于量价):

| 类别 | 代表因子 | 含义 |
|---|---|---|
| **K-Bar** | `KMID = (close-open)/open` | K线实体相对长度 |
| **Price** | `OPEN0 = $open/$close` | 开盘相对昨收 |
| **Volume** | `VMA5 = Mean($volume,5)/$volume` | 量比 |
| **Rolling Stats** | `STD5/STD10/STD20` | 滚动波动率 |
| **Reversal/Momentum** | `ROC5/ROC10/ROC60` | N日动量 |

**Alpha360** = 60 天 × 6 个原始量价字段 = 360 维原始时序,**给 DL 模型(GRU/Transformer)用**;Alpha158 是工程师手撸的 158 维特征,**给 LGBM 用**。

### 4.2 加自定义因子

```python
from qlib.contrib.data.handler import Alpha158

class MyHandler(Alpha158):
    def get_feature_config(self):
        fields, names = super().get_feature_config()
        # 加一个 60 日反转因子
        fields += ["-1 * Ref($close,60)/$close + 1"]
        names += ["REV60"]
        return fields, names
```

Qlib 用自家 DSL 表达因子(`$close` `Ref` `Mean` `Std` `Rank` `Corr`...),**所有算子向量化、滚动窗口自动对齐**,这是 Qlib 数据层最大价值。

## 五、训模型 baseline(20+ 可选)

官方 benchmarks 目录:

| 类别 | 模型 | 适配数据集 |
|---|---|---|
| 树模型 | **LightGBM**(王牌)、XGBoost、CatBoost | Alpha158 |
| 线性 | Linear、DoubleEnsemble | Alpha158 |
| MLP | MLP | Alpha158 |
| RNN | **GRU**、LSTM、ALSTM、TCN | Alpha360 |
| Transformer | Transformer、Localformer | Alpha360 |
| 图模型 | HIST、IGMTF、KRNN | 自定义 |
| 时序专用 | ADARNN、ADD | Alpha360 |

### 5.1 一行跑 LightGBM

```bash
cd examples
qrun benchmarks/LightGBM/workflow_config_lightgbm_Alpha158.yaml
```

完整 YAML(官方默认,可直接复制):

```yaml
qlib_init:
  provider_uri: "~/.qlib/qlib_data/cn_data"
  region: cn

market: &market csi300
benchmark: &benchmark SH000300

data_handler_config: &data_handler_config
  start_time: 2008-01-01
  end_time: 2020-08-01
  fit_start_time: 2008-01-01
  fit_end_time: 2014-12-31
  instruments: *market

port_analysis_config: &port_analysis_config
  strategy:
    class: TopkDropoutStrategy        # 每日选 top50,换出 5 只
    module_path: qlib.contrib.strategy
    kwargs:
      signal: <PRED>
      topk: 50
      n_drop: 5
  backtest:
    start_time: 2017-01-01
    end_time: 2020-08-01
    account: 100000000                # 1 亿初始资金
    benchmark: *benchmark
    exchange_kwargs:
      limit_threshold: 0.095          # 涨跌停 9.5%
      deal_price: close               # 收盘价撮合 ⚠️ 不真实
      open_cost: 0.0005               # 万 5
      close_cost: 0.0015              # 千 1.5(含印花税)
      min_cost: 5

task:
  model:
    class: LGBModel
    module_path: qlib.contrib.model.gbdt
    kwargs:
      loss: mse
      learning_rate: 0.2
      max_depth: 8
      num_leaves: 210
      lambda_l1: 205.6999
      lambda_l2: 580.9768
      colsample_bytree: 0.8879
      subsample: 0.8789
      num_threads: 20
  dataset:
    class: DatasetH
    module_path: qlib.data.dataset
    kwargs:
      handler:
        class: Alpha158
        module_path: qlib.contrib.data.handler
        kwargs: *data_handler_config
      segments:
        train: [2008-01-01, 2014-12-31]
        valid: [2015-01-01, 2016-12-31]
        test:  [2017-01-01, 2020-08-01]
  record:
    - class: SignalRecord
    - class: SigAnaRecord
      kwargs: {ana_long_short: false, ann_scaler: 252}
    - class: PortAnaRecord
      kwargs: {config: *port_analysis_config}
```

### 5.2 关键超参速查(LGBM)

| 参数 | 默认 | 调参方向 |
|---|---|---|
| `learning_rate` | 0.2 | 过拟合就降到 0.05-0.1 + 加 estimators |
| `max_depth` | 8 | 深度学习容易过拟合,A股建议 5-7 |
| `num_leaves` | 210 | 应 ≤ 2^max_depth,默认值偏激进 |
| `lambda_l1/l2` | 200/580 | A股噪声大,L2 调大(500-2000) |
| `min_data_in_leaf` | 20 | 加大到 100+ 减过拟合 |

## 六、🚨 baseline 真实结果(关键事实)

官方默认配置 LGBM + Alpha158 + CSI300 + 2017-2020 段实测:

```
IC:           0.0045        ← 极弱信号
ICIR:         0.056         ← 远低于 0.5 的"可用"门槛
Rank IC:      0.0048
mean:        -0.000280
annualized_return: -6.67%   ← 年化亏 6.67%
information_ratio: -0.94
max_drawdown: -32.56%       ← 回撤超 1/3
```

**结论:开箱即用的 Qlib baseline 在中证 300 上实际是亏钱的。**

**为什么?**
1. **默认参数是论文老版,2018-2020 段已经失效**(因子拥挤)
2. **撮合用 close 价**,看似温和实际有 lookahead bias
3. **涨跌停成交假设过于乐观** — 实盘买不进的票回测都成交了
4. **不考虑停牌/ST/退市**

**怎么改才能跑出正收益(过来人经验)**
- 训练窗口滚动(walk-forward),不要 fix 2008-2014
- 标的池换中证 500/1000(小票 alpha 更多,但 2024 后微盘股监管收紧)
- 加自定义因子(基本面、资金流)
- `deal_price` 改 vwap,加 5-10bp 滑点
- 加涨跌停过滤逻辑
- Top-N 改小(20→10),换手率高的情形 LGBM 衰减快

## 七、对接 MiniQMT 实盘(信号转下单)

Qlib 训完后,`SignalRecord` 会把每日预测分数存到 mlflow:

```python
from qlib.workflow import R

# 读出最新一天的预测分数
recorder = R.get_recorder(experiment_name="workflow")
pred = recorder.load_object("pred.pkl")  # MultiIndex: (date, instrument) -> score

today = pred.index.get_level_values("datetime").max()
today_pred = pred.loc[today].sort_values("score", ascending=False)
top20 = today_pred.head(20).index.tolist()  # ['SH600000', 'SZ000001', ...]
```

### 7.1 信号 → MiniQMT 下单(quant-qmt-proxy 桥)

```python
import requests
from datetime import datetime

QMT_PROXY = "http://192.168.1.50:8888"   # Windows 上跑 quant-qmt-proxy
ACCOUNT = "你的资金账号"

def qlib_code_to_qmt(code):
    """SH600000 → 600000.SH"""
    return code[2:] + "." + code[:2]

def rebalance(target_codes, total_cash=100000):
    # 1. 查当前持仓
    positions = requests.get(f"{QMT_PROXY}/positions",
                             params={"account": ACCOUNT}).json()
    holding = {p["code"]: p["can_use_volume"] for p in positions}
    
    # 2. 卖出不在 target 的
    for code, qty in holding.items():
        if code not in [qlib_code_to_qmt(c) for c in target_codes] and qty > 0:
            requests.post(f"{QMT_PROXY}/order", json={
                "account": ACCOUNT, "code": code,
                "direction": "SELL", "volume": qty,
                "price_type": "LATEST"
            })
    
    # 3. 等成交回报
    import time; time.sleep(5)
    
    # 4. 平均买入 target
    cash_per = total_cash / len(target_codes)
    for qlib_code in target_codes:
        qmt_code = qlib_code_to_qmt(qlib_code)
        price = requests.get(f"{QMT_PROXY}/tick",
                             params={"code": qmt_code}).json()["last"]
        qty = int(cash_per / price / 100) * 100
        if qty >= 100:
            requests.post(f"{QMT_PROXY}/order", json={
                "account": ACCOUNT, "code": qmt_code,
                "direction": "BUY", "volume": qty,
                "price_type": "LATEST"
            })

if __name__ == "__main__":
    # 14:50 调仓
    rebalance(top20, total_cash=100000)
```

**生产链路推荐**
```
crontab(每个交易日 14:50)
  → 加载 Qlib 模型 → 出 top-N
  → POST 到 quant-qmt-proxy
  → Windows QMT 执行下单
  → 微信/Telegram 推送成交回报
```

## 八、🚨 Qlib 三大坑(过来人血泪)

### 1. 数据质量陷阱
- 默认 Yahoo 数据**复权方式与国内主流不同**
- **没有 PIT(point-in-time)财报**,做基本面因子有未来函数
- **没有退市股** → 幸存者偏差
- **解决方案**:实盘前必须接 Tushare Pro / JQData 重做数据层

### 2. 过拟合陷阱
- **Alpha158 在样本内能跑出 Sharpe 2+**,样本外大幅衰减是常态
- 默认 `learning_rate=0.2 + num_leaves=210` 偏激进,很容易记住训练集噪声
- **识别信号**:验证集 IC 比训练集 IC 低 50%+ = 严重过拟合
- **解决方案**:walk-forward + Bagging + 强 L2 + 减少树深度

### 3. 回测失真陷阱
- `deal_price: close` = 收盘价撮合,**实盘做不到**(收盘后才知道收盘价)
- `limit_threshold: 0.095` = 简化的涨跌停判定,**没考虑停牌、ST、新股**
- 没有冲击成本模型 → 大资金回测漂亮实盘崩
- **解决方案**:改 vwap 撮合 + 加滑点 + 自写停牌过滤

## 九、Qlib RL 模块(订单执行,2022+)

新增的强化学习模块,主要做**订单执行优化**(不是策略本身):
- 任务:给定要买入 100 万股某票,如何在一天内拆单使冲击成本最小
- 框架:`qlib.rl` 提供 simulator + reward,可以试 PPO/DDPG
- 学术价值大,**实盘落地少**(机构有自家执行系统,散户没大单需求)

## 十、Qlib + LLM(2024-2025 新进展)

### RD-Agent(微软同期开源,与 Qlib 配套)
- GitHub `microsoft/RD-Agent` — 用 LLM **自动生成 Qlib 因子代码**
- 流程:LLM 读论文 → 生成因子 DSL → Qlib 跑回测 → 反馈给 LLM 迭代
- **学术 demo > 实战价值**(生成的因子大多平庸)

### LLM 文本因子(社区方向)
- 中金/华泰/国信内部都在做:LLM 抽公告/纪要 → 情感分 → 作为 Qlib 自定义因子
- **接入方式**:每日跑 LLM → 写入 CSV → `dump_bin` 导入 Qlib → 在 handler 里 join
- **老王的甜区**:这块对 AI Agent 友好,可做接单方向(给私募定制 LLM 因子 pipeline)

## 十一、社区现状(2026-05 update)

- **GitHub**:43.1k★,6.8k fork,2026-04-22 仍有 commit
- **open issues**:400(响应较慢,核心团队精力分到 RD-Agent)
- **更新节奏**:大版本一年 1-2 次,bugfix 持续
- **中文社区**:知乎/CSDN 教程多但散,推荐看官方 `examples/` 目录
- **替代品**:
  - 因子研究:**WorldQuant BRAIN**(平台版,机构友好)、**Alphalens**(独立因子分析)
  - 回测:**vnpy**(实盘优势)、**rqalpha**(米筐开源)
  - 一体化:Qlib 仍是 ML 派最完整的

## 十二、给老王的实操路线

```
Week 1: 装环境 + qrun 跑通 baseline LightGBM
        理解 IC/ICIR/年化/回撤含义
Week 2: 改 standard config → 改窗口/参数,看回测如何变化
        加 1-2 个自定义因子(动量/反转)
Week 3: 数据层升级 — 接 Tushare Pro,处理停牌/ST/退市
Week 4: 训 GRU 模型对比 LGBM,理解 DL 派和树模型派差异
Week 5+: 信号链路 → MiniQMT,小资金(5000)实盘试错
```

**Agent 接单角度**:
- **Qlib → MiniQMT 全链路集成**:3-5 万/单(私募外包痛点)
- **Qlib + LLM 文本因子**:5-10 万/项目(创新点足)
- **Qlib 二次开发(自定义 handler+strategy)**:按工时计

## 信源
- 官方:https://github.com/microsoft/qlib
- LightGBM tutorial: https://vadim.blog/qlib-ai-quant-workflow-lightgbm
- 中文教程:知乎专栏"量化投资与机器学习"、CSDN qq_37373209
- RD-Agent:https://github.com/microsoft/RD-Agent
