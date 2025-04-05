import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from predict import StudentPerformancePredictor

st.set_page_config(page_title="AI-Powered Student Performance", page_icon="🎓", layout="wide")

# Load predictor
predictor = StudentPerformancePredictor()

# Sidebar Info
with st.sidebar:
    st.title("📘 About")
    st.markdown("""
    This AI-driven app helps **predict student exam performance** using academic and motivational factors.
    It also provides **personalized recommendations** for at-risk students.
    """)
    st.markdown("[View GitHub Repo](https://github.com/Jeezlouis/Cloud-computing)")
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942909.png", width=150)
    st.markdown("---")
    st.markdown("**Legend (Heatmap):**")
    st.markdown("- 🔵 Strong Positive Correlation (+1)")
    st.markdown("- 🔴 Strong Negative Correlation (-1)")
    st.markdown("- ⚪ Weak/No Correlation (0)")

# Header Section
st.image(
    "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1170&q=80",
    use_column_width=True
)
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🎓 AI-Powered Student Performance Monitor</h1>
    <p style='text-align: center; font-size: 18px;'>Leverage Machine Learning to track student progress and predict success.</p>
""", unsafe_allow_html=True)

# ---------------------------
# 📥 Manual Input Section
# ---------------------------
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

# ----------------------------
# 📊 Manual Prediction Output
# ----------------------------
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

    with st.spinner("⏳ Making prediction..."):
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
            mode="gauge+number",
            value=score,
            title={'text': "Predicted Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#4CAF50"},
                'steps': [
                    {'range': [0, 40], 'color': "#ffcccc"},
                    {'range': [40, 70], 'color': "#ffe599"},
                    {'range': [70, 100], 'color': "#d9ead3"},
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': score
                }
            }
        ))
        fig.update_layout(transition_duration=500)
        st.plotly_chart(fig, use_container_width=True)

    # 📊 Feature Contribution
    st.subheader("📈 Feature Snapshot")
    display_df = pd.DataFrame({
        "Feature": ["Hours Studied", "Attendance (%)", "Previous Score", "Tutoring Sessions"],
        "Value": [hours, attendance * 100, previous, tutoring]
    })
    bar = px.bar(display_df, x="Feature", y="Value", color="Feature", text="Value",
                 color_discrete_sequence=px.colors.qualitative.Vivid)
    bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    bar.update_layout(showlegend=False, yaxis=dict(title="Value"))
    st.plotly_chart(bar, use_container_width=True)

# ----------------------------
# 📂 Batch Prediction Section
# ----------------------------
st.markdown("---")
st.header("📂 Upload CSV for Batch Prediction")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        with st.spinner("⏳ Running batch prediction..."):
            results = predictor.predict(df.to_dict(orient="records"))

        results_df = df.copy()
        results_df["Predicted_Score"] = [round(r["predicted_exam_score"], 2) for r in results]
        results_df["At_Risk"] = ["Yes" if r["at_risk"] else "No" for r in results]
        results_df["Recommendation"] = [r["recommendation"] for r in results]

        # Display table
        st.markdown("### 🔍 Batch Prediction Results")
        st.dataframe(results_df, use_container_width=True)

        # Downloadable CSV
        csv = results_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Results as CSV", csv, "predicted_results.csv", "text/csv")

        # 📊 Correlation Heatmap
        st.markdown("### 🧠 Feature Correlation Heatmap")
        numeric_cols = results_df.select_dtypes(include=["float64", "int64"])
        if "Predicted_Score" in numeric_cols.columns and len(numeric_cols.columns) > 1:
            corr = numeric_cols.corr()
            fig_heatmap = px.imshow(
                corr,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                aspect="auto",
                title="Correlation Matrix"
            )
            fig_heatmap.update_layout(margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.warning("⚠️ Not enough numeric data to generate correlation heatmap.")

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")

# ----------------------------
# Footer
# ----------------------------
st.markdown("""
    <hr>
    <div style='text-align: center; color: gray; font-size: 14px;'>
        🚀 Built with Streamlit · © 2025 Student AI Performance · All rights reserved.
    </div>
""", unsafe_allow_html=True)
