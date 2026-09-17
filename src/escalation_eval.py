import pandas as pd

df = pd.read_csv("data/gold_200.csv").fillna("")

print("=== ESCALATION EVALUATION ===")
print("Total cases:", len(df))

print("\nDecision distribution:")
print(df["auto_or_escalate"].value_counts())

print("\nEscalation rate:",
      round((df["auto_or_escalate"] == "ESCALATE").mean(), 3))

print("\nEscalation by intent:")
print(
    pd.crosstab(
        df["intent"],
        df["auto_or_escalate"],
        margins=True
    )
)

print("\nIntent distribution:")
print(df["intent"].value_counts())