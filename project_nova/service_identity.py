"""A durable, scoped registry of NOVA's delegated service identities.

Never stores passwords, API tokens or private keys. It describes accounts
created and authorized by the provider's required human or legal owner.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

def register_service(registry_path, name, provider, handle, scopes, approved_by):
    if not all(isinstance(v, str) and 0 < len(v.strip()) <= 160
               for v in (name, provider, handle, approved_by)):
        raise ValueError("Service, provider, handle and authorizer are required")
    if not isinstance(scopes, list) or not scopes or len(scopes) > 20 or not all(
            isinstance(s, str) and 0 < len(s) <= 100 for s in scopes):
        raise ValueError("Provide explicit permission scopes")
    path = Path(registry_path)
    if path.exists():
        registry = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(registry, dict):
            raise ValueError("Invalid registry")
    else:
        registry = {}
    registry[name] = {
        "provider": provider, "handle": handle, "scopes": scopes,
        "authorized_by": approved_by,
        "status": "registered_not_verified",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    return registry[name]

def list_services(registry_path):
    path = Path(registry_path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
