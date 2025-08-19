import streamlit as st
import joblib
import numpy as np

# Load dictionary
saved = joblib.load("../data/processed/heart_model.pkl")
model = saved["model"]        # classifier
scaler = saved.get("scaler")  # optional, only if you saved a scaler

st.title("Heart Disease Prediction")

# Collect user input
age = st.number_input("Age", min_value=1, max_value=120, value=30)
cholesterol = st.number_input("Cholesterol", min_value=100, max_value=600, value=200)
maxhr = st.number_input("MaxHR", min_value=60, max_value=220, value=150)
oldpeak = st.number_input("Oldpeak", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
fastingbs = st.selectbox("FastingBS (1=Yes, 0=No)", [0, 1])
sex_m = st.selectbox("Sex (1=Male, 0=Female)", [0, 1])
chestpain_ata = st.selectbox("ChestPainType_ATA", [0, 1])
chestpain_nap = st.selectbox("ChestPainType_NAP", [0, 1])
restingecg_st = st.selectbox("RestingECG_ST", [0, 1])
exerciseangina_y = st.selectbox("ExerciseAngina_Y", [0, 1])
st_slope_flat = st.selectbox("ST_Slope_Flat", [0, 1])
st_slope_up = st.selectbox("ST_Slope_Up", [0, 1])

# Create input array
input_data = np.array([[age, cholesterol, maxhr, oldpeak, fastingbs, sex_m,
                        chestpain_ata, chestpain_nap, restingecg_st,
                        exerciseangina_y, st_slope_flat, st_slope_up]])

# Apply scaler if available
if scaler is not None:
    input_data = scaler.transform(input_data)

# Predict
if st.button("Predict"):
    prediction = model.predict(input_data)[0]
    if prediction == 1:
        st.error("⚠️ The model predicts: Heart Disease")
    else:
        st.success("✅ The model predicts: No Heart Disease")
