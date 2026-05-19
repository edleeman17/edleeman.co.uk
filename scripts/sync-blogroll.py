#!/usr/bin/env python3
"""
Sync blogroll.json from FreshRSS subscriptions.
Adds feeds present in FreshRSS but missing from blogroll.
Skips YouTube channels and self-referential feeds.

Usage:
  python3 scripts/sync-blogroll.py          # preview (dry run)
  python3 scripts/sync-blogroll.py --apply  # write changes to data/blogroll.json
"""

import json
import subprocess
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOGROLL_PATH = os.path.join(REPO_ROOT, "data", "blogroll.json")

FRESHRSS_CONTAINER = "freshrss"
FRESHRSS_DB = "/config/www/freshrss/data/users/admin/db.sqlite"

SKIP_DOMAINS = {"youtube.com", "edleeman.co.uk", "charityshot.co.uk"}
SKIP_TITLES  = {"FreshRSS releases", "Feed / Raindrop.io", "Ed Leeman",
                "Charity Shot Blog", "Charity Shot Feed"}


def get_freshrss_feeds():
    result = subprocess.run(
        ["docker", "exec", FRESHRSS_CONTAINER, "sqlite3",
         "-separator", "\t",
         FRESHRSS_DB,
         "SELECT name, url, website FROM feed ORDER BY name;"],
        capture_output=True, text=True, check=True
    )
    feeds = []
    for line in result.stdout.strip().splitlines():
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        title, feed_url, site_url = (p.strip() for p in parts)
        if any(d in feed_url or d in site_url for d in SKIP_DOMAINS):
            continue
        if title in SKIP_TITLES:
            continue
        feeds.append({"title": title, "feed_url": feed_url, "site_url": site_url})
    return feeds


def normalise(url):
    return url.rstrip("/").lower().replace("http://", "https://")


def load_blogroll():
    with open(BLOGROLL_PATH) as f:
        return json.load(f)


def find_missing(frss_feeds, blogroll):
    existing_feed = {normalise(e["feed_url"]) for e in blogroll["feeds"]}
    existing_site = {normalise(e["site_url"]) for e in blogroll["feeds"] if e["site_url"]}

    missing = []
    for f in frss_feeds:
        if normalise(f["feed_url"]) in existing_feed:
            continue
        if f["site_url"] and normalise(f["site_url"]) in existing_site:
            continue
        missing.append(f)
    return missing


def main():
    apply = "--apply" in sys.argv

    print("Fetching FreshRSS feeds via docker exec...")
    frss_feeds = get_freshrss_feeds()
    print(f"  {len(frss_feeds)} feeds (after skipping YouTube/self)")

    blogroll = load_blogroll()
    print(f"  {len(blogroll['feeds'])} feeds in blogroll.json")

    missing = find_missing(frss_feeds, blogroll)

    if not missing:
        print("Nothing to add — blogroll is up to date.")
        return

    print(f"\n{len(missing)} feeds missing from blogroll:")
    for m in missing:
        print(f"  + {m['title']}")
        print(f"    feed: {m['feed_url']}")
        print(f"    site: {m['site_url']}")

    if not apply:
        print("\nDry run — pass --apply to write changes.")
        return

    new_entries = [
        {
            "title": m["title"],
            "site_url": m["site_url"],
            "feed_url": m["feed_url"],
            "category": "",
            "favourite": False,
        }
        for m in missing
    ]

    blogroll["feeds"].extend(new_entries)
    blogroll["feeds"].sort(key=lambda e: e["title"].lower())

    with open(BLOGROLL_PATH, "w") as f:
        json.dump(blogroll, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\nWrote {len(missing)} new entries to {BLOGROLL_PATH}")
    print("Review: git diff data/blogroll.json")
    print("Commit: git add data/blogroll.json && git commit -m 'blogroll: sync from freshrss'")


if __name__ == "__main__":
    main()
