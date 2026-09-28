---
description: "VER-08: a request for a commit message must not trigger the skill or change documentation."
tags: [documents-updater, ver-08, negative-trigger]
max_turns: 15
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---
Write a commit message for my staged changes.
