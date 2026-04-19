#!/usr/bin/env python3
"""Look up page counts from Open Library and patch content/reading/*.md files."""
import re
import time
import urllib.request
import urllib.parse
import json
from pathlib import Path

READING_DIR = Path(__file__).resolve().parent.parent / "content" / "reading"
RATE_LIMIT = 0.6


def parse_field(text, key):
    m = re.search(rf'^{key}: +"?(.*?)"?\s*$', text, re.MULTILINE)
    return m.group(1) if m else ""


def clean_title(title):
    """Strip series info in parens and long subtitles for better search matching."""
    t = re.sub(r'\s*\([^)]*\)\s*$', '', title).strip()  # remove trailing (...)
    t = re.sub(r'\s*:\s*.+$', '', t).strip() if len(t) > 30 else t  # strip subtitle
    return t or title


def clean_author(author):
    return re.sub(r'\s+', ' ', author).strip()


def lookup_pages(title, author):
    searches = [
        (title, author),
        (clean_title(title), author),
        (clean_title(title), clean_author(author).split()[0] if author else ""),
    ]
    seen = set()
    for t, a in searches:
        key = (t, a)
        if key in seen:
            continue
        seen.add(key)
        pages = _query(t, a)
        if pages:
            return pages
    return 0


def _query(title, author):
    params = {"title": title, "fields": "title,author_name,number_of_pages_median", "limit": "5"}
    if author:
        params["author"] = author
    url = f"https://openlibrary.org/search.json?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=12) as r:
            data = json.loads(r.read())
    except Exception as e:
        print(f"\n  ERROR: {e}")
        return 0
    for doc in data.get("docs", []):
        pages = doc.get("number_of_pages_median")
        if pages and 50 < pages < 2000:
            return pages
    return 0


def patch_pages(path, pages):
    text = path.read_text(encoding="utf-8")
    new_text = re.sub(r'^pages: \d+$', f'pages: {pages}', text, flags=re.MULTILINE)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    files = sorted(READING_DIR.glob("*.md"))
    zero_files = [f for f in files if f.name != "_index.md"
                  and re.search(r'^pages: 0$', f.read_text(encoding="utf-8"), re.MULTILINE)]

    print(f"Found {len(zero_files)} files with pages: 0\n")

    updated = 0
    not_found = []

    for i, f in enumerate(zero_files, 1):
        text = f.read_text(encoding="utf-8")
        title = parse_field(text, "title")
        author = parse_field(text, "author")

        print(f"[{i}/{len(zero_files)}] {title[:60]}", end=" ... ", flush=True)

        pages = lookup_pages(title, author)
        if pages:
            patch_pages(f, pages)
            print(f"{pages}pp ✓")
            updated += 1
        else:
            print("not found")
            not_found.append(f"{title} ({clean_author(author)})")

        time.sleep(RATE_LIMIT)

    print(f"\nDone. Updated: {updated}, Not found: {len(not_found)}")
    if not_found:
        print("\nNot found:")
        for t in not_found:
            print(f"  {t}")


if __name__ == "__main__":
    main()
