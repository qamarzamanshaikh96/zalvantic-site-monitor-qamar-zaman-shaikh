from monitor.uptime import check_uptime
from monitor.ssl_check import check_ssl_expiry

def main():
    # Test karne ke liye kuch websites ki list
    test_sites = [
        "https://google.com",
        "https://github.com",
        "https://python.org"
    ]

    print("=== Zalvantic Website Care Monitor - Week 1 ===\n")

    for site in test_sites:
        print(f"Checking: {site}")
        
        # Uptime check
        uptime_result = check_uptime(site)
        print(f"  - Status Code : {uptime_result.get('status_code')}")
        print(f"  - Latency     : {uptime_result.get('latency_seconds')} seconds")
        
        # SSL check (hostname nikal kar)
        hostname = site.replace("https://", "").replace("http://", "").split("/")[0]
        ssl_result = check_ssl_expiry(hostname)
        print(f"  - SSL Days Left: {ssl_result.get('ssl_days_left')}")
        print("-" * 40)

if __name__ == "__main__":
    main()