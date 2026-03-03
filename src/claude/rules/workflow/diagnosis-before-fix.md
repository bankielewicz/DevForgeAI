# Diagnosis Before Fix Rule

## Purpose

Enforce systematic root cause diagnosis before applying fixes to persistent failures. Prevents shotgun debugging by requiring investigation when iterative fixes fail.

---

## HALT Trigger

**HALT: Diagnosis required before fix attempts.**

When ANY of the following conditions are met, you MUST invoke the root-cause-diagnosis skill before attempting further fixes:

1. **3+ consecutive fix attempts** fail on the same error or test
2. **Integration tests fail** with non-environment errors
3. **QA finds CRITICAL/HIGH violations** that were not caught during TDD
4. **Pre-commit hook blocks** after 2+ formatting/validation retries

---

## Enforcement

This rule is MANDATORY. It cannot be skipped, deferred, or overridden without explicit user approval via AskUserQuestion.

### Trigger Detection

```
IF fix_attempt_count >= 3 AND same_error_persists:
    HALT
    Display: "3 fix attempts failed on the same issue. Diagnosis required."
    Invoke: root-cause-diagnosis skill
    DO NOT proceed with fix attempt #4 without diagnosis
```

### Skill Reference

Invoke the root-cause-diagnosis skill at:
`.claude/skills/root-cause-diagnosis/SKILL.md`

The skill enforces a 4-phase methodology:
1. **CAPTURE** - Collect failure artifacts
2. **INVESTIGATE** - Cross-reference against context files (uses diagnostic-analyst subagent)
3. **HYPOTHESIZE** - Generate ranked hypotheses with confidence scores
4. **PRESCRIBE** - Recommend targeted fixes with specific file paths

---

## 3-Attempt Escalation Protocol

| Attempt | Action |
|---------|--------|
| 1 | Normal iterative fix. Apply fix, run tests. |
| 2 | Normal iterative fix. Apply fix, run tests. |
| 3 | **HALT.** Invoke root-cause-diagnosis skill. Apply prescribed fix. |
| 4 | If diagnosis prescription fails, try next hypothesis. |
| 5 | **HALT.** Escalate to user via AskUserQuestion. |

### Escalation Message Template

After attempt 5 (or after all hypotheses exhausted):

```
AskUserQuestion: "Persistent failure after diagnosis and {N} fix attempts.

Error: {error_message}
Diagnosis: {top_hypothesis}
Attempts: {fix_attempt_count}

Options:
1. Provide additional context or hints
2. Skip this acceptance criterion (requires justification)
3. Pause and investigate manually"
```

---

## Scope

### Applies To

- TDD Green phase (Phase 03) - test failures during implementation
- TDD Refactor phase (Phase 04) - regressions during refactoring
- Integration phase (Phase 05) - cross-component failures
- QA deep analysis (Phase 2) - constraint violations

### Does Not Apply To

- TDD Red phase (Phase 02) - tests are EXPECTED to fail
- Environment setup failures (Docker, database, network)
- User-requested manual fixes
- Single-attempt failures (normal iteration)

---

## Anti-Pattern: Shotgun Debugging

**Forbidden behavior:** Making random code changes hoping to fix a failure without understanding the root cause.

**Signs of shotgun debugging:**
- Changing multiple unrelated files per fix attempt
- Reverting and retrying the same approach
- Adding print/log statements without reading the error
- Changing test assertions to match wrong output

**Required behavior:** After 3 failed attempts, STOP making changes and START investigating.

---

## Compliance

Violations of this rule are tracked. If a fix is applied after 3+ failed attempts without invoking diagnosis:
- The fix attempt is logged as a rule violation
- QA validation may flag the pattern as a process anti-pattern
- The observation is captured in `devforgeai/feedback/ai-analysis/`

---

## References

- **Skill:** `.claude/skills/root-cause-diagnosis/SKILL.md`
- **Subagent:** `.claude/agents/diagnostic-analyst.md`
- **Investigation Patterns:** `.claude/skills/root-cause-diagnosis/references/investigation-patterns.md`
- **Workflow Integration:** `.claude/skills/root-cause-diagnosis/references/workflow-integration.md`
