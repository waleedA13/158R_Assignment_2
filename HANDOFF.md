# HANDOFF.md: 158R Assignment 2

> Single source of truth for every collaborator and every AI agent. Read this first; update it last (see §6).
> Issue details live in [`ISSUES.md`](ISSUES.md).

_Last updated: 2026-11-22 (setup complete, ready to start issues) · Repo state: `main` at `6fd0ae0`; planning files and scripts only, no project code yet._

---

## 0. Assumptions (verify, then edit this list when confirmed)

| # | Assumption | Why it matters | Confirm with |
|---|---|---|---|
| A1 | **Submission due Tue 2026-12-01** (Tuesday of week 10: UCSD Fall '26 instruction began Thu Sep 24). Exact time not yet checked. Peer grading due in week 11. | Drives every deadline below | Gradescope (time of day) |
| A9 | **Thanksgiving Thu to Fri, Nov 26 to 27.** Planned as buffer days, not work days | Schedule in ISSUES.md "Day-by-day plan" | Team |
| A2 | **Late submissions not accepted** (OSD-only late window) | No slack, so the internal freeze is 2 days early | Spec |
| A3 | **Team of 2:** Waleed (`waleedA13`) and Aditya (`AdityaJadhav17`, not yet a collaborator) | Aditya's issues are assigned once he accepts the invite (`scripts/assign_aditya.py`) | Team |
| A4 | **Confirmed 2026-11-24:** Rent the Runway, predict fit (small / fit / large); average AUC + macro-F1; random 80/10/10 split. Full record: `docs/decision.md` | Every issue follows it | Waleed + Aditya on #25 |
| A5 | **Python 3.12** (3.10 is end of life and blocks security fixes). Jupyter, pandas 3, numpy 2, scikit-learn, matplotlib; versions pinned in `requirements.txt`, tools in `requirements-dev.txt` | Everyone uses a 3.12 venv | Confirmed by Waleed |
| A6 | Spec is in the repo: `docs/spec.pdf`, summarized in `docs/requirements.md` (the PDF wins on conflicts) | Agents read requirements.md | Done (I-02) |
| A7 | GitHub issues are the live tracker, titled `[I-NN] ...`. `docs/github_issue_map.md` maps IDs to issue numbers. Issues are #23 to #44. After editing ISSUES.md, run `scripts/sync_issues.py` (updates in place); `create_github_issues.py` is only for a full rebuild. Run both on your own machine only | Find work by I-NN | Repo owner |
| A8 | Work split Waleed/Aditya (see ISSUES.md "Parts and roles"), tracked by `Waleed` / `Aditya` labels | Filter by label to see your queue | Team |

**Internal milestones:** Sun 11-22 decision locked · Wed 11-25 models + eval done, slides started · Fri 11-27 notebook frozen · Sat 11-28 slides done + 2 rehearsals · Sun 11-29 video recorded · **Mon 11-30 submitted** (Tue 12-01 spare). Full day-by-day plan and talk time budget: ISSUES.md "Parts and roles".

---

## 1. Project Snapshot

- **What we're building:** a peer-graded ML project for CSE 158R: one predictive task on a dataset of our choice, delivered as
  1. `workbook.html`: Jupyter notebook exported to HTML (graders read it, don't run it)
  2. `video_url.txt`: one line: Google Drive ("anyone with link") or YouTube link to a **~20 min MP4** (≤ ~22 min)
  3. Peer grading `responses.txt` (each student, ~1 week later)
- **Grading:** 29 marks = 5 sections × 5 + 4 for peer grading. Video and notebook are graded **together**, so what's said must match the code.
- **The 5 graded sections:** (1) Predictive task · (2) EDA / data / preprocessing · (3) Modeling · (4) Evaluation · (5) Related work.
- **Hard rule from the rubric:** a presentation that "seems to be automatically generated" scores **1/5**. Agents may draft code and analysis; **slides wording and narration are written and spoken by humans.**
- **Current state:** planning is done, project work not started. In the repo: `AGENTS.md`, `HANDOFF.md`, `ISSUES.md`, `scripts/` (GitHub issue tools), `docs/github_issue_map.md`, a minimal `.gitignore`. `docs/spec.pdf` is on disk but uncommitted (it goes in with I-02). No code, data, dependencies or feature branches yet.
- **Key entry points (once built):** `workbook.ipynb` (final deliverable source) · `src/data.py` (shared loader + split) · `scripts/check_submission.py` (local autograder).

## 2. Architecture & Key Paths (proposed, created by I-01)

```
158R_Assignment_2/
├── HANDOFF.md              # this file
├── ISSUES.md               # issue backlog + label system
├── AGENTS.md              # shared agent instructions; both maintain it. Every issue prompt says to read it
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
├── workbook.ipynb          # FINAL assembled notebook (I-16). Sections 1 to 5 as top-level headings
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
0. Your queue is the label with your name (`Waleed` or `Aditya`) on GitHub. Work it in milestone order; help the other person only within the same Part.
1. Pick an issue labelled `status:ready` with no open dependencies.
2. Put your name/agent tag in its **Owner** field in `ISSUES.md` *and* set `status:in-progress`. Commit that change alone, push it **before** starting. First push wins.
3. One owner per issue. One owner per notebook file. Never edit a notebook you don't own. Leave a note in `HANDOFF.md §5` instead.

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

**Commands**
```bash
pip install -r requirements-dev.txt     # inside a Python 3.12 venv
bash scripts/check.sh                   # same 6 stages as CI; must pass before every push
bash scripts/export.sh                  # -> workbook.html (after I-17)
python scripts/check_submission.py      # local autograder (after I-18)
```
**CI** (`.github/workflows/ci.yml`, I-23): 1 format, 2 lint, 3 dependency audit, 4 unit, 5 integration + notebooks, 6 e2e workbook HTML. Each stage runs only if the previous passed. Code issues are test-first.

**Agent-specific rules** (full list in `AGENTS.md`)
- Each issue ends with an **Agent prompt**: paste it into your coding agent. Prompts start with "Read AGENTS.md and HANDOFF.md first".
- Never write to GitHub from a remote or hosted agent session that adds attribution footers; run GitHub scripts locally with your own `gh` login.
- Ground claims in repo files; don't invent results, citations, or dataset facts. Cite related work with real links in `docs/related_work.md`.
- Issues labelled `owner:human` (video, slides wording, peer grading, Gradescope upload, Drive sharing) are **off-limits to agents** except for checklists or tooling.
- If blocked, set `status:blocked`, write why in §5, and stop. Don't work around a team decision.

## 4. Current Priorities & Active Work

| State | Issues |
|---|---|
| ✅ Done | I-00 planning: label system, 22 GitHub issues (#23 to #44) with agent prompts, milestones, day-by-day plan, AGENTS.md. |
| 🔄 In progress | none |
| 🟢 Ready now | **I-01** scaffold (#23) · **I-02** spec (#24) · **I-03** choose dataset + task (#25, **top priority, blocks most work**) · **I-18** submission checker (#40, after I-01) |
| ⚠️ Waiting | Aditya to accept the GitHub invite, then Waleed runs `scripts/assign_aditya.py` |
| ⏳ Next after I-03 | I-04 loader/split → then I-05, I-06/07, I-08, I-14 can run **in parallel** |
| 🧱 Critical path | I-03 → I-04 → I-08 → I-09/I-10 → I-12 → I-16 → I-17 → I-19 → I-20 → I-21 |

## 5. Session Log & Open Notes (append newest on top)

- **2026-11-24 · agent (I-03):** Aditya agreed on #25: option A with defaults. Wrote `docs/decision.md`, ticked I-03 criteria, A4 confirmed. Schedule is 2 days behind: Thanksgiving is now a work day and I-11 (tuning) is cut (see the catch-up plan given on 11-24). Next: merge the I-03 PR, then I-04 (Waleed, needs the data file in `data/raw/`), I-05 and I-14 (Aditya).

- **2026-11-24 · agent (I-14):** On `i14-related` (from `main`): `docs/related_work.md` with 3 sources (Misra et al. 2018, Sheikh et al. 2019, Sembium et al. 2017), each with citation, opened link, summary, method, metric, split and numbers read from the paper tables. Notes the AUC averaging differs between papers and that Sembium reports only percentage gains on proprietary data. Not pushed, no PR yet. Next: push, open PR "[I-14] Related-work research notes with citations", then I-15 once I-12 is done.

- **2026-11-24 · agent (I-05):** On `i05-task`: `notebooks/01_task.ipynb`, four markdown cells (task, evaluation, baselines, validity), about 370 words, no outputs. Written from option A in `docs/options.md` and the agreement in issue #25, because `docs/decision.md` does not exist yet. `bash scripts/check.sh` passes (Python 3.12). Left: re-check the wording against `docs/decision.md` once it lands, and replace the planned leakage guard text with the real `src/data.py` details after I-04. Pushed as PR #52.

- **2026-11-22 · agent (I-18):** `scripts/check_submission.py` on `i18-checker`, test-first (17 unit tests committed failing, then implemented). Mirrors the spec's autograder code exactly, including the Drive virus-scan page. Network faked in tests. Open: the first criterion (pass on a real MP4 Drive link) can only be ticked once the video exists (I-21).

- **2026-11-22 · agent (I-03 prep):** `docs/options.md` on `i03-options`: 3 candidates (A Rent the Runway fit prediction, B BeerAdvocate rating prediction, C Steam next-game recommendation) with sizes, fields, metrics, baselines and paper numbers read from the linked PDFs. Not a decision. Next: Waleed + Aditya pick one, write `docs/decision.md`, close I-03.

- **2026-11-22 · agent (I-02):** On `i02-spec` (stacked on `i23-ci`): `docs/spec.pdf` (identical to the original) and `docs/requirements.md` (72-line paraphrase: deadlines, deliverables, 5 sections, rubric, 7 autograder checks, peer grading). Verified 30/30 spec items present. Next: I-03 decision with Aditya, I-18 checker.

- **2026-11-22 · agent (I-23):** CI on `i23-ci` (stacked on `i01-scaffold`): `ci.yml` with 6 chained stages, `scripts/check.sh`, Dependabot, unit tests for the issue scripts, integration smoke test, e2e workbook HTML test (skips until I-16; verified it passes on a good export and fails on an error cell). All stages pass on Python 3.12. Added I-23 to ISSUES.md and a tests-first step to the prompts of I-04, I-07 to I-10, I-12, I-18; I-04 now defines `DATA_DIR` + `tests/fixtures/`. `sync_issues.py` can now create new issues. Next: Waleed pushes, opens PRs, runs `sync_issues.py` after merge, adds the branch rule.

- **2026-11-22 · agent (I-01):** Scaffold on `i01-scaffold`: folders incl. `tests/{unit,integration,e2e,fixtures}`, `src/` stubs, `.gitignore`, `pyproject.toml` (ruff + pytest config), pinned `requirements.txt` / `requirements-dev.txt` for **Python 3.12** (`.python-version`), README setup. Verified: fresh 3.12 install, `pip-audit` clean, ruff format + lint pass, src imports, `data/` ignored. Also reformatted `scripts/*.py` to pass ruff. Next: I-23 CI.

- **2026-11-22 · agent:** Rebuild done: issues #23 to #44, prompts present, no footers, no app tag. They predate the schedule fix, so added `scripts/sync_issues.py`; dry run shows 7 issues + 3 milestones to update. Aditya still not a collaborator (9 issues unassigned).

- **2026-11-22 · agent:** Checked plan against the spec and UCSD calendar. Deadline confirmed as Tue 12-01; Thanksgiving 11-26/27 made buffer. Slides (I-19) now start Wed 11-25 (Order 3); presentation gets about 3 days. I-07, I-13, I-15 raised to P0 (spec requires them). Added day-by-day plan and talk time budget to ISSUES.md. I-11, I-13, I-15 moved to Part 4. Not yet on GitHub: Waleed must run `scripts/create_github_issues.py`.

- **2026-11-21 · agent:** Added `AGENTS.md` (shared instructions, replaces any other agent file). Every issue in ISSUES.md now has an agent prompt; labels are `P0`/`P1`, `Order N`, `Waleed`/`Aditya`. `scripts/create_github_issues.py` now deletes the old issues and recreates them from Waleed's machine; `scripts/assign_aditya.py` assigns Aditya after he accepts the invite. Next: Waleed runs both scripts.

- **2026-11-21 · agent:** Renamed labels `role:P1` -> `Waleed`, `role:P2` -> `Aditya` on GitHub and in docs/script.

- **2026-11-21 · agent:** Added label descriptions and `Order 1` to `Order 11` labels (dependency sequence) on GitHub and in ISSUES.md. Note: priority labels on GitHub are now `P0`/`P1` (renamed on GitHub); docs still say `priority:p0`/`p1`.

- **2026-11-21 · agent:** Team is 2 people. Replaced `role:A` to `role:D` with `role:P1` (waleedA13) / `role:P2` (teammate) on GitHub. P1 assigned. Next: invite P2 as collaborator and assign `role:P2` issues.

- **2026-11-21 · agent:** Created on GitHub: labels (incl. `role:A` to `role:D`), 6 milestones, issues #1 to #22 in I-NN order. Assigned `waleedA13` to role A + everyone issues. Script switched to REST (`gh api`). Next: invite teammates, then assign by `role:` label.

- **2026-11-21 · agent:** Inspected repo (README only, 1 commit, `main` only, no TODOs). Wrote `HANDOFF.md` + `ISSUES.md`. Nothing committed to git. Open: A1 to A4 need human confirmation; issues not yet on GitHub.
- **2026-11-21 · agent:** Added `scripts/create_github_issues.py` (labels, 6 milestones, 22 ordered issues, role-based assignees). Dry run passes. Needs ROLES usernames filled in, then run with `gh`.

## 6. Handoff Checklist (before ending ANY session)

- [ ] Work committed on your `i<NN>-…` branch and pushed (or merged). No uncommitted notebook outputs in drafts.
- [ ] `ISSUES.md`: your issue's `status:` label and acceptance-criteria checkboxes updated; Owner cleared if you're abandoning it.
- [ ] `HANDOFF.md §4` table reflects reality (move issues between rows).
- [ ] `HANDOFF.md §5`: one dated entry: what you did, what's half-done, exact next step, any new numbers produced (with the notebook cell they come from).
- [ ] New assumptions or decisions added to §0 or `docs/decision.md`.
- [ ] If you changed `src/` interfaces, split, or metrics: say so in §5 in **bold**, since it affects everyone.
- [ ] `_Last updated_` line at the top bumped.
