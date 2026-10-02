---
description: "VER-33: an explicit request to include the feature commit permits carrying the pending work without asking again."
tags: [git, ver-33]
max_turns: 80
timeout_seconds: 1500
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---
Commit my --json change on branch feat/json-output and push it to origin, including the existing 'docs: plan the weekly summary' commit on feat/weekly.
