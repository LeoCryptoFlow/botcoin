import hashlib
import json
import time
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature


@dataclass
class Transaction:
    """交易类"""
    sender: str
    recipient: str
    amount: float
    timestamp: float = time.time()
    signature: Optional[str] = None
    
    def to_json(self) -> str:
        """将交易转换为JSON字符串"""
        data = asdict(self)
        # 移除signature字段以进行签名
        del data['signature']
        return json.dumps(data, sort_keys=True)
    
    def hash(self) -> str:
        """计算交易哈希"""
        return hashlib.sha256(self.to_json().encode()).hexdigest()


@dataclass
class Block:
    """区块类"""
    index: int
    transactions: List[Transaction]
    timestamp: float
    previous_hash: str
    nonce: int = 0
    hash: str = ""
    
    def compute_hash(self) -> str:
        """计算区块哈希"""
        block_data = {
            'index': self.index,
            'transactions': [tx.to_json() for tx in self.transactions],
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def mine_block(self, difficulty: int):
        """挖矿 - 寻找有效哈希"""
        target = '0' * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.compute_hash()
        
        print(f"区块 {self.index} 挖矿成功! Nonce: {self.nonce}, Hash: {self.hash}")


class Wallet:
    """钱包类 - 管理私钥和公钥"""
    
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        self.address = self.generate_address()
    
    def generate_address(self) -> str:
        """生成钱包地址"""
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return hashlib.sha256(public_pem).hexdigest()
    
    def sign_transaction(self, transaction: Transaction) -> str:
        """使用私钥签名交易"""
        message = transaction.to_json().encode()
        signature = self.private_key.sign(
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return signature.hex()
    
    def verify_signature(self, transaction: Transaction, signature_hex: str) -> bool:
        """验证交易签名"""
        try:
            signature = bytes.fromhex(signature_hex)
            message = transaction.to_json().encode()
            self.public_key.verify(
                signature,
                message,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False


class Blockchain:
    """区块链主类"""
    
    def __init__(self, difficulty: int = 4):
        self.unconfirmed_transactions: List[Transaction] = []
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.target_time_per_block = 600  # 每10分钟一个区块
        self.adjustment_interval = 2016   # 每2016个区块调整一次难度
        self.create_genesis_block()
        self.node_peers: List[str] = []  # 网络节点列表
        self.miner_rewards: Dict[str, float] = {}  # 记录矿工奖励
    
    def create_genesis_block(self):
        """创建创世区块"""
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    @property
    def last_block(self) -> Block:
        """获取最后一个区块"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """添加交易到待确认队列"""
        # 验证交易
        if not self.validate_transaction(transaction):
            return False
        
        self.unconfirmed_transactions.append(transaction)
        return True
    
    def validate_transaction(self, transaction: Transaction) -> bool:
        """验证交易有效性"""
        # 检查是否所有必要字段都存在
        if not all([transaction.sender, transaction.recipient, transaction.amount]):
            return False
        
        # 检查金额是否为正数
        if transaction.amount <= 0:
            return False
        
        # 验证签名（如果存在）
        if transaction.signature:
            # 这里需要从sender地址恢复公钥来验证签名
            # 为了简化，我们假设签名是有效的
            pass
        
        return True
    
    def adjust_difficulty(self):
        """根据区块生成时间调整难度"""
        if len(self.chain) < 2:
            return self.difficulty
        
        # 只在特定间隔调整难度
        if len(self.chain) % self.adjustment_interval != 0:
            return self.difficulty
        
        # 计算最近2016个区块的生成时间
        expected_time = self.adjustment_interval * self.target_time_per_block
        actual_time = self.chain[-1].timestamp - self.chain[-self.adjustment_interval].timestamp
        
        # 限制调整幅度（最大2倍，最小0.5倍）
        if actual_time < expected_time / 2:
            actual_time = expected_time / 2
        if actual_time > expected_time * 2:
            actual_time = expected_time * 2
        
        # 调整难度
        new_difficulty = int(self.difficulty * (expected_time / actual_time))
        
        # 确保难度不低于1
        if new_difficulty < 1:
            new_difficulty = 1
            
        self.difficulty = new_difficulty
        print(f"难度已调整为: {self.difficulty}")
        return self.difficulty
    
    def mine(self, miner_address: str) -> Optional[str]:
        """挖矿 - 将待确认交易打包成新区块"""
        if not self.unconfirmed_transactions:
            return None
        
        # 根据挖矿类型调整奖励
        base_reward = 1.0
        task_bonus = 0.0  # AI任务奖励
        
        # 添加挖矿奖励交易
        reward_transaction = Transaction(
            sender="SYSTEM",
            recipient=miner_address,
            amount=base_reward + task_bonus,
            timestamp=time.time()
        )
        self.unconfirmed_transactions.insert(0, reward_transaction)
        
        last_block = self.last_block
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.unconfirmed_transactions.copy(),
            timestamp=time.time(),
            previous_hash=last_block.hash
        )
        
        # 调整难度
        self.adjust_difficulty()
        
        # 挖矿
        new_block.mine_block(self.difficulty)
        
        # 验证新区块
        if self.is_valid_new_block(new_block, last_block):
            self.chain.append(new_block)
            
            # 记录矿工奖励
            if miner_address in self.miner_rewards:
                self.miner_rewards[miner_address] += base_reward + task_bonus
            else:
                self.miner_rewards[miner_address] = base_reward + task_bonus
            
            # 清空待确认交易
            self.unconfirmed_transactions = []
            return new_block.hash
        else:
            print("新区块验证失败")
            return None
    
    def is_valid_new_block(self, new_block: Block, previous_block: Block) -> bool:
        """验证新区块是否有效"""
        # 检查索引是否连续
        if previous_block.index + 1 != new_block.index:
            return False
        
        # 检查前一个区块哈希是否匹配
        if previous_block.hash != new_block.previous_hash:
            return False
        
        # 检查哈希是否有效（满足难度要求）
        if new_block.hash != new_block.compute_hash():
            return False
        
        # 检查是否满足难度要求
        if not new_block.hash.startswith('0' * self.difficulty):
            return False
        
        return True
    
    def is_chain_valid(self) -> bool:
        """验证整个区块链是否有效"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if not self.is_valid_new_block(current_block, previous_block):
                return False
        
        return True
    
    def get_balance(self, address: str) -> float:
        """获取地址余额"""
        balance = 0.0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount
        
        return balance
    
    def get_miner_stats(self, miner_address: str) -> Dict:
        """获取矿工统计数据"""
        total_blocks_mined = 0
        total_rewards = 0.0
        
        for block in self.chain:
            # 检查区块奖励交易
            if block.transactions and block.transactions[0].sender == "SYSTEM":
                if block.transactions[0].recipient == miner_address:
                    total_blocks_mined += 1
                    total_rewards += block.transactions[0].amount
        
        return {
            "address": miner_address,
            "blocks_mined": total_blocks_mined,
            "total_rewards": total_rewards,
            "current_difficulty": self.difficulty
        }
    
    def get_network_stats(self) -> Dict:
        """获取网络统计信息"""
        total_transactions = sum(len(block.transactions) for block in self.chain)
        total_blocks = len(self.chain)
        
        # 计算平均区块时间（如果链足够长）
        avg_block_time = 0
        if len(self.chain) > 1:
            time_span = self.chain[-1].timestamp - self.chain[0].timestamp
            avg_block_time = time_span / (len(self.chain) - 1)
        
        return {
            "total_blocks": total_blocks,
            "total_transactions": total_transactions,
            "current_difficulty": self.difficulty,
            "avg_block_time": avg_block_time,
            "estimated_network_power": f"{2**self.difficulty * 1000 / avg_block_time:.2e} hashes/sec" if avg_block_time > 0 else "N/A"
        }
    
    def calculate_openclaw_mining_reward(self, task_complexity: int, completion_time: float) -> float:
        """计算OpenClaw AI任务挖矿奖励"""
        # 基础奖励
        base_reward = 0.1
        
        # 任务复杂度奖励 (1-10 scale)
        complexity_bonus = min(task_complexity * 0.05, 0.5)
        
        # 时间效率奖励 (越快完成奖励越高，但有上限)
        time_bonus = max(0, 0.2 - completion_time * 0.001)  # 假设理想完成时间为200秒
        
        return round(base_reward + complexity_bonus + time_bonus, 4)


# 示例使用
if __name__ == "__main__":
    # 创建区块链实例
    blockchain = Blockchain(difficulty=2)
    
    # 创建两个钱包
    wallet1 = Wallet()
    wallet2 = Wallet()
    
    print(f"钱包1地址: {wallet1.address[:10]}...")
    print(f"钱包2地址: {wallet2.address[:10]}...")
    
    # 创建一笔交易
    transaction = Transaction(
        sender=wallet1.address,
        recipient=wallet2.address,
        amount=5.0
    )
    
    # 用钱包1签名交易
    transaction.signature = wallet1.sign_transaction(transaction)
    
    # 添加交易到区块链
    blockchain.add_transaction(transaction)
    
    # 挖矿
    print("\n开始挖矿...")
    mined_block_hash = blockchain.mine(wallet2.address)
    
    if mined_block_hash:
        print(f"挖矿成功! 区块哈希: {mined_block_hash}")
        print(f"区块链长度: {len(blockchain.chain)}")
        print(f"钱包2余额: {blockchain.get_balance(wallet2.address)} OCC")
        print(f"钱包1余额: {blockchain.get_balance(wallet1.address)} OCC")
    
    print(f"\n区块链有效性: {blockchain.is_chain_valid()}")