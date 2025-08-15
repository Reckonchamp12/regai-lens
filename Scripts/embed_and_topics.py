#!/usr/bin/env python
from pathlib import Path
import pandas as pd
from tqdm import tqdm
from src.regailens.viz import build_embeddings, build_umap_hdbscan

# Paths
DATA = Path(__file__).resolve().parents[1] / "data"
CORPUS = DATA / "corpus.csv"
EMBEDS = DATA / "embeds.parquet"

def main():
    if not CORPUS.exists():
        print(f"Corpus file not found at {CORPUS}. Skipping embedding step.")
        return

    # Load corpus
    df = pd.read_csv(CORPUS)
    if df.empty:
        print(f"Corpus is empty. No embeddings to build.")
        return

    # Build embeddings
    embeddings = build_embeddings(df["text"].tolist())

    # Apply UMAP + HDBSCAN clustering
    topics_df = build_umap_hdbscan(embeddings)
    
    # Save embeddings and topics
    df["embedding"] = list(embeddings)
    df["topic"] = topics_df["topic"]
    df.to_parquet(EMBEDS, index=False)
    print(f"Saved embeddings + topics to {EMBEDS}")

if __name__ == "__main__":
    main()

