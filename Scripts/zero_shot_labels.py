#!/usr/bin/env python
from pathlib import Path
import pandas as pd
from src.regailens.viz import summarize_texts

DATA = Path(__file__).resolve().parents[1] / "data"
CORPUS = DATA / "corpus.csv"
SUMMARIES = DATA / "summaries.csv"

def main():
    if not CORPUS.exists():
        print(f"Corpus file not found at {CORPUS}. Skipping summaries.")
        return

    df = pd.read_csv(CORPUS)
    if df.empty:
        print("Corpus is empty. No summaries to generate.")
        return

    summaries = summarize_texts(df["text"].tolist())
    df["summary"] = summaries
    df.to_csv(SUMMARIES, index=False)
    print(f"Saved summaries to {SUMMARIES}")

if __name__ == "__main__":
    main()
