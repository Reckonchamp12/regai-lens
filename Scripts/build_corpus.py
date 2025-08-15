#!/usr/bin/env python
from pathlib import Path
import pandas as pd
from datetime import datetime
from tqdm import tqdm

from src.regailens.io_utils import read_sources
from src.regailens.scrape import fetch_and_cache, extract_links_from_listing
from src.regailens.textprep import html_to_text, normalize_text
from src.regailens.parse_pdf import pdf_to_text

# Ensure data folder exists
DATA = Path(__file__).resolve().parents[1] / "data"
DATA.mkdir(exist_ok=True)
OUT = DATA / "corpus.csv"

def main():
    rows = []
    sources = read_sources()

    for entry in tqdm(sources, desc="Authorities"):
        country = entry["country"]
        authority = entry["authority"]
        for url in entry.get("urls", []):
            status, content, ctype, path = fetch_and_cache(url)
            if status != 200 or not content:
                continue

            if "html" in ctype or url.endswith(("/", ".html", ".htm")):
                text = html_to_text(content)
                rows.append({
                    "country": country,
                    "authority": authority,
                    "url": url,
                    "source_type": "html",
                    "fetched_path": str(path) if path else "",
                    "text": normalize_text(text),
                    "fetched_at": datetime.utcnow().isoformat(),
                })
                for link in extract_links_from_listing(content, url)[:20]:
                    s2, c2, ct2, p2 = fetch_and_cache(link)
                    if s2 != 200 or not c2:
                        continue
                    if "pdf" in ct2 or link.lower().endswith(".pdf"):
                        t2 = pdf_to_text(c2)
                        stype = "pdf"
                    else:
                        t2 = html_to_text(c2)
                        stype = "html"
                    rows.append({
                        "country": country,
                        "authority": authority,
                        "url": link,
                        "source_type": stype,
                        "fetched_path": str(p2) if p2 else "",
                        "text": normalize_text(t2),
                        "fetched_at": datetime.utcnow().isoformat(),
                    })
            else:
                if "pdf" in ctype or url.lower().endswith(".pdf"):
                    text = pdf_to_text(content)
                    stype = "pdf"
                else:
                    text = html_to_text(content)
                    stype = "html"
                rows.append({
                    "country": country,
                    "authority": authority,
                    "url": url,
                    "source_type": stype,
                    "fetched_path": str(path) if path else "",
                    "text": normalize_text(text),
                    "fetched_at": datetime.utcnow().isoformat(),
                })

    df = pd.DataFrame(rows)
    df = df[df["text"].str.len() > 200].reset_index(drop=True)
    df.to_csv(OUT, index=False)
    print(f"Saved {len(df)} documents to {OUT}")

if __name__ == "__main__":
    main()

