---
title: "Formatting JSON files in Vim"
date: 2024-02-09T16:15:14Z
draft: false
type: "note"
---
# Formatting JSON files in Vim

You can paste a bunch of minified JSON into a buffer, open the command window and type `:%!jq` and then hit enter. This will update the buffer with the formatted output.

You can then use `:%!jq -c` to re-minify the output
