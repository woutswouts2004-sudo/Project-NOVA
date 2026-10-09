"""Command-line entry point: no network model by default."""
import argparse
import json
import os
import time
from pathlib import Path
from .agent import Agent
from .conversation import interactive_chat, converse
from .broker import Broker
from .llm import Model
from .memory import Journal
from .portable import export_archive, restore_archive

def main():
    parser = argparse.ArgumentParser(description="Project NOVA")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true", help="Run one agent step (default)")
    mode.add_argument("--loop", action="store_true", help="Repeat until stopped")
    mode.add_argument("--status", action="store_true", help="Show journal status")
    mode.add_argument("--chat", action="store_true", help="Local interactive chat")
    mode.add_argument("--ask", metavar="MESSAGE", help="Single chat message, then exit")
    mode.add_argument("--export-backup", metavar="FILE", help="Export a portable journal archive")
    mode.add_argument("--restore-backup", metavar="FILE", help="Restore into an empty journal")
    parser.add_argument("--interval", type=int, default=3600, help="Seconds between loop steps")
    args = parser.parse_args()
    root = Path(os.getenv("NOVA_HOME", ".")).resolve()
    journal = Journal(root / "data" / "nova.sqlite3")
    if args.status:
        print(json.dumps(journal.status(), indent=2))
        return
    if args.export_backup:
        print(json.dumps(export_archive(journal, args.export_backup), indent=2))
        return
    if args.restore_backup:
        print(json.dumps(restore_archive(journal, args.restore_backup), indent=2))
        return
    model = Model.from_environment()
    if args.chat:
        interactive_chat(journal, model)
        return
    if args.ask is not None:
        print(json.dumps(converse(journal, model, args.ask), indent=2))
        return
    agent = Agent(journal, model, Broker(root))
    if args.loop:
        if args.interval < 60:
            parser.error("--interval must be >= 60")
        while True:
            print(json.dumps(agent.step(), indent=2))
            time.sleep(args.interval)
    else:
        print(json.dumps(agent.step(), indent=2))

if __name__ == "__main__":
    main()
