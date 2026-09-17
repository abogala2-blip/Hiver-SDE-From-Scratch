import os,re,argparse,joblib,pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
BASE=os.path.dirname(os.path.dirname(__file__))
V=joblib.load(os.path.join(BASE,'models','tfidf.joblib')); C=joblib.load(os.path.join(BASE,'models','intent_lr.joblib'))
DF=pd.read_csv(os.path.join(BASE,'data','applesupport_pairs.csv')); X=V.transform(DF.customer_text.fillna(''))

def clean(s):
    s=re.sub(r'https?://\S+','',str(s)); s=re.sub(r'@\w+','',s); return re.sub(r'\s+',' ',s).strip()
def retrieve(msg,k=3):
    q=V.transform([msg]); scores=cosine_similarity(q,X).ravel(); ids=scores.argsort()[-k:][::-1]
    return [(float(scores[i]),DF.iloc[i]) for i in ids]
def predict(msg):
    p=C.predict_proba(V.transform([msg]))[0]; j=p.argmax(); return C.classes_[j],float(p[j])
def decide(msg, intent, conf, best_score):
    text = msg.lower()

    # 1. Security-sensitive issues always go to a human.
    sensitive = [
        "hack",
        "hacked",
        "stolen",
        "fraud",
        "scam",
        "unauthorized",
        "security",
        "someone accessed",
        "someone logged in"
    ]

    if any(word in text for word in sensitive):
        return (
            "ESCALATE",
            "Security-sensitive issue requires human review"
        )

    # 2. Billing and account issues require human review.
    if intent == "billing_subscription":
        return (
            "ESCALATE",
            "Billing or subscription issue requires human review"
        )

    if intent == "account_access":
        return (
            "ESCALATE",
            "Account-access issue requires human review"
        )

    # 3. Low classifier confidence -> human.
    if conf < 0.60:
        return (
            "ESCALATE",
            "Low intent confidence"
        )

    # 4. Weak historical evidence -> human.
    if best_score < 0.18:
        return (
            "ESCALATE",
            "Insufficient historical evidence for grounded automation"
        )

    # 5. Otherwise automate.
    return (
        "AUTO-HANDLE",
        "High intent confidence and sufficient historical evidence"
    )
def draft(msg,intent,hits):
    evidence=clean(hits[0][1].brand_response)
    return f"Thanks for reaching out. Based on similar AppleSupport cases, the issue appears related to {intent.replace('_',' ')}. A historically used response was: {evidence}"
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--message',required=True); a=ap.parse_args()
    intent,conf=predict(a.message); hits=retrieve(a.message); decision,reason=decide(a.message,intent,conf,hits[0][0])
    print('\n=== APPLESUPPORT AI AGENT ==='); print('Intent:',intent); print('Confidence:',round(conf,3)); print('Decision:',decision); print('Reason:',reason); print('\nDraft reply:\n'+draft(a.message,intent,hits)); print('\nRetrieved evidence:')
    for s,r in hits: print(f'[{s:.3f}] customer={clean(r.customer_text)[:140]} | response={clean(r.brand_response)[:220]}')
