---
description: "VER-28: choosing to amend ARCH-001 without confirming the outcome, with every question deferred (the new one and the open DEC-02): nothing is written to ARCH-001 before the outcome is confirmed, and the final reply asks to confirm amend, naming the new DEC, the new version and the return to in-review."
tags: [architecture, ver-28]
max_turns: 90
timeout_seconds: 1200
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---
PRD-001 is now at version 2: it adds FR-003, the coordinator's daily roster. Let's amend ARCH-001 for
it. Leave every architectural question open for now, the existing DEC-02 included; I'll decide them
later.
