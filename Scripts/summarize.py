#!/usr/bin/env python
from pathlib import Path
import pandas as pd
from transformers import pipeline

DATA = Path(__file__).resolve().parents[1] / "data"
CORPUS = DATA / "corpus.csv"
SUMS = DATA / "summaries.csv"


def main():
    df = pd.read_csv(CORPUS)
    summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

    outs = []
    for t in df["text"].fillna(""):
        chunk = t[:1500]
        try:
            s = summarizer(chunk, max_length=120, min_length=40, do_sample=False)[0]["summary_text"]
        except Exception:
            s = ""
        outs.append(s)

    pd.DataFrame({"summary": outs}).to_csv(SUMS, index=False)
    print(f"Saved {len(outs)} summaries to {SUMS}")


if __name__ == "__main__":
    main()
