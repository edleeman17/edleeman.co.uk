---
title: "Ingest"
description: "Capture actionable messages from anywhere — Discord, iOS share sheet, screenshots — into a LAN-hosted, AI-summarised todo list. No cloud. No API key."
github: "https://github.com/edleeman17/ingest"
language: "Python"
stars: 0
status: "active"
---

Messages worth acting on arrive from everywhere — Discord DMs, Signal, iMessage, screenshots of things on screen. Ingest is a self-hosted capture layer that turns them into a searchable, groupable todo list.

Drop anything in via the iOS share sheet, forward a Discord message to a watched channel, or POST from any LAN service. Tesseract OCRs screenshots locally. A local Ollama model summarises the content into a one-line action and adds tags — no API key, no external calls.

Everything lands in SQLite and surfaces in a mobile-first PWA: filter by source or status, drag items into groups, reorder within groups, check things off. Installable on iPhone as a home screen app over WireGuard.

**Tech:** Python, FastAPI, SQLite, Tesseract OCR, Ollama, discord.py, Vanilla JS PWA, Docker
