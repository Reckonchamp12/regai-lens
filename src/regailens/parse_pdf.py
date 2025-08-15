from io import BytesIO
from pdfminer.high_level import extract_text


def pdf_to_text(content: bytes) -> str:
    try:
        txt = extract_text(BytesIO(content))
        return txt
    except Exception:
        return ""


# =========================
# File: src/regailens/textprep.py
# =========================
import re
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 42


def html_to_text(html: bytes) -> str:
    try:
        soup = BeautifulSoup(html, "html.parser")
        for t in soup(["script", "style", "noscript", "header", "footer", "nav", "form"]):
            t.decompose()
        text = soup.get_text(" ")
        text = re.sub(r"\s+", " ", text).strip()
        return text
    except Exception:
        return ""


def normalize_text(t: str) -> str:
    t = re.sub(r"\s+", " ", (t or "")).strip()
    return t


def detect_lang(t: str) -> str:
    try:
        return detect(t)
    except Exception:
        return "unknown"
