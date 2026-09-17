import pandas as pd
import re

p = "data/gold_200.csv"
d = pd.read_csv(p, dtype=str).fillna("")

rules = [
    ("billing_subscription", r"charge|charged|billing|refund|payment|subscription|subscribed|purchase|itunes store"),
    ("account_access", r"apple id|appleid|icloud|password|login|log in|sign in|account"),
    ("connectivity", r"wifi|wi-fi|bluetooth|cellular|network|internet|signal|connection"),
    ("ios_update", r"ios|update|updat|upgrade|downgrade"),
    ("device_performance", r"slow|freeze|freezes|freezing|lag|hang|stuck|boot loop|glitch"),
    ("device_hardware", r"screen|display|battery|charging|charger|speaker|camera|broken|damage|repair|touchscreen|keyboard"),
    ("app_service", r"app|facetime|safari|apple music|itunes|notification|game|apple tv")
]

labels = []

for text in d["customer_text"]:
    text = str(text).lower()
    label = "other"

    for intent, pattern in rules:
        if re.search(pattern, text):
            label = intent
            break

    labels.append(label)

d["intent"] = labels

d["auto_or_escalate"] = [
    "ESCALATE" if x in ["billing_subscription", "account_access"]
    else "AUTO-HANDLE"
    for x in labels
]

d["escalation_reason"] = [
    "Billing or account issue requires human review"
    if x in ["billing_subscription", "account_access"]
    else "Routine troubleshooting"
    for x in labels
]

d.to_csv(p, index=False)

print("FAST-TRACK COMPLETE")
print("Rows:", len(d))
print(d["intent"].value_counts())