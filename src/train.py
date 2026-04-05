import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, recall_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from src.pipeline import get_pipeline


# 🔥 Model Comparison
def compare_models(X_train, X_test, y_train, y_test):
    models = {
        "Logistic Regression": LogisticRegression(max_iter=200),
        "Random Forest": RandomForestClassifier(),
        "XGBoost": XGBClassifier(eval_metric='mlogloss')
    }

    results = []

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        acc = accuracy_score(y_test, preds)
        results.append([name, acc])

    df = pd.DataFrame(results, columns=["Model", "Accuracy"])
    print("\nModel Comparison:\n", df)

def train():
    df = pd.read_csv("data/maternal_health.csv")

    # Encode target
    df["RiskLevel"] = df["RiskLevel"].map({
        "low risk": 0,
        "mid risk": 1,
        "high risk": 2
    })

    X = df.drop("RiskLevel", axis=1)
    y = df["RiskLevel"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # 🔥 Step 1: Compare models
    compare_models(X_train, X_test, y_train, y_test)

    # 🔥 Step 2: Train pipeline
    pipeline = get_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    # 🔥 Step 3: Evaluation
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

    recall = recall_score(y_test, y_pred, average='macro')
    print("Recall:", recall)

    # 🔥 Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)

    plt.figure()
    sns.heatmap(cm, annot=True)
    plt.title("Confusion Matrix")
    plt.savefig("models/confusion_matrix.png")
    plt.close()

    # 🔥 Feature Importance (FIXED)
    model = pipeline.named_steps["model"]
    importances = model.feature_importances_

    feature_names = pipeline.named_steps["preprocessing"].get_feature_names_out()

    fi = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False)

    fi["Feature"] = fi["Feature"].str.replace("num__", "")

    print("\nFeature Importance:\n", fi)

    plt.figure(figsize=(8,6))
    plt.barh(fi["Feature"], fi["Importance"])
    plt.gca().invert_yaxis()
    plt.title("Feature Importance")
    plt.savefig("models/feature_importance.png")
    plt.close()

    # 🔥 Save model
    joblib.dump(pipeline, "models/model.pkl")


if __name__ == "__main__":
    train()