# NOVA's hosting decision (October 2026)

NOVA now has a local host assessment command:

```sh
python -m project_nova.host_finder
```

The evaluator distinguishes **continuously running** from merely
reachable on demand. It cannot discover free compute capacity or
register a provider account by itself.

## Strongest free-host candidate: Oracle Cloud Always Free

Oracle's official Always Free documentation describes ARM virtual
machines, block storage, and a limited free monthly CPU/memory allowance:
https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm

The ARM VM could host NOVA's Docker Compose stack with an appropriately
small Ollama model. Capacity may be unavailable in some regions. Oracle
may reclaim idle free instances. Creating an account may require
verification and agreement to provider terms.

## Alternatives

- An already available owner-operated Docker computer: simplest path
  to a persistent model, but it must remain powered on.
- Render free web service: can host the chat API connected to external
  inference, but it sleeps after 15 minutes idle and local storage is
  ephemeral, so it does not satisfy the persistent-worker requirement.
  Source: https://render.com/docs/free
- GitHub Actions: supports periodic bounded jobs but cannot provide a
  permanently running model server.

## What is still missing

A real authorized machine or cloud account, network configuration,
HTTPS ingress, model download, and a live smoke test. None is deployed
or connected as of this document. The hosting evaluator does not
provision resources or run a browser. It is intentionally honest about
which requirements each option fails.

After a host is available, deploy using `compose.live.yaml` and
`docs/CONTINUOUS_RUNTIME.md`. Verify the local health endpoint,
persisted SQLite data, scheduled worker logs and public HTTPS routing.
