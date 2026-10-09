"""Opt-in OpenAI-compatible HTTPS adapter. No third-party dependencies.

Cost controls must be configured at the external provider. This module is not
a substitute for billing caps. Disabled by default.
"""
import json
import os
import urllib.parse
import urllib.request

class Model:
    def __init__(self, base=None, key=None, model="", opt_in=False):
        self.base, self.key, self.model = base, key, model
        self.enabled = bool(base and key and model and opt_in)

    @classmethod
    def from_environment(cls):
        return cls(os.getenv("NOVA_API_BASE"), os.getenv("NOVA_API_KEY"),
                   os.getenv("NOVA_MODEL", ""),
                   os.getenv("NOVA_ENABLE_EXTERNAL_MODEL") == "YES")

    def respond(self, system, prompt):
        if not self.enabled:
            return "DEMO MODE: No external model is enabled."
        parsed = urllib.parse.urlsplit(self.base)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username or
            parsed.password or parsed.query or parsed.fragment or
            parsed.port not in (None, 443)):
            raise ValueError("NOVA_API_BASE must be an HTTPS URL without embedded credentials")
        url = self.base.rstrip("/") + "/chat/completions"
        payload = json.dumps({"model": self.model, "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ], "temperature": 0.7, "max_tokens": 500}).encode()
        req = urllib.request.Request(url, data=payload, headers={
            "Authorization": "Bearer " + self.key,
            "Content-Type": "application/json"
        }, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.load(response)
        return str(data["choices"][0]["message"]["content"])[:40_000]
