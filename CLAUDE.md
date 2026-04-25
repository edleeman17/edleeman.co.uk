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
| Bookmarks | `content/links/` | `archetypes/links.md` |
| Book reviews | `content/reading/` | — |
| Static pages | `content/*.md` | — |

**Reading frontmatter:** `shelf` (read/currently-reading/to-read), `rating` (0-5), `favourite`, `review`, `date_read`, `goodreads_id`. Only `shelf: "read"` entries are syndicated.

**Links frontmatter:** `link` (external URL), `description`, `category`, `syndicate: true/false`. Only `syndicate: true` links get POSSE'd to Mastodon.

**Notes frontmatter:** supports `in_reply_to`, `like_of`, `repost_of`, `bookmark_of` → renders microformat classes.

### Layouts

- `layouts/partials/header.html` — `<head>`, nav, webmention links, analytics
- `layouts/partials/footer.html` — h-card (hidden), theme toggle, keyboard nav, webring links
- `layouts/page/reading.html` — Reading page (pulls from `data/books.json`)
- `layouts/post/`, `layouts/note/` — single content-type templates with h-entry microformats

### Data

- `data/books.json` — source of truth for all book data (favourites, read, currently-reading, tbr). **Do not overwrite from Goodreads** — it syncs outward only.
- `data/tbr_curated.json` — curated TBR categorised into aligned/risky/not-aligned.

### Book sync (`scripts/book-sync/`)

Python + Playwright pipeline. Reads `data/books.json`, generates per-platform CSVs, uploads to Goodreads and Fable. Auth state stored in `~/.config/book-sync/`. Sync state tracked in `scripts/book-sync/last_synced.json`.

### IndieWeb / POSSE pipeline

**Receiving:** webmention.io endpoint in header. JS on post/note pages fetches and displays webmentions.

**Sending webmentions:** `.github/workflows/send-webmentions.yml` — triggers on push to `content/posts/`, `content/notes/`, `content/links/`. Sends via webmention.app.

**POSSE workflows** (all write `syndication:` URLs back into content frontmatter and git-push):

| Workflow | Triggers on | Platforms |
|----------|-------------|-----------|
| `post-to-mastodon.yml` | posts, notes, links, reading | fosstodon.org |
| `post-to-bluesky.yml` | posts, notes, reading | bsky.app |
| `post-to-threads.yml` | posts, notes, reading | threads.net |

- Posts: `"New Post: {title}\n\n{excerpt}\n\n{url}"` (500-char limit, excerpt truncated dynamically)
- Notes: body excerpt + URL; images uploaded as media attachments on Mastodon
- Links: `"🔖 {title}\n\n{description}\n\n{external_url}\n\nvia {site_url}"` — Mastodon only
- Reading (finished): `"📚 \"{title}\" by {author} — ★★★☆☆\n\n{review}\n\n{url}"`
- Bluesky: 300-char limit; Threads: two-step (create container → publish)
- Skip logic: already has platform URL in frontmatter (`bsky.app`, `threads.net`) or `syndicate: false`

**Post URL derivation:** posts use Hugo's `:title` permalink (slugified title); other content uses `slug` frontmatter or file path.

**Microformats:** h-card in footer (hidden), h-entry on posts/notes/links, u-bookmark-of on links.

**Bridgy Fed** connected to `@edphones@fosstodon.org` for ActivityPub backfeed.

### Required GitHub secrets

- `MASTODON_ACCESS_TOKEN` — fosstodon.org API token
- `WEBMENTION_APP_TOKEN` — webmention.app token
- `BLUESKY_HANDLE` + `BLUESKY_APP_PASSWORD` — Bluesky AT Protocol auth
- `THREADS_USER_ID` + `THREADS_ACCESS_TOKEN` — Meta Threads API (60-day token, needs periodic refresh)
