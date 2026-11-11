import time
import schedule
from monitor.uptime import check_website
from monitor.ssl_check import check_ssl
from database import init_db, save_uptime_result, save_ssl_result
from urllib.parse import urlparse

# Websites ki list jo monitor karni hain
WEBSITES = [
    "https://google.com",
    "https://github.com",
    "https://python.org"
]

def run_checks():
    print("\n--- Running Scheduled Site & SSL Checks ---")
    
    for url in WEBSITES:
        # 1. Uptime Check
        uptime_res = check_website(url)
        save_uptime_result(uptime_res)
        print(f"[Uptime] {url} -> Status: {uptime_res['status_code']}, Latency: {uptime_res['latency_ms']}ms")
        
        # 2. SSL Check
        domain = urlparse(url).netloc
        ssl_res = check_ssl(domain)
        save_ssl_result(ssl_res)
        print(f"[SSL] {domain} -> Valid: {ssl_res['ssl_valid']}, Days Left: {ssl_res['days_remaining']}")
    
    print("--- Checks Completed & Saved to DB ---")

if __name__ == "__main__":
    # Database initialize karein
    init_db()
    
    # Har 1 minute baad run karne ke liye schedule set karein
    # (Aap chahein toh .every(1).minutes ki jagah .every(10).seconds bhi kar sakte hain testing ke liye)
    schedule.every(1).minutes.do(run_checks)
    
    print("🚀 Website Monitor Scheduler Started! Press Ctrl+C to stop.")
    
    # Ek dafa foran start hote hi run kar dein
    run_checks()
    
    # Infinite loop jo background mein scheduler ko chalaye rakhegi
    while True:
        schedule.run_pending()
        time.sleep(1)