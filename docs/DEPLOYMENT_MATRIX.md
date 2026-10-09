# Deployment options and tradeoffs

| Component | Available today | Requires |
| --- | --- | --- |
| Static public website | GitHub Pages | Public repository and Pages enabled |
| Offline daily study | GitHub Actions | Workflow enabled; subject to scheduling |
| Live public model chat | Not deployed | Authorized inference host and API |
| Continuous agent | Not deployed | Persistent host, storage and model |
| Local open-weight model | Code supported | Hardware running Ollama |
| Safe autonomous code promotion | Not deployed | Separate sandbox and review service |

GitHub Actions scheduled workflows are **not** an always-on process.
GitHub Pages cannot execute Python or keep persistent private memory.
Never assume a cloud service is free without checking current limits.
