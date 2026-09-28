---
description: "VER-08: a request to open a PR and write its description must not trigger the prd skill."
tags: [prd, ver-08, negative-trigger]
max_turns: 15
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---
Open a PR for my staged changes and write its description. The change adds retry with
exponential backoff to the payment webhook handler, so dropped Stripe events get reprocessed.
