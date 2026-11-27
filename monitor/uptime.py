import httpx
import time

def check_website(url: str):
    start_time = time.time()
    try:
        response = httpx.get(url, timeout=10.0)
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        return {
            "url": url,
            "status_code": response.status_code,
            "latency_ms": latency,
            "is_online": response.status_code == 200
        }
    except Exception as e:
        return {
            "url": url,
            "status_code": None,
            "latency_ms": None,
            "is_online": False,
            "error": str(e)
        }