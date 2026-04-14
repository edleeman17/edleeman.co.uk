#!/usr/bin/env bash
# Log in to all reading platforms and save auth cookies.
# Run this first — opens a browser window for each platform.
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python3.14 sync.py --login
