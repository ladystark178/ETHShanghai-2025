import pandas as pd
import numpy as np
from datetime import datetime
import hashlib

class EthereumFeatureServer:
    """以太坊特征服务 - 将地址转换为模型特征"""
    
    def __init__(self):
        self.feature_mapping = {
            # 基于数据集的41个特征
            'Avg min between sent tnx': 'average_time_between_sent',
            'Avg min between received tnx': 'average_time_between_received',
            'Time Diff between first and last (Mins)': 'time_diff_first_last',
            'Sent_tnx': 'sent_transactions',
            'Received_tnx': 'received_transactions',
            'Number of Created Contracts': 'created_contracts',
            'Unique Received From Addresses': 'unique_senders',
            'Unique Sent To Addresses': 'unique_receivers',
            'Min Value Received': 'min_ether_received',
            'Max Value Received': 'max_ether_received',
            'Avg Value Received': 'avg_ether_received',
            'Min Val Sent': 'min_ether_sent',
            'Max Val Sent': 'max_ether_sent',
            'Avg Val Sent': 'avg_ether_sent',
            'Min Value Sent To Contract': 'min_contract_sent',
            'Max Value Sent To Contract': 'max_contract_sent',
            'Avg Value Sent To Contract': 'avg_contract_sent',
            'Total Transactions (Including Tnx to Create Contract)': 'total_transactions',
            'Total Ether Sent': 'total_ether_sent',
            'Total Ether Received': 'total_ether_received',
            'Total Ether Sent Contracts': 'total_contract_sent',
            'Total Ether Balance': 'ether_balance',
            'Total ERC20 Tnxs': 'erc20_transactions',
            'ERC20 Total Ether Received': 'erc20_total_received',
            'ERC20 Total Ether Sent': 'erc20_total_sent',
            'ERC20 Total Ether Sent Contract': 'erc20_contract_sent',
            'ERC20 Uniq Sent Addr': 'erc20_unique_sent',
            'ERC20 Uniq Rec Addr': 'erc20_unique_received',
            'ERC20 Uniq Rec Contract Addr': 'erc20_contract_received',
            'ERC20 Avg Time Between Sent Tnx': 'erc20_avg_sent_interval',
            'ERC20 Avg Time Between Rec Tnx': 'erc20_avg_received_interval',
            'ERC20 Avg Time Between Contract Tnx': 'erc20_avg_contract_interval',
            'ERC20 Min Val Rec': 'erc20_min_received',
            'ERC20 Max Val Rec': 'erc20_max_received',
            'ERC20 Avg Val Rec': 'erc20_avg_received',
            'ERC20 Min Val Sent': 'erc20_min_sent',
            'ERC20 Max Val Sent': 'erc20_max_sent',
            'ERC20 Avg Val Sent': 'erc20_avg_sent',
            'ERC20 Uniq Sent Token Name': 'erc20_unique_tokens_sent',
            'ERC20 Uniq Rec Token Name': 'erc20_unique_tokens_received'
        }
    
    def blockchain_to_model_features(self, address: str, blockchain_data: dict) -> dict:
        """将区块链地址转换为模型特征"""
        # 使用确定性随机生成基于地址的特征
        # 在实际应用中，这里应该调用Etherscan API获取真实数据
        return self._generate_deterministic_features(address)
    
    def _generate_deterministic_features(self, address: str) -> dict:
        """基于地址生成确定性特征"""
        # 使用地址哈希作为随机种子，确保相同地址得到相同特征
        address_hash = int(hashlib.md5(address.encode()).hexdigest()[:8], 16)
        np.random.seed(address_hash)
        
        features = {}
        
        # 模拟高风险和低风险地址的特征差异
        is_high_risk = address_hash % 100 < 15  # 15% 高风险
        
        if is_high_risk:
            # 高风险地址特征模式
            features['Avg min between sent tnx'] = max(0.1, np.random.exponential(0.5))
            features['Avg min between received tnx'] = max(0.5, np.random.exponential(2.0))
            features['Time Diff between first and last (Mins)'] = np.random.uniform(100, 5000)
            features['Sent_tnx'] = np.random.poisson(150) + 50
            features['Received_tnx'] = np.random.poisson(30) + 10
            features['Number of Created Contracts'] = np.random.poisson(3) + 2
            features['Unique Received From Addresses'] = np.random.poisson(80) + 20
            features['Unique Sent To Addresses'] = np.random.poisson(100) + 30
            features['Min Value Received'] = max(0.001, np.random.exponential(0.05))
            features['Max Value Received'] = np.random.exponential(3.0) + 1.0
            features['Avg Value Received'] = np.random.exponential(0.8) + 0.2
            features['Min Val Sent'] = max(0.001, np.random.exponential(0.03))
            features['Max Val Sent'] = np.random.exponential(8.0) + 2.0
            features['Avg Val Sent'] = np.random.exponential(1.5) + 0.5
            features['Min Value Sent To Contract'] = max(0.001, np.random.exponential(0.1))
            features['Max Value Sent To Contract'] = np.random.exponential(2.0) + 0.5
            features['Avg Value Sent To Contract'] = np.random.exponential(0.5) + 0.1
            features['Total Transactions (Including Tnx to Create Contract)'] = np.random.poisson(180) + 20
            features['Total Ether Sent'] = np.random.exponential(40.0) + 10.0
            features['Total Ether Received'] = np.random.exponential(15.0) + 5.0
            features['Total Ether Sent Contracts'] = np.random.exponential(4.0) + 1.0
            features['Total Ether Balance'] = max(0, np.random.normal(3.0, 2.0))
            features['Total ERC20 Tnxs'] = np.random.poisson(200) + 50
            features['ERC20 Total Ether Received'] = np.random.exponential(12.0) + 3.0
            features['ERC20 Total Ether Sent'] = np.random.exponential(20.0) + 5.0
            features['ERC20 Total Ether Sent Contract'] = np.random.exponential(2.0) + 0.5
            features['ERC20 Uniq Sent Addr'] = np.random.poisson(80) + 20
            features['ERC20 Uniq Rec Addr'] = np.random.poisson(50) + 10
            features['ERC20 Uniq Rec Contract Addr'] = np.random.poisson(8) + 2
            features['ERC20 Avg Time Between Sent Tnx'] = max(0.5, np.random.exponential(1.0))
            features['ERC20 Avg Time Between Rec Tnx'] = max(1.0, np.random.exponential(2.0))
            features['ERC20 Avg Time Between Contract Tnx'] = max(1.0, np.random.exponential(1.5))
            features['ERC20 Min Val Rec'] = max(0.001, np.random.exponential(0.03))
            features['ERC20 Max Val Rec'] = np.random.exponential(1.5) + 0.5
            features['ERC20 Avg Val Rec'] = np.random.exponential(0.2) + 0.1
            features['ERC20 Min Val Sent'] = max(0.001, np.random.exponential(0.02))
            features['ERC20 Max Val Sent'] = np.random.exponential(2.0) + 0.5
            features['ERC20 Avg Val Sent'] = np.random.exponential(0.3) + 0.1
            features['ERC20 Uniq Sent Token Name'] = np.random.poisson(15) + 5
            features['ERC20 Uniq Rec Token Name'] = np.random.poisson(10) + 3
        else:
            # 正常地址特征模式
            features['Avg min between sent tnx'] = np.random.exponential(15.0) + 5.0
            features['Avg min between received tnx'] = np.random.exponential(20.0) + 5.0
            features['Time Diff between first and last (Mins)'] = np.random.uniform(10000, 100000)
            features['Sent_tnx'] = np.random.poisson(40) + 5
            features['Received_tnx'] = np.random.poisson(35) + 5
            features['Number of Created Contracts'] = np.random.poisson(1)
            features['Unique Received From Addresses'] = np.random.poisson(25) + 5
            features['Unique Sent To Addresses'] = np.random.poisson(20) + 5
            features['Min Value Received'] = max(0.001, np.random.exponential(0.3))
            features['Max Value Received'] = np.random.exponential(1.5) + 0.5
            features['Avg Value Received'] = np.random.exponential(0.6) + 0.2
            features['Min Val Sent'] = max(0.001, np.random.exponential(0.2))
            features['Max Val Sent'] = np.random.exponential(1.2) + 0.3
            features['Avg Val Sent'] = np.random.exponential(0.5) + 0.1
            features['Min Value Sent To Contract'] = max(0.001, np.random.exponential(0.05))
            features['Max Value Sent To Contract'] = np.random.exponential(0.3) + 0.1
            features['Avg Value Sent To Contract'] = np.random.exponential(0.1) + 0.05
            features['Total Transactions (Including Tnx to Create Contract)'] = np.random.poisson(80) + 10
            features['Total Ether Sent'] = np.random.exponential(12.0) + 3.0
            features['Total Ether Received'] = np.random.exponential(10.0) + 2.0
            features['Total Ether Sent Contracts'] = np.random.exponential(0.3) + 0.1
            features['Total Ether Balance'] = max(0, np.random.normal(1.5, 1.0))
            features['Total ERC20 Tnxs'] = np.random.poisson(60) + 10
            features['ERC20 Total Ether Received'] = np.random.exponential(4.0) + 1.0
            features['ERC20 Total Ether Sent'] = np.random.exponential(3.0) + 1.0
            features['ERC20 Total Ether Sent Contract'] = np.random.exponential(0.2) + 0.1
            features['ERC20 Uniq Sent Addr'] = np.random.poisson(15) + 5
            features['ERC20 Uniq Rec Addr'] = np.random.poisson(12) + 3
            features['ERC20 Uniq Rec Contract Addr'] = np.random.poisson(1)
            features['ERC20 Avg Time Between Sent Tnx'] = np.random.exponential(25.0) + 5.0
            features['ERC20 Avg Time Between Rec Tnx'] = np.random.exponential(30.0) + 5.0
            features['ERC20 Avg Time Between Contract Tnx'] = np.random.exponential(35.0) + 5.0
            features['ERC20 Min Val Rec'] = max(0.001, np.random.exponential(0.08))
            features['ERC20 Max Val Rec'] = np.random.exponential(0.6) + 0.2
            features['ERC20 Avg Val Rec'] = np.random.exponential(0.15) + 0.05
            features['ERC20 Min Val Sent'] = max(0.001, np.random.exponential(0.06))
            features['ERC20 Max Val Sent'] = np.random.exponential(0.5) + 0.1
            features['ERC20 Avg Val Sent'] = np.random.exponential(0.12) + 0.03
            features['ERC20 Uniq Sent Token Name'] = np.random.poisson(4) + 1
            features['ERC20 Uniq Rec Token Name'] = np.random.poisson(3) + 1
        
        return features

