#!/usr/bin/env python
from pathlib import Path
import pandas as pd
from transformers import pipeline

DATA = Path(__file__).resolve().parents[1] / "data"
CORPUS = DATA / "corpus.csv"
LABELS = DATA / "labels.csv"

CANDIDATES_USE = [
    "Fraud/AML", "Market Supervision", "Risk & Stress Testing", "Consumer Protection",
    "RegTech/SupTech", "AI Governance/Principles", "Model Risk Management",
    "Data Privacy", "Cybersecurity"
]

CANDIDATES_STAGE = ["Policy", "Research", "Pilot", "In-Use"]


def main():
    df = pd.read_csv(CORPUS)
    clf = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")

    labels_use = []
    labels_stage = []

    for t in df["text"].fillna("").tolist():
        t_short = t[:2000]  # keep it bounded
        p1 = clf(t_short, CANDIDATES_USE, multi_label=True)
        top_use = [c for c, s in zip(p1["labels"], p1["scores"]) if s >= 0.35]
        if not top_use and p1["labels"]:
            top_use = [p1["labels"][0]]
        labels_use.append("|".join(top_use))

        p2 = clf(t_short, CANDIDATES_STAGE, multi_label=False)
        labels_stage.append(p2["labels"][0])

    pd.DataFrame({"use_cases": labels_use, "adoption_stage": labels_stage}).to_csv(LABELS, index=False)
    print(f"Saved labels to {LABELS}")


if __name__ == "__main__":
  main()
