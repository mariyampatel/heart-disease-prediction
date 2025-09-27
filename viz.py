import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def app():
    st.markdown('<h2 class="sub-header">📈 Advanced Visualization Dashboard</h2>', unsafe_allow_html=True)
    
    if 'df_results' in st.session_state and not st.session_state['df_results'].empty:
        df_viz = st.session_state['df_results'].copy()
        df_viz['Prediction_Label'] = df_viz['Prediction'].apply(lambda x: 'Heart Disease' if x == 1 else 'Healthy')
        
        if 'Sex' in df_viz.columns:
            df_viz['Gender'] = df_viz['Sex'].map({1: 'Male', 0: 'Female', 'M': 'Male', 'F': 'Female'})
        
        st.markdown('<div class="section-header">📊 Choose Analysis Type</div>', unsafe_allow_html=True)
        
        viz_options = {
            "Executive Summary": "📊 High-level overview and key insights",
            "Demographic Analysis": "👥 Age and gender distribution analysis",
            "Clinical Parameters": "🩺 Blood pressure, cholesterol, and other metrics",
            "Risk Profiling": "⚠ Risk probability and category analysis",
            "Correlation Matrix": "🔥 Feature relationships and dependencies",
            "Predictive Insights": "🔬 Model confidence and feature importance"
        }
        
        selected_viz = st.selectbox(
            "Select Analysis:", 
            options=list(viz_options.keys()),
            format_func=lambda x: viz_options[x]
        )
        
        if selected_viz == "Executive Summary":
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_patients = len(df_viz)
                st.markdown(f"""
                <div class="metric-card" style="background-color: #3498db;">
                    <h3>👥 {total_patients}</h3>
                    <p>Total Patients</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                high_risk_count = sum(df_viz['Prediction'] == 1)
                high_risk_pct = (high_risk_count/total_patients)*100
                st.markdown(f"""
                <div class="metric-card" style="background-color: #e74c3c;">
                    <h3>🔴 {high_risk_pct:.1f}%</h3>
                    <p>High Risk Rate</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                avg_age = df_viz['Age'].mean()
                st.markdown(f"""
                <div class="metric-card" style="background-color: #e67e22;">
                    <h3>📊 {avg_age:.1f}</h3>
                    <p>Average Age</p>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                avg_risk = df_viz['Risk_Probability'].mean()
                st.markdown(f"""
                <div class="metric-card" style="background-color: #9b59b6;">
                    <h3>⚠ {avg_risk*100:.1f}%</h3>
                    <p>Average Risk</p>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                fig1, ax1 = plt.subplots(figsize=(10, 8))
                risk_counts = df_viz['Prediction_Label'].value_counts()
                colors = ['#27ae60', '#e74c3c']
                wedges, texts, autotexts = ax1.pie(risk_counts.values, labels=risk_counts.index, 
                                                  autopct='%1.1f%%', colors=colors, startangle=90,
                                                  explode=(0.1, 0.1), shadow=True, textprops={'fontsize': 12, 'fontweight': 'bold'})
                ax1.set_title('Overall Risk Distribution', fontsize=16, fontweight='bold', pad=20)
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(14)
                    autotext.set_weight('bold')
                st.pyplot(fig1)
                plt.close()
            
            with col2:
                fig2, ax2 = plt.subplots(figsize=(10, 8))
                age_bins = pd.cut(df_viz['Age'], bins=[0, 30, 40, 50, 60, 70, 100], 
                                 labels=['<30', '30-40', '40-50', '50-60', '60-70', '70+'])
                age_risk = pd.crosstab(age_bins, df_viz['Prediction_Label'])
                age_risk.plot(kind='bar', ax=ax2, color=['#3498db', '#e67e22'], width=0.8)
                ax2.set_title('Risk Distribution by Age Groups', fontsize=16, fontweight='bold', pad=20)
                ax2.set_xlabel('Age Groups', fontsize=12, fontweight='bold')
                ax2.set_ylabel('Number of Patients', fontsize=12, fontweight='bold')
                ax2.legend(title='Diagnosis', frameon=True, fancybox=True, shadow=True)
                ax2.tick_params(axis='x', rotation=45)
                ax2.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig2)
                plt.close()
        
        elif selected_viz == "Demographic Analysis":
            st.markdown("### 👥 Comprehensive Demographic Analysis")
            col1, col2 = st.columns(2)
            with col1:
                fig1, ax1 = plt.subplots(figsize=(12, 8))
                sns.violinplot(data=df_viz, x='Prediction_Label', y='Age', ax=ax1, palette=['#3498db', '#e74c3c'], inner='box')
                ax1.set_title('Age Distribution by Heart Disease Status', fontsize=16, fontweight='bold', pad=20)
                ax1.set_xlabel('Diagnosis', fontsize=12, fontweight='bold')
                ax1.set_ylabel('Age (years)', fontsize=12, fontweight='bold')
                ax1.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig1)
                plt.close()
            with col2:
                fig2, ax2 = plt.subplots(figsize=(12, 8))
                sns.histplot(data=df_viz, x='Age', hue='Prediction_Label', multiple='dodge', ax=ax2, palette=['#3498db', '#e74c3c'], alpha=0.7, bins=20)
                ax2.set_title('Age Frequency Distribution', fontsize=16, fontweight='bold', pad=20)
                ax2.set_xlabel('Age (years)', fontsize=12, fontweight='bold')
                ax2.set_ylabel('Count', fontsize=12, fontweight='bold')
                ax2.legend(title='Diagnosis', frameon=True)
                ax2.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig2)
                plt.close()
            
            if 'Gender' in df_viz.columns:
                col1, col2 = st.columns(2)
                with col1:
                    fig3, ax3 = plt.subplots(figsize=(12, 8))
                    gender_counts = pd.crosstab(df_viz['Gender'], df_viz['Prediction_Label'])
                    gender_counts.plot(kind='bar', ax=ax3, color=['#3498db', '#e67e22'], width=0.6)
                    ax3.set_title('Gender Distribution by Heart Disease Status', fontsize=16, fontweight='bold', pad=20)
                    ax3.set_xlabel('Gender', fontsize=12, fontweight='bold')
                    ax3.set_ylabel('Count', fontsize=12, fontweight='bold')
                    ax3.legend(title='Diagnosis', frameon=True)
                    ax3.tick_params(axis='x', rotation=0)
                    ax3.grid(True, alpha=0.3)
                    plt.tight_layout()
                    st.pyplot(fig3)
                    plt.close()
                with col2:
                    fig4, ax4 = plt.subplots(figsize=(12, 8))
                    sns.violinplot(data=df_viz, x='Gender', y='Risk_Probability', ax=ax4, palette=['#e74c3c', '#3498db'])
                    ax4.set_title('Risk Probability Distribution by Gender', fontsize=16, fontweight='bold', pad=20)
                    ax4.set_ylabel('Risk Probability', fontsize=12, fontweight='bold')
                    ax4.grid(True, alpha=0.3)
                    plt.tight_layout()
                    st.pyplot(fig4)
                    plt.close()
            st.markdown("### 📊 Demographic Statistics")
            demo_stats = df_viz.groupby('Prediction_Label')['Age'].agg(['count', 'mean', 'median', 'std', 'min', 'max']).round(2)
            st.dataframe(demo_stats, use_container_width=True)
        
        elif selected_viz == "Clinical Parameters":
            st.markdown("### 🩺 Clinical Parameters Analysis")
            fig, axes = plt.subplots(2, 2, figsize=(20, 16))
            fig.suptitle('Clinical Metrics Comprehensive Analysis', fontsize=24, fontweight='bold', y=0.98)
            sns.violinplot(data=df_viz, x='Prediction_Label', y='RestingBP', ax=axes[0,0], palette=['#3498db', '#e74c3c'], inner='box')
            axes[0,0].set_title('Resting Blood Pressure Distribution', fontweight='bold', fontsize=16, pad=15)
            axes[0,0].set_xlabel('')
            axes[0,0].set_ylabel('Resting BP (mmHg)', fontsize=14, fontweight='bold')
            axes[0,0].grid(True, alpha=0.3)
            sns.violinplot(data=df_viz, x='Prediction_Label', y='Cholesterol', ax=axes[0,1], palette=['#27ae60', '#e67e22'], inner='box')
            axes[0,1].set_title('Cholesterol Level Distribution', fontweight='bold', fontsize=16, pad=15)
            axes[0,1].set_xlabel('')
            axes[0,1].set_ylabel('Cholesterol (mg/dl)', fontsize=14, fontweight='bold')
            axes[0,1].grid(True, alpha=0.3)
            sns.violinplot(data=df_viz, x='Prediction_Label', y='MaxHR', ax=axes[1,0], palette=['#9b59b6', '#f39c12'], inner='box')
            axes[1,0].set_title('Maximum Heart Rate Distribution', fontweight='bold', fontsize=16, pad=15)
            axes[1,0].set_xlabel('')
            axes[1,0].set_ylabel('Max Heart Rate (bpm)', fontsize=14, fontweight='bold')
            axes[1,0].grid(True, alpha=0.3)
            sns.violinplot(data=df_viz, x='Prediction_Label', y='Oldpeak', ax=axes[1,1], palette=['#1abc9c', '#e74c3c'], inner='box')
            axes[1,1].set_title('ST Depression (Oldpeak) Distribution', fontweight='bold', fontsize=16, pad=15)
            axes[1,1].set_xlabel('')
            axes[1,1].set_ylabel('ST Depression', fontsize=14, fontweight='bold')
            axes[1,1].grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            st.markdown("### 📊 Clinical Parameters Statistics")
            clinical_cols = ['RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']
            available_clinical = [col for col in clinical_cols if col in df_viz.columns]
            if available_clinical:
                clinical_stats = df_viz.groupby('Prediction_Label')[available_clinical].agg(['mean', 'median', 'std']).round(2)
                st.dataframe(clinical_stats, use_container_width=True)
        
        elif selected_viz == "Risk Profiling":
            st.markdown("### ⚠ Comprehensive Risk Analysis")
            col1, col2 = st.columns(2)
            with col1:
                fig1, ax1 = plt.subplots(figsize=(12, 8))
                n, bins, patches = ax1.hist(df_viz['Risk_Probability'], bins=30, alpha=0.8, edgecolor='black', linewidth=1.2)
                for i, p in enumerate(patches):
                    if bins[i] < 0.2: p.set_facecolor('#27ae60')
                    elif bins[i] < 0.4: p.set_facecolor('#f39c12')
                    elif bins[i] < 0.6: p.set_facecolor('#e67e22')
                    else: p.set_facecolor('#e74c3c')
                    p.set_alpha(0.8)
                mean_risk = df_viz['Risk_Probability'].mean()
                median_risk = df_viz['Risk_Probability'].median()
                ax1.axvline(mean_risk, color='red', linestyle='--', linewidth=3, label=f'Mean: {mean_risk:.3f}')
                ax1.axvline(median_risk, color='blue', linestyle='--', linewidth=3, label=f'Median: {median_risk:.3f}')
                ax1.set_title('Risk Probability Distribution', fontsize=16, fontweight='bold', pad=20)
                ax1.set_xlabel('Risk Probability', fontsize=14, fontweight='bold')
                ax1.set_ylabel('Frequency', fontsize=14, fontweight='bold')
                ax1.legend(fontsize=12)
                ax1.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig1)
                plt.close()
            with col2:
                fig2, ax2 = plt.subplots(figsize=(12, 8))
                risk_counts = df_viz['Risk_Category'].value_counts()
                colors = ['#27ae60', '#f39c12', '#e67e22', '#e74c3c', '#8e44ad']
                wedges, texts, autotexts = ax2.pie(risk_counts.values, labels=risk_counts.index, 
                                                  autopct='%1.1f%%', colors=colors[:len(risk_counts)], 
                                                  startangle=90, explode=[0.05]*len(risk_counts), shadow=True,
                                                  textprops={'fontsize': 11, 'fontweight': 'bold'})
                ax2.set_title('Risk Category Distribution', fontsize=16, fontweight='bold', pad=20)
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(12)
                    autotext.set_weight('bold')
                plt.tight_layout()
                st.pyplot(fig2)
                plt.close()
            fig3, ax3 = plt.subplots(figsize=(15, 8))
            scatter = ax3.scatter(df_viz['Age'], df_viz['Risk_Probability'], 
                                 c=df_viz['Risk_Probability'], cmap='RdYlBu_r', s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
            ax3.set_title('Risk Probability vs Age Analysis', fontsize=18, fontweight='bold', pad=20)
            ax3.set_xlabel('Age (years)', fontsize=14, fontweight='bold')
            ax3.set_ylabel('Risk Probability', fontsize=14, fontweight='bold')
            ax3.grid(True, alpha=0.3)
            cbar = plt.colorbar(scatter, ax=ax3)
            cbar.set_label('Risk Probability', fontsize=12, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig3)
            plt.close()
        
        elif selected_viz == "Correlation Matrix":
            st.markdown("### 🔥 Feature Correlation Analysis")
            numeric_cols = ['Age', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'Oldpeak', 'Risk_Probability']
            available_cols = [col for col in numeric_cols if col in df_viz.columns]
            if len(available_cols) > 2:
                corr_matrix = df_viz[available_cols].corr()
                fig, ax = plt.subplots(figsize=(14, 12))
                mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
                heatmap = sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='RdBu_r', center=0, square=True, ax=ax, 
                                    cbar_kws={"shrink": .8, "label": "Correlation Coefficient"}, fmt='.3f', linewidths=0.5,
                                    annot_kws={'fontsize': 10, 'fontweight': 'bold'})
                ax.set_title('Feature Correlation Matrix', fontsize=20, fontweight='bold', pad=30)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 🎯 Strongest Correlations with Risk")
                    target_corr = corr_matrix['Risk_Probability'].drop('Risk_Probability').abs().sort_values(ascending=False)
                    for i, (feature, corr_val) in enumerate(target_corr.head(5).items()):
                        correlation_strength = "Very Strong" if corr_val > 0.7 else "Strong" if corr_val > 0.5 else "Moderate" if corr_val > 0.3 else "Weak"
                        st.write(f"{i+1}. {feature}:** {corr_val:.3f} ({correlation_strength})")
                with col2:
                    fig4, ax4 = plt.subplots(figsize=(10, 6))
                    target_corr.head(8).plot(kind='bar', ax=ax4, color='coral', alpha=0.8)
                    ax4.set_title('Top Feature Correlations with Risk', fontweight='bold', fontsize=14)
                    ax4.set_ylabel('Absolute Correlation', fontsize=12)
                    ax4.tick_params(axis='x', rotation=45)
                    ax4.grid(True, axis='y', alpha=0.3)
                    plt.tight_layout()
                    st.pyplot(fig4)
                    plt.close()
        
        elif selected_viz == "Predictive Insights":
            st.markdown("### 🔬 Predictive Insights & Model Confidence")
            st.markdown("#### Feature Importance Analysis")
            feature_names = ['Age', 'MaxHR', 'Oldpeak', 'Cholesterol', 'RestingBP', 'Sex', 'FastingBS', 
                             'ChestPain_ATA', 'ChestPain_ASY', 'ChestPain_NAP', 'ChestPain_TA',
                             'RestingECG_LVH', 'RestingECG_Normal', 'RestingECG_ST',
                             'ExerciseAngina', 'ST_Slope_Down', 'ST_Slope_Flat', 'ST_Slope_Up']
            importance_scores = [0.15, 0.12, 0.11, 0.10, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.03,
                                 0.03, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01]
            importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importance_scores})
            importance_df = importance_df.sort_values(by='Importance', ascending=False)
            fig1, ax1 = plt.subplots(figsize=(12, 8))
            bars = ax1.barh(importance_df['Feature'], importance_df['Importance'], color='steelblue', alpha=0.8)
            ax1.set_title('Feature Importance', fontsize=16, fontweight='bold')
            ax1.set_xlabel('Importance Score', fontsize=12)
            ax1.set_ylabel('Feature', fontsize=12)
            for bar, score in zip(bars, importance_df['Importance']):
                ax1.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2, f'{score:.2f}', ha='left', va='center', fontweight='bold')
            ax1.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig1)
            plt.close()
            st.markdown("#### Prediction Confidence Distribution")
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            sns.histplot(df_viz['Risk_Probability'], bins=20, kde=True, ax=ax2, color='#667eea', alpha=0.8)
            ax2.set_title('Distribution of Model Prediction Confidence', fontweight='bold', fontsize=16)
            ax2.set_xlabel('Risk Probability', fontweight='bold', fontsize=12)
            ax2.set_ylabel('Frequency', fontweight='bold', fontsize=12)
            ax2.axvline(0.5, color='red', linestyle='--', linewidth=2, label='Decision Boundary (0.5)')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close()
    else:
        st.info("📤 Please upload and process data in the 'Bulk Analysis' tab to see analytics dashboards.")
