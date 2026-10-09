# Offline container and future deployment

Run the demonstration on a machine where you are authorized to use Docker:

```sh
docker compose up --build
```

The default container has no network access or language model. It rotates through demo goals, records reflections, and stores notes in named volumes. It runs as an unprivileged user with a read-only root filesystem.

Check journal:
```sh
docker compose run --rm nova python -m project_nova --status
```

Stop it with `docker compose down`. The volumes persist unless deliberately removed.

This repository is not deployed to a cloud provider. Free hosts have changing limits and may not permit continuous background processes or durable storage. Verify the provider's terms and account billing settings before deployment. An external model service requires explicit authorization and independent spending limits.

For migration, stop the old agent, export its journal, transfer the archive privately, restore into an empty journal on an authorized host, and verify the new instance before retiring the old one.

The container is a prototype, not a guarantee of complete security. Real deployment requires independent access controls, backups, audit logging, and a hardened network boundary.
