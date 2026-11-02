import ssl
import socket
from datetime import datetime

def check_ssl_expiry(hostname: str):
    port = 443
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, port), timeout=10.0) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Expiry date extract karna
                not_after = cert.get('notAfter')
                expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                
                # Baqi din calculate karna
                days_left = (expiry_date - datetime.utcnow()).days
                return {
                    "hostname": hostname,
                    "ssl_days_left": days_left,
                    "is_valid": True
                }
    except Exception as e:
        return {
            "hostname": hostname,
            "ssl_days_left": None,
            "is_valid": False,
            "error": str(e)
        }