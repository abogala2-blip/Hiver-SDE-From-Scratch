import os
import pandas as pd
import joblib

BASE = os.path.dirname(os.path.dirname(__file__))

DATA = os.path.join(BASE, "data", "applesupport_pairs.csv")
GOLD = os.path.join(BASE, "data", "gold_200.csv")

MODEL = os.path.join(BASE, "models", "tfidf.joblib")
CLASSIFIER = os.path.join(BASE, "models", "intent_lr.joblib")

df = pd.read_csv(DATA)

# Select the same 200 examples reproducibly
gold = df.sample(n=200, random_state=123).copy()

vectorizer = joblib.load(MODEL)
classifier = joblib.load(CLASSIFIER)

X = vectorizer.transform(gold["customer_text"].fillna(""))

probabilities = classifier.predict_proba(X)
predictions = classifier.classes_[probabilities.argmax(axis=1)]
confidence = probabilities.max(axis=1)

gold["suggested_intent"] = predictions
gold["suggested_confidence"] = confidence.round(3)

# Suggested automation decision
def suggested_decision(text, intent, confidence):
    text = str(text).lower()

    sensitive = [
        "hack", "hacked", "stolen", "fraud",
        "scam", "unauthorized", "security",
        "someone accessed", "someone logged in"
    ]

    if any(word in text for word in sensitive):
        return "ESCALATE", "Security-sensitive issue requires human review"

    if intent == "billing_subscription":
        return "ESCALATE", "Billing or subscription issue requires human review"

    if intent == "account_access":
        return "ESCALATE", "Account-access issue requires human review"

    if confidence < 0.60:
        return "ESCALATE", "Low intent confidence"

    return "AUTO-HANDLE", "Routine troubleshooting with sufficient evidence"


decisions = [
    suggested_decision(t, i, c)
    for t, i, c in zip(
        gold["customer_text"],
        gold["suggested_intent"],
        gold["suggested_confidence"]
    )
]

gold["suggested_auto_or_escalate"] = [x[0] for x in decisions]
gold["suggested_escalation_reason"] = [x[1] for x in decisions]

# Human-review columns
gold["intent"] = ""
gold["auto_or_escalate"] = ""
gold["escalation_reason"] = ""
gold["human_notes"] = ""

columns = [
    "customer_tweet_id",
    "customer_text",
    "brand_response",
    "suggested_intent",
    "suggested_confidence",
    "suggested_auto_or_escalate",
    "suggested_escalation_reason",
    "intent",
    "auto_or_escalate",
    "escalation_reason",
    "human_notes"
]

gold[columns].to_csv(GOLD, index=False)

print("Created 200 examples for human review.")
print("File:", GOLD)
print()
print("IMPORTANT:")
print("suggested_* columns are model suggestions.")
print("intent / auto_or_escalate / escalation_reason must be human-reviewed.")