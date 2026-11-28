"""Unit tests for the model interface and the MajorityClass baseline in src/models.py."""

import numpy as np
import pandas as pd
import pytest

from src import data, metrics, models


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


# LogisticRegression (I-09): rows look like the output of src.data.preprocess()
def features(size, labels=None) -> pd.DataFrame:
    df = pd.DataFrame({"txn_id": range(len(size)), "size": np.asarray(size, dtype=float)})
    for col in data.NUMERIC:
        df[col] = 1.0
        df[f"{col}_missing"] = 0
    for col in data.CATEGORICAL:
        df[col] = "unknown"
    if labels is not None:
        df["fit"] = labels
    return df


def separable(n=60):
    size = np.random.default_rng(0).uniform(0, 30, n)
    labels = np.where(size < 10, "small", np.where(size < 20, "fit", "large"))
    return features(size, labels)


def test_logreg_fit_returns_self():
    m = models.LogisticRegression()
    assert m.fit(separable()) is m


def test_logreg_proba_columns_rows_sum_to_one_and_index_aligned():
    df = separable().set_index(pd.Index(range(100, 160)))
    proba = models.LogisticRegression().fit(separable()).predict_proba(df)
    assert list(proba.columns) == list(metrics.CLASSES)
    assert proba.shape == (60, 3)
    assert list(proba.index) == list(df.index)
    np.testing.assert_allclose(proba.sum(axis=1), 1.0)


def test_logreg_does_not_read_the_label_column_at_predict_time():
    m = models.LogisticRegression().fit(separable())
    df = separable()
    pd.testing.assert_frame_equal(
        m.predict_proba(df.drop(columns="fit")), m.predict_proba(df.assign(fit="small"))
    )


def test_logreg_beats_majority_when_size_separates_classes():
    train, valid = separable(300), separable(90)
    auc = {}
    for model in (models.MajorityClass(), models.LogisticRegression()):
        proba = model.fit(train).predict_proba(valid)
        auc[type(model).__name__] = metrics.average_auc(valid["fit"], proba)
    assert auc["MajorityClass"] == pytest.approx(0.5)
    assert auc["LogisticRegression"] > 0.9


def test_logreg_predict_returns_labels_from_the_classes():
    pred = models.LogisticRegression().fit(separable()).predict(separable())
    assert set(pred) <= set(metrics.CLASSES)


def test_logreg_handles_a_category_unseen_in_train():
    m = models.LogisticRegression().fit(separable())
    df = features([5.0, 25.0]).assign(body_type="never seen")
    assert len(m.predict_proba(df)) == 2


# LatentFactorFit (I-10): same feature rows plus user_id and item_id
def with_ids(df: pd.DataFrame, users, items) -> pd.DataFrame:
    return df.assign(user_id=list(users), item_id=list(items))


def by_item(n, seed=0):
    """Label depends only on the item, so no feature column carries any signal."""
    rng = np.random.default_rng(seed)
    item = rng.integers(0, 20, n)
    labels = np.array(["small", "fit", "large"])[item % 3]
    df = features(np.ones(n), labels)
    return with_ids(df, [f"u{u}" for u in rng.integers(0, 50, n)], [f"i{i}" for i in item])


def test_latent_fit_returns_self():
    m = models.LatentFactorFit(K=2)
    assert m.fit(by_item(120)) is m


def test_latent_proba_columns_rows_sum_to_one_and_index_aligned():
    df = by_item(60).set_index(pd.Index(range(100, 160)))
    proba = models.LatentFactorFit(K=2).fit(by_item(120)).predict_proba(df)
    assert list(proba.columns) == list(metrics.CLASSES)
    assert proba.shape == (60, 3)
    assert list(proba.index) == list(df.index)
    np.testing.assert_allclose(proba.sum(axis=1), 1.0)


def test_latent_handles_unseen_user_and_item():
    m = models.LatentFactorFit(K=2).fit(by_item(120))
    df = with_ids(features([5.0, 25.0]), ["new user", "u1"], ["i1", "new item"])
    proba = m.predict_proba(df)
    assert proba.shape == (2, 3) and proba.notna().all().all()


def test_latent_does_not_read_the_label_column_at_predict_time():
    m = models.LatentFactorFit(K=2).fit(by_item(120))
    df = by_item(40, seed=1)
    pd.testing.assert_frame_equal(
        m.predict_proba(df.drop(columns="fit")), m.predict_proba(df.assign(fit="small"))
    )


def test_latent_is_deterministic():
    a = models.LatentFactorFit(K=2).fit(by_item(120)).predict_proba(by_item(40, seed=1))
    b = models.LatentFactorFit(K=2).fit(by_item(120)).predict_proba(by_item(40, seed=1))
    pd.testing.assert_frame_equal(a, b)


def test_latent_beats_logreg_when_the_label_depends_on_the_item():
    train, valid = by_item(600), by_item(300, seed=1)
    auc = {}
    for model in (models.LogisticRegression(), models.LatentFactorFit(K=2)):
        proba = model.fit(train).predict_proba(valid)
        auc[type(model).__name__] = metrics.average_auc(valid["fit"], proba)
    assert auc["LogisticRegression"] < 0.6
    assert auc["LatentFactorFit"] > 0.9


def test_latent_class_weight_balanced_runs():
    proba = models.LatentFactorFit(K=0, class_weight="balanced").fit(by_item(120)).predict_proba(by_item(30))
    np.testing.assert_allclose(proba.sum(axis=1), 1.0)
