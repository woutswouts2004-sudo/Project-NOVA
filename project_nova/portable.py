"""Portable, versioned journal archive.

Backups contain potentially sensitive reflections. They are not encrypted.
Do not commit exports or upload them to untrusted services.
"""
import hashlib
import json
from pathlib import Path

FORMAT = "project-nova-journal-v1"
MAX_ARCHIVE = 5_000_000

def export_archive(journal, destination):
    events = journal.all_events()
    payload = {"format": FORMAT, "events": events}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    archive = {"payload": payload, "sha256": hashlib.sha256(canonical).hexdigest()}
    serialized = json.dumps(archive, indent=2)
    if len(serialized.encode("utf-8")) > MAX_ARCHIVE:
        raise ValueError("Archive too large")
    destination = Path(destination)
    if destination.exists():
        raise FileExistsError("Refusing to overwrite an existing backup")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(serialized, encoding="utf-8")
    return {"path": str(destination), "events": len(events), "sha256": archive["sha256"]}

def restore_archive(journal, source):
    source = Path(source)
    if source.stat().st_size > MAX_ARCHIVE:
        raise ValueError("Archive too large")
    archive = json.loads(source.read_text(encoding="utf-8"))
    payload = archive["payload"]
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    if payload.get("format") != FORMAT or hashlib.sha256(canonical).hexdigest() != archive.get("sha256"):
        raise ValueError("Invalid archive format or checksum")
    events = payload["events"]
    if not isinstance(events, list) or len(events) > 50_000:
        raise ValueError("Invalid event list")
    for event in events:
        if (not isinstance(event, dict) or
            set(event) != {"at", "kind", "content"} or
            any(not isinstance(v, str) for v in event.values()) or
            event["kind"] not in {"observation", "reflection", "goal", "action", "error"} or
            len(event["content"]) > 100_000):
            raise ValueError("Invalid event")
    journal.import_events(events)
    return {"restored": len(events)}
