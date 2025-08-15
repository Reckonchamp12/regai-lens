***RegAI‑Lens — Multilingual AI Policy Analytics for Financial Regulators***

**What it is:** End‑to‑end ML pipeline + app that ingests **official** regulator pages and PDFs related to **AI**, then performs:

- **Scraping** of curated official sources (HTML, PDF)
- **Text normalization** + language detection
- **Sentence embeddings** (\*MiniLM, multilingual capable)
- **Unsupervised topic discovery** (UMAP + HDBSCAN) with interactive scatter
- **Multilingual zero‑shot classification** (XLM‑RoBERTa XNLI) into AI policy/use‑case labels
- **Semantic search** and similarity exploration
- **Auto‑summaries** (optional, light T5) per document

Deliverable: a beautiful **Streamlit** dashboard showing a UMAP map of documents, filters by regulator/country/use‑case/stage, search, and a right‑pane reader with key metadata, zero‑shot labels, and source link.

## Demo (local)
```bash
python -m venv .venv
. .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/build_corpus.py         # scrape + parse (HTML/PDF) ➜ data/corpus.csv
python scripts/embed_and_topics.py     # embeddings + UMAP + HDBSCAN ➜ data/embeds.parquet
python scripts/zero_shot_labels.py     # optional: multilingual zero‑shot labels ➜ data/labels.csv
python scripts/summarize.py            # optional: lightweight summaries ➜ data/summaries.csv
streamlit run app/streamlit_app.py
```

> **Note:** Zero‑shot and summarization download Hugging Face models on first run. If you prefer minimal footprint, skip those two scripts—the app still works (it will show clustering + search without labels/summaries).

## Deploy
- **Streamlit Cloud**: point entry to `app/streamlit_app.py` and set `PYTHON_VERSION=3.10`.
- For private runners: ensure outbound HTTPS allowed for model downloads (first run) or pre‑bake a Docker image.

## Repo Structure
```
regai-lens/
├─ app/
│  └─ streamlit_app.py
├─ data/
│  ├─ sources.yaml          # curated official URLs
│  ├─ seed/authorities.csv  # authorities list
│  ├─ corpus.csv            # built by build_corpus.py
│  ├─ embeds.parquet        # built by embed_and_topics.py
│  ├─ labels.csv            # built by zero_shot_labels.py (optional)
│  ├─ summaries.csv         # built by summarize.py (optional)
│  └─ docs/                 # downloaded PDFs (cached)
├─ scripts/
│  ├─ build_corpus.py
│  ├─ embed_and_topics.py
│  ├─ zero_shot_labels.py
│  └─ summarize.py
├─ src/regailens/
│  ├─ __init__.py
│  ├─ io_utils.py
│  ├─ scrape.py
│  ├─ parse_pdf.py
│  ├─ textprep.py
│  └─ viz.py
├─ requirements.txt
└─ LICENSE
```

## Labels (Zero‑Shot Candidates)
- **Use‑cases:** `Fraud/AML`, `Market Supervision`, `Risk & Stress Testing`, `Consumer Protection`, `RegTech/SupTech`, `AI Governance/Principles`, `Model Risk Management`, `Data Privacy`, `Cybersecurity`.
- **Stage:** `Policy`, `Research`, `Pilot`, `In‑Use`.

Extend lists in `zero_shot_labels.py`.

## Ethics & Licence
- Only official public documents are scraped.
- MIT License.
