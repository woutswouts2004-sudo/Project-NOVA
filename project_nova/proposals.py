"""Create self-edit proposals without granting permission to deploy them.

The AI may generate arbitrary candidate source as *data* inside workspace.
The protected deployment process is deliberately out of scope.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import PurePosixPath

ALLOWED_PREFIX = "project_nova/"
ALLOWED_SUFFIX = ".py"
MAX_SOURCE_BYTES = 100_000

def propose_code_change(broker, target, new_source, reason):
    if not isinstance(target, str) or not isinstance(new_source, str):
        raise ValueError("target and source must be strings")
    p = PurePosixPath(target)
    if (not target.startswith(ALLOWED_PREFIX) or p.is_absolute() or
            ".." in p.parts or p.suffix != ALLOWED_SUFFIX or
            p.name in {"broker.py", "tools.py", "proposals.py"}):
        raise ValueError("Target is not an editable agent module")
    if len(new_source.encode("utf-8")) > MAX_SOURCE_BYTES:
        raise ValueError("Candidate is too large")
    compile(new_source, target, "exec")  # syntax only; NEVER execute proposals here
    digest = hashlib.sha256((target + "\n" + new_source).encode()).hexdigest()[:16]
    record = {"created_at": datetime.now(timezone.utc).isoformat(),
              "target": target, "reason": str(reason)[:1000],
              "source_sha256": hashlib.sha256(new_source.encode()).hexdigest(),
              "status": "awaiting_external_review"}
    broker.write_note("proposals/" + digest + ".json", json.dumps(record, indent=2))
    broker.write_note("proposals/" + digest + ".txt", new_source)
    return {"proposal_id": digest, "status": "awaiting_external_review"}
