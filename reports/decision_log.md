# Decision Log
1. Chose AppleSupport because it has a large number of brand responses in the dataset.
2. Defined the basic data unit as customer tweet → referenced brand response.
3. Sampled 15,000 pairs with a fixed seed for fast reproducibility.
4. Used an 8-class intent taxonomy to keep labels actionable.
5. Used TF-IDF + logistic regression for an interpretable, fast baseline.
6. Used historical retrieval to ground responses in real brand behavior.
7. Used cosine similarity because it is deterministic and easy to inspect.
8. Added confidence-based abstention instead of forcing every case to automation.
9. Escalated security/billing/legal-sensitive cases conservatively.
10. Created a 200-row gold set, with human review required before evaluation claims.
11. Included a trivial baseline to expose class-imbalance effects.
12. Included a keyword baseline to measure the value of the learned model.
13. Separate classification quality from reply quality because they measure different things.
14. Treat headline accuracy as incomplete evidence of trustworthiness.
15. Prefer one more week of labelled data and calibration over adding unnecessary model complexity.
