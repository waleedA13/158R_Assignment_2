"""Data loading, the shared train/valid/test split, and preprocessing (I-04, I-07).

Every notebook and model uses `load()` and `split()` from here, so the whole team
works on the same rows and the same split (see docs/decision.md).
"""

import gzip
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE_NAME = "renttherunway_final_data.json.gz"
DEFAULT_DATA_DIR = ROOT / "data" / "raw"
SEED = 158
PROPORTIONS = (0.8, 0.1, 0.1)  # train, valid, test


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
