# AppleSupport AI Support Agent — Take-Home Report

## 1. Problem framing
Define what “good” means for support: correct intent, useful grounded reply, and conservative escalation.

## 2. Data
Customer Support on Twitter; one brand: AppleSupport. Use customer tweets paired to the AppleSupport response referenced by `in_response_to_tweet_id`. State sample size and random seed.

## 3. System
Customer message → TF-IDF intent model → top historical cases → grounded response → escalation gate.

## 4. Results
| System | Accuracy | Macro F1 | Auto-handle coverage | Reply quality |
|---|---:|---:|---:|---:|
| Trivial | | | | |
| Keyword | | | | |
| Proposed | | | | |

## 5. Failure analysis
Include at least five real failures. For each: customer text, predicted intent, expected intent, retrieval evidence, why it failed, fix hypothesis.

## 6. What is misleading about my headline number?
Explain how a single aggregate metric can hide class imbalance, abstention behavior, ambiguous multi-intent messages, and poor response quality.

## 7. What I would do with one more week
Human-labelled training set, conversation-level retrieval, better escalation calibration, stronger LLM judge calibration, and adversarial/safety tests.

## 8. Decision log
Document 10–15 non-obvious decisions and why they were made.
