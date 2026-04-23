# edleeman.co.uk TODO

## Notes → Status Updates
- [x] Update archetype `archetypes/notes.md` — status-update style, `syndication: []`, no title template
- [x] Move existing long-form notes to `content/posts/` with `aliases` for old URLs
- [x] `new-pages-on-the-site.md` kept as note (already status-update style)
- [ ] Update `layouts/note/` list template to reflect status-style display (compact, no title required)

## Mastodon Syndication (Notes)
- [x] `.github/workflows/post-to-mastodon.yml` already covers `content/notes/**`

## Bluesky Syndication
- [x] Created `.github/workflows/post-to-bluesky.yml` (AT Protocol, curl-based)
- [ ] Add GitHub secrets: `BLUESKY_HANDLE` (e.g. `edleeman.bsky.social`) + `BLUESKY_APP_PASSWORD`
- [ ] Test: push new post → check Bluesky + syndication URL written back

## Threads Syndication
- [x] Created `.github/workflows/post-to-threads.yml` (Threads Graph API)
- [ ] Add GitHub secrets: `THREADS_USER_ID` + `THREADS_ACCESS_TOKEN` (long-lived, 60-day)
- [ ] Note: access token needs periodic refresh (or automate with cron workflow)
- [ ] Test: push new post → check Threads + syndication URL written back

## human.json
- [x] Created `/static/human.json` (author, site purpose, colophon, IndieWeb, AI declaration link)
- [x] Added `<link rel="human">` to `layouts/partials/head.html`
- [x] Linked from footer

## AI Declaration
- [x] Created `content/ai-declaration.md`
- [x] Linked from footer + human.json
