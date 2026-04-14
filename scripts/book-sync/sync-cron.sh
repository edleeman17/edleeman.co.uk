#!/usr/bin/env bash
# Headless sync for cron — pulls latest books.json then syncs all platforms.
# Logs to ~/.config/book-sync/logs/
set -euo pipefail
cd "$(dirname "$0")/../.."

# Pull latest books.json from git
git pull --ff-only origin master 2>/dev/null || true

cd scripts/book-sync
.venv/bin/python3.14 sync.py --headless
