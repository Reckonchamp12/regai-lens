from pathlib import Path
import yaml
import requests

DATA = Path(__file__).resolve().parents[2] / "data"
DOCS = DATA / "docs"
DOCS.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}


def read_sources():
    with open(DATA / "sources.yaml", "r", encoding="utf-8") as f:
        y = yaml.safe_load(f)
    return y.get("sources", [])


def safe_get(url: str, timeout: int = 25):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        return r.status_code, r.content, r.headers.get("content-type", "")
    except Exception:
        return 0, b"", ""


def save_doc(url: str, content: bytes) -> Path:
    name = url.split("/")[-1] or "index.html"
    path = DOCS / name
    path.write_bytes(content)
    return path
