&#x20;  AppleSupport AI Agent



An AI-powered customer support agent for AppleSupport-style queries. The system combines \*\*intent classification, semantic retrieval, grounded response generation, and rule-based escalation\*\* to determine whether a customer issue can be handled automatically or requires human review.



\---



&#x20;  Overview



Customer support systems need to handle large volumes of queries while maintaining consistency, reliability, and appropriate safety boundaries.



This project implements an end-to-end support pipeline that:



1\. Classifies customer messages into support intents.

2\. Retrieves similar historical customer-support cases.

3\. Uses retrieved evidence to construct a grounded response.

4\. Applies an escalation policy for sensitive or low-confidence cases.

5\. Evaluates classification, retrieval, escalation, and baseline performance.



The project was developed using an AppleSupport-style dataset containing \*\*15,000 customer-support pairs\*\*.



\---



&#x20;     Key Features



\- \*\*Intent Classification\*\*

&#x20; - TF-IDF text representation

&#x20; - Logistic Regression classifier

&#x20; - Eight support categories



\- \*\*Semantic Retrieval\*\*

&#x20; - TF-IDF based similarity search

&#x20; - Cosine similarity

&#x20; - Top-k historical evidence retrieval



\- \*\*Grounded Responses\*\*

&#x20; - Responses are based on retrieved historical support cases

&#x20; - Helps reduce unsupported responses



\- \*\*Escalation System\*\*

&#x20; - Automatically handles routine issues

&#x20; - Escalates billing, account-access, security-sensitive, and low-confidence cases



\- \*\*Evaluation Framework\*\*

&#x20; - Accuracy

&#x20; - Precision

&#x20; - Recall

&#x20; - F1-score

&#x20; - Confusion matrix

&#x20; - Retrieval agreement

&#x20; - Escalation analysis

&#x20; - Baseline comparison



\- \*\*Human Gold Set\*\*

&#x20; - 200 examples prepared for human-reviewed evaluation



\---



\## System Architecture



```text

&#x20;                   Customer Query

&#x20;                         |

&#x20;                         v

&#x20;               +-------------------+

&#x20;               |  Text Preprocess  |

&#x20;               +-------------------+

&#x20;                         |

&#x20;                         v

&#x20;               +-------------------+

&#x20;               | Intent Classifier |

&#x20;               | LogisticRegression|

&#x20;               +-------------------+

&#x20;                         |

&#x20;                Intent + Confidence

&#x20;                         |

&#x20;            +------------+------------+

&#x20;            |                         |

&#x20;            v                         v

&#x20;     Semantic Retrieval        Escalation Policy

&#x20;            |                         |

&#x20;            v                         v

&#x20;      Historical Cases         AUTO-HANDLE / ESCALATE

&#x20;            |

&#x20;            v

&#x20;     Grounded Response

&#x20;            |

&#x20;            v

&#x20;       Final Support Reply



Intent Taxonomy



The system currently uses the following support categories:



Intent	Description

account\_access	Apple ID, iCloud, login and account-access issues

app\_service	Apps, Apple services and related functionality

billing\_subscription	Billing, subscriptions and payment-related issues

connectivity	Wi-Fi, Bluetooth, cellular and network connectivity

device\_hardware	Hardware, battery, screen, speaker and physical-device issues

device\_performance	Freezing, lagging, crashing and performance issues

ios\_update	iOS updates, upgrades and update-related issues

other	Queries outside the primary support categories

Dataset



The project uses an AppleSupport-style customer-support dataset.



Dataset preparation

Raw archive was extracted locally.

Customer-support records were processed into structured pairs.

15,000 customer-support pairs were prepared.

A separate 200-example human gold set was created for evaluation.

The final gold set contains manually reviewed intent labels used as evaluation ground truth.

Main data files

data/

├── applesupport\_pairs.csv

└── gold\_200.csv

Machine Learning Pipeline

1\. Text Representation



Customer messages are converted into numerical feature vectors using TF-IDF.



Customer Text

&#x20;     |

&#x20;     v

&#x20;   TF-IDF

&#x20;     |

&#x20;     v

Feature Vector

2\. Intent Classification



A Logistic Regression classifier predicts the customer's support intent.



TF-IDF Features

&#x20;      |

&#x20;      v

Logistic Regression

&#x20;      |

&#x20;      v

Predicted Intent

&#x20;      +

Confidence Score



The trained artifacts are stored in:



models/

├── intent\_lr.joblib

└── tfidf.joblib

Retrieval



After intent classification, the system retrieves similar historical support cases using cosine similarity.



For a customer query q and historical document d:



cosine\_similarity(q, d)



The highest-scoring historical examples are returned as supporting evidence.



The agent uses this retrieved evidence when constructing its draft response.



Escalation Policy



The system uses an explicit decision policy rather than automatically responding to every query.



Escalate when:

Intent confidence is below the configured threshold.

Billing or subscription issues require human/account review.

Account-access issues require human review.

Security-sensitive or disputed cases are detected.

Auto-handle when:

The predicted intent has sufficient confidence.

Historical retrieval provides sufficient supporting evidence.

The query falls within routine troubleshooting categories.



Example:



Customer Query

&#x20;     |

&#x20;     v

Intent Prediction

&#x20;     |

&#x20;     +---- Low confidence ----> ESCALATE

&#x20;     |

&#x20;     +---- Sensitive issue ---> ESCALATE

&#x20;     |

&#x20;     +---- Otherwise ---------> Check Evidence

&#x20;                                     |

&#x20;                                     +--> Sufficient --> AUTO-HANDLE

&#x20;                                     |

&#x20;                                     +--> Insufficient -> ESCALATE

Example

Input

My iPhone is not connecting to WiFi

Agent Output

Intent: connectivity

Confidence: 0.918

Decision: AUTO-HANDLE



The system retrieves similar historical AppleSupport cases and uses them as evidence for the response.



Evaluation Results



The final evaluation was performed using the 200-example gold set.



Classification Performance

Metric	Result

Accuracy	0.85

Macro F1	0.7485

Weighted F1	0.84

Evaluation Samples	200

Per-Intent Performance

Intent	Precision	Recall	F1

account\_access	1.00	0.62	0.77

app\_service	0.90	0.93	0.91

billing\_subscription	1.00	0.31	0.47

connectivity	1.00	0.33	0.50

device\_hardware	0.59	1.00	0.74

device\_performance	1.00	0.77	0.87

ios\_update	0.88	0.91	0.89

other	0.74	0.94	0.83

Baseline Comparison



A simple majority-class baseline was implemented to provide a reference point.



Model	Accuracy	Macro F1

Proposed pipeline	0.80	0.3869

Majority baseline	0.37	0.0675



The proposed pipeline provides a substantially stronger reference than simply assigning every query to the most frequent intent.



Escalation Evaluation



Evaluation was performed on 200 cases.



AUTO-HANDLE : 179

ESCALATE    : 21



Escalation rate:



10.5%



The intent-level analysis is available in:



src/escalation\_eval.py

Retrieval Evaluation



Retrieval was evaluated on 200 queries.



Results:



Metric	Agreement

Top-1 retrieved-intent agreement	47%

Top-3 retrieved-intent agreement	73%



Top-3 retrieval provides broader historical evidence than relying only on the single highest-ranked result.



Project Structure

Hiver-SDE-From-Scratch/

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

│   ├── FINAL\_REPORT.md

│   ├── decision\_log.md

│   └── report\_template.md

│

├── src/

│   ├── agent.py

│   ├── baseline.py

│   ├── baselines.py

│   ├── escalation\_eval.py

│   ├── evaluate.py

│   ├── fast\_gold.py

│   ├── final\_results.py

│   ├── llm\_judge.py

│   ├── make\_gold.py

│   ├── prepare\_data.py

│   ├── retrieval\_eval.py

│   ├── taxonomy.py

│   └── train.py

│

├── .gitignore

├── README.md

└── requirements.txt

Installation

Requirements

Python 3.13

pip

Windows/Linux/macOS

Create virtual environment

python -m venv .venv

Activate on Windows

.venv\\Scripts\\activate

Install dependencies

pip install -r requirements.txt

Running the Project

Prepare the dataset

python src/prepare\_data.py

Train the intent classifier

python src/train.py

Run the AI agent

python src/agent.py --message "My iPhone is not connecting to WiFi"

Run classification evaluation

python src/evaluate.py

Run baseline comparison

python src/baselines.py

Run escalation evaluation

python src/escalation\_eval.py

Run retrieval evaluation

python src/retrieval\_eval.py

Generate the human gold set

python src/make\_gold.py

Optional LLM Judge



The repository also contains an optional LLM-judge component.



src/llm\_judge.py



The judge is designed to evaluate:



Grounding

Helpfulness

Clarity

Safety



The LLM judge requires an appropriate API key and should be run separately from the core evaluation pipeline.



Engineering Considerations

Reliability



The agent does not rely only on model confidence. Retrieval evidence and explicit escalation rules are also considered.



Safety



Sensitive or disputed issues are routed for human review rather than being automatically handled.



Interpretability



The system exposes:

Predicted intent

Confidence

Decision

Escalation reason

Retrieved historical evidence

This makes the decision process easier to inspect and debug.

Reproducibility



The project keeps:

Training scripts

Evaluation scripts

Model artifacts

Dataset preparation scripts

Reports

Requirements

within a structured repository.



Limitations:

The dataset is an AppleSupport-style historical support dataset and may contain class imbalance.

Some intents have relatively small evaluation support.

Retrieval quality depends on the similarity between a new query and historical cases.

The current system uses TF-IDF rather than a large language model embedding model.

The LLM judge is optional and is not required for the core pipeline.

Future Improvements



Potential extensions include:



Transformer-based sentence embeddings for retrieval

Hybrid BM25 + semantic retrieval

Reranking retrieved support cases

More extensive human-reviewed evaluation data

Confidence calibration

Multilingual support

Structured troubleshooting workflows

Production API deployment

Monitoring and logging

Automated regression testing

Technologies

Python 3.13

pandas

NumPy

scikit-learn

TF-IDF

Logistic Regression

Cosine Similarity

joblib

Git / GitHub

Author



B. Anantha Narasimha Reddy

Computer Science Engineering



License

This project is intended for educational, evaluation, and demonstration purposes.

