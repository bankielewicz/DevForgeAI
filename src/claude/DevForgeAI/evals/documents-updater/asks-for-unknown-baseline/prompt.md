---
description: "VER-06: with no tag, remote or integration branch, the skill asks where the branch work began and writes no changelog."
tags: [documents-updater, ver-06]
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---
Update the changelog with the work on my branch.
