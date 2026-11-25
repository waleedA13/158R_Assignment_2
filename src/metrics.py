"""Evaluation metrics used everywhere in the report (I-08).

Both metrics come from docs/decision.md. Labels are the `fit` column with classes CLASSES.
The primary metric needs scores, so models return class probabilities (see src/models.py).
"""

import numpy as np
from sklearn.metrics import f1_score, roc_auc_score

CLASSES = ("small", "fit", "large")


def average_auc(y_true, proba) -> float:
    """Primary metric: one-vs-rest AUC for each class, averaged with equal weight.

    `proba` is an (n, 3) array or DataFrame with columns in CLASSES order and rows summing to 1.
    Calls sklearn `roc_auc_score(multi_class="ovr", average="macro")`, after reordering the columns
    to the sorted label order sklearn requires.
    Constant scores give 0.5, a perfect ranking gives 1.0.
    """
    order = np.argsort(CLASSES)  # sklearn requires `labels` sorted, so reorder the columns to match
    scores = np.asarray(proba)[:, order]
    return float(roc_auc_score(y_true, scores, multi_class="ovr", average="macro", labels=sorted(CLASSES)))


def macro_f1(y_true, y_pred) -> float:
    """Secondary metric: F1 per class on hard labels, averaged with equal weight.

    Calls sklearn `f1_score(average="macro", labels=CLASSES)`. A class that is never predicted
    scores 0 for that class.
    """
    return float(f1_score(y_true, y_pred, average="macro", labels=list(CLASSES), zero_division=0))


if __name__ == "__main__":
    y = ["small", "fit", "large", "fit"]
    perfect = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 0]], dtype=float)
    assert average_auc(y, perfect) == 1.0
    assert average_auc(y, np.tile([0.2, 0.6, 0.2], (4, 1))) == 0.5
    mixed = np.array([[0.9, 0.1, 0.0], [0.1, 0.7, 0.2], [0.0, 0.5, 0.5], [0.0, 0.4, 0.6]])
    assert abs(average_auc(y, mixed) - (1 + 0.75 + 2 / 3) / 3) < 1e-12  # 1.0, 3/4, 2/3 by hand
    assert abs(macro_f1(y, ["small", "fit", "fit", "fit"]) - 0.6) < 1e-12  # (1.0 + 0.8 + 0) / 3
    print("metrics self-check passed")
