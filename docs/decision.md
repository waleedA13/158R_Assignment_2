# Decision: dataset and predictive task (I-03)

Agreed on issue #25 on 2026-11-24. Options considered: `docs/options.md`. Every later issue follows this file; change it only by agreement of both of us.

**Dataset:** Rent the Runway clothing fit data (UCSD McAuley lab)
- Source: https://mcauleylab.ucsd.edu/public_datasets/data/renttherunway/renttherunway_final_data.json.gz (listed on https://cseweb.ucsd.edu/~jmcauley/datasets.html)
- Size: 192,544 transactions, 105,508 users, 5,850 items; one 31 MB gzipped JSON file
- Subsample plan: none needed, it runs on a laptop
- Paper: Misra, Wan, McAuley, "Decomposing fit semantics for product size recommendation in metric spaces", RecSys 2018, https://cseweb.ucsd.edu/~jmcauley/pdfs/recsys18e.pdf

**Task:** given a user and an item in a specific size (plus the user's measurements), predict the fit feedback: small, fit or large. One prediction per transaction (three-class classification).
- Split: random 80/10/10 into train/valid/test, fixed seed 158 (`src/data.py`, I-04). Test set used once, in I-12.

**Metrics**
- Primary: average AUC over the three classes (one-vs-rest), the metric the paper reports
- Secondary: macro-F1, because about 74% of labels are "fit", so accuracy would reward always predicting "fit"

**Baselines**
- Trivial: always predict "fit"
- Course model: logistic regression on size and measurement features

**Main model:** user and item latent factors with biases on top of the features, trained with class weighting.

**Open (does not block work):** whether Assignment 1 used this dataset. Reuse is allowed.

**Agreed by:** Waleed, Aditya (2026-11-24)
