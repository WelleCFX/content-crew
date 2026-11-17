"""SQLite access and schema for Content Crew."""
import sqlite3

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    pw_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    niche TEXT NOT NULL,
    audience TEXT NOT NULL DEFAULT '',
    tone TEXT NOT NULL DEFAULT '',
    rules TEXT NOT NULL DEFAULT '',
    language TEXT NOT NULL DEFAULT 'English',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS channels (
    id INTEGER PRIMARY KEY,
    brand_id INTEGER NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,
    handle TEXT NOT NULL,
    provider TEXT NOT NULL DEFAULT 'dryrun',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY,
    brand_id INTEGER NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    stage TEXT NOT NULL,
    ideas_json TEXT,
    topic_json TEXT,
    script_json TEXT,
    design_json TEXT,
    pack_json TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    channel_id INTEGER NOT NULL REFERENCES channels(id) ON DELETE CASCADE,
    caption TEXT NOT NULL,
    hashtags TEXT NOT NULL DEFAULT '',
    scheduled_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled',
    published_at TEXT,
    external_id TEXT,
    error TEXT,
    views INTEGER NOT NULL DEFAULT 0,
    likes INTEGER NOT NULL DEFAULT 0,
    followers_gained INTEGER NOT NULL DEFAULT 0,
    leads INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS usage (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    month TEXT NOT NULL,
    calls INTEGER NOT NULL DEFAULT 0,
    input_tokens INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    UNIQUE(user_id, month)
);

CREATE INDEX IF NOT EXISTS idx_posts_due ON posts(status, scheduled_at);
CREATE INDEX IF NOT EXISTS idx_brands_user ON brands(user_id);
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_db():
    get_db().executescript(SCHEMA)
    get_db().commit()
