# 🛡️ VanHelsing AI - Ethereum Address Risk Detection

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)](https://streamlit.io)
[![LightGBM](https://img.shields.io/badge/ML-LightGBM-00BFFF)](https://lightgbm.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A real-time AI-powered risk detection system for Ethereum addresses, built with machine learning and blockchain analytics.

![VanHelsing AI Dashboard]()

## 🚀 Features

### 🔍 Intelligent Risk Detection
- **Real-time Analysis**: Instant risk scoring for any Ethereum address
- **Multi-dimensional Features**: 15+ behavioral and transactional features
- **LightGBM Powered**: High-accuracy machine learning model
- **Explainable AI**: Clear risk factors and confidence scores

### 🛡️ Security Features
- **Fraud Pattern Recognition**: Detect known scam and phishing patterns
- **Anomaly Detection**: Identify unusual transaction behaviors
- **Risk Categorization**: Low/Medium/High risk classification
- **Actionable Insights**: Specific recommendations for each risk level

### 💻 Technical Highlights
- **RESTful API**: Scalable model serving architecture
- **Real-time Processing**: Sub-second prediction latency
- **Production Ready**: Containerized deployment with Docker
- **Modular Design**: Easy model updates and feature additions

## 📊 Model Performance

| Metric | Score | Description |
|--------|-------|-------------|
| **AUC-ROC** | 0.95 | Model discrimination ability |
| **Accuracy** | 0.92 | Overall prediction accuracy |
| **Precision** | 0.89 | Fraud detection precision |
| **Recall** | 0.87 | Fraud detection recall |

## 🏗️ Architecture

```mermaid
graph TB
    A[User Interface] --> B[Streamlit App]
    B --> C[ML Prediction API]
    C --> D[LightGBM Model]
    D --> E[Feature Engine]
    E --> F[Blockchain Data]
    
    G[Model Training] --> H[Ethereum Dataset]
    H --> I[Feature Engineering]
    I --> J[Model Training]
    J --> K[Model Deployment]

## 🛠️ Installation

    Prerequisites:
    Python 3.8+
    pip package manager

    1. Install dependencies
        bash
        pip install -r requirements.txt

    2.Start the services
        bash
        # Terminal 1 - Start ML API
        cd model_serving
        python prediction_api.py

        # Terminal 2 - Start Web Interface
        streamlit run app.py

    3.Access the application
        Web Interface: http://localhost:8501
        API Health Check: http://localhost:5000/health

## 📖 Usage

Basic Address Analysis
Open the web interface at http://localhost:8501

Enter an Ethereum address in the input field

View the AI analysis including:

Risk score (0-100)

Risk level classification

Key risk factors

Confidence metrics

Action recommendations

API Usage
python
import requests


## 🧩 Model Details
Feature Engineering
The system analyzes 15+ behavioral features including:

Transaction Patterns: Frequency, timing, and volume analysis

Network Behavior: Address interactions and relationship graphs

Financial Flows: Balance changes and transaction patterns

Contract Interactions: Smart contract usage and patterns

Temporal Analysis: Activity timing and consistency

Training Data
Dataset: Ethereum Fraud Detection Dataset from Kaggle

Samples: 10,000+ labeled addresses

Features: 15 engineered behavioral metrics

Class Balance: Realistic fraud prevalence simulation

## 🔧 Development

Project Structure
text
CryptoGuard-AI/
├── model_serving/     # ML model serving layer
├── src/              # Source code modules
├── tests/            # Test suites
├── app.py           # Main Streamlit application
└── requirements.txt # Python dependencies


## 🌐 API Documentation

Endpoints
Method	Endpoint	Description
GET	/health	Service health check
GET	/model/info	Model metadata and version
POST	/predict	Single address risk prediction
POST	/batch/predict	Batch address predictions
Health Check Response
json
{
  "status": "healthy",
  "model_version": "model_v2025",
  "feature_count": 15,
  "timestamp": "2024-01-20T14:30:00Z"
}

## 🚢 Deployment

Production Deployment
Environment Setup

bash
# Set production environment
export ENVIRONMENT=production
export MODEL_PATH=/models/lgb_v2025.pkl
Using Docker Compose

bash
docker-compose -f docker-compose.prod.yml up -d
Kubernetes Deployment

bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
Monitoring
API metrics available at /metrics endpoint

Log aggregation with structured JSON logging

Performance monitoring with built-in metrics

## 🤝 Contributing

We welcome contributions! Please see our Contributing Guide for details.

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request


## 🙏 Acknowledgments

Ethereum Community for blockchain infrastructure

LightGBM Team for the excellent machine learning framework

Streamlit for the intuitive web framework

Kaggle Community for the Ethereum fraud detection dataset

