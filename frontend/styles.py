# C:\legal_ai\frontend\styles.py
import streamlit as st

def apply_global_styles():
    st.markdown("""
        <style>
            /* Hide Streamlit's default header and toolbar */
            header {display: none !important;}
            [data-testid="stHeader"] {display: none !important;}
            [data-testid="stToolbar"] {display: none !important;}
            #MainMenu {display: none !important;}
            [data-testid="stDecoration"] {display: none !important;}
            [data-testid="stStatusWidget"] {display: none !important;}

            /* Base App Styling */
            .stApp {
                margin: 0 !important;
                padding: 0 !important;
                background: linear-gradient(135deg, #f8f9fa, #e7eaf6);
                overflow-x: hidden !important;
            }

            /* Ensure Streamlit containers don’t interfere */
            [data-testid="stAppViewContainer"] {
                padding: 0 !important;
                margin: 0 !important;
                overflow-x: hidden !important;
            }
            .block-container {
                padding: 0 100px !important; /* Adds 100px gaps on left and right, 0 on top */
                margin: 0 !important;
                overflow-x: hidden !important;
            }

            /* Sidebar Styling to Prevent Pushing Content */
            [data-testid="stSidebar"] {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
            [data-testid="stSidebar"] > div {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }

            /* Main Content Container */
            .main-container {
                padding: 0 !important; /* Remove internal padding to avoid extra space */
                margin: 0 !important; /* Remove any margins */
                box-sizing: border-box;
            }

            /* Title Styling */
            .title {
                text-align: center;
                font-size: 50px;
                font-weight: bold;
                color: #113f67;
                margin: -100px 0 10px 0 !important; /* Increased negative top margin to pull the heading up further */
                padding: 0 !important; /* Remove any padding */
                animation: fadeIn 2s ease-in-out;
            }

            /* Subheader Styling */
            .subheader {
                text-align: center;
                font-size: 22px;
                color: #555;
                margin: 0 0 40px 0 !important; /* Remove top margin, keep bottom margin */
                padding: 0 !important; /* Remove any padding */
                animation: fadeIn 2.5s ease-in-out;
            }

            /* Feature Box */
            .feature-box {
                background: linear-gradient(135deg, #f8f9fa, #e7eaf6);
                padding: 20px;
                border-radius: 12px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
                animation: slideIn 1.5s ease-in-out;
            }

            /* Highlight Section */
            .highlight {
                display: flex;
                flex-direction: column; /* Stack items vertically */
                gap: 30px !important; /* Vertical gap between highlight-item boxes */
                margin-bottom: 40px;
            }
            .highlight-item {
                background: #ffffff;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                animation: bounceIn 2s ease-out;
                margin-bottom: 30px; /* Fallback for gap */
            }
            .highlight-item:last-child {
                margin-bottom: 0; /* Remove margin from the last item to avoid extra space */
            }
            .highlight-item:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
            }
            .highlight-item h3 {
                font-size: 20px;
                color: #113f67;
                margin-bottom: 10px;
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 10px;
            }
            .highlight-item p {
                font-size: 16px;
                color: #718096;
                margin: 0;
            }

            /* Animations */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes slideIn {
                from { opacity: 0; transform: translateX(-20px); }
                to { opacity: 1; transform: translateX(0); }
            }
            @keyframes bounceIn {
                0% { opacity: 0; transform: scale(0.9); }
                60% { opacity: 1; transform: scale(1.05); }
                100% { transform: scale(1); }
            }
        </style>
    """, unsafe_allow_html=True)