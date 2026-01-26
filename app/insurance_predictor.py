#!/usr/bin/env python3
"""
Insurance Eligibility Prediction API
Save model and scaler for production use
"""

import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression

# Note: This script assumes the model has been trained
# In production, load the trained model and scaler from the Jupyter notebook

def save_model_artifacts(model, scaler, output_dir='models'):
    """Save trained model and scaler"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    with open(f'{output_dir}/insurance_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Save scaler
    with open(f'{output_dir}/minmax_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print(f"✓ Model saved to {output_dir}/insurance_model.pkl")
    print(f"✓ Scaler saved to {output_dir}/minmax_scaler.pkl")

def load_model_artifacts(model_path='models/insurance_model.pkl', 
                        scaler_path='models/minmax_scaler.pkl'):
    """Load trained model and scaler"""
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    return model, scaler

def predict_insurance_eligibility(age, gender, icd_frequency, cpt_frequency, month):
    """
    Predict insurance eligibility for a patient
    
    Args:
        age (float): Patient age in years (e.g., 45.5)
        gender (str): 'Male' or 'Female'
        icd_frequency (int): Frequency of ICD code (1-683)
        cpt_frequency (int): Frequency of CPT code (1-1815)
        month (int): Month of approval (1-6)
    
    Returns:
        dict: Prediction result with eligibility status and confidence
    """
    
    try:
        # Load model and scaler
        model, scaler = load_model_artifacts()
        
        # Encode gender
        gender_encoded = 1 if gender.lower() == 'male' else 0
        
        # Create feature array
        features = np.array([[age, gender_encoded, icd_frequency, cpt_frequency, month]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Get prediction
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        
        result = {
            'eligible': bool(prediction),
            'eligibility_status': 'ELIGIBLE' if prediction == 1 else 'NOT ELIGIBLE',
            'confidence_not_eligible': float(probability[0]),
            'confidence_eligible': float(probability[1]),
            'risk_score': float(probability[0]),
            'input_data': {
                'age': age,
                'gender': gender,
                'icd_frequency': icd_frequency,
                'cpt_frequency': cpt_frequency,
                'month': month
            }
        }
        
        return result
    
    except FileNotFoundError:
        return {
            'error': 'Model files not found. Please train and save the model first.',
            'status': 'error'
        }

if __name__ == '__main__':
    # Example usage
    print("Insurance Eligibility Prediction System")
    print("=" * 50)
    
    # Example prediction
    result = predict_insurance_eligibility(
        age=45.5,
        gender='Male',
        icd_frequency=15,
        cpt_frequency=8,
        month=6
    )
    
    print("\nPrediction Result:")
    print(f"Status: {result.get('eligibility_status')}")
    print(f"Confidence (Eligible): {result.get('confidence_eligible', 'N/A'):.2%}")
    print(f"Confidence (Not Eligible): {result.get('confidence_not_eligible', 'N/A'):.2%}")
