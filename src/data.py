"""Data loading, the shared train/valid/test split, and preprocessing (I-04, I-07).

Every notebook and model uses `load()` and `split()` from here, so the whole team
works on the same rows and the same split (see docs/decision.md).
"""

import gzip
import hashlib
import json
import os
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE_NAME = "renttherunway_final_data.json.gz"
DEFAULT_DATA_DIR = ROOT / "data" / "raw"
SEED = 158
PROPORTIONS = (0.8, 0.1, 0.1)  # train, valid, test

# Preprocessing (I-07)
POST_RENTAL = (
    "rating",
    "review_text",
    "review_summary",
    "review_date",
)  # written after the outcome: leak fit
NUMERIC = ("weight_lbs", "height_in", "bust_band", "cup", "age")
CATEGORICAL = ("body_type", "category", "rented_for")
CUP_ORDER = {"aa": 0, "a": 1, "b": 2, "c": 3, "d": 4, "d+": 5, "dd": 5, "ddd/e": 6, "f": 7}
CUP_ORDER.update({cup: 8 + i for i, cup in enumerate("ghij")})  # g=8 ... j=11
AGE_RANGE = (15, 90)  # outside this is a data-entry error (the raw file has ages 0 to 117)


def data_dir() -> Path:
    """Folder with the raw file: $DATA_DIR if set (relative to the repo root), else data/raw."""
    folder = Path(os.environ.get("DATA_DIR", DEFAULT_DATA_DIR))
    return folder if folder.is_absolute() else ROOT / folder


def load(folder: str | Path | None = None) -> pd.DataFrame:
    """Read the Rent the Runway file as raw values, one row per transaction.

    - `txn_id` is the 0-based line number in the raw file, so every row can be traced back.
    - Exact duplicate lines are dropped, keeping the first. 189 lines in the real file are exact
      copies of an earlier line; keeping them could put the same transaction in train and test.
    - Values are kept as in the file (e.g. weight "137lbs", height 5' 8"). Parsing is I-07.
    """
    path = Path(folder or data_dir()) / RAW_FILE_NAME
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. See README.md, section 'Data', for the download.")
    rows, seen = [], set()
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for txn_id, line in enumerate(f):
            if not line.strip():
                continue
            record = json.loads(line)
            key = json.dumps(record, sort_keys=True)
            if key in seen:
                continue
            seen.add(key)
            rows.append({"txn_id": txn_id, **record})
    return pd.DataFrame(rows)


def split(df: pd.DataFrame, seed: int = SEED) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Random 80/10/10 split of transactions into (train, valid, test), fixed by `seed`.

    Rows are ordered by `txn_id` before shuffling, so the result does not depend on the input
    order. Each transaction lands in exactly one split. The same user or item can appear in
    several splits on purpose: the latent factor models need to have seen a user to score them.
    Leakage rule: anything fitted from data (encoders, means, vocabularies) uses `train` only.
    The test split is scored once, in I-12.
    """
    ordered = df.sort_values("txn_id").reset_index(drop=True)
    perm = np.random.default_rng(seed).permutation(len(ordered))
    n_valid = int(len(ordered) * PROPORTIONS[1])
    n_test = int(len(ordered) * PROPORTIONS[2])
    parts = (perm[n_test + n_valid :], perm[n_test : n_test + n_valid], perm[:n_test])
    return tuple(ordered.iloc[np.sort(p)].reset_index(drop=True) for p in parts)


def _number(value, pattern: str) -> float:
    match = re.fullmatch(pattern, str(value)) if isinstance(value, str) else None
    return float(match.group(1)) if match else np.nan


def _height_inches(value) -> float:
    match = re.fullmatch(r"(\d+)' (\d+)\"", value) if isinstance(value, str) else None
    return 12 * int(match.group(1)) + int(match.group(2)) if match else np.nan


def _bust(value) -> tuple[float, float]:
    match = re.fullmatch(r"(\d+)(.+)", value) if isinstance(value, str) else None
    if not match or match.group(2) not in CUP_ORDER:
        return np.nan, np.nan
    return float(match.group(1)), float(CUP_ORDER[match.group(2)])


def parse(df: pd.DataFrame) -> pd.DataFrame:
    """Turn raw rows into typed model inputs. Row by row: nothing is learned from the data here.

    - weight "137lbs" -> weight_lbs 137; height 5' 8" -> height_in 68
    - bust size "34ddd/e" -> bust_band 34, cup 6 (ordered scale CUP_ORDER; d+ and dd share a step)
    - age outside AGE_RANGE -> NaN
    - drops POST_RENTAL fields (rating and the review), which are written after the fit is known
    - renames "body type" / "rented for" to body_type / rented_for
    """
    out = pd.DataFrame(
        {
            "txn_id": df["txn_id"],
            "fit": df["fit"],
            "user_id": df["user_id"],
            "item_id": df["item_id"],
            "size": df["size"].astype(float),
            "weight_lbs": df["weight"].map(lambda v: _number(v, r"(\d+)lbs")),
            "height_in": df["height"].map(_height_inches),
        },
        index=df.index,
    )
    bust = df["bust size"].map(_bust)
    out["bust_band"] = bust.map(lambda b: b[0])
    out["cup"] = bust.map(lambda b: b[1])
    age = df["age"].map(lambda v: _number(v, r"(\d+)"))
    out["age"] = age.where(age.between(*AGE_RANGE))
    for col in CATEGORICAL:
        out[col] = df[col.replace("_", " ")].astype(object)
    return out


def preprocess(
    train: pd.DataFrame, valid: pd.DataFrame, test: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Parse all three splits, then fill missing values using statistics from `train` only.

    Each NUMERIC column gets a `<col>_missing` 0/1 flag and is filled with the train median.
    Missing CATEGORICAL values become "unknown". Rows and their order are unchanged.
    """
    parts = [parse(part) for part in (train, valid, test)]
    medians = parts[0][list(NUMERIC)].median()
    for part in parts:
        for col in NUMERIC:
            part[f"{col}_missing"] = part[col].isna().astype(int)
            part[col] = part[col].fillna(medians[col])
        for col in CATEGORICAL:
            part[col] = part[col].fillna("unknown")
    return tuple(parts)


def ids_hash(df: pd.DataFrame) -> str:
    """Short fingerprint of a split's transactions, to confirm two runs produced the same split."""
    joined = ",".join(map(str, sorted(df["txn_id"])))
    return hashlib.sha256(joined.encode()).hexdigest()[:12]


if __name__ == "__main__":
    frame = load()
    print(f"loaded {len(frame)} transactions from {data_dir()}")
    for name, part in zip(("train", "valid", "test"), split(frame), strict=True):
        dist = part["fit"].value_counts(normalize=True).round(3).to_dict()
        print(f"{name:5} {len(part):7}  fit={dist}  hash={ids_hash(part)}")
