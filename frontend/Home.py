# C:\legal_ai\frontend\Home.py
import streamlit as st
from streamlit.components.v1 import html
from sidebar import apply_sidebar_style
from styles import apply_global_styles  # Import the shared styles

st.set_page_config(
    page_title="Legal Case Analysis",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Apply the shared styles and sidebar styling
apply_global_styles()  # Apply the CSS from styles.py
apply_sidebar_style()

# JavaScript to hide the Streamlit header and toolbar
html("""
    <script>
        function hideStreamlitHeader() {
            const header = document.querySelector('header');
            const toolbar = document.querySelector('[data-testid="stToolbar"]');
            const mainMenu = document.querySelector('#MainMenu');
            const decoration = document.querySelector('[data-testid="stDecoration"]');
            const statusWidget = document.querySelector('[data-testid="stStatusWidget"]');

            if (header) header.style.display = 'none';
            if (toolbar) toolbar.style.display = 'none';
            if (mainMenu) mainMenu.style.display = 'none';
            if (decoration) decoration.style.display = 'none';
            if (statusWidget) statusWidget.style.display = 'none';

            const appContainer = document.querySelector('.stApp');
            const appViewContainer = document.querySelector('[data-testid="stAppViewContainer"]');
            const blockContainer = document.querySelector('.block-container');

            if (appContainer) {
                appContainer.style.marginTop = '0px';
                appContainer.style.paddingTop = '0px';
            }
            if (appViewContainer) {
                appViewContainer.style.paddingTop = '0px';
                appViewContainer.style.marginTop = '0px';
            }
            if (blockContainer) {
                blockContainer.style.paddingTop = '0px';
                blockContainer.style.marginTop = '0px';
            }
        }

        window.addEventListener('load', hideStreamlitHeader);
        setTimeout(hideStreamlitHeader, 100);
        setTimeout(hideStreamlitHeader, 500);
    </script>
""")

# Main Content Container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Page Title
st.markdown("<h1 class='title'>⚖️ Legal Case Analysis System</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subheader'>AI-Powered Insights for Smarter Legal Decisions</h3>", unsafe_allow_html=True)

# Introduction Section
st.markdown('<div class="feature-box">', unsafe_allow_html=True)
st.markdown("""
Welcome to the **Legal Case Analysis System**, the ultimate AI-powered tool designed to revolutionize how legal professionals work. Built for **lawyers, researchers, and law students**, this cutting-edge platform harnesses advanced artificial intelligence to deliver **unparalleled insights**, **streamlined research**, and **data-driven decision-making**—all at your fingertips.

Imagine a tool that **instantly finds relevant case precedents**, **predicts case outcomes with precision**, and **breaks down complex legal arguments** into actionable insights. That’s exactly what we offer. Whether you’re preparing for trial, drafting a legal opinion, or studying landmark rulings, our system empowers you to:  
- **Save Time**: Cut hours of manual research with automated case analysis.  
- **Gain Clarity**: Understand judicial trends and argument strengths effortlessly.  
- **Boost Confidence**: Make informed decisions backed by AI-driven predictions.  

From **intuitive case searches** to **detailed breakdowns of court rulings**, the Legal Case Analysis System is your partner in navigating the complexities of law with speed, accuracy, and ease. Join the future of legal research today—where **technology meets justice**.
""")
st.markdown('</div>', unsafe_allow_html=True)

# Highlight Benefits
st.markdown('<div class="highlight">', unsafe_allow_html=True)
st.markdown("""
<div class="highlight-item">
    <h3>🔎 Precision Research</h3>
    <p>Find similar cases and precedents in seconds with AI-powered search.</p>
</div>
<div class="highlight-item">
    <h3>📊 Predictive Power</h3>
    <p>Forecast case outcomes with confidence using advanced analytics.</p>
</div>
<div class="highlight-item">
    <h3>⚖️ Strategic Insights</h3>
    <p>Analyze arguments and evidence to build stronger cases.</p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Close Main Container
st.markdown('</div>', unsafe_allow_html=True)