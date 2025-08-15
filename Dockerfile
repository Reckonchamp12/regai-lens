FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8501
CMD ["bash", "-lc", "python scripts/build_corpus.py && python scripts/embed_and_topics.py && streamlit run app/streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]

# =========================
# File: README_addendum.md
# =========================
## CI & Docker quick-start

### GitHub Actions (CI)
This repo includes `.github/workflows/build.yml` which:
- Runs on push and weekly (Mon 02:00 UTC)
- Scrapes sources, rebuilds embeddings/topics
- Runs zero-shot & summaries on the scheduled run
- Uploads `data/` artifacts

To enable the status badge, replace `YourUsername/YourRepoName` in the README with your repo path.

### Docker
```bash
docker build -t regai-lens .
docker run -p 8501:8501 regai-lens
```
Open http://localhost:8501 to use the app.
