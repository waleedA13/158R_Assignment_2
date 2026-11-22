# HANDOFF.md — 158R Assignment 2

> Single source of truth for every collaborator and every AI agent. Read this first; update it last (see §6).
> Issue details live in [`ISSUES.md`](ISSUES.md).

_Last updated: 2026-11-21 by Claude (initial setup) · Repo state at that time: 1 commit (`eacade8 Initial commit`), README only._

---

## 0. Assumptions (verify — edit this list when confirmed)

| # | Assumption | Why it matters | Confirm with |
|---|---|---|---|
| A1 | **Submission due Tue of week 10 ≈ Tue 2026-12-01** (UCSD Fall '26). Peer grading due in week 11. | Drives every deadline below | Gradescope |
| A2 | **Late submissions not accepted** (OSD-only late window) | No slack — internal freeze is 2 days early | Spec |
| A3 | Group size and members not yet known (max 4) | Owners in ISSUES.md are blank | Team |
| A4 | **No dataset or predictive task chosen yet** | Blocks almost everything (I-03) | Team |
| A5 | Stack: Python 3 + Jupyter, pandas/numpy/scikit-learn/matplotlib (course-standard). Nothing installed in repo yet | Proposed layout in §2 | I-01 |
| A6 | Spec PDF lives *outside* this repo at `../Assignment 2/158 _ 258 2026 Assignment 2.pdf` | Agents can't see it unless copied in | I-02 |
| A7 | GitHub remote `waleedA13/158R_Assignment_2` is the shared repo; issues not yet created on GitHub | Use ISSUES.md until imported | Repo owner |

**Internal milestones (from A1):** Sun 11-22 decision locked · Wed 11-25 models + eval done · Fri 11-27 notebook frozen · Sun 11-29 video recorded · **Mon 11-30 submitted** (1-day buffer).

---

## 1. Project Snapshot

- **What we're building:** a peer-graded ML project for CSE 158R: one predictive task on a dataset of our choice, delivered as
  1. `workbook.html` — Jupyter notebook exported to HTML (graders read it, don't run it)
  2. `video_url.txt` — one line: Google Drive ("anyone with link") or YouTube link to a **~20 min MP4** (≤ ~22 min)
  3. Peer grading `responses.txt` (each student, ~1 week later)
- **Grading:** 29 marks = 5 sections × 5 + 4 for peer grading. Video and notebook are graded **together** — what's said must match the code.
- **The 5 graded sections:** (1) Predictive task · (2) EDA / data / preprocessing · (3) Modeling · (4) Evaluation · (5) Related work.
- **Hard rule from the rubric:** a presentation that "seems to be automatically generated" scores **1/5**. Agents may draft code and analysis; **slides wording and narration are written and spoken by humans.**
- **Current state:** nothing built. README is a title only. No code, data, deps, or branches.
- **Key entry points (once built):** `workbook.ipynb` (final deliverable source) · `src/data.py` (shared loader + split) · `scripts/check_submission.py` (local autograder).

## 2. Architecture & Key Paths (proposed — created by I-01)

```
158R_Assignment_2/
├── HANDOFF.md              # this file
├── ISSUES.md               # issue backlog + label system
├── AGENTS.md / CLAUDE.md   # 2-line pointer to HANDOFF.md (so agents auto-load it)
├── README.md
├── requirements.txt        # pinned deps
├── .gitignore              # ignores data/, *.mp4, .ipynb_checkpoints, __pycache__
├── docs/
│   ├── spec.pdf            # copy of assignment spec (I-02)
│   ├── decision.md         # dataset + task + metric decision record (I-03)
│   └── related_work.md     # notes + citations (I-14)
├── data/                   # NOT committed. raw/ and processed/ ; download script documents source
├── src/
│   ├── data.py             # load(), split(seed=158) -> train/valid/test  ← the ONE split everyone uses
│   ├── metrics.py          # every metric used in the report
│   └── models.py           # baselines + models with a common fit/predict interface
├── notebooks/              # per-section DRAFT notebooks, one owner each
│   ├── 01_task.ipynb  02_eda.ipynb  03_models.ipynb  04_eval.ipynb
├── workbook.ipynb          # FINAL assembled notebook (I-16). Sections 1–5 as top-level headings
├── workbook.html           # export of the above (submitted)
├── video_url.txt           # submitted
├── slides/                 # deck source/export (I-19)
└── scripts/
    ├── check_submission.py # replicates the autograder from the spec (I-18)
    └── export.sh           # execute + export workbook (I-17)
```

- **Core logic:** `src/` (shared). **Schemas/config:** split seed + paths as constants at top of `src/data.py`. **Tests:** `scripts/check_submission.py` + "notebook runs top-to-bottom" (§3).
- **Why `src/` + inlining:** graders only see `workbook.html`, so code in `src/` must be **inlined or `%load`-ed into `workbook.ipynb`** during assembly. `src/` exists so drafts share one split and one metric implementation.

## 3. Agent & Collaborator Protocol

**Claiming work**
1. Pick an issue labelled `status:ready` with no open dependencies.
2. Put your name/agent tag in its **Owner** field in `ISSUES.md` *and* set `status:in-progress` — commit that change alone, push it **before** starting. First push wins.
3. One owner per issue. One owner per notebook file. Never edit a notebook you don't own — open a note in `HANDOFF.md §5` instead.

**Branches & commits**
- Branch: `i<NN>-<short-slug>` → e.g. `i09-latent-factor`. Branch from up-to-date `main`.
- Commit: `[I-09] add latent factor model with bias terms` (imperative, issue ID first).
- Small PRs into `main`; another person (or the issue owner's partner) skims before merge. Squash-merge.
- **Notebooks:** clear outputs before committing drafts (`jupyter nbconvert --clear-output --inplace notebooks/*.ipynb`) to keep diffs mergeable. Exception: `workbook.ipynb` is committed **with outputs** once frozen.
- Never commit `data/`, videos, credentials, or the Drive link's private sharing settings.

**Shared invariants (don't break)**
- Everyone uses `src/data.split()` with the fixed seed. No private splits. Test set touched only in I-12/I-13.
- All metrics come from `src/metrics.py`. Report numbers only from code that's in the repo.
- Every number shown in slides must appear in `workbook.html`.

**Commands (valid once I-01/I-17/I-18 land)**
```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace workbook.ipynb   # must run clean top-to-bottom
bash scripts/export.sh                                               # -> workbook.html
python scripts/check_submission.py                                   # local autograder
```

**Agent-specific rules**
- Ground claims in repo files; don't invent results, citations, or dataset facts. Cite related work with real links in `docs/related_work.md`.
- Issues labelled `owner:human` (video, slides wording, peer grading, Gradescope upload, Drive sharing) are **off-limits to agents** except for checklists or tooling.
- If blocked, set `status:blocked`, write why in §5, and stop — don't work around a team decision.

## 4. Current Priorities & Active Work

| State | Issues |
|---|---|
| ✅ Done | Repo created (`eacade8`). Spec breakdown + this plan (I-00). |
| 🔄 In progress | — |
| 🟢 Ready now | **I-01** scaffold · **I-02** copy spec in · **I-03** choose dataset + task (**top priority — blocks most work**) · **I-18** submission checker |
| ⏳ Next after I-03 | I-04 loader/split → then I-05, I-06/07, I-08, I-14 can run **in parallel** |
| 🧱 Critical path | I-03 → I-04 → I-08 → I-09/I-10 → I-12 → I-16 → I-17 → I-19 → I-20 → I-21 |

## 5. Session Log & Open Notes (append newest on top)

- **2026-11-21 · Claude:** Inspected repo (README only, 1 commit, `main` only, no TODOs). Wrote `HANDOFF.md` + `ISSUES.md`. Nothing committed to git. Open: A1–A4 need human confirmation; issues not yet on GitHub.

## 6. Handoff Checklist (before ending ANY session)

- [ ] Work committed on your `i<NN>-…` branch and pushed (or merged). No uncommitted notebook outputs in drafts.
- [ ] `ISSUES.md`: your issue's `status:` label and acceptance-criteria checkboxes updated; Owner cleared if you're abandoning it.
- [ ] `HANDOFF.md §4` table reflects reality (move issues between rows).
- [ ] `HANDOFF.md §5`: one dated entry — what you did, what's half-done, exact next step, any new numbers produced (with the notebook cell they come from).
- [ ] New assumptions or decisions added to §0 or `docs/decision.md`.
- [ ] If you changed `src/` interfaces, split, or metrics: say so in §5 in **bold** — it affects everyone.
- [ ] `_Last updated_` line at the top bumped.
