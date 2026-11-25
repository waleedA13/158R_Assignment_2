"""Integration tests on the committed sample in tests/fixtures/ (never the real data)."""

from pathlib import Path

import pytest

from src import data

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


@pytest.fixture
def df(monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(FIXTURES))
    return data.load()


def test_fixture_has_the_raw_schema(df):
    for col in ["fit", "user_id", "item_id", "size", "rating", "weight", "height", "bust size", "age"]:
        assert col in df.columns
    assert set(df["fit"]) == {"fit", "small", "large"}


def test_fixture_duplicates_are_dropped(df):
    assert len(df) == 200
    assert df["txn_id"].is_unique


def test_load_then_split_on_fixture(df):
    train, valid, test = data.split(df)
    assert (len(train), len(valid), len(test)) == (160, 20, 20)
    seen = set(train["txn_id"]) | set(valid["txn_id"]) | set(test["txn_id"])
    assert seen == set(df["txn_id"])


def test_load_split_preprocess_on_fixture(df):
    train, valid, test = data.preprocess(*data.split(df))
    assert (len(train), len(valid), len(test)) == (160, 20, 20)
    for part in (train, valid, test):
        assert not part[list(data.NUMERIC)].isna().any(axis=None)
        assert set(data.POST_RENTAL).isdisjoint(part.columns)
