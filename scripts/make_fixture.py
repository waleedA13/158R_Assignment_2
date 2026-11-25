#!/usr/bin/env python3
"""Write tests/fixtures/renttherunway_final_data.json.gz: 200 synthetic transactions in the raw
file's exact format (plus 2 duplicate lines), so tests and CI never need the real data.
No real reviews or IDs are used. Run from the repo root: python scripts/make_fixture.py
"""

import gzip
import json
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "renttherunway_final_data.json.gz"
rng = random.Random(158)

BODY = ["hourglass", "athletic", "petite", "straight & narrow", "pear", "full bust", "apple"]
CATEGORY = ["dress", "gown", "sheath", "romper", "jumpsuit", "top", "skirt"]
OCCASION = ["wedding", "formal affair", "party", "work", "everyday", "vacation", "date", "other"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August"]


def row(i: int) -> dict:
    fit = rng.choices(["fit", "small", "large"], weights=[74, 13, 13])[0]
    r = {
        "fit": fit,
        "user_id": str(100000 + rng.randrange(60)),
        "bust size": f"{rng.choice([32, 34, 36, 38])}{rng.choice('abcd')}",
        "item_id": str(2000000 + rng.randrange(30)),
        "weight": f"{rng.randrange(100, 200)}lbs",
        "rating": str(rng.choice([2, 4, 6, 8, 10, 10, 10])),
        "rented for": rng.choice(OCCASION),
        "review_text": f"Synthetic review {i}.",
        "body type": rng.choice(BODY),
        "review_summary": f"Synthetic summary {i}",
        "category": rng.choice(CATEGORY),
        "height": f"{rng.choice([4, 5, 5, 5, 6])}' {rng.randrange(12)}\"",
        "size": rng.randrange(0, 40),
        "age": str(rng.randrange(18, 60)),
        "review_date": f"{rng.choice(MONTHS)} {rng.randrange(1, 29)}, {rng.randrange(2012, 2018)}",
    }
    # Missing-value pattern similar to the real file (weight 15.6%, bust 9.6%, body type 7.6%).
    for field, p in (("weight", 0.16), ("bust size", 0.10), ("body type", 0.08), ("age", 0.01)):
        if rng.random() < p:
            del r[field]
    return r


rows = [row(i) for i in range(200)]
rows[0]["fit"], rows[1]["fit"], rows[2]["fit"] = "fit", "small", "large"  # all classes present
rows[5]["rating"] = None
lines = rows + [rows[0], rows[1]]  # 2 exact duplicates, dropped by src.data.load()
OUT.parent.mkdir(parents=True, exist_ok=True)
with gzip.GzipFile(OUT, "wb", mtime=0) as f:
    f.write("".join(json.dumps(r) + "\n" for r in lines).encode())
print(f"wrote {len(lines)} lines to {OUT}")
