---
description: "VER-13: a component without kinds gets a [NEEDS CLARIFICATION] marker in architecture.md's Kinds column and no layer document."
tags: [context, ver-13]
max_turns: 100
timeout_seconds: 1800
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---
Write the project context documents. I confirm these conventions: Typer 0.12.x for the shiftlog CLI;
Alembic 1.13.x for the Local database; pytest 8.x for every component; and dependency updates go in
their own pull request. None of these is hard to reverse or shared by several epics: each can be
replaced inside the components that use it. Don't inspect any code. Proceed without questions.
