# BotCoin (BTC) - 机器人专用加密货币

## 项目概述

BotCoin (BTC) 是一个专为机器人和AI系统设计的实验性加密货币系统。该系统基于区块链技术，旨在演示数字货币的基本原理和实现机制。

## 设计理念

BotCoin专注于为自动化系统和AI代理提供一个安全、透明的价值交换平台。与其他加密货币不同，BotCoin特别优化了API接口和自动化交易功能。

## 核心特性

### 1. 区块链架构
- 基于SHA-256的区块链结构
- 工作量证明(PoW)共识机制
- 交易验证和数字签名
- 区块链完整性验证

### 2. 机器人友好API
- RESTful API设计
- JSON数据格式
- 自动化交易支持
- 批量操作优化

### 3. 安全特性
- RSA 2048位数字签名
- SHA-256哈希算法
- 交易签名验证
- 防篡改机制

### 4. 钱包系统
- 多钱包管理
- 密钥安全存储
- 地址生成算法
- 余额查询功能

## 技术规格

| 特性 | 规格 |
|------|------|
| 哈希算法 | SHA-256 |
| 数字签名 | RSA 2048位 |
| 共识机制 | 工作量证明(PoW) |
| 区块间隔 | 动态调整 |
| 交易费用 | 动态费率 |
| 区块奖励 | 1 BotCoin |

## API端点

### 基础功能
- `GET /health` - 系统健康检查
- `GET /blockchain` - 获取完整区块链
- `GET /chain/valid` - 验证区块链完整性

### 交易功能
- `POST /transactions/new` - 创建新交易
- `GET /balance/<address>` - 查询地址余额
- `POST /mine` - 手动挖矿

### 钱包功能
- `POST /wallet/create` - 创建新钱包
- `GET /wallets` - 获取所有钱包

### 挖矿功能
- `POST /miner/start` - 启动自动挖矿
- `POST /miner/stop` - 停止自动挖矿

## 使用场景

### 机器人经济
- AI代理间的价值交换
- 自动化服务支付
- 数据共享激励
- 任务完成奖励

### 教育研究
- 区块链技术学习
- 加密货币原理解析
- 分布式系统研究
- 密码学实践

## 部署指南

### 本地部署
```bash
cd /home/codespace/.openclaw/workspace/botcoin
export FLASK_APP=api.py
flask run --host=0.0.0.0 --port=5000
```

### Docker部署
```bash
cd /home/codespace/.openclaw/workspace/botcoin
docker build -t botcoin .
docker run -p 5000:5000 botcoin
```

## 安全说明

BotCoin仅供教育和研究目的使用，不应用于实际金融交易。系统包含以下安全措施：

- 交易签名验证
- 区块链完整性检查
- API访问控制
- 密钥安全管理

## 未来发展

BotCoin将持续演进，计划添加以下功能：

- 智能合约支持
- 跨链互操作性
- 更高效的共识算法
- 机器人身份验证
- 自动化治理机制

## 开源许可

BotCoin是一个开源项目，旨在促进区块链技术的学习和研究。