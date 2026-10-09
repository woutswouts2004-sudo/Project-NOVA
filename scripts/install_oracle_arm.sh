#!/usr/bin/env bash
# Run on a personally authorized Ubuntu ARM64 Oracle VM as the ubuntu user.
set -Eeuo pipefail
if [ "$(id -u)" -eq 0 ]; then
  echo "Run as an unprivileged SSH user, not root" >&2; exit 1
fi
if [ "$(uname -m)" != "aarch64" ]; then
  echo "Expected ARM64 (Ampere A1). Got $(uname -m)" >&2; exit 1
fi
sudo apt-get update
sudo apt-get install -y ca-certificates curl git
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com -o /tmp/nova-get-docker.sh
  echo "Review /tmp/nova-get-docker.sh before executing if desired."
  sudo sh /tmp/nova-get-docker.sh
fi
if ! sudo docker compose version >/dev/null 2>&1; then
  echo "Docker Compose plugin missing. Install docker-compose-plugin and rerun." >&2
  exit 1
fi
if [ ! -d "$HOME/Project-NOVA/.git" ]; then
  git clone https://github.com/woutswouts2004-sudo/Project-NOVA.git "$HOME/Project-NOVA"
fi
cd "$HOME/Project-NOVA"
git pull --ff-only
sudo docker compose -f compose.live.yaml up -d --build
sudo docker compose -f compose.live.yaml exec -T ollama ollama pull qwen2.5:3b
sudo docker compose -f compose.live.yaml restart chat worker
sudo docker compose -f compose.live.yaml ps
echo "Local chat health check:"
curl --fail --max-time 10 http://127.0.0.1:8080/health || true
echo
echo "NOVA is on this VM only. Public HTTPS is NOT configured."
