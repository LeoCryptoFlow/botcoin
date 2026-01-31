from flask import Flask, request, jsonify
import json
from blockchain import Blockchain, Transaction
from wallet import WalletManager, SimpleWallet
import threading
import time


app = Flask(__name__)

# 初始化区块链和钱包管理器
blockchain = Blockchain(difficulty=2)
wallet_manager = WalletManager()
simple_wallet = SimpleWallet(wallet_manager)

# 模拟挖矿线程
mining_thread = None
mining_active = False


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'message': 'BotCoin API is running'
    })


@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    """获取完整区块链"""
    chain_data = []
    for block in blockchain.chain:
        block_info = {
            'index': block.index,
            'transactions': [json.loads(tx.to_json()) for tx in block.transactions],
            'timestamp': block.timestamp,
            'previous_hash': block.previous_hash,
            'hash': block.hash,
            'nonce': block.nonce
        }
        chain_data.append(block_info)
    
    return jsonify({
        'length': len(chain_data),
        'chain': chain_data,
        'difficulty': blockchain.difficulty
    })


@app.route('/mine', methods=['POST'])
def mine_block():
    """挖矿 - 手动触发挖矿"""
    data = request.get_json()
    miner_address = data.get('miner_address')
    
    if not miner_address:
        return jsonify({'error': 'miner_address is required'}), 400
    
    # 触发挖矿
    block_hash = blockchain.mine(miner_address)
    
    if block_hash:
        return jsonify({
            'message': 'Block mined successfully',
            'block_hash': block_hash,
            'index': len(blockchain.chain) - 1
        })
    else:
        return jsonify({'message': 'No transactions to mine'}), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """创建新交易"""
    data = request.get_json()
    
    required_fields = ['sender', 'recipient', 'amount']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # 创建交易
    transaction = Transaction(
        sender=data['sender'],
        recipient=data['recipient'],
        amount=float(data['amount'])
    )
    
    # 如果提供了签名，则使用提供的签名，否则尝试从钱包获取
    if 'signature' in data:
        transaction.signature = data['signature']
    
    # 添加交易到待确认队列
    if blockchain.add_transaction(transaction):
        return jsonify({
            'message': 'Transaction added successfully',
            'transaction_index': len(blockchain.unconfirmed_transactions) - 1
        })
    else:
        return jsonify({'error': 'Invalid transaction'}), 400


@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    """获取地址余额"""
    balance = blockchain.get_balance(address)
    return jsonify({
        'address': address,
        'balance': balance
    })


@app.route('/wallet/create', methods=['POST'])
def create_wallet():
    """创建新钱包"""
    data = request.get_json()
    name = data.get('name', '')
    
    wallet = wallet_manager.create_wallet(name)
    
    return jsonify({
        'address': wallet.address,
        'message': 'Wallet created successfully'
    })


@app.route('/wallets', methods=['GET'])
def get_wallets():
    """获取所有钱包地址"""
    addresses = wallet_manager.get_all_addresses()
    return jsonify({
        'wallets': addresses,
        'count': len(addresses)
    })


@app.route('/chain/valid', methods=['GET'])
def is_valid():
    """验证区块链有效性"""
    valid = blockchain.is_chain_valid()
    return jsonify({
        'valid': valid,
        'message': 'Blockchain is valid' if valid else 'Blockchain is invalid'
    })


def start_mining_daemon():
    """启动自动挖矿守护进程"""
    global mining_active
    mining_active = True
    
    while mining_active:
        if blockchain.unconfirmed_transactions:
            # 尝试挖矿 - 使用默认地址作为矿工奖励
            default_miner = "default_miner_address"
            blockchain.mine(default_miner)
            print(f"[MINER] Block mined at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        time.sleep(10)  # 每10秒检查一次


@app.route('/miner/start', methods=['POST'])
def start_miner():
    """启动自动挖矿"""
    global mining_thread, mining_active
    
    if mining_active:
        return jsonify({'message': 'Miner already running'})
    
    mining_thread = threading.Thread(target=start_mining_daemon)
    mining_thread.daemon = True
    mining_thread.start()
    
    return jsonify({'message': 'Miner started successfully'})


@app.route('/miner/stop', methods=['POST'])
def stop_miner():
    """停止自动挖矿"""
    global mining_active
    mining_active = False
    return jsonify({'message': 'Miner stopped'})


@app.route('/miner/stats/<miner_address>', methods=['GET'])
def get_miner_stats(miner_address):
    """获取矿工统计信息"""
    stats = blockchain.get_miner_stats(miner_address)
    return jsonify(stats)


@app.route('/network/stats', methods=['GET'])
def get_network_stats():
    """获取网络统计信息"""
    stats = blockchain.get_network_stats()
    return jsonify(stats)


@app.route('/mining/task', methods=['POST'])
def submit_ai_task():
    """提交AI任务进行挖矿"""
    data = request.get_json()
    
    required_fields = ['miner_address', 'task_complexity', 'completion_time']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields: miner_address, task_complexity, completion_time'}), 400
    
    miner_address = data['miner_address']
    task_complexity = int(data.get('task_complexity', 1))  # 1-10 scale
    completion_time = float(data.get('completion_time', 300.0))  # in seconds
    
    # 计算AI任务挖矿奖励
    reward = blockchain.calculate_openclaw_mining_reward(task_complexity, completion_time)
    
    if reward > 0:
        # 创建奖励交易
        reward_transaction = Transaction(
            sender="SYSTEM",
            recipient=miner_address,
            amount=reward,
            timestamp=time.time()
        )
        
        # 添加到待确认交易队列
        blockchain.add_transaction(reward_transaction)
        
        return jsonify({
            'message': 'AI task submitted successfully',
            'reward': reward,
            'task_complexity': task_complexity,
            'completion_time': completion_time
        })
    else:
        return jsonify({'error': 'Task did not qualify for reward'}), 400


@app.route('/', methods=['GET'])
def index():
    """API首页"""
    return jsonify({
        'name': 'BotCoin API',
        'version': '0.1.0',
        'endpoints': [
            {'method': 'GET', 'path': '/health', 'description': 'Health check'},
            {'method': 'GET', 'path': '/blockchain', 'description': 'Get full blockchain'},
            {'method': 'POST', 'path': '/mine', 'description': 'Mine a new block'},
            {'method': 'POST', 'path': '/transactions/new', 'description': 'Create new transaction'},
            {'method': 'GET', 'path': '/balance/<address>', 'description': 'Get balance for address'},
            {'method': 'POST', 'path': '/wallet/create', 'description': 'Create new wallet'},
            {'method': 'GET', 'path': '/wallets', 'description': 'Get all wallets'},
            {'method': 'GET', 'path': '/chain/valid', 'description': 'Validate blockchain'},
            {'method': 'POST', 'path': '/miner/start', 'description': 'Start auto-miner'},
            {'method': 'POST', 'path': '/miner/stop', 'description': 'Stop auto-miner'},
            {'method': 'GET', 'path': '/miner/stats/<miner_address>', 'description': 'Get miner statistics'},
            {'method': 'GET', 'path': '/network/stats', 'description': 'Get network statistics'},
            {'method': 'POST', 'path': '/mining/task', 'description': 'Submit AI task for mining reward'}
        ]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)