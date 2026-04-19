#!/usr/bin/env python3
"""One-time migration: convert data/books.json → content/reading/*.md + data/reading-index.json"""
import json
import re
import os
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parent.parent
BOOKS_JSON = REPO_ROOT / "data" / "books.json"
READING_DIR = REPO_ROOT / "content" / "reading"
INDEX_JSON = REPO_ROOT / "data" / "reading-index.json"


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def extract_goodreads_id(cover_url: str) -> str:
    if not cover_url:
        return ""
    m = re.search(r"/(\d+)[._]", cover_url)
    return m.group(1) if m else ""


def fmt_date(val) -> str:
    if not val:
        return ""
    if isinstance(val, str):
        return val
    return ""


def make_frontmatter(book: dict, shelf: str, favourite: bool) -> str:
    title = book.get("title", "")
    author = book.get("author", "")
    cover = book.get("cover", "")
    pages = book.get("pages", "") or ""
    goodreads_url = book.get("link", "")
    goodreads_id = extract_goodreads_id(cover)
    rating = book.get("rating", 0) or 0
    review = book.get("review", "") or ""
    date_read = fmt_date(book.get("date_read", ""))
    date_started = fmt_date(book.get("date_started", ""))
    date_added = fmt_date(book.get("date_added", ""))

    # Hugo page date: date_read for read books, date_added otherwise
    if shelf == "read" and date_read:
        page_date = date_read
    elif date_started:
        page_date = date_started
    else:
        page_date = date_added or datetime.now(timezone.utc).isoformat()

    try:
        pages_int = int(pages) if pages else 0
    except (ValueError, TypeError):
        pages_int = 0

    lines = [
        "---",
        f'title: "{title.replace(chr(34), chr(92) + chr(34))}"',
        f"date: {page_date}",
        'type: "reading"',
        "draft: false",
        f'author: "{author.replace(chr(34), chr(92) + chr(34))}"',
        f'cover: "{cover}"',
        f"pages: {pages_int}",
        f'goodreads_url: "{goodreads_url}"',
        f'goodreads_id: "{goodreads_id}"',
        f'shelf: "{shelf}"',
        f"rating: {int(rating)}",
        f"favourite: {str(favourite).lower()}",
        f'date_read: "{date_read}"',
        f'date_started: "{date_started}"',
        f'date_added: "{date_added}"',
        f'review: "{review.replace(chr(34), chr(92) + chr(34))}"',
        "---",
        "",
    ]
    return "\n".join(lines)


def book_to_index_entry(book: dict, slug: str, shelf: str, favourite: bool) -> dict:
    cover = book.get("cover", "")
    return {
        "slug": slug,
        "title": book.get("title", ""),
        "author": book.get("author", ""),
        "cover": cover,
        "pages": book.get("pages", "") or "",
        "goodreads_url": book.get("link", ""),
        "goodreads_id": extract_goodreads_id(cover),
        "shelf": shelf,
        "rating": int(book.get("rating", 0) or 0),
        "favourite": favourite,
        "date_read": fmt_date(book.get("date_read", "")),
        "date_started": fmt_date(book.get("date_started", "")),
        "date_added": fmt_date(book.get("date_added", "")),
        "review": book.get("review", "") or "",
        "syndication": [],
    }


def main():
    with open(BOOKS_JSON) as f:
        data = json.load(f)

    favourite_titles = {b["title"] for b in data.get("favourites", [])}

    READING_DIR.mkdir(parents=True, exist_ok=True)

    seen_slugs: dict[str, int] = {}
    index: list[dict] = []
    written = 0
    skipped = 0

    # Section → shelf mapping; process currently-reading last so it can override a tbr entry
    sections = [
        ("tbr", "tbr"),
        ("currently-reading", "currently-reading"),
        ("read", "read"),
    ]

    slug_to_path: dict[str, Path] = {}

    for section_key, shelf in sections:
        books = data.get(section_key, [])
        for book in books:
            title = book.get("title", "").strip()
            if not title:
                continue

            base_slug = slugify(title)
            # Deduplicate slugs within migration
            if base_slug in seen_slugs:
                seen_slugs[base_slug] += 1
                slug = f"{base_slug}-{seen_slugs[base_slug]}"
            else:
                seen_slugs[base_slug] = 1
                slug = base_slug

            favourite = title in favourite_titles
            frontmatter = make_frontmatter(book, shelf, favourite)
            md_path = READING_DIR / f"{slug}.md"

            # If same slug was written by earlier section (tbr), overwrite with higher-priority shelf
            if slug in slug_to_path:
                print(f"  Overwriting {slug} (was tbr, now {shelf})")
                skipped -= 1  # undo earlier count

            md_path.write_text(frontmatter, encoding="utf-8")
            slug_to_path[slug] = md_path
            written += 1

            entry = book_to_index_entry(book, slug, shelf, favourite)
            # Remove previous entry for same slug if overwriting
            index = [e for e in index if e["slug"] != slug]
            index.append(entry)
            print(f"  [{shelf}] {title} → {slug}.md")

    index_data = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "books": index,
    }
    INDEX_JSON.write_text(json.dumps(index_data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nDone. {written} markdown files written to {READING_DIR}")
    print(f"Index written to {INDEX_JSON} ({len(index)} entries)")


if __name__ == "__main__":
    main()
