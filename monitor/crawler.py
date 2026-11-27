import time
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup


def find_broken_links(start_url: str, max_links: int = 20, delay_seconds: float = 0.5):
    broken_links = []
    visited = set()

    try:
        headers = {"User-Agent": "ZalvanticSiteMonitor/1.0 (Polite Link Checker)"}
        response = httpx.get(start_url, timeout=10.0, follow_redirects=True, headers=headers)
        if response.status_code >= 400:
            return [{
                "source_url": start_url,
                "broken_url": start_url,
                "status_code": response.status_code,
                "error": "Starting page unreachable"
            }]

        soup = BeautifulSoup(response.text, "html.parser")
        base_domain = urlparse(start_url).netloc

        links_to_check = []
        for tag in soup.find_all("a", href=True):
            raw_href = tag["href"].strip()
            if not raw_href or raw_href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue

            full_url = urljoin(start_url, raw_href)
            parsed = urlparse(full_url)

            if parsed.scheme in ("http", "https") and parsed.netloc == base_domain:
                if full_url not in visited:
                    visited.add(full_url)
                    links_to_check.append(full_url)

            if len(links_to_check) >= max_links:
                break

        for link in links_to_check:
            try:
                res = httpx.get(link, timeout=8.0, follow_redirects=True, headers=headers)
                if res.status_code >= 400:
                    broken_links.append({
                        "source_url": start_url,
                        "broken_url": link,
                        "status_code": res.status_code,
                        "error": None
                    })
            except Exception as exc:
                broken_links.append({
                    "source_url": start_url,
                    "broken_url": link,
                    "status_code": None,
                    "error": str(exc)
                })
            time.sleep(delay_seconds)

    except Exception as exc:
        broken_links.append({
            "source_url": start_url,
            "broken_url": start_url,
            "status_code": None,
            "error": str(exc)
        })

    return broken_links