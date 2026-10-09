"""Finite independent project steps using journal, model, and workspace broker."""
import argparse
import json
import os
from pathlib import Path
from .agent import Agent
from .broker import Broker
from .memory import Journal
from .llm import Model
from .local_model import LocalModel

def select_model():
    checkpoint = os.getenv("NOVA_OWN_CHECKPOINT", "").strip()
    if checkpoint:
        from .own_model import OwnModel
        return OwnModel(checkpoint)
    local = os.getenv("NOVA_LOCAL_MODEL", "").strip()
    return LocalModel(local) if local else Model.from_environment()

def run_steps(journal, model, broker, steps=1):
    if not isinstance(steps, int) or not 1 <= steps <= 20:
        raise ValueError("Budget must be 1 to 20 steps")
    agent = Agent(journal, model, broker)
    results = []
    for _ in range(steps):
        result = agent.step()
        results.append(result)
        if "error" in result:
            break
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", default=os.getenv("NOVA_HOME", "./nova_runtime"))
    parser.add_argument("--steps", type=int, default=1)
    args = parser.parse_args()
    home = Path(args.home).resolve()
    home.mkdir(parents=True, exist_ok=True)
    journal = Journal(home / "journal.sqlite3")
    broker = Broker(home)
    print(json.dumps(run_steps(journal, select_model(), broker, steps=args.steps), indent=2))

if __name__ == "__main__":
    main()
