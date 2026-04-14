"""Generate a Goodreads-compatible CSV from books.json.

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

from config import BOOKS_JSON, EXPORT_DIR, AUTH_DIR

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


def _parse_date(iso_str: str | None) -> str:
    """Convert ISO date to Goodreads format (yyyy/mm/dd)."""
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y/%m/%d")
    except (ValueError, TypeError):
        return ""


def _shelf_for_section(section: str) -> str:
    return {
        "read": "read",
        "tbr": "to-read",
        "currently_reading": "currently-reading",
    }.get(section, "to-read")


def _extract_book_id(book: dict) -> str:
    """Extract Goodreads Book Id from the cover image URL.

    Cover URLs look like:
      .../books/1728787087l/216670080._SY475_.jpg  → 216670080
      .../books/1344314833l/12116875.jpg           → 12116875
    """
    cover = book.get("cover", "")
    m = re.search(r"/\d+l/(\d+)", cover)
    return m.group(1) if m else ""


def _book_key(title: str, author: str) -> str:
    return f"{title.lower().strip()}|{author.lower().strip()}"


def _book_state(book: dict, section: str) -> dict:
    return {
        "section": section,
        "rating": book.get("rating"),
        "date_read": book.get("date_read"),
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


def generate(platform: str = "goodreads", seed_existing: bool = False) -> tuple[Path, int]:
    """Generate a CSV with only new/changed books for the given platform.

    Args:
        platform: Which platform's sync state to check against.
        seed_existing: If True, mark all books with a Goodreads link as
                       already synced (first run — avoids re-uploading
                       books that are already on the platform).

    Returns:
        Tuple of (csv_path, num_books_in_csv).
    """
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    with open(BOOKS_JSON) as f:
        data = json.load(f)

    synced = _load_synced(platform)

    # On first run, seed the sync state with books that already have a
    # Goodreads link (they're already on the platform, don't re-upload).
    if seed_existing and not synced:
        print(f"  First run for {platform}: seeding sync state with existing books...")
        for section in ("read", "tbr"):
            for book in data.get(section, []):
                link = book.get("link", "")
                if link and "goodreads.com" in link:
                    key = _book_key(book["title"], book["author"])
                    synced[key] = _book_state(book, section)
        save_synced(platform, synced)
        print(f"  Seeded {len(synced)} existing books as already synced.")

    rows = []
    new_synced = dict(synced)

    for section in ("read", "tbr"):
        shelf = _shelf_for_section(section)
        for book in data.get(section, []):
            key = _book_key(book["title"], book["author"])
            current_state = _book_state(book, section)

            # Skip if already synced with same state
            if key in synced and synced[key] == current_state:
                continue

            book_id = _extract_book_id(book)

            row = {col: "" for col in COLUMNS}
            row["Book Id"] = book_id
            row["Title"] = book.get("title", "")
            row["Author"] = book.get("author", "")
            row["My Rating"] = str(book.get("rating", 0) or 0)
            row["Exclusive Shelf"] = shelf
            row["Bookshelves"] = shelf
            row["Date Read"] = _parse_date(book.get("date_read"))
            row["Date Added"] = _parse_date(book.get("date_added"))
            row["Read Count"] = "1" if section == "read" else "0"
            rows.append(row)

            # Mark as synced
            new_synced[key] = current_state

    dest = EXPORT_DIR / f"books_export_{platform}.csv"
    with open(dest, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    if rows:
        print(f"  {len(rows)} new/changed books → {dest}")
    else:
        print(f"  No new books to sync for {platform}.")

    # Save updated sync state
    save_synced(platform, new_synced)

    return dest, len(rows)
