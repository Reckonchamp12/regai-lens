import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
CORPUS = DATA / "corpus.csv"
EMBEDS = DATA / "embeds.parquet"
LABELS = DATA / "labels.csv"
SUMS = DATA / "summaries.csv"

st.set_page_config(page_title="RegAI‑Lens", layout="wide")
st.title("RegAI‑Lens: Multilingual AI Policy Analytics for Financial Regulators")

if not CORPUS.exists():
    st.error("Corpus not found. Run: python scripts/build_corpus.py")
    st.stop()

@st.cache_data
def load_data():
    df_c = pd.read_csv(CORPUS)
    if EMBEDS.exists():
        df_e = pd.read_parquet(EMBEDS)
    else:
        df_e = None
    if LABELS.exists():
        df_l = pd.read_csv(LABELS)
    else:
        df_l = None
    if SUMS.exists():
        df_s = pd.read_csv(SUMS)
    else:
        df_s = None
    return df_c, df_e, df_l, df_s


df_c, df_e, df_l, df_s = load_data()

# Merge
df = df_e if df_e is not None else df_c.copy()
for col in ["use_cases", "adoption_stage"]:
    if df_l is not None and col in df_l.columns:
        df[col] = df_l[col]
if df_s is not None and "summary" in df_s.columns:
    df["summary"] = df_s["summary"]

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    countries = sorted(df["country"].dropna().unique().tolist())
    sel_countries = st.multiselect("Country", countries)

    auths = sorted(df["authority"].dropna().unique().tolist())
    sel_auth = st.multiselect("Authority", auths)

    usecases = sorted({u for s in df.get("use_cases", pd.Series()).fillna("") for u in str(s).split("|") if u})
    sel_use = st.multiselect("Use‑cases", usecases)

    stages = sorted(df.get("adoption_stage", pd.Series()).fillna("").unique().tolist())
    sel_stage = st.multiselect("Stage", [s for s in stages if s])

    q = st.text_input("Semantic search (keywords)", "risk model supervision")

# Filter
Q = df.copy()
if sel_countries:
    Q = Q[Q["country"].isin(sel_countries)]
if sel_auth:
    Q = Q[Q["authority"].isin(sel_auth)]
if sel_use:
    Q = Q[Q["use_cases"].apply(lambda s: any(u in str(s) for u in sel_use))]
if sel_stage:
    Q = Q[Q["adoption_stage"].isin(sel_stage)]

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Documents", len(Q))
c2.metric("Authorities", Q["authority"].nunique())
c3.metric("Countries", Q["country"].nunique())
c4.metric("Clusters", Q.get("cluster", pd.Series([-1])).nunique())

# UMAP scatter
if {"umap_x", "umap_y"}.issubset(Q.columns):
    st.subheader("Document landscape (UMAP)")
    color_col = "use_cases" if "use_cases" in Q.columns else "cluster"
    fig = px.scatter(
        Q, x="umap_x", y="umap_y", hover_data=["authority", "country"], color=color_col,
        title="UMAP projection of documents"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Run embeddings/topics to see the UMAP scatter: python scripts/embed_and_topics.py")

# Semantic search (cosine in embedding space if available, else text contains)
st.subheader("Search & Browse")
if q and "embedding" in Q.columns:
    import numpy as np
    from numpy.linalg import norm
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    qv = model.encode([q], normalize_embeddings=True)[0]

    def cos(a, b):
        return float(np.dot(a, b) / (norm(a) * norm(b) + 1e-9))

    sims = [cos(qv, np.array(e)) for e in Q["embedding"].tolist()]
    Q = Q.assign(score=sims).sort_values("score", ascending=False)
elif q:
    Q = Q[Q["text"].str.contains(q, case=False, na=False)]

# Table + inspector
st.dataframe(Q[["country", "authority", "use_cases", "adoption_stage", "cluster", "url"]].fillna(""), use_container_width=True, hide_index=True)

st.subheader("Document Inspector")
idx = st.number_input("Row index", min_value=0, max_value=max(0, len(Q)-1), value=0)
if len(Q):
    row = Q.iloc[int(idx)]
    st.markdown(f"**Authority:** {row.get('authority','')}  ")
    st.markdown(f"**Country:** {row.get('country','')}  ")
    st.markdown(f"**URL:** [{row.get('url','')}]({row.get('url','')})  ")
    if "summary" in row and isinstance(row["summary"], str) and row["summary"].strip():
        st.markdown("**Summary**")
        st.write(row["summary"])
    with st.expander("Full text"):
        st.write(row.get("text", "")[:5000])

st.caption("Zero‑shot labels and summaries are optional; the core clustering + search work without them.")
