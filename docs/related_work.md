# Related work (I-14)

Task (from the team decision): on Rent the Runway data, given a user and an item in a size plus measurements, predict small / fit / large. Primary metric average AUC, secondary macro-F1.

Every link below was opened on 2026-11-24 and the numbers were read from the paper text and tables. Numbers that could not be confirmed are left out.

## 1. Misra, Wan, McAuley (2018): the dataset's own paper

- **Citation:** Rishabh Misra, Mengting Wan, Julian McAuley. "Decomposing Fit Semantics for Product Size Recommendation in Metric Spaces." Proceedings of the 12th ACM Conference on Recommender Systems (RecSys '18), Vancouver, 2018, pp. 422-426.
- **Link:** https://cseweb.ucsd.edu/~jmcauley/pdfs/recsys18e.pdf (PDF title: "Decomposing Fit Semantics for Product Size Recommendation in Metric Spaces")
- **Summary:** The authors treat size recommendation as predicting whether a size fits, using the fit feedback customers leave with returns or reviews. They argue that fit feedback also reflects style and other product traits, so a single "true size" per customer and product is too crude. They also release the two datasets, ModCloth and Rent the Runway, that this project uses.
- **Method:** An ordinal regression learns K-dimensional latent factors for customers and products, plus bias terms and monotonicity constraints across sizes of the same product. Each transaction is then embedded, and a nearest-neighbor classifier runs in a space learned with large margin nearest neighbor metric learning on a small set of selected prototype transactions. The prototypes address the label imbalance.
- **Metric and split:** AUC, labelled "average AUC" in Table 2, following the protocol of Sembium et al. (2017). The text does not spell out how the average is taken across the three classes. Split: random 80:10:10 train, validation, test; hyperparameters tuned on validation.
- **Reported numbers (Table 2, Rent the Runway average AUC):** 0.61 for the single-latent-variable baseline with logistic regression (1-LV-LR), 0.676 for K-LV-LR, 0.672 for K-LF-LR, 0.681 for K-LV-ML, and 0.719 for the proposed K-LF-ML. On ModCloth the same row reads 0.615, 0.617, 0.626, 0.621, 0.657.

## 2. Sheikh et al. (2019): a neural model benchmarked on the same data

- **Citation:** Abdul-Saboor Sheikh, Romain Guigoures, Evgenii Koriagin, Yuen King Ho, Reza Shirvany, Roland Vollgraf, Urs Bergmann. "A Deep Learning System for Predicting Size and Fit in Fashion E-Commerce." Thirteenth ACM Conference on Recommender Systems (RecSys '19), Copenhagen, 2019. arXiv:1907.09844.
- **Link:** https://arxiv.org/abs/1907.09844 (page title: "A Deep Learning System for Predicting Size and Fit in Fashion E-Commerce"); PDF at https://arxiv.org/pdf/1907.09844
- **Summary:** A Zalando-led team replaces the two-step pipeline of Misra et al. with one network trained end to end on customer and article features. Besides ModCloth and Rent the Runway, they test on Zalando data, including cold-start cases. They report that dropping the item ID hurts accuracy, while dropping the customer ID changes little, because most customers have a single transaction.
- **Method:** Two input pathways, one for customer features and one for article features, with entity embeddings for categorical fields. Their outputs are combined and passed through shared layers to predict small, fit or large.
- **Metric and split:** Micro-averaged AUC, accuracy and average log-likelihood. Random 80/10/10 train, validation, test, following Misra et al. The authors say they do not know the exact split of Misra et al., so they report mean and standard deviation over 10 independent runs.
- **Reported numbers (Table 4, Rent the Runway):** micro-averaged AUC 0.692 (MLP baseline) and 0.749 (their model, SFnet); accuracy 0.733 (MLP baseline) and 0.760 (SFnet). The same table repeats the four Misra et al. rows (0.676, 0.672, 0.681, 0.719), copied from the earlier paper.
- **Comparability note:** Misra et al. report "average AUC" and Sheikh et al. report "micro-averaged AUC". The papers do not state that the two are the same quantity, so compare them with care.

## 3. Sembium, Rastogi, Saroop, Merugu (2017): the original fit-prediction formulation

- **Citation:** Vivek Sembium, Rajeev Rastogi, Atul Saroop, Srujana Merugu. "Recommending Product Sizes to Customers." Proceedings of the 11th ACM Conference on Recommender Systems (RecSys '17), Como, 2017, pp. 243-250.
- **Link:** https://cdn.amazon.science/e0/1f/f6eff24d42858edc71ab97d8d7e8/recommending-product-sizes-to-customers.pdf (PDF title: "Recommending Product Sizes to Customers")
- **Summary:** An Amazon team frames size recommendation as predicting small, fit or large for a customer and product pair. Each customer and product gets a latent "true size", and the outcome depends on the difference between the two. Misra et al. cite it as the source of their evaluation protocol, and Sheikh et al. cite it as a starting point for the task.
- **Method:** Latent factor model fit to purchase and return data with an ordinal loss (a hinge loss and a second loss variant). The learned sizes feed a logistic regression or random forest classifier. Personas and return codes are added as extras.
- **Metric and split:** Weighted AUC of the downstream classifier. Time-based split: the first 80% of transactions in time order for training, the rest for testing. The data is proprietary Amazon shoe data in six categories, so it cannot be reproduced here.
- **Reported numbers:** The paper gives percentage improvements in weighted AUC over a catalog-size baseline (17 to 21% for the main algorithm across the six datasets, Table 1) and no absolute AUC values that we could read. These numbers are not comparable to ours. Use the paper for method and split design only.

## How prior work approached this task

- Fit is framed as a three-class ordinal outcome (small, fit, large) and scored with AUC, which suits imbalanced labels better than accuracy.
- The common core is a latent size or latent factor for each customer and product, with the fit decided by their difference. Sembium et al. introduced it and Misra et al. extended it to K dimensions.
- Label imbalance is handled inside the model (prototype selection with metric learning in Misra et al.), not left to the metric alone.
- Later work feeds customer and article features with entity embeddings into one network, and reports a gain over the latent-factor models on the same Rent the Runway data.
- Splits differ: random 80/10/10 on the public data, time-based 80/20 on the Amazon data. Any comparison with reported numbers must name the split, and the exact random split of Misra et al. is not available.

## Comparison with our results (I-15)

Our numbers are test-split scores from `notebooks/04_eval.ipynb` (I-12), run on the full data. Reported numbers are copied from the sections above.

| Source | Reported model | Reported metric | Reported | Our model | Our metric | Ours |
|---|---|---|---|---|---|---|
| Misra et al. 2018 | 1-LV-LR | average AUC | 0.61 | LogisticRegression | average AUC | 0.620 |
| Misra et al. 2018 | K-LF-ML (proposed) | average AUC | 0.719 | LatentFactorFit | average AUC | 0.758 |

Sheikh et al. 2019 has no row. They report micro-averaged AUC (0.692 for their MLP baseline, 0.749 for SFnet). Micro averaging pools the three one-vs-rest problems into one ranking, and a constant score that only reflects the class frequencies already ranks "fit" rows above the rest. The majority baseline, which knows nothing about any row, scores a micro AUC of 0.804 on our test split (printed by the comparison cell in `notebooks/04_eval.ipynb`), higher than both reported values. A micro AUC therefore says more about the label mix than about the model, and we do not compare against it.

Caveats, which apply to every row:

- **Split.** Ours, Misra et al. and Sheikh et al. all use a random 80/10/10 split, but the exact split of Misra et al. is not available. Sembium et al. use a time-based split. Our interval (about 0.014 wide for average AUC) covers test-row sampling in one split only.
- **Averaging.** Our average AUC is the one-vs-rest mean over three classes. Misra et al. do not define their average.
- **Rows.** Our loader drops 189 exact duplicate lines (192,355 rows remain). We do not know whether the paper kept them.
- **Models.** We have no metric learning and no neural network.
- **Sembium et al. 2017** reports only percentage gains on proprietary data, so it has no row.

Reading: our logistic regression lands near the 0.61 of the Misra baseline, and our main model scores above their proposed model on the same metric. With these caveats the table shows that our numbers are in the same range as the literature. It does not show that we beat it.
