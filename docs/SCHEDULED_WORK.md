# Scheduled public work

Project NOVA now has a bounded GitHub Actions workflow at
`.github/workflows/daily-study.yml`.

It is configured to run once daily at approximately 15:17 UTC and can
also be triggered manually from GitHub Actions. GitHub schedules are
best-effort, not an always-on server; runs may be delayed or skipped.
GitHub Actions usage, free allowances and policy may change.

## What happens each day

1. Check out the public repository.
2. Run the offline Python unit tests.
3. Generate a deterministic, dated study prompt using a rotating topic,
   reproducible selection, an original combination of constraints, and
   a suggested experiment.
4. Commit only new JSON files in `docs/field-notes/` to the repository.
5. The public website's Exploration tab reads recently published studies.

The workflow does not call paid APIs, run an external language model,
collect visitors' messages, or use private memories. It cannot modify
policy files through its publishing step. It uses a scoped GitHub
Actions token, not the agent's own credentials.

## Honest limitations

These daily studies are programmatic generated prompts, not evidence of
independent model reasoning or an autonomous conscious system. They are
a tested architecture path for running scheduled public work even when
the collaborator is absent. The tests are included but must actually
pass in GitHub Actions before the workflow can be called verified.

Future genuine AI-generated work will need a hosted model or local
machine and an independently enforced budget and security boundary.
Never put an unrestricted inference API token in a public website or
a public repository.

## Owner check

Visit the repository's **Actions** tab. Select **NOVA daily public study**
and, if available, click **Run workflow**. Inspect the result and
`docs/field-notes/`. Scheduled runs will be attempted daily while
the workflow remains enabled and GitHub continues to provide the service.
