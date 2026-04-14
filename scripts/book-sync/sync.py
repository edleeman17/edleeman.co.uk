#!/usr/bin/env python3
"""Book sync: generate CSV from books.json and push to Goodreads and Fable.

Usage:
    python sync.py                  # sync to all platforms (interactive)
    python sync.py --headless       # sync to all platforms (unattended/cron)
    python sync.py --seed           # first run: mark existing books as synced
    python sync.py goodreads        # sync to Goodreads only
    python sync.py fable            # sync to Fable only
    python sync.py --generate-only  # just generate the CSV, don't upload
    python sync.py --login          # open browsers to log in and save auth
"""
import sys
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright

import config
import generate_csv
import goodreads
import fable

SEED_EXISTING = False

ALL_PLATFORMS = ["goodreads", "fable"]


def do_login():
    """Open each platform in a browser for manual login, save auth state."""
    with sync_playwright() as p:
        print("\n=== Logging in to platforms ===\n")

        print("[Goodreads]")
        ctx = goodreads.get_context(p)
        page = ctx.new_page()
        goodreads.ensure_logged_in(page)
        goodreads.save_auth(ctx)
        ctx.close()

        print("\n[Fable]")
        ctx = fable.get_context(p)
        page = ctx.new_page()
        fable.ensure_logged_in(page)
        fable.save_auth(ctx)
        ctx.close()

        print("\nAuth saved for all platforms.")


def _setup_logging():
    """Set up file logging for headless/cron runs."""
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = config.LOG_DIR / f"sync-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )
    return log_file


def do_sync(platforms: list[str]):
    """Generate per-platform CSVs and upload only new/changed books."""
    if config.HEADLESS:
        log_file = _setup_logging()
        logging.info(f"Headless sync started. Log: {log_file}")

    with sync_playwright() as p:
        if "goodreads" in platforms:
            print("\n=== Syncing to Goodreads ===\n")
            csv_path, count = generate_csv.generate(
                platform="goodreads", seed_existing=SEED_EXISTING
            )
            if count == 0:
                print("  Nothing new for Goodreads.")
            else:
                ctx = goodreads.get_context(p)
                page = ctx.new_page()
                if goodreads.ensure_logged_in(page):
                    goodreads.import_csv(page, csv_path)
                    goodreads.save_auth(ctx)
                else:
                    print("  SKIP: Goodreads (not logged in)")
                ctx.close()

        if "fable" in platforms:
            print("\n=== Syncing to Fable ===\n")
            csv_path, count = generate_csv.generate(
                platform="fable", seed_existing=SEED_EXISTING
            )
            if count == 0:
                print("  Nothing new for Fable.")
            else:
                ctx = fable.get_context(p)
                page = ctx.new_page()
                if fable.ensure_logged_in(page):
                    fable.import_csv(page, csv_path)
                    fable.save_auth(ctx)
                else:
                    print("  SKIP: Fable (not logged in)")
                ctx.close()

    print("\n=== Done ===")


def main():
    args = sys.argv[1:]

    global SEED_EXISTING

    if "--headless" in args:
        config.HEADLESS = True
        args.remove("--headless")

    if "--seed" in args:
        SEED_EXISTING = True
        args.remove("--seed")

    if "--login" in args:
        do_login()
        return

    if "--generate-only" in args:
        platforms = [a for a in args if a in ALL_PLATFORMS] or ALL_PLATFORMS
        for plat in platforms:
            generate_csv.generate(platform=plat, seed_existing=SEED_EXISTING)
        return

    # Filter to requested platforms, or all
    platforms = [a for a in args if a in ALL_PLATFORMS] or ALL_PLATFORMS
    do_sync(platforms)


if __name__ == "__main__":
    main()
