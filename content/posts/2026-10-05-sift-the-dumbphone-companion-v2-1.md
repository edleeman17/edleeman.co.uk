---
title: "Sift: The Dumbphone Companion v2.1"
date: 2026-10-05T10:07:45+01:00
draft: false
type: "post"
slug: "sift-the-dumbphone-companion-v2-1"
description: "Sift no longer needs a Raspberry Pi. A £5 ESP32 now listens for iPhone notifications - and fixing it taught me why the Pi version never really stayed connected either."
syndication:
  - "https://fosstodon.org/@edphones/117387536976719280"
  - "https://bsky.app/profile/edleeman.co.uk/post/3mx4lcjzbql2w"
---

# Sift: The Dumbphone Companion v2.1

## The Problem

v2 got rid of the Mac. This one makes the Pi optional.

The Raspberry Pi Zero was always the fragile part of Sift. Its whole job is to sit near my iPhone, listen for notifications over Bluetooth and pass them on - but to do that it needed an SD card, a Linux Bluetooth stack, three systemd services and a watchdog whose only purpose was keeping the other three alive.

I had two [ESP32 boards](https://www.amazon.co.uk/s?k=ESP32+WROOM-32+development+board&tag=ismypassportv-21) sat in a drawer doing nothing. So the question became: can a £5 microcontroller do the Pi's job?

## ESP32 vs Pi

Quick detour, because I didn't really know when to pick one over the other before this.

A Pi Zero is a small Linux computer. An ESP32 is a microcontroller - no operating system, half a megabyte of RAM, one program that boots in under a second and doesn't care if you pull the plug on it.

My rule of thumb now:

- **ESP32** if the job fits in one sentence and moves tiny bits of data - a sensor, a button, a Bluetooth bridge, a small screen.
- **Pi** if it needs a USB device, files, big libraries like ffmpeg, or several jobs at once.

"Listen for iPhone notifications and POST them somewhere" is about as one-sentence as it gets.

## What Actually Worked

```
iPhone → Bluetooth → ESP32 → Processor → SMTP → Email → iPhone → Shortcut → Dumbphone
```

The ESP32 does exactly what the Pi did, and nothing else. It pairs with the iPhone over Bluetooth Low Energy, subscribes to Apple's ANCS (Apple Notification Center Service), and POSTs each notification to the processor as the same JSON the Pi used to send. It even serves the same `/health` endpoint, so the dashboard, the battery alerts and the `PING` command didn't need changing - I just pointed them at a new IP.

`RESET` got simpler too. On the Pi it SSHed in and restarted the Bluetooth stack. Now it's an HTTP POST that reboots the board, which takes about a second.

Setup is a firmware flash, a WiFi hotspot on first boot to type your WiFi password into, and one pairing. Updates after that go over WiFi - I haven't needed the USB cable since.

## The iPhone Doesn't Want To Talk To It

The first problem: it doesn't show up in Settings → Bluetooth.

The Pi did, because the Pi also speaks "classic" Bluetooth. The ESP32 is Bluetooth LE only, and iOS won't list an LE gadget there until it's been paired once. The workaround is a free app called nRF Connect - scan, connect, pair, allow notifications. After that it appears in Settings like anything else and iOS remembers it.

## The Link Kept Dropping

Once it was paired, it dropped the connection every 10 to 40 seconds. Every time.

My first assumption was a cheap board with a weak radio. Then I went back through the Pi's logs and found it had been doing exactly the same thing all along - 220 disconnects in a single afternoon and evening. It just never surfaced, because the Pi quietly reconnected and nobody was watching.

~~The cause turned out to be one number.~~ iOS gives a Bluetooth connection about 0.7 seconds of silence before it calls it dead. On an ESP32, WiFi and Bluetooth share the same radio, so the odd gap longer than that is inevitable. The fix is to ask the iPhone - politely, within Apple's published limits - for a 5 second timeout instead. iOS accepted it, ~~and the constant dropping stopped~~.

**Update, later the same day:** it hadn't stopped. The timeout helped, but the link still dropped every few seconds, and after enough failed reconnects iOS gave up trying altogether. I moved the board, gave it its own power, and started eyeing up my AirPods. Then I ran it for ten minutes with WiFi switched off - zero drops, with AirPods streaming the whole time. That shared radio wasn't causing the odd gap, it was the whole problem: WiFi was starving Bluetooth. Putting WiFi into its deepest power-save mode, so it only wakes every 300ms or so, fixed it - zero drops in fifteen minutes with WiFi on. The Pi's chip shares its radio the same way, which is probably where its 220 disconnects came from too. That's [v2.1.1](https://github.com/edleeman17/Sift/releases/tag/v2.1.1).

## Only The iPhone Can Call

The other thing I learned: with Bluetooth LE, only the iPhone can start a connection. The bridge can advertise "I'm here" as loudly as it likes, but it can't ring the phone.

The Pi version had a watchdog that tried anyway, running `bluetoothctl connect` every few seconds. I checked its logs. Nine and a half thousand attempts in six days. Successful connections: zero. Every reconnect it ever had was iOS deciding to come back on its own.

So the ESP32 does what Apple recommends instead - advertise fast for 30 seconds after a drop, then slow down. The phone usually comes back within 2 to 7 seconds. After you've been out of the house for a while, iOS sometimes gives up and needs a tap on the device in Settings. Same as the Pi, just more honest about it.

The way commercial gadgets (watches, fitness trackers) get around this is a companion app on the phone that tells iOS "keep reconnecting to this forever". I'm not writing an iOS app for this.

## Hardware Requirements

You now get a choice of bridge. Both send the processor exactly the same thing, so nothing else in Sift cares which one you pick.

- **ESP32** - a [classic ESP32 dev board](https://www.amazon.co.uk/s?k=ESP32+WROOM-32+development+board&tag=ismypassportv-21) (ESP32-WROOM-32 style - mine was about £5). Pick this if all you want is the bridge.
- **Raspberry Pi** - [Zero 2 W](https://www.amazon.co.uk/s?k=Raspberry+Pi+Zero+2+W&tag=ismypassportv-21) or anything newer. Pick this if you already have one, or want it doing other jobs too. Mine streams vinyl now.

**Required:**
- One of the above
- iPhone (any version with Bluetooth LE)
- A dumbphone (I use a [T185 4G](https://www.amazon.co.uk/dp/B0FG7T2MS3?tag=ismypassportv-21))
- Somewhere to run the processor - any machine that runs a container

If you go with the ESP32, keep it within a few metres of wherever your phone usually lives. ~~One shared radio doesn't have much range to spare.~~ Range turned out not to be the problem (see the update above), but closer doesn't hurt.

## Try It

~~Tagged as v2.1.0, with the firmware in `esp32-bridge/`: [github.com/edleeman17/Sift/releases/tag/v2.1.0](https://github.com/edleeman17/Sift/releases/tag/v2.1.0)~~

**Update:** grab [v2.1.1](https://github.com/edleeman17/Sift/releases/tag/v2.1.1) instead - same firmware plus the WiFi fix.

If you're already running the Pi version, there's no rush to switch. If you do, the ESP32 starts with forwarding off, so you can run both side by side and check it's catching everything before you turn the Pi off.

Same fair warning as before: this is a personal project that works for me, not a product. Test it before you rely on it.
