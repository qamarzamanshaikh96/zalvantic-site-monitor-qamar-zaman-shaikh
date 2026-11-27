import time
import schedule
from urllib.parse import urlparse
from monitor.uptime import check_website
from monitor.ssl_check import check_ssl
from monitor.crawler import find_broken_links
from monitor.seo_check import check_seo_basics
from database import (
    init_db,
    save_uptime_result,
    save_ssl_result,
    save_broken_link_result,
    save_seo_result,
)

WEBSITES = [
    "https://google.com",
    "https://github.com",
    "https://python.org",
]


def run_checks():
    print("\n--- Running Scheduled Site, SSL, Broken Link & SEO Checks ---")

    for url in WEBSITES:
        uptime_res = check_website(url)
        save_uptime_result(uptime_res)
        print(
            f"[Uptime] {url} -> Status: {uptime_res['status_code']}, Latency: {uptime_res['latency_ms']}ms"
        )

        domain = urlparse(url).netloc
        ssl_res = check_ssl(domain)
        save_ssl_result(ssl_res)
        print(
            f"[SSL] {domain} -> Valid: {ssl_res['ssl_valid']}, Days Left: {ssl_res['days_remaining']}"
        )

        broken_links = find_broken_links(url, max_links=15, delay_seconds=0.5)
        for item in broken_links:
            save_broken_link_result(item)
        print(f"[Broken Links] {url} -> Found: {len(broken_links)}")

        seo_res = check_seo_basics(url)
        save_seo_result(seo_res)
        print(
            f"[SEO] {url} -> Title Len: {seo_res['title_length']}, "
            f"Meta Desc: {seo_res['has_meta_description']}, "
            f"H1: {seo_res['h1_count']}, Missing Alt: {seo_res['images_missing_alt']}"
        )

    print("--- Checks Completed & Saved to DB ---")


if __name__ == "__main__":
    init_db()
    schedule.every(1).minutes.do(run_checks)
    print("🚀 Website Monitor Scheduler Started! Press Ctrl+C to stop.")
    run_checks()

    while True:
        schedule.run_pending()
        time.sleep(1)