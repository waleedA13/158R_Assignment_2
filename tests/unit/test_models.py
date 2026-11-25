"""Unit tests for the model interface and the MajorityClass baseline in src/models.py."""

import numpy as np
import pandas as pd
import pytest

from src import metrics, models


def frame(labels) -> pd.DataFrame:
    return pd.DataFrame({"txn_id": range(len(labels)), "fit": labels})


TRAIN = frame(["fit"] * 6 + ["small"] * 2 + ["large"] * 2)


def test_fit_returns_self():
    m = models.MajorityClass()
    assert m.fit(TRAIN) is m


def test_predict_proba_shape_columns_and_row_alignment():
    df = frame(["small", "fit", "large"]).set_index(pd.Index([10, 20, 30]))
    proba = models.MajorityClass().fit(TRAIN).predict_proba(df)
    assert list(proba.columns) == list(metrics.CLASSES)
    assert proba.shape == (3, 3)
    assert list(proba.index) == [10, 20, 30]


def test_probabilities_are_train_frequencies_and_sum_to_one():
    proba = models.MajorityClass().fit(TRAIN).predict_proba(frame(["fit"] * 4))
    np.testing.assert_allclose(proba.sum(axis=1), 1.0)
    assert proba.iloc[0].to_dict() == pytest.approx({"small": 0.2, "fit": 0.6, "large": 0.2})


def test_predict_is_the_majority_label_for_every_row():
    df = frame(["small", "large", "fit"])
    pred = models.MajorityClass().fit(TRAIN).predict(df)
    assert list(pred) == ["fit"] * 3
    assert list(pred.index) == list(df.index)


def test_fit_uses_the_train_frame_only():
    m = models.MajorityClass().fit(frame(["large"] * 3 + ["fit"]))
    assert m.predict(frame(["fit"] * 10)).iloc[0] == "large"  # labels of the scored frame are ignored


def test_predict_proba_does_not_need_the_label_column():
    m = models.MajorityClass().fit(TRAIN)
    assert len(m.predict_proba(pd.DataFrame({"txn_id": [1, 2]}))) == 2


def test_majority_baseline_auc_is_half():
    m = models.MajorityClass().fit(TRAIN)
    valid = frame(["small", "fit", "large", "fit"])
    assert metrics.average_auc(valid["fit"], m.predict_proba(valid)) == pytest.approx(0.5)
