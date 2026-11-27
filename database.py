import sqlite3

DB_NAME = "monitor.db"


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uptime_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                status_code INTEGER,
                latency_ms REAL,
                is_online BOOLEAN,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ssl_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hostname TEXT NOT NULL,
                ssl_valid BOOLEAN,
                days_remaining INTEGER,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS broken_link_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_url TEXT NOT NULL,
                broken_url TEXT NOT NULL,
                status_code INTEGER,
                error TEXT,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seo_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                title TEXT,
                title_length INTEGER,
                has_meta_description BOOLEAN,
                meta_description_length INTEGER,
                h1_count INTEGER,
                images_total INTEGER,
                images_missing_alt INTEGER,
                has_robots_txt BOOLEAN,
                has_sitemap_xml BOOLEAN,
                error TEXT,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()


def save_uptime_result(result: dict):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO uptime_logs (url, status_code, latency_ms, is_online)
            VALUES (?, ?, ?, ?)
        """, (result["url"], result["status_code"], result["latency_ms"], result["is_online"]))
        conn.commit()


def save_ssl_result(result: dict):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ssl_logs (hostname, ssl_valid, days_remaining)
            VALUES (?, ?, ?)
        """, (result["hostname"], result["ssl_valid"], result["days_remaining"]))
        conn.commit()


def save_broken_link_result(item: dict):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO broken_link_logs (source_url, broken_url, status_code, error)
            VALUES (?, ?, ?, ?)
        """, (
            item.get("source_url"),
            item.get("broken_url"),
            item.get("status_code"),
            item.get("error"),
        ))
        conn.commit()


def save_seo_result(result: dict):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO seo_logs (
                url, title, title_length, has_meta_description,
                meta_description_length, h1_count, images_total,
                images_missing_alt, has_robots_txt, has_sitemap_xml, error
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result.get("url"),
            result.get("title"),
            result.get("title_length"),
            result.get("has_meta_description"),
            result.get("meta_description_length"),
            result.get("h1_count"),
            result.get("images_total"),
            result.get("images_missing_alt"),
            result.get("has_robots_txt"),
            result.get("has_sitemap_xml"),
            result.get("error"),
        ))
        conn.commit()