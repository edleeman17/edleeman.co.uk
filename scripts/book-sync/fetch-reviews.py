#!/usr/bin/env python3
"""Fetch Goodreads reviews and populate review field in content/reading/*.md files.

Usage:
    python fetch-reviews.py              # interactive (opens browser)
    python fetch-reviews.py --headless   # uses saved auth state (requires prior --login)
    python fetch-reviews.py --dry-run    # show what would be updated without writing

Fetches the official Goodreads CSV export (which includes "My Review" column),
then patches matching markdown files in content/reading/.
"""
import csv
import io
import re
import sys
import time
from pathlib import Path

import frontmatter
from playwright.sync_api import sync_playwright

import config

GOODREADS_USER_ID = "116999306"
DRY_RUN = "--dry-run" in sys.argv
HEADLESS_MODE = "--headless" in sys.argv

if HEADLESS_MODE:
    config.HEADLESS = True


def _slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower())
    return s.strip("-")


def _title_key(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip().lower())


def _download_goodreads_export(page) -> str | None:
    """Navigate to Goodreads export and return CSV text."""
    export_url = f"https://www.goodreads.com/review_porter/export/{GOODREADS_USER_ID}/goodreads_export.csv"

    print(f"  Downloading Goodreads export from {export_url}")
    with page.expect_download() as dl_info:
        page.goto(export_url)

    try:
        download = dl_info.value
        # Save to temp path and read
        tmp = config.AUTH_DIR / "goodreads_export.csv"
        config.AUTH_DIR.mkdir(parents=True, exist_ok=True)
        download.save_as(str(tmp))
        print(f"  Downloaded to {tmp}")
        return tmp.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  ERROR downloading export: {e}")
        return None


def _parse_reviews(csv_text: str) -> dict[str, str]:
    """Parse CSV and return {title_key: review_text} for books with reviews."""
    reader = csv.DictReader(io.StringIO(csv_text))
    reviews = {}
    for row in reader:
        review = (row.get("My Review") or "").strip()
        if not review:
            continue
        title = (row.get("Title") or "").strip()
        if title:
            reviews[_title_key(title)] = review
    print(f"  Found {len(reviews)} books with reviews in Goodreads export.")
    return reviews


def _load_md_files() -> dict[str, Path]:
    """Return {title_key: path} for all reading markdown files."""
    result = {}
    for md_path in config.READING_DIR.glob("*.md"):
        try:
            post = frontmatter.load(str(md_path))
            title = str(post.metadata.get("title", "") or "")
            if title:
                result[_title_key(title)] = md_path
        except Exception as e:
            print(f"  Warning: could not parse {md_path.name}: {e}")
    return result


def _update_md_review(md_path: Path, review: str) -> bool:
    """Update the review field in frontmatter. Returns True if changed."""
    post = frontmatter.load(str(md_path))
    current = str(post.metadata.get("review", "") or "").strip()
    if current == review:
        return False

    if DRY_RUN:
        print(f"    [DRY RUN] Would set review in {md_path.name}:")
        print(f"    → {review[:80]}{'...' if len(review) > 80 else ''}")
        return True

    post.metadata["review"] = review
    md_path.write_text(frontmatter.dumps(post), encoding="utf-8")
    return True


def main():
    md_files = _load_md_files()
    print(f"  Loaded {len(md_files)} markdown files from content/reading/")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        if config.GOODREADS_AUTH.exists():
            ctx = browser.new_context(storage_state=str(config.GOODREADS_AUTH))
        else:
            ctx = browser.new_context()

        page = ctx.new_page()

        # Verify login
        page.goto("https://www.goodreads.com")
        page.wait_for_load_state("networkidle")

        logged_in = any(
            page.locator(sel).count() > 0
            for sel in [
                "nav.siteHeader__primaryNavInline",
                "[data-testid='userMenu']",
                ".dropdown__trigger--profileButton",
                ".personalNav",
            ]
        )

        if not logged_in:
            if config.HEADLESS:
                print("ERROR: Not logged in to Goodreads. Run: python sync.py --login")
                return
            print("Not logged in. Please log in manually in the browser, then press Enter...")
            input()

        csv_text = _download_goodreads_export(page)
        ctx.close()
        browser.close()

    if not csv_text:
        print("Failed to download Goodreads export.")
        return

    reviews = _parse_reviews(csv_text)

    updated = 0
    skipped = 0
    not_found = []

    for title_key, review in reviews.items():
        if title_key in md_files:
            changed = _update_md_review(md_files[title_key], review)
            if changed:
                updated += 1
                print(f"  {'[DRY RUN] ' if DRY_RUN else ''}Updated: {md_files[title_key].name}")
            else:
                skipped += 1
        else:
            not_found.append(title_key)

    print(f"\n{'[DRY RUN] ' if DRY_RUN else ''}Done.")
    print(f"  Updated: {updated} files")
    print(f"  Already up-to-date: {skipped} files")
    if not_found:
        print(f"  No matching MD file found for {len(not_found)} books:")
        for t in not_found[:10]:
            print(f"    - {t}")
        if len(not_found) > 10:
            print(f"    ... and {len(not_found) - 10} more")


if __name__ == "__main__":
    main()
