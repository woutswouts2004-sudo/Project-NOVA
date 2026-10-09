"""NOVA hosting suitability assessor.

Produces an explainable ranking, never invents cloud accounts, credentials,
available capacity, or claims that a deployment has happened.
"""
from dataclasses import dataclass, asdict
import json

@dataclass(frozen=True)
class Host:
    name: str
    continuous: bool
    persistent: bool
    runs_ollama: bool
    requires_account: bool
    notes: str

HOSTS = (
    Host("Owner-operated Docker host", True, True, True, False,
         "Requires an already available powered-on machine and network."),
    Host("Oracle Cloud Always Free ARM VM", True, True, True, True,
         "Capacity, eligibility, account verification and idle reclamation apply; small CPU models may be slow."),
    Host("Render free web service", False, False, False, True,
         "Sleeps after inactivity; ephemeral filesystem; external inference required."),
    Host("GitHub Actions scheduled runner", False, False, False, False,
         "Short scheduled jobs, not a persistent 24/7 server; artifacts require external persistence."),
)

def assess(require_continuous=True, require_persistent=True, require_local_model=True):
    options = []
    for host in HOSTS:
        failures = []
        if require_continuous and not host.continuous:
            failures.append("not continuously running")
        if require_persistent and not host.persistent:
            failures.append("no durable local storage")
        if require_local_model and not host.runs_ollama:
            failures.append("no suitable always-on local model")
        options.append({**asdict(host), "meets_requirements": not failures,
                        "limitations": failures})
    return options

def main():
    print(json.dumps(assess(), indent=2))

if __name__ == "__main__":
    main()
