---
description: Perform Root Cause Analysis with 5 Whys methodology
argument-hint: [issue-description] [severity]
model: opus
allowed-tools: Read, Skill, AskUserQuestion
---

# /rca

Pure orchestrator. ALL logic — argument capture, severity validation,
mode detection, evidence gathering, RCA document generation, and downstream
hand-off — lives in the spec-driven-rca skill.

No argument parsing, no mode routing, no display logic, no error handling here.
The skill handles everything.

```
Skill(command="spec-driven-rca")
```
