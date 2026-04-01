#!/usr/bin/env python3
"""
Fetches Goodreads read/TBR shelves via RSS and outputs data/books.json.
Requires GOODREADS_USER_ID environment variable.
"""

import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import urllib.request

DATE_FORMATS = [
    "%a, %d %b %Y %H:%M:%S %z",
    "%a, %d %b %Y %H:%M:%S %Z",
]


def parse_date(date_str):
    if not date_str or not date_str.strip():
        return None
    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            continue
    return None


def get_text(item, tag, default=""):
    el = item.find(tag)
    if el is not None and el.text:
        return el.text.strip()
    return default


def fetch_shelf(user_id, shelf):
    sort = "date_read" if shelf == "read" else "date_added"
    url = (
        f"https://www.goodreads.com/review/list_rss/{user_id}"
        f"?shelf={shelf}&per_page=200&sort={sort}&order=d"
    )

    print(f"  Fetching {shelf} shelf from {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; book-fetcher/1.0)"})
    with urllib.request.urlopen(req, timeout=30) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("No <channel> found in RSS feed")

    books = []
    for item in channel.findall("item"):
        cover = (
            get_text(item, "book_large_image_url")
            or get_text(item, "book_medium_image_url")
            or get_text(item, "book_image_url")
        )

        review = get_text(item, "user_review")

        book = {
            "title": get_text(item, "title"),
            "author": get_text(item, "author_name"),
            "link": get_text(item, "link"),
            "cover": cover,
            "rating": int(get_text(item, "user_rating", "0") or "0"),
            "pages": get_text(item, "num_pages"),
            "review": review if review else None,
        }

        if shelf == "read":
            book["date_read"] = parse_date(get_text(item, "user_read_at"))
            book["date_added"] = parse_date(get_text(item, "user_date_added") or get_text(item, "pubDate"))
        else:
            book["date_added"] = parse_date(get_text(item, "user_date_added") or get_text(item, "pubDate"))

        books.append(book)

    return books


def sort_read_books(books):
    """Sort by rating desc, then date_read desc (most recent first within same rating)."""
    def sort_key(b):
        rating = -(b.get("rating") or 0)
        date_str = b.get("date_read") or ""
        # ISO format strings sort correctly lexicographically, negate with empty = sorts last
        return (rating, "" if not date_str else "\xff" + date_str[::-1])

    # Two-pass stable sort: date first, then rating (stable preserves date order within rating)
    def to_ts(b):
        d = b.get("date_read")
        if not d:
            return 0
        try:
            return datetime.strptime(d, "%Y-%m-%dT%H:%M:%SZ").timestamp()
        except ValueError:
            return 0

    books.sort(key=to_ts, reverse=True)  # most recent first
    books.sort(key=lambda b: b.get("rating") or 0, reverse=True)  # highest rating first
    return books


def main():
    user_id = os.environ.get("GOODREADS_USER_ID", "").strip()
    if not user_id:
        print("Error: GOODREADS_USER_ID environment variable is not set")
        raise SystemExit(1)

    print(f"Fetching books for Goodreads user {user_id}...")

    read_books = fetch_shelf(user_id, "read")
    print(f"  Found {len(read_books)} read books")

    tbr_books = fetch_shelf(user_id, "to-read")
    print(f"  Found {len(tbr_books)} TBR books")

    pinned_links = set()
    if os.path.exists("data/pinned.json"):
        with open("data/pinned.json", encoding="utf-8") as f:
            raw = json.load(f)
        # Strip UTM params so links match regardless of source
        for link in raw:
            pinned_links.add(link.split("?")[0])

    favourites = [b for b in read_books if b.get("link", "").split("?")[0] in pinned_links]
    print(f"  Found {len(favourites)} pinned favourite books")

    sort_read_books(read_books)

    output = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "favourites": favourites,
        "read": read_books,
        "tbr": tbr_books,
    }

    os.makedirs("data", exist_ok=True)
    with open("data/books.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Written data/books.json — {len(favourites)} favourites, {len(read_books)} read, {len(tbr_books)} TBR")


if __name__ == "__main__":
    main()
