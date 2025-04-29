import streamlit as st
import requests
from sidebar import apply_sidebar_style

API_BASE_URL = "http://127.0.0.1:8000"
apply_sidebar_style()

# Custom CSS (No background, no white bars)
st.markdown("""
    <style>
        .input-section {
            padding: 20px 0;
            border-bottom: 1px solid #d1d5db;
            margin-bottom: 20px;
        }
        textarea { 
            border: 1px solid #d1d5db; 
            border-radius: 8px; 
            padding: 12px; 
            font-size: 16px; 
            width: 100%; 
            box-sizing: border-box; 
        }
        .predict-button {
            background: #1e3a8a;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            border: none;
            transition: background 0.3s;
        }
        .predict-button:hover { background: #3b82f6; }
        .result-section {
            padding: 20px 0;
            border-top: 1px solid #d1d5db;
        }
        h1 { color: #1e3a8a; font-weight: 700; }
        h3 { color: #1e3a8a; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>📊 Legal Case Prediction</h1>", unsafe_allow_html=True)

# Input
st.markdown('<div class="input-section">', unsafe_allow_html=True)
case_text = st.text_area("Enter legal case details:", placeholder="Type or paste case description here...", height=200)
st.markdown('</div>', unsafe_allow_html=True)

# Predict Button
if st.button("⚖️ Predict Outcome", key="predict"):
    if case_text.strip():
        with st.spinner("Analyzing case..."):
            response = requests.post(f"{API_BASE_URL}/predict/", json={"text": case_text})
            if response.status_code == 200:
                prediction = response.json()
                label = prediction["predicted_label"]
                confidence = prediction["confidence"]
                reasoning = prediction["reasoning"]

                st.markdown('<div class="result-section">', unsafe_allow_html=True)
                st.success("✅ Prediction Completed!")
                st.markdown(f"<h3>🔹 Predicted Outcome: {label}</h3>", unsafe_allow_html=True)
                st.progress(confidence)
                with st.expander("📜 Explanation of Prediction"):
                    st.markdown(f"<p style='font-size:16px;'>{reasoning}</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("❌ Error fetching prediction.")
    else:
        st.warning("⚠️ Please enter case details.")