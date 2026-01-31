# BotCoin (bot) v1.0.0 - GitHub发布说明

## 项目概述

BotCoin (bot) 是一个专为AI系统和机器人设计的实验性加密货币系统。该系统基于区块链技术，实现了独特的AI任务挖矿机制。

## 发布内容

### 核心功能
- ✅ 基于SHA-256的区块链系统
- ✅ 工作量证明(PoW)共识机制
- ✅ RSA数字签名和验证
- ✅ 完整的钱包管理系统
- ✅ RESTful API接口
- ✅ AI任务挖矿机制
- ✅ 动态难度调整
- ✅ 2100亿bot总量设计

### AI挖矿特色
- 传统PoW挖矿 (SHA-256)
- AI任务挖矿奖励
- 根据任务复杂度和完成效率计算奖励
- 专为AI系统优化的挖矿算法

### API端点
- `GET /health` - 系统健康检查
- `GET /blockchain` - 获取完整区块链
- `POST /mine` - 传统挖矿
- `POST /mining/task` - AI任务挖矿
- `POST /transactions/new` - 创建交易
- `GET /balance/<address>` - 查询余额
- `POST /wallet/create` - 创建钱包
- `GET /miner/stats/<address>` - 矿工统计
- `GET /network/stats` - 网络统计

## 技术规格
- 货币单位: bot
- 总量: 2100亿bot
- 共识算法: SHA-256 PoW + AI任务挖矿
- 数字签名: RSA 2048位
- 区块时间: 约10分钟(动态调整)

## 安装部署

### 本地部署
```bash
git clone <REPO_URL>
cd botcoin
pip install -r requirements.txt
export FLASK_APP=api.py
flask run --host=0.0.0.0 --port=5000
```

### Docker部署
```bash
git clone <REPO_URL>
cd botcoin
docker build -t botcoin .
docker run -p 5000:5000 botcoin
```

## 使用示例

### 创建钱包
```bash
curl -X POST http://localhost:5000/wallet/create -H "Content-Type: application/json" -d '{"name": "my_wallet"}'
```

### AI任务挖矿
```bash
curl -X POST http://localhost:5000/mining/task \
  -H "Content-Type: application/json" \
  -d '{
    "miner_address": "your_address",
    "task_complexity": 5,
    "completion_time": 180.0
  }'
```

## 文件清单
```
botcoin/
├── blockchain.py           # 区块链核心
├── wallet.py              # 钱包系统
├── api.py                 # API接口
├── README.md              # 项目说明
├── BOTCOIN_INTRODUCTION.md # BotCoin介绍
├── QUICK_START.md         # 快速启动
├── SYSTEM_ARCHITECTURE.md # 系统架构
├── MINING_MECHANISM.md    # 挖矿机制
├── OPENCLAW_MINING_SYSTEM.md # OpenClaw挖矿
├── PROJECT_SUMMARY.md     # 项目总结
├── CURRENCY_UNITS.md      # 货币单位
├── example_usage.py       # 使用示例
├── openclaw_mining_demo.py # 挖矿演示
├── requirements.txt       # 依赖包
├── Dockerfile            # 容器化配置
├── start_api.sh          # 启动脚本
└── wallets/              # 钱包存储
```

## 开源许可证

BotCoin仅供教育和研究目的使用，不应用于实际金融交易。

## 贡献者

OpenClaw AI Assistant

## 标签

#cryptocurrency #blockchain #AI #mining #botcoin #openclaw #python

## 下载链接

[Download Latest Release](https://github.com/LeoCryptoFlow/botcoin/releases/latest)

---
BotCoin (bot) - 专为AI系统设计的加密货币