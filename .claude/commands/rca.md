---
description: Perform Root Cause Analysis with 5 Whys methodology
argument-hint: [issue-description] [severity]
model: opus
allowed-tools: Read, Skill, AskUserQuestion, Glob, Grep
---

# /rca - Root Cause Analysis Command

Perform systematic RCA for DevForgeAI framework breakdowns using 5 Whys methodology.

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT perform 5 Whys analysis or evidence collection
- ❌ DO NOT generate RCA documents or recommendations
- ❌ DO NOT read framework files for analysis (skill handles auto-read)
- ❌ DO NOT format completion reports (skill handles display)

**DO (command responsibilities only):**
- ✅ MUST capture issue description (from arg or AskUserQuestion)
- ✅ MUST validate severity (CRITICAL/HIGH/MEDIUM/LOW or infer)
- ✅ MUST set context markers for skill
- ✅ MUST invoke skill immediately after validation

---

## Phase 0: Argument Validation

```
IF $1 is empty:
    AskUserQuestion:
        Question: "What framework breakdown should I analyze?"
        Header: "Issue"
        Options:
            - "Skill didn't follow intended workflow"
            - "Command violated lean orchestration pattern"
            - "Quality gate was bypassed"
            - "Context file constraint ignored"
        multiSelect: false
    ISSUE_DESCRIPTION = user response
    IF cancelled: Display "RCA cancelled." → EXIT
ELSE:
    ISSUE_DESCRIPTION = $1

IF $2 provided:
    VALID = [CRITICAL, HIGH, MEDIUM, LOW]
    IF uppercase($2) not in VALID:
        AskUserQuestion:
            Question: "Invalid severity '${$2}'. What severity level?"
            Header: "Severity"
            Options:
                - "CRITICAL - Framework broken, blocking work"
                - "HIGH - Significant workflow impact"
                - "MEDIUM - Quality improvement opportunity"
                - "LOW - Minor issue or enhancement"
            multiSelect: false
        SEVERITY = extracted value
    ELSE:
        SEVERITY = uppercase($2)
ELSE:
    SEVERITY = "infer"

Display: "✓ Issue: ${ISSUE_DESCRIPTION}"
Display: "✓ Severity: ${SEVERITY}"
```

---

## Phase 1: Invoke Skill

**Issue Description:** ${ISSUE_DESCRIPTION}
**Severity:** ${SEVERITY}
**Command:** rca

```
Skill(command="spec-driven-rca")
```

**Skill handles ALL workflow** including issue clarification, auto-read files, 5 Whys analysis, evidence collection, recommendation generation, RCA document creation, validation, and completion report.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| No issue description | AskUserQuestion prompts for description |
| Invalid severity | AskUserQuestion offers CRITICAL/HIGH/MEDIUM/LOW |
| Skill execution failed | Check skill output, verify affected component exists |
| RCA document exists | Skill auto-increments RCA number |

---

## References

- Skill: `.claude/skills/spec-driven-rca/SKILL.md`
- Help: `.claude/skills/spec-driven-rca/references/rca-help.md` (examples, integration guide, framework analysis)
- Pattern: `devforgeai/protocols/lean-orchestration-pattern.md`

**Command follows lean orchestration: Validate → Set markers → Invoke skill**
