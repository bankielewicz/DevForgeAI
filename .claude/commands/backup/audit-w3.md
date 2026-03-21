---
description: Audit codebase for W3 violations (auto-skill chaining without user control)
argument-hint: [--verbose|--fix-hints|--quiet]
model: opus
allowed-tools: Read, Grep, Glob
---

# /audit-w3 - W3 Compliance Audit

Scans for W3 violations: auto-skill chaining without user control.

**W3 Definition:** Skills/commands that auto-invoke other skills without user approval,
causing token overflow and violating lean orchestration principles.

**Reference:** BRAINSTORM-001 (line 85), STORY-135

---

## Phase 0: Parse Arguments

```
MODE = "normal"
QUIET = false
FIX_HINTS = false

FOR arg in $ARGUMENTS:
    IF arg == "--verbose":
        MODE = "verbose"
    ELIF arg == "--quiet":
        QUIET = true
    ELIF arg == "--fix-hints":
        FIX_HINTS = true
```

---

## Phase 1: Invoke Scanning Skill

**Set context markers:**
```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  W3 Compliance Audit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Command:** audit-w3
**Mode:** ${MODE}
**Quiet:** ${QUIET}
**Fix Hints:** ${FIX_HINTS}

Delegating to auditing-w3-compliance skill...
"
```

**Invoke skill:**
```
Skill(command="auditing-w3-compliance")
```

**After skill invocation:**
- Skill's SKILL.md content expands inline in conversation
- **YOU execute the skill's scanning phases** (not waiting for external result)
- Follow the skill's instructions phase by phase
- Produce output as skill instructs

---

## Phase 2: Display Results

Skill produces structured report with violation counts and tables.
Display the report output directly to the user.

```
IF QUIET:
    Display only: exit code and violation count summary
ELSE:
    Display full report from skill output
```

---

## Error Handling

### Skill Invocation Failed
```
ERROR: W3 compliance skill execution failed

Error: {skill_error_message}

Try running scan manually:
  Grep(pattern='Skill\s*\(\s*command\s*=', path='.claude/agents/', glob='*.md')
```

---

## Remediation Guidance

**HIGH violations:** Files invoking Skill() without user approval should add AskUserQuestion before Skill() call or use display-only recommendation pattern.

**Pattern check:** Skill validates that each Skill() call has an AskUserQuestion gate or is display-only.

---

## Integration

**Invoked by:** Manual user command, /release command (Phase 0.5)
**Invokes:** `auditing-w3-compliance` skill (all scanning logic)
**Output:** Display report to user, exit code for CI/CD

**Version:** 2.0 - Lean Orchestration | **Pattern:** Command delegates to skill
