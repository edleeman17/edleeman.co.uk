#!/usr/bin/env bash
# Sync books.json to Goodreads only.
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python3.14 sync.py goodreads
