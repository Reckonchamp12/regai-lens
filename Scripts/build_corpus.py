#!/usr/bin/env python
from pathlib import Path
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from src.regailens.viz import build_embeddings, build_umap_hdbscan

DATA = Path(__file__).resolve().parents[1] / "data"
CORPUS = DATA / "corpus.csv"
EMBEDS = DATA / "embeds.parquet"


def main():
    df = pd.read_csv(CORPUS)
    texts = df["text"].fillna("").tolist()

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    em = build_embeddings(model, texts)

    x2, labels = build_umap_hdbscan(em, min_cluster_size=6)
    df["umap_x"] = x2[:,0]
    df["umap_y"] = x2[:,1]
    df["cluster"] = labels

    # store embeddings separately to keep CSV light
    out = df.copy()
    out["embedding"] = [e.astype(np.float32).tolist() for e in em]
    out.to_parquet(EMBEDS, index=False)
    print(f"Saved embeddings + UMAP to {EMBEDS}")


if __name__ == "__main__":
    main()
