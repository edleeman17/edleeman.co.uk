---
title: "Foundation Cram"
description: "Free revision app for the UK amateur radio Foundation exam. Drills your weak spots, runs timed mock exams and estimates your chance of passing. Runs in the browser, no sign-up."
website: "https://edleeman.co.uk/ham/"
github: "https://github.com/edleeman17/foundation-cram"
language: "JavaScript"
stars: 0
status: "active"
---

I built this to revise for my own Foundation exam, and passed with 22 out of 26. [More on that here](/posts/foundation-cram/).

It's 238 questions checked against the Foundation column of the RSGB syllabus, so nothing from the Intermediate level sneaks in. It keeps track of which topics you're losing marks on and serves you more of those. There are 26-question mock exams with the real 60 minute timer, flashcards, and an estimate of your chance of passing that goes up as you improve.

In the exam you get a four page reference booklet called EX307, and a lot of answers are on it. After each question the app tells you which page and row to look at, so by exam day you know your way round it.

Your progress stays in your own browser. There's no account. You can download a backup file and restore it on another device.

**Tech:** Vanilla JS, single HTML file, localStorage, optional nginx + Docker for syncing between devices
