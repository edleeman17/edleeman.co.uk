---
title: "I passed my Foundation (and the app I built to get there)"
date: 2026-11-19T14:02:06Z
type: "post"
draft: false
slug: "foundation-cram"
syndication:
  - "https://fosstodon.org/@edphones/117643474552968103"
  - "https://bsky.app/profile/edleeman.co.uk/post/3n2oafiqvsj2q"
---

I passed my amateur radio Foundation exam yesterday. 22 out of 26, with 19 needed to pass. My callsign is in the post - the paper kind - so for now I still just listen.

I've had a Quansheng UV-K5 sat on my desk since October, receive only. I'd been listening to the Thursday night net from the loft for weeks, unable to say anything back. That got old fast.

## The problem

The Foundation exam is 26 multiple choice questions in an hour. You need 19 to pass. It's not hard, but it's broad - licence conditions, a bit of Ohm's law, antennas, propagation, interference, safety. Lots of small facts that are easy to half-know.

I'm bad at revising from a book. I read a page, nod along, then can't remember any of it a day later. What works for me is being asked questions over and over until the wrong answers stop happening.

So I built an app.

## What it does

It's called Foundation Cram. A single web page, no sign-up, works on your phone.

- **Cram weak spots** - serves you the questions you keep getting wrong, weighted towards your worst topics
- **Mock exam** - 26 questions split by topic like the real paper, with a 60 minute timer
- **Flashcards** - for the bus
- **Everything mode** - every question once, then it loops the ones you missed until you get them right
- **Pass likelihood** - a rough percentage chance of you scoring 19 or more, and which topic is costing you the most marks

That last one ended up being the most useful bit. Seeing "62% chance of passing, most marks to gain: Licence conditions" told me exactly where to spend my evening. Watching it creep up over a few weeks was oddly motivating.

## The EX307 trick

In the exam you get a four page reference booklet called EX307. Band plans, frequencies, the wavelength chart, that sort of thing. A surprising number of questions are answered by it, if you know where to look.

So after each question the app tells you if the answer is on the sheet, and which page and row. There's a hint button too, so you can practise finding it before you answer. By exam day I knew my way round that booklet, which saved a lot of panic.

## The bit I got wrong

My first version of the question bank had around 60 questions that weren't even Foundation level. Q-codes, for example. I'd assumed they'd be on it. They're not - that's Intermediate.

I went back through every question against the Foundation column of the RSGB syllabus and binned anything that didn't belong. Worth doing if you're revising from random internet question banks too. A lot of them mix the levels up.

## Try it

It's free at [edleeman.co.uk/ham](/ham/).

Your progress stays in your own browser. Nothing gets sent anywhere and there's no account. The catch is that if you clear your browser data, it's gone - so there's a button to download a backup file, and you can restore it on another phone or laptop. On an iPhone, add it to your home screen, otherwise Safari can clear it if you don't visit for a week.

It doesn't include the RSGB's own mock papers or the EX307 sheet, as those are theirs. Grab them from the [RSGB mock exams page](https://rsgb.org/mock-exams) and do them as well. They're the closest thing to the real exam.

The code is on [GitHub](https://github.com/edleeman17/foundation-cram) if you want to run your own copy or spot a wrong answer. Open an issue and I'll fix it.

Now to actually press the transmit button.
