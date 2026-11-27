import socket
import ssl
from datetime import datetime

def check_ssl(hostname: str):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Expiry date extract karna
                expire_date_str = cert['notAfter']
                expire_date = datetime.strptime(expire_date_str, "%b %d %H:%M:%S %Y %Z")
                days_left = (expire_date - datetime.utcnow()).days
                
                return {
                    "hostname": hostname,
                    "ssl_valid": True,
                    "days_remaining": days_left
                }
    except Exception as e:
        return {
            "hostname": hostname,
            "ssl_valid": False,
            "days_remaining": 0,
            "error": str(e)
        }