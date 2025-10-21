from flask import Flask, request, jsonify
from model_manager import EthereumModelManager
from feature_server import EthereumFeatureServer
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 初始化服务
model_manager = EthereumModelManager("models")  # 指定模型目录
feature_server = EthereumFeatureServer()

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    try:
        model_info = model_manager.get_model_info()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'model_version': model_info['version'],
            'model_type': model_info['model_type'],
            'feature_count': model_info['feature_count'],
            'service': 'CryptoGuard ML Prediction API'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/model/info', methods=['GET'])
def model_info():
    """获取模型信息"""
    try:
        info = model_manager.get_model_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """风险预测端点"""
    try:
        start_time = datetime.now()
        
        # 获取请求数据
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '请求体为空'
            }), 400
        
        address = data.get('address', '')
        if not address:
            return jsonify({
                'success': False,
                'error': '缺少 address 字段'
            }), 400
        
        # 特征工程 - 将地址转换为模型特征
        features = feature_server.blockchain_to_model_features(address, data)
        
        # 模型预测
        prediction_result = model_manager.predict_risk(features)
        
        # 添加处理时间
        processing_time = (datetime.now() - start_time).total_seconds()
        prediction_result['processing_time_seconds'] = processing_time
        prediction_result['address'] = address
        
        logger.info(f"预测完成 - 地址: {address}, "
                   f"分数: {prediction_result['risk_score']:.1f}, "
                   f"耗时: {processing_time:.3f}s")
        
        return jsonify(prediction_result)
    
    except Exception as e:
        logger.error(f"预测请求处理失败: {e}")
        return jsonify({
            'success': False,
            'error': f'预测失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/batch/predict', methods=['POST'])
def batch_predict():
    """批量预测端点"""
    try:
        data = request.get_json()
        
        if not data or 'addresses' not in data:
            return jsonify({'error': '缺少 addresses 字段'}), 400
        
        addresses = data['addresses']
        if not isinstance(addresses, list):
            return jsonify({'error': 'addresses 必须是列表'}), 400
        
        results = []
        for address in addresses[:10]:  # 限制批量处理数量
            features = feature_server.blockchain_to_model_features(address, {})
            prediction = model_manager.predict_risk(features)
            prediction['address'] = address
            results.append(prediction)
        
        return jsonify({
            'success': True,
            'results': results,
            'total_processed': len(results),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/features/demo', methods=['GET'])
def features_demo():
    """特征演示端点 - 返回示例特征"""
    try:
        # 生成示例特征
        address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"  # Vitalik的地址作为示例
        features = feature_server.blockchain_to_model_features(address, {})
        
        return jsonify({
            'address': address,
            'features': features,
            'feature_count': len(features),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 启动 CryptoGuard ML API 服务...")
    print("📁 模型目录:", "model_serving/models")
    
    # 测试模型加载
    try:
        model_info = model_manager.get_model_info()
        print(f"✅ 模型加载成功: {model_info['model_type']} v{model_info['version']}")
        print(f"📊 特征数量: {model_info['feature_count']}")
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        exit(1)
    
    # 启动服务 - 修复编码问题
    print("🌐 API服务运行在: http://localhost:5000")
    try:
        # 方法1: 使用127.0.0.1代替0.0.0.0
        app.run(host='127.0.0.1', port=5000, debug=False)
    except UnicodeDecodeError:
        # 方法2: 如果还有问题，使用localhost
        print("⚠️ 检测到编码问题，使用localhost...")
        app.run(host='localhost', port=5000, debug=False)


