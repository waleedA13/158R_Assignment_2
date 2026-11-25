"""Unit tests for parsing and train-only preprocessing in src/data.py (I-07)."""

import math

import pandas as pd
import pytest

from src import data


def raw(**overrides) -> dict:
    row = {
        "txn_id": 0,
        "fit": "fit",
        "user_id": "1",
        "item_id": "9",
        "size": 8,
        "weight": "137lbs",
        "height": "5' 8\"",
        "bust size": "34d",
        "age": "28",
        "body type": "hourglass",
        "category": "dress",
        "rented for": "wedding",
        "rating": "10",
        "review_text": "Runs small.",
        "review_summary": "Cute",
        "review_date": "April 20, 2016",
    }
    row.update(overrides)
    return row


# ---- parse: units and formats
def test_parse_weight_and_height_to_numbers():
    p = data.parse(pd.DataFrame([raw()]))
    assert p.loc[0, "weight_lbs"] == 137
    assert p.loc[0, "height_in"] == 68


@pytest.mark.parametrize(
    "bust, band, cup",
    [("34d", 34, 4), ("32aa", 32, 0), ("34d+", 34, 5), ("36dd", 36, 5), ("34ddd/e", 34, 6), ("38j", 38, 11)],
)
def test_parse_bust_size_into_band_and_ordered_cup(bust, band, cup):
    p = data.parse(pd.DataFrame([raw(**{"bust size": bust})]))
    assert (p.loc[0, "bust_band"], p.loc[0, "cup"]) == (band, cup)


@pytest.mark.parametrize(
    "age, expected", [("28", 28), ("15", 15), ("90", 90), ("0", None), ("116", None), (None, None)]
)
def test_parse_age_outside_15_to_90_becomes_missing(age, expected):
    value = data.parse(pd.DataFrame([raw(age=age)])).loc[0, "age"]
    assert math.isnan(value) if expected is None else value == expected


def test_parse_missing_values_become_nan():
    p = data.parse(pd.DataFrame([raw(weight=None, height=None, **{"bust size": None})]))
    assert p[["weight_lbs", "height_in", "bust_band", "cup"]].isna().all(axis=None)


def test_parse_drops_fields_written_after_the_rental():
    p = data.parse(pd.DataFrame([raw()]))
    for col in data.POST_RENTAL:
        assert col not in p.columns
    for col in ("txn_id", "fit", "user_id", "item_id", "size"):
        assert col in p.columns


# ---- preprocess: train-only fitting
def three(train_weights, other_weights):
    train = pd.DataFrame([raw(txn_id=i, weight=w) for i, w in enumerate(train_weights)])
    other = pd.DataFrame([raw(txn_id=100 + i, weight=w) for i, w in enumerate(other_weights)])
    return data.preprocess(train, other, other.copy())


def test_missing_values_are_filled_with_the_train_median_and_flagged():
    train_p, valid_p, _ = three(["100lbs", "200lbs", "300lbs"], [None, "150lbs"])
    assert valid_p["weight_lbs"].tolist() == [200, 150]
    assert valid_p["weight_lbs_missing"].tolist() == [1, 0]
    assert train_p["weight_lbs_missing"].tolist() == [0, 0, 0]


def test_valid_and_test_values_never_change_the_fill_value():
    _, a, _ = three(["100lbs", "200lbs", "300lbs"], [None, "50lbs"])
    _, b, _ = three(["100lbs", "200lbs", "300lbs"], [None, "290lbs"])
    assert a.loc[0, "weight_lbs"] == b.loc[0, "weight_lbs"] == 200


def test_preprocess_keeps_rows_and_order_and_leaves_no_numeric_nan():
    train = pd.DataFrame([raw(txn_id=i, age=a) for i, a in enumerate(["28", None, "116"])])
    valid = pd.DataFrame([raw(txn_id=10, **{"bust size": None, "body type": None})])
    train_p, valid_p, test_p = data.preprocess(train, valid, valid.copy())
    assert train_p["txn_id"].tolist() == [0, 1, 2] and len(valid_p) == len(test_p) == 1
    for part in (train_p, valid_p, test_p):
        assert not part[list(data.NUMERIC)].isna().any(axis=None)
    assert valid_p.loc[0, "body_type"] == "unknown"


def test_preprocess_does_not_modify_its_inputs():
    train = pd.DataFrame([raw()])
    before = train.copy()
    data.preprocess(train, train.copy(), train.copy())
    pd.testing.assert_frame_equal(train, before)
