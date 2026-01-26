# API Helper Module for Production Integration

import pickle
import numpy as np
from typing import Dict, Tuple

class InsuranceEligibilityPredictor:
    """
    Production-ready insurance eligibility predictor.
    
    Usage:
        predictor = InsuranceEligibilityPredictor()
        result = predictor.predict(age=45, gender="Male", icd_freq=15, cpt_freq=8, month=6)
        print(result)  # {'eligible': True, 'confidence': 0.558, 'probability': 0.558}
    """
    
    def __init__(self, model_path='model.pkl', scaler_path='scaler.pkl', features_path='features.pkl'):
        """Initialize predictor with model artifacts."""
        self.model = pickle.load(open(model_path, 'rb'))
        self.scaler = pickle.load(open(scaler_path, 'rb'))
        self.features = pickle.load(open(features_path, 'rb'))
    
    def predict(self, age: int, gender: str, icd_freq: int, cpt_freq: int, month: int) -> Dict:
        """
        Predict insurance eligibility for a single patient.
        
        Args:
            age: Patient age (1-120)
            gender: "Male" or "Female"
            icd_freq: ICD code frequency (1-683)
            cpt_freq: CPT code frequency (1-1815)
            month: Approval month (1-6)
        
        Returns:
            Dictionary with prediction results:
            {
                'eligible': bool,
                'confidence': float (0-1),
                'eligible_probability': float (0-1),
                'not_eligible_probability': float (0-1),
                'prediction_text': str
            }
        """
        # Validate inputs
        if not 1 <= age <= 120:
            raise ValueError(f"Age must be 1-120, got {age}")
        if gender.lower() not in ['male', 'female']:
            raise ValueError(f"Gender must be 'male' or 'female', got {gender}")
        if not 1 <= icd_freq <= 683:
            raise ValueError(f"ICD frequency must be 1-683, got {icd_freq}")
        if not 1 <= cpt_freq <= 1815:
            raise ValueError(f"CPT frequency must be 1-1815, got {cpt_freq}")
        if not 1 <= month <= 6:
            raise ValueError(f"Month must be 1-6, got {month}")
        
        # Encode gender
        gender_encoded = 1 if gender.lower() == 'male' else 0
        
        # Prepare data
        patient_data = np.array([[age, gender_encoded, icd_freq, cpt_freq, month]])
        
        # Scale
        patient_scaled = self.scaler.transform(patient_data)
        
        # Predict
        prediction = self.model.predict(patient_scaled)[0]
        probabilities = self.model.predict_proba(patient_scaled)[0]
        
        return {
            'eligible': bool(prediction == 1),
            'confidence': float(max(probabilities)),
            'eligible_probability': float(probabilities[1]),
            'not_eligible_probability': float(probabilities[0]),
            'prediction_text': 'ELIGIBLE' if prediction == 1 else 'NOT ELIGIBLE'
        }
    
    def predict_batch(self, patients: list) -> list:
        """
        Predict eligibility for multiple patients.
        
        Args:
            patients: List of dictionaries with keys: age, gender, icd_freq, cpt_freq, month
        
        Returns:
            List of prediction results
        """
        results = []
        for patient in patients:
            result = self.predict(
                age=patient['age'],
                gender=patient['gender'],
                icd_freq=patient['icd_freq'],
                cpt_freq=patient['cpt_freq'],
                month=patient['month']
            )
            results.append(result)
        return results

# Example usage
if __name__ == "__main__":
    # Single prediction
    predictor = InsuranceEligibilityPredictor()
    
    result = predictor.predict(
        age=45,
        gender="Male",
        icd_freq=15,
        cpt_freq=8,
        month=6
    )
    
    print("Single Prediction:")
    print(f"  Eligible: {result['eligible']}")
    print(f"  Confidence: {result['confidence']:.2%}")
    print(f"  Result: {result['prediction_text']}")
    
    # Batch predictions
    patients = [
        {'age': 35, 'gender': 'Male', 'icd_freq': 10, 'cpt_freq': 5, 'month': 3},
        {'age': 55, 'gender': 'Female', 'icd_freq': 25, 'cpt_freq': 15, 'month': 9},
        {'age': 42, 'gender': 'Male', 'icd_freq': 12, 'cpt_freq': 7, 'month': 6},
    ]
    
    batch_results = predictor.predict_batch(patients)
    print("\nBatch Predictions:")
    for i, result in enumerate(batch_results, 1):
        print(f"  Patient {i}: {result['prediction_text']} ({result['confidence']:.2%} confidence)")
