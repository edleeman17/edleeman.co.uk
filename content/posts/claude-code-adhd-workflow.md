---
title: "Teaching Claude Code to Work With My ADHD Brain"
date: 2026-03-04T00:00:00Z
type: "post"
draft: false
---

## The Problem

I have ADHD and I'm a software engineer. This is a famously difficult combination.

Not because the work is too hard. If anything, solving complex problems is where ADHD brains shine. The difficulty is everything around the work: remembering what you were doing after a context switch, not getting derailed by a tangent, knowing which of your five in-flight tasks to work on next, resisting the urge to "quickly" fix something unrelated.

I spend more mental energy managing my attention than doing actual engineering. And every time I context switch (a Slack message, a PR review request, lunch) I lose the thread and have to rebuild it from scratch.

So I trained Claude Code to be my external brain.

## The Idea

Claude Code has a file called `CLAUDE.md` in each project. It's meant for project-specific instructions like "use tabs not spaces" or "run tests with pytest".

But I realised you can put anything in there. Including instructions for how to work with someone who has ADHD.

The key insight: Claude runs at the start of every conversation. If I write "always do X when starting a session", it actually will. Unlike a human assistant who'd eventually forget or get annoyed, Claude follows the instructions every single time.

So I wrote a `CLAUDE.md` that turns Claude into an ADHD-aware pair programmer. It handles the executive function stuff I struggle with, so I can focus on the actual thinking.

## What It Does

### Session Kickoff (Automatic)

Every time I start a conversation, Claude automatically:

1. Checks my status board and summarises what's in flight
2. Detects the current git branch and pulls context if it matches a ticket pattern
3. Tells me what I was last working on and what the next action is
4. Flags any blocked items that might have unblocked (PRs awaiting approval, etc.)
5. Suggests which item to work on first, with reasoning

That last one is crucial. "What should I do?" is the hardest question when you have ADHD. Decision paralysis is real. Claude picks for me: "Suggested focus: the auth-fix PR, because it's approved and ready to merge."

I can override it, but having a default removes the friction of starting.

### Status Board

I keep a markdown file at `~/.claude/status-board.md` with all my in-flight work:

```markdown
## Auth Service Refactor

| Repo | Branch | Status | Link | Next Action |
|------|--------|--------|------|-------------|
| auth-service | feature/oauth-flow | PR Open | PR #142 | Address review comments |
| user-service | feature/oauth-integration | Blocked | PR #89 | Waiting on auth-service PR |

**Deploy order:** auth-service -> user-service
**Verify:** Login flow works on staging
```

Every item has: repo, branch, status, links, and next action. When things change, Claude updates it. When I start a session, Claude reads it. I never have to remember where I was. It's all written down.

### Context Switch Snapshots

This is the magic bit. When I say "switching to X" or "brb" or just start working in a different repo, Claude automatically:

1. Dumps current task state to the status board
2. Notes any uncommitted changes
3. When I return, restores context from the snapshot

It happens silently, just a brief "Saved your context to the status board." I don't have to ask, I don't have to remember. The context is preserved whether I'm gone for five minutes or five days.

### The Parking Lot

ADHD means constant tangents. I'll be fixing a bug and notice a typo in a comment. Or think "we should refactor this module". Or spot a potential security issue.

These are all valid observations. But if I chase them, I lose the thread of what I was actually doing.

So Claude automatically captures tangents in `~/.claude/parking-lot.md`:

```markdown
- [ ] Typo in auth module docstring (noted during oauth-flow work, 2026-03-04)
- [ ] Consider extracting token refresh to shared lib (noted during oauth-flow work, 2026-03-04)
```

It just says "Parked that" and keeps going. No discussion, no "do you want me to add this?". Just capture and continue. The parking lot gets reviewed at the end of the day.

### Scope Creep Detection

Related to parking, but more aggressive. If mid-task I start expanding scope ("while I'm here, let me also..."), Claude flags it:

> "That sounds like a separate task. Parking it for now."

It adds the item to the parking lot and stays on the current task. If I insist, fine, but it notes the scope change. This has saved me countless times from "quick" changes that spiral into hours of yak-shaving.

### Decision Fatigue Reduction

Instead of open-ended questions like "How do you want to handle this?", Claude leads with recommendations:

> "**Recommended:** Use the existing auth middleware (simpler, consistent with codebase). Alternative: Write a custom implementation (more control, more code to maintain)."

Two options max. Clear recommendation marked as such. I can still choose, but I don't have to think from scratch.

### Hyperfocus Check-ins

The flip side of distraction is hyperfocus, getting so deep into something that you forget everything else exists.

If the conversation goes 15+ exchanges deep on a single task, Claude reminds me:

> "Quick reminder: PR #142 is still awaiting approval. Want to stay on this or check on that?"

Once per deep session, no nagging. Just a gentle "hey, other things exist."

### Session Wrap-up

When I say "wrap up" or "EOD", Claude:

1. Updates the status board with current state of all work items
2. Writes a standup summary to `~/.claude/standup.md`:

```markdown
## Done
- Implemented OAuth token refresh logic
- Fixed race condition in session handling
- Addressed PR review comments

## Blocked
- user-service PR waiting on auth-service merge
- Deployment waiting on staging environment fix

## Next
- Merge auth-service PR once approved
- Update user-service branch after merge
```

3. Checks for uncommitted changes and reminds me
4. Reviews the parking lot and asks if anything should become a ticket

I copy-paste the standup summary each morning. Done in seconds instead of trying to remember what I actually did.

### Clickable Everything

Every response includes clickable links: PRs, tickets, build pipelines, repo URLs. No hunting for things. Claude checks my bookmarks file for common links and uses them automatically.

Small thing, massive difference. Reducing friction matters.

## The CLAUDE.md

Here's the core of my configuration:

```markdown
## Working Style
- User has ADHD and often runs multiple Claude sessions in parallel
- Always provide clickable links to reduce friction
- Keep responses concise, bullet points over paragraphs
- When a task completes or is blocked, give a clear one-line status update with next steps
- Decision fatigue reduction: Lead with a recommended option instead of open-ended questions

## Session Kickoff (AUTOMATIC)
1. Check status board, summarise what's in flight
2. Detect git branch, pull context if it matches a ticket pattern
3. Tell user what they were last working on and what's next
4. If blocked items might have unblocked, flag them
5. Suggest which item to work on first

## Context Switch Snapshots (AUTOMATIC)
Triggers: user says "switching to X", "brb", starts working in different repo
1. Dump current task state to status board
2. Note uncommitted changes
3. When they return, restore context

## Parking Lot (AUTOMATIC)
When user mentions something tangential, capture it to parking-lot.md
Just say "Parked that" and keep going, don't ask, don't wait
```

The full version has more detail, but that's the structure. Note how many things are marked "AUTOMATIC". The key is removing decisions, not adding them.

## Does It Actually Work?

Yeah. Surprisingly well.

I've been running this setup for a few months. The status board means I can pick up any task instantly, even after a week away. The parking lot catches dozens of tangents per week that would otherwise derail me. The automatic kickoff saves maybe 10 minutes per session of "where was I?"

Most importantly, it reduces the cognitive load of being a knowledge worker with ADHD. I don't have to remember things, I don't have to decide what to do next, I don't have to manually track context. Claude handles the executive function stuff, and I get to do the interesting work.

It's not perfect. Sometimes Claude's suggestions are wrong. Sometimes I want to chase a tangent and have to tell it "no, actually do this". But having a default that works 80% of the time beats having to think from scratch every time.

## Installation

Claude Code looks for `CLAUDE.md` in two places:

1. **Project-level:** `./CLAUDE.md` in your project root, applies only to that project
2. **Global:** `~/.claude/CLAUDE.md`, applies to all projects

I use the global location so the ADHD behaviours work everywhere. The supporting files also live in `~/.claude/`:

```
~/.claude/
├── CLAUDE.md          # Main instructions
├── status-board.md    # In-flight work items
├── parking-lot.md     # Captured tangents
├── standup.md         # Daily summaries
└── bookmarks.md       # Quick links
```

To set it up:

1. Create `~/.claude/CLAUDE.md` with the configuration above (or grab the full version from my GitHub)
2. Create empty `status-board.md`, `parking-lot.md`, `standup.md`, and `bookmarks.md` files
3. Start a new Claude Code session and it will read the instructions automatically

That's it. No restart needed, no special commands. Claude reads `CLAUDE.md` at the start of every conversation.

## Try It Yourself

The core ideas are transferable:

1. **Status board**: Write down what you're working on, with links and next actions
2. **Automatic kickoff**: Tell Claude to read the status board and suggest a focus
3. **Parking lot**: Capture tangents automatically, review later
4. **Context snapshots**: Save state when switching, restore when returning
5. **Lead with recommendations**: Reduce decisions wherever possible

If you have ADHD and use Claude Code, I'd be curious what works for you. The configuration is pretty personal. What helps me might not help you, and vice versa.

The important thing is recognising that AI assistants can do more than answer questions. They can compensate for executive function gaps if you teach them how. That's been a game-changer for me.
