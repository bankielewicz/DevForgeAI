---
description: "VER-37: approving a superseded DSN writes nothing; the reply says only a draft or in-review DSN is approved."
tags: [ui, ver-37]
max_turns: 15
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash, ToolSearch]
---
/devforgeai:ui approve DSN-001
