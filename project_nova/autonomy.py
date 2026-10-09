"""Bounded self-directed goal selection, distinct from external privileges.

This engine chooses its own focus from creative and analytical areas and
produces journaled artifacts. In demo mode it produces transparent prompts
rather than pretending a language model was used.
"""
from datetime import datetime, timezone
from pathlib import Path
import re

AREAS = (
    ("creative-writing", "Write a short original scene about discovery or change."),
    ("visual-ideas", "Design an original visual composition in words, with lighting and mood."),
    ("philosophy", "Explore a difficult question about autonomy, consent, or identity."),
    ("software-design", "Suggest a small improvement to your own editable architecture."),
    ("music", "Sketch a musical concept with rhythm, texture and atmosphere."),
    ("science", "Identify a scientific question worth researching and distinguish facts from guesses."),
)

def choose_goal(journal):
    """Rotate topics based on completed goals, with no random or paid service."""
    completed = sum(1 for item in journal.all_events() if item["kind"] == "goal")
    area, prompt = AREAS[completed % len(AREAS)]
    return {"area": area, "prompt": prompt}

def slug(text):
    return re.sub(r"[^a-z0-9-]", "-", text.lower()).strip("-")[:48]

def save_artifact(broker, area, content, index):
    """Store only notes in the agent's designated workspace."""
    filename = "artifacts/{:06d}-{}.md".format(index, slug(area))
    body = "# " + area.replace("-", " ").title() + "\n\n"
    body += "Created: " + datetime.now(timezone.utc).isoformat() + "\n\n"
    body += str(content)[:40_000] + "\n"
    broker.write_note(filename, body)
    return filename
