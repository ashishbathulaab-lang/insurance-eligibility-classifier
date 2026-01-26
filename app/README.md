# Insurance Eligibility Prediction System

A machine learning-based REST API and web interface for predicting patient insurance eligibility using Logistic Regression with MinMax scaling.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## 🎯 Features

- **Web Interface**: User-friendly form to input patient data
- **REST API**: JSON endpoints for programmatic access
- **ML Algorithm**: Logistic Regression with MinMax scaling
- **Real-time Predictions**: Instant eligibility determination
- **Confidence Scores**: Probability estimates for predictions
- **Production Ready**: Containerized, scalable, documented

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 58.09% |
| Precision | 84.51% |
| Recall | 56.15% |
| F1-Score | 0.6747 |
| ROC-AUC | 0.6269 |

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Build Docker image
docker build -t insurance-predictor .

# Run container
docker run -p 5000:5000 insurance-predictor

# Open browser
open http://localhost:5000
```

### Option 2: Local Setup

```bash
# Clone repository
git clone https://github.com/yourusername/insurance-eligibility-predictor.git
cd insurance-eligibility-predictor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask application
python app/api.py

# Open browser
open http://localhost:5000
```

## 📝 API Documentation

### Prediction Endpoint

**POST** `/api/predict`

Request body:
```json
{
    "age": 45.5,
    "gender": "Male",
    "icd_frequency": 15,
    "cpt_frequency": 8,
    "month": 6,
    "disease": "Back Pain"
}
```

Response:
```json
{
    "eligible": true,
    "eligibility_status": "ELIGIBLE",
    "confidence_eligible": 0.5581,
    "confidence_not_eligible": 0.4419,
    "risk_score": 0.4419,
    "disease": "Back Pain",
    "timestamp": "2026-01-26T21:50:00.000000",
    "input_data": {
        "age": 45.5,
        "gender": "Male",
        "icd_frequency": 15,
        "cpt_frequency": 8,
        "month": 6
    }
}
```

### Health Check

**GET** `/api/health`

```bash
curl http://localhost:5000/api/health
```

### Model Information

**GET** `/api/info`

Returns model specifications, features, and metrics.

## 🔧 Input Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| age | float | 1-120 | Patient age in years |
| gender | string | Male/Female | Patient gender |
| icd_frequency | integer | 1-683 | Frequency of ICD code |
| cpt_frequency | integer | 1-1815 | Frequency of CPT code |
| month | integer | 1-6 | Month of approval (1=Jan, 6=Jun) |
| disease | string | Any | Optional: disease/condition name |

## 📚 Algorithm Details

### Model Type
**Logistic Regression** (Binary Classification)

### Scaling Method
**MinMax Normalization** - All features scaled to [0, 1] range

$$X_{scaled} = \frac{X - X_{min}}{X_{max} - X_{min}}$$

### Feature Importance (Coefficients)

| Feature | Coefficient | Effect |
|---------|-------------|--------|
| Gender (Male=1) | +0.8108 | Positive |
| CPT Frequency | +0.6610 | Positive |
| Age (Years) | -0.5054 | Negative |
| ICD Frequency | -0.3128 | Negative |
| Month of Approval | -0.0687 | Negative |

### Decision Rule

```
If P(Eligible | Features) > 0.5 → ELIGIBLE
Else → NOT ELIGIBLE

P(Eligible) = 1 / (1 + e^(-z))
where z = -0.3114 + Σ(coefficient × scaled_feature)
```

## 🗂️ Project Structure

```
insurance-eligibility-predictor/
├── app/
│   ├── api.py                  # Flask API
│   ├── insurance_predictor.py   # Model prediction logic
│   ├── templates/
│   │   └── index.html          # Web interface
│   └── static/
│       └── (CSS/JS if separate)
├── models/
│   ├── insurance_model.pkl      # Trained model
│   └── minmax_scaler.pkl        # MinMax scaler
├── notebooks/
│   └── Insurance_Eligibility_Classification.ipynb
├── Dockerfile
├── requirements.txt
├── README.md
└── setup.py
```

## 🔄 Training the Model

To retrain the model with new data:

1. Prepare your dataset with columns:
   - Age, Gender, ICD, CPT, ApprovedDate, Insurance

2. Run the Jupyter notebook:
   ```bash
   jupyter notebook Insurance_Eligibility_Classification.ipynb
   ```

3. Execute all cells to train and save the model

4. Models are saved to `models/` directory

## 💻 Example Usage

### Using Python

```python
from app.insurance_predictor import predict_insurance_eligibility

# Make prediction
result = predict_insurance_eligibility(
    age=45.5,
    gender='Male',
    icd_frequency=15,
    cpt_frequency=8,
    month=6
)

print(f"Status: {result['eligibility_status']}")
print(f"Confidence: {result['confidence_eligible']:.2%}")
```

### Using cURL

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45.5,
    "gender": "Male",
    "icd_frequency": 15,
    "cpt_frequency": 8,
    "month": 6,
    "disease": "Back Pain"
  }'
```

### Using Python Requests

```python
import requests

payload = {
    "age": 45.5,
    "gender": "Male",
    "icd_frequency": 15,
    "cpt_frequency": 8,
    "month": 6,
    "disease": "Back Pain"
}

response = requests.post(
    'http://localhost:5000/api/predict',
    json=payload
)

result = response.json()
print(result)
```

## 📦 Dependencies

- Python 3.8+
- Flask 2.0+
- scikit-learn 0.24+
- pandas 1.2+
- numpy 1.19+
- Flask-CORS

See `requirements.txt` for complete list.

## 🐳 Docker Setup

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY models/ models/

EXPOSE 5000

CMD ["python", "api.py"]
```

### Build and Run

```bash
docker build -t insurance-predictor .
docker run -p 5000:5000 insurance-predictor
```

## ⚙️ Configuration

### Environment Variables

```bash
FLASK_ENV=production
FLASK_DEBUG=False
MODEL_PATH=models/insurance_model.pkl
SCALER_PATH=models/minmax_scaler.pkl
```

### Flask Configuration

Edit `api.py` to customize:
- Port (default: 5000)
- Debug mode
- CORS settings
- Request timeouts

## 🔒 Security Considerations

1. **Input Validation**: All inputs validated before prediction
2. **Error Handling**: Graceful error responses
3. **CORS**: Configured for specific origins
4. **No Data Storage**: Predictions not stored by default
5. **HTTPS**: Use in production with SSL/TLS

## 📈 Monitoring & Logging

Add monitoring to production:

```python
# Example: Log all predictions
import logging

logger = logging.getLogger(__name__)

@app.route('/api/predict', methods=['POST'])
def predict():
    # ... prediction logic ...
    logger.info(f"Prediction: {result['eligibility_status']}")
    return jsonify(result)
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test coverage
pytest --cov=app tests/
```

## 📊 Data Overview

- **Original Records**: 20,776
- **Cleaned Records**: 20,270 (2.44% removed)
- **Training Set**: 16,213 (80%)
- **Test Set**: 4,054 (20%)

### Target Distribution
- Eligible: 77.4%
- Not Eligible: 22.6%

## ⚠️ Limitations

1. **Moderate Accuracy**: 58% - Use as support tool, not sole decision
2. **Class Imbalance**: Model biased toward "eligible" class
3. **Limited Context**: No clinical severity or cost data
4. **Temporal Data**: Only considers approval month
5. **Dataset Specific**: Trained on 2024 GMU radiology data

## 📈 Improvement Roadmap

- [ ] Add more features (clinical severity, cost estimates)
- [ ] Implement ensemble methods (Random Forest, XGBoost)
- [ ] Add patient history tracking
- [ ] Implement A/B testing framework
- [ ] Add model monitoring/drift detection
- [ ] Create mobile app
- [ ] Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 📧 Contact & Support

- **Email**: support@insurance-predictor.dev
- **Issues**: GitHub Issues
- **Documentation**: See docs/ folder

## 🙏 Acknowledgments

- GMU Radiology Department for dataset
- Scikit-learn for ML algorithms
- Flask community for excellent framework

## 📚 References

- [Logistic Regression](https://en.wikipedia.org/wiki/Logistic_regression)
- [MinMax Scaling](https://scikit-learn.org/stable/modules/preprocessing.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [REST API Best Practices](https://restfulapi.net/)

---

**Version**: 1.0.0  
**Last Updated**: January 26, 2026  
**Status**: ✅ Production Ready

**⭐ If you find this helpful, please star the repository!**
