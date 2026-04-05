import pandas as pd
import joblib

model = joblib.load("models/model.pkl")

def predict(input_data):
    columns = ["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"]
    df = pd.DataFrame([input_data], columns=columns)

    prediction = model.predict(df)[0]

    reasons = []
    suggestions = []

    # 🔥 BP
    if df["SystolicBP"][0] > 130:
        reasons.append("High Systolic Blood Pressure")
        suggestions.append("Reduce salt intake and monitor blood pressure regularly")

    if df["DiastolicBP"][0] > 85:
        reasons.append("High Diastolic Blood Pressure")
        suggestions.append("Practice stress management and maintain healthy lifestyle")

    # 🔥 Blood Sugar
    if df["BS"][0] > 7:
        reasons.append("High Blood Sugar")
        suggestions.append("Control sugar intake and follow balanced diet")

    # 🔥 Temperature
    if df["BodyTemp"][0] > 99:
        reasons.append("Elevated Body Temperature")
        suggestions.append("Stay hydrated and consult doctor if fever persists")

    # 🔥 Heart Rate
    if df["HeartRate"][0] > 90:
        reasons.append("High Heart Rate")
        suggestions.append("Avoid stress and monitor heart rate regularly")

    # ✅ Normal case
    if len(reasons) == 0:
        reasons.append("All parameters are within normal range")
        suggestions.append("Maintain healthy lifestyle and regular checkups")

    return int(prediction), reasons, suggestions