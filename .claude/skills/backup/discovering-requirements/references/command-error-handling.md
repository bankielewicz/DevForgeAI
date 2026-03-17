---
id: command-error-handling
title: Command Error Handling Reference
version: "1.0"
created: 2026-02-18
status: Published
---

# Command Error Handling Reference

Error handling for the `/ideate` command when invoking the `discovering-requirements` skill.

---

## Table of Contents

- [Overview](#overview)
- [Error Categorization](#error-categorization)
- [Section 1: Skill Loading Failure](#section-1-skill-loading-failure)
  - [1.1 Pre-Invocation Check](#11-pre-invocation-check)
  - [1.2 Pattern Matching for Error Detection](#12-pattern-matching-for-error-detection)
  - [1.3 Error Handler Display Template](#13-error-handler-display-template)
- [Section 2: Recovery Actions](#section-2-recovery-actions)
  - [2.1 Error-Specific Recovery Actions Table](#21-error-specific-recovery-actions-table)
  - [2.2 Skill Invocation Failed Recovery](#22-skill-invocation-failed-recovery)
  - [2.3 Skill Validation Failure Recovery](#23-skill-validation-failure-recovery)
  - [2.4 User Exits During Session Recovery](#24-user-exits-during-session-recovery)
- [Section 3: Session Continuity](#section-3-session-continuity)
- [Success Criteria](#success-criteria)

---

## Overview

| Attribute | Value |
|-----------|-------|
| **Purpose** | Detect and recover from skill invocation errors |
| **Trigger** | /ideate command Phase 2.2 (skill invocation) |
| **Input** | Error from Skill(command="discovering-requirements") |
| **Effect** | Actionable recovery message, session remains active |

---

## Error Categorization

Four error categories are handled by the `/ideate` command:

| Error Category | Trigger | Severity |
|----------------|---------|----------|
| Skill Loading Failure | SKILL.md missing, YAML invalid, permissions denied | Critical |
| Skill Invocation Failed | Runtime error during skill execution | High |
| Skill Validation Failure | Phase 6.4 self-validation reports critical failures | High |
| User Exits During Session | User cancels during 10-60 question workflow | Low |

---

## Section 1: Skill Loading Failure

### 1.1 Pre-Invocation Check

Before invoking the skill, perform a quick validation:

```
# Check if SKILL.md exists
skill_check = Glob(pattern=".claude/skills/discovering-requirements/SKILL.md")

IF skill_check is empty:
    GOTO Skill Load Error Handler with errorType="FILE_MISSING"
```

### 1.2 Pattern Matching for Error Detection

After invocation attempt, categorize the error using pattern matching:

```
TRY:
    Skill(command="discovering-requirements")
CATCH error:
    # Pattern matching against error message content
    IF error matches pattern "ENOENT" OR "no such file":
        errorType = "FILE_MISSING"
        errorDetails = "SKILL.md not found at .claude/skills/discovering-requirements/"

    ELIF error matches pattern "YAML" OR "parse" OR "syntax":
        errorType = "YAML_PARSE_ERROR"
        lineNumber = extract_line_number(error) OR "unknown"
        errorDetails = "Invalid YAML in frontmatter at line {lineNumber}"

    ELIF error matches pattern "missing" AND ("section" OR "field"):
        errorType = "INVALID_STRUCTURE"
        sectionName = extract_missing_section(error) OR "unknown"
        errorDetails = "Missing required section: {sectionName}"

    ELIF error matches pattern "EACCES" OR "permission":
        errorType = "PERMISSION_DENIED"
        errorDetails = "Cannot read SKILL.md - permission denied"

    ELSE:
        errorType = "UNKNOWN"
        errorDetails = error.message

    # Preserve error context
    errorContext = {
        errorType: errorType,
        filePath: ".claude/skills/discovering-requirements/SKILL.md",
        expectedLocation: ".claude/skills/discovering-requirements/",
        details: errorDetails
    }

    GOTO Skill Load Error Handler
```

### 1.3 Error Handler Display Template

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Skill Loading Failure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The discovering-requirements skill failed to load.

Error Type: {errorType}
Details: {errorDetails}

Possible causes:
- SKILL.md has invalid YAML frontmatter
- SKILL.md file is missing or corrupted
- Reference files in references/ are missing

Recovery steps:
1. Check: .claude/skills/discovering-requirements/SKILL.md exists
2. Validate YAML frontmatter (lines 1-10)
3. Compare with GitHub version: https://github.com/anthropics/claude-code
4. Run: git checkout .claude/skills/discovering-requirements/

If issue persists, report at: https://github.com/anthropics/claude-code/issues
```

---

## Section 2: Recovery Actions

### 2.1 Error-Specific Recovery Actions Table

| Error Type | Message | Recovery Action |
|------------|---------|-----------------|
| FILE_MISSING | "SKILL.md not found at expected location" | "Run: git checkout .claude/skills/discovering-requirements/" |
| YAML_PARSE_ERROR | "Invalid YAML in frontmatter at line {N}" | "Check frontmatter syntax (lines 1-10)" |
| INVALID_STRUCTURE | "Missing required section: {section_name}" | "Compare with template at https://github.com/anthropics/claude-code" |
| PERMISSION_DENIED | "Cannot read SKILL.md - permission denied" | "Check file permissions: chmod 644" |

### 2.2 Skill Invocation Failed Recovery

If skill does not execute or throws a runtime error:

```
Troubleshooting steps:
1. Verify skill file exists:
   Glob(pattern=".claude/skills/discovering-requirements/SKILL.md")

2. Check skill is properly registered (restart Claude Code terminal if needed)

3. Verify allowed-tools permissions include Skill tool

If issue persists:
- Review skill file for syntax errors
- Check skill frontmatter is valid YAML
- Try invoking skill directly: Skill(command="discovering-requirements")
```

### 2.3 Skill Validation Failure Recovery

If skill's Phase 6.4 self-validation detects critical failures:

```
HALT: Skill validation failed

The discovering-requirements skill's Phase 6.4 self-validation reported critical failure(s).
Error details are displayed in the skill's validation report above.

The command does NOT attempt recovery or re-validation.
Error messages from skill Phase 6.4 are passed through verbatim.

To resolve:
1. Review the validation error message from the skill
2. Address the specific issue (e.g., missing required field, invalid YAML)
3. Re-run /ideate [business-idea] to retry ideation
```

### 2.4 User Exits During Session Recovery

If user cancels during the skill's 10-60 question session:

```
Ideation incomplete - user exited during requirements phase

To complete ideation:
- Re-run /ideate [business-idea] and answer all questions
- Or skip ideation and create requirements manually

Note: Comprehensive requirements gathering ensures zero ambiguity in specifications,
preventing technical debt downstream.
```

---

## Section 3: Session Continuity

After any error display, session continuity is preserved:

```
# After error display, session continues
Display: "Session active. You can run other commands or retry /ideate after repair."
```

**Session continuity guarantees:**
- Session remains active after all error types (no terminal crash)
- User can run other commands while resolving errors
- User can retry `/ideate` after repair without restarting
- No orphaned processes or corrupted state
- HALT behavior stops the /ideate command but does NOT crash the session

---

## Success Criteria

Error handling successful when:
- [ ] Error detected accurately (correct categorization)
- [ ] User presented clear recovery actions with specific steps
- [ ] Session remains active after error display
- [ ] User can retry after fixing issue
- [ ] No data loss from partial execution

---

**Version:** 1.0 | **Status:** Published | **Created:** 2026-02-18
