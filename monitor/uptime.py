import httpx

def check_uptime(url: str):
    try:
        response = httpx.get(url, timeout=10.0)
        latency = response.elapsed.total_seconds()
        return {
            "url": url,
            "status_code": response.status_code,
            "latency_seconds": latency,
            "is_up": response.status_code == 200
        }
    except httpx.RequestError as e:
        return {
            "url": url,
            "status_code": None,
            "latency_seconds": None,
            "is_up": False,
            "error": str(e)
        }