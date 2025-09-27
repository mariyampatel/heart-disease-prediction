import streamlit as st

def app():
    st.markdown('<h2 class="sub-header">🏥 Welcome to Heart Disease Prediction System</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h3>🔬 Advanced Cardiovascular Risk Assessment</h3>
            <p>CardioPredict is a state-of-the-art AI system designed to assist healthcare professionals 
            in rapid cardiovascular risk evaluation. Our machine learning model analyzes 18 key health 
            parameters to provide accurate risk predictions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="success-box">
            <h4>✨ Key Features</h4>
            <ul>
                <li><strong>Individual Assessment:</strong> Real-time analysis of patient data</li>
                <li><strong>Batch Processing:</strong> Analyze multiple patients simultaneously</li>
                <li><strong>Visual Analytics:</strong> Comprehensive charts and insights</li>
                <li><strong>Risk Stratification:</strong> Clear risk categories and recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>92.3%</h3>
            <p>Model Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h3>918</h3>
            <p>Training Records</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h3>18</h3>
            <p>Clinical Parameters</p>
        </div>
        """, unsafe_allow_html=True)
