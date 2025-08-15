from bs4 import BeautifulSoup
from .io_utils import safe_get, save_doc


def extract_links_from_listing(html: bytes, base_url: str):
    soup = BeautifulSoup(html, "html.parser")
    # Heuristic: get article/report links
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if any(x in href.lower() for x in ["pdf", "report", "paper", "blog", "speech", "article", "publication"]):
            if href.startswith("http"):
                links.append(href)
            elif href.startswith("/"):
                root = base_url.split("//", 1)[0] + "//" + base_url.split("//", 1)[1].split("/", 1)[0]
                links.append(root + href)
    return list(dict.fromkeys(links))


def fetch_and_cache(url: str):
    status, content, ctype = safe_get(url)
    if status == 200 and content:
        path = save_doc(url, content)
        return status, content, ctype, path
    return status, b"", ctype, None
