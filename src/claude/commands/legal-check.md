---
description: "Invoke guided legal assessment via the advising-legal skill. Covers business structure, IP protection, and compliance guidance."
argument-hint: "[topic] - Optional: 'business-structure', 'ip-protection', or blank for full assessment"
---

# /legal-check

Delegates to the advising-legal skill for educational legal guidance.

## Usage

```
/legal-check                    # Full guided legal assessment
/legal-check business-structure # Business entity selection guidance
/legal-check ip-protection      # IP protection checklist
```

## Behavior

1. Pass `$ARGUMENTS` to the advising-legal skill
2. Skill handles all guidance logic, adaptive pacing, and disclaimer enforcement

## Delegation

```
Skill(command="advising-legal $ARGUMENTS")
```

**Skill path:** `.claude/skills/advising-legal/SKILL.md`

## Notes

- This command contains zero business logic
- All processing delegated to the advising-legal skill
- Disclaimer enforcement handled by the skill
- Works in both standalone and project-anchored modes
