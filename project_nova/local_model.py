"""Optional local Ollama model adapter: no cloud API account required.

Requires the owner to install and run Ollama on an authorized machine.
No automatic downloads, background installs, purchases or remote execution.
"""
import json
import os
import urllib.parse
import urllib.request

class LocalModel:
    def __init__(self, model, base=None):
        base = base or os.getenv("NOVA_OLLAMA_URL", "http://127.0.0.1:11434")
        if not isinstance(model, str) or not model.strip():
            raise ValueError("A local model name is required")
        parsed = urllib.parse.urlsplit(base)
        if (parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "ollama"}
                or parsed.port != 11434 or parsed.username or parsed.password
                or parsed.query or parsed.fragment or parsed.path not in {"", "/"}):
            raise ValueError("Only the local Ollama endpoint on port 11434 is allowed")
        self.base = base.rstrip("/")
        self.model = model
        self.enabled = True

    def respond(self, system, prompt):
        payload = json.dumps({
            "model": self.model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": prompt}],
            "stream": False,
            "options": {"num_predict": 450}
        }).encode("utf-8")
        req = urllib.request.Request(
            self.base + "/api/chat", data=payload,
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.load(response)
        output = result.get("message", {}).get("content")
        if not isinstance(output, str) or not output.strip():
            raise ValueError("Local model returned no content")
        return output[:40_000]
