# ISSUES.md — 158R Assignment 2 backlog

Import-ready backlog. Each issue = one branch = one owner. Protocol and assumptions are in [`HANDOFF.md`](HANDOFF.md).
Section numbers refer to the spec's 5 graded sections (5 marks each).

## Label system

| Category | Labels | Use |
|---|---|---|
| `type:` | `setup` · `decision` · `data` · `model` · `eval` · `research` · `writing` · `presentation` · `submission` | What kind of work |
| `area:` | `s1-task` · `s2-eda` · `s3-modeling` · `s4-eval` · `s5-related` · `notebook` · `video` · `infra` | Graded section or artifact it feeds |
| `priority:` | `p0` (blocks submission) · `p1` (needed for a 4/5) · `p2` (stretch toward 5/5) | Order of pickup |
| `status:` | `ready` · `blocked` · `in-progress` · `review` · `done` | Claiming / filtering |
| `owner:` | `human` · `agent-ok` | `human` = agents must not do it (rubric penalizes auto-generated presentations; also accounts/uploads) |

GitHub colors (optional): type=blue, area=purple, priority p0 red / p1 orange / p2 yellow, status=gray, owner=green.

## Index

| ID | Title | Pri | Owner type | Depends on | Status |
|---|---|---|---|---|---|
| I-01 | Scaffold repo layout, deps, .gitignore | p0 | agent-ok | — | ready |
| I-02 | Add assignment spec to `docs/` | p1 | agent-ok | — | ready |
| I-03 | Decide dataset, predictive task, metric | p0 | human | — | ready |
| I-04 | Shared data loader + fixed split in `src/data.py` | p0 | agent-ok | I-01, I-03 | blocked |
| I-05 | Write Section 1: predictive task framing | p0 | agent-ok | I-03 | blocked |
| I-06 | EDA: dataset context, stats tables, plots | p0 | agent-ok | I-04 | blocked |
| I-07 | Document preprocessing pipeline | p1 | agent-ok | I-04 | blocked |
| I-08 | Implement trivial baselines | p0 | agent-ok | I-04 | blocked |
| I-09 | Implement course-model baseline | p0 | agent-ok | I-08 | blocked |
| I-10 | Implement main model + features | p1 | agent-ok | I-09 | blocked |
| I-11 | Tune hyperparameters on validation set | p1 | agent-ok | I-10 | blocked |
| I-12 | Evaluation harness + results table on test | p0 | agent-ok | I-08, I-09 | blocked |
| I-13 | Result plots, error analysis, metric justification | p1 | agent-ok | I-12 | blocked |
| I-14 | Related-work research notes with citations | p0 | agent-ok | I-03 | blocked |
| I-15 | Compare our results to reported results | p1 | agent-ok | I-12, I-14 | blocked |
| I-16 | Assemble and narrate `workbook.ipynb` | p0 | agent-ok | I-05–I-15 | blocked |
| I-17 | Execute + export `workbook.html` | p0 | agent-ok | I-16 | blocked |
| I-18 | Local submission checker script | p1 | agent-ok | I-01 | ready |
| I-19 | Build slide deck (human-written wording) | p0 | human | I-16 | blocked |
| I-20 | Record and edit ~20-min MP4 video | p0 | human | I-17, I-19 | blocked |
| I-21 | Upload video, write `video_url.txt`, submit | p0 | human | I-17, I-18, I-20 | blocked |
| I-22 | Complete peer grading (each member) | p0 | human | I-21 + instructor release | blocked |

---

### I-01 · Scaffold repo layout, deps, .gitignore
**Labels:** `type:setup` `area:infra` `priority:p0` `status:ready` `owner:agent-ok`
**Context & Scope:** Repo has only `README.md`. Create the layout in HANDOFF.md §2: `src/`, `notebooks/`, `scripts/`, `docs/`, `slides/`, `data/` (gitignored). Add `requirements.txt` (pandas, numpy, scikit-learn, matplotlib, jupyter, nbconvert; pin versions). Add `AGENTS.md` and `CLAUDE.md` as two-line pointers to `HANDOFF.md`. Expand `README.md` with a one-paragraph description + setup command.
**Acceptance Criteria:**
- [ ] `pip install -r requirements.txt` succeeds in a fresh venv
- [ ] `.gitignore` excludes `data/`, `*.mp4`, `.ipynb_checkpoints/`, `__pycache__/`, `.venv/`
- [ ] Empty `src/__init__.py`, `src/data.py`, `src/metrics.py`, `src/models.py` exist
- [ ] `AGENTS.md`/`CLAUDE.md` point to `HANDOFF.md`
**Dependencies:** none

### I-02 · Add assignment spec to `docs/`
**Labels:** `type:setup` `area:infra` `priority:p1` `status:ready` `owner:agent-ok`
**Context & Scope:** The spec lives outside the repo (`../Assignment 2/158 _ 258 2026 Assignment 2.pdf`). Copy to `docs/spec.pdf` and add `docs/requirements.md` with the 5 sections and their bullets so agents can read it as text.
**Acceptance Criteria:**
- [ ] `docs/spec.pdf` committed
- [ ] `docs/requirements.md` lists all 5 sections, the rubric (0–5), the submission files and the autograder checks
**Dependencies:** none

### I-03 · Decide dataset, predictive task, metric
**Labels:** `type:decision` `area:s1-task` `priority:p0` `status:ready` `owner:human`
**Context & Scope:** Nothing is chosen. Pick a dataset (e.g. from cseweb.ucsd.edu/~jmcauley/datasets.html or the Assignment 1 data) and a task relevant to course content (rating prediction, read/purchase prediction, classification from text, etc.). Record it in `docs/decision.md`. Agents may draft 2–3 candidate options with pros/cons; humans choose.
**Acceptance Criteria:**
- [ ] `docs/decision.md` states: dataset + source URL + size, task (inputs → output), primary metric + secondary metric, ≥2 planned baselines (≥1 from course), at least one course model
- [ ] Dataset size is workable on a laptop (or subsampling plan documented)
- [ ] Every group member has agreed (names listed)
- [ ] HANDOFF.md §0 A4 marked confirmed
**Dependencies:** none — **blocks almost everything**

### I-04 · Shared data loader + fixed split in `src/data.py`
**Labels:** `type:data` `area:s2-eda` `priority:p0` `status:blocked` `owner:agent-ok`
**Context & Scope:** Implement `load()` and `split(seed=158)` → train/valid/test. Document how to download raw data into `data/raw/` (the data itself is not committed). This is the one split everyone uses.
**Acceptance Criteria:**
- [ ] `from src.data import load, split` works from repo root and from `notebooks/`
- [ ] Split is deterministic (same sizes and IDs across two runs)
- [ ] Split proportions and any leakage guard (e.g. by user/time) documented in the docstring
- [ ] Download instructions are in `README.md`
**Dependencies:** I-01, I-03

### I-05 · Write Section 1: predictive task framing
**Labels:** `type:writing` `area:s1-task` `priority:p0` `status:blocked` `owner:agent-ok`
**Context & Scope:** `notebooks/01_task.ipynb`, markdown only: the task, how it's evaluated, which baselines, how prediction validity is assessed (held-out test, sanity checks, significance or variance across seeds).
**Acceptance Criteria:**
- [ ] Covers all 3 spec bullets for Section 1 explicitly, under headings
- [ ] States why the task is relevant to course content
- [ ] Consistent with `docs/decision.md`
**Dependencies:** I-03

### I-06 · EDA: dataset context, stats tables, plots
**Labels:** `type:data` `area:s2-eda` `priority:p0` `status:blocked` `owner:agent-ok`
**Context & Scope:** `notebooks/02_eda.ipynb`. Where the data came from, its purpose and how it was collected; summary stats; distributions of target and key features; sparsity/long-tail plots where relevant.
**Acceptance Criteria:**
- [ ] Context paragraph with source citation
- [ ] ≥1 summary table (counts, missing values, target distribution)
- [ ] ≥3 labelled plots, each followed by a 1–2 sentence takeaway
- [ ] Each finding linked to a modeling choice ("→ motivates X")
**Dependencies:** I-04

### I-07 · Document preprocessing pipeline
**Labels:** `type:data` `area:s2-eda` `priority:p1` `status:blocked` `owner:agent-ok`
**Context & Scope:** Filtering, cleaning, feature construction and encoding, in `src/data.py` with an explanation in `notebooks/02_eda.ipynb`. Note what was already preprocessed by the dataset authors.
**Acceptance Criteria:**
- [ ] Every transformation listed, with its rationale
- [ ] Row counts before/after each filter shown
- [ ] No test-set statistics used in fitting transforms
**Dependencies:** I-04

### I-08 · Implement trivial baselines
**Labels:** `type:model` `area:s3-modeling` `priority:p0` `status:blocked` `owner:agent-ok`
**Context & Scope:** `src/models.py` + `notebooks/03_models.ipynb`. E.g. global mean / majority class / popularity. Common `fit(train)` / `predict(X)` interface.
**Acceptance Criteria:**
- [ ] ≥1 trivial baseline implemented and scored on validation via `src/metrics.py`
- [ ] Interface documented so I-09/I-10 reuse it
**Dependencies:** I-04

### I-09 · Implement course-model baseline
**Labels:** `type:model` `area:s3-modeling` `priority:p0` `status:blocked` `owner:agent-ok`
**Context & Scope:** A model taught in the course that fits the task (e.g. linear/logistic regression on features, latent factor model with biases, Jaccard/similarity-based recommender). Required by the spec even if the main model comes from elsewhere.
**Acceptance Criteria:**
- [ ] Model implemented with the shared interface; validation score reported
- [ ] Inputs, outputs and objective stated in markdown
- [ ] Beats or is compared honestly against I-08
**Dependencies:** I-08

### I-10 · Implement main model + features
**Labels:** `type:model` `area:s3-modeling` `priority:p1` `status:blocked` `owner:agent-ok`
**Context & Scope:** The improved model (richer features, a combined model, or one from another class). Explain the architectural choices.
**Acceptance Criteria:**
- [ ] Implemented in `src/models.py`, demonstrated in `notebooks/03_models.ipynb`
- [ ] Markdown compares ≥2 approaches on complexity, efficiency and implementation difficulty
- [ ] Training time recorded
**Dependencies:** I-09

### I-11 · Tune hyperparameters on validation set
**Labels:** `type:model` `area:s3-modeling` `priority:p1` `status:blocked` `owner:agent-ok`
**Context & Scope:** Grid or small search over key hyperparameters (regularization, latent dimension, etc.) using validation only.
**Acceptance Criteria:**
- [ ] Table or plot of validation metric vs. hyperparameter
- [ ] Chosen values recorded and used in I-12
- [ ] Test set not used
**Dependencies:** I-10

### I-12 · Evaluation harness + results table on test
**Labels:** `type:eval` `area:s4-eval` `priority:p0` `status:blocked` `owner:agent-ok`
**Context & Scope:** `src/metrics.py` + `notebooks/04_eval.ipynb`. Score every model (I-08 to I-11) on the held-out test set once.
**Acceptance Criteria:**
- [ ] One results table: every model × primary + secondary metric
- [ ] Results reproducible from a fresh kernel
- [ ] Variance or a confidence estimate reported (seeds, bootstrap, or similar)
**Dependencies:** I-08, I-09 (I-10/I-11 rows added when ready)

### I-13 · Result plots, error analysis, metric justification
**Labels:** `type:eval` `area:s4-eval` `priority:p1` `status:blocked` `owner:agent-ok`
**Context & Scope:** Explain why the chosen metrics fit better than alternatives; show where the model fails (by segment, by sparsity, etc.); explain any negative results.
**Acceptance Criteria:**
- [ ] Paragraph justifying metrics vs. ≥1 alternative
- [ ] ≥2 evaluation plots (e.g. per-segment error, calibration/ROC, error vs. activity level)
- [ ] Negative or surprising results explained
**Dependencies:** I-12

### I-14 · Related-work research notes with citations
**Labels:** `type:research` `area:s5-related` `priority:p0` `status:blocked` `owner:agent-ok`
**Context & Scope:** `docs/related_work.md`. How this dataset (or similar ones) has been used; how prior work approached the task; the numbers they reported. Real, verifiable sources only.
**Acceptance Criteria:**
- [ ] ≥3 sources with working links
- [ ] Each source: 2–3 sentence summary in our own words, plus its reported metric if any
- [ ] No invented citations (every link opened and checked)
**Dependencies:** I-03

### I-15 · Compare our results to reported results
**Labels:** `type:research` `area:s5-related` `priority:p1` `status:blocked` `owner:agent-ok`
**Context & Scope:** A short table and discussion: our numbers vs. the literature, and why they differ (data split, subset, metric definition).
**Acceptance Criteria:**
- [ ] Comparison table, with caveats on comparability
- [ ] Added to `workbook.ipynb` Section 5
**Dependencies:** I-12, I-14

### I-16 · Assemble and narrate `workbook.ipynb`
**Labels:** `type:writing` `area:notebook` `priority:p0` `status:blocked` `owner:agent-ok`
**Context & Scope:** Merge the draft notebooks into a single `workbook.ipynb` with 5 top-level headings matching the spec sections, in an obvious order. Inline any `src/` code graders need to see. Markdown before and after each code block.
**Acceptance Criteria:**
- [ ] Headings exactly: 1 Predictive Task · 2 EDA · 3 Modeling · 4 Evaluation · 5 Related Work
- [ ] Runs top-to-bottom on a fresh kernel with no errors
- [ ] No leftover debug cells, giant raw outputs or warnings spam
- [ ] Every number planned for the slides appears in it
- [ ] Notebook frozen by the internal milestone date (HANDOFF §0)
**Dependencies:** I-05 to I-15 (p2/p1 items may be dropped if late — note in HANDOFF)

### I-17 · Execute + export `workbook.html`
**Labels:** `type:submission` `area:notebook` `priority:p0` `status:blocked` `owner:agent-ok`
**Context & Scope:** `scripts/export.sh`: execute, then `jupyter nbconvert --to html workbook.ipynb`.
**Acceptance Criteria:**
- [ ] `workbook.html` starts with `<!DOCTYPE html>`
- [ ] Opens in a browser with all plots visible
- [ ] Committed to `main`
**Dependencies:** I-16

### I-18 · Local submission checker script
**Labels:** `type:setup` `area:infra` `priority:p1` `status:ready` `owner:agent-ok`
**Context & Scope:** `scripts/check_submission.py`, replicating the spec's autograder: both files exist; HTML prefix check; Drive file ID parsing, download >1 MB, `video/mp4` MIME via `python-magic` (YouTube links skip the download checks).
**Acceptance Criteria:**
- [ ] Passes on a known-good HTML file and MP4 Drive link
- [ ] Fails with a clear message on: renamed `.ipynb`, a link without a file ID, a non-MP4 file
- [ ] Usage documented in README
**Dependencies:** I-01

### I-19 · Build slide deck (human-written wording)
**Labels:** `type:presentation` `area:video` `priority:p0` `status:blocked` `owner:human`
**Context & Scope:** Slides for the 5 sections, planned to switch to code walkthroughs of `workbook.html`. Agents may make charts or check numbers against the notebook; humans write all slide text. The rubric gives 1/5 to presentations that look auto-generated.
**Acceptance Criteria:**
- [ ] One clearly titled block per section, in the same order as the notebook
- [ ] Every number on a slide matches `workbook.html`
- [ ] Timing plan adds up to 18–22 min
**Dependencies:** I-16

### I-20 · Record and edit ~20-min MP4 video
**Labels:** `type:presentation` `area:video` `priority:p0` `status:blocked` `owner:human`
**Context & Scope:** Record slides plus code walkthrough (Zoom or similar). Export H.264 MP4.
**Acceptance Criteria:**
- [ ] Length 18–22 min
- [ ] MP4, H.264/AAC, plays in a standard browser and in QuickTime
- [ ] Audio is clear; code is readable at 1080p
- [ ] Narration matches the notebook
**Dependencies:** I-17, I-19

### I-21 · Upload video, write `video_url.txt`, submit
**Labels:** `type:submission` `area:video` `priority:p0` `status:blocked` `owner:human`
**Context & Scope:** Upload to Google Drive with "anyone with the link" sharing (or YouTube). Write the one-line `video_url.txt`. Run the checker. Submit both files to Gradescope (with group members added).
**Acceptance Criteria:**
- [ ] `python scripts/check_submission.py` passes
- [ ] Link opens in an incognito window
- [ ] Gradescope autograder passes; all group members are on the submission
- [ ] Submitted ≥1 day before the deadline (A1)
**Dependencies:** I-17, I-18, I-20

### I-22 · Complete peer grading (each member)
**Labels:** `type:submission` `area:infra` `priority:p0` `status:blocked` `owner:human`
**Context & Scope:** Each student uploads an empty `responses.txt` to the peer-grading assignment, grades the assigned projects, then re-uploads the completed file. Worth 4 marks.
**Acceptance Criteria:**
- [ ] Every member's `responses.txt` passes the Gradescope format check
**Dependencies:** I-21 and instructor release (week 11)
