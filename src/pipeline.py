import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.compose import ColumnTransformer
from xgboost import XGBClassifier


# 🔥 Feature Engineering
def add_features(X):
    import pandas as pd

    X = X.copy()

    # Age grouping
    X["AgeGroup"] = pd.cut(X["Age"], bins=[0, 20, 35, 50], labels=[0,1,2])

    # Mean Blood Pressure
    X["MeanBP"] = (X["SystolicBP"] + X["DiastolicBP"]) / 2

    # Risk Score (UPDATED)
    X["RiskScore"] = (
        X["SystolicBP"] * 0.25 +
        X["DiastolicBP"] * 0.25 +
        X["BS"] * 0.2 +
        X["BodyTemp"] * 0.15 +
        X["HeartRate"] * 0.15
    )

    return X


def get_pipeline():
    numeric_features = [
    "Age",
    "SystolicBP",
    "DiastolicBP",
    "BS",
    "BodyTemp",
    "HeartRate"
]
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features)
        ],
        remainder="passthrough"
    )

    pipeline = Pipeline([
        ("feature_engineering", FunctionTransformer(add_features)),
        ("preprocessing", preprocessor),
        ("model", XGBClassifier(eval_metric='mlogloss'))
    ])

    return pipeline