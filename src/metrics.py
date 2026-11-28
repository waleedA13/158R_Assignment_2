"""Evaluation metrics used everywhere in the report (I-08).

Both metrics come from docs/decision.md. Labels are the `fit` column with classes CLASSES.
The primary metric needs scores, so models return class probabilities (see src/models.py).
"""

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, roc_auc_score

CLASSES = ("small", "fit", "large")


def average_auc(y_true, proba) -> float:
    """Primary metric: one-vs-rest AUC for each class, averaged with equal weight.

    `proba` is a DataFrame with a column per class (matched by name), or an (n, 3) array with
    columns in CLASSES order. Rows sum to 1.
    Calls sklearn `roc_auc_score(multi_class="ovr", average="macro")`, after reordering the columns
    to the sorted label order sklearn requires.
    Constant scores give 0.5, a perfect ranking gives 1.0.
    """
    if isinstance(proba, pd.DataFrame):
        proba = proba[list(CLASSES)]  # by name: sklearn models return columns in alphabetical order
    order = np.argsort(CLASSES)  # sklearn requires `labels` sorted, so reorder the columns to match
    scores = np.asarray(proba)[:, order]
    return float(roc_auc_score(y_true, scores, multi_class="ovr", average="macro", labels=sorted(CLASSES)))


def macro_f1(y_true, y_pred) -> float:
    """Secondary metric: F1 per class on hard labels, averaged with equal weight.

    Calls sklearn `f1_score(average="macro", labels=CLASSES)`. A class that is never predicted
    scores 0 for that class.
    """
    return float(f1_score(y_true, y_pred, average="macro", labels=list(CLASSES), zero_division=0))


def bootstrap_ci(y_true, proba, n_boot: int = 1000, seed: int = 0, level: float = 0.95) -> dict:
    """Percentile bootstrap interval for both metrics, from one set of test predictions.

    Resamples rows with replacement `n_boot` times (fixed `seed`) and recomputes `average_auc` and
    `macro_f1` (hard labels = most likely class). Returns {"average AUC": (low, high), "macro-F1":
    (low, high)}. A resample that misses a class is skipped, since AUC is undefined without it.
    """
    y = np.asarray(y_true)
    scores = proba[list(CLASSES)].to_numpy() if isinstance(proba, pd.DataFrame) else np.asarray(proba)
    labels = np.asarray(CLASSES)[scores.argmax(axis=1)]
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(n_boot):
        i = rng.integers(0, len(y), len(y))
        if len(set(y[i])) == len(CLASSES):
            draws.append((average_auc(y[i], scores[i]), macro_f1(y[i], labels[i])))
    tails = [100 * (1 - level) / 2, 100 * (1 + level) / 2]
    return {
        name: tuple(float(v) for v in np.percentile([d[k] for d in draws], tails))
        for k, name in enumerate(("average AUC", "macro-F1"))
    }


if __name__ == "__main__":
    y = ["small", "fit", "large", "fit"]
    perfect = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 0]], dtype=float)
    assert average_auc(y, perfect) == 1.0
    assert average_auc(y, np.tile([0.2, 0.6, 0.2], (4, 1))) == 0.5
    mixed = np.array([[0.9, 0.1, 0.0], [0.1, 0.7, 0.2], [0.0, 0.5, 0.5], [0.0, 0.4, 0.6]])
    assert abs(average_auc(y, mixed) - (1 + 0.75 + 2 / 3) / 3) < 1e-12  # 1.0, 3/4, 2/3 by hand
    assert abs(macro_f1(y, ["small", "fit", "fit", "fit"]) - 0.6) < 1e-12  # (1.0 + 0.8 + 0) / 3
    print("metrics self-check passed")
