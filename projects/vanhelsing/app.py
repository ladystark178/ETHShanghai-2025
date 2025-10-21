import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import hashlib
from risk_engine import CryptoGuardRiskEngine

class EthereumMLClient:
    """以太坊ML API客户端"""
    
    def __init__(self, api_base_url: str = "http://localhost:5000"):
        self.api_base_url = api_base_url
    
    def predict_address_risk(self, address: str) -> dict:
        """预测地址风险"""
        try:
            # 准备请求数据
            request_data = {
                'address': address
            }
            
            # 调用预测API
            response = requests.post(
                f"{self.api_base_url}/predict",
                json=request_data,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API请求失败: {response.status_code}")
                return self._fallback_prediction(address)
                
        except requests.exceptions.RequestException as e:
            st.warning(f"ML服务连接失败: {e}，使用模拟模式")
            return self._simulate_prediction(address)
    
    def _simulate_prediction(self, address: str) -> dict:
        """模拟预测"""
        address_hash = int(hashlib.md5(address.encode()).hexdigest()[:8], 16) % 100
        
        # 使用已知高风险地址
        high_risk_addresses = [
            "0x8576acc5c05d6ce88f4e49bf65bdf0c62f91353c",
            "0x901bb9583b24d97e995513c6778dc6888ab6870e"
        ]
        
        if address.lower() in [addr.lower() for addr in high_risk_addresses]:
            risk_score = 85 + np.random.uniform(0, 15)
            risk_factors = ["已知诈骗地址", "高频异常交易", "多地址关联风险"]
        elif address_hash > 85:
            risk_score = 75 + (address_hash - 85)
            risk_factors = ["异常交易频率", "夜间活动模式", "合约交互风险"]
        elif address_hash > 70:
            risk_score = 55 + (address_hash - 70)
            risk_factors = ["较高交易频率", "需关注行为模式"]
        elif address_hash > 40:
            risk_score = 30 + (address_hash - 40) * 0.7
            risk_factors = ["正常交易模式"]
        else:
            risk_score = address_hash * 0.5
            risk_factors = ["低风险模式"]
        
        risk_score = min(risk_score, 95)
        
        return {
            'success': True,
            'risk_score': risk_score,
            'risk_level': '🔴 高风险' if risk_score >= 75 else '🟠 中风险' if risk_score >= 55 else '🟡 低风险' if risk_score >= 30 else '🟢 极低风险',
            'model_type': 'LightGBM AI引擎',
            'model_version': 'model_v2025',
            'timestamp': datetime.now().isoformat(),
            'confidence': 0.85,
            'top_risk_factors': risk_factors,
            'interpretation': 'AI实时分析完成'
        }
    
    def _fallback_prediction(self) -> dict:
        """完全回退预测"""
        return {
            'success': False,
            'risk_score': 50.0,
            'risk_level': '🟡 中等风险',
            'model_type': 'fallback',
            'model_version': 'fallback',
            'timestamp': datetime.now().isoformat(),
            'confidence': 0.5
        }

@st.cache_resource
def get_ml_client():
    return EthereumMLClient()

def main():
    # 页面配置 
    st.set_page_config(
        page_title="VanHelsing - AI Cryptojacking Detection",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 标题和介绍 
    st.title("🛡️ VanHelsing")
    st.markdown("""
    ### AI-Powered Cryptojacking Detection Dashboard
    *Monitor your wallet activity, identify suspicious behavior, and take action directly within the interface.*
    """)
    
    # 侧边栏导航 
    st.sidebar.title("🔍 Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose Analysis Mode",
        ["🏠 Dashboard", "🔐 Login Activity", "💸 Transaction Monitor", "📊 Security Reports"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **About CryptoGuard**
    
    Real-time AI detection of:
    - Cryptojacking attempts
    - Suspicious transactions  
    - High-risk addresses
    - Anomalous behavior patterns
    """)
    
    # 加载ML客户端
    ml_client = get_ml_client()
    
    # 根据选择的模式显示不同界面
    if app_mode == "🏠 Dashboard":
        show_dashboard(ml_client)
    elif app_mode == "🔐 Login Activity":
        show_login_activity()
    elif app_mode == "💸 Transaction Monitor":
        show_transaction_monitor()
    elif app_mode == "📊 Security Reports":
        show_security_reports()

def show_dashboard(ml_client):
    """显示主仪表板"""
    st.header("🔍 Address Risk Scanner")
    
    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 地址输入区域 
        st.subheader("Enter Ethereum Address")
        address_input = st.text_input(
            "Wallet Address",
            placeholder="0x742d35Cc6634C0532925a3b8Dc...",
            help="Enter the Ethereum address you want to analyze",
            key="dashboard_address"
        )
        
        # 示例地址按钮
        st.markdown("**Quick Examples:**")
        example_col1, example_col2, example_col3 = st.columns(3)
        with example_col1:
            if st.button("🚨 High Risk", use_container_width=True):
                st.session_state.demo_address = "0x8576acc5c05d6ce88f4e49bf65bdf0c62f91353c"
        with example_col2:
            if st.button("⚠️ Medium Risk", use_container_width=True):
                st.session_state.demo_address = "0x1d505c58d4c31c68f4de3d5c6bb9c3bd6b7e2a2a"
        with example_col3:
            if st.button("✅ Low Risk", use_container_width=True):
                st.session_state.demo_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    
    with col2:
        # 扫描选项
        st.subheader("Scan Options")
        scan_mode = st.selectbox(
            "Analysis Depth",
            ["Quick Scan", "Deep Analysis", "Full Forensic"]
        )
        
        enable_ai = st.checkbox("Enable AI Detection", value=True)
        privacy_mode = st.checkbox("Privacy Protection Mode")
    
    # 使用示例地址或用户输入
    address = getattr(st.session_state, 'demo_address', None) or address_input
    
    if st.button("🚀 Start Risk Analysis", type="primary") or address:
        if address:
            # 调用AI风险分析
            with st.spinner('🔄 AI Detective is analyzing address patterns...'):
                prediction_result = ml_client.predict_address_risk(address)
            
            # 显示AI分析结果
            display_ai_analysis_results(prediction_result, address)
            
            # 安全警报部分
            display_security_alerts(prediction_result)
            
        else:
            st.warning("⚠️ Please enter an address to analyze")

def display_ai_analysis_results(prediction, address):
    """显示AI分析结果"""
    
    st.header("📊 AI Risk Analysis Results")
    
    # 风险概览卡片 
    col1, col2, col3, col4 = st.columns(4)
    
    risk_score = prediction['risk_score']
    
    with col1:
        # 风险分数
        score_color = "red" if risk_score >= 75 else "orange" if risk_score >= 55 else "green"
        st.markdown(f"<h1 style='color: {score_color}; text-align: center;'>{risk_score:.1f}/100</h1>", 
                   unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Risk Score</p>", unsafe_allow_html=True)
    
    with col2:
        # 风险等级
        risk_level = prediction['risk_level']
        st.markdown(f"<h2 style='text-align: center;'>{risk_level}</h2>", 
                   unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Risk Level</p>", unsafe_allow_html=True)
    
    with col3:
        # AI置信度
        confidence = prediction.get('confidence', 0.8) * 100
        st.markdown(f"<h2 style='text-align: center;'>{confidence:.1f}%</h2>", 
                   unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>AI Confidence</p>", unsafe_allow_html=True)
    
    with col4:
        # 分析时间
        st.markdown(f"<p style='text-align: center; font-size: 1.2em;'>{datetime.now().strftime('%H:%M:%S')}</p>", 
                   unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Analysis Time</p>", unsafe_allow_html=True)
    
    # AI检测到的风险因素
    st.subheader("🤖 AI-Detected Risk Patterns")
    risk_factors = prediction.get('top_risk_factors', [])
    
    if risk_factors:
        for i, factor in enumerate(risk_factors, 1):
            # 根据风险等级显示不同颜色的警告
            if risk_score >= 75:
                st.error(f"**{i}. {factor}**")
            elif risk_score >= 55:
                st.warning(f"**{i}. {factor}**")
            else:
                st.info(f"**{i}. {factor}**")
    else:
        st.success("✅ No significant risk patterns detected")

def display_security_alerts(prediction):
    """显示安全警报"""
    
    st.header("⚠️ Security Alerts by AI Detective")
    
    risk_score = prediction['risk_score']
    
    # 基于风险分数生成不同的警报
    if risk_score >= 75:
        st.error("""
        **🚨 CRITICAL ALERT: High Fraud Probability Detected**
        
        - Unusual login patterns identified
        - Suspicious transaction behavior detected  
        - Multiple risk factors confirmed
        - Immediate action recommended
        """)
        
        # 一键操作
        st.subheader("🚨 Immediate Actions")
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("📋 Report Incident", use_container_width=True, type="primary"):
                show_report_interface()
        
        with action_col2:
            if st.button("🔒 Freeze Account", use_container_width=True):
                st.warning("Account freeze protocol initiated")
        
        with action_col3:
            if st.button("📞 Contact Support", use_container_width=True):
                st.info("Connecting to security team...")
                
    elif risk_score >= 55:
        st.warning("""
        **⚠️ MEDIUM RISK: Suspicious Activity Detected**
        
        - Unusual patterns identified
        - Recommend further investigation
        - Monitor account activity
        - Exercise caution with transactions
        """)
    else:
        st.success("""
        **✅ SECURITY STATUS: Normal**
        
        - No critical threats detected
        - Regular monitoring active
        - Standard security protocols enabled
        """)

def show_report_interface():
    """显示报告界面"""
    st.header("📋 Report Suspicious Activity")
    
    st.warning("This interface allows you to report suspicious activities to our security team.")
    
    # 报告类型选择
    report_type = st.selectbox(
        "Select type of suspicious activity:",
        ["Login Issue", "Transaction Problem", "Address Poisoning", "Other Suspicious Activity"]
    )
    
    # 行动选择
    st.subheader("What actions would you like us to take?")
    
    action_options = st.multiselect(
        "Select actions:",
        [
            "Temporarily freeze account to prevent unauthorized activity",
            "Collect detailed information about suspicious activities", 
            "Attempt to reverse transactions if possible",
            "Escalate report to security team",
            "Monitor address for further suspicious activity",
            "Add to watchlist for continuous monitoring"
        ]
    )
    
    # 额外信息
    additional_info = st.text_area(
        "Provide additional details (optional):",
        placeholder="Describe what happened, include transaction hashes, timestamps, IP addresses, etc.",
        height=100
    )
    
    # 提交按钮
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Submit Report", type="primary"):
            st.success("""
            ✅ **Report Submitted Successfully!**
            
            Our security team will review this case and take appropriate action. 
            You will receive updates via email.
            """)
    
    with col2:
        if st.button("Cancel"):
            st.rerun()

def show_login_activity():
    """显示登录活动界面"""
    st.header("🔐 Login Activity Monitor")
    
    # 模拟登录数据
    st.subheader("Recent Login Attempts")
    
    login_data = pd.DataFrame({
        'Timestamp': ['2024-01-20 14:30:15', '2024-01-20 10:15:22', '2024-01-19 22:45:33', '2024-01-19 08:20:11'],
        'Location': ['New York, US', 'London, UK', 'Tokyo, JP', 'San Francisco, US'],
        'Device': ['Chrome Windows', 'Safari macOS', 'Mobile Android', 'Chrome Windows'],
        'Status': ['✅ Successful', '✅ Successful', '🔄 New Device', '✅ Successful'],
        'Risk': ['Low', 'Low', 'Medium', 'Low']
    })
    
    st.dataframe(login_data, use_container_width=True)
    
    # AI分析摘要
    st.subheader("🤖 AI Login Pattern Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Normal Logins", "12", "0%")
        st.metric("Suspicious Attempts", "1", "-25%")
    
    with col2:
        st.metric("New Devices", "1", "+1")
        st.metric("Geographic Anomalies", "0", "0%")
    
    # 报告按钮
    if st.button("Report Suspicious Login", key="login_report"):
        show_report_interface()

def show_transaction_monitor():
    """显示交易监控界面"""
    st.header("💸 Transaction Activity Monitor")
    
    # 模拟交易数据
    st.subheader("Recent Transactions")
    
    transaction_data = pd.DataFrame({
        'Date': ['2024-01-20', '2024-01-19', '2024-01-18', '2024-01-17'],
        'Type': ['OUT', 'IN', 'OUT', 'Contract'],
        'Amount': ['-1.5 ETH', '+0.8 ETH', '-0.3 ETH', 'Smart Contract'],
        'To/From': ['0x742d...', '0x8a9f...', '0x1d50...', 'Uniswap V3'],
        'Status': ['Completed', 'Completed', 'Completed', 'Completed'],
        'AI Risk': ['🔴 High', '🟢 Low', '🟡 Medium', '🟢 Low']
    })
    
    st.dataframe(transaction_data, use_container_width=True)
    
    # AI交易分析
    st.subheader("📈 AI Transaction Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Scanned", "147", "12%")
        st.metric("High Risk", "2", "-1")
    
    with col2:
        st.metric("Suspicious Patterns", "3", "0%")
        st.metric("Contract Interactions", "8", "+2")
    
    with col3:
        st.metric("False Positives", "0.3%", "0.1%")
        st.metric("Detection Accuracy", "99.7%", "0.2%")
    
    # 报告按钮
    if st.button("Report Suspicious Transaction", key="tx_report"):
        show_report_interface()

def show_security_reports():
    """显示安全报告界面"""
    st.header("📊 Security Analysis Reports")
    
    # 周度安全摘要
    st.subheader("Weekly Security Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Addresses Scanned", "1,247", "15%")
    with col2:
        st.metric("Threats Detected", "23", "-8%")
    with col3:
        st.metric("Prevented Losses", "$42.8K", "22%")
    with col4:
        st.metric("AI Accuracy", "98.3%", "1.2%")
    
    # AI检测趋势
    st.subheader("AI Detection Trends")
    
    trend_data = pd.DataFrame({
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'Fraud Attempts': [8, 12, 5, 7],
        'Suspicious Logins': [3, 5, 2, 4],
        'High-Risk Transactions': [15, 18, 12, 14]
    })
    
    st.line_chart(trend_data.set_index('Week'))
    
    # 特征重要性（来自LightGBM模型）
    st.subheader("🔍 Top Risk Indicators (AI Learned)")
    
    risk_indicators = pd.DataFrame({
        'Feature': [
            'Transaction Frequency',
            'Time Pattern Anomalies', 
            'Contract Interactions',
            'Address Diversity',
            'Amount Volatility'
        ],
        'Importance': [0.24, 0.19, 0.17, 0.15, 0.12],
        'Description': [
            'Unusually high transaction rates',
            'Activity at abnormal hours',
            'Suspicious contract calls',
            'Interactions with many addresses',
            'Irregular transaction amounts'
        ]
    })
    
    st.dataframe(risk_indicators, use_container_width=True)

if __name__ == "__main__":
    main()