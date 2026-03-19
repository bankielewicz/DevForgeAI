# W3 Report Templates Reference

This file contains the exact report format specifications used during Phase 03 (Reporting). Load this file fresh at the start of Phase 03. Do NOT rely on memory of previous reads.

---

## Report Header (Box-Drawing Format)

```
╔════════════════════════════════════════════════════════════════════╗
║                    W3 COMPLIANCE AUDIT REPORT                    ║
╠════════════════════════════════════════════════════════════════════╣
║  Scanned: {TOTAL_FILES} files in .claude/                        ║
║  Violations: {CRITICAL_COUNT + HIGH_COUNT + MEDIUM_COUNT}        ║
║    CRITICAL: {CRITICAL_COUNT}                                    ║
║    HIGH: {HIGH_COUNT}                                            ║
║    MEDIUM: {MEDIUM_COUNT}                                        ║
╚════════════════════════════════════════════════════════════════════╝
```

**Usage:** Display when $QUIET is false. Substitute variable placeholders with actual values from Phase 02 scan results.

---

## Violation Tables

### CRITICAL Violations Table

**Condition:** Display when CRITICAL_COUNT > 0

```markdown
## CRITICAL Violations (Block Release)

| File | Line | Issue |
|------|------|-------|
| {file_path} | {line_number} | Subagent invoking Skill() - FORBIDDEN |

**Action Required:** Subagents CANNOT invoke skills per architecture-constraints.md
```

### HIGH Violations Table

**Condition:** Display when HIGH_COUNT > 0

```markdown
## HIGH Priority (Review Required)

| File | Line | Issue |
|------|------|-------|
| {file_path} | {line_number} | Auto-invokes skill without user approval |

**Action Required:** Add user consent gate before Skill() OR use display-only pattern
```

### MEDIUM Violations Table

**Condition:** Display when MEDIUM_COUNT > 0

```markdown
## MEDIUM Priority (Documentation Gap)

| File | Issue |
|------|-------|
| {file_path} | Missing W3 compliance note |

**Action Required:** Add W3 compliance note explaining invocation pattern
```

### Clean Audit Message

**Condition:** Display when ALL counts are 0

```
No W3 violations detected. All skill invocations are compliant.
```

---

## Remediation Pattern (Fix Hints)

**Condition:** Display when $FIX_HINTS is true

### BEFORE (W3 Violation)
```
Skill(command="spec-driven-architecture")
```

### AFTER Option A: Display-Only Recommendation (Preferred)
```
**Recommended Next Action (display-only, no auto-invocation):**
Run /create-context [project-name]
**NOTE:** Per W3 compliance, this skill does NOT auto-invoke other skills.
```

### AFTER Option B: User Consent Gate
```
AskUserQuestion:
    Question: "Proceed with architecture creation?"
    Options: ["Yes, invoke /create-context", "No, skip"]

IF user approves:
    Skill(command="spec-driven-architecture")
```

**Reference:** STORY-135

---

## Quiet Mode Output

**Condition:** Display when $QUIET is true

Single-line summary format:
```
W3 Audit: CRITICAL={CRITICAL_COUNT} HIGH={HIGH_COUNT} MEDIUM={MEDIUM_COUNT}
```

---

## Final Summary Banner

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {RESULT_ICON}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CRITICAL: {CRITICAL_COUNT}
  HIGH:     {HIGH_COUNT}
  MEDIUM:   {MEDIUM_COUNT}
  INFO:     {INFO_COUNT}
  Result:   {RESULT_LABEL}
  Exit:     {EXIT_STATUS}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**RESULT_ICON values:**
- CRITICAL > 0: `"AUDIT FAILED"`
- HIGH > 0: `"AUDIT WARNING"`
- All zero: `"W3 AUDIT PASSED"`

**RESULT_LABEL values:**
- CRITICAL > 0: `"FAILED"`
- HIGH > 0: `"WARNING"`
- All zero: `"PASSED"`

**EXIT_STATUS values:**
- CRITICAL > 0: `1`
- Otherwise: `0`
