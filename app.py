
import streamlit as st
import joblib
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Medical Cost Predictor",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""

<style>

/* Main background */
.stApp {
    background-color: #F4F7FA;
    color: #FFFFFF;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1150px;
}

/* Header */
.header {
    background: linear-gradient(120deg, #123047, #087F75);
    padding: 35px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.header h1 {
    color: #FFFFFF !important;
    font-size: 34px;
    margin-bottom: 8px;
}

.header p {
    color: #FFFFFF !important;
    font-size: 16px;
}

/* Main headings */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.section-title {
    color: #FFFFFF !important;
    font-weight: 700;
}

/* Normal text */
.stApp p,
.stApp .stMarkdown {
    color: #1F2937;
}

/* Input labels */
.stSlider label,
.stRadio label,
.stSelectbox label {
    color: #102A43 !important;
    font-weight: 700 !important;
}

/* Radio options */
.stRadio div[role="radiogroup"] label p {
    color: #1F2937 !important;
}

/* Dropdown text */
.stSelectbox div[data-baseweb="select"] * {
    color: #102A43 !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #FFFFFF;
}

/* Slider values */
.stSlider [data-testid="stThumbValue"] {
    color: #102A43 !important;
}

/* Input cards */
.section-card {
    background: #FFFFFF;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #D5E0E8;
    margin-bottom: 20px;
}

.section-title {
    font-size: 21px;
    margin-bottom: 15px;
}

/* Prediction button */
div.stButton > button {
    background-color: #087F75 !important;
    color: #FFFFFF !important;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-size: 17px;
    font-weight: 700;
    width: 100%;
}

div.stButton > button p {
    color: #FFFFFF !important;
}

div.stButton > button:hover {
    background-color: #06645D !important;
    color: #FFFFFF !important;
}

/* Captions */
.stCaption,
.stCaption p {
    color: #374151 !important;
}

/* Footer */
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



# ---------------- INPUT FORM ----------------
st.markdown("### Enter Your Information")

st.write(
    "Provide the following details to estimate your medical costs."
)

col1, col2 = st.columns(2, gap="large")


# ---------------- PERSONAL INFORMATION ----------------
with col1:

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">👤 Personal Information</div>',
        unsafe_allow_html=True
    )

    age = st.slider(
        "Age",
        18, 64, 30
    )

    sex = st.radio(
        "Sex",
        ["male", "female"],
        horizontal=True
    )

    region = st.selectbox(
        "Residential Region",
        ["northeast", "northwest", "southeast", "southwest"]
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- HEALTH INFORMATION ----------------
with col2:

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">🩺 Health Information</div>',
        unsafe_allow_html=True
    )

    bmi = st.slider(
        "Body Mass Index (BMI)",
        15.0, 53.0, 25.0
    )

    children = st.selectbox(
        "Number of Children",
        [0, 1, 2, 3, 4, 5]
    )

    smoker = st.radio(
        "Smoking Status",
        ["no", "yes"],
        horizontal=True
    )

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

    # Predict medical cost
    pred = model.predict(data)[0]


    # Display prediction result
    st.markdown("---")

    st.markdown(
        "<h3 style='text-align:center; color:#102A43;'>"
        "YOUR ESTIMATED MEDICAL COST</h3>",
        unsafe_allow_html=True
    )

    st.metric(
        label="Estimated Insurance Expense",
        value=f"${pred:,.2f}"
    )

    st.caption(
        "This is an ML-based estimate, not an actual insurance "
        "quote or medical assessment."
    )



# ---------------- FOOTER ----------------
st.write("")
st.divider()

st.markdown("""
<center>
    <p style="color:#1F2937; font-size:13px;">
        Developed by H.M.D.N. Herath (SA25610046)
        <br>
        Powered by Machine Learning | Linear Regression
    </p>
</center>
""", unsafe_allow_html=True)
