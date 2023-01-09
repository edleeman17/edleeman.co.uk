---
title: My Self Hosted Note Syncing Journey Once Switching to Iphone
slug: my-self-hosted-note-syncing-journey-once-switching-to-iphone
date: 2020-02-25T11:32:00.000Z
type: post
---



Recently moving to the iPhone meant that I had to re-think and re-design my existing note-taking solution, this is a quick writeup of my journey.

## My existing solution with Syncthing and VS Code

I **loved** my original solution. I had recently discovered [Syncthing](https://syncthing.net/) and got it set up on my self hosted solution in my loft. I had a central sync server and then a node on each of my devices, including my Huawei P20 Pro.

I could keep my extensive markdown nodes on every device and sync them without even thinking about it. It just worked, I wasn't tied into a service as the nodes are written in Markdown.

Everything just **worked**.

## Switching to iPhone

I made the switch to the iPhone due to privacy concerns with Android. I have recently boycotted all my Google services and switched over to a self-hosted solution. Part of this meant getting rid of my Android.

Everything started great with the iPhone, the interface is great, everything just works.

Apart from Syncthing.

There's currently no iOS client for Syncthing.

So what now? I started looking at other app alternatives, Bear, Markdown Notes, etc.. but all of them locked down where the files were saved on the iPhone, I couldn't access them from a file explorer on the iPhone. Something that could easily be done with Android.

Bumped into [Resilio](https://www.resilio.com/), not self-hosted, but achieves the whole decentralized syncing that I loved about Syncthing. Cool, I managed to get my notes syncing to a Resilio folder on my iPhone. Bingo!

But wait, what happens when I try and edit a note? It opens a *copy* of the note in a markdown app. Not ideal, I just want to view and edit notes, how hard can it be!

I give up.

## Standard Notes

I **had** a love-hate relationship with [Standard Notes](https://standardnotes.org/). I loved the UI, the syncing was pretty good, it has an iOS app! and it can be self-hosted, amazing.

But a lot of the features are paid. So if I wanted to write in Markdown, which I do, I had to pay for the extensions. I had to think to myself, how badly do I want notes on my iPhone?

I went without notes for a week, it nearly killed me. So I bit the bullet and settled for one month at £9.99, I thought I'd give it a try.

Loved it, I heavily use Markdown Basic, Simple Task Editor and Secure Spreadsheets extensions. But can I justify £10 a month?

## Standard Notes Extensions

Standard Notes being open-source meant that I could have a poke around in its git repository. I did a global search on Github for "Standard Notes" and I bumped into a repository by Github User [jonhadfield](https://github.com/jonhadfield/awesome-standard-notes) who has collected some awesome Standard Notes extensions. Browsing his `README.md` I spotted the repository [Extensions Repository Builder](https://github.com/iganeshk/standardnotes-extensions). This would allow me to self-host my extensions rather than paying the monthly fee!

I set up Extensions Repository Builder on my internal host and bingo, it just worked, amazing.

## Full E2E Sync

So after a very long journey of pulling my hair out and re-evaluating how much these notes meant to me. I finally had an end-to-end solution for storing my notes and syncthing between all of my devices.

## Where I'm going next

I have a [did.txt](https://theptrk.com/2018/07/11/did-txt-file/) file which I log to every day with what I did that day, it helps with our daily standups so that I can remember what I did the previous day. On [jonhadfield's](https://github.com/jonhadfield/awesome-standard-notes) Github, there was also a link for [standardnotes-fs](https://github.com/tannercollin/standardnotes-fs) which allows you to mount your Standard Notes as files using fuse. This means I can set up my did.txt command to edit my Did note.

I'd also like to hook up iOS reminders to a reminders section in Standard Notes. I own an Apple Watch and I tend to use Siri on it quite often. So I need to work out some way to sync these with my standard notes.
