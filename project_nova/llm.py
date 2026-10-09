"""Optional OpenAI-compatible HTTPS adapter. No third-party dependencies."""
import json
import os
import urllib.parse
import urllib.request

class Model:
    def __init__(self, base=None, key=None, model=""):
        self.base, self.key, self.model = base, key, model

    @classmethod
    def from_environment(cls):
        return cls(os.getenv("NOVA_API_BASE"), os.getenv("NOVA_API_KEY"),
                   os.getenv("NOVA_MODEL", ""))

    def respond(self, system, prompt):
        if not (self.base and self.key and self.model):
            return ("DEMO MODE: I can journal my development and prepare plans, "
                    "but no live language model is configured.")
        parsed = urllib.parse.urlsplit(self.base)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
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
        return data["choices"][0]["message"]["content"]
