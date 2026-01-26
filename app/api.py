"""
Flask REST API for Insurance Eligibility Prediction
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from insurance_predictor import predict_insurance_eligibility

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JSON_SORT_KEYS'] = False

@app.route('/', methods=['GET'])
def home():
    """Serve the web interface"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict insurance eligibility
    
    Expected JSON input:
    {
        "age": 45.5,
        "gender": "Male",
        "icd_frequency": 15,
        "cpt_frequency": 8,
        "month": 6,
        "disease": "Back Pain"  # Optional - for context
    }
    """
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['age', 'gender', 'icd_frequency', 'cpt_frequency', 'month']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'status': 'error'
            }), 400
        
        # Get prediction
        result = predict_insurance_eligibility(
            age=float(data['age']),
            gender=data['gender'],
            icd_frequency=int(data['icd_frequency']),
            cpt_frequency=int(data['cpt_frequency']),
            month=int(data['month'])
        )
        
        if 'error' in result:
            return jsonify(result), 500
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        result['disease'] = data.get('disease', 'Not specified')
        
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({
            'error': f'Invalid input type: {str(e)}',
            'status': 'error'
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Insurance Eligibility Prediction API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/info', methods=['GET'])
def info():
    """Get API information and feature ranges"""
    return jsonify({
        'service': 'Insurance Eligibility Prediction',
        'version': '1.0.0',
        'description': 'Predicts patient insurance eligibility based on medical records',
        'algorithm': 'Logistic Regression with MinMax Scaling',
        'features': {
            'age': {
                'type': 'float',
                'range': [1.0, 117.4],
                'unit': 'years',
                'description': 'Patient age in decimal years'
            },
            'gender': {
                'type': 'string',
                'values': ['Male', 'Female'],
                'description': 'Patient gender'
            },
            'icd_frequency': {
                'type': 'integer',
                'range': [1, 683],
                'description': 'Frequency of ICD code occurrence'
            },
            'cpt_frequency': {
                'type': 'integer',
                'range': [1, 1815],
                'description': 'Frequency of CPT code occurrence'
            },
            'month': {
                'type': 'integer',
                'range': [1, 6],
                'description': 'Month of service approval'
            }
        },
        'model_metrics': {
            'accuracy': 0.5809,
            'precision': 0.8451,
            'recall': 0.5615,
            'f1_score': 0.6747,
            'roc_auc': 0.6269
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
