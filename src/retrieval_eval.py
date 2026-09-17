import os
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

BASE = os.path.dirname(os.path.dirname(__file__))

DATA = os.path.join(BASE, "data", "applesupport_pairs.csv")
GOLD = os.path.join(BASE, "data", "gold_200.csv")

df = pd.read_csv(DATA).fillna("")
gold = pd.read_csv(GOLD).fillna("")

vectorizer = joblib.load(
    os.path.join(BASE, "models", "tfidf.joblib")
)

classifier = joblib.load(
    os.path.join(BASE, "models", "intent_lr.joblib")
)

X = vectorizer.transform(df["customer_text"])
Q = vectorizer.transform(gold["customer_text"])

top1_correct = 0
top3_correct = 0

for i in range(len(gold)):

    scores = cosine_similarity(Q[i], X).ravel()

    # Remove exact same tweet from retrieval if present
    same_id = df["customer_tweet_id"].astype(str) == str(
        gold.iloc[i]["customer_tweet_id"]
    )

    scores[same_id.values] = -1

    top3 = scores.argsort()[-3:][::-1]

    retrieved_texts = df.iloc[top3]["customer_text"].tolist()

    retrieved_X = vectorizer.transform(retrieved_texts)

    retrieved_predictions = classifier.predict(retrieved_X)

    true_intent = gold.iloc[i]["intent"]

    if retrieved_predictions[0] == true_intent:
        top1_correct += 1

    if true_intent in retrieved_predictions:
        top3_correct += 1

print("=== RETRIEVAL EVALUATION ===")
print("Queries:", len(gold))
print(
    "Top-1 retrieved-evidence intent agreement:",
    round(top1_correct / len(gold), 4)
)
print(
    "Top-3 retrieved-evidence intent agreement:",
    round(top3_correct / len(gold), 4)
)