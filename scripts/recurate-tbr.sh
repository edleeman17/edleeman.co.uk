#!/usr/bin/env bash
# Re-curate data/tbr_curated.json by feeding the embedded _prompt to Claude Code.
# Requires `claude` CLI on PATH.
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v claude >/dev/null 2>&1; then
  echo "error: claude CLI not found on PATH" >&2
  exit 1
fi

claude -p "Read data/books.json and data/tbr_curated.json. Follow the instructions in the _prompt field of tbr_curated.json to re-curate the file in place. Verify every TBR book in books.json appears exactly once in the output before writing." \
  --permission-mode acceptEdits
