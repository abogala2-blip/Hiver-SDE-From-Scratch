import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

df = pd.read_csv("data/gold_200.csv").fillna("")

y_true = df["intent"]
y_pred = df["suggested_intent"]

print("=== PROPOSED MODEL ===")
print("Accuracy:", round(accuracy_score(y_true, y_pred), 4))
print("Macro F1:", round(f1_score(y_true, y_pred, average="macro"), 4))

majority = y_true.value_counts().idxmax()
majority_pred = [majority] * len(y_true)

print("\n=== MAJORITY BASELINE ===")
print("Majority class:", majority)
print("Accuracy:", round(accuracy_score(y_true, majority_pred), 4))
print("Macro F1:", round(f1_score(y_true, majority_pred, average="macro", zero_division=0), 4))

print("\n=== COMPARISON ===")
print("Proposed Accuracy:", round(accuracy_score(y_true, y_pred), 4))
print("Proposed Macro F1:", round(f1_score(y_true, y_pred, average="macro"), 4))
print("Majority Accuracy:", round(accuracy_score(y_true, majority_pred), 4))
print("Majority Macro F1:", round(f1_score(y_true, majority_pred, average="macro", zero_division=0), 4))