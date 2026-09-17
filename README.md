\# AppleSupport AI Agent



An AI-assisted customer support agent developed for the Hiver SDE take-home project.



The system classifies customer queries into support intents, retrieves similar historical AppleSupport cases, generates evidence-grounded responses, and decides whether a case should be automatically handled or escalated to a human.



\## Features



\- Intent classification using TF-IDF + Logistic Regression

\- 8-class support intent taxonomy

\- Historical case retrieval using cosine similarity

\- Evidence-grounded response drafting

\- Confidence-based escalation

\- Safety-sensitive escalation rules

\- Classification evaluation

\- Retrieval evaluation

\- Baseline comparison

\- Optional LLM-judge rubric



\## Dataset



The project uses 15,000 AppleSupport customer-support pairs.



Main dataset:



`data/applesupport\_pairs.csv`



Evaluation dataset:



`data/gold\_200.csv`



The evaluation set contains 200 examples.



\## Intent Taxonomy



The system supports eight intents:



\- `account\_access`

\- `app\_service`

\- `billing\_subscription`

\- `connectivity`

\- `device\_hardware`

\- `device\_performance`

\- `ios\_update`

\- `other`



\## Architecture



```text

Customer Query

&#x20;     |

&#x20;     v

Text Preprocessing

&#x20;     |

&#x20;     v

TF-IDF + Logistic Regression

&#x20;     |

&#x20;     +----------------------+

&#x20;     |                      |

&#x20;     v                      v

Intent Prediction       Historical Retrieval

&#x20;     |                      |

&#x20;     +----------+-----------+

&#x20;                |

&#x20;                v

&#x20;         Safety / Policy Rules

&#x20;                |

&#x20;         +------+------+

&#x20;         |             |

&#x20;         v             v

&#x20;    AUTO-HANDLE     ESCALATE

&#x20;         |

&#x20;         v

&#x20;  Grounded Response

