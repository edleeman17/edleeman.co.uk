"""Generate a Goodreads-compatible CSV from content/reading/*.md files.

Only includes books that haven't been synced yet (or have changed).
Tracks sync state per platform in ~/.config/book-sync/<platform>_synced.json.

Uses the Goodreads Book Id (extracted from cover image URLs) to ensure
exact edition matching and prevent duplicate imports.
"""
import csv
import json
import re
from datetime import datetime
from pathlib import Path

import frontmatter  # python-frontmatter

from config import READING_DIR, EXPORT_DIR, AUTH_DIR

# Goodreads CSV columns — Book Id first for exact edition matching
COLUMNS = [
    "Book Id",
    "Title",
    "Author",
    "ISBN",
    "ISBN13",
    "My Rating",
    "Average Rating",
    "Publisher",
    "Binding",
    "Number of Pages",
    "Year Published",
    "Original Publication Year",
    "Date Read",
    "Date Added",
    "Bookshelves",
    "Bookshelves with positions",
    "Exclusive Shelf",
    "My Review",
    "Spoiler",
    "Private Notes",
    "Read Count",
    "Recommended For",
    "Recommended By",
    "Owned Copies",
    "Original Purchase Date",
    "Original Purchase Location",
    "Condition",
    "Condition Description",
    "BCID",
]


def _parse_date(iso_str) -> str:
    """Convert ISO date string to Goodreads format (yyyy/mm/dd)."""
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(str(iso_str).replace("Z", "+00:00"))
        return dt.strftime("%Y/%m/%d")
    except (ValueError, TypeError):
        return ""


def _shelf_for(shelf: str) -> str:
    return {
        "read": "read",
        "tbr": "to-read",
        "currently-reading": "currently-reading",
    }.get(shelf, "to-read")


def _extract_book_id(cover: str) -> str:
    """Extract Goodreads Book Id from cover image URL."""
    m = re.search(r"/\d+l/(\d+)", cover or "")
    return m.group(1) if m else ""


def _book_state(meta: dict, shelf: str) -> dict:
    return {
        "shelf": shelf,
        "rating": meta.get("rating"),
        "date_read": str(meta.get("date_read", "") or ""),
    }


def _sync_state_path(platform: str) -> Path:
    return AUTH_DIR / f"{platform}_synced.json"


def _load_synced(platform: str) -> dict:
    path = _sync_state_path(platform)
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def save_synced(platform: str, state: dict):
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    with open(_sync_state_path(platform), "w") as f:
        json.dump(state, f, indent=2)


def _load_reading_pages() -> list[dict]:
    """Parse all content/reading/*.md files and return list of frontmatter dicts."""
    pages = []
    for md_path in sorted(READING_DIR.glob("*.md")):
        try:
            post = frontmatter.load(str(md_path))
            meta = dict(post.metadata)
            meta["_slug"] = md_path.stem
            pages.append(meta)
        except Exception as e:
            print(f"  Warning: could not parse {md_path.name}: {e}")
    return pages


def generate(platform: str = "goodreads", seed_existing: bool = False) -> tuple[Path, int]:
    """Generate a CSV with only new/changed books for the given platform.

    Args:
        platform: Which platform's sync state to check against.
        seed_existing: If True, mark all books with a goodreads_url as already
                       synced (first run — avoids re-uploading existing books).

    Returns:
        Tuple of (csv_path, num_books_in_csv).
    """
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    pages = _load_reading_pages()
    synced = _load_synced(platform)

    if seed_existing and not synced:
        print(f"  First run for {platform}: seeding sync state with existing books...")
        for meta in pages:
            shelf = str(meta.get("shelf", ""))
            if shelf not in ("read", "tbr"):
                continue
            if meta.get("goodreads_url"):
                slug = meta["_slug"]
                synced[slug] = _book_state(meta, shelf)
        save_synced(platform, synced)
        print(f"  Seeded {len(synced)} existing books as already synced.")

    rows = []
    new_synced = dict(synced)

    for meta in pages:
        shelf = str(meta.get("shelf", ""))
        if shelf not in ("read", "tbr"):
            continue

        slug = meta["_slug"]
        current_state = _book_state(meta, shelf)

        if slug in synced and synced[slug] == current_state:
            continue

        cover = str(meta.get("cover", "") or "")
        goodreads_id = str(meta.get("goodreads_id", "") or "") or _extract_book_id(cover)

        row = {col: "" for col in COLUMNS}
        row["Book Id"] = goodreads_id
        row["Title"] = str(meta.get("title", ""))
        row["Author"] = str(meta.get("author", ""))
        row["My Rating"] = str(int(meta.get("rating", 0) or 0))
        row["Exclusive Shelf"] = _shelf_for(shelf)
        row["Bookshelves"] = _shelf_for(shelf)
        row["Date Read"] = _parse_date(meta.get("date_read"))
        row["Date Added"] = _parse_date(meta.get("date_added"))
        row["Read Count"] = "1" if shelf == "read" else "0"
        rows.append(row)

        new_synced[slug] = current_state

    dest = EXPORT_DIR / f"books_export_{platform}.csv"
    with open(dest, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    if rows:
        print(f"  {len(rows)} new/changed books → {dest}")
    else:
        print(f"  No new books to sync for {platform}.")

    save_synced(platform, new_synced)

    return dest, len(rows)
