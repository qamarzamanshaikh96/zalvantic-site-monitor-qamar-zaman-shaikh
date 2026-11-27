from urllib.parse import urljoin
import httpx
from bs4 import BeautifulSoup


def check_seo_basics(url: str) -> dict:
    """Website ke basic on-page aur technical SEO elements check karta hai."""
    result = {
        "url": url,
        "title": None,
        "title_length": 0,
        "has_meta_description": False,
        "meta_description_length": 0,
        "h1_count": 0,
        "images_total": 0,
        "images_missing_alt": 0,
        "has_robots_txt": False,
        "has_sitemap_xml": False,
        "error": None,
    }

    headers = {"User-Agent": "ZalvanticSiteMonitor/1.0"}

    try:
        with httpx.Client(timeout=10.0, follow_redirects=True, headers=headers) as client:
            response = client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # 1. Title Tag Check
            if soup.title and soup.title.string:
                title_text = soup.title.string.strip()
                result["title"] = title_text
                result["title_length"] = len(title_text)

            # 2. Meta Description Check
            meta_desc = soup.find("meta", attrs={"name": lambda v: v and v.lower() == "description"})
            if meta_desc and meta_desc.get("content"):
                desc_text = meta_desc["content"].strip()
                if desc_text:
                    result["has_meta_description"] = True
                    result["meta_description_length"] = len(desc_text)

            # 3. H1 Headings Count
            result["h1_count"] = len(soup.find_all("h1"))

            # 4. Images Missing Alt Attribute
            images = soup.find_all("img")
            result["images_total"] = len(images)
            missing_alt = sum(
                1 for img in images if not img.get("alt") or not img.get("alt").strip()
            )
            result["images_missing_alt"] = missing_alt

            # 5. robots.txt Check
            robots_url = urljoin(url, "/robots.txt")
            robots_res = client.get(robots_url)
            result["has_robots_txt"] = robots_res.status_code == 200

            # 6. sitemap.xml Check
            sitemap_url = urljoin(url, "/sitemap.xml")
            sitemap_res = client.get(sitemap_url)
            result["has_sitemap_xml"] = sitemap_res.status_code == 200

    except Exception as exc:
        result["error"] = str(exc)

    return result