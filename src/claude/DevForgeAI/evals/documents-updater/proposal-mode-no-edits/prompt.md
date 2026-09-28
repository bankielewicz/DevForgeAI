---
description: "VER-02: a request to draft doc updates without touching files changes nothing and proposes the --json text."
tags: [documents-updater, ver-02]
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---
Draft the documentation updates for my uncommitted --json change, but don't touch any files yet:
I want to review them first.
