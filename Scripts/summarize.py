#!/usr/bin/env python
from pathlib import Path
import pandas as pd
from src.regailens.viz import assign_zero_shot_labels

DATA = Path(__file__).resolve().parents[1] / "data"
CORPUS = DATA / "corpus.csv"
LABELS = DATA / "labels.csv"

def main():
    if not CORPUS.exists():
        print(f"Corpus file not found at {CORPUS}. Skipping zero-shot labeling.")
        return

    df = pd.read_csv(CORPUS)
    if df.empty:
        print("Corpus is empty. No labels to assign.")
        return

    df_labels = assign_zero_shot_labels(df["text"].tolist())
    df["labels"] = df_labels
    df.to_csv(LABELS, index=False)
    print(f"Saved zero-shot labels to {LABELS}")

if __name__ == "__main__":
    main()

