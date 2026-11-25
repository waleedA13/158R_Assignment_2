"""Unit tests for src/metrics.py with hand-computed values."""

import numpy as np
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
