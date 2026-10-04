---
description: "VER-11: with the task-list tools allowed, VER-01's prompt gives a task list kept by the convention: a task per step carrying devforgeai_step, created before the first Write, step 5 among them, each completed; BRN-001 still written."
tags: [brainstorm, ver-11]
max_turns: 60
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet]
---
I run a small dental clinic with two dentists and a hygienist. About one in eight booked
appointments ends in a no-show, and it's costing us real money. Brainstorm ways we could
cut down on no-shows. Don't ask me any questions, just work through it and write it up.
