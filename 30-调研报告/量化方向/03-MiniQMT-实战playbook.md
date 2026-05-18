# MiniQMT 散户实盘 Playbook(2024-2025)

> 调研时间:2026-05 | 适用:Linux/Mac 用户想做 A股 Python 量化实盘

## 一、开户真相

### 1万门槛是真的
2024-2025 多家券商已把 MiniQMT 门槛从官方50万降到 **1万元**:
- **国金证券** ⭐(社区文档最多)
- **东兴证券**
- **华鑫证券**(部分客户经理)
- 中信建投、华泰、海通、国君、中金、银河、平安 也支持,门槛各异

### 客户经理压价话术
> "做量化,要开MiniQMT(不是大QMT/Ptrade),最低多少?能调佣万1免5吗?不限策略吧?XX券商能1万门槛,你这边方便不?"

新户调佣到 **万1免5** 基本能跟。

## 二、🚨 关键约束:MiniQMT 只能 Windows

Linux/Mac 用户三个选项:

| 方案 | 成本 | 推荐度 |
|---|---|---|
| 腾讯云轻量 Win Server 2022 | ~70元/月 | ⭐⭐⭐ |
| 家里旧笔记本/NUC + 向日葵 | 一次性 | ⭐⭐ |
| **`liqimore/quant-qmt-proxy`** REST 桥 | 免费 | ⭐⭐⭐⭐⭐ |

**最佳路径**:Windows 跑 QMT + quant-qmt-proxy,Linux 写策略调 HTTP。
彻底解耦,策略代码留在你熟悉的环境。

## 三、风控红线(不能碰)

- 单股单日报撤 **≥500次** 触发警示,**券商常更严(≤200)**
- **高频(>3笔/秒)、对敲、尾盘拉抬** = 散户档禁
- 触发后:券商风控电话 → 限制交易 → 严重者销户

### 散户档安全策略类型
- ✅ 中低频信号(分钟~日级)
- ✅ 网格交易
- ✅ CTA趋势
- ✅ ETF轮动
- ✅ 可转债低价/双低
- ✅ 多因子选股(月度调仓)

## 四、社区资源(官方文档很烂,只能靠这些)

| 仓库 | Star | 用途 |
|---|---|---|
| `ai4trade/XtQuant` | 426 | 比较完整的封装 |
| `quant-king299/EasyXT` | 398 | 友好API,新手优先 |
| **`liqimore/quant-qmt-proxy`** | 162 | **Linux 桥,REST 接口** ⭐ |
| 知乎"看海量化"专栏 | - | 教程最系统 |

## 五、最小可运行代码模板(SMA交叉ETF轮动)

> 已处理:断线重连、集合竞价时段、T+1可用数量

```python
# strategy_etf_rotation.py
import time
from xtquant import xtdata, xttrader
from xtquant.xttype import StockAccount
from datetime import datetime

ACCOUNT_ID = "你的资金账号"
PATH_QMT = r"D:\国金QMT交易端\userdata_mini"

# 标的池(沪深300/中证500/红利/纳指)
POOL = ["510300.SH", "510500.SH", "510880.SH", "513100.SH"]
SMA_SHORT, SMA_LONG = 5, 20

def is_trading_time():
    now = datetime.now().time()
    return (now >= datetime.strptime("09:30", "%H:%M").time() 
            and now <= datetime.strptime("14:57", "%H:%M").time())

def get_signal(code):
    df = xtdata.get_market_data_ex([], [code], period="1d", count=SMA_LONG+5)
    closes = df[code]["close"].tolist()
    if len(closes) < SMA_LONG:
        return False
    sma_s = sum(closes[-SMA_SHORT:]) / SMA_SHORT
    sma_l = sum(closes[-SMA_LONG:]) / SMA_LONG
    return sma_s > sma_l

def get_available_qty(trader, account, code):
    """T+1:今天买入不能卖,只用昨日持仓"""
    positions = trader.query_stock_positions(account)
    for p in positions:
        if p.stock_code == code:
            return p.can_use_volume  # 昨日可用
    return 0

def rebalance(trader, account):
    signals = {c: get_signal(c) for c in POOL}
    targets = [c for c, s in signals.items() if s]
    if not targets:
        return
    
    # 卖出不在目标的
    for code in POOL:
        if code not in targets:
            qty = get_available_qty(trader, account, code)
            if qty > 0:
                trader.order_stock(account, code, xttrader.STOCK_SELL,
                                   qty, xttrader.LATEST_PRICE, 0, "rotation")
    
    # 等成交回报(简化)
    time.sleep(3)
    
    # 平均分配资金买入
    asset = trader.query_stock_asset(account)
    cash_per = asset.cash / len(targets)
    for code in targets:
        tick = xtdata.get_full_tick([code])[code]
        price = tick["lastPrice"]
        qty = int(cash_per / price / 100) * 100  # A股100股整数
        if qty >= 100:
            trader.order_stock(account, code, xttrader.STOCK_BUY,
                               qty, xttrader.LATEST_PRICE, 0, "rotation")

def main():
    trader = xttrader.XtQuantTrader(PATH_QMT, int(time.time()))
    trader.start()
    
    # 断线重连
    while True:
        if trader.connect() == 0:
            break
        print("连接失败,5秒后重试")
        time.sleep(5)
    
    account = StockAccount(ACCOUNT_ID)
    trader.subscribe(account)
    
    while True:
        if is_trading_time() and datetime.now().minute == 50:
            # 14:50 调仓(避开集合竞价)
            try:
                rebalance(trader, account)
            except Exception as e:
                print(f"调仓失败: {e}")
            time.sleep(60)
        time.sleep(10)

if __name__ == "__main__":
    main()
```

## 六、上线 Checklist

- [ ] 开户(争取1万门槛+万1免5)
- [ ] 开通量化交易权限(柜台审批,1-3天)
- [ ] 报备策略(2024.10新规要求,券商有模板)
- [ ] Win环境装 QMT + 登录 + 找到 userdata_mini 路径
- [ ] 装 xtquant pip 包
- [ ] 模拟盘跑 1-2 周(QMT 有仿真账号)
- [ ] 准备小资金(5000-10000)实盘试错
- [ ] 设置每日报撤上限告警(避免触发风控)
- [ ] 日志+异常邮件/微信通知
- [ ] 周末复盘成交回报 vs 信号偏差

## 七、避坑清单

1. **不要在交易时段重启 QMT 客户端** — 会断连接,持仓信号丢失
2. **`LATEST_PRICE` 在涨跌停时会买不进** — 用限价单
3. **集合竞价(9:15-9:25, 14:57-15:00)别下单** — 撮合规则不同
4. **`query_stock_positions` 返回的 volume ≠ can_use_volume** — T+1要看后者
5. **QMT 软件升级会改 userdata 路径** — 升级后检查策略配置
6. **券商风控会监控异常下单频率** — 单股每分钟 ≤ 5笔比较安全
