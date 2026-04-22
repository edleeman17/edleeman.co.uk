---
title: "Obsidian Live Sync Backup"
description: "Headless backup tool that extracts notes directly from CouchDB, decrypts them, and creates daily zip archives — no Obsidian installation required."
github: "https://github.com/edleeman17/Obsidian-Live-Sync-Backup"
language: "TypeScript"
stars: 0
status: "active"
---

If you use the [Obsidian Live Sync](https://github.com/vrtmrz/obsidian-livesync) plugin, your notes live in CouchDB — but getting them out without running Obsidian itself is non-trivial.

This tool connects directly to the CouchDB instance, decrypts the notes using your Live Sync credentials, and produces daily zip archives. Designed to run headlessly in a cron job or Docker container.

**Tech:** TypeScript, CouchDB, end-to-end encryption
