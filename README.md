# AIagent

几个简单的 Python 脚本，用于查看当前机器的出口公网 IP，以及查询腾讯控股（`0700.HK`）的最新股价。

## 文件

- `check_egress_ip.py`：查询当前出口 IP
- `query_tencent_price.py`：查询腾讯控股（`0700.HK`）最新实时或近实时股价
- `query_local_weather.py`：根据 IP 定位自动查询本地天气
- `bilibili_homepage.html`：仿哔哩哔哩移动端首页的单文件静态页面示例
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

查询本地天气（基于 IP 自动定位，无需输入城市）：

```bash
python3 query_local_weather.py
```

脚本会输出类似以下信息：

```
Location:    Tokyo, Tokyo, Japan
Temperature: 18.2 °C
Condition:   Partly cloudy
Wind speed:  12.3 km/h
Timestamp:   2026-03-28T14:00
Queried at:  2026-03-28 05:00:00 UTC
```

查看哔哩哔哩风格移动首页静态示例：

```bash
open bilibili_homepage.html
```

或直接在浏览器中打开仓库根目录下的 `bilibili_homepage.html`。

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
