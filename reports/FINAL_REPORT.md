\# AppleSupport AI Agent

\## Hiver SDE Take-Home Project — Final Report



\## 1. Project Overview



The AppleSupport AI Agent is an AI-assisted customer support system designed to classify customer queries, retrieve similar historical support cases, generate evidence-grounded responses, and decide whether a query can be automatically handled or should be escalated to a human agent.



The system combines supervised intent classification, historical-case retrieval, rule-based safety checks, and response generation.



\---



\## 2. Dataset



The project uses AppleSupport customer-support data.



A dataset of 15,000 customer-support pairs was prepared from the provided AppleSupport data.



Each pair contains customer text and a corresponding historical support response.



The prepared dataset is stored as:



`data/applesupport\_pairs.csv`



A separate evaluation set containing 200 examples was created and stored as:



`data/gold\_200.csv`



\---



\## 3. Intent Taxonomy



The final system uses eight support intents:



1\. account\_access

2\. app\_service

3\. billing\_subscription

4\. connectivity

5\. device\_hardware

6\. device\_performance

7\. ios\_update

8\. other



The initial weak-label analysis showed class imbalance. The final taxonomy was therefore kept compact and focused on the major support categories.



\---



\## 4. System Architecture



The system follows this pipeline:



Customer Query

&#x20;       |

&#x20;       v

Text Preprocessing

&#x20;       |

&#x20;       v

TF-IDF Feature Extraction

&#x20;       |

&#x20;       v

Intent Classification

&#x20;       |

&#x20;       +------------------+

&#x20;       |                  |

&#x20;       v                  v

Historical Retrieval    Safety / Policy Rules

&#x20;       |                  |

&#x20;       +---------+--------+

&#x20;                 |

&#x20;                 v

&#x20;       AUTO-HANDLE / ESCALATE

&#x20;                 |

&#x20;                 v

&#x20;       Grounded Draft Response



\---



\## 5. Intent Classification



A TF-IDF vectorizer is used to convert customer messages into numerical text features.



A Logistic Regression classifier is then used to predict the support intent.



The trained artifacts are stored in:



`models/tfidf.joblib`



`models/intent\_lr.joblib`



The training pipeline was executed successfully on 15,000 examples.



\---



\## 6. Classification Evaluation



The final evaluation was performed on 200 examples.



Results:



| Metric | Result |

|---|---:|

| Accuracy | 0.80 |

| Macro F1 | 0.3869 |

| Weighted F1 | 0.82 |



The weighted F1 is higher than the macro F1 because the dataset contains substantial class imbalance.



Per-class results:



| Intent | Precision | Recall | F1 |

|---|---:|---:|---:|

| account\_access | 1.00 | 0.62 | 0.77 |

| app\_service | 0.90 | 0.93 | 0.91 |

| billing\_subscription | 1.00 | 0.31 | 0.47 |

| connectivity | 1.00 | 0.33 | 0.50 |

| device\_hardware | 0.59 | 1.00 | 0.74 |

| device\_performance | 1.00 | 0.77 | 0.87 |

| ios\_update | 0.88 | 0.91 | 0.89 |

| other | 0.74 | 0.94 | 0.83 |



\---



\## 7. Historical Retrieval



The agent retrieves similar historical AppleSupport cases using TF-IDF representations and cosine similarity.



For each incoming customer query, the system retrieves the most similar historical examples and uses their previous responses as supporting evidence.



Retrieval evaluation was performed on 200 queries.



Results:



| Retrieval Metric | Result |

|---|---:|

| Top-1 intent agreement | 0.47 |

| Top-3 intent agreement | 0.73 |



The Top-3 result indicates that the relevant intent is frequently present among the retrieved historical cases even when it is not always the highest-ranked result.



\---



\## 8. Grounded Response Generation



The system generates a draft response using retrieved historical support evidence.



The response-generation pipeline:



1\. Receives the customer query.

2\. Predicts the customer intent.

3\. Retrieves similar historical cases.

4\. Selects relevant historical responses.

5\. Generates a draft response based on the retrieved evidence.



This reduces the risk of producing unsupported responses because the agent has access to previous AppleSupport cases related to the query.



\---



\## 9. Escalation Policy



The agent contains a safety and escalation layer.



Cases involving sensitive topics such as:



\- security

\- hacking

\- fraud

\- unauthorized activity

\- legal issues

\- payment disputes



are candidates for escalation.



Billing/subscription and account-access issues are also configured for human review.



Low-confidence predictions are escalated instead of being automatically handled.



\---



\## 10. Escalation Evaluation



The escalation policy was evaluated on 200 examples.



| Decision | Cases |

|---|---:|

| AUTO-HANDLE | 179 |

| ESCALATE | 21 |

| Total | 200 |



Escalation rate:



10.5%



The distribution by intent was:



| Intent | Auto-Handle | Escalate | Total |

|---|---:|---:|---:|

| account\_access | 0 | 8 | 8 |

| app\_service | 74 | 0 | 74 |

| billing\_subscription | 0 | 13 | 13 |

| connectivity | 6 | 0 | 6 |

| device\_hardware | 13 | 0 | 13 |

| device\_performance | 13 | 0 | 13 |

| ios\_update | 55 | 0 | 55 |

| other | 18 | 0 | 18 |



\---



\## 11. Baseline Comparison



The proposed system was compared with a simple majority-class baseline.



| Model | Accuracy | Macro F1 |

|---|---:|---:|

| Proposed model | 0.80 | 0.3869 |

| Majority baseline | 0.37 | 0.0675 |



The proposed approach provides substantially better classification performance than predicting the most frequent class for every example.



\---



\## 12. End-to-End Agent Test



The final agent was tested with customer messages such as:



`My iPhone is not connecting to WiFi`



The system produced:



\- Intent: connectivity

\- Confidence: 0.918

\- Decision: AUTO-HANDLE



The system also correctly routed a billing-related example such as:



`I was charged twice for my Apple subscription`



to:



\- Intent: billing\_subscription

\- Decision: ESCALATE



These tests demonstrate the complete classification, retrieval, response, and escalation pipeline.



\---



\## 13. LLM Judge



An optional LLM-judge rubric was implemented in:



`src/llm\_judge.py`



The rubric evaluates:



\- Grounding

\- Helpfulness

\- Clarity

\- Safety



The current implementation defines the evaluation rubric but does not report LLM-judge scores.



LLM-judge scores are intentionally not reported because the evaluation process requires a small human-rated subset for validation of the judge, and such a validated human-rated subset was not available during this implementation.



\---



\## 14. Limitations



The main limitations are:



1\. The dataset has significant class imbalance.

2\. Some intents have relatively few evaluation examples.

3\. Retrieval Top-1 agreement is lower than Top-3 agreement.

4\. The current response generator is evidence-based but not a full generative LLM system.

5\. The LLM judge was prepared as an optional evaluation component but was not used to produce final reported scores.

6\. The 200-example evaluation set is relatively small compared with the full training dataset.



\---



\## 15. Future Improvements



Potential improvements include:



\- Increasing human-labeled training data.

\- Improving class balance.

\- Using sentence embeddings for semantic retrieval.

\- Adding a reranking stage after retrieval.

\- Using an LLM for higher-quality grounded response generation.

\- Expanding the human evaluation set.

\- Validating an LLM judge against human ratings.

\- Adding monitoring and feedback loops for production deployment.



\---



\## 16. Project Structure



```text

Hiver\_SDE\_Submission/

│

├── README.md

├── requirements.txt

│

├── data/

│   ├── applesupport\_pairs.csv

│   └── gold\_200.csv

│

├── models/

│   ├── intent\_lr.joblib

│   └── tfidf.joblib

│

├── reports/

│   ├── decision\_log.md

│   ├── report\_template.md

│   └── FINAL\_REPORT.md

│

└── src/

&#x20;   ├── agent.py

&#x20;   ├── baseline.py

&#x20;   ├── baselines.py

&#x20;   ├── escalation\_eval.py

&#x20;   ├── evaluate.py

&#x20;   ├── fast\_gold.py

&#x20;   ├── final\_results.py

&#x20;   ├── llm\_judge.py

&#x20;   ├── make\_gold.py

&#x20;   ├── prepare\_data.py

&#x20;   ├── retrieval\_eval.py

&#x20;   ├── taxonomy.py

&#x20;   └── train.py

