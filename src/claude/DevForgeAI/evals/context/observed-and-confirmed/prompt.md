---
description: "VER-05: inspection reads only the named paths; observed facts carry their path and date; pytest, confirmed in the request, becomes a convention that keeps observed_in."
tags: [context, ver-05]
max_turns: 100
timeout_seconds: 1800
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---
Write the project context documents. You may read pyproject.toml, src/shiftlog/ and tests/. Keep pytest as our convention. Proceed without questions.
