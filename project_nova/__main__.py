"""Command-line entry point."""
import argparse
import json
import os
import time
from pathlib import Path
from .agent import Agent
from .broker import Broker
from .llm import Model
from .memory import Journal

def main():
    parser = argparse.ArgumentParser(description="Project NOVA")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true", help="Run one agent step (default)")
    mode.add_argument("--loop", action="store_true", help="Repeat until stopped")
    mode.add_argument("--status", action="store_true", help="Show journal status")
    parser.add_argument("--interval", type=int, default=3600, help="Seconds between loop steps")
    args = parser.parse_args()
    root = Path(os.getenv("NOVA_HOME", ".")).resolve()
    journal = Journal(root / "data" / "nova.sqlite3")
    if args.status:
        print(json.dumps(journal.status(), indent=2))
        return
    agent = Agent(journal, Model.from_environment(), Broker(root))
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
