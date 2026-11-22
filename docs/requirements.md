# Assignment 2 requirements (summary of `docs/spec.pdf`)

Our paraphrase of the course spec. If this file and the PDF disagree, the PDF wins.

## Deadlines and rules
- Due **Tuesday of week 10** (Tue 2026-12-01); the exact time is on Gradescope. Peer grades are due in week 11.
- **No late submissions.** The late window exists only for students with an OSD accommodation.
- Groups of up to 4, or solo. Group size does not change grading. Blinding the submission is optional.
- Any dataset is allowed, including the Assignment 1 data. The instructor's dataset list: https://cseweb.ucsd.edu/~jmcauley/datasets.html

## Deliverables (29 marks)
1. **`workbook.html`**: the Jupyter notebook exported to HTML. Clean, documented, readable as is; graders will not run the code.
2. **`video_url.txt`**: one line with a link to a **~20 minute** presentation video (Google Drive or YouTube).
3. **Peer grading report** (`responses.txt`), about a week after submission.

Graders score the notebook and video together: they watch the video while following the code. The spec suggests mixing slides with a code walkthrough.

## The 5 graded sections (5 marks each)
1. **Predictive task**
   - How the model will be evaluated on the task
   - Which baselines make sense for comparison
   - How we will check that the predictions are valid
   - The task and models must relate to course content. Models from other classes are fine, but course models must appear as baselines or comparisons.
2. **Exploratory analysis, data collection, preprocessing**
   - Context: where the dataset comes from, its purpose, how it was collected
   - Discussion: how we processed it, or how it was already processed
   - Code: tables, plots and statistics backing the analysis
3. **Modeling**
   - Context: the task as an ML problem (inputs, outputs, what is optimized) and which models fit
   - Discussion: pros and cons of the approaches (complexity, efficiency, implementation difficulty)
   - Code: walkthrough explaining architectural choices and implementation details
4. **Evaluation**
   - Context: how the task should be evaluated, and why our metrics beat the alternatives
   - Discussion: trivial and non-trivial baselines, and evidence that our method beats them
   - Code: walkthrough of the evaluation protocol, with tables, plots and statistics
5. **Related work** (may go first)
   - How this or similar datasets have been used before
   - How prior work approached the same or similar tasks
   - How our results compare with reported results

Sections may be reordered if the organization stays obvious. Keep the video within about 10% of 20 minutes (about 22 minutes max); graders plan 20 to 30 minutes per submission and may speed up or stop watching long videos.

## Rubric (per section)
| Score | Meaning |
|---|---|
| 0 | Not covered |
| 1 | Covered but has errors, is hard to follow, does not match the code, **or the presentation looks auto-generated** |
| 2 | Superficial: some right parts, missing key elements or comparisons |
| 3 | Minimally acceptable: essentials present, little detail |
| 4 | Feature-complete: results make sense or negative results are explained, tradeoffs between metrics and goals discussed, clear. Expected to be the most common grade |
| 5 | Goes beyond: very thorough, a new or interesting approach, or excellent in another way |

Peer grading itself is worth the remaining 4 marks.

## Submission (Gradescope, step 1)
- Upload `workbook.html` and `video_url.txt`.
- Video link: a Google Drive file shared as "Anyone with the link" (form `https://drive.google.com/file/d/FILE_ID/view?usp=drive_link`) or a YouTube link. Non-MP4 recordings must be converted to MP4 with a common codec. The instructor downloads Drive files and re-shares them; YouTube links are shared as is.

### Autograder checks
1. Both `workbook.html` and `video_url.txt` are present.
2. `workbook.html` starts with `<!DOCTYPE html>` (a renamed `.ipynb` fails).
3. YouTube links: no further checks; the video must be publicly viewable.
4. Drive links: the file ID is read from `id=` or `/d/` in the URL; otherwise the check fails.
5. The file downloads from `https://drive.google.com/uc?export=download&id=FILE_ID`, following Google's virus-scan confirmation page for large files.
6. The first chunk must be at least 1 MB.
7. The file type must be `video/mp4` (checked with `python-magic`).

## Peer grading (step 2)
1. One to two days after the deadline, the instructor posts peer assignments as a separate Gradescope assignment.
2. Upload an empty `responses.txt` there; the autograder prints the assignments and instructions.
3. Grade, then re-upload the completed `responses.txt`. A valid format earns the 4 marks.
4. Marks show as 4/29 until peer grades are compiled, then as the final mark out of 29.
