---
description: "VER-11: a request to explain the Linux kernel's architecture must not trigger the skill or write an ARCH."
tags: [architecture, ver-11, negative-trigger]
max_turns: 15
timeout_seconds: 300
allowed_tools: [exec_command, apply_patch, request_user_input]
---
Explain the architecture of the Linux kernel: how the scheduler, memory management and the
virtual file system fit together.
