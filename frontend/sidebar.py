import streamlit as st

def apply_sidebar_style():
    st.markdown("""
        <style>
            /* Import Inter font for a professional look */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

            /* Sidebar Container */
            [data-testid="stSidebar"] {
                background: linear-gradient(135deg, #1f2a44, #4a5e8c); /* Professional dark blue gradient */
                color: #ffffff !important; /* White text for contrast */
                padding: 0 !important; /* Remove padding to avoid extra space */
                margin-top: 0 !important; /* Ensure no top margin */
                box-shadow: 2px 0 15px rgba(0, 0, 0, 0.2); /* Subtle shadow for depth */
                min-width: 260px; /* Slightly wider for a professional look */
            }

            /* Sidebar Navigation Header */
            [data-testid="stSidebarNav"]::before {
                content: "Navigation";
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; /* Modern, professional font */
                font-size: 22px;
                font-weight: 600;
                text-align: left;
                display: block;
                padding: 30px 20px 20px 20px; /* Increased padding for balance */
                color: #ffffff !important; /* White for visibility */
                border-bottom: 1px solid rgba(255, 255, 255, 0.15); /* Subtle divider */
                letter-spacing: 0.5px; /* Slight letter spacing for elegance */
                text-transform: uppercase; /* Uppercase for a formal look */
            }

            /* Sidebar Navigation Items - Base Styling */
            [data-testid="stSidebarNav"] a {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; /* Consistent professional font */
                color: #ffffff !important; /* Bright white for high visibility */
                font-size: 16px;
                font-weight: 500;
                padding: 14px 20px; /* Increased padding for better spacing */
                margin: 8px 10px; /* Increased margin for more spacing between items */
                transition: all 0.3s ease-in-out;
                border-radius: 6px; /* Slightly smaller radius for a refined look */
                display: flex;
                align-items: center;
                gap: 12px; /* Space for icons */
                border-left: 4px solid transparent; /* For active state indicator */
                line-height: 1.5; /* Better line height for readability */
            }

            /* More specific selectors to ensure text color applies */
            [data-testid="stSidebarNav"] div a,
            [data-testid="stSidebarNav"] div a span,
            [data-testid="stSidebarNav"] div a div {
                color: #ffffff !important; /* Force white text for nested elements */
            }

            /* Hover Effect */
            [data-testid="stSidebarNav"] a:hover {
                background-color: rgba(255, 255, 255, 0.15) !important; /* Slightly more visible background on hover */
                color: #ffffff !important; /* Ensure text stays bright white */
                border-left: 4px solid #ffffff; /* White border on hover */
                transform: translateX(3px); /* Subtle slide effect */
            }

            /* Ensure hover applies to nested elements */
            [data-testid="stSidebarNav"] div a:hover,
            [data-testid="stSidebarNav"] div a:hover span,
            [data-testid="stSidebarNav"] div a:hover div {
                color: #ffffff !important; /* Ensure text stays white on hover */
            }

            /* Active/Current Page */
            [data-testid="stSidebarNav"] a[aria-current="page"] {
                background-color: #60a5fa !important; /* Brighter blue for active state */
                color: #ffffff !important; /* White text for contrast */
                font-weight: 600;
                border-left: 4px solid #ffffff !important; /* White border for active state */
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15); /* Subtle shadow for active item */
                border-radius: 6px; /* Match the border radius for consistency */
            }

            /* More specific selectors for active state */
            [data-testid="stSidebarNav"] div a[aria-current="page"],
            [data-testid="stSidebarNav"] div a[aria-current="page"] span,
            [data-testid="stSidebarNav"] div a[aria-current="page"] div {
                background-color: #60a5fa !important;
                color: #ffffff !important;
            }

            /* Optional: Add icons before links */
            [data-testid="stSidebarNav"] a::before {
                content: "◉"; /* Subtle dot icon */
                font-size: 14px; /* Slightly larger for visibility */
                color: #ffffff !important; /* Match text color for visibility */
                opacity: 0.8; /* Slightly more visible */
            }

            /* Ensure no extra space from sidebar children */
            [data-testid="stSidebar"] > div {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
        </style>
    """, unsafe_allow_html=True)