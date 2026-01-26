"""
Flask API for Insurance Eligibility Prediction
Run with: python api.py
Access at: http://localhost:5000
"""

from flask import Flask, request, jsonify
import pickle
import numpy as np
import json

app = Flask(__name__)

# Load model, scaler, and features
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
features = pickle.load(open('features.pkl', 'rb'))

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Insurance Eligibility Predictor'})

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict insurance eligibility
    
    Request JSON:
    {
        "age": 45,
        "gender": "Male",
        "icd_frequency": 15,
        "cpt_frequency": 8,
        "month": 6
    }
    
    Response JSON:
    {
        "eligible": true,
        "confidence": 0.558,
        "eligible_probability": 0.558,
        "not_eligible_probability": 0.442
    }
    """
    try:
        data = request.json
        
        # Validate input
        required_fields = ['age', 'gender', 'icd_frequency', 'cpt_frequency', 'month']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing fields. Required: {required_fields}'}), 400
        
        # Extract data
        age = int(data['age'])
        gender = data['gender'].lower()
        icd_freq = int(data['icd_frequency'])
        cpt_freq = int(data['cpt_frequency'])
        month = int(data['month'])
        
        # Validate ranges
        if not 1 <= age <= 120:
            return jsonify({'error': 'Age must be 1-120'}), 400
        if gender not in ['male', 'female']:
            return jsonify({'error': 'Gender must be male or female'}), 400
        if not 1 <= icd_freq <= 683:
            return jsonify({'error': 'ICD frequency must be 1-683'}), 400
        if not 1 <= cpt_freq <= 1815:
            return jsonify({'error': 'CPT frequency must be 1-1815'}), 400
        if not 1 <= month <= 6:
            return jsonify({'error': 'Month must be 1-6'}), 400
        
        # Prepare data
        gender_encoded = 1 if gender == 'male' else 0
        patient_data = np.array([[age, gender_encoded, icd_freq, cpt_freq, month]])
        
        # Scale and predict
        patient_scaled = scaler.transform(patient_data)
        prediction = model.predict(patient_scaled)[0]
        probabilities = model.predict_proba(patient_scaled)[0]
        
        return jsonify({
            'eligible': bool(prediction == 1),
            'confidence': float(max(probabilities)),
            'eligible_probability': float(probabilities[1]),
            'not_eligible_probability': float(probabilities[0]),
            'patient_info': {
                'age': age,
                'gender': gender.capitalize(),
                'icd_frequency': icd_freq,
                'cpt_frequency': cpt_freq,
                'month': month
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict-batch', methods=['POST'])
def predict_batch():
    """
    Predict eligibility for multiple patients
    
    Request JSON:
    {
        "patients": [
            {"age": 45, "gender": "Male", "icd_frequency": 15, "cpt_frequency": 8, "month": 6},
            {"age": 55, "gender": "Female", "icd_frequency": 25, "cpt_frequency": 15, "month": 3}
        ]
    }
    """
    try:
        data = request.json
        
        if 'patients' not in data:
            return jsonify({'error': 'Missing patients array'}), 400
        
        patients = data['patients']
        results = []
        
        for patient in patients:
            try:
                age = int(patient['age'])
                gender = patient['gender'].lower()
                icd_freq = int(patient['icd_frequency'])
                cpt_freq = int(patient['cpt_frequency'])
                month = int(patient['month'])
                
                gender_encoded = 1 if gender == 'male' else 0
                patient_array = np.array([[age, gender_encoded, icd_freq, cpt_freq, month]])
                
                patient_scaled = scaler.transform(patient_array)
                prediction = model.predict(patient_scaled)[0]
                probabilities = model.predict_proba(patient_scaled)[0]
                
                results.append({
                    'eligible': bool(prediction == 1),
                    'confidence': float(max(probabilities)),
                    'eligible_probability': float(probabilities[1])
                })
            except Exception as e:
                results.append({'error': str(e)})
        
        return jsonify({'results': results, 'total': len(results)})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/info', methods=['GET'])
def info():
    """Get model information"""
    model_info = pickle.load(open('model_info.pkl', 'rb'))
    
    return jsonify({
        'model_type': model_info['model_type'],
        'features': model_info['features'],
        'coefficients': model_info['coefficients'],
        'intercept': float(model_info['intercept']),
        'performance': {
            'accuracy': float(model_info['accuracy']),
            'precision': float(model_info['precision']),
            'recall': float(model_info['recall']),
            'f1_score': float(model_info['f1_score']),
            'roc_auc': float(model_info['roc_auc'])
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
