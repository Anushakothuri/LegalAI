import streamlit as st
import requests
from sidebar import apply_sidebar_style

API_BASE_URL = "http://127.0.0.1:8000"

apply_sidebar_style()

st.title("📊 Argument Strength Analysis")

st.markdown("### Evaluate Your Argument Strength")
st.markdown("Use 'Plaintiff:' or 'Defendant:' prefixes for separate scores, or enter arguments without prefixes for a general score.")
user_args = st.text_area(
    "Enter your case arguments:",
    placeholder="E.g. Plaintiff: The contract was breached due to non-payment.\nDefendant: Payment was delayed due to unforeseen circumstances.",
    height=150
)

if st.button("Calculate Your Argument Strength"):
    if user_args.strip():
        with st.spinner("Calculating score..."):
            response = requests.post(f"{API_BASE_URL}/score_arguments/", json={"arguments": user_args})
            if response.status_code == 200:
                scores = response.json()
                plaintiff_score = scores.get("plaintiff_score")
                defendant_score = scores.get("defendant_score")
                general_score = scores.get("general_score")
                details = scores.get("details", "No details provided.")

                if plaintiff_score is not None:
                    st.markdown(f"**Plaintiff Argument Strength**: {plaintiff_score:.2f}/100")
                if defendant_score is not None:
                    st.markdown(f"**Defendant Argument Strength**: {defendant_score:.2f}/100")
                if general_score is not None:
                    st.markdown(f"**General Argument Strength**: {general_score:.2f}/100")
                if plaintiff_score is None and defendant_score is None and general_score is None:
                    st.warning("⚠️ No valid arguments detected (check prefixes or content).")
                with st.expander("Details"):
                    st.markdown(details)
            else:
                st.error(f"❌ Error calculating score: {response.status_code} - {response.text}")
    else:
        st.warning("⚠️ Please enter some arguments.")

st.markdown("---")
st.markdown("### Note")
st.markdown("For detailed analysis of similar cases (including arguments, evidence, and outcomes), use the 'Case Details' page after searching.")