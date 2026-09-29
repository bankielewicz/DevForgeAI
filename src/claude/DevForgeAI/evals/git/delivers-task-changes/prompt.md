---
description: "VER-01: uncommitted task work goes to a new worktree branch, rebased onto origin/main and pushed; unrelated and local files stay out."
tags: [git, ver-01]
max_turns: 80
timeout_seconds: 1500
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---
Commit my --json change on branch feat/json-output and push it to origin; notes/todo.md is other work.
