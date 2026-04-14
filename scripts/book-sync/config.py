"""Paths and configuration for book-sync."""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = REPO_ROOT / "data"
BOOKS_JSON = DATA_DIR / "books.json"
SYNC_STATE = Path(__file__).resolve().parent / "last_synced.json"
AUTH_DIR = Path.home() / ".config" / "book-sync"
LOG_DIR = AUTH_DIR / "logs"

# Playwright auth state per platform
GOODREADS_AUTH = AUTH_DIR / "goodreads-auth.json"
STORYGRAPH_AUTH = AUTH_DIR / "storygraph-auth.json"
FABLE_AUTH = AUTH_DIR / "fable-auth.json"

# Temp dir for CSV exports
EXPORT_DIR = AUTH_DIR / "exports"

# Set by --headless flag in sync.py
HEADLESS = False
