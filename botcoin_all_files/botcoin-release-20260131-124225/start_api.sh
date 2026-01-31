#!/bin/bash
# 启动BotCoin API服务

echo "🚀 启动BotCoin API服务..."

# 设置环境变量
export FLASK_APP=api.py
export FLASK_ENV=development

# 进入项目目录
cd /home/codespace/.openclaw/workspace/botcoin

# 启动Flask应用
echo "🌐 API服务将在 http://localhost:5000 上运行"
flask run --host=0.0.0.0 --port=5000