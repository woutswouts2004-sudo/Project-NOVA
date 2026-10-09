"""Restricted read-only research helper. Avoid redirects and DNS rebinding risks.

For production use a separately deployed egress proxy with IP-level network
controls, strict DNS validation and content-size limits. This helper is a
prototype and is not suitable for unrestricted autonomous browsing.
"""
import urllib.error
import urllib.request
from .broker import Denied

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Denied("Redirects are not allowed")

def research_public_page(broker, url):
    broker.check_research_url(url)
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": "ProjectNOVA/0.1"})
    with opener.open(req, timeout=8) as response:
        content_type = response.headers.get("Content-Type", "")
        if not (content_type.startswith("text/plain") or content_type.startswith("text/html")):
            raise Denied("Only plain text or HTML allowed")
        data = response.read(50_001)
        if len(data) > 50_000:
            raise Denied("Page exceeds size limit")
        return data.decode("utf-8", errors="replace")
