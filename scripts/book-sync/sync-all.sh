#!/usr/bin/env bash
# Generate CSV from books.json and upload to Goodreads, StoryGraph, and Fable.
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python3.14 sync.py
