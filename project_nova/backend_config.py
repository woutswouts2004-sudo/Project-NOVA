"""Validate backend URLs before they are put into a public website.

Only explicit HTTPS hosts are accepted. Do not embed API keys.
"""
from urllib.parse import urlsplit

def validate_backend_url(value):
    if not isinstance(value, str):
        raise ValueError("Backend URL must be text")
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or not parsed.hostname
            or parsed.username or parsed.password or parsed.query
            or parsed.fragment or parsed.port not in (None, 443)):
        raise ValueError("Public backend must be HTTPS without credentials")
    if parsed.hostname in {"localhost", "127.0.0.1"}:
        raise ValueError("A public site cannot use localhost")
    return value.rstrip("/")
