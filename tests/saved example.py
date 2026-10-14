"""Label saved chat turns by hand. Usage: python examples/label.py"""
import json
from pathlib import Path

PATH = Path("data/turns.jsonl")
LABELS = ("neutral", "happy", "sad", "angry", "anxious", "surprised", "disgusted")


def load_rows(path):
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def save_rows(path, rows):
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    rows = load_rows(PATH)
    todo = [r for r in rows if r["label"] is None]
    print(f"{len(todo)} unlabeled of {len(rows)} turns. Labels: {', '.join(LABELS)}  (s=skip, q=quit)")

    for row in todo:
        print(f"\nyou said: {row['user_text']}")
        print(f"ECHO guessed: {row['emotion']} ({row['emotion_confidence']:.2f})")
        answer = input("true emotion> ").strip().lower()
        if answer == "q":
            break
        if answer == "s":
            continue
        if answer in LABELS:
            row["label"] = answer
        else:
            print("not a valid label, skipped")

    save_rows(PATH, rows)
    labeled = sum(1 for r in rows if r["label"] is not None)
    print(f"saved. {labeled} labeled turns total.")


if __name__ == "__main__":
    main()