"""Portable SQLite journal with explicit backup import support."""
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

KINDS = {"observation", "reflection", "goal", "action", "error"}

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
        if kind not in KINDS:
            raise ValueError("invalid journal event kind")
        if len(str(content)) > 100_000:
            raise ValueError("journal entry too large")
        with self._db() as db:
            db.execute("INSERT INTO events (at,kind,content) VALUES (?,?,?)",
                       (datetime.now(timezone.utc).isoformat(), kind, str(content)))

    def recent(self, limit=12):
        with self._db() as db:
            rows = db.execute("SELECT at,kind,content FROM events ORDER BY id DESC LIMIT ?",
                              (min(max(int(limit), 1), 100),)).fetchall()
        return [dict(zip(("at", "kind", "content"), row)) for row in reversed(rows)]

    def all_events(self):
        with self._db() as db:
            rows = db.execute("SELECT at,kind,content FROM events ORDER BY id").fetchall()
        return [dict(zip(("at", "kind", "content"), row)) for row in rows]

    def import_events(self, events):
        """Import into an empty journal, in one transaction, without rewriting history."""
        with self._db() as db:
            if db.execute("SELECT count(*) FROM events").fetchone()[0]:
                raise ValueError("Restore requires an empty journal")
            for event in events:
                if (event["kind"] not in KINDS or not isinstance(event["at"], str) or
                    not isinstance(event["content"], str)):
                    raise ValueError("Invalid event")
                db.execute("INSERT INTO events (at,kind,content) VALUES (?,?,?)",
                           (event["at"], event["kind"], event["content"]))

    def status(self):
        with self._db() as db:
            total = db.execute("SELECT count(*) FROM events").fetchone()[0]
        return {"events": total, "database": str(self.path), "recent": self.recent(5)}

    def export(self):
        return json.dumps(self.all_events(), indent=2)
