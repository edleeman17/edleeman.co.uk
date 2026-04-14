#!/usr/bin/env bash
# Just generate the Goodreads-format CSV without uploading anywhere.
# Output: ~/.config/book-sync/exports/books_export.csv
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python3.14 sync.py --generate-only
