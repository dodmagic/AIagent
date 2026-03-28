# AIagent

几个简单的 Python 脚本，用于查看当前机器的出口公网 IP，以及查询腾讯控股（`0700.HK`）的最新股价。

## 文件

- `check_egress_ip.py`：查询当前出口 IP
- `query_tencent_price.py`：查询腾讯控股（`0700.HK`）最新实时或近实时股价
- `requirements.txt`：Python 依赖列表

## 运行环境

- Python 3
- 如需查询腾讯股价，请先安装 `requirements.txt` 中的依赖

## 使用方法

```bash
python3 check_egress_ip.py
```

或者：

```bash
python3 /path/to/check_egress_ip.py
```

查询腾讯控股最新股价：

```bash
python3 -m pip install -r requirements.txt
python3 query_tencent_price.py
```

脚本会输出类似以下信息：

```bash
Tencent Holdings latest price
Ticker: 0700.HK
Price: 500.00
Currency: HKD
Timestamp: 2026-03-28 15:30:00+08:00
```

## 工作逻辑

脚本会按顺序尝试：

1. `https://api.ipify.org?format=json`
2. `https://ifconfig.me/ip`（作为回退）

如果成功，会输出：

```bash
Current egress IP: x.x.x.x
```

如果两个服务都无法访问，脚本会报错退出。

腾讯股价脚本使用 Yahoo Finance 数据源（通过 `yfinance` 库），优先读取 `0700.HK` 的 1 分钟级别行情；如果当日分钟数据不可用，则回退到最近 5 个交易日的日线收盘价。
