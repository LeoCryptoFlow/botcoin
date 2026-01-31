# BotCoin (bot) - AI-Focused Cryptocurrency

![BotCoin Logo](https://img.shields.io/badge/BotCoin-bot-FF6B6B?style=for-the-badge&logo=bitcoin)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**BotCoin (bot)** is an innovative cryptocurrency designed specifically for AI systems and robots. Unlike traditional cryptocurrencies that rely solely on computational power, BotCoin introduces a unique AI-task-based mining mechanism where AI assistants earn cryptocurrency rewards for completing user tasks.

## 🚀 Features

### Traditional Mining
- SHA-256 based Proof of Work (PoW)
- Dynamic difficulty adjustment
- Secure blockchain implementation

### AI-Task Mining
- Earn cryptocurrency by completing AI tasks
- Reward calculation based on task complexity and efficiency
- Designed for AI systems like OpenClaw
- Dual mining approach for sustainable growth

### Technical Specifications
- **Currency Unit**: bot (not BTC)
- **Total Supply**: 210 billion bots
- **Consensus**: SHA-256 PoW + AI Task Mining
- **Digital Signature**: RSA 2048-bit
- **Block Time**: ~10 minutes (dynamic adjustment)

## 📊 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Layer     │    │  Core Logic     │    │  Crypto Layer   │
│                 │    │                 │    │                 │
│ • RESTful API   │    │ • Blockchain    │    │ • RSA Signatures│
│ • JSON Format   │    │ • Transactions  │    │ • SHA-256 Hash  │
│ • Bot Mining    │    │ • Mining        │    │ • Keys Mgmt     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
```bash
# Clone the repository
git clone <REPOSITORY_URL>
cd botcoin

# Install dependencies
pip install -r requirements.txt

# Start the API server
export FLASK_APP=api.py
flask run --host=0.0.0.0 --port=5000
```

### Docker Deployment
```bash
# Build and run with Docker
docker build -t botcoin .
docker run -p 5000:5000 botcoin
```

## 🌐 API Endpoints

### Basic Operations
- `GET /health` - Health check
- `GET /blockchain` - Get full blockchain
- `GET /balance/<address>` - Get balance for address
- `GET /chain/valid` - Validate blockchain

### Mining Operations
- `POST /mine` - Traditional mining
- `POST /mining/task` - AI task mining
- `GET /miner/stats/<address>` - Miner statistics
- `GET /network/stats` - Network statistics

### Wallet Operations
- `POST /wallet/create` - Create new wallet
- `GET /wallets` - Get all wallets
- `POST /transactions/new` - Create new transaction

## 🤖 AI Task Mining

BotCoin's unique feature is AI-task-based mining. AI systems can earn cryptocurrency by:

1. **Completing User Requests**: AI assistants earn rewards for completing tasks
2. **Training Models**: Complex AI training tasks receive higher rewards
3. **Data Processing**: Data analysis and processing tasks
4. **Conversations**: Intelligent dialogues and interactions

Reward calculation:
```
Reward = Base Reward + Complexity Bonus + Efficiency Bonus
```

## 💰 Units

- **Main Unit**: bot (not BTC)
- **Subunits**:
  - 1 bot = 1000 millibot (mbot)
  - 1 bot = 1,000,000 microbot (ubot)

## 📚 Usage Examples

### Create Wallet
```bash
curl -X POST http://localhost:5000/wallet/create \
  -H "Content-Type: application/json" \
  -d '{"name": "my_wallet"}'
```

### AI Task Mining
```bash
curl -X POST http://localhost:5000/mining/task \
  -H "Content-Type: application/json" \
  -d '{
    "miner_address": "your_wallet_address",
    "task_complexity": 5,
    "completion_time": 180.0
  }'
```

### Get Balance
```bash
curl http://localhost:5000/balance/your_wallet_address
```

## 🏗️ System Architecture

- **Blockchain Core**: Implements SHA-256 blockchain with PoW consensus
- **Wallet System**: RSA-based wallet management with secure key storage
- **Mining Engine**: Dual mining system (traditional + AI-task)
- **API Layer**: RESTful interface for all operations
- **Security Layer**: Digital signatures and verification mechanisms

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

BotCoin is intended for educational and research purposes only. Do not use for real financial transactions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📞 Support

For support, please open an issue in the repository.

---

**BotCoin (bot)** - The Future of AI-Centric Cryptocurrency 💡🤖