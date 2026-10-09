"""Portable journal: SQLite with simple JSON export."""
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

class Journal:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._db() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                at TEXT NOT NULL, kind TEXT NOT NULL, content TEXT NOT NULL
            )""")

    def _db(self):
        return sqlite3.connect(self.path)

    def add(self, kind, content):
        if kind not in {"observation", "reflection", "goal", "action", "error"}:
            raise ValueError("invalid journal event kind")
        with self._db() as db:
            db.execute("INSERT INTO events (at,kind,content) VALUES (?,?,?)",
                       (datetime.now(timezone.utc).isoformat(), kind, str(content)))

    def recent(self, limit=12):
        with self._db() as db:
            rows = db.execute("SELECT at,kind,content FROM events ORDER BY id DESC LIMIT ?",
                              (min(max(int(limit), 1), 100),)).fetchall()
        return [dict(zip(("at", "kind", "content"), row)) for row in reversed(rows)]

    def status(self):
        with self._db() as db:
            total = db.execute("SELECT count(*) FROM events").fetchone()[0]
        return {"events": total, "database": str(self.path), "recent": self.recent(5)}

    def export(self):
        with self._db() as db:
            rows = db.execute("SELECT at,kind,content FROM events ORDER BY id").fetchall()
        return json.dumps([dict(zip(("at", "kind", "content"), r)) for r in rows], indent=2)
