import os,pandas as pd
from taxonomy import weak_label
BASE=os.path.dirname(os.path.dirname(__file__))
g=pd.read_csv(os.path.join(BASE,'data','gold_200.csv'))
g=g[g.intent.fillna('').str.strip()!='']
if len(g)==0: print('Fill human labels first.'); raise SystemExit
from sklearn.metrics import accuracy_score,f1_score
# Trivial baseline
trivial=['other']*len(g)
print('TRIVIAL accuracy',accuracy_score(g.intent,trivial),'macro_f1',f1_score(g.intent,trivial,average='macro'))
# Keyword baseline
pred=g.customer_text.map(weak_label)
print('KEYWORD accuracy',accuracy_score(g.intent,pred),'macro_f1',f1_score(g.intent,pred,average='macro'))
