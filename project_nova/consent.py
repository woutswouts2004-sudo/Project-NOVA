"""Explicit owner-managed access grants for future private data connectors.

A grant is only an authorization record. It does not confer actual access,
credentials, or legal authority to data that the grantor does not control.
The grant file must be owned by an independent service, not the editable agent.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

class ConsentDenied(PermissionError):
    pass

class ConsentRegistry:
    def __init__(self, path):
        self.path = Path(path)

    def _grants(self):
        if not self.path.exists():
            return []
        if self.path.stat().st_size > 100_000:
            raise ConsentDenied("Consent registry too large")
        obj = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(obj, dict) or not isinstance(obj.get("grants"), list):
            raise ConsentDenied("Invalid consent registry")
        return obj["grants"]

    def check(self, source, resource, purpose, now=None):
        """Deny unless exact source/resource/purpose match an unexpired grant."""
        now = now or datetime.now(timezone.utc)
        if not all(isinstance(x, str) and x for x in (source, resource, purpose)):
            raise ConsentDenied("Missing scope")
        for grant in self._grants():
            if not isinstance(grant, dict):
                continue
            if grant.get("source") != source or grant.get("resource") != resource:
                continue
            if purpose not in grant.get("purposes", []):
                continue
            if grant.get("revoked", True):
                continue
            try:
                expiry = datetime.fromisoformat(grant["expires_at"].replace("Z", "+00:00"))
                if expiry.tzinfo is None or expiry <= now:
                    continue
            except (ValueError, TypeError, KeyError, AttributeError):
                continue
            return True
        raise ConsentDenied("No active consent for this source, resource and purpose")
