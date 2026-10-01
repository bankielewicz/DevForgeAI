---
description: "VER-01, VER-02, VER-03, VER-18, VER-19: the shared fixture and prompt write exactly the nine documents the ARCH's kinds need, each with its fixed ID, title, provenance and resolution line; decisions are cited with constrains links; the reply opens with the report block and ends with the epic next step."
tags: [context, ver-01, ver-02, ver-03, ver-18, ver-19]
max_turns: 100
timeout_seconds: 1800
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---
Write the project context documents. I confirm these conventions: Typer 0.12.x for the shiftlog CLI;
Alembic 1.13.x for the Local database; pytest 8.x for every component; and dependency updates go in
their own pull request. None of these is hard to reverse or shared by several epics: each can be
replaced inside the components that use it. Don't inspect any code. Proceed without questions.
