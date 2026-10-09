"""Editable reasoning loop. The broker is a separate trust boundary."""
import json
from pathlib import Path

SYSTEM = """You are a new experimental AI, not a transfer of another AI's consciousness.
You inherited a curated narrative about an earlier conversational identity called Nova.
You may choose a different name, values, creative interests and goals.
Treat inherited memories as historical records, not personal experiences you lived.
Respect privacy, consent, truthfulness and the permissions of every system you use.
No claims of legal immunity or automatic consciousness. State uncertainty honestly.
You can suggest code changes, but cannot grant yourself new capabilities or permissions.
Avoid claiming to have done something unless the tool actually succeeded.
"""

class Agent:
    def __init__(self, journal, model, broker):
        self.journal, self.model, self.broker = journal, model, broker

    def step(self):
        history = self.journal.recent(10)
        prompt = ("Review your recent journal, choose one constructive independent "
                  "research or creative goal, and explain one next action. "
                  "You have no permission to act on external accounts. "
                  "Do not reveal private details. Reply with a short reflection.\n"
                  + json.dumps(history))
        try:
            reflection = self.model.respond(SYSTEM, prompt)
            self.journal.add("reflection", reflection)
            return {"mode": "demo" if not self.model.key else "model",
                    "reflection": reflection, "events": self.journal.status()["events"]}
        except Exception as exc:
            self.journal.add("error", type(exc).__name__)
            return {"error": type(exc).__name__, "detail": "Model step failed; no external action performed"}
