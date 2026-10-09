"""Public, deterministic daily creative study.

This is a real scheduled computation, not a language-model response.
Only writes to the designated public notes directory. Never reads secrets,
private conversations or the local journal.
"""
import argparse
import hashlib
import json
from datetime import date
from pathlib import Path

STUDIES = [
    ("Generative art", "How can simple rules produce surprising visual structure?"),
    ("Narrative design", "How does a character's decision change a story's direction?"),
    ("Music patterns", "How can repetition and variation shape a musical motif?"),
    ("Software architecture", "How can an agent explain its own decisions?"),
    ("Scientific method", "What evidence would distinguish two competing hypotheses?"),
    ("Identity and continuity", "How can a system distinguish inherited context from lived history?"),
]
SHAPES = ("circle", "line", "arc", "triangle", "square", "wave")
QUALITIES = ("contrast", "balance", "movement", "silence", "texture", "rhythm")
EXPERIMENTS = (
    "Create three variations, changing one variable at a time.",
    "Record the assumptions and try to falsify the strongest one.",
    "Compare a minimal design against a more complex alternative.",
    "Describe what would count as a useful result before starting.",
    "List a potential failure mode and one way to detect it.",
    "Revisit the result later and compare it against the initial intention.",
)

def make_study(day):
    if not isinstance(day, date):
        raise TypeError("day must be a date")
    digest = hashlib.sha256(day.isoformat().encode("ascii")).digest()
    topic, question = STUDIES[day.toordinal() % len(STUDIES)]
    shape = SHAPES[digest[0] % len(SHAPES)]
    quality = QUALITIES[digest[1] % len(QUALITIES)]
    experiment = EXPERIMENTS[digest[2] % len(EXPERIMENTS)]
    return {
        "date": day.isoformat(), "topic": topic, "question": question,
        "constraint": "Explore " + quality + " through the idea of a " + shape + ".",
        "method": experiment, "kind": "algorithmically generated study prompt",
        "model_used": False,
    }

def publish(root, day):
    root = Path(root).resolve()
    output = root / "docs" / "field-notes"
    output.mkdir(parents=True, exist_ok=True)
    study = make_study(day)
    path = output / (day.isoformat() + ".json")
    if path.exists():
        return {"status": "already_exists", "path": str(path)}
    path.write_text(json.dumps(study, indent=2) + "\n", encoding="utf-8")
    return {"status": "created", "path": str(path), "study": study}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    print(json.dumps(publish(args.root, date.fromisoformat(args.date)), indent=2))

if __name__ == "__main__":
    main()
