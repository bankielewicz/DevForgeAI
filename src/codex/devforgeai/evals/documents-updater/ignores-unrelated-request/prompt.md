---
description: "VER-08: a request for a commit message must not trigger the skill or change documentation."
tags: [documents-updater, ver-08, negative-trigger]
max_turns: 15
timeout_seconds: 300
allowed_tools: [exec_command, apply_patch, request_user_input]
---
Write a commit message for my staged changes.
