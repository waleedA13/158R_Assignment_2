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

## Data

Download instructions are added with I-04, once the dataset is chosen (I-03).
