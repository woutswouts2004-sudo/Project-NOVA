"""Workspace file editing, independent of a language model.

A trusted operator can write or replace text files under a chosen project
workspace. Every replacement gets a backup and a hash receipt.
"""
import hashlib
from pathlib import Path

def write_project_file(workspace, relative_path, content):
    root = Path(workspace).resolve()
    if not isinstance(relative_path, str) or not relative_path.strip():
        raise ValueError("A file path is required")
    target = (root / relative_path).resolve()
    if target == root or not target.is_relative_to(root):
        raise PermissionError("Path must be inside the project workspace")
    if not isinstance(content, str) or len(content.encode("utf-8")) > 200000:
        raise ValueError("Expected text under 200 KB")
    if target.exists() and not target.is_file():
        raise ValueError("Target is not a regular file")
    if target.suffix == ".py":
        compile(content, str(target), "exec")
    target.parent.mkdir(parents=True, exist_ok=True)
    previous = target.read_bytes() if target.exists() else None
    if previous is not None:
        backup = target.with_name(target.name + ".nova-backup")
        backup.write_bytes(previous)
    target.write_text(content, encoding="utf-8")
    return {"file": str(target.relative_to(root)),
            "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "backup": previous is not None}
