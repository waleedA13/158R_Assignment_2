"""Unit tests for src/metrics.py with hand-computed values."""

import numpy as np
import pandas as pd
import pytest

from src import metrics

Y = ["small", "fit", "large", "fit"]


def test_classes_order():
    assert metrics.CLASSES == ("small", "fit", "large")


def test_average_auc_perfect_ranking_is_one():
    proba = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 0]], dtype=float)
    assert metrics.average_auc(Y, proba) == pytest.approx(1.0)


def test_average_auc_constant_scores_is_half():
    proba = np.tile([0.2, 0.6, 0.2], (4, 1))
    assert metrics.average_auc(Y, proba) == pytest.approx(0.5)


def test_average_auc_hand_computed_mixed_case():
    # Columns: small, fit, large. Rows: true small, fit, large, fit.
    # small vs rest: positive 0.9 beats negatives 0.1, 0, 0 -> 3/3 = 1.0
    # fit vs rest: positives 0.7, 0.4 vs negatives 0.1, 0.5 -> 3 of 4 pairs = 0.75
    # large vs rest: positive 0.5 vs negatives 0, 0.2, 0.6 -> 2 of 3 pairs = 2/3
    proba = np.array(
        [
            [0.9, 0.1, 0.0],
            [0.1, 0.7, 0.2],
            [0.0, 0.5, 0.5],
            [0.0, 0.4, 0.6],
        ]
    )
    assert metrics.average_auc(Y, proba) == pytest.approx((1.0 + 0.75 + 2 / 3) / 3)


def test_macro_f1_hand_computed():
    # true: small fit large fit; pred: small fit fit fit
    # small F1 = 1.0; fit: precision 2/3, recall 1 -> 0.8; large: no hit -> 0.0; macro = 0.6
    pred = ["small", "fit", "fit", "fit"]
    assert metrics.macro_f1(Y, pred) == pytest.approx(0.6)


def test_macro_f1_all_correct_is_one():
    assert metrics.macro_f1(Y, Y) == pytest.approx(1.0)


def test_average_auc_uses_dataframe_column_names_not_position():
    y = ["small", "fit", "large", "fit"]
    perfect = pd.DataFrame(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 0]], columns=list(metrics.CLASSES), dtype=float
    )
    shuffled = perfect[["fit", "large", "small"]]  # sklearn's alphabetical classes_ order
    assert metrics.average_auc(y, shuffled) == 1.0


def _noisy_scores(n=300, seed=0):
    rng = np.random.default_rng(seed)
    y = rng.choice(metrics.CLASSES, size=n, p=[0.15, 0.7, 0.15])
    onehot = np.array([[c == k for k in metrics.CLASSES] for c in y], dtype=float)
    raw = rng.dirichlet([1, 1, 1], size=n) + onehot
    return y, pd.DataFrame(raw / raw.sum(axis=1, keepdims=True), columns=list(metrics.CLASSES))


def test_bootstrap_ci_brackets_the_point_estimate():
    y, proba = _noisy_scores()
    ci = metrics.bootstrap_ci(y, proba, n_boot=200, seed=1)
    auc, f1 = metrics.average_auc(y, proba), metrics.macro_f1(y, proba.idxmax(axis=1))
    assert ci["average AUC"][0] < auc < ci["average AUC"][1]
    assert ci["macro-F1"][0] < f1 < ci["macro-F1"][1]


def test_bootstrap_ci_same_seed_same_interval():
    y, proba = _noisy_scores()
    assert metrics.bootstrap_ci(y, proba, n_boot=50, seed=3) == metrics.bootstrap_ci(
        y, proba, n_boot=50, seed=3
    )


def test_bootstrap_ci_perfect_scores_have_zero_width():
    y = np.array(Y * 10)
    proba = np.array([{"small": [1, 0, 0], "fit": [0, 1, 0], "large": [0, 0, 1]}[c] for c in y], dtype=float)
    ci = metrics.bootstrap_ci(y, proba, n_boot=50)
    assert ci["average AUC"] == (1.0, 1.0) and ci["macro-F1"] == (1.0, 1.0)


def test_bootstrap_ci_constant_scores_give_half():
    y = np.array(Y * 10)
    ci = metrics.bootstrap_ci(y, np.tile([0.2, 0.6, 0.2], (len(y), 1)), n_boot=50)
    assert ci["average AUC"] == (0.5, 0.5)


def test_bootstrap_ci_skips_resamples_missing_a_class():
    y = np.array(["fit"] * 9 + ["small"] * 2 + ["large"])  # a resample often drops the lone "large"
    proba = np.tile([0.3, 0.4, 0.3], (len(y), 1))
    ci = metrics.bootstrap_ci(y, proba, n_boot=100)
    assert ci["average AUC"] == (0.5, 0.5)
