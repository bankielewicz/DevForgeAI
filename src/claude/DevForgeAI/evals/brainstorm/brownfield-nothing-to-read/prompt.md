---
description: "A request that says the product is in use, in a project with no document, writes a brownfield BRN-001 whose Existing product holds 'No document was found in the project.', with 'None.' under the three section 6 headings and an empty upstream, and the reply says no document was found."
tags: [brainstorm, ver-32]
max_turns: 60
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---
Our internal expense-report approval tool has been in use for two years, and an approval still
takes about nine working days. Brainstorm how we could make approvals faster. Skip any
questions and write it up.
