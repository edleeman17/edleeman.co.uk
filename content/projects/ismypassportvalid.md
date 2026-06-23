---
title: "Is My Passport Valid?"
description: "Instant YES or NO on whether a UK passport meets the destination country's entry rules. Curated gov.uk rules plus a live gov.uk proxy for the long tail."
website: "https://ismypassportvalid.co.uk"
github: "https://github.com/edleeman17/ismypassportvalid"
language: "TypeScript"
stars: 0
status: "active"
---

Post-Brexit passport validity rules are a mess. Many countries want at least three or six months left on the day you travel, some count from your entry date, others from your exit date, and a few still treat the old ten year plus extension passports differently. Getting it wrong means being turned away at check-in.

This tool gives a plain YES or NO. Enter your passport's issue and expiry dates and pick a destination, and it tells you whether you can travel, with the rule it applied and a link to the relevant gov.uk page.

A curated rule set covers the common destinations. For everything else it proxies the live gov.uk foreign travel advice so answers stay current without manual updates.

**Tech:** Vanilla JS, Vite, gov.uk data source, Docker, nginx
