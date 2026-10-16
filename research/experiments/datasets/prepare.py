import csv
import json
from pathlib import Path


def write_jsonl(path, rows):
    """Write a list of dictionaries to a file, one JSON object per line."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} rows -> {path}")


def read_csv(path):
    """Read a CSV file into a list of dictionaries, one per row."""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

import pandas as pd

NAMES = ("admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion",
         "curiosity", "desire", "disappointment", "disapproval", "disgust", "embarrassment",
         "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness", "optimism",
         "pride", "realization", "relief", "remorse", "sadness", "surprise", "neutral")    