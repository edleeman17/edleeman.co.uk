---
title: "Vinyl Companion"
description: "Play records on Sonos with a now-playing screen: auto-play on needle drop, lossless streaming, song recognition, synced lyrics and retro VU meters."
github: "https://github.com/edleeman17/vinyl-companion"
language: "Python"
stars: 0
status: "active"
---

![Vinyl Companion: spinning record with synced lyrics, VU meters and the About panel](https://raw.githubusercontent.com/edleeman17/vinyl-companion/main/docs/demo.gif)

My turntable plays through an app on an old iPad, and every session started with picking the Sonos outputs again. Vinyl Companion replaces that. Drop the needle and the chosen rooms start playing by themselves, and a quiet five minutes after the side ends they stop.

A Raspberry Pi at the turntable captures the record as lossless FLAC and a small server relays it to the Sonos. Shazam identifies the first song, then it follows the album's vinyl tracklist from Discogs, side by side, re-checking only when something looks off. Compilations are spotted and handled too.

The now-playing page is built for an iPad on a stand: a spinning record with the cover as its label, synced lyrics, a retro VU meter view, credits and your play counts. It also measures the turntable's real speed from every song it hears, which is how I found mine running 2.7% fast.

**Tech:** Python, FastAPI, ffmpeg, SoCo (Sonos), Shazam, Discogs, Last.fm, LRCLIB, Raspberry Pi, Docker
