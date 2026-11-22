"""Unit tests for scripts/check_submission.py. The network is always faked."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import check_submission as cs  # noqa: E402

MB = 1024 * 1024
MP4 = b"\x00\x00\x00\x20ftypisom\x00\x00\x02\x00isomiso2avc1mp41" + b"\x00" * MB
SCAN_PAGE = (
    b"<html><title>Google Drive - Virus scan warning</title>"
    b'<form><input type="hidden" name="uuid" value="abc-123"></form></html>'
)


class FakeResponse:
    def __init__(self, data: bytes):
        self.data = data

    def iter_content(self, chunk_size):
        for i in range(0, len(self.data), chunk_size):
            yield self.data[i : i + chunk_size]


class FakeGet:
    """Stands in for requests.get: returns queued payloads and records URLs."""

    def __init__(self, *payloads: bytes):
        self.payloads = list(payloads)
        self.urls = []

    def __call__(self, url, stream=True):
        self.urls.append(url)
        return FakeResponse(self.payloads.pop(0))


# ---- workbook.html
def test_workbook_html_passes(tmp_path):
    p = tmp_path / "workbook.html"
    p.write_text("<!DOCTYPE html>\n<html></html>")
    cs.check_workbook(p)


def test_renamed_ipynb_fails(tmp_path):
    p = tmp_path / "workbook.html"
    p.write_text('{"cells": [], "nbformat": 4}')
    with pytest.raises(cs.CheckError, match="not a html file"):
        cs.check_workbook(p)


# ---- file presence and video_url.txt
def test_missing_files_are_reported(tmp_path):
    assert cs.missing_files(tmp_path) == ["workbook.html", "video_url.txt"]


def test_video_url_is_read_and_stripped(tmp_path):
    (tmp_path / "video_url.txt").write_text("  https://youtu.be/x  \n")
    assert cs.read_video_url(tmp_path / "video_url.txt") == "https://youtu.be/x"


def test_video_url_with_two_lines_fails(tmp_path):
    (tmp_path / "video_url.txt").write_text("https://a\nhttps://b\n")
    with pytest.raises(cs.CheckError, match="single line"):
        cs.read_video_url(tmp_path / "video_url.txt")


# ---- Drive file ID parsing (mirrors the autograder exactly)
@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://drive.google.com/file/d/ABC123/view?usp=drive_link", "ABC123"),
        ("https://drive.google.com/uc?export=download&id=ABC123", "ABC123"),
        ("https://drive.google.com/open?id=ABC123", "ABC123"),
        ("https://example.com/video.mp4", None),
    ],
)
def test_drive_file_id(url, expected):
    assert cs.drive_file_id(url) == expected


# ---- video checks
def test_youtube_link_skips_download():
    get = FakeGet()
    msg = cs.check_video("https://www.youtube.com/watch?v=abc", get=get)
    assert get.urls == []
    assert "publicly viewable" in msg


def test_url_without_file_id_fails():
    with pytest.raises(cs.CheckError, match="file ID"):
        cs.check_video("https://example.com/video.mp4", get=FakeGet())


def test_small_file_fails():
    with pytest.raises(cs.CheckError, match="less than 1mb"):
        cs.check_video("https://drive.google.com/file/d/ID/view", get=FakeGet(b"tiny"))


def test_non_mp4_file_fails():
    with pytest.raises(cs.CheckError, match="not an mp4"):
        cs.check_video("https://drive.google.com/file/d/ID/view", get=FakeGet(b"<html>" + b"x" * MB))


def test_mp4_passes_and_uses_the_download_url():
    get = FakeGet(MP4)
    cs.check_video("https://drive.google.com/file/d/ID/view", get=get)
    assert get.urls == ["https://drive.google.com/uc?export=download&id=ID"]


def test_virus_scan_page_is_followed():
    get = FakeGet(SCAN_PAGE, MP4)
    cs.check_video("https://drive.google.com/file/d/ID/view", get=get)
    assert get.urls[1] == (
        "https://drive.usercontent.google.com/download?id=ID&export=download&confirm=t&uuid=abc-123"
    )


# ---- main
def test_main_returns_0_on_pass(tmp_path, monkeypatch):
    (tmp_path / "workbook.html").write_text("<!DOCTYPE html><html></html>")
    (tmp_path / "video_url.txt").write_text("https://youtu.be/abc\n")
    assert cs.main(folder=tmp_path) == 0


def test_main_returns_1_on_failure(tmp_path):
    (tmp_path / "workbook.html").write_text("not html")
    (tmp_path / "video_url.txt").write_text("https://youtu.be/abc\n")
    assert cs.main(folder=tmp_path) == 1
