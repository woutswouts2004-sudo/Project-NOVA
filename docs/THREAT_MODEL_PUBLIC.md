# Public web threat model

Public visitors may submit hostile or misleading text. The public API
treats visitor history as untrusted and does not expose agent tools.

Risks requiring additional production controls:
- Shared IP addresses and proxy-aware request quotas.
- Resource exhaustion and concurrent model requests.
- API billing, token exhaustion and model abuse.
- Browser storage loss and accidental sensitive-data entry.
- Provider retention and server access logs.
- Injection into any future research or code-editing pipeline.
- CORS mistakes and accidental credential exposure.

Current prototype defenses are partial. Do not put the public API on an
unrestricted internet host until a trusted reverse proxy, budget caps,
abuse protections and operational monitoring are implemented.
