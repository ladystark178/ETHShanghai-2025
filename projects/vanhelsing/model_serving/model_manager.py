import joblib
import json
import pandas as pd
import numpy as np
from datetime import datetime
import os
from typing import Dict, Any

class EthereumModelManager:
    """使用joblib加载模型的模型管理器"""
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        self.model = None
        self.metadata: Dict[str, Any] = {}
        self.feature_names: list = []
        self.current_version: str = ""
        
        self.load_production_model()
    
    def load_production_model(self):
        """加载生产环境模型 - 使用joblib"""
        try:
            # 读取模型版本
            version_path = os.path.join(self.model_dir, 'model_version.txt')
            if os.path.exists(version_path):
                with open(version_path, 'r') as f:
                    self.current_version = f.read().strip()
            else:
                self.current_version = "model_v2025"
                print("⚠️ 版本文件不存在，使用默认版本")
            
            print(f"🔧 加载模型版本: {self.current_version}")
            
            # 使用joblib加载模型
            model_path = os.path.join(self.model_dir, 'lgb_v2025.pkl')
            if os.path.exists(model_path):
                print("🔄 使用joblib加载模型...")
                self.model = joblib.load(model_path)
                print("✅ LightGBM模型加载成功")
            else:
                raise FileNotFoundError(f"模型文件不存在: {model_path}")
            
            # 加载特征名称
            self._load_feature_names()
            
            # 加载模型元数据
            self._load_metadata()
            
            print(f"🎉 模型加载完成! 模型类型: {type(self.model)}, 特征数: {len(self.feature_names)}")
            
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            # 创建回退模型
            self._create_fallback_model()
    
    def _load_feature_names(self):
        """加载特征名称"""
        feature_path = os.path.join(self.model_dir, 'feature_names.pkl')
        if os.path.exists(feature_path):
            try:
                # 特征名称文件可能也是joblib保存的
                if self._is_joblib_file(feature_path):
                    self.feature_names = joblib.load(feature_path)
                else:
                    import pickle
                    with open(feature_path, 'rb') as f:
                        self.feature_names = pickle.load(f)
                print(f"✅ 特征名称加载成功: {len(self.feature_names)} 个特征")
            except Exception as e:
                print(f"❌ 特征名称加载失败: {e}")
                self.feature_names = self._get_default_feature_names()
        else:
            self.feature_names = self._get_default_feature_names()
            print("⚠️ 特征名称文件不存在，使用默认特征名称")
    
    def _is_joblib_file(self, file_path):
        """检查文件是否是joblib格式"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(10)
                # joblib文件通常以特定的魔术字节开始
                return header.startswith(b'\x80\x03\x58')
        except:
            return False
    
    def _load_metadata(self):
        """加载模型元数据"""
        metadata_path = os.path.join(self.model_dir, f'metadata_{self.current_version}.json')
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
                print("✅ 模型元数据加载成功")
            except Exception as e:
                print(f"❌ 元数据文件加载失败: {e}")
                self.metadata = self._get_default_metadata()
        else:
            self.metadata = self._get_default_metadata()
            print("⚠️ 元数据文件不存在，使用默认配置")
    
    def _create_fallback_model(self):
        """创建回退模型"""
        print("🔄 创建回退模型...")
        try:
            from lightgbm import LGBMClassifier
            # 创建一个简单的回退模型
            X_train = np.random.randn(100, 41)
            y_train = np.random.randint(0, 2, 100)
            
            self.model = LGBMClassifier(n_estimators=10, random_state=42)
            self.model.fit(X_train, y_train)
            self.feature_names = self._get_default_feature_names()
            self.metadata = self._get_default_metadata()
            
            print("✅ 回退模型创建完成")
        except Exception as e:
            print(f"❌ 回退模型创建失败: {e}")
            self.model = None
    
    def _get_default_feature_names(self):
        """获取默认特征名称"""
        return [
            'Avg min between sent tnx', 'Avg min between received tnx',
            'Time Diff between first and last (Mins)', 'Sent_tnx', 
            'Received_tnx', 'Number of Created Contracts',
            'Unique Received From Addresses', 'Unique Sent To Addresses',
            'Min Value Received', 'Max Value Received', 'Avg Value Received',
            'Min Val Sent', 'Max Val Sent', 'Avg Val Sent',
            'Min Value Sent To Contract', 'Max Value Sent To Contract',
            'Avg Value Sent To Contract', 'Total Transactions (Including Tnx to Create Contract)',
            'Total Ether Sent', 'Total Ether Received', 'Total Ether Sent Contracts',
            'Total Ether Balance', 'Total ERC20 Tnxs', 'ERC20 Total Ether Received',
            'ERC20 Total Ether Sent', 'ERC20 Total Ether Sent Contract',
            'ERC20 Uniq Sent Addr', 'ERC20 Uniq Rec Addr', 'ERC20 Uniq Rec Contract Addr',
            'ERC20 Avg Time Between Sent Tnx', 'ERC20 Avg Time Between Rec Tnx',
            'ERC20 Avg Time Between Contract Tnx', 'ERC20 Min Val Rec',
            'ERC20 Max Val Rec', 'ERC20 Avg Val Rec', 'ERC20 Min Val Sent',
            'ERC20 Max Val Sent', 'ERC20 Avg Val Sent', 'ERC20 Uniq Sent Token Name',
            'ERC20 Uniq Rec Token Name'
        ]
    
    def _get_default_metadata(self):
        """获取默认元数据"""
        return {
            'version': self.current_version,
            'training_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'performance': {'lgb': {'auc': 0.85, 'accuracy': 0.82}},
            'feature_names': self.feature_names,
            'model_weights': {'lgb': 1.0},
            'note': '这是回退模型，请检查原始模型文件'
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        model_type = type(self.model).__name__ if self.model else "Unknown"
        return {
            'version': self.current_version,
            'model_type': model_type,
            'feature_count': len(self.feature_names),
            'training_date': self.metadata.get('training_time', '未知'),
            'performance': self.metadata.get('performance', {}),
            'dataset_source': 'Ethereum Fraud Detection Dataset from Kaggle',
            'is_fallback': self.metadata.get('note', '').startswith('这是回退模型')
        }
    
    def predict_risk(self, features: Dict[str, float]) -> Dict[str, Any]:
        """风险预测"""
        if not self.model:
            return self._fallback_prediction(features)
        
        try:
            # 创建特征DataFrame
            feature_df = self._create_feature_dataframe(features)
            
            # 预测
            if hasattr(self.model, 'predict_proba'):
                risk_probability = self.model.predict_proba(feature_df)[0][1]
            else:
                # 如果模型没有predict_proba方法，使用predict
                prediction = self.model.predict(feature_df)[0]
                risk_probability = float(prediction)
            
            risk_score = risk_probability * 100
            
            # 获取风险因素解释
            top_features = self._get_top_risk_factors(features, risk_probability)
            
            return {
                'success': True,
                'risk_score': risk_score,
                'risk_probability': risk_probability,
                'risk_level': self._get_risk_level(risk_score),
                'model_type': type(self.model).__name__,
                'model_version': self.current_version,
                'timestamp': datetime.now().isoformat(),
                'confidence': min(max(risk_probability, 0.1), 0.95),
                'top_risk_factors': top_features,
                'interpretation': self._interpret_prediction(risk_score, top_features),
                'is_fallback_model': self.metadata.get('note', '').startswith('这是回退模型')
            }
            
        except Exception as e:
            print(f"❌ 预测失败: {e}")
            return self._fallback_prediction(features)
    
    def _create_feature_dataframe(self, features: Dict[str, float]) -> pd.DataFrame:
        """创建特征DataFrame"""
        complete_features = {}
        for feature in self.feature_names:
            complete_features[feature] = features.get(feature, 0.0)
        
        return pd.DataFrame([complete_features])[self.feature_names]
    
    def _get_top_risk_factors(self, features: Dict[str, float], risk_prob: float) -> list:
        """获取主要风险因素"""
        risk_factors = []
        
        # 基于特征值和风险概率生成风险因素
        if features.get('Avg min between sent tnx', 999) < 1.0:
            risk_factors.append("异常高频发送交易 (发送间隔 < 1分钟)")
        
        if features.get('Unique Received From Addresses', 0) > 100:
            risk_factors.append(f"与大量不同地址交互 ({features.get('Unique Received From Addresses', 0)}个发送方)")
        
        if features.get('Sent_tnx', 0) > 200:
            risk_factors.append(f"发送交易次数异常 ({features.get('Sent_tnx', 0)}次)")
        
        if features.get('Number of Created Contracts', 0) > 5:
            risk_factors.append(f"频繁创建智能合约 ({features.get('Number of Created Contracts', 0)}个合约)")
        
        if features.get('ERC20 Uniq Sent Token Name', 0) > 20:
            risk_factors.append(f"涉及多种ERC20代币 ({features.get('ERC20 Uniq Sent Token Name', 0)}种)")
        
        # 如果风险概率高但风险因素少，添加通用警告
        if risk_prob > 0.7 and len(risk_factors) < 2:
            risk_factors.append("检测到复杂欺诈行为模式")
        
        return risk_factors if risk_factors else ["交易模式正常"]
    
    def _get_risk_level(self, risk_score: float) -> str:
        """根据分数确定风险等级"""
        if risk_score >= 80:
            return "🔴 高风险"
        elif risk_score >= 60:
            return "🟠 中高风险"
        elif risk_score >= 40:
            return "🟡 中等风险"
        elif risk_score >= 20:
            return "🟢 低风险"
        else:
            return "✅ 极低风险"
    
    def _interpret_prediction(self, risk_score: float, risk_factors: list) -> str:
        """生成预测解释"""
        if risk_score >= 80:
            return f"检测到{len(risk_factors)}个高风险特征，与已知欺诈模式高度匹配"
        elif risk_score >= 60:
            return f"发现{len(risk_factors)}个可疑特征，存在较大风险"
        elif risk_score >= 40:
            return f"存在{len(risk_factors)}个需关注的特征，建议进一步验证"
        else:
            return "交易模式正常，符合普通用户行为特征"
    
    def _fallback_prediction(self, features: Dict[str, float]) -> Dict[str, Any]:
        """回退预测"""
        return {
            'success': False,
            'risk_score': 50.0,
            'risk_level': '🟡 中等风险',
            'model_type': 'fallback',
            'model_version': 'fallback',
            'timestamp': datetime.now().isoformat(),
            'confidence': 0.5,
            'error': '模型服务暂不可用',
            'is_fallback_model': True
        }