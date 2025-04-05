import joblib
import pandas as pd
import numpy as np

class StudentPerformancePredictor:
    def __init__(self):
        # Load the trained model and preprocessors
        self.model = joblib.load("final_gradient_boosting_model.pkl")
        self.scaler = joblib.load("final_scaler.pkl")
        self.label_encoders = joblib.load("final_label_encoders.pkl")

    def preprocess_input(self, data):
        # Convert input dictionary to DataFrame
        df = pd.DataFrame([data], columns=[
            "Hours_Studied", "Attendance", "Previous_Scores",
            "Motivation_Level", "Tutoring_Sessions",
            "Parental_Involvement", "Access_to_Resources"
        ])
        
        # Encode categorical variables
        for col in ["Parental_Involvement", "Access_to_Resources", "Motivation_Level"]:
            df[col] = self.label_encoders[col].transform(df[col])
        
        # Scale numerical columns
        numerical_cols = ["Hours_Studied", "Attendance", "Previous_Scores", "Motivation_Level", "Tutoring_Sessions"]
        df[numerical_cols] = self.scaler.transform(df[numerical_cols])
        
        # Feature engineering (consistent with training)
        df["Hours_Motivation"] = df["Hours_Studied"] * (df["Motivation_Level"] + 1)
        df["Attendance_Impact"] = df["Attendance"] * df["Previous_Scores"]
        
        return df

    def predict(self, instances, **kwargs):
        # Process multiple instances (required for AI Platform compatibility)
        results = []
        for instance in instances:
            # Preprocess the input
            processed_data = self.preprocess_input(instance)
            
            # Make prediction
            predicted_score = self.model.predict(processed_data)[0]
            
            # At-risk classification
            at_risk_threshold = 60
            at_risk = int(predicted_score < at_risk_threshold)

            # Extract scaled features for recommendation logic
            hours_studied = processed_data["Hours_Studied"].values[0]
            attendance = processed_data["Attendance"].values[0]
            tutoring = processed_data["Tutoring_Sessions"].values[0]

            # Generate recommendation
            if at_risk:
                if hours_studied < -1:  # Scaled threshold (approx. < 5 hours in original scale)
                    recommendation = "Increase study hours and consider tutoring."
                elif attendance < -1:  # Scaled threshold (approx. < 0.6 in original scale)
                    recommendation = "Increase attendance and consider tutoring."
                elif tutoring < 0:  # Scaled threshold (approx. < 1 session)
                    recommendation = "Schedule more tutoring sessions."
                else:
                    recommendation = "Focus on study habits."
            else:
                recommendation = "Keep up the good work!"

            # Append result
            results.append({
                "predicted_exam_score": float(predicted_score),
                "at_risk": at_risk,
                "recommendation": recommendation
            })
        
        return results

    @classmethod
    def from_path(cls, model_dir):
        # Required for AI Platform to instantiate the class
        return cls()

if __name__ == "__main__":
    # Test locally
    predictor = StudentPerformancePredictor()
    sample_input = {
        "Hours_Studied": 5,
        "Attendance": 0.8,
        "Previous_Scores": 70,
        "Motivation_Level": "Medium",
        "Tutoring_Sessions": 2,
        "Parental_Involvement": "High",
        "Access_to_Resources": "Low"
    }
    result = predictor.predict([sample_input])
    print(result)