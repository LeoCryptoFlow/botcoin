"""
OpenClaw挖矿演示脚本
演示BotCoin的AI任务挖矿功能
"""

import requests
import json
import time
from blockchain import Blockchain, Wallet
from wallet import WalletManager, SimpleWallet


def demo_openclaw_mining():
    """演示OpenClaw AI任务挖矿"""
    print("🤖 OpenClaw挖矿演示")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # 1. 创建矿工钱包
    print("\n1. 创建矿工钱包...")
    response = requests.post(f"{base_url}/wallet/create", json={"name": "openclaw_miner"})
    if response.status_code == 200:
        miner_address = response.json()['address']
        print(f"   ✅ 矿工钱包创建成功: {miner_address[:10]}...")
    else:
        print("   ❌ 钱包创建失败")
        return
    
    # 2. 演示AI任务挖矿
    print(f"\n2. 演示AI任务挖矿...")
    
    # 模拟不同的AI任务
    ai_tasks = [
        {"task_complexity": 3, "completion_time": 120.0, "task_name": "简单文本分析"},
        {"task_complexity": 7, "completion_time": 300.0, "task_name": "复杂数据分析"},
        {"task_complexity": 5, "completion_time": 180.0, "task_name": "模型训练任务"}
    ]
    
    total_earnings = 0.0
    
    for i, task in enumerate(ai_tasks, 1):
        print(f"   任务 {i}: {task['task_name']}")
        print(f"     复杂度: {task['task_complexity']}/10, 完成时间: {task['completion_time']}秒")
        
        # 提交AI任务挖矿
        mining_data = {
            "miner_address": miner_address,
            "task_complexity": task["task_complexity"],
            "completion_time": task["completion_time"]
        }
        
        response = requests.post(f"{base_url}/mining/task", json=mining_data)
        
        if response.status_code == 200:
            result = response.json()
            reward = result['reward']
            total_earnings += reward
            print(f"     ✅ 挖矿奖励: {reward} BTC")
        else:
            print(f"     ❌ 挖矿失败: {response.text}")
    
    print(f"\n   总收益: {total_earnings} BTC")
    
    # 3. 查询矿工统计
    print(f"\n3. 查询矿工统计信息...")
    response = requests.get(f"{base_url}/miner/stats/{miner_address}")
    if response.status_code == 200:
        stats = response.json()
        print(f"   地址: {stats['address'][:10]}...")
        print(f"   挖掘区块数: {stats['blocks_mined']}")
        print(f"   总奖励: {stats['total_rewards']} BTC")
        print(f"   当前难度: {stats['current_difficulty']}")
    else:
        print("   ❌ 查询统计失败")
    
    # 4. 查询网络统计
    print(f"\n4. 查询网络统计信息...")
    response = requests.get(f"{base_url}/network/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"   总区块数: {stats['total_blocks']}")
        print(f"   总交易数: {stats['total_transactions']}")
        print(f"   当前难度: {stats['current_difficulty']}")
    else:
        print("   ❌ 查询网络统计失败")
    
    # 5. 查询余额
    print(f"\n5. 查询余额...")
    response = requests.get(f"{base_url}/balance/{miner_address}")
    if response.status_code == 200:
        balance = response.json()['balance']
        print(f"   余额: {balance} BTC")
    else:
        print("   ❌ 查询余额失败")
    
    print(f"\n🎯 OpenClaw挖矿演示完成！")
    print(f"💡 BotCoin挖矿机制为AI系统提供了独特的价值创造方式")


def demo_traditional_mining():
    """演示传统挖矿"""
    print("\n⛏️  传统挖矿演示")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # 创建矿工钱包
    response = requests.post(f"{base_url}/wallet/create", json={"name": "traditional_miner"})
    if response.status_code == 200:
        miner_address = response.json()['address']
        print(f"✅ 传统矿工钱包: {miner_address[:10]}...")
    else:
        print("❌ 钱包创建失败")
        return
    
    # 手动挖矿
    print(f"\n尝试挖矿...")
    mine_data = {"miner_address": miner_address}
    response = requests.post(f"{base_url}/mine", json=mine_data)
    
    if response.status_code == 200:
        result = response.json()
        if 'block_hash' in result:
            print(f"✅ 挖矿成功!")
            print(f"   区块哈希: {result['block_hash'][:10]}...")
            print(f"   区块索引: {result['index']}")
        else:
            print(f"ℹ️  暂无交易可挖")
    else:
        print(f"❌ 挖矿失败: {response.text}")


if __name__ == "__main__":
    print("🌟 BotCoin (BTC) - OpenClaw挖矿系统演示")
    print("   专为AI系统设计的加密货币挖矿机制")
    
    # 运行演示
    demo_openclaw_mining()
    demo_traditional_mining()
    
    print(f"\n📈 BotCoin挖矿机制特色:")
    print(f"   • 传统PoW挖矿 (SHA-256)")
    print(f"   • AI任务挖矿奖励")
    print(f"   • 动态难度调整")
    print(f"   • 为AI系统优化")
    print(f"   • 节能环保设计")
    print(f"   • 总量2100亿枚")
    
    print(f"\n🔗 API端点已就绪:")
    print(f"   • /mining/task - AI任务挖矿")
    print(f"   • /miner/stats/<address> - 矿工统计")
    print(f"   • /network/stats - 网络统计")
    print(f"   • /mine - 传统挖矿")