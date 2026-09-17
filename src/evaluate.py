import os,joblib,pandas as pd
from sklearn.metrics import accuracy_score,f1_score,classification_report,confusion_matrix
BASE=os.path.dirname(os.path.dirname(__file__))
g=pd.read_csv(os.path.join(BASE,'data','gold_200.csv')); g=g[g.intent.fillna('').str.strip()!='']
if len(g)==0: print('Fill human labels first.'); raise SystemExit
V=joblib.load(os.path.join(BASE,'models','tfidf.joblib')); C=joblib.load(os.path.join(BASE,'models','intent_lr.joblib'))
p=C.predict(V.transform(g.customer_text.fillna('')))
print('N=',len(g)); print('Accuracy=',accuracy_score(g.intent,p)); print('Macro F1=',f1_score(g.intent,p,average='macro'))
print(classification_report(g.intent,p,zero_division=0))
print('Confusion matrix labels:',list(C.classes_)); print(confusion_matrix(g.intent,p,labels=C.classes_))
