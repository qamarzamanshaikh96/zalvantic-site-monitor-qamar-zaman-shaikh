import sqlite3

DB_NAME = "monitor.db"

def init_db():
    """Database aur tables create karta hai agar pehle se na bane hon."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Uptime Logs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS uptime_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                status_code INTEGER,
                latency_ms REAL,
                is_online BOOLEAN,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # SSL Logs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ssl_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hostname TEXT NOT NULL,
                ssl_valid BOOLEAN,
                days_remaining INTEGER,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def save_uptime_result(result: dict):
    """Uptime check ka result database mein store karta hai."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO uptime_logs (url, status_code, latency_ms, is_online)
            VALUES (?, ?, ?, ?)
        ''', (result["url"], result["status_code"], result["latency_ms"], result["is_online"]))
        conn.commit()

def save_ssl_result(result: dict):
    """SSL check ka result database mein store karta hai."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ssl_logs (hostname, ssl_valid, days_remaining)
            VALUES (?, ?, ?)
        ''', (result["hostname"], result["ssl_valid"], result["days_remaining"]))
        conn.commit()