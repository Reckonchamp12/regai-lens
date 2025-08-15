import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import umap
import hdbscan


def build_embeddings(model, texts: list[str]) -> np.ndarray:
    return model.encode(texts, normalize_embeddings=True, batch_size=32, show_progress_bar=True)


def build_umap_hdbscan(embeds: np.ndarray, min_cluster_size: int = 5):
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric="cosine", random_state=42)
    X2 = reducer.fit_transform(embeds)
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric='euclidean')
    labels = clusterer.fit_predict(X2)
    return X2, labels
