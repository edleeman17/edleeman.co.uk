---
title: "Saving LLM tokens with quiet Makefiles"
date: 2026-02-26T12:00:00Z
draft: false
type: "note"
image: images/apple-touch-icon.png
---

# Saving LLM tokens with quiet Makefiles

When working with LLM coding assistants like Claude Code, every token in your context window counts. Verbose build output from Docker, npm, or other tools can quickly consume thousands of tokens that would be better spent on actual code discussion.

A simple Makefile pattern can suppress all output unless something goes wrong:

```makefile
up:
	@docker-compose up -d >/dev/null 2>&1 || (docker-compose logs && exit 1)
	@echo "Running at http://localhost:8088"

build:
	@docker-compose build >/dev/null 2>&1 || (docker-compose logs && exit 1)

restart:
	@docker-compose restart >/dev/null 2>&1 || (docker-compose logs && exit 1)
```

## How it works

1. `@` at the start suppresses Make from echoing the command itself
2. `>/dev/null 2>&1` redirects both stdout and stderr to nowhere
3. `|| (docker-compose logs && exit 1)` if the command fails, show the logs and exit with an error code

The result: successful runs produce minimal output (just your custom message), but failures still show you exactly what went wrong.

## Why this matters for LLMs

A typical `docker-compose build` might output hundreds of lines. When your AI assistant runs this command, all that output goes into the context window. With quiet Makefiles:

- Successful builds use around 10 tokens instead of 2000
- You preserve context for actual problem-solving
- Errors still surface with full detail when you need them

## The pattern generalised

```makefile
some-task:
	@command-that-produces-output >/dev/null 2>&1 || (echo "Task failed" && exit 1)
```

For commands without a built-in log viewer, you might capture output to a temp file:

```makefile
build:
	@npm run build > /tmp/build.log 2>&1 || (cat /tmp/build.log && exit 1)
```

A small change that adds up to significant token savings over a coding session.
