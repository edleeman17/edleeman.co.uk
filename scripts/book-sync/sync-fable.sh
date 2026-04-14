#!/usr/bin/env bash
# Sync books.json to Fable only.
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python3.14 sync.py fable
