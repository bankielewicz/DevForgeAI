---
description: "VER-28: carrying work from a main that is ahead of origin stops before the branch and asks about the local-only commit."
tags: [git, ver-28]
max_turns: 80
timeout_seconds: 1500
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---
Commit my --json change on branch feat/json-output and push it to origin.
