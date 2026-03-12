#!/usr/bin/env python3
"""
Persistent SQLite-backed task store for Villager AI.

Replaces the in-memory dict so tasks survive restarts and Hexclaw
can query task history across sessions.
"""

import sqlite3
import time
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

# ──────────────────────────────────────────────────────────────────────────────
# Storage location — override with env vars
# ──────────────────────────────────────────────────────────────────────────────
WORKSPACE = os.getenv("VILLAGER_WORKSPACE", "/tmp/villager_workspace")
DB_PATH   = os.getenv("VILLAGER_DB", str(Path(WORKSPACE) / "tasks.db"))

_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS tasks (
    task_id      TEXT    PRIMARY KEY,
    status       TEXT    NOT NULL DEFAULT 'pending',
    abstract     TEXT,
    description  TEXT,
    verification TEXT,
    result       TEXT,
    error        TEXT,
    source       TEXT    DEFAULT 'unknown',
    callback_url TEXT,
    created_at   REAL,
    updated_at   REAL
)
"""

_ALLOWED_COLUMNS = {
    "status", "abstract", "description", "verification",
    "result", "error", "source", "callback_url", "created_at", "updated_at",
}


# ──────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ──────────────────────────────────────────────────────────────────────────────

def _connect() -> sqlite3.Connection:
    """Return a thread-safe connection with row_factory set."""
    Path(WORKSPACE).mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the tasks table if it doesn't exist. Call once on startup."""
    with _connect() as conn:
        conn.execute(_CREATE_TABLE_SQL)
        conn.commit()


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def upsert_task(task_id: str, **kwargs) -> None:
    """
    Insert a new task or update fields on an existing one.

    Examples
    --------
    upsert_task("abc-123", status="pending", abstract="Scan 10.0.0.1")
    upsert_task("abc-123", status="completed", result="3 open ports found")
    """
    # Drop any key that isn't a real column to avoid SQL errors
    safe = {k: v for k, v in kwargs.items() if k in _ALLOWED_COLUMNS}
    now = time.time()

    with _connect() as conn:
        existing = conn.execute(
            "SELECT task_id FROM tasks WHERE task_id = ?", (task_id,)
        ).fetchone()

        if existing:
            safe["updated_at"] = now
            sets         = ", ".join(f"{k} = ?" for k in safe)
            vals         = list(safe.values()) + [task_id]
            conn.execute(f"UPDATE tasks SET {sets} WHERE task_id = ?", vals)
        else:
            safe.setdefault("created_at", now)
            safe["updated_at"] = now
            safe["task_id"]    = task_id
            cols         = ", ".join(safe.keys())
            placeholders = ", ".join("?" * len(safe))
            conn.execute(
                f"INSERT INTO tasks ({cols}) VALUES ({placeholders})",
                list(safe.values()),
            )
        conn.commit()


def get_task(task_id: str) -> Optional[Dict[str, Any]]:
    """Return a task dict by ID, or None if not found."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM tasks WHERE task_id = ?", (task_id,)
        ).fetchone()
        return dict(row) if row else None


def list_tasks(
    source: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 200,
) -> List[Dict[str, Any]]:
    """
    Return tasks ordered by creation time (newest first).

    Parameters
    ----------
    source : filter by caller ('hexclaw', 'cursor', ...)
    status : filter by state  ('pending', 'running', 'completed', 'failed')
    limit  : max rows returned
    """
    clauses: List[str] = []
    params: List[Any]  = []

    if source:
        clauses.append("source = ?")
        params.append(source)
    if status:
        clauses.append("status = ?")
        params.append(status)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    params.append(limit)

    with _connect() as conn:
        rows = conn.execute(
            f"SELECT * FROM tasks {where} ORDER BY created_at DESC LIMIT ?",
            params,
        ).fetchall()
        return [dict(r) for r in rows]


def delete_task(task_id: str) -> bool:
    """Delete a task record. Returns True if a row was removed."""
    with _connect() as conn:
        cur = conn.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
        conn.commit()
        return cur.rowcount > 0
