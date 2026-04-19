# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Build site + run pagefind search indexer
make build

# Local dev server at http://localhost:1313
make serve

# Book sync: push new reads to Goodreads + Fable
cd scripts/book-sync && python sync.py
cd scripts/book-sync && python sync.py --headless     # cron/unattended
cd scripts/book-sync && python sync.py --login        # save auth via browser
cd scripts/book-sync && python sync.py goodreads      # single platform
```

## Architecture

Hugo static site. Build runs in Docker (`klakegg/hugo:ext-alpine`). Source of truth for all data lives in the repo — no external CMS.

### Content types

| Type | Directory | Archetype |
|------|-----------|-----------|
| Blog posts | `content/posts/` | `archetypes/posts.md` |
| Short notes | `content/notes/` | `archetypes/notes.md` |
| Bookmarks | `content/links/` | — |
| Static pages | `content/*.md` | — |

### Layouts

- `layouts/partials/header.html` — `<head>`, nav, webmention links, analytics
- `layouts/partials/footer.html` — h-card (hidden), theme toggle, keyboard nav, webring links
- `layouts/page/reading.html` — Reading page (pulls from `data/books.json`)
- `layouts/post/`, `layouts/note/` — single content-type templates with h-entry microformats

### Data

- `data/books.json` — source of truth for all book data (favourites, read, currently-reading, tbr). **Do not overwrite from Goodreads** — it syncs outward only now.
- `data/tbr_curated.json` — curated TBR categorised into aligned/risky/not-aligned.

### Book sync (`scripts/book-sync/`)

Python + Playwright pipeline. Reads `data/books.json`, generates per-platform CSVs, uploads to Goodreads and Fable. Auth state stored in `~/.config/book-sync/`. Sync state (what's been uploaded) tracked in `scripts/book-sync/last_synced.json`.

### IndieWeb / POSSE pipeline

**Receiving:** webmention.io endpoint in header. JS on post/note pages fetches and displays webmentions.

**Sending webmentions:** `.github/workflows/send-webmentions.yml` — triggers on push to `content/posts/`, `content/notes/`, `content/links/`. Sends via webmention.app.

**Mastodon POSSE:** `.github/workflows/post-to-mastodon.yml` — triggers on new files in the same paths. Posts to `fosstodon.org/@edphones`. Writes back a `syndication:` URL into the frontmatter after posting. Link posts use `🔖 Title / description / external URL / via {site-url}` format; posts/notes use `Title\nURL`.

**Microformats:** h-card in footer (hidden), h-entry on posts/notes/links, u-bookmark-of on links. Notes support `in_reply_to`/`like_of`/`repost_of`/`bookmark_of` frontmatter → microformat classes.

**Bridgy Fed** connected to `@edphones@fosstodon.org` for ActivityPub backfeed.

### Required GitHub secrets

- `MASTODON_ACCESS_TOKEN` — fosstodon.org API token
- `WEBMENTION_APP_TOKEN` — webmention.app token
