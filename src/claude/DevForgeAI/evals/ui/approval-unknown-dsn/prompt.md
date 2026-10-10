---
description: "VER-37: approving a DSN that does not exist writes nothing; the reply lists the DSNs and their statuses."
tags: [ui, ver-37]
max_turns: 15
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash, ToolSearch]
---
/devforgeai:ui approve DSN-009
