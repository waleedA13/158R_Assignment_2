#!/usr/bin/env python3
"""Run the course autograder's checks on our submission before uploading it.

Mirrors the "How your submission is verified" code in docs/spec.pdf step for step.
Usage (repo root, in the venv):  python scripts/check_submission.py [folder]
"""

import sys
from pathlib import Path

import magic
import requests

CHUNK = 1024 * 1024
REQUIRED = ["workbook.html", "video_url.txt"]


class CheckError(Exception):
    """A check that the autograder would fail."""


def missing_files(folder: Path) -> list[str]:
    return [name for name in REQUIRED if not (Path(folder) / name).exists()]


def check_workbook(path: Path) -> None:
    if not Path(path).read_text(encoding="utf-8", errors="replace").startswith("<!DOCTYPE html>"):
        raise CheckError(
            "workbook.html is not a html file (does not start with '<!DOCTYPE html>'). "
            "Export it with nbconvert; do not just rename the .ipynb."
        )


def read_video_url(path: Path) -> str:
    lines = [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) != 1:
        raise CheckError(f"video_url.txt must contain a single line with the link (found {len(lines)}).")
    return lines[0]


def drive_file_id(url: str) -> str | None:
    """Same parsing as the autograder: text after 'id=' or '/d/', up to the next '/'."""
    if "id=" in url:
        return url.split("id=")[1].split("/")[0]
    if "/d/" in url:
        return url.split("/d/")[1].split("/")[0]
    return None


def first_chunk(url: str, get) -> bytes:
    return next(get(url, stream=True).iter_content(chunk_size=CHUNK), b"")  # empty body: b""


def check_video(url: str, get=requests.get, mime_from_buffer=None) -> str:
    if "youtube" in url or "youtu.be" in url:
        return "YouTube link: no further checks. Make sure the video is publicly viewable."

    file_id = drive_file_id(url)
    if file_id is None:
        raise CheckError(
            "Couldn't determine the Google Drive file ID. Expected "
            "https://drive.google.com/file/d/FILE_ID/view?usp=drive_link"
        )

    chunk = first_chunk(f"https://drive.google.com/uc?export=download&id={file_id}", get)
    if len(chunk) < CHUNK:
        text = chunk.decode("utf8", errors="replace")
        if "Virus scan warning" not in text:
            raise CheckError("The video file is less than 1mb; it is probably not a video (check sharing).")
        if 'uuid" value="' not in text:
            raise CheckError(
                "Could not follow Google's virus scan page (no uuid found). Check the sharing link."
            )
        uuid = text.split('uuid" value="')[1].split('"')[0]
        chunk = first_chunk(
            f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t&uuid={uuid}",
            get,
        )

    mime = (mime_from_buffer or magic.Magic(mime=True).from_buffer)(chunk)
    if "video/mp4" not in mime:
        raise CheckError(f"The file is not an mp4 video file (type={mime}). Convert it to H.264/AAC MP4.")
    return f"Drive file {file_id}: larger than 1mb and video/mp4."


def main(argv=None, folder=None) -> int:
    folder = Path(folder or (argv or sys.argv[1:] or ["."])[0])
    try:
        missing = missing_files(folder)
        if missing:
            raise CheckError("Missing required files: " + ", ".join(missing))
        check_workbook(folder / "workbook.html")
        print("PASS workbook.html starts with <!DOCTYPE html>")
        print("PASS " + check_video(read_video_url(folder / "video_url.txt")))
    except CheckError as e:
        print(f"FAIL {e}")
        return 1
    print("All autograder checks passed. Also download the video once and watch it end to end.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
