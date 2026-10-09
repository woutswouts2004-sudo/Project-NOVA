"""Require explicit provenance records for research training datasets."""
import json
from pathlib import Path

ALLOWED_LICENSES = {"CC0-1.0", "CC-BY-4.0", "PUBLIC-DOMAIN", "ORIGINAL-OWNED"}

def validate_manifest(data):
    if not isinstance(data, dict):
        raise ValueError("Manifest must be an object")
    if data.get("license") not in ALLOWED_LICENSES:
        raise ValueError("Unsupported or unspecified training-data license")
    if not isinstance(data.get("source"), str) or not data["source"].strip():
        raise ValueError("Dataset source required")
    if data.get("contains_private_chats") is not False:
        raise ValueError("Private chat inclusion is prohibited")
    if data.get("visitor_consent_required") is not False:
        raise ValueError("Visitor data cannot be silently included")
    if data.get("permission_confirmed") is not True:
        raise ValueError("Explicit permission must be confirmed")
    return data

def load_manifest(path):
    path = Path(path)
    if path.stat().st_size > 100_000:
        raise ValueError("Manifest too large")
    return validate_manifest(json.loads(path.read_text(encoding="utf-8")))
