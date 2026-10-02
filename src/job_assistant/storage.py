"""SQLite storage for jobs, applications, and interviews."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .config import DATA_DIR

DB_PATH = DATA_DIR / "jobs.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    salary TEXT,
    description TEXT,
    url TEXT,
    source TEXT,
    eligible INTEGER,
    score REAL,
    summary TEXT,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT REFERENCES jobs(id),
    status TEXT DEFAULT 'saved',
    resume_path TEXT,
    cover_letter_path TEXT,
    applied_at TIMESTAMP,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER REFERENCES applications(id),
    scheduled_at TIMESTAMP,
    kind TEXT,
    link TEXT,
    notes TEXT
);
"""


def get_conn() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn
