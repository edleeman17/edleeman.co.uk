---
title: "MeshCore Companion"
description: "A self-hosted web app for MeshCore LoRa radios: a Raspberry Pi holds the Bluetooth link, and any phone or laptop gets chat, push notifications, repeater admin and proper signal stats."
github: "https://github.com/edleeman17/meshcore-companion"
language: "Python"
stars: 0
status: "active"
---

I got into [MeshCore](https://meshcore.io), the off-grid LoRa mesh where people text each other through a chain of solar repeaters with no phone network. A companion radio only pairs with one phone at a time, though, and the official app tells you very little about *why* a message didn't get through.

MeshCore Companion moves the radio onto a Raspberry Pi. The Pi keeps the Bluetooth link open around the clock, saves every message, and serves an installable web app. Any device on my network can chat through it, and my phone gets push notifications even when the app is closed.

Most of the work went into answering "did my message actually go out?" Every received message shows its signal strength and hop count, colour-coded. Channel posts count how many repeaters echoed them back. A failed DM tells you whether it reached the mesh but got no receipt, or never left. A link-health card tracks the error rate, the noise floor, and your airtime against the 10% legal duty cycle.

There's also repeater admin (status, telemetry, a CLI console, and trace in both directions), plus a map and a "nearby now" list. It can even discover hashtag channels: their name *is* their encryption key, so it tests likely names against packets it hears until one verifies.

**Tech:** Python, FastAPI, Bluetooth LE (BlueZ/bleak), meshcore_py, SQLite, Server-Sent Events, Web Push, vanilla JS PWA, Raspberry Pi
