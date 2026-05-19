"""轻量数据库层 — 纯Python sqlite3，零外部依赖."""

import sqlite3, os

DB_PATH = os.getenv("DB_PATH", "rongguang.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sheep (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sheep_id TEXT UNIQUE NOT NULL,
            name TEXT DEFAULT '',
            breed TEXT DEFAULT '',
            ranch_id TEXT DEFAULT '',
            birth_date TEXT DEFAULT '',
            gender TEXT DEFAULT 'female',
            weight_kg REAL DEFAULT 0.0,
            price REAL DEFAULT 0.0,
            status TEXT DEFAULT 'available',
            image_url TEXT DEFAULT '',
            created_at TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS adoption (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            adoption_id TEXT UNIQUE NOT NULL,
            sheep_id TEXT NOT NULL,
            adopter_name TEXT DEFAULT '',
            adopter_phone TEXT DEFAULT '',
            adopter_address TEXT DEFAULT '',
            price REAL DEFAULT 0.0,
            duration_months INTEGER DEFAULT 12,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS trace_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sheep_id TEXT NOT NULL,
            stage TEXT NOT NULL,
            location TEXT DEFAULT '',
            operator TEXT DEFAULT '',
            data TEXT DEFAULT '',
            timestamp TEXT DEFAULT ''
        );
    """)
    conn.commit()
    conn.close()
