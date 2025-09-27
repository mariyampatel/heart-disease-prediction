import streamlit as st
import pickle
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# The scaler expects only 8 features
SCALER_FEATURES = ['Age', 'Sex', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'ExerciseAngina', 'Oldpeak']

# Load the saved machine learning pipeline components
@st.cache_resource
def load_model():
    """Loads the model and scaler components from the pickled file."""
    try:
        with open('model/heart_model_pipeline_v2.pkl', 'rb') as file:
            pipeline_components = pickle.load(file)
        return pipeline_components['model'], pipeline_components['scaler']
    except FileNotFoundError:
        st.error("❌ Model file not found. Please ensure 'heart_model_pipeline_v2.pkl' is in the 'model' directory.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Model loading error: {e}")
        st.stop()

model, scaler = load_model()

def normalize_column_names(df):
    """Normalize column names to handle different variations"""
    df_normalized = df.copy()
    if 'ChestPainType' in df_normalized.columns and 'ChestPain' not in df_normalized.columns:
        df_normalized['ChestPain'] = df_normalized['ChestPainType']
        df_normalized = df_normalized.drop('ChestPainType', axis=1)
    return df_normalized

def prepare_features_for_scaler(df):
    """Prepare only the 8 features that scaler expects"""
    df_copy = normalize_column_names(df)
    
    if 'Sex' in df_copy.columns:
        df_copy['Sex'] = df_copy['Sex'].astype(str).str.upper().map({'M': 1, 'F': 0}).fillna(df_copy['Sex'])
        df_copy['Sex'] = pd.to_numeric(df_copy['Sex'], errors='coerce').fillna(0).astype(int)
    
    if 'ExerciseAngina' in df_copy.columns:
        df_copy['ExerciseAngina'] = df_copy['ExerciseAngina'].astype(str).str.upper().map({'Y': 1, 'N': 0}).fillna(df_copy['ExerciseAngina'])
        df_copy['ExerciseAngina'] = pd.to_numeric(df_copy['ExerciseAngina'], errors='coerce').fillna(0).astype(int)

    return df_copy[SCALER_FEATURES]

def prepare_features_for_model(df):
    """Prepare all 18 features that model expects"""
    df_copy = normalize_column_names(df)
    
    if 'Sex' in df_copy.columns:
        df_copy['Sex'] = df_copy['Sex'].astype(str).str.upper().map({'M': 1, 'F': 0}).fillna(df_copy['Sex'])
        df_copy['Sex'] = pd.to_numeric(df_copy['Sex'], errors='coerce').fillna(0).astype(int)
    
    if 'ChestPain' in df_copy.columns:
        chest_pain_dummies = pd.get_dummies(df_copy['ChestPain'], prefix='ChestPain')
        df_copy = pd.concat([df_copy, chest_pain_dummies], axis=1)
        df_copy = df_copy.drop('ChestPain', axis=1)
    
    for cp_type in ['ChestPain_ATA', 'ChestPain_ASY', 'ChestPain_NAP', 'ChestPain_TA']:
        if cp_type not in df_copy.columns:
            df_copy[cp_type] = 0
    
    if 'RestingECG' in df_copy.columns:
        resting_ecg_dummies = pd.get_dummies(df_copy['RestingECG'], prefix='RestingECG')
        df_copy = pd.concat([df_copy, resting_ecg_dummies], axis=1)
        df_copy = df_copy.drop('RestingECG', axis=1)
    
    for ecg_type in ['RestingECG_LVH', 'RestingECG_Normal', 'RestingECG_ST']:
        if ecg_type not in df_copy.columns:
            df_copy[ecg_type] = 0
    
    if 'ExerciseAngina' in df_copy.columns:
        df_copy['ExerciseAngina'] = df_copy['ExerciseAngina'].astype(str).str.upper().map({'Y': 1, 'N': 0}).fillna(df_copy['ExerciseAngina'])
        df_copy['ExerciseAngina'] = pd.to_numeric(df_copy['ExerciseAngina'], errors='coerce').fillna(0).astype(int)
    
    if 'ST_Slope' in df_copy.columns:
        st_slope_dummies = pd.get_dummies(df_copy['ST_Slope'], prefix='ST_Slope')
        df_copy = pd.concat([df_copy, st_slope_dummies], axis=1)
        df_copy = df_copy.drop('ST_Slope', axis=1)
    
    for slope_type in ['ST_Slope_Down', 'ST_Slope_Flat', 'ST_Slope_Up']:
        if slope_type not in df_copy.columns:
            df_copy[slope_type] = 0
    
    model_features = [
        'Age', 'Sex', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'Oldpeak',
        'ChestPain_ATA', 'ChestPain_ASY', 'ChestPain_NAP', 'ChestPain_TA',
        'RestingECG_LVH', 'RestingECG_Normal', 'RestingECG_ST',
        'ExerciseAngina', 'ST_Slope_Down', 'ST_Slope_Flat', 'ST_Slope_Up'
    ]
    
    for col in model_features:
        if col not in df_copy.columns:
            df_copy[col] = 0
    
    return df_copy[model_features]

def make_prediction(input_df):
    """Make predictions with correct feature handling"""
    try:
        scaler_data = prepare_features_for_scaler(input_df)
        scaled_data = scaler.transform(scaler_data)
        
        model_data = prepare_features_for_model(input_df)
        final_features = model_data.values.copy()
        final_features[:, :8] = scaled_data
        
        predictions = model.predict(final_features)
        probabilities = model.predict_proba(final_features)
        
        return predictions, probabilities
        
    except Exception as e:
        st.error(f"❌ Prediction error: {e}")
        return None, None

def get_risk_interpretation(risk_prob):
    """Get risk interpretation based on probability"""
    if risk_prob >= 0.8:
        return "🔴 VERY HIGH RISK", "Immediate medical attention recommended"
    elif risk_prob >= 0.6:
        return "🟠 HIGH RISK", "Consult cardiologist soon"
    elif risk_prob >= 0.4:
        return "🟡 MODERATE RISK", "Regular monitoring advised"
    elif risk_prob >= 0.2:
        return "🟢 LOW RISK", "Maintain healthy lifestyle"
    else:
        return "✅ VERY LOW RISK", "Continue current health practices"

def app():
    st.markdown('<h2 class="sub-header">🩺 Individual Patient Assessment</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">📝 Patient Information</div>', unsafe_allow_html=True)
    
    with st.form("manual_prediction_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("👤 Demographics**")
            age = st.number_input("🎂 Age (years)", min_value=1, max_value=120, value=50, help="Patient's age in years")
            sex = st.selectbox("⚥ Gender", options=['M', 'F'], 
                              format_func=lambda x: "👨 Male" if x == 'M' else "👩 Female")
            
            st.markdown("💓 Cardiovascular**")
            resting_bp = st.number_input("🩸 Resting BP (mmHg)", min_value=80, max_value=200, value=120,
                                        help="Resting blood pressure in mmHg")
            cholesterol = st.number_input("🧪 Cholesterol (mg/dl)", min_value=0, max_value=600, value=200,
                                         help="Serum cholesterol level")
        
        with col2:
            st.markdown("🔬 Clinical Tests**")
            fasting_bs = st.selectbox("🍽 Fasting Blood Sugar > 120 mg/dl", options=[0, 1], 
                                     format_func=lambda x: "✅ Yes" if x == 1 else "❌ No")
            max_hr = st.number_input("❤ Max Heart Rate (bpm)", min_value=60, max_value=220, value=150,
                                    help="Maximum heart rate achieved during exercise")
            
            st.markdown("🏃 Exercise Response**")
            exercise_angina = st.selectbox("💔 Exercise Induced Angina", options=['Y', 'N'], 
                                          format_func=lambda x: "✅ Yes" if x == 'Y' else "❌ No")
            oldpeak = st.number_input("📉 ST Depression (Oldpeak)", min_value=0.0, max_value=10.0, value=1.0, step=0.1,
                                     help="ST depression induced by exercise")
        
        with col3:
            st.markdown("📋 Clinical Categories**")
            chest_pain_options = {
                'ATA': '⚡ Atypical Angina',
                'NAP': '🔸 Non-Anginal Pain', 
                'ASY': '🔹 Asymptomatic',
                'TA': '💔 Typical Angina'
            }
            chest_pain = st.selectbox("💔 Chest Pain Type", 
                                     options=list(chest_pain_options.keys()),
                                     format_func=lambda x: chest_pain_options[x])
            
            ecg_options = {
                'Normal': '✅ Normal',
                'ST': '📈 ST-T Wave Abnormality',
                'LVH': '🫀 Left Ventricular Hypertrophy'
            }
            resting_ecg = st.selectbox("📊 Resting ECG", 
                                      options=list(ecg_options.keys()),
                                      format_func=lambda x: ecg_options[x])
            
            slope_options = {
                'Up': '📈 Upsloping',
                'Flat': '➡ Flat',
                'Down': '📉 Downsloping'
            }
            st_slope = st.selectbox("📈 ST Slope", 
                                   options=list(slope_options.keys()),
                                   format_func=lambda x: slope_options[x])
    
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("🔍 Analyze Risk Profile", use_container_width=True, type="primary")

    if submitted:
        input_data = pd.DataFrame({
            'Age': [age], 'Sex': [sex], 'ChestPain': [chest_pain], 'RestingBP': [resting_bp],
            'Cholesterol': [cholesterol], 'FastingBS': [fasting_bs], 'RestingECG': [resting_ecg],
            'MaxHR': [max_hr], 'ExerciseAngina': [exercise_angina], 'Oldpeak': [oldpeak], 'ST_Slope': [st_slope]
        })
        
        prediction, prediction_proba = make_prediction(input_data)
        
        if prediction is not None:
            result = {
                'prediction': prediction[0],
                'prob_disease': prediction_proba[0][1],
                'prob_healthy': prediction_proba[0][0],
                'risk_percentage': prediction_proba[0][1] * 100
            }
            
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            
            risk_level, recommendation = get_risk_interpretation(result['prob_disease'])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                risk_color = "background-color: #e74c3c;" if result['prediction'] == 1 else "background-color: #27ae60;"
                st.markdown(f"""
                <div class="metric-card" style="{risk_color}">
                    <h3>{risk_level.split()[1]} {risk_level.split()[2]}</h3>
                    <p>Risk Assessment</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card" style="background-color: #e67e22;">
                    <h3>{result['risk_percentage']:.1f}%</h3>
                    <p>Disease Probability</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card" style="background-color: #3498db;">
                    <h3>{(1-result['prob_disease'])*100:.1f}%</h3>
                    <p>Healthy Probability</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### 📋 Clinical Interpretation")
            
            if result['prob_disease'] >= 0.6:
                st.markdown(f"""
                <div class="warning-box">
                    <h4>{risk_level}</h4>
                    <p><strong>Recommendation:</strong> {recommendation}</p>
                    <p><strong>Next Steps:</strong> Comprehensive cardiovascular evaluation recommended. 
                    Consider additional diagnostic tests such as stress testing, echocardiogram, or coronary angiography.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="success-box">
                    <h4>{risk_level}</h4>
                    <p><strong>Recommendation:</strong> {recommendation}</p>
                    <p><strong>Next Steps:</strong> Continue regular health maintenance. 
                    Monitor cardiovascular risk factors and maintain healthy lifestyle practices.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
