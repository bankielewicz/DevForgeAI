---
name: create-stories-from-rca
description: Create user stories from RCA recommendations
argument-hint: "RCA-NNN [--threshold HOURS]"
model: opus
allowed-tools: Read, Skill, AskUserQuestion
---

# /create-stories-from-rca

Parse an RCA document, interactively select recommendations, and batch-create stories. The `spec-driven-stories` skill owns parsing, selection, creation, and RCA-story back-linking.

```
RCA_ID = uppercase(extract "RCA-[0-9]+" from $ARGUMENTS)

IF RCA_ID empty:
    Display "Usage: /create-stories-from-rca RCA-NNN [--threshold HOURS]" → HALT

**RCA ID:** ${RCA_ID}
**Created From:** /create-stories-from-rca
Skill(command="spec-driven-stories", args="--RCA")
```

## References

- Skill: `.claude/skills/spec-driven-stories/SKILL.md`
- RCA workflow refs: `references/create-stories-from-rca/{parsing,selection,batch-creation,linking}-workflow.md`
