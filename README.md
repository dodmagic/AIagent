# AIagent

一个简单的 Python 脚本，用于查看当前机器的出口公网 IP。

## 文件

- `check_egress_ip.py`：查询当前出口 IP

## 运行环境

- Python 3
- 无需安装额外依赖，只使用 Python 标准库

## 使用方法

```bash
python3 check_egress_ip.py
```

或者：

```bash
python3 /path/to/check_egress_ip.py
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
