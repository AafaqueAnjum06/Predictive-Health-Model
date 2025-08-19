import streamlit as st
import joblib
import numpy as np
import random

# Load model and scaler
model_dict = joblib.load("../data/processed/heart_model.pkl")
model = model_dict["model"]
scaler = model_dict["scaler"]

st.title("🫀 Heart Disease Risk Prediction App")

st.write(
    """
    This tool uses machine learning to estimate your **risk of heart disease** 
    based on clinical features.  
    Please note: This is **not a medical diagnosis**. Always consult a healthcare professional.
    """
)

st.write("Fill out the details below to assess your risk of heart disease.")

# User-friendly inputs
age = st.number_input("Age", min_value=1, max_value=120, value=40)
cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=100, max_value=600, value=200)
maxhr = st.number_input("Maximum Heart Rate Achieved", min_value=50, max_value=220, value=150)
oldpeak = st.number_input("ST Depression (Oldpeak)", min_value=0.0, max_value=10.0, step=0.1, value=1.0)

# Friendly Yes/No mapping
fastingbs = st.radio("Fasting Blood Sugar > 120 mg/dL?", ["No", "Yes"])
sex_m = st.radio("Sex", ["Female", "Male"])
chestpain_ata = st.radio("Chest Pain Type: ATA?", ["No", "Yes"])
chestpain_nap = st.radio("Chest Pain Type: NAP?", ["No", "Yes"])
restingecg_st = st.radio("Resting ECG: ST?", ["No", "Yes"])
exerciseangina_y = st.radio("Exercise-Induced Angina?", ["No", "Yes"])
st_slope_flat = st.radio("ST Slope: Flat?", ["No", "Yes"])
st_slope_up = st.radio("ST Slope: Up?", ["No", "Yes"])

# Map inputs to numerical values
fastingbs = 1 if fastingbs == "Yes" else 0
sex_m = 1 if sex_m == "Male" else 0
chestpain_ata = 1 if chestpain_ata == "Yes" else 0
chestpain_nap = 1 if chestpain_nap == "Yes" else 0
restingecg_st = 1 if restingecg_st == "Yes" else 0
exerciseangina_y = 1 if exerciseangina_y == "Yes" else 0
st_slope_flat = 1 if st_slope_flat == "Yes" else 0
st_slope_up = 1 if st_slope_up == "Yes" else 0

# Risk-specific tips
low_risk_tips = [
    "✅ Keep it up! Maintain regular physical activity like walking or cycling.",
    "🥗 Continue eating a heart-friendly diet with more fruits and vegetables.",
    "💧 Stay hydrated and avoid excessive sugary drinks.",
    "🛌 Prioritize good sleep to support your heart health.",
    "🚭 If you smoke, consider quitting—it’s the best gift to your heart."
]

medium_risk_tips = [
    "⚠️ Try reducing your daily salt intake to help manage blood pressure.",
    "🏃 Aim for at least 30 minutes of exercise, 5 times a week.",
    "🥦 Choose whole grains and green vegetables over fried food.",
    "🧘 Practice stress management techniques like yoga or meditation.",
    "📋 Schedule a routine health check-up for cholesterol and sugar levels."
]

high_risk_tips = [
    "❗ Please consult a doctor soon for a professional heart check-up.",
    "💊 If prescribed medicines, take them regularly without skipping.",
    "🚶 Start light physical activity, but only after your doctor’s approval.",
    "🍲 Shift towards a low-fat, low-salt diet immediately.",
    "🚨 Do not ignore chest pain, shortness of breath, or unusual fatigue."
]

# Prediction
if st.button("🔍 Predict"):
    input_data = np.array([[age, cholesterol, maxhr, oldpeak, fastingbs, sex_m,
                            chestpain_ata, chestpain_nap, restingecg_st,
                            exerciseangina_y, st_slope_flat, st_slope_up]])

    input_data = scaler.transform(input_data)
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][prediction]

    # Risk categories
    if probability < 0.4:
        risk_category = "Low Risk"
        tip = random.choice(low_risk_tips)
    elif probability < 0.7:
        risk_category = "Medium Risk"
        tip = random.choice(medium_risk_tips)
    else:
        risk_category = "High Risk"
        tip = random.choice(high_risk_tips)

    # Professional Output
    if prediction == 1:
        st.error(f"⚠️ The model predicts **Heart Disease Risk**.\n\n"
                 f"**Confidence:** {probability*100:.2f}%\n"
                 f"\n**Risk Category:** {risk_category}")
    else:
        st.success(f"✅ The model predicts **No Heart Disease Risk**.\n\n"
                   f"**Confidence:** {probability*100:.2f}%\n"
                   f"\n**Risk Category:** {risk_category}")

    
    # Show a risk-specific random tip
    st.success(tip)
    
    # Disclaimer
    st.info("⚠️ This tool provides only a risk estimation, not a diagnosis. Please consult a healthcare professional for confirmation.")
