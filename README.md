# 158R_Assignment_2

CSE 158R Assignment 2: one predictive task on a public dataset, delivered as a Jupyter notebook exported to HTML (`workbook.html`) plus a ~20 minute presentation video. Planning, protocol and current status live in `HANDOFF.md`; the issue backlog with agent prompts is in `ISSUES.md`; agent rules are in `AGENTS.md`.

## Setup

Requires **Python 3.12** (pinned in `.python-version`).

```bash
# macOS, once
brew install python@3.12 libmagic

# in the repo root
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt   # project + test/check tools (requirements.txt is project only)
```

## Layout

| Path | What it holds |
|---|---|
| `src/` | All reusable logic: data loading and split (`data.py`), metrics (`metrics.py`), models (`models.py`) |
| `notebooks/` | Per-section draft notebooks |
| `workbook.ipynb` / `workbook.html` | Final assembled notebook and its export (the submission) |
| `tests/` | `unit/`, `integration/`, `e2e/` tests and small `fixtures/` data |
| `scripts/` | GitHub issue tools and (later) export and submission checks |
| `docs/` | Spec, requirements summary, dataset decision, related work |
| `data/` | Raw and processed data. Not committed |

## Before submitting

```bash
python scripts/check_submission.py   # runs the course autograder's checks on workbook.html and video_url.txt
```
It mirrors the autograder code in `docs/spec.pdf`: both files present, `workbook.html` starts with `<!DOCTYPE html>`, and for a Google Drive link the file downloads, is over 1 MB and is `video/mp4`. YouTube links skip the download checks.

## Data

Rent the Runway clothing fit data (UCSD McAuley lab), chosen in `docs/decision.md`.

1. Download https://mcauleylab.ucsd.edu/public_datasets/data/renttherunway/renttherunway_final_data.json.gz (31 MB, listed on https://cseweb.ucsd.edu/~jmcauley/datasets.html).
2. Put it, still gzipped and with the same name, at `data/raw/renttherunway_final_data.json.gz`. `data/` is gitignored, so it is never committed.
3. Check it: `python -m src.data` should print 192355 transactions and these split sizes and fingerprints:

```
train  153885  ...  hash=b4ab00b3355f
valid   19235  ...  hash=405c410be45b
test    19235  ...  hash=3c40a84ea105
```

In code, always use the shared loader and split (from a notebook in `notebooks/`, add `sys.path.append("..")` first):

```python
from src.data import load, split

train, valid, test = split(load())
```

Tests and CI use the synthetic sample in `tests/fixtures/` instead (`DATA_DIR=tests/fixtures`); `scripts/make_fixture.py` regenerates it.
