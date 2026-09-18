---
description: Invoke building-team skill for team-building guidance
argument-hint: [topic] (first-hire | co-founder | role-planning | full)
model: opus
allowed-tools: AskUserQuestion, Read, Skill
execution-mode: immediate
---

# /build-team - Team Building Guidance

Invoke building-team skill for team-building guidance. Validates arguments and delegates to skill.

---

## ARGUMENTS

Valid: `first-hire`, `co-founder`, `role-planning`, `full`

---

## Validation

```
FOR arg in arguments:
    IF arg matches "first-hire|co-founder|role-planning|full":
        PHASE_ARG = arg
IF PHASE_ARG empty: Display usage and HALT
```

---

## Skill Invocation

```
Display: "Team Building Guidance - Topic: ${PHASE_ARG}"
Skill(command="building-team", args="${PHASE_ARG}")
```

---

## Error Handling

| Error | Resolution |
|-------|------------|
| No/invalid argument | Show valid options |
| Skill not found | Error: src/claude/skills/building-team/SKILL.md missing |
