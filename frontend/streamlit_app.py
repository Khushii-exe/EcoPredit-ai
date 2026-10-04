import os
from datetime import datetime

import requests
import streamlit as st

DEFAULT_API_URL = "https://ecopredit-ai.onrender.com"

st.set_page_config(
    page_title="EcoPredict AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f6f8f3 0%, #ffffff 45%, #f7faf7 100%);
    }
    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 2rem 2.2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #173f35 0%, #285d4d 55%, #3e7862 100%);
        color: white;
        margin-bottom: 1.4rem;
        box-shadow: 0 12px 35px rgba(23, 63, 53, .16);
    }
    .hero h1 {
        margin: 0;
        font-size: 2.7rem;
        letter-spacing: -0.04em;
    }
    .hero p {
        margin: .55rem 0 0;
        color: #e5f2eb;
        font-size: 1.08rem;
    }
    .pill {
        display: inline-block;
        padding: .35rem .7rem;
        border-radius: 999px;
        background: rgba(255,255,255,.14);
        color: #f2fff7;
        font-size: .82rem;
        margin-bottom: .8rem;
    }
    .section-title {
        font-size: 1.25rem;
        font-weight: 750;
        color: #173f35;
        margin: .4rem 0 .8rem;
    }
    .info-card {
        border: 1px solid #dce8df;
        background: white;
        border-radius: 18px;
        padding: 1rem 1.1rem;
        height: 100%;
        box-shadow: 0 5px 18px rgba(23,63,53,.05);
    }
    .info-card h4 {
        margin: 0 0 .35rem;
        color: #173f35;
    }
    .info-card p {
        margin: 0;
        color: #52655d;
        line-height: 1.5;
    }
    .result-card {
        border: 1px solid #d8e8dd;
        border-radius: 22px;
        padding: 1.35rem 1.45rem;
        background: white;
        box-shadow: 0 10px 30px rgba(23,63,53,.07);
    }
    .result-value {
        font-size: 2.65rem;
        font-weight: 800;
        color: #173f35;
        line-height: 1.1;
    }
    .result-unit {
        color: #687a72;
        font-size: .95rem;
    }
    .recommendation {
        margin-top: 1rem;
        padding: 1rem 1.1rem;
        border-radius: 15px;
        background: #eef7f1;
        border-left: 4px solid #3e7862;
        color: #29483e;
        line-height: 1.5;
    }
    .footer {
        text-align: center;
        color: #708078;
        font-size: .85rem;
        padding-top: 2rem;
    }
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #dce8df;
        padding: 1rem;
        border-radius: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

api_url = os.getenv("API_URL", DEFAULT_API_URL).rstrip("/")

st.markdown(
    """
    <div class="hero">
        <div class="pill">AI • CLOUD • SUSTAINABILITY</div>
        <h1>🌱 EcoPredict AI</h1>
        <p>Predict household appliance energy consumption and turn the prediction into a simple sustainability action.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# API status
try:
    health = requests.get(f"{api_url}/health", timeout=8)
    api_online = health.ok
except requests.RequestException:
    api_online = False

status_col, api_col = st.columns([1, 3])
with status_col:
    if api_online:
        st.success("● API Online")
    else:
        st.error("● API Unavailable")
with api_col:
    st.caption(f"Backend: {api_url}")

st.markdown('<div class="section-title">Prediction controls</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🌿 EcoPredict AI")
    st.caption("Configure the conditions used by the deployed ML model.")

    st.markdown("### Household & environment")
    lights = st.slider("Lighting load", 0.0, 100.0, 0.0, 0.5)
    t1 = st.number_input("Indoor temperature T1 (°C)", 10.0, 35.0, 19.7, 0.1)
    rh1 = st.number_input("Indoor humidity RH1 (%)", 10.0, 100.0, 45.59, 0.1)
    t_out = st.number_input("Outdoor temperature (°C)", -10.0, 45.0, 5.48, 0.1)
    rh_out = st.number_input("Outdoor humidity (%)", 0.0, 100.0, 90.17, 0.1)
    windspeed = st.number_input("Wind speed", 0.0, 30.0, 5.0, 0.1)

    st.markdown("### Time context")
    hour = st.slider("Hour of day", 0, 23, 10)
    day_of_week = st.selectbox(
        "Day of week",
        options=list(range(7)),
        format_func=lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][x],
        index=1,
    )
    month = st.slider("Month", 1, 12, 1)
    is_weekend = int(day_of_week >= 5)

    st.markdown("### Recent consumption")
    lag1 = st.number_input("Previous consumption (Wh)", 0.0, 1000.0, 260.0, 1.0)
    lag2 = st.number_input("Consumption 2 steps ago (Wh)", 0.0, 1000.0, 30.0, 1.0)
    lag3 = st.number_input("Consumption 3 steps ago (Wh)", 0.0, 1000.0, 40.0, 1.0)

    with st.expander("Advanced sensor inputs"):
        t2 = st.number_input("T2", -10.0, 45.0, 18.89, 0.01)
        rh2 = st.number_input("RH2", 0.0, 100.0, 44.23, 0.01)
        t3 = st.number_input("T3", -10.0, 45.0, 19.89, 0.01)
        rh3 = st.number_input("RH3", 0.0, 100.0, 44.90, 0.01)
        t4 = st.number_input("T4", -10.0, 45.0, 19.17, 0.01)
        rh4 = st.number_input("RH4", 0.0, 100.0, 45.03, 0.01)
        t5 = st.number_input("T5", -10.0, 45.0, 18.00, 0.01)
        rh5 = st.number_input("RH5", 0.0, 100.0, 49.66, 0.01)
        t6 = st.number_input("T6", -10.0, 45.0, 4.73, 0.01)
        rh6 = st.number_input("RH6", 0.0, 100.0, 96.47, 0.01)
        t7 = st.number_input("T7", -10.0, 45.0, 17.70, 0.01)
        rh7 = st.number_input("RH7", 0.0, 100.0, 41.59, 0.01)
        t8 = st.number_input("T8", -10.0, 45.0, 18.53, 0.01)
        rh8 = st.number_input("RH8", 0.0, 100.0, 49.40, 0.01)
        t9 = st.number_input("T9", -10.0, 45.0, 17.00, 0.01)
        rh9 = st.number_input("RH9", 0.0, 100.0, 45.73, 0.01)
        pressure = st.number_input("Pressure (mm Hg)", 650.0, 800.0, 742.88, 0.01)
        visibility = st.number_input("Visibility", 0.0, 100.0, 30.83, 0.01)
        dewpoint = st.number_input("Dew point", -20.0, 40.0, 3.95, 0.01)
        rv1 = st.number_input("Random variable 1", 0.0, 100.0, 49.63, 0.01)
        rv2 = st.number_input("Random variable 2", 0.0, 100.0, 49.63, 0.01)

    predict = st.button("⚡ Predict Energy", type="primary", use_container_width=True)

payload = {
    "lights": lights,
    "T1": t1, "RH_1": rh1,
    "T2": t2, "RH_2": rh2,
    "T3": t3, "RH_3": rh3,
    "T4": t4, "RH_4": rh4,
    "T5": t5, "RH_5": rh5,
    "T6": t6, "RH_6": rh6,
    "T7": t7, "RH_7": rh7,
    "T8": t8, "RH_8": rh8,
    "T9": t9, "RH_9": rh9,
    "T_out": t_out,
    "Press_mm_hg": pressure,
    "RH_out": rh_out,
    "Windspeed": windspeed,
    "Visibility": visibility,
    "Tdewpoint": dewpoint,
    "rv1": rv1, "rv2": rv2,
    "hour": hour,
    "day_of_week": day_of_week,
    "month": month,
    "is_weekend": is_weekend,
    "Appliances_lag_1": lag1,
    "Appliances_lag_2": lag2,
    "Appliances_lag_3": lag3,
    "Appliances_rolling_mean_3": (lag1 + lag2 + lag3) / 3.0,
}

left, right = st.columns([1.25, 1], gap="large")

with left:
    st.markdown(
        """
        <div class="info-card">
            <h4>What the model considers</h4>
            <p>Indoor and outdoor conditions, time context, lighting load, and the recent consumption pattern are passed to the trained Random Forest regression model.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="info-card">
            <h4>Cloud architecture</h4>
            <p>This dashboard calls the deployed FastAPI backend. The browser-facing UI contains no model logic—the prediction stays in the cloud API.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### Prediction result")

if predict:
    if not api_online:
        st.error("The FastAPI backend is currently unavailable. Wait a few seconds and try again.")
    else:
        try:
            with st.spinner("Running the cloud ML model..."):
                response = requests.post(
                    f"{api_url}/predict",
                    json=payload,
                    timeout=45,
                )
            if response.ok:
                result = response.json()
                prediction = float(result["predicted_energy_wh"])
                category = result["consumption_category"]
                recommendations = result.get("recommendations", [])

                c1, c2, c3 = st.columns(3)
                c1.metric("Predicted energy", f"{prediction:.2f} Wh")
                c2.metric("Consumption level", category)
                c3.metric("Weekend context", "Yes" if is_weekend else "No")

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-value">{prediction:.2f}</div>
                        <div class="result-unit">watt-hours predicted appliance consumption</div>
                        <div class="recommendation">
                            <strong>🌱 Recommendation</strong><br>
                            {" ".join(recommendations) if recommendations else "Maintain efficient energy usage."}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.progress(min(max(prediction / 300.0, 0.0), 1.0))
                st.caption("The progress indicator is a simple visual scale for the demo; the API category is based on the model's configured thresholds.")
                st.success(f"Cloud prediction completed at {datetime.now().strftime('%H:%M:%S')}.")
            else:
                st.error(f"API returned HTTP {response.status_code}: {response.text}")
        except requests.RequestException as exc:
            st.error(f"Could not reach the prediction API: {exc}")
else:
    st.info("Configure the inputs in the sidebar and click **Predict Energy** to run the deployed model.")

st.markdown(
    """
    <div class="footer">
        EcoPredict AI • ML + FastAPI + Docker + GitHub Actions + Render • AI for Sustainable Energy
    </div>
    """,
    unsafe_allow_html=True,
)
