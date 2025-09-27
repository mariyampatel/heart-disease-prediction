import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# Import your helper functions from the 'manual.py' module
from pages.manual import make_prediction

def app():
    st.markdown('<h2 class="sub-header">📊 Bulk Patient Analysis</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-box">Upload a CSV file containing multiple patient records for batch processing and comprehensive analysis.</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📁 Upload Patient Dataset", type="csv", 
                                    help="Upload a CSV file with patient data following the required format")
    
    if uploaded_file:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown('<div class="section-header">📋 Dataset Preview</div>', unsafe_allow_html=True)
                st.dataframe(df_uploaded.head(10), use_container_width=True)
            
            with col2:
                st.markdown('<div class="section-header">📈 Dataset Statistics</div>', unsafe_allow_html=True)
                
                total_patients = len(df_uploaded)
                total_features = len(df_uploaded.columns)
                missing_data = df_uploaded.isnull().sum().sum()
                data_quality = (1 - missing_data/(total_patients * total_features)) * 100
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{total_patients}</h3>
                    <p>Total Patients</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{total_features}</h3>
                    <p>Features</p>
                </div>
                """, unsafe_allow_html=True)
                
                quality_class = "high-quality" if data_quality > 95 else "medium-quality" if data_quality > 85 else "low-quality"
                st.markdown(f"""
                <div class="metric-card">
                    <h3><span class="quality-indicator {quality_class}">{data_quality:.1f}%</span></h3>
                    <p>Data Quality</p>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("🔬 Generate Predictions for All Patients", use_container_width=True, type="primary"):
                with st.spinner("🔄 Processing patient data... This may take a moment."):
                    predictions, probabilities = make_prediction(df_uploaded)
                    
                    if predictions is not None:
                        df_uploaded['Prediction'] = predictions
                        df_uploaded['Risk_Probability'] = [p[1] for p in probabilities]
                        df_uploaded['Healthy_Probability'] = [p[0] for p in probabilities]
                        df_uploaded['Risk_Category'] = df_uploaded['Risk_Probability'].apply(
                            lambda x: 'Very High' if x > 0.8 else 'High' if x > 0.6 else 'Moderate' if x > 0.4 else 'Low' if x > 0.2 else 'Very Low'
                        )
                        df_uploaded['Risk_Level'] = df_uploaded['Prediction'].apply(
                            lambda x: 'High Risk' if x == 1 else 'Low Risk'
                        )
                        
                        st.session_state['df_results'] = df_uploaded
                        
                        st.markdown('<div class="section-header">📊 Analysis Summary</div>', unsafe_allow_html=True)
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            high_risk = sum(df_uploaded['Prediction'] == 1)
                            high_risk_pct = (high_risk/len(df_uploaded))*100
                            st.markdown(f"""
                            <div class="metric-card" style="background-color: #e74c3c">
                                <h3>{high_risk}</h3>
                                <p>High Risk ({high_risk_pct:.1f}%)</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            low_risk = sum(df_uploaded['Prediction'] == 0)
                            low_risk_pct = (low_risk/len(df_uploaded))*100
                            st.markdown(f"""
                            <div class="metric-card" style="background-color: #27ae60">
                                <h3>{low_risk}</h3>
                                <p>Low Risk ({low_risk_pct:.1f}%)</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            avg_risk = df_uploaded['Risk_Probability'].mean()
                            st.markdown(f"""
                            <div class="metric-card" style="background-color: #e67e22">
                                <h3>{avg_risk*100:.1f}%</h3>
                                <p>Average Risk</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col4:
                            max_risk = df_uploaded['Risk_Probability'].max()
                            st.markdown(f"""
                            <div class="metric-card" style="background-color: #9b59b6">
                                <h3>{max_risk*100:.1f}%</h3>
                                <p>Highest Risk</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        risk_counts = df_uploaded['Risk_Category'].value_counts()
                        colors = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c', '#8e44ad']
                        
                        wedges, texts, autotexts = ax.pie(risk_counts.values, labels=risk_counts.index, 
                                                         autopct='%1.1f%%', colors=colors, startangle=90,
                                                         explode=[0.05]*len(risk_counts), shadow=True)
                        ax.set_title('Risk Category Distribution', fontsize=16, fontweight='bold', pad=20)
                        
                        for autotext in autotexts:
                            autotext.set_color('white')
                            autotext.set_fontsize(12)
                            autotext.set_weight('bold')
                        
                        st.pyplot(fig)
                        plt.close()
                        
                        st.markdown('<div class="section-header">📋 Detailed Results</div>', unsafe_allow_html=True)
                        st.dataframe(df_uploaded, use_container_width=True)
                        
                        csv_data = df_uploaded.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="💾 Download Complete Analysis",
                            data=csv_data,
                            file_name=f'cardiopredict_analysis_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.csv',
                            mime='text/csv',
                            use_container_width=True
                        )
                    else:
                        st.error("❌ Error processing the dataset. Please check the data format.")
        
        except Exception as e:
            st.error(f"❌ Error reading the file: {str(e)}")
            st.info("💡 Please ensure your CSV file contains the required columns with proper formatting.")
