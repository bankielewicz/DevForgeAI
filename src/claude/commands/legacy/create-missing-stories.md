---
description: Create stories for all detected coverage gaps in an epic
argument-hint: "EPIC-NNN"
model: opus
allowed-tools: Read, Skill, AskUserQuestion
---

# /create-missing-stories

Detect coverage gaps in an epic and batch-create stories. The `spec-driven-coverage` skill owns gap detection, metadata collection, batch invocation of `spec-driven-stories`, and failure isolation.

```
IF $ARGUMENTS empty OR not matching "^EPIC-[0-9]{3}$" (case-insensitive):
    Display "Usage: /create-missing-stories EPIC-NNN" → HALT

**Epic ID:** ${ARGUMENTS}
**Created From:** /create-missing-stories
Skill(command="spec-driven-coverage")
```

## References

- Skill: `.claude/skills/spec-driven-coverage/SKILL.md` (detection + batch creation + failure isolation)
- Story producer: `.claude/skills/spec-driven-stories/SKILL.md` (invoked by spec-driven-coverage Phase 04)
