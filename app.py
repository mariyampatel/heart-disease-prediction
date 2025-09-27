import streamlit as st
import warnings

warnings.filterwarnings('ignore')

# Import your page modules safely
import pages.home as home
import pages.manual as manual
import pages.bulk as bulk
import pages.viz as viz

# --- Page Config and CSS ---
st.set_page_config(
    page_title="Heart Disease Prediction System",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
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
    /* ... keep the rest of your CSS same ... */
</style>
""", unsafe_allow_html=True)

# --- Main App Layout ---
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

# --- Navigation ---
PAGES = {
    "🏠 Home": home,
    "🩺 Manual Assessment": manual,
    "📊 Bulk Analysis": bulk,
    "📈 Visualization": viz
}

selected_tab = st.selectbox(
    "Navigation", 
    list(PAGES.keys()),
    label_visibility="collapsed"
)

# Render the selected page
PAGES[selected_tab].app()

# --- Footer ---
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
