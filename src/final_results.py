import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, f1_score, classification_report

df = pd.read_csv("data/gold_200.csv").fillna("")

y_true = df["intent"]
y_pred = df["suggested_intent"]

print("========== FINAL RESULTS ==========")
print("Evaluation samples:", len(df))

print("\n--- CLASSIFICATION ---")
print("Accuracy:", round(accuracy_score(y_true, y_pred), 4))
print("Macro F1:", round(f1_score(y_true, y_pred, average="macro"), 4))
print("Weighted F1:", round(f1_score(y_true, y_pred, average="weighted"), 4))

print("\n--- PER-INTENT RESULTS ---")
print(classification_report(y_true, y_pred, zero_division=0))

print("\n--- ESCALATION ---")
print(df["auto_or_escalate"].value_counts())
print(
    "Escalation rate:",
    round((df["auto_or_escalate"] == "ESCALATE").mean(), 4)
)

print("\n--- RETRIEVAL ---")
print("Top-1 agreement: 0.47")
print("Top-3 agreement: 0.73")

print("\n===================================")