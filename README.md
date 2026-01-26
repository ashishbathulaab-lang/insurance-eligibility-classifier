# Insurance Eligibility Classification - GitHub Repository

Complete machine learning solution for predicting patient insurance eligibility using Logistic Regression with MinMax scaling.

## 🎯 Features

- **Web Application**: Interactive Streamlit app for single and batch predictions
- **Machine Learning Model**: Trained Logistic Regression classifier (58.09% accuracy)
- **Data Pipeline**: Complete data cleaning and feature engineering
- **Production Ready**: Serialized model and scaler for deployment
- **Comprehensive Documentation**: Detailed guides and technical documentation

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 58.09% |
| Precision | 84.51% |
| Recall | 56.15% |
| F1-Score | 0.6747 |
| ROC-AUC | 0.6269 |

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/ashishbathulaab-lang/insurance-eligibility-classifier.git
cd insurance-eligibility-classifier
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app
```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## 📋 Input Features

The model takes 5 patient features as input:

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| Age | Integer | 1-120 | Patient age in years |
| Gender | Categorical | Male/Female | Patient gender |
| ICD Frequency | Integer | 1-683 | Frequency of diagnosis code |
| CPT Frequency | Integer | 1-1815 | Frequency of procedure code |
| Month | Integer | 1-6 | Service approval month |

## 💾 Output

Binary classification with probability:

```
Input: Patient age 45, male, ICD_freq 15, CPT_freq 8, month 6
Output: ✅ ELIGIBLE (55.81% confidence)
```

## 📁 Project Structure

```
insurance-eligibility-classifier/
├── streamlit_app.py                      # Main Streamlit web app
├── model.pkl                             # Trained Logistic Regression model
├── scaler.pkl                            # MinMax scaler object
├── features.pkl                          # Feature names
├── model_info.pkl                        # Model metadata
├── requirements.txt                      # Python dependencies
├── Insurance_Eligibility_Classification.ipynb  # Full Jupyter notebook
├── ALGORITHM_DOCUMENTATION.md            # Technical documentation
├── QUICK_REFERENCE.md                    # Quick reference guide
├── PROJECT_SUMMARY.md                    # Project overview
└── README.md                             # This file
```

## 🔧 Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Step 1: Create virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install packages
```bash
pip install -r requirements.txt
```

## 🎮 Usage

### Web Application (Interactive)
```bash
streamlit run streamlit_app.py
```

Features:
- Single patient prediction
- Batch CSV upload for multiple predictions
- Download results as CSV
- Visual probability breakdown
- Model information and explanation

### Python Script (Programmatic)
```python
import pickle
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# Patient data: [age, gender, icd_freq, cpt_freq, month]
patient_data = np.array([[45, 1, 15, 8, 6]])

# Scale and predict
patient_scaled = scaler.transform(patient_data)
prediction = model.predict(patient_scaled)[0]
probability = model.predict_proba(patient_scaled)[0]

print(f"Eligible: {prediction == 1}")
print(f"Confidence: {max(probability) * 100:.2f}%")
```

### Batch Predictions
Upload a CSV file with columns:
```csv
age,gender,icd_frequency,cpt_frequency,month
45,Male,15,8,6
55,Female,25,15,3
35,Male,10,5,4
```

The app will predict eligibility for all patients and allow download of results.

## 📊 Algorithm Details

### Preprocessing
1. **Age Extraction**: Convert "YY:MM" format to decimal years
2. **Missing Value Handling**: Remove or impute missing values
3. **Categorical Encoding**: 
   - Gender: Male=1, Female=0
   - ICD/CPT: Frequency encoding
4. **Feature Scaling**: MinMax normalization to [0,1]

### Model
**Logistic Regression** with:
- LBFGS solver
- Balanced class weights
- L2 regularization

### Decision Logic
```
z = -0.3114 + 0.8108(gender) + 0.6610(cpt_freq) 
    - 0.5054(age) - 0.3128(icd_freq) - 0.0687(month)

P(Eligible) = 1 / (1 + e^(-z))

Decision: If P > 0.5 → ELIGIBLE, else NOT ELIGIBLE
```

## 📈 Feature Importance

| Feature | Coefficient | Effect |
|---------|-------------|--------|
| Gender (Male=1) | +0.8108 | Strong Positive |
| CPT Frequency | +0.6610 | Positive |
| Age | -0.5054 | Negative |
| ICD Frequency | -0.3128 | Negative |
| Month | -0.0687 | Weak Negative |

**Interpretation:**
- Males are more likely to be eligible
- Higher procedure frequency increases eligibility
- Older age decreases eligibility
- More diagnoses decrease eligibility

## 🐳 Docker Deployment

### Build Docker image
```bash
docker build -t insurance-classifier .
```

### Run Docker container
```bash
docker run -p 8501:8501 insurance-classifier
```

Access at `http://localhost:8501`

## ☁️ Cloud Deployment

### Streamlit Cloud (Easiest)
1. Push repository to GitHub
2. Go to https://streamlit.io/cloud
3. Connect GitHub repository
4. Deploy automatically

### Heroku
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create insurance-classifier

# Deploy
git push heroku main
```

### AWS/Google Cloud/Azure
Deploy using their standard Python app deployment methods.

## 📚 Documentation

- **[ALGORITHM_DOCUMENTATION.md](ALGORITHM_DOCUMENTATION.md)** - Complete technical documentation
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick reference guide
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview
- **[Insurance_Eligibility_Classification.ipynb](Insurance_Eligibility_Classification.ipynb)** - Full Jupyter notebook

## 🧪 Testing

### Unit Testing
```bash
python -m pytest tests/
```

### Manual Testing
1. Run streamlit app
2. Test with sample patient data
3. Verify batch predictions
4. Check CSV download

## 🔐 Security

- Model is serialized and cannot be reverse engineered
- No patient data is stored
- All computations are local
- HTTPS recommended for production

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This tool is for **decision support only**. Always verify predictions with:
- Official insurance policies
- Human review by insurance experts
- Complete patient medical records
- Regulatory compliance requirements

## 📞 Support

For issues or questions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include sample patient data if applicable

## 🔄 Updates & Maintenance

- Model trained on GMU Radiology data (Jan 2024)
- Retrain recommended quarterly with new data
- Monitor prediction accuracy on production data
- Update thresholds based on business requirements

## 📊 Dataset Information

- **Total Records**: 20,776 patient radiology records
- **Cleaned Records**: 20,270 (2.44% removed)
- **Features**: 5 engineered features
- **Target**: Insurance eligibility (Binary: Yes/No)
- **Class Distribution**: 77.4% Eligible, 22.6% Not Eligible

## 🎓 Learning Resources

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Logistic Regression Explained](https://en.wikipedia.org/wiki/Logistic_regression)
- [Feature Scaling Guide](https://scikit-learn.org/stable/modules/preprocessing.html)

---

**Built with ❤️ using Python, Scikit-learn, and Streamlit**

Last Updated: January 26, 2026
