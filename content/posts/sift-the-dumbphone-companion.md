---
title: "Sift: The Dumbphone Companion"
date: 2026-02-20T00:00:00Z
type: "post"
draft: false
---

## The Problem

My phone was ruining my concentration.

Not dramatically - I wasn't doomscrolling for hours. But the constant little interruptions were fragmenting my focus. A Discord ping here, a promotional email there, someone reacting to something in a group chat. Each one tiny, but collectively they meant I never got more than twenty minutes of unbroken thought.

So I bought a dumbphone.

## The Dumbphone Experiment

I'd been watching [Ben Vallack's videos](https://github.com/benvallack) about intentional tech use and minimal computing for a while. His approach to stripping things back to essentials got me thinking.

The idea is simple: leave the smartphone at home (or in a drawer), carry a basic phone instead. No apps, no notifications, no temptation to "quickly check" anything. Just calls and texts.

It works brilliantly for focus. But there's an obvious problem: what if something actually important happens?

My mum sends a WhatsApp asking me to call her urgently. A delivery driver can't find my house. The bank texts a fraud alert. My server's on fire.

I needed a filter. Something that would watch my iPhone, decide what was genuinely important, and forward only those messages to my dumbphone via SMS.

So I built Sift.

## What It Does

The system captures every notification from my iPhone, runs it through a rule engine, and forwards the important ones to my dumbphone.

```
iPhone → Bluetooth → Raspberry Pi → Processor → SMS to dumbphone
```

The Pi connects to my iPhone via Bluetooth Low Energy using Apple's ANCS (Apple Notification Center Service). Every notification that would normally appear on the iPhone gets sent to the Pi instead.

The processor then decides what to do with each notification:

- **Send** - Forward immediately (messages from family, verification codes, etc.)
- **Drop** - Ignore completely (group chats, marketing, social media)
- **Ask AI** - Let a local LLM decide for ambiguous cases

Finally, important notifications get forwarded via Twilio SMS, ntfy, Bark, or iMessage - whatever suits your setup.

## Rules

The rule engine is the core of it. YAML config, nothing fancy:

```yaml
apps:
  whatsapp:
    default: drop
    rules:
      - sender_contains: "Mum"
        action: send
      - sender_contains: "Dad"
        action: send
      - body_contains: "urgent"
        action: send

  gmail:
    default: drop
    rules:
      - body_regex: "(verification|security) code"
        action: send

  discord:
    default: drop
    rules:
      - sender_contains: "@ed"
        action: send
```

Global rules apply everywhere - useful for verification codes and VIP contacts. App-specific rules handle the rest. Unknown apps get dropped by default.

## Sentiment Detection

Here's the interesting bit. Sometimes a message that should be dropped is actually urgent.

Your mate usually sends memes and banter - so you drop WhatsApp from him. But what if he texts "I'm at A&E can you call me"? That's clearly urgent, and the rules would miss it.

So I added sentiment detection. Messages that match a drop rule get a final check: is this actually urgent? The LLM scans for genuine emergencies - not just the word "urgent" (which people overuse), but actual distress signals.

This catches maybe one or two messages a week that would otherwise slip through. Worth it.

## The SMS Assistant

Once I had the Pi running, I realised I could go further. Why not let the dumbphone send commands back?

Text "WEATHER" to my iPhone number, and a script on my Mac checks the forecast and replies via SMS. Text "TODO" and it reads my task list from Obsidian. Text "PING" and it checks whether the Pi is still connected to my iPhone.

It's become surprisingly useful:

```
Me:  BRIEFING
Bot: Friday 20 February
     12C, 0% rain
     3 TODOs. First: Call dentist
     BIN: Tuesday black waste

Me:  REMIND 3pm call dentist
Bot: Reminder set for 15:00

Me:  CALL dad
Bot: Dad: +44**********

Me:  NAV home to kings cross
Bot: Getting directions...
     5.1km, ~15 min via A1
     Head north through Islington...
```

There's something satisfying about texting your phone and getting useful information back. Feels a bit like having a personal assistant from the early 2000s.

## Hardware Requirements

**Required:**
- Raspberry Pi (any model with Bluetooth - I use a Pi Zero W)
- iPhone (any version with Bluetooth LE)
- Mac (for sending/receiving SMS via iMessage)
- A dumbphone (I use a T185 4G)

**Optional:**
- Ollama for AI features (7B model runs fine on an M1 Mac)

The clever bit: the Mac can send and receive SMS through iMessage. So notifications go iPhone → Pi → Mac → SMS to dumbphone. And when you text back from the dumbphone, the Mac receives it via iMessage and the SMS assistant processes your commands. No Twilio account needed.

The Pi needs to stay within Bluetooth range of your iPhone - about 10 metres. I leave both on my desk at home. The iPhone stays plugged in, and the Pi forwards everything to wherever I am.

## Does It Actually Work?

Yeah. I've been running it for a few months now.

The filtering is good enough that I trust it. I've missed maybe three messages that I'd have wanted - and caught dozens of urgent ones that would've been dropped by simple app-level filtering.

The latency is about 2-3 seconds from iPhone notification to SMS received. Good enough for anything that matters.

Battery on the iPhone lasts forever when you're not actually using it. The dumbphone goes a week between charges. The Pi draws maybe 1W.

## Who Is This For?

Honestly, a pretty small group:

1. **People doing serious dumbphone experiments** - You want to reduce smartphone dependency but can't completely disconnect
2. **On-call engineers** - Filter out noise, escalate real alerts to SMS
3. **Parents of teenagers** - Only get notified for important contacts, ignore the meme spam
4. **Anyone who's tried "Do Not Disturb" and found it too blunt**

It's not for everyone. Setting up Bluetooth ANCS on a Pi takes some patience. The filtering rules need tuning. But if you're the kind of person who self-hosts things and enjoys solving this sort of problem, it's a fun project.

## What's Next

I'm working on an Android version. Should be simpler - Android actually has APIs for this, so no Bluetooth bridge needed. The app captures notifications locally and forwards them directly.

Also thinking about smarter rules - learning from feedback, maybe clustering similar notifications to reduce noise.

## Try Sift

The whole thing is open source:

**GitHub:** https://github.com/edleeman17/sift

Fair warning: this is a personal project that works for me, but Bluetooth can be temperamental and I can't guarantee notifications will always arrive. Test it properly before relying on it for anything important. If you miss something critical, that's on you. Everything is configurable though - the example rules are just how I use it. Edit `config.yaml` to match your own contacts and priorities.

If you try it, let me know how it goes. Always interested to hear how other people configure their filters.
