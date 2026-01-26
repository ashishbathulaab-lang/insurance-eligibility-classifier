# Insurance Eligibility Classification - Quick Reference Guide

## 📊 Dataset Summary
- **Original Records:** 20,776
- **Cleaned Records:** 20,270
- **Training Data:** 16,213 (80%)
- **Testing Data:** 4,054 (20%)
- **Eligible Patients:** 77.4%
- **Not Eligible Patients:** 22.6%

---

## 🎯 Model Performance

### Key Metrics
| Metric | Value | Grade |
|--------|-------|-------|
| Accuracy | 58.09% | C+ |
| Precision | 84.51% | A |
| Recall | 56.15% | C |
| F1-Score | 0.6747 | C+ |
| ROC-AUC | 0.6269 | C |

### Confusion Matrix
```
                    Predicted
                  Not Elg  Eligible
Actual Not Elg      593      323
       Eligible    1376     1762
```

---

## 🔬 Algorithm Details

**Type:** Logistic Regression (Binary Classification)  
**Scaling:** MinMax (0-1 range normalization)  
**Training Method:** LBFGS with balanced class weights  
**Decision Threshold:** 0.5 probability

---

## 📋 Features Used (5 Total)

| # | Feature | Type | Range | Importance | Effect |
|---|---------|------|-------|------------|--------|
| 1 | Age (years) | Continuous | 1-117 | ⭐⭐⭐ | Negative |
| 2 | Gender | Binary | 0-1 | ⭐⭐⭐⭐ | Positive |
| 3 | ICD Frequency | Discrete | 1-683 | ⭐⭐ | Negative |
| 4 | CPT Frequency | Discrete | 1-1815 | ⭐⭐⭐ | Positive |
| 5 | Approval Month | Discrete | 1-6 | ⭐ | Negative |

---

## 📈 Feature Importance Ranking

### Positive Factors (Increase Eligibility)
1. **Male Gender** (+0.8108) - Strongest positive predictor
2. **High CPT Frequency** (+0.6610) - More common procedures = more eligible

### Negative Factors (Decrease Eligibility)
1. **Advanced Age** (-0.5054) - Older patients less likely to be eligible
2. **Many ICD Codes** (-0.3128) - More diagnoses = less eligible
3. **Later Approval Months** (-0.0687) - Weak effect

---

## 🧮 MinMax Scaling Formula

Applied to all 5 features:

$$X_{scaled} = \frac{X - X_{min}}{X_{max} - X_{min}}$$

**Result:** All features normalized to [0, 1] range

### Scaling Parameters

| Feature | Min | Max |
|---------|-----|-----|
| Age | 1.00 | 117.42 |
| Gender | 0.00 | 1.00 |
| ICD Freq | 1.00 | 683.00 |
| CPT Freq | 1.00 | 1815.00 |
| Month | 1.00 | 6.00 |

---

## 🔮 Making Predictions

### The Formula
```
z = -0.3114 + 0.8108(gender) + 0.6610(cpt_freq) 
    - 0.5054(age) - 0.3128(icd_freq) - 0.0687(month)

P(Eligible) = 1 / (1 + e^(-z))

Decision: If P > 0.5 → ELIGIBLE, else NOT ELIGIBLE
```

### Example: 45.5-Year-Old Male

**Original Values:**
- Age: 45.5 years
- Gender: Male
- ICD Freq: 15
- CPT Freq: 8
- Month: 6

**After Scaling:**
- Age: 0.382
- Gender: 1.0
- ICD Freq: 0.021
- CPT Freq: 0.004
- Month: 1.0

**Prediction:**
- P(Eligible) = **55.81%** ✓ **ELIGIBLE**

---

## 💡 How to Use

### Step 1: Prepare Patient Data
```
age_years = 45.5
gender = "Male" → 1
icd_frequency = 15
cpt_frequency = 8
month = 6
```

### Step 2: Scale Features
```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaled_data = scaler.transform([[45.5, 1, 15, 8, 6]])
```

### Step 3: Get Prediction
```python
probability = model.predict_proba(scaled_data)[0][1]
prediction = "ELIGIBLE" if probability > 0.5 else "NOT ELIGIBLE"
confidence = probability * 100
```

### Step 4: Interpret Results
- **P > 0.7:** High confidence eligible
- **P > 0.5:** Moderately eligible
- **P < 0.5:** Not eligible
- **0.4 < P < 0.6:** Review manually

---

## ⚠️ Important Notes

### When to Trust the Model
✓ Large patient batches (100+)  
✓ Similar demographics to training data  
✓ Complete, clean data  

### When to be Careful
⚠️ Single patient predictions  
⚠️ Extreme ages (< 5 or > 100 years)  
⚠️ Missing/invalid features  
⚠️ Predictions near 0.5 threshold  

### Model Limitations
- Moderate accuracy (58%) - use as support tool, not sole decision
- Imbalanced classes (77% vs 23%) - biased toward "eligible"
- Missing clinical context - no severity/risk data
- Historical data ignored - doesn't account for past denials

---

## 🚀 Production Checklist

- [ ] Validate on new patient data
- [ ] Monitor prediction accuracy quarterly
- [ ] Log all predictions for audit trail
- [ ] Set up manual review process
- [ ] Train staff on interpreting results
- [ ] Backup model and scaler files
- [ ] Document any threshold adjustments
- [ ] Implement error handling for invalid inputs

---

## 📊 Performance by Patient Type

### High Probability of Eligibility
- Younger males (20-40 years)
- With 5-15 common procedures
- Single diagnosis (ICD code)

### Low Probability of Eligibility
- Older females (60+ years)
- With 1-2 rare procedures
- Multiple diagnoses (many ICD codes)

---

## 🔧 Technical Specs

**Language:** Python 3.14+  
**Libraries:** scikit-learn, pandas, numpy  
**Model Size:** ~2 KB  
**Inference Time:** <1 ms per prediction  
**Batch Prediction:** 1000+ patients/second  

---

## 📞 Support

For detailed implementation:
- See: `Insurance_Eligibility_Classification.ipynb`
- Full docs: `ALGORITHM_DOCUMENTATION.md`
- Python code available in notebook cells

---

**Last Updated:** January 26, 2026  
**Model Version:** 1.0  
**Status:** Ready for Production Testing
