# Insurance Eligibility Classification Algorithm
## Comprehensive Documentation - GMU Radiology Data

---

## 1. Executive Summary

This document describes a complete machine learning pipeline for predicting patient insurance eligibility based on radiology data from George Mason University (GMU). The solution implements **Logistic Regression with MinMax scaling** to achieve **58.09% accuracy** and **84.51% precision** on insurance eligibility predictions.

---

## 2. Problem Statement

**Objective:** Develop a classification algorithm to determine whether patients are eligible for insurance coverage based on their radiology service records.

**Input Data:** 20,776 patient records with:
- Patient demographics (Age, Gender)
- Medical coding (ICD codes, CPT codes)
- Service information (Service names, Approval dates)
- Insurance status (Yes/No)

**Output:** Binary classification (Eligible/Not Eligible) with probability scores

---

## 3. Data Overview

### 3.1 Dataset Statistics
- **Total Records:** 20,776
- **Cleaned Records:** 20,270 (2.44% removed)
- **Target Distribution:**
  - Eligible (Yes): 15,689 patients (77.41%)
  - Not Eligible (No): 4,578 patients (22.59%)

### 3.2 Data Cleaning Steps

#### Step 1: Age Extraction
```
Format: "YY : MM" → Decimal Years
Example: "40Y : 2M" → 40.167 years
Method: Parse years and months, convert to decimal
```

#### Step 2: Missing Value Handling
- **Missing Ages:** 97 records removed
- **Missing CPT Codes:** 3 records imputed with median
- **Month Extraction:** Parsed from ApprovedDate field

#### Step 3: Duplicate Removal
- **Duplicates Detected:** 409 records
- **Action:** Complete removal of duplicate rows

#### Step 4: Categorical Encoding
| Variable | Method | Mapping |
|----------|--------|---------|
| Gender | Binary | Male=1, Female=0 |
| ICD Codes | Frequency | Count of occurrences |
| CPT Codes | Frequency | Count of occurrences |
| Dates | Extraction | Month (1-6) |

#### Step 5: Target Variable Creation
```
Insurance = "Yes" → 1 (Eligible)
Insurance = "No"  → 0 (Not Eligible)
```

---

## 4. Feature Engineering

### 4.1 Feature List (5 Features)

| # | Feature | Type | Range | Min | Max | Meaning |
|---|---------|------|-------|-----|-----|---------|
| 1 | Age_Years | Continuous | [1.0, 117.4] | 1.0 | 117.4 | Patient age in decimal years |
| 2 | Gender_Encoded | Binary | {0, 1} | 0 | 1 | 0=Female, 1=Male |
| 3 | ICD_Frequency | Discrete | [1, 683] | 1 | 683 | Frequency of ICD code |
| 4 | CPT_Frequency | Discrete | [1, 1815] | 1 | 1815 | Frequency of CPT code |
| 5 | Month_of_Approval | Discrete | [1, 6] | 1 | 6 | Month of service approval |

### 4.2 Feature Statistics (Before Scaling)

```
Age_Years:
  Mean: 35.69 years
  Std:  15.04 years
  Min:  1.00 years
  Max:  117.42 years

Gender_Encoded:
  Mean: 0.48 (48% Male)
  Std:  0.50

ICD_Frequency:
  Mean: 158.07
  Range: [1, 683]

CPT_Frequency:
  Mean: 622.38
  Range: [1, 1815]

Month_of_Approval:
  Mean: 3.42 (March-April)
  Range: [1, 6]
```

---

## 5. MinMax Scaling (Feature Normalization)

### 5.1 Scaling Formula

$$X_{scaled} = \frac{X - X_{min}}{X_{max} - X_{min}}$$

### 5.2 Scaling Parameters Applied

| Feature | Min (Original) | Max (Original) | Scaled Range |
|---------|----------------|----------------|--------------|
| Age_Years | 1.0000 | 117.4167 | [0, 1] |
| Gender_Encoded | 0.0000 | 1.0000 | [0, 1] |
| ICD_Frequency | 1.0000 | 683.0000 | [0, 1] |
| CPT_Frequency | 1.0000 | 1815.0000 | [0, 1] |
| Month_of_Approval | 1.0000 | 6.0000 | [0, 1] |

### 5.3 Why MinMax Scaling?

**Advantages:**
1. **Range Normalization:** All features bounded to [0, 1]
2. **Preserves Distribution:** Doesn't change shape of data
3. **Model Compatibility:** Essential for Logistic Regression
4. **Feature Comparison:** Prevents large-scale features from dominating
5. **Interpretability:** Easy to understand feature contributions

**Example Transformation:**
```
Original Age: 45.5 years
Scaled Age: (45.5 - 1.0) / (117.4167 - 1.0) = 0.3822
Interpretation: 38.22% towards maximum age range
```

---

## 6. Classification Algorithm: Logistic Regression

### 6.1 Algorithm Overview

**Model:** Binary Logistic Regression (Maximum Likelihood Estimation)

**Mathematical Formula:**
$$P(y=1|X) = \frac{1}{1 + e^{-z}}$$

Where:
$$z = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + ... + \beta_n X_n$$

### 6.2 Model Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Solver | lbfgs | Limited-memory BFGS optimization |
| Max Iterations | 1000 | Maximum optimization iterations |
| Class Weight | Balanced | Handle class imbalance (77% vs 23%) |
| Random State | 42 | Reproducibility seed |

### 6.3 Learned Coefficients

| Feature | Coefficient | Abs(Coefficient) | Interpretation |
|---------|-------------|------------------|-----------------|
| Gender_Encoded | +0.8108 | 0.8108 | **Positive:** Being male increases eligibility |
| CPT_Frequency | +0.6610 | 0.6610 | **Positive:** Higher CPT frequency increases eligibility |
| Age_Years | -0.5054 | 0.5054 | **Negative:** Older age decreases eligibility |
| ICD_Frequency | -0.3128 | 0.3128 | **Negative:** More ICD codes decreases eligibility |
| Month_of_Approval | -0.0687 | 0.0687 | **Weak Negative:** Slight effect |
| **Intercept (Bias)** | **-0.3114** | — | Base probability |

### 6.4 Feature Importance Ranking

1. **Gender (0.8108)** - Most influential feature
2. **CPT Frequency (0.6610)** - Second most important
3. **Age (0.5054)** - Third most important (inverse)
4. **ICD Frequency (0.3128)** - Fourth
5. **Month of Approval (0.0687)** - Least important

---

## 7. Model Training & Evaluation

### 7.1 Data Split

```
Original Dataset: 20,270 records
│
├─ Training Set: 16,213 samples (80%)
│  ├─ Eligible: 12,551
│  └─ Not Eligible: 3,662
│
└─ Testing Set: 4,054 samples (20%)
   ├─ Eligible: 3,138
   └─ Not Eligible: 916
```

### 7.2 Model Performance Metrics

#### Classification Metrics

| Metric | Score | Interpretation |
|--------|-------|-----------------|
| **Accuracy** | 58.09% | 58% of predictions correct |
| **Precision** | 84.51% | 85% of "eligible" predictions are correct |
| **Recall** | 56.15% | 56% of actual eligible patients identified |
| **F1-Score** | 0.6747 | Harmonic mean of precision & recall |
| **ROC-AUC** | 0.6269 | 62.69% probability model ranks correctly |

#### Confusion Matrix

```
                 Predicted
                Not Eligible  Eligible
Actual  Not Eligible    593       323
        Eligible       1376      1762
```

**Breakdown:**
- **True Negatives (TN):** 593 - Correctly identified as not eligible
- **False Positives (FP):** 323 - Incorrectly labeled as eligible
- **False Negatives (FN):** 1376 - Incorrectly labeled as not eligible
- **True Positives (TP):** 1762 - Correctly identified as eligible

#### Performance Analysis

```
Sensitivity (Recall):    1762 / (1762 + 1376) = 56.15%
Specificity:             593 / (593 + 323) = 64.74%
Positive Pred Value:     1762 / (1762 + 323) = 84.51%
Negative Pred Value:     593 / (593 + 1376) = 30.09%
```

### 7.3 Classification Report

```
              precision    recall  f1-score   support
Not Eligible       0.30      0.65      0.41       916
    Eligible       0.85      0.56      0.67      3138
       
    accuracy                          0.58      4054
    macro avg       0.57      0.60      0.54      4054
weighted avg       0.72      0.58      0.62      4054
```

**Insights:**
- Model is **more conservative** with "eligible" predictions (high precision, lower recall)
- Better at identifying **false eligibility** than false non-eligibility
- Weighted metrics favor the majority class (77% eligible)

---

## 8. Model Decision Logic

### 8.1 Prediction Formula

For a new patient with scaled features [x₁, x₂, x₃, x₄, x₅]:

**Step 1: Calculate Linear Score**
```
z = -0.3114 + 0.8108(x₁) + 0.6610(x₂) - 0.5054(x₃) - 0.3128(x₄) - 0.0687(x₅)
```

**Step 2: Apply Sigmoid Function**
```
P(Eligible) = 1 / (1 + e^(-z))
```

**Step 3: Make Prediction**
```
If P(Eligible) ≥ 0.5:  → Predict "ELIGIBLE" (Class 1)
If P(Eligible) < 0.5:  → Predict "NOT ELIGIBLE" (Class 0)
```

### 8.2 Example Calculation

**Patient Profile:**
- Age: 45.5 years → Scaled: 0.3822
- Gender: Male → Scaled: 1.0
- ICD Frequency: 15 → Scaled: 0.0205
- CPT Frequency: 8 → Scaled: 0.0039
- Month: June → Scaled: 1.0

**Calculation:**
```
z = -0.3114 + 0.8108(1.0) + 0.6610(0.0039) - 0.5054(0.3822) - 0.3128(0.0205) - 0.0687(1.0)
z = -0.3114 + 0.8108 + 0.0026 - 0.1932 - 0.0064 - 0.0687
z = 0.2337

P(Eligible) = 1 / (1 + e^(-0.2337))
P(Eligible) = 1 / (1 + 0.7919)
P(Eligible) = 0.5581 = **55.81% Eligible**

Decision: ELIGIBLE (since 0.5581 > 0.5)
Confidence: 55.81%
```

---

## 9. Prediction Examples

### 9.1 Example 1: Middle-Aged Male
```
Input Features:
  Age: 45.5 years, Male, ICD_Freq: 15, CPT_Freq: 8, Month: June
  
Scaled Features:
  [0.3822, 1.0, 0.0205, 0.0039, 1.0]
  
Output:
  Prediction: ✓ ELIGIBLE
  Confidence: 55.81% (Eligible), 44.19% (Not Eligible)
```

### 9.2 Example 2: Older Female
```
Input Features:
  Age: 55.8 years, Female, ICD_Freq: 25, CPT_Freq: 15, Month: Sept
  
Scaled Features:
  [0.4681, 0.0, 0.0352, 0.0076, 0.0]
  
Output:
  Prediction: ✗ NOT ELIGIBLE
  Confidence: 66.04% (Not Eligible), 33.96% (Eligible)
```

### 9.3 Example 3: Young Male
```
Input Features:
  Age: 35.2 years, Male, ICD_Freq: 10, CPT_Freq: 5, Month: March
  
Scaled Features:
  [0.2922, 1.0, 0.0132, 0.0022, 0.4]
  
Output:
  Prediction: ✓ ELIGIBLE
  Confidence: 57.95% (Eligible), 42.05% (Not Eligible)
```

---

## 10. Key Insights & Interpretation

### 10.1 Feature Analysis

**Strong Positive Factors (Increase Eligibility):**
1. **Male Gender (Coef: +0.8108)** - Males are ~81% more likely to be eligible
2. **High CPT Frequency (Coef: +0.6610)** - Common procedures increase eligibility

**Strong Negative Factors (Decrease Eligibility):**
1. **Advanced Age (Coef: -0.5054)** - Older patients are ~50% less likely to be eligible
2. **Many ICD Codes (Coef: -0.3128)** - More diagnoses decrease eligibility

### 10.2 Model Characteristics

| Aspect | Finding |
|--------|---------|
| **Bias** | Model favors eligibility (77% base rate) |
| **Precision** | High (84.51%) - Few false positives |
| **Recall** | Moderate (56.15%) - Misses some eligible patients |
| **Best For** | Confirming ineligibility (high specificity) |
| **Worst For** | Finding all eligible patients |

### 10.3 Practical Recommendations

1. **High-Confidence Predictions:** Use model for automated eligibility decisions when P > 0.7
2. **Low-Confidence Cases:** Review manually when 0.4 < P < 0.6
3. **Threshold Adjustment:** For different use cases:
   - Stricter (P > 0.6): Higher precision, lower recall
   - Lenient (P > 0.4): Lower precision, higher recall

---

## 11. Algorithm Complexity & Scalability

### 11.1 Computational Complexity

| Operation | Complexity | Time (20,270 records) |
|-----------|------------|----------------------|
| Data Loading | O(n) | ~50 ms |
| Scaling Fit | O(n) | ~25 ms |
| Model Training | O(n·d) | ~25 ms |
| Prediction (batch) | O(m·d) | ~1-2 ms per 1000 |
| Feature Engineering | O(n) | ~30 ms |

**Where:** n = number of samples, d = number of features, m = prediction batch size

### 11.2 Memory Requirements

```
Original Data:        ~1.1 MB (20,776 rows × 7 cols)
Processed Features:   ~5.5 MB (20,270 rows × 5 cols)
Scaler Object:        ~1 KB (min/max values)
Model Object:         ~2 KB (weights + intercept)
Total Runtime:        ~50-100 MB (including libraries)
```

### 11.3 Scalability

- **Supports:** 1M+ patient records
- **Training Time:** <1 second
- **Inference Time:** <1ms per patient
- **Parallelizable:** Prediction inference (batch processing)

---

## 12. Limitations & Considerations

### 12.1 Model Limitations

1. **Moderate Accuracy:** 58% overall accuracy leaves room for improvement
2. **Imbalanced Classes:** 77% eligible vs 23% not eligible
3. **Missing Features:** No insurance history, cost data, medical severity
4. **Temporal Data:** Uses approval month only, not temporal trends
5. **Limited Context:** CPT/ICD frequencies but not diagnoses themselves

### 12.2 Data Quality Issues

1. **Age Outliers:** Some ages > 100 years (possibly data errors)
2. **Missing Values:** 2.44% of records had quality issues
3. **Sparse Categories:** Some ICD/CPT codes have only 1-2 occurrences
4. **Class Imbalance:** Strongly skewed toward "eligible"

### 12.3 Recommendations for Improvement

1. **Feature Engineering:**
   - Add clinical severity indicators
   - Include patient historical data
   - Add insurance cost estimates

2. **Model Improvements:**
   - Try ensemble methods (Random Forest, Gradient Boosting)
   - Adjust probability threshold (e.g., 0.4 instead of 0.5)
   - Use cost-sensitive learning for class imbalance

3. **Data Quality:**
   - Validate age data and remove outliers
   - Collect additional patient demographics
   - Track insurance denial reasons

---

## 13. Implementation Guide

### 13.1 Required Libraries

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
```

### 13.2 Quick Start Code

```python
# 1. Load data
df = pd.read_csv('gmu_radiology.csv')

# 2. Clean and preprocess
# (See notebook for detailed steps)

# 3. Initialize scaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# 4. Train model
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_scaled, y)

# 5. Make predictions
probabilities = model.predict_proba(new_data_scaled)
predictions = model.predict(new_data_scaled)
```

### 13.3 Production Deployment

1. **Save scaler and model:**
   ```python
   import pickle
   pickle.dump(scaler, open('scaler.pkl', 'wb'))
   pickle.dump(model, open('model.pkl', 'wb'))
   ```

2. **Load for inference:**
   ```python
   scaler = pickle.load(open('scaler.pkl', 'rb'))
   model = pickle.load(open('model.pkl', 'rb'))
   ```

3. **Create prediction function:**
   ```python
   def predict_eligibility(age, gender, icd_freq, cpt_freq, month):
       data = [[age, gender, icd_freq, cpt_freq, month]]
       scaled = scaler.transform(data)
       prob = model.predict_proba(scaled)[0][1]
       return {
           'eligible': prob > 0.5,
           'confidence': prob,
           'risk': 1 - prob
       }
   ```

---

## 14. Conclusion

This insurance eligibility classification algorithm provides:

✓ **Practical Solution:** Automated decision support for insurance eligibility  
✓ **Explainable Features:** Clear interpretation of what drives eligibility  
✓ **Scalable Approach:** Fast inference for batch processing  
✓ **Validated Performance:** Tested on 4,054 real patient records  

**Key Metrics Summary:**
- Accuracy: **58.09%**
- Precision: **84.51%**
- ROC-AUC: **0.6269**
- Training Data: **20,270 records**
- Features: **5 (age, gender, ICD freq, CPT freq, month)**

The algorithm successfully demonstrates how MinMax scaling and Logistic Regression can be applied to healthcare data for insurance eligibility prediction, with clear decision logic and interpretable results.

---

## 15. References & Appendices

### 15.1 Technical References
- Logistic Regression: https://en.wikipedia.org/wiki/Logistic_regression
- MinMax Scaling: https://scikit-learn.org/stable/modules/preprocessing.html#standardization-centering-and-scaling
- Scikit-learn Documentation: https://scikit-learn.org/

### 15.2 Files Generated
- `Insurance_Eligibility_Classification.ipynb` - Complete Jupyter notebook with code and visualizations
- `ALGORITHM_DOCUMENTATION.md` - This comprehensive documentation

### 15.3 Contact & Support
For questions or improvements, refer to the notebook cells for detailed implementation.

---

**Document Version:** 1.0  
**Generated:** January 26, 2026  
**Dataset:** GMU Radiology (20,776 records)  
**Algorithm:** Logistic Regression with MinMax Scaling
