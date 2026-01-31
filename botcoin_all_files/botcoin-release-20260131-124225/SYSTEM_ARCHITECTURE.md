# BotCoin (BTC) 系统架构文档

## 1. 概述

BotCoin (BTC) 是一个基于区块链技术的加密货币系统。该系统采用模块化设计，主要包括区块链核心、钱包系统、API接口和网络协议四个主要组件。

## 2. 核心组件

### 2.1 区块链核心 (blockchain.py)

#### 主要类：
- `Transaction`: 交易类，包含发送方、接收方、金额、时间戳和签名
- `Block`: 区块类，包含交易列表、时间戳、前区块哈希等
- `Blockchain`: 区块链主类，负责维护区块链状态

#### 核心功能：
- 工作量证明(PoW)挖矿算法
- 交易验证和签名
- 区块链验证
- 余额查询

### 2.2 钱包系统 (wallet.py)

#### 主要类：
- `Wallet`: 钱包类，管理RSA密钥对
- `WalletManager`: 钱包管理器，管理多个钱包
- `SimpleWallet`: 简化钱包接口

#### 核心功能：
- 密钥生成和管理
- 交易签名
- 钱包持久化存储

### 2.3 API接口 (api.py)

#### 主要端点：
- `GET /health`: 健康检查
- `GET /blockchain`: 获取完整区块链
- `POST /mine`: 挖矿
- `POST /transactions/new`: 创建交易
- `GET /balance/<address>`: 查询余额
- `POST /wallet/create`: 创建钱包
- `GET /wallets`: 获取所有钱包
- `GET /chain/valid`: 验证区块链
- `POST /miner/start`: 启动自动挖矿
- `POST /miner/stop`: 停止自动挖矿

## 3. 数据结构

### 3.1 交易结构
```python
{
    "sender": "string",      # 发送方地址
    "recipient": "string",   # 接收方地址
    "amount": float,         # 金额
    "timestamp": float,      # 时间戳
    "signature": "string"    # 数字签名
}
```

### 3.2 区块结构
```python
{
    "index": int,                    # 区块索引
    "transactions": [Transaction],   # 交易列表
    "timestamp": float,              # 时间戳
    "previous_hash": "string",       # 前区块哈希
    "hash": "string",                # 当前区块哈希
    "nonce": int                     # 随机数
}
```

## 4. 安全特性

### 4.1 加密算法
- SHA-256: 区块和交易哈希
- RSA 2048: 数字签名和验证
- 工作量证明: 防止双重支付

### 4.2 验证机制
- 交易签名验证
- 区块链完整性验证
- PoW难度验证

## 5. 网络协议

系统支持节点间的通信，通过REST API进行交互。节点可以：
- 同步区块链数据
- 广播新交易
- 共享挖矿奖励

## 6. 性能特征

- 挖矿难度可调节
- 交易确认时间取决于网络负载
- 区块大小无硬性限制

## 7. 扩展性

系统设计考虑了以下扩展方向：
- 智能合约支持
- 跨链互操作性
- 更高效的共识算法
- 分片技术

## 8. 使用场景

- 教育演示
- 实验性应用
- 内部代币系统
- 学习区块链原理