"""End-to-end check of what graders see: workbook.ipynb executed and exported to HTML.

Skips until workbook.ipynb exists (I-16). From then on it executes the notebook
(on the fixture data when DATA_DIR points at tests/fixtures), exports it, and checks
the HTML. If a committed workbook.html exists, that file is checked too.
"""

import os
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / "workbook.ipynb"
COMMITTED_HTML = ROOT / "workbook.html"
SECTIONS = ["Predictive Task", "Exploratory", "Modeling", "Evaluation", "Related Work"]


def check_html(html: str) -> None:
    assert html.startswith("<!DOCTYPE html>"), "autograder requires the file to start with <!DOCTYPE html>"
    headings = " ".join(re.findall(r"<h[12][^>]*>(.*?)</h[12]>", html, flags=re.S | re.I))
    for section in SECTIONS:
        assert re.search(section, headings, re.I), f"missing section heading: {section}"
    assert "Traceback (most recent call last)" not in html, "an output cell shows an error"
    assert not re.search(r'class="[^"]*output_error', html), "an output cell shows an error"
    assert re.search(r'<img[^>]+src="data:image/png;base64,', html), "no embedded plot found"


@pytest.mark.skipif(not NOTEBOOK.exists(), reason="workbook.ipynb not created yet (I-16)")
def test_workbook_executes_and_exports(tmp_path):
    env = {**os.environ, "DATA_DIR": os.environ.get("DATA_DIR", str(ROOT / "tests" / "fixtures"))}
    subprocess.run(
        ["jupyter", "nbconvert", "--to", "html", "--execute", str(NOTEBOOK), "--output-dir", str(tmp_path)],
        check=True,
        cwd=ROOT,
        env=env,
    )
    check_html((tmp_path / "workbook.html").read_text(encoding="utf-8"))


@pytest.mark.skipif(not COMMITTED_HTML.exists(), reason="workbook.html not exported yet (I-17)")
def test_committed_workbook_html():
    check_html(COMMITTED_HTML.read_text(encoding="utf-8"))


def test_check_html_rejects_a_bad_export():
    with pytest.raises(AssertionError):
        check_html("<html><h1>Modeling</h1>Traceback (most recent call last)</html>")
