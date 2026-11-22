# ISSUES.md: 158R Assignment 2 backlog

Backlog spec. Live tracker: GitHub issues, titled `[I-NN] ...` (search the ID to find one). Each issue = one branch = one owner. Protocol and assumptions are in [`HANDOFF.md`](HANDOFF.md).
Section numbers refer to the spec's 5 graded sections (5 marks each).

## Label system

| Category | Labels | Use |
|---|---|---|
| `type:` | `setup` · `decision` · `data` · `model` · `eval` · `research` · `writing` · `presentation` · `submission` | What kind of work |
| `area:` | `s1-task` · `s2-eda` · `s3-modeling` · `s4-eval` · `s5-related` · `notebook` · `video` · `infra` | Graded section or artifact it feeds |
| Priority | `P0` (blocks submission) · `P1` (needed for a 4/5) · `P2` (stretch toward 5/5) | How important |
| `status:` | `ready` · `blocked` · `in-progress` · `review` · `done` | Claiming / filtering |
| Owner name | `Waleed` · `Aditya` | Who owns it (see Parts and roles). Shared issues carry both |
| `Order N` | `Order 1` to `Order 11` | Work sequence from the dependency chain. An issue is one step after its latest dependency. Same order = can run in parallel |
| `owner:` | `human` · `agent-ok` | `human` = agents must not do it (rubric penalizes auto-generated presentations; also accounts/uploads) |

Every issue below ends with an **Agent prompt**: paste it into your coding agent to do that issue. `owner:human` issues have a helper prompt for checks only.

## Parts (GitHub milestones) and roles

Deadline: **Tue 2026-12-01** (Tuesday of week 10; UCSD instruction began Thu Sep 24). Thanksgiving is **Thu to Fri, Nov 26 to 27**: treat those days as buffer, not planned work. Check the exact submission time on Gradescope.

| Part | Due | Issues |
|---|---|---|
| 1 Setup and decision | Sun 11-22 | I-01, I-02, I-03, I-18, I-23 |
| 2 Data and task | Tue 11-24 | I-04, I-05, I-06, I-07, I-14 |
| 3 Models and evaluation | Wed 11-25 | I-08, I-09, I-10, I-12 |
| 4 Analysis and notebook | Fri 11-27 | I-11, I-13, I-15, I-16, I-17 |
| 5 Presentation and submission | Mon 11-30 | I-19 (starts Wed 11-25), I-20, I-21 |
| 6 Peer grading | week 11 | I-22 |

### Day-by-day plan

| Day | Waleed | Aditya |
|---|---|---|
| Sun 11-22 | I-01, I-23 CI, I-02, I-18 · I-03 with Aditya | I-03 with Waleed |
| Mon 11-23 | I-04 split | I-05 task framing, I-14 related work |
| Tue 11-24 | I-06 EDA, I-07 preprocessing | I-08 baselines, I-09 course model |
| Wed 11-25 | I-16 notebook skeleton (Sections 1, 2, 5 in) · I-19 slide template + intro, S1, S2 slides | I-10 main model, I-12 test evaluation |
| Thu 11-26 | Thanksgiving: buffer | Thanksgiving: buffer |
| Fri 11-27 | I-16 assemble + I-17 export: **notebook frozen by evening** | I-13 metric/error analysis, I-15 comparison (morning) · I-11 only if on track · S3, S4, S5 slides |
| Sat 11-28 | Finish slides · numbers check vs `workbook.html` · **2 timed rehearsals together** | same |
| Sun 11-29 | I-20 record + convert + check | I-20 record |
| Mon 11-30 | I-21 upload, run checker, **submit** | confirm on Gradescope |
| Tue 12-01 | Deadline. Spare day only, no planned work | |

**Presentation gets about 3 days** (Wed draft, Fri to Sat finish and rehearse, Sun record). If anything slips, cut in this order: I-11 tuning (use defaults), extra plots in I-13, I-10 (present the course model as the main model). Never cut rehearsal or recording time.

### Talk time budget (target 20 min, hard max 22)

| Segment | Speaker | Minutes | Must show |
|---|---|---|---|
| Intro | Waleed | 1 | task in one sentence, dataset, headline result |
| S1 Predictive task | Waleed | 3 | task, metrics, baselines, how validity is checked |
| S2 Data and EDA | Waleed | 4 | dataset origin, preprocessing steps, 2 to 3 key plots, code walkthrough |
| S3 Modeling | Aditya | 5 | ML formulation (inputs, outputs, objective), tradeoffs between approaches, code walkthrough |
| S4 Evaluation | Aditya | 5 | why these metrics, results table vs baselines, uncertainty, code walkthrough |
| S5 Related work | Aditya | 2 | prior use of the dataset, prior approaches, how our numbers compare |

Every section needs all three spec parts (context, discussion, code), or graders cap it at 2/5.

| Owner | GitHub | Owns | Issues |
|---|---|---|---|
| Waleed | `waleedA13` | dataset decision, setup, CI, split, EDA, preprocessing, notebook assembly, submission | I-01, I-02, I-03, I-04, I-06, I-07, I-16, I-17, I-18, I-21, I-23 |
| Aditya | `AdityaJadhav17` | task framing, all models, evaluation, related work | I-05, I-08, I-09, I-10, I-11, I-12, I-13, I-14, I-15 |
| Both | Waleed + Aditya | slides for your own sections, video, peer grading (each person) | I-19, I-20, I-22 |

Aditya can start I-14 (related work) and I-05 (task framing) right after I-03 is decided, while Waleed builds the split (I-04).

## Index

| Order | ID | Title | Pri | Owner type | Depends on | Status |
|---|---|---|---|---|---|---|
| 1 | I-01 | Scaffold repo layout, deps, .gitignore | P0 | agent-ok | none | ready |
| 1 | I-02 | Add assignment spec to `docs/` | P1 | agent-ok | none | ready |
| 1 | I-03 | Decide dataset, predictive task, metric | P0 | human | none | ready |
| 2 | I-04 | Shared data loader + fixed split in `src/data.py` | P0 | agent-ok | I-01, I-03 | blocked |
| 2 | I-05 | Write Section 1: predictive task framing | P0 | agent-ok | I-03 | blocked |
| 3 | I-06 | EDA: dataset context, stats tables, plots | P0 | agent-ok | I-04 | blocked |
| 3 | I-07 | Document preprocessing pipeline | P0 | agent-ok | I-04 | blocked |
| 3 | I-08 | Implement trivial baselines | P0 | agent-ok | I-04 | blocked |
| 4 | I-09 | Implement course-model baseline | P0 | agent-ok | I-08 | blocked |
| 5 | I-10 | Implement main model + features | P1 | agent-ok | I-09 | blocked |
| 6 | I-11 | Tune hyperparameters on validation set | P1 | agent-ok | I-10 | blocked |
| 5 | I-12 | Evaluation harness + results table on test | P0 | agent-ok | I-08, I-09 | blocked |
| 6 | I-13 | Result plots, error analysis, metric justification | P0 | agent-ok | I-12 | blocked |
| 2 | I-14 | Related-work research notes with citations | P0 | agent-ok | I-03 | blocked |
| 6 | I-15 | Compare our results to reported results | P0 | agent-ok | I-12, I-14 | blocked |
| 7 | I-16 | Assemble and narrate `workbook.ipynb` | P0 | agent-ok | I-05 to I-15 | blocked |
| 8 | I-17 | Execute + export `workbook.html` | P0 | agent-ok | I-16 | blocked |
| 2 | I-18 | Local submission checker script | P1 | agent-ok | I-01 | ready |
| 3 | I-19 | Build slide deck (human-written wording) | P0 | human | I-05 (start), I-17 (final numbers) | blocked |
| 9 | I-20 | Record and edit ~20-min MP4 video | P0 | human | I-17, I-19 | blocked |
| 10 | I-21 | Upload video, write `video_url.txt`, submit | P0 | human | I-17, I-18, I-20 | blocked |
| 11 | I-22 | Complete peer grading (each member) | P0 | human | I-21 + instructor release | blocked |
| 2 | I-23 | Set up CI pipeline (format, lint, audit, tests) | P0 | agent-ok | I-01 | review |

---

### I-01 · Scaffold repo layout, deps, .gitignore
**Labels:** `type:setup` `area:infra` `P0` `status:ready` `owner:agent-ok` `Order 1` `Waleed`
**Context & Scope:** Repo has only `README.md`. Create the layout in HANDOFF.md §2: `src/`, `notebooks/`, `scripts/`, `docs/`, `slides/`, `data/` (gitignored). Add `requirements.txt` (pandas, numpy, scikit-learn, matplotlib, jupyter, nbconvert; pin versions).  `AGENTS.md` already exists (shared agent instructions); leave it. Expand `README.md` with a one-paragraph description + setup command.
**Acceptance Criteria:**
- [x] `pip install -r requirements.txt` succeeds in a fresh venv (Python 3.12)
- [x] `.gitignore` excludes `data/`, `*.mp4`, `.ipynb_checkpoints/`, `__pycache__/`, `.venv/`
- [x] Empty `src/__init__.py`, `src/data.py`, `src/metrics.py`, `src/models.py` exist
- [x] `python -c "import src.data, src.metrics, src.models"` works from the repo root
**Dependencies:** none

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-01) in ISSUES.md. Follow their rules exactly.
Branch: i01-scaffold from up-to-date main. Commit messages: "[I-01] ...".

Task: create the repo skeleton described in HANDOFF.md section 2.
Steps:
1. Create folders: src/, notebooks/, scripts/ (exists), docs/, slides/, data/raw/, data/processed/. Add a .gitkeep to empty folders except data/.
2. Create src/__init__.py (empty) and src/data.py, src/metrics.py, src/models.py, each with only a one-line module docstring saying what will live there.
3. Create .gitignore with: data/, *.mp4, .ipynb_checkpoints/, __pycache__/, .venv/, .DS_Store.
4. Create requirements.txt: pandas, numpy, scikit-learn, matplotlib, jupyter, nbconvert, requests, python-magic. Install them in a fresh venv and pin the exact installed versions (pip freeze, keep only these packages).
5. Expand README.md: one paragraph on the project, then setup: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt.
6. AGENTS.md already exists: do not rewrite it.
Verify (paste output in PR):
- rm -rf /tmp/v && python3 -m venv /tmp/v && /tmp/v/bin/pip install -r requirements.txt  (must succeed)
- git status shows data/ is ignored after creating data/raw/test.txt (delete the test file after).
- python -c "import src.data, src.metrics, src.models" succeeds from the repo root.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-01] Scaffold repo layout, deps, .gitignore" for Aditya to review. Do not mark anything done that you did not verify.
```

### I-02 · Add assignment spec to `docs/`
**Labels:** `type:setup` `area:infra` `P1` `status:ready` `owner:agent-ok` `Order 1` `Waleed`
**Context & Scope:** The spec lives outside the repo (`../Assignment 2/158 _ 258 2026 Assignment 2.pdf`). Copy to `docs/spec.pdf` and add `docs/requirements.md` with the 5 sections and their bullets so agents can read it as text.
**Acceptance Criteria:**
- [x] `docs/spec.pdf` committed
- [x] `docs/requirements.md` lists all 5 sections, the rubric (0 to 5), the submission files and the autograder checks
**Dependencies:** none

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-02) in ISSUES.md. Follow their rules exactly.
Branch: i02-spec from up-to-date main. Commit messages: "[I-02] ...".

Task: make the assignment spec readable inside the repo.
Steps:
1. A human copies the spec PDF from "../Assignment 2/158 _ 258 2026 Assignment 2.pdf" to docs/spec.pdf (it lives outside this repo).
2. Extract its text (pdftotext docs/spec.pdf - or a Python PDF library) and write docs/requirements.md with:
   - the 5 graded sections and every bullet under each, paraphrased in our words
   - the 0 to 5 rubric
   - the submission files (workbook.html, video_url.txt) and every autograder check
   - the peer grading steps
3. Keep it under 120 lines. Do not copy long passages verbatim.
Verify: every one of the 5 sections and every autograder check in the PDF appears in docs/requirements.md (list them side by side in the PR description).

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-02] Add assignment spec to `docs/`" for Aditya to review. Do not mark anything done that you did not verify.
```

### I-03 · Decide dataset, predictive task, metric
**Labels:** `type:decision` `area:s1-task` `P0` `status:ready` `owner:human` `Order 1` `Waleed`
**Context & Scope:** Nothing is chosen. Pick a dataset (e.g. from cseweb.ucsd.edu/~jmcauley/datasets.html or the Assignment 1 data) and a task relevant to course content (rating prediction, read/purchase prediction, classification from text, etc.). Record it in `docs/decision.md`. Agents may draft 2 or 3 candidate options with pros/cons; humans choose.
**Acceptance Criteria:**
- [ ] `docs/decision.md` states: dataset + source URL + size, task (inputs → output), primary metric + secondary metric, ≥2 planned baselines (≥1 from course), at least one course model
- [ ] Dataset size is workable on a laptop (or subsampling plan documented)
- [ ] Every group member has agreed (names listed)
- [ ] HANDOFF.md §0 A4 marked confirmed
**Dependencies:** none. **Blocks almost everything.**

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-03) in ISSUES.md. Follow their rules exactly.
Branch: i03-decision from up-to-date main. Commit messages: "[I-03] ...".

This is human-only work (owner:human). The agent may only help with the checks below. It must not write slide text, narration, or reviews.
Waleed and Aditya choose together. The agent prepares options only.
Helper prompt for the agent:
"Using https://cseweb.ucsd.edu/~jmcauley/datasets.html (and the Assignment 1 data if we have it), propose 3 dataset + predictive task options suited to CSE 158 models (latent factor models, similarity-based recommenders, linear/logistic regression on features, bag-of-words/TF-IDF). For each give: dataset name and link, approximate size and whether it runs on a laptop (or a subsample plan), key fields, the exact task (given X predict Y per Z), a primary and secondary metric with a one-line reason, a trivial baseline, a course-model baseline, a plausible main model, and at least one real paper that used the dataset (with a working link you opened). Put it in a comparison table in docs/options.md. Do not choose. Do not invent sizes or papers; write 'unknown' if you could not check."
Then the humans:
1. Read docs/options.md, pick one, and write docs/decision.md using this template:
   Dataset: name, source URL, size, subsample plan
   Task: given X, predict Y per Z; split scheme (random / by time / by user) and proportions
   Metrics: primary + why; secondary
   Baselines: trivial; course model
   Main model:
   Agreed by: Waleed, Aditya (date)
2. Close this issue and move I-04, I-05, I-14 to status:ready.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-03] Decide dataset, predictive task, metric" for Aditya to review. Do not mark anything done that you did not verify.
```

### I-04 · Shared data loader + fixed split in `src/data.py`
**Labels:** `type:data` `area:s2-eda` `P0` `status:blocked` `owner:agent-ok` `Order 2` `Waleed`
**Context & Scope:** Implement `load()` and `split(seed=158)` → train/valid/test. Document how to download raw data into `data/raw/` (the data itself is not committed). This is the one split everyone uses.
**Acceptance Criteria:**
- [ ] `from src.data import load, split` works from repo root and from `notebooks/`
- [ ] Split is deterministic (same sizes and IDs across two runs)
- [ ] Split proportions and any leakage guard (e.g. by user/time) documented in the docstring
- [ ] Download instructions are in `README.md`
**Dependencies:** I-01, I-03

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-04) in ISSUES.md. Follow their rules exactly.
Branch: i04-split from up-to-date main. Commit messages: "[I-04] ...".

Tests first: before writing any implementation, add tests for this issue's acceptance criteria under tests/unit/test_data.py (deterministic split, proportions, no ID overlap between splits, leakage rule) and tests/integration/test_pipeline.py (load -> split on tests/fixtures/), run them and confirm they FAIL, and commit them alone as "[I-04] add failing tests". Then implement until they pass.
Task: implement the one shared loader and split in src/data.py, following docs/decision.md exactly.
Steps:
1. Add a download section to README.md: where to get the raw files and the exact path under data/raw/.
2. In src/data.py implement:
   - constants at the top: RAW_DIR = Path(os.environ.get("DATA_DIR", "data/raw")), PROCESSED_DIR, SEED = 158, split proportions from docs/decision.md
   - tests/fixtures/: a small sample (about 200 rows) in exactly the raw file format, so CI runs without the real data (DATA_DIR=tests/fixtures). Use synthetic rows or a tiny public sample; nothing private
   - load() -> pandas DataFrame of the raw data (subsample here if decision.md says so, with the fixed seed)
   - split(df, seed=SEED) -> (train, valid, test) using the scheme in docs/decision.md, with a guard against leakage (e.g. by time or by user if the task needs it)
   - a docstring on split() stating proportions and the leakage rule
3. Add `if __name__ == "__main__":` that prints row counts per split and a hash of the sorted test-set IDs.
Verify (paste in PR):
- python -m src.data run twice prints identical counts and identical hash.
- from notebooks/: import sys; sys.path.append(".."); from src.data import load, split works.
Do not: look at test-set statistics, or change decision.md.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-04] Shared data loader + fixed split in `src/data.py`" for Aditya to review. Do not mark anything done that you did not verify.
```

### I-05 · Write Section 1: predictive task framing
**Labels:** `type:writing` `area:s1-task` `P0` `status:blocked` `owner:agent-ok` `Order 2` `Aditya`
**Context & Scope:** `notebooks/01_task.ipynb`, markdown only: the task, how it's evaluated, which baselines, how prediction validity is assessed (held-out test, sanity checks, significance or variance across seeds).
**Acceptance Criteria:**
- [ ] Covers all 3 spec bullets for Section 1 explicitly, under headings
- [ ] States why the task is relevant to course content
- [ ] Consistent with `docs/decision.md`
**Dependencies:** I-03

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-05) in ISSUES.md. Follow their rules exactly.
Branch: i05-task from up-to-date main. Commit messages: "[I-05] ...".

Task: write graded Section 1 (predictive task) as markdown in notebooks/01_task.ipynb.
Steps:
1. Read docs/decision.md and docs/requirements.md (Section 1 bullets).
2. Write four headed markdown cells:
   - The task: inputs, output, unit of prediction, and why it fits course content
   - Evaluation: primary and secondary metric and what a good score means
   - Baselines: the trivial and course-model baselines and why they are fair comparisons
   - Validity: held-out test set used once, the leakage guard from src/data.py, variance across seeds or bootstrap, sanity checks
3. Keep it tight: about 250 to 400 words total.
Verify: each Section 1 bullet in docs/requirements.md maps to a heading (list the mapping in the PR). Nothing contradicts docs/decision.md.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-05] Write Section 1: predictive task framing" for Waleed to review. Do not mark anything done that you did not verify.
```

### I-06 · EDA: dataset context, stats tables, plots
**Labels:** `type:data` `area:s2-eda` `P0` `status:blocked` `owner:agent-ok` `Order 3` `Waleed`
**Context & Scope:** `notebooks/02_eda.ipynb`. Where the data came from, its purpose and how it was collected; summary stats; distributions of target and key features; sparsity/long-tail plots where relevant.
**Acceptance Criteria:**
- [ ] Context paragraph with source citation
- [ ] ≥1 summary table (counts, missing values, target distribution)
- [ ] ≥3 labelled plots, each followed by a 1 to 2 sentence takeaway
- [ ] Each finding linked to a modeling choice ("→ motivates X")
**Dependencies:** I-04

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-06) in ISSUES.md. Follow their rules exactly.
Branch: i06-eda from up-to-date main. Commit messages: "[I-06] ...".

Task: graded Section 2 exploratory analysis in notebooks/02_eda.ipynb.
Steps:
1. Load data only via from src.data import load, split. Do EDA on the train split only (note this in markdown).
2. Context cell: where the dataset comes from, what it was built for, how it was collected, with a citation link (from docs/decision.md or the dataset page).
3. Summary table: rows, users/items (if relevant), missing values per column, target distribution.
4. At least 3 plots with titles, axis labels and units: target distribution; activity long tail (per user/item counts, log scale) or feature distributions; one relationship between a feature and the target.
5. After every plot: a 1 to 2 sentence takeaway ending with "-> motivates ..." naming a modeling choice.
Verify: restart kernel and run all with no errors; every plot has a takeaway; no test-set data used.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-06] EDA: dataset context, stats tables, plots" for Aditya to review. Do not mark anything done that you did not verify.
```

### I-07 · Document preprocessing pipeline
**Labels:** `type:data` `area:s2-eda` `P0` `status:blocked` `owner:agent-ok` `Order 3` `Waleed`
**Context & Scope:** Filtering, cleaning, feature construction and encoding, in `src/data.py` with an explanation in `notebooks/02_eda.ipynb`. Note what was already preprocessed by the dataset authors.
**Acceptance Criteria:**
- [ ] Every transformation listed, with its rationale
- [ ] Row counts before/after each filter shown
- [ ] No test-set statistics used in fitting transforms
**Dependencies:** I-04

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-07) in ISSUES.md. Follow their rules exactly.
Branch: i07-preprocess from up-to-date main. Commit messages: "[I-07] ...".

Tests first: before writing any implementation, add tests for this issue's acceptance criteria under tests/unit/test_preprocess.py (statistics fitted on train only, row counts per step), run them and confirm they FAIL, and commit them alone as "[I-07] add failing tests". Then implement until they pass.
Task: implement and document preprocessing.
Steps:
1. In src/data.py add preprocess(train, valid, test) that applies every cleaning/filtering/feature step. Fit any statistics (means, vocabularies, encoders) on train only and apply to valid/test.
2. In notebooks/02_eda.ipynb add a "Preprocessing" section: a table of each step, its rationale, and row counts before/after.
3. Note anything the dataset authors already preprocessed.
Verify: a cell asserts row counts match the table; grep src/data.py shows no fit on valid/test; restart and run all passes.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-07] Document preprocessing pipeline" for Aditya to review. Do not mark anything done that you did not verify.
```

### I-08 · Implement trivial baselines
**Labels:** `type:model` `area:s3-modeling` `P0` `status:blocked` `owner:agent-ok` `Order 3` `Aditya`
**Context & Scope:** `src/models.py` + `notebooks/03_models.ipynb`. E.g. global mean / majority class / popularity. Common `fit(train)` / `predict(X)` interface.
**Acceptance Criteria:**
- [ ] ≥1 trivial baseline implemented and scored on validation via `src/metrics.py`
- [ ] Interface documented so I-09/I-10 reuse it
**Dependencies:** I-04

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-08) in ISSUES.md. Follow their rules exactly.
Branch: i08-baselines from up-to-date main. Commit messages: "[I-08] ...".

Tests first: before writing any implementation, add tests for this issue's acceptance criteria under tests/unit/test_metrics.py (hand-computed values) and tests/unit/test_models.py (fit/predict shapes, baseline output), run them and confirm they FAIL, and commit them alone as "[I-08] add failing tests". Then implement until they pass.
Task: trivial baselines plus the shared metric code.
Steps:
1. src/metrics.py: implement the primary and secondary metrics from docs/decision.md as plain functions (y_true, y_pred) -> float, with docstrings. Add a tiny self-check under if __name__ == "__main__" using hand-computed examples.
2. src/models.py: a common interface (class with fit(train) and predict(df)) and at least one trivial baseline (global mean, majority class, or popularity, whichever fits the task).
3. notebooks/03_models.ipynb: load via src.data, fit on train, score on valid, show a one-row results table.
Verify (paste in PR): python -m src.metrics passes; notebook restart-and-run-all passes; validation score printed.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-08] Implement trivial baselines" for Waleed to review. Do not mark anything done that you did not verify.
```

### I-09 · Implement course-model baseline
**Labels:** `type:model` `area:s3-modeling` `P0` `status:blocked` `owner:agent-ok` `Order 4` `Aditya`
**Context & Scope:** A model taught in the course that fits the task (e.g. linear/logistic regression on features, latent factor model with biases, Jaccard/similarity-based recommender). Required by the spec even if the main model comes from elsewhere.
**Acceptance Criteria:**
- [ ] Model implemented with the shared interface; validation score reported
- [ ] Inputs, outputs and objective stated in markdown
- [ ] Beats or is compared honestly against I-08
**Dependencies:** I-08

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-09) in ISSUES.md. Follow their rules exactly.
Branch: i09-course-model from up-to-date main. Commit messages: "[I-09] ...".

Tests first: before writing any implementation, add tests for this issue's acceptance criteria under tests/unit/test_models.py (fit/predict shapes, beats a constant predictor on a tiny synthetic example), run them and confirm they FAIL, and commit them alone as "[I-09] add failing tests". Then implement until they pass.
Task: implement the course-model baseline named in docs/decision.md.
Steps:
1. Add it to src/models.py with the same fit/predict interface (e.g. latent factor model with user/item biases, Jaccard or cosine similarity recommender, or logistic/linear regression on engineered features).
2. In notebooks/03_models.ipynb: markdown stating inputs, outputs, and the objective being optimized (write the equation); then fit on train, score on valid with src/metrics.py, append to the results table next to I-08.
3. If it does not beat the trivial baseline, say so and give a likely reason. Do not tune on test.
Verify: restart-and-run-all passes; results table has both rows; objective is written out.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-09] Implement course-model baseline" for Waleed to review. Do not mark anything done that you did not verify.
```

### I-10 · Implement main model + features
**Labels:** `type:model` `area:s3-modeling` `P1` `status:blocked` `owner:agent-ok` `Order 5` `Aditya`
**Context & Scope:** The improved model (richer features, a combined model, or one from another class). Explain the architectural choices.
**Acceptance Criteria:**
- [ ] Implemented in `src/models.py`, demonstrated in `notebooks/03_models.ipynb`
- [ ] Markdown compares ≥2 approaches on complexity, efficiency and implementation difficulty
- [ ] Training time recorded
**Dependencies:** I-09

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-10) in ISSUES.md. Follow their rules exactly.
Branch: i10-main-model from up-to-date main. Commit messages: "[I-10] ...".

Tests first: before writing any implementation, add tests for this issue's acceptance criteria under tests/unit/test_models.py (fit/predict shapes, deterministic with a fixed seed), run them and confirm they FAIL, and commit them alone as "[I-10] add failing tests". Then implement until they pass.
Task: implement the main model from docs/decision.md.
Steps:
1. Add it to src/models.py with the shared interface. Keep the code readable; comment each architectural choice.
2. In notebooks/03_models.ipynb: a markdown comparison of at least 2 approaches (including this one) on complexity, efficiency (record training time with time.perf_counter), and implementation difficulty.
3. Score on valid and add to the results table.
Verify: restart-and-run-all passes; training time shown; comparison table present.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-10] Implement main model + features" for Waleed to review. Do not mark anything done that you did not verify.
```

### I-11 · Tune hyperparameters on validation set
**Labels:** `type:model` `area:s3-modeling` `P1` `status:blocked` `owner:agent-ok` `Order 6` `Aditya`
**Context & Scope:** Grid or small search over key hyperparameters (regularization, latent dimension, etc.) using validation only.
**Acceptance Criteria:**
- [ ] Table or plot of validation metric vs. hyperparameter
- [ ] Chosen values recorded and used in I-12
- [ ] Test set not used
**Dependencies:** I-10

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-11) in ISSUES.md. Follow their rules exactly.
Branch: i11-tuning from up-to-date main. Commit messages: "[I-11] ...".

Task: tune the key hyperparameters of the main model (and course model if cheap) on the validation set only.
Steps:
1. Small grid (about 5 to 20 settings): e.g. regularization strength, latent dimension, learning rate, feature choices.
2. Plot validation metric vs. each hyperparameter, mark the chosen value.
3. Record the chosen values as constants at the top of the notebook section and in HANDOFF.md section 5.
Verify: no call touches the test split (grep for test in the section); restart-and-run-all passes.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-11] Tune hyperparameters on validation set" for Waleed to review. Do not mark anything done that you did not verify.
```

### I-12 · Evaluation harness + results table on test
**Labels:** `type:eval` `area:s4-eval` `P0` `status:blocked` `owner:agent-ok` `Order 5` `Aditya`
**Context & Scope:** `src/metrics.py` + `notebooks/04_eval.ipynb`. Score every model (I-08 to I-11) on the held-out test set once.
**Acceptance Criteria:**
- [ ] One results table: every model × primary + secondary metric
- [ ] Results reproducible from a fresh kernel
- [ ] Variance or a confidence estimate reported (seeds, bootstrap, or similar)
**Dependencies:** I-08, I-09 (I-10/I-11 rows added when ready)

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-12) in ISSUES.md. Follow their rules exactly.
Branch: i12-eval from up-to-date main. Commit messages: "[I-12] ...".

Tests first: before writing any implementation, add tests for this issue's acceptance criteria under tests/integration/test_pipeline.py (every model trains and is scored on the fixture data via src/metrics.py), run them and confirm they FAIL, and commit them alone as "[I-12] add failing tests". Then implement until they pass.
Task: final evaluation protocol on the test set, run once.
Steps:
1. notebooks/04_eval.ipynb: load splits via src.data, retrain each model (trivial, course, main with tuned values) on train (or train+valid, state which), predict test.
2. One results table: every model x primary and secondary metric.
3. Uncertainty: either 5 seeds (mean +/- std) or a bootstrap 95% interval on test.
4. One paragraph: does the main model beat both baselines, by how much, and is the gap larger than the uncertainty.
Verify: restart-and-run-all reproduces the same table twice; every number comes from src/metrics.py.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-12] Evaluation harness + results table on test" for Waleed to review. Do not mark anything done that you did not verify.
```

### I-13 · Result plots, error analysis, metric justification
**Labels:** `type:eval` `area:s4-eval` `P0` `status:blocked` `owner:agent-ok` `Order 6` `Aditya`
**Context & Scope:** Explain why the chosen metrics fit better than alternatives; show where the model fails (by segment, by sparsity, etc.); explain any negative results.
**Acceptance Criteria:**
- [ ] Paragraph justifying metrics vs. ≥1 alternative
- [ ] ≥2 evaluation plots (e.g. per-segment error, calibration/ROC, error vs. activity level)
- [ ] Negative or surprising results explained
**Dependencies:** I-12

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-13) in ISSUES.md. Follow their rules exactly.
Branch: i13-analysis from up-to-date main. Commit messages: "[I-13] ...".

Task: metric justification, plots, and error analysis.
Steps:
1. Markdown: why the primary metric fits this task better than at least one alternative (e.g. MSE vs MAE, accuracy vs BER/AUC under imbalance).
2. At least 2 plots: e.g. error by user/item activity level, error by segment or feature bucket, calibration or ROC curve.
3. Explain any negative or surprising results honestly.
Verify: restart-and-run-all passes; each plot has a 1 to 2 sentence takeaway.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-13] Result plots, error analysis, metric justification" for Waleed to review. Do not mark anything done that you did not verify.
```

### I-14 · Related-work research notes with citations
**Labels:** `type:research` `area:s5-related` `P0` `status:blocked` `owner:agent-ok` `Order 2` `Aditya`
**Context & Scope:** `docs/related_work.md`. How this dataset (or similar ones) has been used; how prior work approached the task; the numbers they reported. Real, verifiable sources only.
**Acceptance Criteria:**
- [ ] ≥3 sources with working links
- [ ] Each source: 2 to 3 sentence summary in our own words, plus its reported metric if any
- [ ] No invented citations (every link opened and checked)
**Dependencies:** I-03

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-14) in ISSUES.md. Follow their rules exactly.
Branch: i14-related from up-to-date main. Commit messages: "[I-14] ...".

Task: related-work notes in docs/related_work.md.
Steps:
1. Find at least 3 real sources: the dataset's own paper, and papers or reports that tackle the same or a similar task on this or similar data.
2. For each: full citation, working link (open it and confirm), a 2 to 3 sentence summary in our own words, the method used, and any reported metric with its exact definition and split.
3. A final short section: how prior work approached this task, in 3 to 5 bullets.
Do not: invent citations, quote more than a short phrase, or copy abstracts. If a number cannot be confirmed from the source, leave it out.
Verify: every link opened successfully (list them in the PR with the page title you saw).

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-14] Related-work research notes with citations" for Waleed to review. Do not mark anything done that you did not verify.
```

### I-15 · Compare our results to reported results
**Labels:** `type:research` `area:s5-related` `P0` `status:blocked` `owner:agent-ok` `Order 6` `Aditya`
**Context & Scope:** A short table and discussion: our numbers vs. the literature, and why they differ (data split, subset, metric definition).
**Acceptance Criteria:**
- [ ] Comparison table, with caveats on comparability
- [ ] Added to `workbook.ipynb` Section 5
**Dependencies:** I-12, I-14

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-15) in ISSUES.md. Follow their rules exactly.
Branch: i15-compare from up-to-date main. Commit messages: "[I-15] ...".

Task: compare our results to reported results.
Steps:
1. From docs/related_work.md and the I-12 table, build a comparison table: source, their metric value, ours, and why they may not be comparable (split, subset, metric definition).
2. Write 1 short paragraph on where we match or differ and why.
3. Add both to the Section 5 cells of notebooks/04_eval.ipynb (they move into workbook.ipynb in I-16).
Verify: every number in the table traces to a cited source or to the I-12 output.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-15] Compare our results to reported results" for Waleed to review. Do not mark anything done that you did not verify.
```

### I-16 · Assemble and narrate `workbook.ipynb`
**Labels:** `type:writing` `area:notebook` `P0` `status:blocked` `owner:agent-ok` `Order 7` `Waleed`
**Context & Scope:** Merge the draft notebooks into a single `workbook.ipynb` with 5 top-level headings matching the spec sections, in an obvious order. Inline any `src/` code graders need to see. Markdown before and after each code block.
**Acceptance Criteria:**
- [ ] Headings exactly: 1 Predictive Task · 2 EDA · 3 Modeling · 4 Evaluation · 5 Related Work
- [ ] Runs top-to-bottom on a fresh kernel with no errors
- [ ] No leftover debug cells, giant raw outputs or warnings spam
- [ ] Every number planned for the slides appears in it
- [ ] Notebook frozen by the internal milestone date (HANDOFF §0)
**Dependencies:** I-05 to I-15 (p2/p1 items may be dropped if late; note it in HANDOFF)

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-16) in ISSUES.md. Follow their rules exactly.
Branch: i16-assemble from up-to-date main. Commit messages: "[I-16] ...".

Task: assemble the final workbook.ipynb that graders read.
Steps:
1. Create workbook.ipynb with top-level headings in this exact order: 1 Predictive Task, 2 Exploratory Analysis and Preprocessing, 3 Modeling, 4 Evaluation, 5 Related Work.
2. Copy the cells from notebooks/01 to 04 into the matching sections. Inline the src/ functions graders need to see (paste the code or use %load) so the HTML shows the real implementation.
3. Add a short intro cell (what we predict, the dataset, the headline result) and a markdown cell before and after every code cell.
4. Remove debug cells, long raw outputs, and warning spam (fix warnings, do not just hide them).
5. Commit workbook.ipynb with outputs (the one exception to clearing outputs).
Verify: jupyter nbconvert --to notebook --execute --inplace workbook.ipynb finishes with no errors; pytest tests/e2e passes (it already exists and enforces the 5 headings, no error outputs, embedded plots); list every number planned for the slides with its section.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-16] Assemble and narrate `workbook.ipynb`" for Aditya to review. Do not mark anything done that you did not verify.
```

### I-17 · Execute + export `workbook.html`
**Labels:** `type:submission` `area:notebook` `P0` `status:blocked` `owner:agent-ok` `Order 8` `Waleed`
**Context & Scope:** `scripts/export.sh`: execute, then `jupyter nbconvert --to html workbook.ipynb`.
**Acceptance Criteria:**
- [ ] `workbook.html` starts with `<!DOCTYPE html>`
- [ ] Opens in a browser with all plots visible
- [ ] Committed to `main`
**Dependencies:** I-16

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-17) in ISSUES.md. Follow their rules exactly.
Branch: i17-export from up-to-date main. Commit messages: "[I-17] ...".

Task: export the submission HTML.
Steps:
1. Create scripts/export.sh: execute workbook.ipynb in place, then jupyter nbconvert --to html workbook.ipynb (output workbook.html in the repo root). Exit non-zero on any error.
2. Run it and commit workbook.html.
Verify (paste in PR): head -c 15 workbook.html prints <!DOCTYPE html>; open it in a browser and confirm all plots render; file size is reasonable (under about 10 MB).

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-17] Execute + export `workbook.html`" for Aditya to review. Do not mark anything done that you did not verify.
```

### I-18 · Local submission checker script
**Labels:** `type:setup` `area:infra` `P1` `status:ready` `owner:agent-ok` `Order 2` `Waleed`
**Context & Scope:** `scripts/check_submission.py`, replicating the spec's autograder: both files exist; HTML prefix check; Drive file ID parsing, download >1 MB, `video/mp4` MIME via `python-magic` (YouTube links skip the download checks).
**Acceptance Criteria:**
- [ ] Passes on a known-good HTML file and MP4 Drive link
- [ ] Fails with a clear message on: renamed `.ipynb`, a link without a file ID, a non-MP4 file
- [ ] Usage documented in README
**Dependencies:** I-01

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-18) in ISSUES.md. Follow their rules exactly.
Branch: i18-checker from up-to-date main. Commit messages: "[I-18] ...".

Tests first: before writing any implementation, add tests for this issue's acceptance criteria under tests/unit/test_check_submission.py (HTML prefix check, Drive ID parsing, <1 MB and non-MP4 rejection; fake the network, never call Google), run them and confirm they FAIL, and commit them alone as "[I-18] add failing tests". Then implement until they pass.
Task: a local copy of the course autograder checks in scripts/check_submission.py.
Steps:
1. Read the "How your submission is verified" part of docs/requirements.md (or docs/spec.pdf).
2. Implement: both files exist (workbook.html, video_url.txt); workbook.html starts with <!DOCTYPE html>; video_url.txt has one URL; YouTube links skip the download checks with a warning to make it public; Google Drive links: parse FILE_ID from "id=" or "/d/", download the first 1 MB via https://drive.google.com/uc?export=download&id=FILE_ID, handle the virus-scan warning page (uuid confirm URL), fail if under 1 MB, check MIME is video/mp4 with python-magic.
3. Clear pass/fail messages; exit code 0 only if everything passes. Usage in README.md.
Verify: test with (a) a renamed .ipynb as workbook.html -> fails, (b) a Drive URL without an ID -> fails, (c) a real nbconvert HTML -> passes the HTML check. Paste outputs in PR.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-18] Local submission checker script" for Aditya to review. Do not mark anything done that you did not verify.
```

### I-19 · Build slide deck (human-written wording)
**Labels:** `type:presentation` `area:video` `P0` `status:blocked` `owner:human` `Order 3` `Waleed` `Aditya`
**Context & Scope:** Slides for the 5 sections, planned to switch to code walkthroughs of `workbook.html`. Agents may make charts or check numbers against the notebook; humans write all slide text. The rubric gives 1/5 to presentations that look auto-generated.
**Acceptance Criteria:**
- [ ] Slide template made Wed 11-25; intro, S1, S2 drafted Wed; S3, S4, S5 drafted Fri 11-27
- [ ] One clearly titled block per section, in the same order as the notebook, each with context, discussion and a code walkthrough
- [ ] Every number on a slide matches `workbook.html` (checked after I-17)
- [ ] Follows the talk time budget in "Parts and roles" (target 20 min, max 22)
- [ ] Two full timed rehearsals done together on Sat 11-28
**Dependencies:** I-05 to start drafting; I-17 for the final numbers check

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-19) in ISSUES.md. Follow their rules exactly.
Branch: i19-slides from up-to-date main. Commit messages: "[I-19] ...".

This is human-only work (owner:human). The agent may only help with the checks below. It must not write slide text, narration, or reviews.
Each person writes the slides for their own sections in their own words: Waleed for the intro, S1 and S2; Aditya for S3, S4 and S5 (see the talk time budget in ISSUES.md). Start Wed 11-25 with the sections that are already done; do not wait for the frozen notebook.
Helper prompt for the agent (checks only):
"From workbook.html, list every number, table and plot title by section with the cell it comes from, as a checklist in slides/numbers.md. Then compare against slides/ (exported text) and list any number on a slide that does not match the notebook. Do not write or rewrite any slide text."
Plan the timing so the total is 18 to 22 minutes, in the same order as the notebook sections.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-19] Build slide deck (human-written wording)" for the other person to review. Do not mark anything done that you did not verify.
```

### I-20 · Record and edit ~20-min MP4 video
**Labels:** `type:presentation` `area:video` `P0` `status:blocked` `owner:human` `Order 9` `Waleed` `Aditya`
**Context & Scope:** Record slides plus code walkthrough (Zoom or similar). Export H.264 MP4.
**Acceptance Criteria:**
- [ ] Length 18 to 22 min
- [ ] MP4, H.264/AAC, plays in a standard browser and in QuickTime
- [ ] Audio is clear; code is readable at 1080p
- [ ] Narration matches the notebook
- [ ] Recorded Sun 11-29, leaving Mon 11-30 for upload and submit
**Dependencies:** I-17, I-19

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-20) in ISSUES.md. Follow their rules exactly.
Branch: i20-video from up-to-date main. Commit messages: "[I-20] ...".

This is human-only work (owner:human). The agent may only help with the checks below. It must not write slide text, narration, or reviews.
Record slides plus a live code walkthrough of workbook.html (Zoom or similar), both of you narrating your own sections.
Helper prompt for the agent (file checks only):
"Run ffprobe on the recorded file and report duration, container, video codec, audio codec and resolution. If it is not H.264/AAC MP4, give me the single ffmpeg command to convert it (libx264, -preset veryfast, aac) and nothing else."
Done when: 18 to 22 minutes, H.264/AAC MP4, plays in a browser and in QuickTime, code readable at 1080p, audio clear.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-20] Record and edit ~20-min MP4 video" for the other person to review. Do not mark anything done that you did not verify.
```

### I-21 · Upload video, write `video_url.txt`, submit
**Labels:** `type:submission` `area:video` `P0` `status:blocked` `owner:human` `Order 10` `Waleed`
**Context & Scope:** Upload to Google Drive with "anyone with the link" sharing (or YouTube). Write the one-line `video_url.txt`. Run the checker. Submit both files to Gradescope (with group members added).
**Acceptance Criteria:**
- [ ] `python scripts/check_submission.py` passes
- [ ] Link opens in an incognito window
- [ ] Gradescope autograder passes; all group members are on the submission
- [ ] Submitted ≥1 day before the deadline (A1)
**Dependencies:** I-17, I-18, I-20

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-21) in ISSUES.md. Follow their rules exactly.
Branch: i21-submit from up-to-date main. Commit messages: "[I-21] ...".

This is human-only work (owner:human). The agent may only help with the checks below. It must not write slide text, narration, or reviews.
Steps for Waleed:
1. Upload the MP4 to Google Drive, set sharing to "Anyone with the link", copy the link.
2. Write it as the only line of video_url.txt.
3. Run python scripts/check_submission.py and fix anything it reports.
4. Open the link in a private window to confirm it plays.
5. Submit workbook.html and video_url.txt on Gradescope and add Aditya to the group submission.
6. Confirm the Gradescope autograder passes. Target: at least 1 day before the deadline.
Helper prompt for the agent: "Run python scripts/check_submission.py and explain any failure in one line each."

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-21] Upload video, write `video_url.txt`, submit" for Aditya to review. Do not mark anything done that you did not verify.
```

### I-22 · Complete peer grading (each member)
**Labels:** `type:submission` `area:infra` `P0` `status:blocked` `owner:human` `Order 11` `Waleed` `Aditya`
**Context & Scope:** Each student uploads an empty `responses.txt` to the peer-grading assignment, grades the assigned projects, then re-uploads the completed file. Worth 4 marks.
**Acceptance Criteria:**
- [ ] Every member's `responses.txt` passes the Gradescope format check
**Dependencies:** I-21 and instructor release (week 11)

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-22) in ISSUES.md. Follow their rules exactly.
Branch: i22-peer from up-to-date main. Commit messages: "[I-22] ...".

This is human-only work (owner:human). The agent may only help with the checks below. It must not write slide text, narration, or reviews.
Each of us does this separately once peer assignments are released (week 11). Worth 4 marks each.
1. Upload an empty responses.txt to the peer grading assignment on Gradescope to get your assignments.
2. Watch each assigned video while following its notebook; grade each of the 5 sections on the 0 to 5 rubric.
3. Fill in responses.txt in the required format and re-upload; confirm the format check passes.
No agent prompt: reviews are written by you.

If you changed any code, notebook or test, `bash scripts/check.sh` must pass (it runs the same stages as CI); paste its last lines in the PR.
Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-22] Complete peer grading (each member)" for the other person to review. Do not mark anything done that you did not verify.
```

### I-23 · Set up CI pipeline (format, lint, audit, tests)
**Labels:** `type:setup` `area:infra` `P0` `status:review` `owner:agent-ok` `Order 2` `Waleed`
**Context & Scope:** `.github/workflows/ci.yml` runs 6 stages in order, each only if the previous passed: 1 `ruff format --check`, 2 `ruff check`, 3 `pip-audit -r requirements-dev.txt`, 4 `pytest tests/unit` (+ coverage, informational), 5 `pytest tests/integration` + `nbmake` on `notebooks/`, 6 `pytest tests/e2e` (executes `workbook.ipynb` on `tests/fixtures` and checks the exported HTML). Python 3.12. `scripts/check.sh` runs the same stages locally. `.github/dependabot.yml` opens weekly dependency update PRs. No browser tests: there is no web app.
**Acceptance Criteria:**
- [x] `ci.yml` with the 6 stages chained via `needs`
- [x] `scripts/check.sh` runs the same stages locally and passes on Python 3.12
- [x] Unit tests for the issue scripts; e2e test skips until `workbook.ipynb` exists, then enforces headings, no errors, embedded plots
- [ ] CI is green on GitHub for the PR
- [ ] `main` branch rule requires CI to pass before merging (Waleed: Settings, Branches)
**Dependencies:** I-01

**Agent prompt** (paste into your coding agent):
```text
Read AGENTS.md and HANDOFF.md first, then this issue (I-23) in ISSUES.md. Follow their rules exactly.
Branch: i23-ci from up-to-date main. Commit messages: "[I-23] ...".

Task: keep the CI pipeline working. Only change .github/workflows/ci.yml, .github/dependabot.yml, scripts/check.sh, pyproject.toml or tests/ as the fix requires.
Steps:
1. Run bash scripts/check.sh and read the first failing stage.
2. Fix the cause, not the check: do not loosen ruff rules, skip tests, or ignore audit findings without writing the reason in HANDOFF.md section 5.
3. If a dependency has a vulnerability, bump its pin to the fixed version that supports Python 3.12 and rerun the full check.
Verify: bash scripts/check.sh passes locally and the CI run on the PR is green.

Before you stop: tick the acceptance criteria you met in ISSUES.md, add a dated entry to HANDOFF.md section 5 (what you did, what is left, exact next step), push, and open a PR titled "[I-23] Set up CI pipeline (format, lint, audit, tests)" for Aditya to review. Do not mark anything done that you did not verify.
```
