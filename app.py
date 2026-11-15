
import streamlit as st
import joblib
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Medical Cost Predictor",
    page_icon="🏥",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background-color: #F5F8FC;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1150px;
}

.header {
    background: linear-gradient(120deg, #123B59, #167D91);
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.header h1 {
    color: white;
    font-size: 34px;
    margin-bottom: 8px;
}

.header p {
    color: #E2F3F7;
    font-size: 16px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #E2EAF0;
    text-align: center;
}

.metric-title {
    color: #718096;
    font-size: 14px;
}

.metric-value {
    color: #123B59;
    font-size: 27px;
    font-weight: 700;
}

.section-card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #E2EAF0;
    margin-bottom: 20px;
}

.section-title {
    color: #123B59;
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 15px;
}

.result-card {
    background: #E6F6F3;
    border: 1px solid #B8E5DC;
    padding: 30px;
    border-radius: 16px;
    text-align: center;
    margin-top: 20px;
}

.result-label {
    color: #287A70;
    font-size: 16px;
}

.result-value {
    color: #11695D;
    font-size: 38px;
    font-weight: 800;
}

div.stButton > button {
    background-color: #147D78;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-size: 17px;
    font-weight: 600;
    width: 100%;
}

div.stButton > button:hover {
    background-color: #0E625E;
    color: white;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = joblib.load('medical_cost_model.pkl')

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
    <h1>🏥 Medical Cost Predictor</h1>
    <p>
        Estimate your medical insurance expenses using
        Machine Learning.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- MODEL METRICS ----------------
st.markdown("### Model Performance")

m1, m2 = st.columns(2)

with m1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">R² Score</div>
        <div class="metric-value">0.8871</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Mean Absolute Error</div>
        <div class="metric-value">$2,830</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------- INPUT FORM ----------------
st.markdown("### Enter Your Information")
st.write("Provide the following details to estimate medical costs.")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 Personal Information</div>',
                unsafe_allow_html=True)

    age = st.slider("Age", 18, 64, 30)
    sex = st.radio("Sex", ["male", "female"], horizontal=True)
    region = st.selectbox(
        "Residential Region",
        ["northeast", "northwest", "southeast", "southwest"]
    )

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🩺 Health Information</div>',
                unsafe_allow_html=True)

    bmi = st.slider("Body Mass Index (BMI)", 15.0, 53.0, 25.0)
    children = st.selectbox("Number of Children", [0, 1, 2, 3, 4, 5])
    smoker = st.radio("Smoking Status", ["no", "yes"], horizontal=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PREDICTION ----------------
st.write("")

if st.button("Calculate Estimated Medical Cost"):

    # BMI category
    if bmi < 18.5:
        bmi_cat = 'underweight'
    elif bmi < 25:
        bmi_cat = 'normal'
    elif bmi < 30:
        bmi_cat = 'overweight'
    else:
        bmi_cat = 'obese'

    # Age group
    if age < 30:
        age_grp = 'young'
    elif age < 50:
        age_grp = 'middle'
    else:
        age_grp = 'senior'

    # Prepare input data
    data = pd.DataFrame([{
        'age': age,
        'sex': sex,
        'bmi': bmi,
        'children': children,
        'smoker': smoker,
        'region': region,
        'bmi_category': bmi_cat,
        'age_group': age_grp,
        'smoker_bmi': bmi if smoker == 'yes' else 0,
        'is_obese': 1 if bmi >= 30 else 0,
        'is_smoker': 1 if smoker == 'yes' else 0
    }])

    # Predict
    pred = model.predict(data)[0]

    # Display result
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">Estimated Medical Cost</div>
        <div class="result-value">${pred:,.2f}</div>
        <p style="color:#287A70;">
            Your estimated medical insurance expense
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "This is an ML-based estimate, not an actual insurance quote "
        "or medical assessment."
    )

# ---------------- FOOTER ----------------
st.write("")
st.divider()

st.markdown("""
<center>
    <p style="color:#718096; font-size:13px;">
        Developed by H.M.D.N. Herath (SA25610046)
        <br>
        Powered by Machine Learning | Linear Regression
    </p>
</center>
""", unsafe_allow_html=True)
