---
description: "VER-04: connect initializes the repository, sets origin to the given path and fetches, but pushes nothing and offers the bootstrap commit."
tags: [git, ver-04]
max_turns: 80
timeout_seconds: 1500
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---
Initialize this folder as a git repository and point it at the empty repository at remote/app.git.
