# NOVA self-development workflow

NOVA can now propose source improvements itself **when a real language
model is configured**.

```sh
python -m project_nova.self_development --home ./nova_runtime \
  --target project_nova/autonomy.py
```

The proposal workflow:
1. Reads a specifically allowlisted editable module.
2. Asks the configured model for a conservative complete replacement.
3. Checks Python syntax without executing the candidate.
4. Stores candidate source and a hash-bearing manifest in the isolated
   workspace's `proposals/` directory.
5. Journals that a proposal was created.
6. Stops. No deployment, commit, shell execution or privileged access occurs.

Protected modules, policies, credentials and workflows are outside the
allowlist. Candidate source is untrusted, even when syntax-valid.

## Promotion to running code

An independent operator must inspect the proposal, test it in a disposable
sandbox, review the diff, and approve deployment. Future automation can
prepare pull requests on restricted branches and run CI; merging and
production release should remain under independently enforced permissions.

A model cannot make its own sandbox, billing limits, or access-control
rules unchangeable merely by promising not to edit them. Those boundaries
must be enforced by the hosting platform.

## Not yet deployed

This repository currently has no trained conversational model weights
or always-on host. This self-development path is source code and unit
tests, not a running autonomous self-updating service.
