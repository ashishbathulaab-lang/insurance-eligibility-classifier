import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# Page configuration
st.set_page_config(
    page_title="Insurance Eligibility Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        border-radius: 5px;
        font-size: 16px;
        padding: 10px;
    }
    .prediction-eligible {
        background-color: #d4edda;
        border: 2px solid #28a745;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
        font-size: 20px;
        color: #155724;
        font-weight: bold;
    }
    .prediction-not-eligible {
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
        font-size: 20px;
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
st.title("🏥 Insurance Eligibility Prediction System")
st.markdown("**Predict patient insurance eligibility using AI**")

# Sidebar
st.sidebar.title("📋 About")
st.sidebar.info(
    """
    This application predicts whether a patient is eligible for insurance based on:
    - Patient age
    - Gender
    - ICD code (diagnosis) frequency
    - CPT code (procedure) frequency
    - Service approval month
    
    **Model**: Logistic Regression with MinMax Scaling
    **Accuracy**: 58.09% | **Precision**: 84.51%
    """
)

# Main content - Two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Patient Information")
    
    # Age input
    age = st.number_input(
        "Age (years)",
        min_value=1,
        max_value=120,
        value=45,
        step=1,
        help="Patient age in years"
    )
    
    # Gender input
    gender = st.radio(
        "Gender",
        options=["Male", "Female"],
        horizontal=True,
        help="Patient gender"
    )
    
    # ICD Frequency
    icd_frequency = st.number_input(
        "ICD Code Frequency",
        min_value=1,
        max_value=683,
        value=50,
        step=1,
        help="How many times this ICD code appears in records (1-683)"
    )
    
    # CPT Frequency
    cpt_frequency = st.number_input(
        "CPT Code Frequency",
        min_value=1,
        max_value=1815,
        value=300,
        step=1,
        help="How many times this CPT code appears in records (1-1815)"
    )
    
    # Month of Approval
    month = st.slider(
        "Approval Month",
        min_value=1,
        max_value=6,
        value=3,
        step=1,
        help="Service approval month (1=January, 6=June)"
    )

with col2:
    st.subheader("🔍 Feature Summary")
    
    # Display feature ranges
    feature_info = {
        "Age (years)": f"{age} (Range: 1-117)",
        "Gender": gender,
        "ICD Frequency": f"{icd_frequency} (Range: 1-683)",
        "CPT Frequency": f"{cpt_frequency} (Range: 1-1815)",
        "Month": f"{month} (Range: 1-6)"
    }
    
    for feature, value in feature_info.items():
        st.metric(label=feature, value=value)
    
    st.markdown("---")
    st.subheader("📊 Model Information")
    st.write(f"**Features used**: {len(features)}")
    st.write(f"**Model type**: Logistic Regression")
    st.write(f"**Scaling method**: MinMax (0-1)")

# Prediction section
st.markdown("---")
st.subheader("🎯 Make Prediction")

if st.button("🔮 Predict Insurance Eligibility", use_container_width=True):
    # Prepare input data
    gender_encoded = 1 if gender == "Male" else 0
    
    input_data = np.array([[age, gender_encoded, icd_frequency, cpt_frequency, month]])
    
    # Scale input
    input_scaled = scaler.transform(input_data)
    
    # Make prediction
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0]
    
    # Display results
    st.markdown("---")
    st.subheader("📈 Prediction Results")
    
    # Create columns for results
    result_col1, result_col2, result_col3 = st.columns(3)
    
    with result_col1:
        st.metric(
            "Eligibility Status",
            "✅ ELIGIBLE" if prediction == 1 else "❌ NOT ELIGIBLE",
            delta=None
        )
    
    with result_col2:
        st.metric(
            "Confidence Score",
            f"{max(probability) * 100:.2f}%",
            delta=None
        )
    
    with result_col3:
        if prediction == 1:
            risk_score = probability[0] * 100
            status = "Risk of Denial"
        else:
            risk_score = probability[1] * 100
            status = "Risk of Approval"
        st.metric(
            status,
            f"{risk_score:.2f}%",
            delta=None
        )
    
    # Detailed probability breakdown
    st.markdown("### Probability Breakdown")
    
    prob_col1, prob_col2 = st.columns(2)
    
    with prob_col1:
        st.write("**Not Eligible Probability**")
        st.progress(probability[0])
        st.text(f"{probability[0] * 100:.2f}%")
    
    with prob_col2:
        st.write("**Eligible Probability**")
        st.progress(probability[1])
        st.text(f"{probability[1] * 100:.2f}%")
    
    # Detailed explanation
    st.markdown("---")
    st.subheader("📋 Decision Explanation")
    
    explanation = f"""
    **Patient Profile:**
    - Age: {age} years
    - Gender: {gender}
    - ICD Code Frequency: {icd_frequency}
    - CPT Code Frequency: {cpt_frequency}
    - Approval Month: {month}
    
    **Model Decision:**
    The model calculated a probability score of **{probability[1]:.4f}** (on a 0-1 scale).
    
    - If probability > 0.5 → Patient is **ELIGIBLE** ✅
    - If probability < 0.5 → Patient is **NOT ELIGIBLE** ❌
    - Current probability: **{probability[1]:.4f}**
    
    **Result:** Patient is **{"ELIGIBLE" if prediction == 1 else "NOT ELIGIBLE"}** for insurance
    with a confidence level of **{max(probability) * 100:.2f}%**.
    """
    
    st.info(explanation)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
        <p>Insurance Eligibility Prediction System | Built with Logistic Regression + MinMax Scaling</p>
        <p>⚠️ This tool is for decision support only. Always verify with official insurance policies.</p>
    </div>
""", unsafe_allow_html=True)

# Batch prediction section
st.markdown("---")
st.subheader("📊 Batch Prediction")

st.write("Upload a CSV file to predict eligibility for multiple patients.")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=['csv'],
    help="CSV should have columns: age, gender, icd_frequency, cpt_frequency, month"
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        
        # Validate columns
        required_cols = ['age', 'gender', 'icd_frequency', 'cpt_frequency', 'month']
        if not all(col.lower() in df.columns.str.lower() for col in required_cols):
            st.error(f"❌ CSV must contain columns: {', '.join(required_cols)}")
        else:
            # Prepare data
            df_clean = df.copy()
            df_clean.columns = df_clean.columns.str.lower()
            
            df_clean['gender_encoded'] = (df_clean['gender'].str.lower() == 'male').astype(int)
            
            # Scale and predict
            X_batch = df_clean[['age', 'gender_encoded', 'icd_frequency', 'cpt_frequency', 'month']].values
            X_batch_scaled = scaler.transform(X_batch)
            
            predictions = model.predict(X_batch_scaled)
            probabilities = model.predict_proba(X_batch_scaled)
            
            # Add results to dataframe
            results_df = df_clean.copy()
            results_df['prediction'] = ['ELIGIBLE' if p == 1 else 'NOT ELIGIBLE' for p in predictions]
            results_df['confidence'] = [f"{max(prob) * 100:.2f}%" for prob in probabilities]
            results_df['eligible_probability'] = [f"{prob[1] * 100:.2f}%" for prob in probabilities]
            
            st.success(f"✅ Processed {len(results_df)} patients")
            
            st.dataframe(results_df, use_container_width=True)
            
            # Download results
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results CSV",
                data=csv,
                file_name="insurance_predictions.csv",
                mime="text/csv"
            )
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
