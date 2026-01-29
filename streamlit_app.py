import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# Page configuration
st.set_page_config(
    page_title="Insurance Eligibility Predictor",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        max-width: 600px;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        border-radius: 5px;
        font-size: 16px;
        padding: 12px;
        font-weight: bold;
    }
    .prediction-eligible {
        background-color: #d4edda;
        border: 3px solid #28a745;
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        font-size: 32px;
        color: #155724;
        font-weight: bold;
    }
    .prediction-not-eligible {
        background-color: #f8d7da;
        border: 3px solid #dc3545;
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        font-size: 32px;
        color: #721c24;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Load model and scaler
@st.cache_resource
def load_model_artifacts():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try local paths first
    paths = {
        'model': os.path.join(script_dir, 'model.pkl'),
        'scaler': os.path.join(script_dir, 'scaler.pkl'),
        'features': os.path.join(script_dir, 'features.pkl')
    }
    
    # If not found, try parent directory
    if not os.path.exists(paths['model']):
        parent_dir = os.path.dirname(script_dir)
        for key in paths:
            paths[key] = os.path.join(parent_dir, f"{key}.pkl")
    
    model = pickle.load(open(paths['model'], 'rb'))
    scaler = pickle.load(open(paths['scaler'], 'rb'))
    features = pickle.load(open(paths['features'], 'rb'))
    
    return model, scaler, features

try:
    model, scaler, features = load_model_artifacts()
except Exception as e:
    st.error(f"❌ Error loading model: {str(e)}")
    st.stop()

# Title
st.title("🏥 Insurance Eligibility Check")
st.markdown("**Predict insurance approval in seconds**")

# Main form
st.subheader("Enter Patient Information")

# Age input
age = st.number_input(
    "Age (years)",
    min_value=1,
    max_value=120,
    value=45,
    step=1
)

# Gender input
gender = st.radio(
    "Gender",
    options=["Male", "Female"],
    horizontal=True
)

# Service Name input - dropdown with common services
service_options = [
    "Select a service...",
    "Radiology",
    "Surgery",
    "Physical Therapy",
    "Laboratory Tests",
    "Cardiology",
    "Orthopedics",
    "Neurology",
    "Dermatology",
    "Other"
]

service_name = st.selectbox(
    "Service Name",
    options=service_options,
    help="Select the medical service for eligibility check"
)

# Map service names to frequency values for model prediction
service_frequency_map = {
    "Radiology": 100,
    "Surgery": 200,
    "Physical Therapy": 50,
    "Laboratory Tests": 150,
    "Cardiology": 120,
    "Orthopedics": 110,
    "Neurology": 80,
    "Dermatology": 60,
    "Other": 75
}

# Get frequency value based on service
if service_name == "Select a service...":
    service_frequency = 100
else:
    service_frequency = service_frequency_map[service_name]

# Default values for fields we're not asking about
cpt_frequency = 300  # Default procedure frequency
month = 3  # Default month

# Prediction section
st.markdown("---")

if st.button("🔍 Check Eligibility", use_container_width=True):
    # Validate that a service is selected
    if service_name == "Select a service...":
        st.error("❌ Please select a service to check eligibility")
    else:
        # Prepare input data
        gender_encoded = 1 if gender == "Male" else 0
        
        input_data = np.array([[age, gender_encoded, service_frequency, cpt_frequency, month]])
        
        # Scale input
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0]
        
        # Display results
        st.markdown("")
        
        if prediction == 1:
            st.markdown("""
                <div class="prediction-eligible">
                ✅ APPROVED
                </div>
            """, unsafe_allow_html=True)
            st.success(f"Insurance Eligibility: **APPROVED** (Confidence: {max(probability) * 100:.1f}%)")
        else:
            st.markdown("""
                <div class="prediction-not-eligible">
                ❌ NOT APPROVED
                </div>
            """, unsafe_allow_html=True)
            st.error(f"Insurance Eligibility: **NOT APPROVED** (Confidence: {max(probability) * 100:.1f}%)")
    

