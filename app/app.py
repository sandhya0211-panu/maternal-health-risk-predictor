import streamlit as st
import requests
import plotly.graph_objects as go

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="Maternal Health Risk Predictor",
    layout="centered",
    page_icon="🤰"
)

# ===============================
# 🌈 Custom CSS (Gradient + UI)
# ===============================
st.markdown("""
<style>

/* Gradient Background */
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
}

/* Title */
.big-title {
    font-size:32px !important;
    font-weight:700;
    text-align:center;
}

/* Glass Card */
.card {
    padding:15px;
    border-radius:15px;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    margin-bottom:15px;
    color: white;
}

/* Input styling */
input, .stNumberInput input {
    background-color: rgba(255,255,255,0.8) !important;
    color: black !important;
    border-radius: 8px !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #ff7e5f, #feb47b);
    color: white;
    border-radius: 10px;
    font-weight: bold;
    height: 3em;
    width: 100%;
}

/* Divider */
hr {
    border: 1px solid rgba(255,255,255,0.3);
}

</style>
""", unsafe_allow_html=True)

# ===============================
# 🎯 Gauge Function
# ===============================
def show_gauge(risk):
    risk_map = {
        "Low Risk": 0,
        "Mid Risk": 1,
        "High Risk": 2
    }

    value = risk_map.get(risk, 0)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': "Risk Level"},
        gauge={
            'axis': {'range': [0, 2]},
            'bar': {'color': "white"},
            'steps': [
                {'range': [0, 0.66], 'color': "green"},
                {'range': [0.66, 1.33], 'color': "yellow"},
                {'range': [1.33, 2], 'color': "red"}
            ],
        }
    ))

    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return fig


# ===============================
# 🏷 Title
# ===============================
st.markdown('<p class="big-title">🤰 Maternal Health Risk Predictor</p>', unsafe_allow_html=True)
st.write("AI-powered system for predicting maternal risk with explanations and suggestions.")

st.markdown("---")

# ===============================
# 📝 Input Section
# ===============================
st.subheader("📝 Patient Details")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=10, max_value=100, value=30)
    systolic = st.number_input("Systolic BP", value=120)
    bs = st.number_input("Blood Sugar", value=6.5)

with col2:
    diastolic = st.number_input("Diastolic BP", value=80)
    temp = st.number_input("Body Temperature", value=98.0)
    hr = st.number_input("Heart Rate", value=75)

st.markdown("---")

# ===============================
# 🚀 Predict Button
# ===============================
col_center = st.columns([1,2,1])
with col_center[1]:
    predict_btn = st.button("🚀 Predict Risk")

# ===============================
# 🔍 Prediction Section
# ===============================
if predict_btn:

    data = {
        "Age": age,
        "SystolicBP": systolic,
        "DiastolicBP": diastolic,
        "BS": bs,
        "BodyTemp": temp,
        "HeartRate": hr
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=data)
        result = response.json()

        risk = result["RiskLevel"]
        reasons = result["Reasons"]
        suggestions = result["Suggestions"]
        disclaimer = result["Disclaimer"]

        st.markdown("## 🩺 Prediction Result")

        # 🎨 Risk Display
        if risk == "Low Risk":
            st.success(f"🟢 {risk}")
        elif risk == "Mid Risk":
            st.warning(f"🟡 {risk}")
        else:
            st.error(f"🔴 {risk}")

        # 📊 Gauge
        st.plotly_chart(show_gauge(risk), use_container_width=True)

        # 🧾 Cards
        col1, col2 = st.columns(2)

        # Reasons
        with col1:
            st.markdown("### 🔍 Reasons")
            for r in reasons:
                st.markdown(f'<div class="card">• {r}</div>', unsafe_allow_html=True)

        # Suggestions
        with col2:
            st.markdown("### 💡 Suggestions")
            for s in suggestions:
                st.markdown(f'<div class="card">• {s}</div>', unsafe_allow_html=True)

        # Disclaimer
        st.markdown("---")
        st.info(f"⚠️ {disclaimer}")

    except Exception as e:
        st.error(f"Error: {e}")
        st.markdown("---")
    st.markdown(
       "<center>Built with ❤️ using ML + FastAPI + Streamlit</center>",
         unsafe_allow_html=True
    )