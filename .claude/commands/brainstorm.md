---
description: Transform business problems into structured brainstorm sessions
argument-hint: [optional-topic] | --resume BRAINSTORM-ID
model: opus
allowed-tools: Read, Skill, AskUserQuestion
---

# /brainstorm

This command is a pure orchestrator. ALL logic lives in the discovering-problems skill.

No argument parsing, no resume detection, no display logic, no error handling here.
The skill handles everything.

```
Skill(command="discovering-problems")
```
