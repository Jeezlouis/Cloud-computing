import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from predict import StudentPerformancePredictor

st.set_page_config(page_title="AI-Powered Student Performance", page_icon="🎓", layout="wide")

# Load model predictor
predictor = StudentPerformancePredictor()

# Sidebar Info
with st.sidebar:
    st.title("📘 About")
    st.markdown("""
    This AI-driven app helps **predict student exam performance** using academic and motivational factors.
    It also provides **personalized recommendations** for at-risk students.
    """)
    st.markdown("[View GitHub Repo](https://github.com/yourusername/yourrepo)")
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942909.png", width=150)

# Header Section
st.image(
    "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1170&q=80",
    use_column_width=True
)
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🎓 AI-Powered Student Performance Monitor</h1>
    <p style='text-align: center; font-size: 18px;'>Leverage Machine Learning to track student progress and predict success.</p>
""", unsafe_allow_html=True)

# Input Form
st.header("📥 Input Student Data")
with st.form("student_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Academic")
        hours = st.slider("Hours Studied", 0, 40, 20)
        attendance = st.slider("Attendance (%)", 0.0, 1.0, 0.9)
        previous = st.slider("Previous Scores", 0, 100, 75)
    
    with col2:
        st.subheader("💡 Motivation & Resources")
        motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
        tutoring = st.number_input("Tutoring Sessions", 0, 10, 2)
        parental = st.selectbox("Parental Involvement", ["Low", "Medium", "High"])
        resources = st.selectbox("Access to Resources", ["Low", "Medium", "High"])

    submitted = st.form_submit_button("🚀 Predict")

# Prediction Output
if submitted:
    input_data = {
        "Hours_Studied": hours,
        "Attendance": attendance,
        "Previous_Scores": previous,
        "Motivation_Level": motivation,
        "Tutoring_Sessions": tutoring,
        "Parental_Involvement": parental,
        "Access_to_Resources": resources
    }

    result = predictor.predict([input_data])[0]
    score = round(result["predicted_exam_score"], 2)

    st.markdown("---")
    st.subheader("📊 Prediction Summary")
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric("🎯 Predicted Exam Score", f"{score}")
        if result["at_risk"]:
            st.error("⚠️ At Risk of Underperforming")
        else:
            st.success("✅ Performing Well")
        st.markdown("### 💬 Recommendation")
        st.info(result["recommendation"])

    with col2:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            title={'text': "Predicted Score"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "#4CAF50"},
                   'steps': [
                       {'range': [0, 40], 'color': "#ffcccc"},
                       {'range': [40, 70], 'color': "#ffe599"},
                       {'range': [70, 100], 'color': "#d9ead3"}]},
        ))
        st.plotly_chart(fig, use_container_width=True)

    # Contribution Bar Chart
    st.subheader("📈 Feature Contributions (Input Snapshot)")
    display_df = pd.DataFrame({
        "Feature": ["Hours Studied", "Attendance", "Previous Score", "Tutoring"],
        "Value": [hours, attendance * 100, previous, tutoring]
    })
    bar = px.bar(display_df, x="Feature", y="Value", color="Feature", text="Value",
                 color_discrete_sequence=px.colors.qualitative.Vivid)
    bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    bar.update_layout(showlegend=False, yaxis=dict(title="Value"))
    st.plotly_chart(bar, use_container_width=True)

# Footer
st.markdown("""
    <hr>
    <div style='text-align: center; color: gray; font-size: 14px;'>
        🚀 Built with Streamlit · © 2025 Student AI Performance · All rights reserved.
    </div>
""", unsafe_allow_html=True)
