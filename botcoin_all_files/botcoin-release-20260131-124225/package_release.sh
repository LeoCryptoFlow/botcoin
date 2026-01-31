#!/bin/bash

# BotCoin发布包创建脚本

echo "📦 创建BotCoin (bot) v1.0.0 发布包..."

# 创建发布目录
RELEASE_DIR="botcoin-release-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$RELEASE_DIR"

# 复制项目文件（排除.git和临时文件）
rsync -av --exclude='.git' --exclude='*.log' --exclude='__pycache__' --exclude='wallets/*' --exclude='.gitignore' /home/codespace/.openclaw/workspace/botcoin/ "$RELEASE_DIR/"

# 创建发布说明
cat > "$RELEASE_DIR/RELEASE_NOTES.md" << EOF
# BotCoin (bot) v1.0.0

## 发布信息
- 版本: v1.0.0
- 发布日期: $(date)
- 项目: BotCoin (bot) - AI-focused cryptocurrency
- 单位: bot
- 总量: 2100亿bot

## 项目描述
BotCoin是专为AI系统设计的加密货币，具有独特的AI任务挖矿机制。

## 安装说明
1. 解压文件
2. 安装依赖: pip install -r requirements.txt
3. 启动API: export FLASK_APP=api.py && flask run --host=0.0.0.0 --port=5000

## 文件清单
- blockchain.py : 区块链核心
- wallet.py : 钱包系统
- api.py : API接口
- 各种文档和示例文件
EOF

# 创建ZIP压缩包
zip -r "botcoin-v1.0.0.zip" "$RELEASE_DIR"

# 创建校验和
sha256sum "botcoin-v1.0.0.zip" > "botcoin-v1.0.0-checksum.txt"

echo "✅ 发布包创建完成!"
echo "📁 文件: botcoin-v1.0.0.zip"
echo "🔍 校验和: botcoin-v1.0.0-checksum.txt"
echo "📂 详细文件夹: $RELEASE_DIR"

echo ""
echo "要发布到GitHub，请:"
echo "1. 在GitHub上创建名为'botcoin'的新仓库"
echo "2. 上传botcoin-v1.0.0.zip文件"
echo "3. 创建新版本发布"