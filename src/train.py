import os, joblib, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from taxonomy import weak_label

BASE=os.path.dirname(os.path.dirname(__file__))
df=pd.read_csv(os.path.join(BASE,'data','applesupport_pairs.csv'))
df['weak_intent']=df.customer_text.fillna('').map(weak_label)
vec=TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=60000,sublinear_tf=True,strip_accents='unicode')
X=vec.fit_transform(df.customer_text.fillna(''))
clf=LogisticRegression(max_iter=1200,class_weight='balanced')
clf.fit(X,df.weak_intent)
os.makedirs(os.path.join(BASE,'models'),exist_ok=True)
joblib.dump(vec,os.path.join(BASE,'models','tfidf.joblib'))
joblib.dump(clf,os.path.join(BASE,'models','intent_lr.joblib'))
print('Training rows:',len(df))
print('Intent distribution:')
print(df.weak_intent.value_counts())
