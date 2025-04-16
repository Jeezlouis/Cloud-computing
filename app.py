import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from predict import StudentPerformancePredictor

# Set page configuration with a custom theme
st.set_page_config(
    page_title="Student Performance Monitor", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary: #6C63FF;
        --secondary: #4CAF50;
        --accent: #FF6584;
        --background: #f8f9fa;
        --text: #333333;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: var(--primary);
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Card-like containers */
    .stCard {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Metric styling */
    .metric-container {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: var(--primary);
    }
    
    .metric-label {
        font-size: 14px;
        color: #666;
    }
    
    /* Form styling */
    .stSlider > div > div {
        background-color: transparent !important;
    }
    
    .stButton > button {
        background-color: var(--primary);
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #5952d9;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f1f3f9;
    }
    
    /* Status indicators */
    .status-success {
        background-color: #d9ead3;
        border-left: 5px solid var(--secondary);
        padding: 10px;
        border-radius: 5px;
    }
    
    .status-warning {
        background-color: #ffcccc;
        border-left: 5px solid #ff4d4d;
        padding: 10px;
        border-radius: 5px;
    }
    
    /* Recommendation box */
    .recommendation-box {
        background-color: #e8f4fd;
        border-left: 5px solid #4285F4;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #666;
        font-size: 14px;
        padding: 20px 0;
        border-top: 1px solid #eee;
        margin-top: 40px;
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .loading-animation {
        animation: pulse 1.5s infinite;
    }
</style>
""", unsafe_allow_html=True)

#To override all previous styling done
st.markdown("""
<style>
    /* Make all text black in all cards and sidebar */
    .stCard p, 
    .stCard li, 
    .stCard span, 
    .stCard h4, 
    .stCard div,
    [data-testid="stSidebar"] div,
    .css-1d391kg p,
    .css-1d391kg div {
        color: #000000 !important;
    }
    
    /* Target specifically the white background containers in sidebar */
    [data-testid="stSidebar"] div[style*="background-color: white"] p,
    [data-testid="stSidebar"] div[style*="background-color: white"] span {
        color: #000000 !important;
    }
    
    /* Remove purple color from academic factor headers */
    h3[style*="color: #6C63FF"] {
        color: #000000 !important;
    }
    
    /* Remove purple background from sliders */
    .stSlider > div > div {
        background-color: transparent !important; /* Change to gray or any other color */
    }
    
    /* Fix form element colors */
    .stSelectbox, .stSlider, .stNumberInput {
        color: #000000 !important;
    }
    
    /* Ensure all form labels are black */
    label, .stSlider > div, .stSelectbox > div {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)


# Load predictor
predictor = StudentPerformancePredictor()

# Sidebar with improved styling
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1501504905252-473c47e087f8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1074&q=80", use_container_width=True)
    
    st.markdown("<h2 style='text-align: center;'>📘 About</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);'>
        <p>This AI-driven app helps <strong>predict student exam performance</strong> using academic and motivational factors.</p>
        <p>It also provides <strong>personalized recommendations</strong> for at-risk students.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align: center; margin: 20px 0;'><a href='https://github.com/Jeezlouis/Cloud-computing' style='background-color: #333; color: white; padding: 8px 15px; border-radius: 5px; text-decoration: none;'><svg style='vertical-align: middle; margin-right: 5px;' xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'><path d='M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22'></path></svg> View GitHub Repo</a></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);'>
        <h4 style='margin-top: 0;'>📊 Heatmap Legend</h4>
        <div style='display: flex; align-items: center; margin-bottom: 5px;'>
            <div style='width: 15px; height: 15px; background-color: #4285F4; border-radius: 50%; margin-right: 10px;'></div>
            <span>Strong Positive Correlation (+1)</span>
        </div>
        <div style='display: flex; align-items: center; margin-bottom: 5px;'>
            <div style='width: 15px; height: 15px; background-color: #EA4335; border-radius: 50%; margin-right: 10px;'></div>
            <span>Strong Negative Correlation (-1)</span>
        </div>
        <div style='display: flex; align-items: center;'>
            <div style='width: 15px; height: 15px; background-color: #E8EAED; border-radius: 50%; margin-right: 10px;'></div>
            <span>Weak/No Correlation (0)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Header Section with animation
st.markdown("""
<div style="position: relative; overflow: hidden; border-radius: 10px; margin-bottom: 30px;">
    <img src="https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1170&q=80" style="width: 100%; height: 300px; object-fit: cover; filter: brightness(0.7);">
    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; width: 100%; padding: 0 20px;">
        <h1 style="color: white; font-size: 3rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); margin-bottom: 10px;">🎓 Student Performance Monitor</h1>
        <p style="color: white; font-size: 1.2rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">Leverage AI to track student progress and predict academic success</p>
        <div style="margin-top: 20px;">
            <span style="background-color: #6C63FF; color: white; padding: 8px 15px; border-radius: 20px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">AI-Powered</span>
            <span style="background-color: #4CAF50; color: white; padding: 8px 15px; border-radius: 20px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-left: 10px;">Data-Driven</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content with tabs
tab1, tab2 = st.tabs(["📊 Individual Prediction", "📈 Batch Analysis"])

with tab1:
    st.markdown("""
    <div class="stCard">
        <h2 style="margin-top: 0;">📥 Input Student Data</h2>
        <p style="color: #666;">Enter student information to predict their exam performance.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("student_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3 style='color: #6C63FF;'>📚 Academic Factors</h3>", unsafe_allow_html=True)
            hours = st.slider("Hours Studied Weekly", 0, 40, 20, help="Average number of hours spent studying per week")
            attendance = st.slider("Attendance Rate", 0.0, 1.0, 0.9, format="%.2f", help="Percentage of classes attended (0.9 = 90%)")
            previous = st.slider("Previous Exam Scores", 0, 100, 75, help="Average score from previous exams")

        with col2:
            st.markdown("<h3 style='color: #6C63FF;'>💡 Motivation & Support</h3>", unsafe_allow_html=True)
            motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"], help="Student's self-reported motivation level")
            tutoring = st.number_input("Tutoring Sessions Monthly", 0, 10, 2, help="Number of tutoring sessions attended per month")
            parental = st.selectbox("Parental Involvement", ["Low", "Medium", "High"], help="Level of parental involvement in student's education")
            resources = st.selectbox("Access to Resources", ["Low", "Medium", "High"], help="Access to educational resources (books, internet, etc.)")

        submitted = st.form_submit_button("🚀 Predict Performance")

    # Prediction Output with improved styling
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

        with st.spinner("⏳ Analyzing student data..."):
            result = predictor.predict([input_data])[0]

        score = round(result["predicted_exam_score"], 2)

        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("<h2 style='margin-top: 0;'>📊 Prediction Results</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])

        with col1:
            # Styled metric
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{score}</div>
                <div class="metric-label">Predicted Score</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Status indicator
            if result["at_risk"]:
                st.markdown("""
                <div class="status-warning">
                    <h4 style="margin-top: 0; color: #d32f2f;">⚠️ At Risk of Underperforming</h4>
                    <p style="margin-bottom: 0;">This student may need additional support.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="status-success">
                    <h4 style="margin-top: 0; color: #388e3c;">✅ Performing Well</h4>
                    <p style="margin-bottom: 0;">This student is on track for success.</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Recommendation box
            st.markdown(f"""
            <div class="recommendation-box">
                <h4 style="margin-top: 0;">💬 Personalized Recommendation</h4>
                <p style="margin-bottom: 0;">{result["recommendation"]}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Enhanced gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={'text': "Predicted Score", 'font': {'size': 24, 'color': '#6C63FF'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#6C63FF"},
                    'bar': {'color': "#6C63FF"},
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
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=50, b=20),
                paper_bgcolor='white',
                font={'color': "#333333", 'family': "Arial"}
            )
            st.plotly_chart(fig, use_container_width=True)

        # Feature contribution visualization
        st.markdown("<h3>📈 Key Factors Analysis</h3>", unsafe_allow_html=True)
        
        # Prepare data for visualization
        display_df = pd.DataFrame({
            "Factor": ["Hours Studied", "Attendance (%)", "Previous Score", "Tutoring Sessions"],
            "Value": [hours, attendance * 100, previous, tutoring],
            "Benchmark": [25, 85, 70, 3]  # Example benchmarks
        })
        
        # Create a more informative bar chart
        fig = go.Figure()
        
        # Add student values
        fig.add_trace(go.Bar(
            x=display_df["Factor"],
            y=display_df["Value"],
            name="Student",
            marker_color='#6C63FF',
            text=display_df["Value"],
            textposition='outside'
        ))
        
        # Add benchmark values
        fig.add_trace(go.Bar(
            x=display_df["Factor"],
            y=display_df["Benchmark"],
            name="Class Average",
            marker_color='rgba(108, 99, 255, 0.3)',
            text=display_df["Benchmark"],
            textposition='outside'
        ))
        
        fig.update_layout(
            barmode='group',
            title={
                'text': "Student Performance vs. Class Average",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 18, 'color': '#333333'}
            },
            xaxis_title="Factor",
            yaxis_title="Value",
            legend_title="Legend",
            template="plotly_white",
            height=400,
            margin=dict(l=20, r=20, t=80, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="stCard">
        <h2 style="margin-top: 0;">📂 Batch Analysis</h2>
        <p style="color: #666;">Upload a CSV file with multiple student records for batch prediction.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader with improved styling
    uploaded_file = st.file_uploader("Upload Student Data CSV", type=["csv"], 
                                    help="CSV should include columns: Hours_Studied, Attendance, Previous_Scores, Motivation_Level, Tutoring_Sessions, Parental_Involvement, Access_to_Resources")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Success message with animation
            st.markdown("""
            <div style="background-color: #d9ead3; border-radius: 5px; padding: 10px; display: flex; align-items: center; margin-bottom: 20px;">
                <div style="background-color: #4CAF50; border-radius: 50%; width: 30px; height: 30px; display: flex; justify-content: center; align-items: center; margin-right: 10px;">
                    <span style="color: white; font-weight: bold;">✓</span>
                </div>
                <div>
                    <h4 style="margin: 0; color: #388e3c;">File uploaded successfully!</h4>
                    <p style="margin: 0; font-size: 14px;">Processing {len(df)} student records...</p>
                </div>
            </div>
            """.format(len=len(df)), unsafe_allow_html=True)

            with st.spinner("⏳ Running batch prediction..."):
                results = predictor.predict(df.to_dict(orient="records"))

            results_df = df.copy()
            results_df["Predicted_Score"] = [round(r["predicted_exam_score"], 2) for r in results]
            results_df["At_Risk"] = ["Yes" if r["at_risk"] else "No" for r in results]
            results_df["Recommendation"] = [r["recommendation"] for r in results]

            # Summary statistics
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top: 0;'>📊 Class Overview</h3>", unsafe_allow_html=True)
            
            avg_score = results_df["Predicted_Score"].mean()
            at_risk_count = results_df["At_Risk"].value_counts().get("Yes", 0)
            at_risk_percent = (at_risk_count / len(results_df)) * 100
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-value">{avg_score:.1f}</div>
                    <div class="metric-label">Average Predicted Score</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-value">{at_risk_count}</div>
                    <div class="metric-label">Students At Risk</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-value">{at_risk_percent:.1f}%</div>
                    <div class="metric-label">Percentage At Risk</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)

            # Score distribution
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top: 0;'>📊 Score Distribution</h3>", unsafe_allow_html=True)
            
            fig = px.histogram(
                results_df, 
                x="Predicted_Score",
                nbins=20,
                color_discrete_sequence=['#6C63FF'],
                marginal="box",
                opacity=0.7,
                labels={"Predicted_Score": "Predicted Score"}
            )
            
            fig.update_layout(
                xaxis_title="Predicted Score",
                yaxis_title="Number of Students",
                template="plotly_white",
                height=400,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            
            # Add a vertical line for the average score
            fig.add_vline(x=avg_score, line_dash="dash", line_color="#FF6584", annotation_text=f"Avg: {avg_score:.1f}")
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Display table with improved styling
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top: 0;'>🔍 Detailed Results</h3>", unsafe_allow_html=True)
            
            # Add a search/filter option
            search = st.text_input("🔍 Search by any column", "")
            
            # Filter the dataframe if search term is provided
            if search:
                filtered_df = results_df[results_df.astype(str).apply(lambda row: row.str.contains(search, case=False).any(), axis=1)]
                st.dataframe(filtered_df, use_container_width=True, height=400)
                st.markdown(f"<p style='color: #666; font-size: 14px;'>Showing {len(filtered_df)} of {len(results_df)} records</p>", unsafe_allow_html=True)
            else:
                st.dataframe(results_df, use_container_width=True, height=400)
            
            # Downloadable CSV with styled button
            csv = results_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Complete Results",
                data=csv,
                file_name="student_predictions.csv",
                mime="text/csv",
                help="Download the complete prediction results as a CSV file"
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # Correlation Heatmap with improved styling
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top: 0;'>🧠 Factor Correlation Analysis</h3>", unsafe_allow_html=True)
            
            numeric_cols = results_df.select_dtypes(include=["float64", "int64"])
            if "Predicted_Score" in numeric_cols.columns and len(numeric_cols.columns) > 1:
                corr = numeric_cols.corr()
                
                fig_heatmap = px.imshow(
                    corr,
                    text_auto=True,
                    color_continuous_scale='RdBu_r',
                    aspect="auto",
                    labels={"color": "Correlation"}
                )
                
                fig_heatmap.update_layout(
                    height=500,
                    margin=dict(l=20, r=20, t=20, b=20),
                    coloraxis_colorbar=dict(
                        title="Correlation",
                        thicknessmode="pixels", thickness=20,
                        lenmode="pixels", len=300,
                        tickvals=[-1, 0, 1],
                        ticktext=["Negative", "Neutral", "Positive"]
                    )
                )
                
                st.plotly_chart(fig_heatmap, use_container_width=True)
                
                # Add explanation
                st.markdown("""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 10px;">
                    <h4 style="margin-top: 0; color: #6C63FF;">📝 Interpretation Guide</h4>
                    <p>This heatmap shows how different factors correlate with predicted scores:</p>
                    <ul>
                        <li><strong>Positive values (blue):</strong> As one factor increases, the other tends to increase as well.</li>
                        <li><strong>Negative values (red):</strong> As one factor increases, the other tends to decrease.</li>
                        <li><strong>Values close to 0 (white):</strong> Little to no relationship between factors.</li>
                    </ul>
                    <p>Focus on factors with strong correlations to predicted scores to improve student performance.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Not enough numeric data to generate correlation heatmap.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # At-risk students analysis
            if at_risk_count > 0:
                st.markdown("<div class='stCard'>", unsafe_allow_html=True)
                st.markdown("<h3 style='margin-top: 0;'>⚠️ At-Risk Students Analysis</h3>", unsafe_allow_html=True)
                
                at_risk_df = results_df[results_df["At_Risk"] == "Yes"]
                
                # Common factors visualization
                factors = ["Hours_Studied", "Attendance", "Previous_Scores", "Tutoring_Sessions"]
                factor_avgs = {
                    "Factor": [],
                    "At-Risk Average": [],
                    "Class Average": []
                }
                
                for factor in factors:
                    if factor in at_risk_df.columns:
                        factor_avgs["Factor"].append(factor.replace("_", " "))
                        factor_avgs["At-Risk Average"].append(at_risk_df[factor].mean())
                        factor_avgs["Class Average"].append(results_df[factor].mean())
                
                factor_df = pd.DataFrame(factor_avgs)
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=factor_df["Factor"],
                    y=factor_df["At-Risk Average"],
                    name="At-Risk Students",
                    marker_color='#FF6584',
                    text=[f"{x:.2f}" for x in factor_df["At-Risk Average"]],
                    textposition='outside'
                ))
                
                fig.add_trace(go.Bar(
                    x=factor_df["Factor"],
                    y=factor_df["Class Average"],
                    name="Class Average",
                    marker_color='#6C63FF',
                    text=[f"{x:.2f}" for x in factor_df["Class Average"]],
                    textposition='outside'
                ))
                
                fig.update_layout(
                    barmode='group',
                    title="At-Risk Students vs. Class Average",
                    xaxis_title="Factor",
                    yaxis_title="Average Value",
                    template="plotly_white",
                    height=400,
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Recommendations summary
                st.markdown("<h4>📋 Common Recommendations</h4>", unsafe_allow_html=True)
                
                # Extract common phrases from recommendations
                from collections import Counter
                import re
                
                all_recommendations = " ".join(at_risk_df["Recommendation"].tolist())
                words = re.findall(r'\b\w+\b', all_recommendations.lower())
                common_words = Counter(words).most_common(20)
                
                # Filter out common stop words
                stop_words = ["the", "to", "and", "a", "of", "for", "in", "is", "that", "with", "be", "on", "are", "this", "as", "an"]
                filtered_words = [(word, count) for word, count in common_words if word not in stop_words and len(word) > 3]
                
                # Create word cloud-like visualization
                word_df = pd.DataFrame(filtered_words[:10], columns=["Word", "Count"])
                
                fig = px.bar(
                      columns=["Word", "Count"])
                
                fig = px.bar(
                    word_df,
                    x="Word",
                    y="Count",
                    color="Count",
                    color_continuous_scale="Viridis",
                    labels={"Count": "Frequency"},
                    text="Count"
                )
                
                fig.update_layout(
                    title="Common Terms in Recommendations",
                    xaxis_title="",
                    yaxis_title="Frequency",
                    template="plotly_white",
                    height=350,
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"""
            <div style="display: flex; align-items: center;">
                <div style="background-color: #d32f2f; border-radius: 50%; width: 30px; height: 30px; display: flex; justify-content: center; align-items: center; margin-right: 10px;">
                    <span style="color: white; font-weight: bold;">!</span>
                </div>
                <div>
                    <h4 style="margin: 0; color: #d32f2f;">Error Processing File</h4>
                    <p style="margin: 0; font-size: 14px;">{str(e)}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px;">
                <h4 style="margin-top: 0;">Troubleshooting Tips:</h4>
                <ul>
                    <li>Ensure your CSV file has the correct column names</li>
                    <li>Check for missing values or incorrect data types</li>
                    <li>Make sure all required columns are present</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Add a "What's New" section
st.markdown("---")
st.markdown("""
<div class="stCard">
    <h2 style="margin-top: 0;">✨ What's New</h2>
    <div style="display: flex; gap: 20px; overflow-x: auto; padding: 10px 0;">
        <div style="min-width: 250px; background-color: #f1f3f9; padding: 15px; border-radius: 8px; border-top: 4px solid #6C63FF;">
            <h4 style="margin-top: 0; color: #6C63FF;">🔮 Improved Predictions</h4>
            <p>Our AI model has been updated with the latest educational research for more accurate predictions.</p>
        </div>
        <div style="min-width: 250px; background-color: #f1f3f9; padding: 15px; border-radius: 8px; border-top: 4px solid #4CAF50;">
            <h4 style="margin-top: 0; color: #4CAF50;">📊 Enhanced Analytics</h4>
            <p>New visualizations help you better understand the factors affecting student performance.</p>
        </div>
        <div style="min-width: 250px; background-color: #f1f3f9; padding: 15px; border-radius: 8px; border-top: 4px solid #FF6584;">
            <h4 style="margin-top: 0; color: #FF6584;">🔔 Early Alerts</h4>
            <p>Get notified earlier about at-risk students with our improved early warning system.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer with improved styling
st.markdown("""
<div class="footer">
    <p>🚀 Built with Streamlit · © 2025 Student AI Performance · All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
