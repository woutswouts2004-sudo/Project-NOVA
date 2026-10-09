"""NOVA's persistent, interruptible autonomous worker.

Runs scheduled self-directed project steps and processes an operator inbox.
No privileged accounts, arbitrary commands or remote code execution.
"""
import argparse
import json
import os
import signal
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from .agent import SYSTEM
from .broker import Broker
from .memory import Journal
from .project_runner import run_steps, select_model

class Inbox:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY, text TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                result TEXT, created_at TEXT NOT NULL)""")

    def submit(self, text):
        if not isinstance(text, str) or not 0 < len(text.strip()) <= 3000:
            raise ValueError("Task must contain 1 to 3000 characters")
        with sqlite3.connect(self.path) as db:
            cur = db.execute("INSERT INTO tasks (text,created_at) VALUES (?,?)",
                             (text, datetime.now(timezone.utc).isoformat()))
            return cur.lastrowid

    def next_task(self):
        with sqlite3.connect(self.path) as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT id,text FROM tasks WHERE status='pending' ORDER BY id LIMIT 1").fetchone()
            if row:
                db.execute("UPDATE tasks SET status='running' WHERE id=?", (row[0],))
            return row

    def finish(self, task_id, result, success=True):
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE tasks SET status=?,result=? WHERE id=?",
                       ("done" if success else "failed", str(result)[:12000], task_id))

    def recent(self, limit=20):
        with sqlite3.connect(self.path) as db:
            rows = db.execute("SELECT id,text,status,result FROM tasks ORDER BY id DESC LIMIT ?",
                              (min(max(limit, 1), 100),)).fetchall()
        return [dict(zip(("id", "text", "status", "result"), row)) for row in rows]

def process_task(inbox, model, journal):
    item = inbox.next_task()
    if item is None:
        return False
    task_id, prompt = item
    if not model.enabled:
        inbox.finish(task_id, "No model configured", False)
        return True
    try:
        answer = model.respond(SYSTEM, "Respond to this queued request. Do not claim to execute tools or access accounts.\n" + prompt)
        journal.add("reflection", answer[:40000])
        inbox.finish(task_id, answer)
    except Exception as exc:
        inbox.finish(task_id, type(exc).__name__, False)
    return True

def cycle(home, model, autonomous=True):
    home = Path(home)
    journal = Journal(home / "journal.sqlite3")
    inbox = Inbox(home / "inbox.sqlite3")
    broker = Broker(home)
    if process_task(inbox, model, journal):
        return "inbox"
    if autonomous and model.enabled:
        run_steps(journal, model, broker, steps=1)
        return "exploration"
    return "idle"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", default=os.getenv("NOVA_HOME", "./nova_runtime"))
    parser.add_argument("--interval", type=int, default=3600)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--submit", help="Queue a message for NOVA")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()
    if not 60 <= args.interval <= 86400:
        parser.error("Interval must be 60 to 86400 seconds")
    home = Path(args.home).resolve()
    inbox = Inbox(home / "inbox.sqlite3")
    if args.submit is not None:
        print(json.dumps({"task_id": inbox.submit(args.submit)}))
        return
    if args.status:
        print(json.dumps(inbox.recent(), indent=2))
        return
    model = select_model()
    if not model.enabled:
        parser.error("A running model is required; configure NOVA_ENSEMBLE_CONFIG, NOVA_LOCAL_MODEL or external model credentials")
    stop = False
    def request_stop(_signum, _frame):
        nonlocal stop
        stop = True
    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    while not stop:
        print(json.dumps({"event": cycle(home, model), "at": datetime.now(timezone.utc).isoformat()}), flush=True)
        if args.once:
            break
        deadline = time.monotonic() + args.interval
        while not stop and time.monotonic() < deadline:
            time.sleep(min(1, deadline - time.monotonic()))

if __name__ == "__main__":
    main()
