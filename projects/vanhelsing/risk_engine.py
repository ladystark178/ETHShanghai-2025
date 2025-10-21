#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import asyncio
import nest_asyncio

# 修复事件循环问题
try:
    nest_asyncio.apply()
except:
    pass

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
from web3 import Web3
import json

class CryptoGuardRiskEngine:
    def __init__(self):
        self.risk_weights = {
            'transaction_velocity': 0.25,
            'behavior_pattern': 0.20,
            'contract_interaction': 0.15,
            'association_risk': 0.30,
            'reputation_score': 0.10
        }
        
        # 加载已知风险模式数据库
        self.risk_patterns = self.load_risk_patterns()
        
    def load_risk_patterns(self):
        """加载已知风险地址和模式"""
        return {
            "known_scam_addresses": {
                "0x8576acc5c05d6ce88f4e49bf65bdf0c62f91353c": {
                    "type": "phishing",
                    "severity": "high",
                    "description": "Known phishing wallet"
                },
                "0x901bb9583b24d97e995513c6778dc6888ab6870e": {
                    "type": "scam",
                    "severity": "high", 
                    "description": "Fake token sale"
                }
            },
            "suspicious_contracts": {
                "0x1d505c58d4c31c68f4de3d5c6bb9c3bd6b7e2a2a": "Malicious smart contract"
            },
            "behavioral_redflags": [
                "rapid_token_minting",
                "high_frequency_arbitrage", 
                "micro_transaction_spam",
                "address_poisoning"
            ]
        }
    
    def analyze_address_risk(self, address, transaction_data=None):
        """综合分析地址风险"""
        print(f"🔍 Analyzing risk for address: {address}")
        
        risk_factors = []
        risk_score = 0
        detailed_analysis = {}
        
        # 1. 基础地址验证
        if not self.is_valid_address(address):
            return self._generate_risk_result(100, ["Invalid Ethereum address"], {})
        
        # 2. 已知风险地址检查
        known_risk = self.check_known_risks(address)
        if known_risk:
            risk_factors.append(known_risk['description'])
            risk_score += 70
            detailed_analysis['known_risks'] = known_risk
        
        # 3. 交易模式分析
        tx_analysis = self.analyze_transaction_patterns(address, transaction_data)
        if tx_analysis['risk_level'] != 'low':
            risk_factors.extend(tx_analysis['factors'])
            risk_score += tx_analysis['score'] * self.risk_weights['transaction_velocity']
        detailed_analysis['transactions'] = tx_analysis
        
        # 4. 行为模式分析
        behavior_analysis = self.analyze_behavior_patterns(address, transaction_data)
        if behavior_analysis['risk_level'] != 'low':
            risk_factors.extend(behavior_analysis['factors'])
            risk_score += behavior_analysis['score'] * self.risk_weights['behavior_pattern']
        detailed_analysis['behavior'] = behavior_analysis
        
        # 5. 合约交互分析
        contract_analysis = self.analyze_contract_interactions(address, transaction_data)
        if contract_analysis['risk_level'] != 'low':
            risk_factors.extend(contract_analysis['factors'])
            risk_score += contract_analysis['score'] * self.risk_weights['contract_interaction']
        detailed_analysis['contracts'] = contract_analysis
        
        # 6. 关联风险分析
        association_analysis = self.analyze_association_risk(address)
        if association_analysis['risk_level'] != 'low':
            risk_factors.extend(association_analysis['factors'])
            risk_score += association_analysis['score'] * self.risk_weights['association_risk']
        detailed_analysis['associations'] = association_analysis
        
        # 确保分数在0-100之间
        risk_score = min(100, risk_score)
        
        return self._generate_risk_result(risk_score, risk_factors, detailed_analysis)
    
    def is_valid_address(self, address):
        """验证以太坊地址格式"""
        try:
            return Web3.is_address(address)
        except:
            return False
    
    def check_known_risks(self, address):
        """检查已知风险地址"""
        address_lower = address.lower()
        for risk_addr, info in self.risk_patterns["known_scam_addresses"].items():
            if address_lower == risk_addr.lower():
                return info
        return None
    
    def analyze_transaction_patterns(self, address, transaction_data):
        """分析交易模式"""
        factors = []
        score = 0
        
        # 模拟交易数据分析
        # 在实际应用中，这里应该调用区块链API获取真实数据
        simulated_data = self._simulate_transaction_data(address)
        
        # 高频交易检测
        if simulated_data['tx_count_24h'] > 100:
            factors.append(f"High transaction frequency: {simulated_data['tx_count_24h']} transactions in 24h")
            score += 40
        
        # 异常时间模式
        if simulated_data['night_activity_ratio'] > 0.7:
            factors.append("Unusual activity pattern: high nighttime transactions")
            score += 20
        
        # 小额测试交易
        if simulated_data['micro_tx_count'] > 10:
            factors.append("Multiple micro-transactions detected (possible testing)")
            score += 15
        
        risk_level = 'high' if score >= 40 else 'medium' if score >= 20 else 'low'
        
        return {
            'risk_level': risk_level,
            'score': score,
            'factors': factors,
            'metrics': simulated_data
        }
    
    def analyze_behavior_patterns(self, address, transaction_data):
        """分析行为模式"""
        factors = []
        score = 0
        
        # 模拟行为分析
        simulated_behavior = self._simulate_behavior_data(address)
        
        # 快速资金周转
        if simulated_behavior['fund_rotation_ratio'] > 0.8:
            factors.append("Rapid fund rotation detected")
            score += 25
        
        # 与新建地址交互
        if simulated_behavior['new_address_interactions'] > 15:
            factors.append("Frequent interactions with newly created addresses")
            score += 20
        
        # 混合器使用模式
        if simulated_behavior['mixer_usage_suspected']:
            factors.append("Possible mixer/tumbler usage pattern")
            score += 30
        
        risk_level = 'high' if score >= 30 else 'medium' if score >= 15 else 'low'
        
        return {
            'risk_level': risk_level,
            'score': score,
            'factors': factors,
            'behavior_metrics': simulated_behavior
        }
    
    def analyze_contract_interactions(self, address, transaction_data):
        """分析合约交互风险"""
        factors = []
        score = 0
        
        # 模拟合约交互数据
        contract_interactions = self._simulate_contract_data(address)
        
        # 与已知风险合约交互
        if contract_interactions['known_risky_interactions'] > 0:
            factors.append(f"Interacted with {contract_interactions['known_risky_interactions']} known risky contracts")
            score += 50
        
        # 可疑合约方法调用
        if contract_interactions['suspicious_method_calls']:
            factors.extend([f"Suspicious method: {method}" for method in contract_interactions['suspicious_method_calls']])
            score += 30
        
        # 新合约部署模式
        if contract_interactions['new_contracts_deployed'] > 5:
            factors.append("Multiple new contracts deployed (possible scam factory)")
            score += 25
        
        risk_level = 'high' if score >= 40 else 'medium' if score >= 20 else 'low'
        
        return {
            'risk_level': risk_level,
            'score': score,
            'factors': factors,
            'contract_metrics': contract_interactions
        }
    
    def analyze_association_risk(self, address):
        """分析关联风险"""
        factors = []
        score = 0
        
        # 模拟关联分析
        association_data = self._simulate_association_data(address)
        
        # 直接关联风险
        if association_data['direct_high_risk_associations'] > 0:
            factors.append(f"Direct association with {association_data['direct_high_risk_associations']} high-risk addresses")
            score += 40
        
        # 二级关联风险
        if association_data['secondary_risk_associations'] > 10:
            factors.append(f"Multiple secondary associations with risky addresses")
            score += 25
        
        # 集群风险
        if association_data['risk_cluster_member']:
            factors.append("Member of known risk cluster")
            score += 35
        
        risk_level = 'high' if score >= 40 else 'medium' if score >= 20 else 'low'
        
        return {
            'risk_level': risk_level,
            'score': score,
            'factors': factors,
            'association_metrics': association_data
        }
    
    def _generate_risk_result(self, risk_score, risk_factors, detailed_analysis):
        """生成标准化风险结果"""
        return {
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'risk_factors': risk_factors,
            'detailed_analysis': detailed_analysis,
            'timestamp': datetime.now().isoformat(),
            'recommended_actions': self._get_recommended_actions(risk_score)
        }
    
    def _get_risk_level(self, score):
        """根据分数确定风险等级"""
        if score >= 75:
            return "🔴 HIGH RISK"
        elif score >= 50:
            return "🟠 MEDIUM RISK"
        elif score >= 25:
            return "🟡 LOW RISK"
        else:
            return "🟢 MINIMAL RISK"
    
    def _get_recommended_actions(self, risk_score):
        """根据风险分数推荐行动"""
        if risk_score >= 75:
            return [
                "Immediately revoke any token approvals",
                "Do not interact with this address",
                "Report to wallet security team",
                "Consider moving funds to new wallet"
            ]
        elif risk_score >= 50:
            return [
                "Exercise extreme caution",
                "Verify transaction details carefully",
                "Limit interaction amounts",
                "Monitor for suspicious activity"
            ]
        elif risk_score >= 25:
            return [
                "Proceed with caution",
                "Double-check addresses",
                "Use small test transactions first"
            ]
        else:
            return ["Standard security practices recommended"]
    
    # 模拟数据生成方法（在实际应用中替换为真实数据）
    def _simulate_transaction_data(self, address):
        return {
            'tx_count_24h': np.random.randint(0, 200),
            'night_activity_ratio': np.random.random(),
            'micro_tx_count': np.random.randint(0, 20),
            'avg_tx_value': np.random.uniform(0.001, 10)
        }
    
    def _simulate_behavior_data(self, address):
        return {
            'fund_rotation_ratio': np.random.random(),
            'new_address_interactions': np.random.randint(0, 30),
            'mixer_usage_suspected': np.random.random() > 0.7
        }
    
    def _simulate_contract_data(self, address):
        return {
            'known_risky_interactions': np.random.randint(0, 3),
            'suspicious_method_calls': ['unlimited_approval', 'hidden_transfer'] if np.random.random() > 0.8 else [],
            'new_contracts_deployed': np.random.randint(0, 10)
        }
    
    def _simulate_association_data(self, address):
        return {
            'direct_high_risk_associations': np.random.randint(0, 5),
            'secondary_risk_associations': np.random.randint(0, 20),
            'risk_cluster_member': np.random.random() > 0.9
        }

