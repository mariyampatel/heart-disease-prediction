import streamlit as st
import warnings

warnings.filterwarnings('ignore')

# Import your page modules from the 'pages' directory
from pages import home, manual, bulk, viz

# --- Page Config and CSS ---
st.set_page_config(
    page_title="Heart Disease Prediction System",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aapka poora CSS code yahan paste karein
st.markdown("""
<style>
    /* ... (Your entire CSS code here) ... */
    @import url('https://fonts.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background-color: #e6f0ff;
        font-family: 'Inter', sans-serif;
        color: #2c3e50;
    }
    
    @keyframes heartbeat {
        0% { transform: scale(1); }
        25% { transform: scale(1.1); }
        50% { transform: scale(1.2); }
        75% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .heart {
        animation: heartbeat 2s infinite;
        color: #e74c3c;
        font-size: 4rem;
        display: inline-block;
        margin-right: 1rem;
        filter: drop-shadow(0 0 10px rgba(231, 76, 60, 0.5));
    }
    
    .main-header {
        font-size: 3.5rem;
        color: #0b1f3a;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .sub-header {
        font-size: 2rem;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        font-weight: 600;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
    }

    .metric-card {
        background: linear-gradient(135deg, #1f4068, #355685);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        text-align: center;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    .metric-card h3 {
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    .metric-card p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .info-box {
        background-color: #3572ad;
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: none;
    }
    .warning-box {
        background-color: #e74c3c;
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .success-box {
        background-color: #3498db;
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .css-1d391kg {
        background-color: #0d284a;
    }
    .css-1d391kg .css-1outpf7 {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stForm {
        background: rgba(255, 255, 255, 0.8);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .stButton>button {
        background: #3498db;
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        border-radius: 12px;
        padding: 12px 30px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        background: #2980b9;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: #3498db;
        color: white !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .stNumberInput input, .stSelectbox select {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }
    .section-header {
        background: #34495e;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .result-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .quality-indicator {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    .high-quality {
        background: #00b894;
        color: white;
    }
    .medium-quality {
        background: #fdcb6e;
        color: #2d3436;
    }
    .low-quality {
        background: #e17055;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- Main App Logic ---
st.markdown('<h1 class="main-header"><span class="heart">🫀</span> Heart Disease Prediction System</h1>', unsafe_allow_html=True)
st.markdown('<div class="info-box">🔬 Advanced AI-powered cardiovascular risk assessment and analysis system for healthcare professionals</div>', unsafe_allow_html=True)

# --- Sidebar Content ---
with st.sidebar:
    st.markdown('<div class="section-header">🏥 Model Information</div>', unsafe_allow_html=True)
    st.markdown("""
    *🤖 AI Model Details:*
    - *Algorithm:* Random Forest Classifier
    - *Features:* 18 clinical parameters
    - *Accuracy:* 92.3% on test data
    - *Training Data:* 918 patient records
    - *Status:* ✅ Active & Validated
    """)
    st.markdown('<div class="section-header">📋 Required Parameters</div>', unsafe_allow_html=True)
    st.markdown("""
    *Primary Metrics:*
    - Age, Gender, Blood Pressure
    - Cholesterol, Fasting Blood Sugar
    - Maximum Heart Rate, ST Depression
    
    *Clinical Categories:*
    - Chest Pain Type, Resting ECG
    - Exercise Angina, ST Slope
    """)
    st.markdown('<div class="section-header">⚕ Medical Disclaimer</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; font-size: 0.9rem;">
    This tool is for educational and screening purposes only. 
    Always consult qualified healthcare professionals for medical decisions.
    </div>
    """, unsafe_allow_html=True)

# Navigation using a dictionary to map tab names to page modules
PAGES = {
    "🏠 Home": home,
    "🩺 Manual Assessment": manual,
    "📊 Bulk Analysis": bulk,
    "📈 Visualization": viz
}

st.session_state.selected_tab = st.selectbox(
    "Navigation", 
    list(PAGES.keys()),
    label_visibility="collapsed"
)

# Render the selected page by calling its 'app' function
PAGES[st.session_state.selected_tab].app()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Heart Disease Prediction App v2.1</strong></p>
    <p>Professional AI-powered cardiovascular risk assessment tool</p>
    <p style='font-size: 12px; color: #999; margin-top: 10px;'>
        ⚠ This system is for educational and research purposes only. 
        Always consult healthcare professionals for medical decisions.
    </p>
</div>
""", unsafe_allow_html=True)
