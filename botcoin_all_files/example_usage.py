"""
BotCoin (BTC) 使用示例
演示如何使用BTC系统的各种功能
"""

import requests
import json
import time
from blockchain import Blockchain, Wallet
from wallet import WalletManager, SimpleWallet


def demo_standalone():
    """演示独立模式使用"""
    print("=== BotCoin 独立模式演示 ===\n")
    
    # 创建区块链实例
    blockchain = Blockchain(difficulty=2)
    print("1. 区块链初始化完成")
    print(f"   创世区块: {blockchain.last_block.hash[:10]}...")
    
    # 创建钱包
    wallet_manager = WalletManager()
    alice_wallet = wallet_manager.create_wallet("alice")
    bob_wallet = wallet_manager.create_wallet("bob")
    
    print(f"\n2. 钱包创建完成")
    print(f"   Alice地址: {alice_wallet.address[:10]}...")
    print(f"   Bob地址: {bob_wallet.address[:10]}...")
    
    # 创建交易
    simple_wallet = SimpleWallet(wallet_manager)
    transaction = simple_wallet.create_transaction(
        alice_wallet.address, 
        bob_wallet.address, 
        5.0
    )
    
    print(f"\n3. 交易创建完成")
    print(f"   交易: {transaction.sender[:10]}... -> {transaction.recipient[:10]}... ({transaction.amount} OCC)")
    
    # 添加交易到区块链
    blockchain.add_transaction(transaction)
    print(f"   交易已加入待确认队列")
    
    # 挖矿
    print(f"\n4. 开始挖矿...")
    block_hash = blockchain.mine(alice_wallet.address)
    
    if block_hash:
        print(f"   挖矿成功! 区块哈希: {block_hash[:10]}...")
        print(f"   区块链长度: {len(blockchain.chain)}")
        
        # 查询余额
        alice_balance = blockchain.get_balance(alice_wallet.address)
        bob_balance = blockchain.get_balance(bob_wallet.address)
        print(f"\n5. 余额查询")
        print(f"   Alice余额: {alice_balance} OCC")
        print(f"   Bob余额: {bob_balance} OCC")
    
    print(f"\n6. 区块链验证: {'有效' if blockchain.is_chain_valid() else '无效'}")


def demo_api():
    """演示API模式使用（如果API服务运行中）"""
    print("\n=== BotCoin API模式演示 ===\n")
    
    base_url = "http://localhost:5000"
    
    try:
        # 检查API健康状态
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("1. API服务连接成功")
            print(f"   状态: {response.json()['status']}")
        else:
            print("1. API服务不可用")
            return
        
        # 获取区块链信息
        response = requests.get(f"{base_url}/blockchain")
        if response.status_code == 200:
            data = response.json()
            print(f"2. 区块链信息")
            print(f"   区块数量: {data['length']}")
            print(f"   难度: {data['difficulty']}")
        else:
            print("2. 无法获取区块链信息")
        
        # 创建钱包
        response = requests.post(f"{base_url}/wallet/create", 
                                json={"name": "demo_wallet"})
        if response.status_code == 200:
            wallet_addr = response.json()['address']
            print(f"3. 钱包创建成功")
            print(f"   地址: {wallet_addr[:10]}...")
        else:
            print("3. 钱包创建失败")
        
        # 查询钱包列表
        response = requests.get(f"{base_url}/wallets")
        if response.status_code == 200:
            wallets = response.json()['wallets']
            print(f"4. 钱包总数: {len(wallets)}")
        else:
            print("4. 无法获取钱包列表")
        
    except requests.exceptions.ConnectionError:
        print("1. API服务未运行，请先启动API服务")
        print("   运行: cd /home/codespace/.openclaw/workspace/botcoin && python3 -m flask run --host=0.0.0.0 --port=5000")


def demo_conceptual_features():
    """演示概念性功能"""
    print("\n=== BotCoin 概念功能 ===\n")
    
    features = [
        "✅ 基于区块链的去中心化账本",
        "✅ 工作量证明共识机制",
        "✅ RSA数字签名验证",
        "✅ 交易手续费机制",
        "✅ 钱包管理系统",
        "✅ RESTful API接口",
        "✅ 自动挖矿守护进程",
        "✅ 区块链验证机制",
        "✅ 余额查询功能",
        "✅ 交易历史记录"
    ]
    
    for feature in features:
        print(f"   {feature}")
    
    print(f"\n💡 BotCoin专为教育和实验设计")
    print(f"   适合学习区块链原理和技术实现")


if __name__ == "__main__":
    print("/BotCoin (BTC) 演示程序/")
    print("=" * 50)
    
    # 演示独立功能
    demo_standalone()
    
    # 演示API功能
    demo_api()
    
    # 概念功能介绍
    demo_conceptual_features()
    
    print("\n" + "=" * 50)
    print("演示完成！")
    print("了解更多请查看: /home/codespace/.openclaw/workspace/botcoin/")