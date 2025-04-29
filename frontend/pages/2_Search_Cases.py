import streamlit as st
import requests

from sidebar import apply_sidebar_style 

API_BASE_URL = "http://127.0.0.1:8000"

# Apply the sidebar styling
apply_sidebar_style()

st.title("🔍 Search Cases")

query = st.text_input("Enter a legal case query:", placeholder="E.g. Self-defense claim in an assault case")

if st.button("Search"):
    if query:
        with st.spinner("Searching for similar cases..."):
            response = requests.get(f"{API_BASE_URL}/search/", params={"query": query})
            if response.status_code == 200:
                cases = response.json()["cases"]
                if cases:
                    st.session_state["cases"] = cases  # Save cases
                    st.success("Cases found! Go to 'Case Details' to view.")
                else:
                    st.warning("No similar cases found.")
            else:
                st.error("Error fetching cases.")
