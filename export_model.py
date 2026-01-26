import pandas as pd
import numpy as np
import pickle
import sys
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression

# Load and prepare data
file_path = "/Users/ashishbathula/Desktop/gmu data /csv file -gmu radiology.csv"
df = pd.read_csv(file_path)

# Age extraction function
def extract_age(age_str):
    try:
        if pd.isna(age_str):
            return np.nan
        years = int(str(age_str).split(':')[0].strip().replace('Y', '').strip())
        months = int(str(age_str).split(':')[1].strip().replace('M', '').strip())
        total_age = years + (months / 12)
        return total_age
    except:
        return np.nan

df['Age_Years'] = df['Age'].apply(extract_age)
df = df.dropna(subset=['Age_Years'])
df = df.drop_duplicates()

# Gender encoding
gender_mapping = {'Male': 1, 'Female': 0}
df['Gender_Encoded'] = df['Gender'].map(gender_mapping)

# ICD and CPT frequencies
icd_category_counts = df.groupby('ICD').size().reset_index(name='ICD_Frequency')
df = df.merge(icd_category_counts, on='ICD', how='left')

cpt_category_counts = df.groupby('CPT').size().reset_index(name='CPT_Frequency')
df = df.merge(cpt_category_counts, on='CPT', how='left')

# Date parsing
df['ApprovedDate'] = pd.to_datetime(df['ApprovedDate'], format='%m/%d/%y', errors='coerce')
df['Month_of_Approval'] = df['ApprovedDate'].dt.month
df['Month_of_Approval'] = df['Month_of_Approval'].fillna(df['Month_of_Approval'].median())

# Target variable
df['Insurance_Eligible'] = (df['Insurance'].str.strip() == 'Yes').astype(int)

# Handle missing values
df['Age_Years'].fillna(df['Age_Years'].median(), inplace=True)
df['ICD_Frequency'].fillna(df['ICD_Frequency'].median(), inplace=True)
df['CPT_Frequency'].fillna(df['CPT_Frequency'].median(), inplace=True)

# Select features
features = ['Age_Years', 'Gender_Encoded', 'ICD_Frequency', 'CPT_Frequency', 'Month_of_Approval']
X = df[features].copy()
y = df['Insurance_Eligible'].copy()

# Remove NaN values
valid_indices = ~X.isna().any(axis=1)
X = X[valid_indices]
y = y[valid_indices]

# Initialize and fit scaler
scaler = MinMaxScaler(feature_range=(0, 1))
X_scaled = scaler.fit_transform(X)

# Train model
model = LogisticRegression(random_state=42, max_iter=1000, solver='lbfgs', class_weight='balanced')
model.fit(X_scaled, y)

# Save model and scaler
with open('/Users/ashishbathula/Desktop/gmu data /model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('/Users/ashishbathula/Desktop/gmu data /scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Save feature names
with open('/Users/ashishbathula/Desktop/gmu data /features.pkl', 'wb') as f:
    pickle.dump(features, f)

# Save ICD/CPT mappings for reference
icd_mapping = dict(zip(icd_category_counts['ICD'], icd_category_counts['ICD_Frequency']))
cpt_mapping = dict(zip(cpt_category_counts['CPT'], cpt_category_counts['CPT_Frequency']))

with open('/Users/ashishbathula/Desktop/gmu data /icd_mapping.pkl', 'wb') as f:
    pickle.dump(icd_mapping, f)

with open('/Users/ashishbathula/Desktop/gmu data /cpt_mapping.pkl', 'wb') as f:
    pickle.dump(cpt_mapping, f)

print("✅ Model saved: model.pkl")
print("✅ Scaler saved: scaler.pkl")
print("✅ Features saved: features.pkl")
print("✅ ICD mapping saved: icd_mapping.pkl")
print("✅ CPT mapping saved: cpt_mapping.pkl")
print(f"\n📊 Model Performance on Training Data:")
print(f"   Accuracy: {model.score(X_scaled, y):.4f}")
print(f"\n🎯 Model Coefficients:")
for feat, coef in zip(features, model.coef_[0]):
    print(f"   {feat}: {coef:.6f}")
print(f"\n📌 Intercept: {model.intercept_[0]:.6f}")
