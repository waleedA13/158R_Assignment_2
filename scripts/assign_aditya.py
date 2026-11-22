#!/usr/bin/env python3
"""Assign Aditya to every open issue labelled "Aditya". Run after he accepts the collaborator invite."""

import json
import subprocess

R = "repos/waleedA13/158R_Assignment_2"
issues = json.loads(
    subprocess.run(
        ["gh", "api", f"{R}/issues?state=open&labels=Aditya&per_page=100"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
)
for i in issues:
    subprocess.run(
        [
            "gh",
            "api",
            "-X",
            "POST",
            f"{R}/issues/{i['number']}/assignees",
            "-f",
            "assignees[]=AdityaJadhav17",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    print(f"assigned #{i['number']} {i['title']}")
