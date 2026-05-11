---
title: "Ingest"
description: "Capture actionable messages from anywhere — Discord, iOS share sheet, any HTTP client — into a self-hosted todo list. Ollama summarisation and Tesseract OCR optional."
github: "https://github.com/edleeman17/ingest"
language: "Python"
stars: 0
status: "active"
---
![Ingest PWA screenshot](https://raw.githubusercontent.com/edleeman17/ingest/main/docs/screenshot.jpg)


Messages worth acting on arrive from everywhere — Discord DMs, Signal, iMessage, screenshots of things on screen — and most of them vanish before you act on them. Ingest is a self-hosted capture layer that funnels all of it into one place.

Send text or images via the iOS share sheet, forward a Discord message to a watched channel, POST from any script or LAN service, or type directly into the PWA. Everything lands in SQLite and surfaces in a mobile-first todo list: filter by source or status, drag items into named groups, reorder within groups, check things off.

Ollama summarisation and Tesseract OCR are both optional — configure them if you have them, skip them if you don't. Without Ollama, raw text is stored as-is. The only hard requirement is Docker.

**Tech:** Python, FastAPI, SQLite, Vanilla JS PWA, Docker — Tesseract OCR + Ollama + discord.py optional
