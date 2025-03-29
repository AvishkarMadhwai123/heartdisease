import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Heart Disease & Symptom Detection App", layout="wide")

st.title("Heart Disease & Symptom Detection App")
st.write("### Predict the likelihood of heart disease and check for possible conditions based on your symptoms.")

# Section 1: Heart Disease Prediction
st.subheader("Heart Disease Risk Assessment")

# User input for health parameters
name = st.text_input("Enter your name")
date_of_check = st.date_input("Date of Check")
age = st.number_input("Age", min_value=1, max_value=120, value=30)
sex = st.selectbox("Sex", ["Male", "Female"])
cp = st.selectbox("Chest Pain Type", ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"])
trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=50, max_value=250, value=120)
chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=100, max_value=600, value=200)
fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ["Yes", "No"])
restecg = st.selectbox("Resting ECG Results", ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"])
thalach = st.number_input("Maximum Heart Rate Achieved", min_value=50, max_value=250, value=150)
exang = st.selectbox("Exercise-Induced Angina", ["Yes", "No"])
oldpeak = st.number_input("ST Depression Induced by Exercise", min_value=0.0, max_value=10.0, value=1.0)
slope = st.selectbox("Slope of the Peak Exercise ST Segment", ["Upsloping", "Flat", "Downsloping"])
ca = st.selectbox("Number of Major Vessels Colored by Fluoroscopy", [0, 1, 2, 3, 4])
thal = st.selectbox("Thalassemia", ["Normal", "Fixed Defect", "Reversible Defect"])

# Calculate risk level based on user input
def calculate_risk_level(age, trestbps, chol, thalach, oldpeak):
    risk_score = 0
    if age > 50: risk_score += 1
    if trestbps > 130: risk_score += 1
    if chol > 240: risk_score += 1
    if thalach < 120: risk_score += 1
    if oldpeak > 2.0: risk_score += 1
    
    if risk_score >= 3:
        return "High"
    elif risk_score == 2:
        return "Moderate"
    else:
        return "Low"

risk_level = ""
if st.button("Predict Heart Disease Risk"):
    risk_level = calculate_risk_level(age, trestbps, chol, thalach, oldpeak)
    if risk_level == "High":
        st.error(f"High risk of heart disease detected.")
    elif risk_level == "Moderate":
        st.warning(f"Moderate risk of heart disease.")
    else:
        st.success(f"Low risk of heart disease.")

# Section 2: Symptom Checker
st.subheader("Symptom Checker")

symptoms = st.multiselect("Select your symptoms:", [
    "Fever", "Cough", "Shortness of Breath", "Chest Pain", "Fatigue", "Headache", "Nausea", "Dizziness", "Swelling in Legs", "Palpitations"
])

# Simple symptom-based condition suggestions
def suggest_conditions(symptoms):
    conditions = []
    if "Fever" in symptoms and "Cough" in symptoms and "Shortness of Breath" in symptoms:
        conditions.append("Possible Respiratory Infection (e.g., Pneumonia, COVID-19)")
    if "Chest Pain" in symptoms and "Shortness of Breath" in symptoms:
        conditions.append("Possible Heart Condition (e.g., Angina, Heart Attack)")
    if "Fatigue" in symptoms and "Swelling in Legs" in symptoms:
        conditions.append("Possible Heart Failure")
    if "Headache" in symptoms and "Dizziness" in symptoms:
        conditions.append("Possible Hypertension or Neurological Issue")
    if not conditions:
        conditions.append("No specific condition detected. Please consult a doctor for a detailed diagnosis.")
    return conditions

conditions = []
if st.button("Check Symptoms"):
    conditions = suggest_conditions(symptoms)
    st.write("### Possible Conditions:")
    for condition in conditions:
        st.write(f"- {condition}")

# Visualization Section
st.subheader("Visualization of Risk Factors")

# Plot heart disease risk factors
risk_factors = {
    "Age": age,
    "Resting Blood Pressure": trestbps,
    "Cholesterol": chol,
    "Max Heart Rate": thalach,
    "ST Depression": oldpeak
}

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=list(risk_factors.keys()), y=list(risk_factors.values()), ax=ax)
ax.set_title("Heart Disease Risk Factors")
ax.set_ylabel("Values")
ax.set_xlabel("Factors")
plt.tight_layout()
st.pyplot(fig)

# Symptoms distribution pie chart
if symptoms:
    symptom_counts = {symptom: symptoms.count(symptom) for symptom in set(symptoms)}
    fig2, ax2 = plt.subplots()
    ax2.pie(symptom_counts.values(), labels=symptom_counts.keys(), autopct="%1.1f%%", startangle=140)
    ax2.set_title("Symptom Distribution")
    plt.tight_layout()
    st.pyplot(fig2)
