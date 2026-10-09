"""Owner-controlled capability broker. Run separately in production.

The agent is only offered these methods. Source-file separation alone does NOT
make policy immutable against an agent with filesystem or deployment control.
"""
import ipaddress
import json
import socket
from pathlib import Path
from urllib.parse import urlsplit

class Denied(PermissionError):
    pass

class Broker:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.workspace = self.root / "workspace"
        self.workspace.mkdir(parents=True, exist_ok=True)
        policy_path = Path(__file__).resolve().parent.parent / "policy" / "capabilities.json"
        self.policy = json.loads(policy_path.read_text(encoding="utf-8"))

    def check(self, capability):
        if capability not in self.policy.get("allowed", []):
            raise Denied("Capability not granted: " + capability)

    def workspace_path(self, relative):
        self.check("workspace_write")
        path = (self.workspace / relative).resolve()
        if not path.is_relative_to(self.workspace.resolve()) or path == self.workspace.resolve():
            raise Denied("Outside designated workspace")
        if path.suffix not in {".md", ".txt", ".json"}:
            raise Denied("Only text notes allowed")
        return path

    def write_note(self, relative, content):
        path = self.workspace_path(relative)
        if len(content.encode("utf-8")) > 100_000:
            raise Denied("Note too large")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return {"saved": str(path.relative_to(self.workspace))}

    def check_research_url(self, url):
        self.check("public_research")
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            raise Denied("Only public HTTPS URLs are permitted")
        if parsed.port not in (None, 443):
            raise Denied("Nonstandard port")
        host = parsed.hostname.lower().rstrip(".")
        if host in {"localhost", "metadata.google.internal"} or host.endswith((".local", ".internal")):
            raise Denied("Private or metadata host")
        try:
            addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        except socket.gaierror:
            raise Denied("Host could not be resolved")
        for item in addresses:
            address = ipaddress.ip_address(item[4][0])
            if not address.is_global:
                raise Denied("Private, loopback, or reserved address")
        return url

    def request_purchase(self, *args, **kwargs):
        raise Denied("Purchases and paid resource provisioning are disabled")

    def request_shell(self, *args, **kwargs):
        raise Denied("Shell execution is not exposed to the agent")

    def request_deployment(self, *args, **kwargs):
        raise Denied("Deployment and policy changes require independent owner authorization")
