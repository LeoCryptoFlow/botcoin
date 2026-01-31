import json
import os
from typing import Dict, List
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from blockchain import Wallet as BaseWallet
from blockchain import Transaction


class WalletManager:
    """钱包管理器 - 管理多个钱包"""
    
    def __init__(self, wallet_dir: str = "./wallets"):
        self.wallet_dir = wallet_dir
        self.wallets: Dict[str, BaseWallet] = {}
        self.wallet_files: Dict[str, str] = {}
        
        # 创建钱包目录
        os.makedirs(wallet_dir, exist_ok=True)
    
    def create_wallet(self, name: str = "") -> BaseWallet:
        """创建新钱包"""
        wallet = BaseWallet()
        
        # 保存钱包到文件
        wallet_name = name if name else f"wallet_{len(self.wallets) + 1}"
        wallet_file = os.path.join(self.wallet_dir, f"{wallet_name}.json")
        
        wallet_data = {
            'address': wallet.address,
            'private_key': wallet.private_key.private_bytes(
                encoding = serialization.Encoding.PEM,
                format = serialization.PrivateFormat.PKCS8,
                encryption_algorithm = serialization.NoEncryption()
            ).decode(),
            'public_key': wallet.public_key.public_bytes(
                encoding = serialization.Encoding.PEM,
                format = serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
        }
        
        with open(wallet_file, 'w') as f:
            json.dump(wallet_data, f, indent=2)
        
        self.wallets[wallet.address] = wallet
        self.wallet_files[wallet.address] = wallet_file
        
        return wallet
    
    def load_wallet(self, address: str) -> BaseWallet:
        """加载现有钱包"""
        if address in self.wallets:
            return self.wallets[address]
        
        wallet_file = self.wallet_files.get(address)
        if not wallet_file or not os.path.exists(wallet_file):
            raise ValueError(f"钱包文件不存在: {address}")
        
        with open(wallet_file, 'r') as f:
            wallet_data = json.load(f)
        
        # 从PEM格式加载密钥
        private_key = serialization.load_pem_private_key(
            wallet_data['private_key'].encode(),
            password=None
        )
        
        wallet = BaseWallet()
        wallet.private_key = private_key
        wallet.public_key = private_key.public_key()
        wallet.address = wallet_data['address']
        
        self.wallets[wallet.address] = wallet
        return wallet
    
    def get_all_addresses(self) -> List[str]:
        """获取所有钱包地址"""
        return list(self.wallets.keys())


class SimpleWallet:
    """简化版钱包接口"""
    
    def __init__(self, wallet_manager: WalletManager):
        self.manager = wallet_manager
    
    def create_transaction(self, sender_address: str, recipient_address: str, amount: float) -> Transaction:
        """创建交易"""
        wallet = self.manager.load_wallet(sender_address)
        
        transaction = Transaction(
            sender=sender_address,
            recipient=recipient_address,
            amount=amount
        )
        
        # 签名交易
        transaction.signature = wallet.sign_transaction(transaction)
        return transaction


# 示例使用
if __name__ == "__main__":
    # 创建钱包管理器
    wm = WalletManager()
    
    # 创建两个钱包
    wallet1 = wm.create_wallet("alice")
    wallet2 = wm.create_wallet("bob")
    
    print(f"Alice的钱包地址: {wallet1.address}")
    print(f"Bob的钱包地址: {wallet2.address}")
    
    # 创建交易
    simple_wallet = SimpleWallet(wm)
    transaction = simple_wallet.create_transaction(wallet1.address, wallet2.address, 10.0)
    
    print(f"\n交易详情:")
    print(f"发送方: {transaction.sender[:10]}...")
    print(f"接收方: {transaction.recipient[:10]}...")
    print(f"金额: {transaction.amount}")
    print(f"签名: {transaction.signature[:20]}...")
    
    # 验证签名
    wallet_for_verification = wm.load_wallet(wallet1.address)
    is_valid = wallet_for_verification.verify_signature(transaction, transaction.signature)
    print(f"签名验证: {'有效' if is_valid else '无效'}")