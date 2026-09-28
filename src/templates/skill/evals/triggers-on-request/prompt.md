---
description: "A realistic request the skill should handle. Phrase it as a user would, without naming the skill."
tags: [skill-name, ver-01]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]   # read-only tools only; a skill that writes files needs the operator grant: claude plugin eval <plugin> --allow-tools Write Edit
---
<The request exactly as a user would type it. Include every fact the task needs;
the run starts in an empty workspace unless case.yaml seeds it.>
