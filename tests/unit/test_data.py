"""Unit tests for the shared loader and split in src/data.py."""

import gzip
import json

import pandas as pd
import pytest

from src import data


def frame(n: int) -> pd.DataFrame:
    return pd.DataFrame({"txn_id": range(n), "fit": ["fit"] * n})


def ids(df: pd.DataFrame) -> list[int]:
    return sorted(df["txn_id"].tolist())


# ---- split
def test_split_is_deterministic():
    a = data.split(frame(1000))
    b = data.split(frame(1000))
    assert [ids(x) for x in a] == [ids(x) for x in b]


def test_split_uses_seed_158_by_default_and_other_seeds_differ():
    assert data.SEED == 158
    assert ids(data.split(frame(1000))[2]) != ids(data.split(frame(1000), seed=1)[2])


def test_split_proportions_are_80_10_10():
    train, valid, test = data.split(frame(1000))
    assert (len(train), len(valid), len(test)) == (800, 100, 100)


def test_splits_are_disjoint_and_cover_every_row():
    train, valid, test = data.split(frame(997))
    all_ids = ids(train) + ids(valid) + ids(test)
    assert sorted(all_ids) == list(range(997))
    assert len(set(all_ids)) == 997


def test_split_does_not_depend_on_input_row_order():
    df = frame(500)
    shuffled = df.sample(frac=1, random_state=0)
    assert [ids(x) for x in data.split(df)] == [ids(x) for x in data.split(shuffled)]


def test_split_does_not_modify_its_input():
    df = frame(100)
    before = df.copy()
    data.split(df)
    pd.testing.assert_frame_equal(df, before)


# ---- load
def write_raw(folder, rows):
    with gzip.open(folder / data.RAW_FILE_NAME, "wt") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def test_load_reads_data_dir_at_call_time(tmp_path, monkeypatch):
    write_raw(tmp_path, [{"fit": "fit", "user_id": "1", "item_id": "9", "size": 4}])
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    df = data.load()
    assert len(df) == 1 and df.loc[0, "user_id"] == "1"


def test_load_keeps_raw_values_and_adds_txn_id_from_line_order(tmp_path):
    write_raw(tmp_path, [{"fit": "small", "weight": "137lbs"}, {"fit": "large", "weight": None}])
    df = data.load(tmp_path)
    assert df["txn_id"].tolist() == [0, 1]
    assert df.loc[0, "weight"] == "137lbs"


def test_load_drops_exact_duplicate_rows_keeping_the_first(tmp_path):
    r = {"fit": "fit", "user_id": "1", "item_id": "9", "size": 4}
    write_raw(tmp_path, [r, {**r, "size": 5}, r])
    df = data.load(tmp_path)
    assert df["txn_id"].tolist() == [0, 1]


def test_load_explains_a_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError, match="README"):
        data.load(tmp_path)
