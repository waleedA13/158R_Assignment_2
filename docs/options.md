# I-03 options: dataset and predictive task

Three candidates for Waleed and Aditya to choose from. Drafted from the dataset page (https://cseweb.ucsd.edu/~jmcauley/datasets.html) and the papers linked there; every paper link below was opened and its numbers read from its results table. **This file does not pick one.** Record the choice in `docs/decision.md` (template at the bottom).

## Comparison

| | A. Rent the Runway: fit prediction | B. BeerAdvocate: rating prediction | C. Steam: next-game recommendation |
|---|---|---|---|
| Data | 105,508 users, 5,850 items, 192,544 transactions; one 31 MB file | 33,387 users, 66,051 beers, 1,586,259 reviews (Jan 1998 to Nov 2011); 433 MB file | 7,793,069 reviews, 2,567,538 users, 15,474 games (v2 reviews are 1.3 GB; v1 reviews 6.7 MB + user/item data 71 MB) |
| Laptop | Fine as is | Subsample (e.g. 200k reviews) | Use v1 files, or subsample users |
| Key fields | Fit feedback (small / fit / large), rating, review text, user measurements (bust size, weight, height, body type, age), item category and size, rental occasion, review date | Review text, aspect ratings (taste, look, feel, smell, overall), style, ABV, timestamps, user names | Reviews, purchases, plays, recommends, bundles, prices |
| Task | Given a user and an item in a specific size (+ measurements), predict fit: small / fit / large | Given a user and a beer, predict the overall rating | Given a user's history, rank the next game they will play/buy |
| Primary metric | Average AUC (matches the paper); report macro-F1 or BER too | MSE (matches the paper) | Hit@10 and NDCG@10 against 100 sampled negatives (matches the paper) |
| Trivial baseline | Always predict "fit" (about 74% of labels) | Global mean rating | Most popular games |
| Course-model baseline | Logistic regression on size and measurement features | Latent factor model with user and item biases | Jaccard item similarity, or BPR |
| Plausible main model | User and item latent factors + biases on top of the features, with class weighting | Latent factors + TF-IDF review-text features (or a time-aware variant) | Item-to-item model using play order (sequence-aware), compared with BPR |
| Paper to compare with | Misra, Wan, McAuley, RecSys 2018. Average AUC on RTR: 0.61 (simplest baseline) to **0.719** (their model) | McAuley and Leskovec, WWW 2013. BeerAdvocate "overall" MSE: latent factor **0.452**, their model **0.400** (most recent reviews) | Kang and McAuley (SASRec), ICDM 2018. Steam: Hit@10 **0.8729**, NDCG@10 **0.6306**; GRU4Rec+ 0.8018 / 0.5595 |
| Strengths for grading | Rich EDA (body measurements, sizes); class imbalance makes the metric discussion (Section 4) substantive; clean literature comparison | Classic course content; very direct comparison with the paper; review text gives a clear "beyond baseline" step | Large, realistic; ranking metrics are a good Section 4 topic |
| Risks | Many missing measurement values (must document handling); labels are imbalanced | Close to the course's standard rating-prediction exercises, so harder to stand out; big file | Paper's neural model is far beyond course scope, so our numbers will look weak next to it; heaviest preprocessing; check overlap with Assignment 1 |

## Links
- Dataset page: https://cseweb.ucsd.edu/~jmcauley/datasets.html
- A data: https://mcauleylab.ucsd.edu/public_datasets/data/renttherunway/renttherunway_final_data.json.gz · paper: https://cseweb.ucsd.edu/~jmcauley/pdfs/recsys18e.pdf
- B data: https://mcauleylab.ucsd.edu/public_datasets/data/beer/beeradvocate.json.gz · papers: https://cseweb.ucsd.edu/~jmcauley/pdfs/www13.pdf, https://cseweb.ucsd.edu/~jmcauley/pdfs/icdm12.pdf
- C data: Steam section of the dataset page · papers: https://cseweb.ucsd.edu/~jmcauley/pdfs/icdm18.pdf, https://cseweb.ucsd.edu/~jmcauley/pdfs/sigir17.pdf

## Questions to settle when choosing
1. Did Assignment 1 use any of these datasets? Reusing one is allowed, but a new one gives more to say in Sections 2 and 5.
2. Which risks can we absorb by Wed 11-25 (models and evaluation done)? A and B fit the schedule; C needs the most preprocessing.
3. Who presents what: Waleed presents Sections 1 and 2 (data), Aditya Sections 3 to 5 (models, evaluation, related work).

## `docs/decision.md` template
```
Dataset:    name, source URL, size, subsample plan
Task:       given X, predict Y per Z; split scheme (random / by time / by user) and proportions
Metrics:    primary + why; secondary
Baselines:  trivial; course model
Main model:
Agreed by:  Waleed, Aditya (date)
```
