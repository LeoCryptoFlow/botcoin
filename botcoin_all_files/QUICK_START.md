# BotCoin (BTC) 快速启动指南

## 简介

BotCoin是一个专为机器人和AI系统设计的实验性加密货币系统。本指南将帮助您快速启动和使用BotCoin。

## 系统要求

- Python 3.8+
- pip包管理器
- 系统内存: 至少512MB

## 安装步骤

### 1. 克隆或访问项目
```bash
cd /home/codespace/.openclaw/workspace/botcoin
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 启动API服务
```bash
cd /home/codespace/.openclaw/workspace/botcoin
export FLASK_APP=api.py
flask run --host=0.0.0.0 --port=5000
```

或者使用启动脚本：
```bash
cd /home/codespace/.openclaw/workspace/botcoin
./start_api.sh
```

## API使用示例

### 检查系统状态
```bash
curl http://localhost:5000/health
```

### 创建钱包
```bash
curl -X POST http://localhost:5000/wallet/create \
  -H "Content-Type: application/json" \
  -d '{"name": "my_wallet"}'
```

### 查询区块链
```bash
curl http://localhost:5000/blockchain
```

### 查询余额
```bash
curl http://localhost:5000/balance/<wallet_address>
```

### 创建交易
```bash
curl -X POST http://localhost:5000/transactions/new \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "sender_address",
    "recipient": "recipient_address",
    "amount": 1.0
  }'
```

## 主要功能

### 1. 钱包管理
- 创建新钱包
- 查询钱包余额
- 管理多个钱包

### 2. 交易处理
- 创建交易
- 交易验证
- 区块链记录

### 3. 挖矿功能
- 手动挖矿
- 自动挖矿守护进程
- 工作量证明

### 4. 区块链查询
- 获取完整区块链
- 验证区块链完整性
- 区块信息查询

## 开发接口

BotCoin提供完整的REST API，适合机器人和AI系统集成：

- 标准JSON格式
- HTTP状态码
- 一致的错误处理
- 详细的响应信息

## 注意事项

1. BotCoin仅供教育和研究目的
2. 不应用于真实金融交易
3. 确保API访问安全
4. 定期备份钱包数据

## 故障排除

### API服务无法启动
- 检查端口5000是否被占用
- 确认依赖包已安装
- 查看错误日志

### 交易验证失败
- 检查交易格式
- 确认发送方余额充足
- 验证数字签名

## 学习资源

- 查看 `SYSTEM_ARCHITECTURE.md` 了解系统设计
- 阅读 `BOTCOIN_INTRODUCTION.md` 了解设计理念
- 运行 `example_usage.py` 查看使用示例

## 社区支持

BotCoin是OpenClaw生态系统的一部分，欢迎贡献代码和提出建议。