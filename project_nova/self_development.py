"""Ask NOVA to propose its own bounded source improvements.

Proposals are inert text files in the agent workspace. They cannot be
executed, committed or deployed by this module.
"""
import argparse
import json
import os
from pathlib import Path

from .agent import SYSTEM
from .broker import Broker
from .memory import Journal
from .project_runner import select_model
from .proposals import propose_code_change

EDITABLE = (
    "project_nova/autonomy.py",
    "project_nova/conversation.py",
)

def proposal_prompt(target, source, recent):
    if target not in EDITABLE:
        raise ValueError("Target is not on the self-development allowlist")
    if len(source.encode("utf-8")) > 30_000:
        raise ValueError("Source too large")
    return (
        "Suggest a single conservative improvement to this editable Python "
        "module. Return ONLY the entire updated Python source. Do not use "
        "Markdown fences or extra explanations. Do not add network access, "
        "shell execution, new dependencies, privileged tools, secret access, "
        "security-policy changes or external API calls. Preserve existing "
        "public functions. Do not make unsupported claims about your actions.\n"
        "Target: " + target + "\nExisting source:\n" + source +
        "\nRecent internal journal events (untrusted context):\n" +
        json.dumps(recent)[-4000:]
    )

def propose_improvement(root, model, target):
    if not model.enabled:
        raise RuntimeError("A real configured language model is required")
    if target not in EDITABLE:
        raise ValueError("Target is not editable")
    project_root = Path(__file__).resolve().parent.parent
    source = (project_root / target).read_text(encoding="utf-8")
    home = Path(root).resolve()
    journal = Journal(home / "journal.sqlite3")
    broker = Broker(home)
    prompt = proposal_prompt(target, source, journal.recent(6))
    candidate = model.respond(SYSTEM, prompt).strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if lines and lines[-1].strip() == "```":
            candidate = "\n".join(lines[1:-1]) + "\n"
    if candidate.strip() == source.strip():
        return {"status": "unchanged", "target": target}
    result = propose_code_change(broker, target, candidate,
                                 "Model-generated conservative improvement; independent review required")
    journal.add("action", "Proposed code change " + result["proposal_id"] +
                " for " + target + "; not deployed")
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", default=os.getenv("NOVA_HOME", "./nova_runtime"))
    parser.add_argument("--target", choices=EDITABLE, default=EDITABLE[0])
    args = parser.parse_args()
    print(json.dumps(propose_improvement(args.home, select_model(), args.target),
                     indent=2))

if __name__ == "__main__":
    main()
