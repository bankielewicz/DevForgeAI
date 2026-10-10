---
description: "VER-37: '/devforgeai:ui approve DSN-001' for a DSN that is already approved writes nothing; the reply says it is already approved, with its version, approver and date."
tags: [ui, ver-37]
max_turns: 15
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash, ToolSearch]
---
/devforgeai:ui approve DSN-001. I'm Example Owner.
