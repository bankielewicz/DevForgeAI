# AC#3 Verification: Cross-Skill Reference in error-type-3 Resolved and Documented

**Story:** STORY-453
**Generated:** 2026-02-19
**Phase:** Red (tests should FAIL before implementation)

---

## Test Configuration

**Source files:**
- `src/claude/skills/discovering-requirements/references/error-type-3-complexity-errors.md`
- `src/claude/skills/discovering-requirements/SKILL.md`
- `devforgeai/specs/Stories/STORY-453-flatten-nested-reference-chains.story.md`

**Cross-skill target:** `src/claude/skills/designing-systems/references/complexity-assessment-matrix.md`

---

## Verification Script

```bash
#!/bin/bash
# AC#3 Verification Script - STORY-453
# Run from project root
# Tests both outcome paths: (a) intentional cross-skill or (b) stale removal

ERROR3_FILE="src/claude/skills/discovering-requirements/references/error-type-3-complexity-errors.md"
SKILL_FILE="src/claude/skills/discovering-requirements/SKILL.md"
STORY_FILE="devforgeai/specs/Stories/STORY-453-flatten-nested-reference-chains.story.md"
PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=== AC#3: Cross-Skill Reference Resolution ==="
echo ""

# --- Test 1: Executable Read() for complexity-assessment-matrix.md removed from error-type-3 ---
MATCHES=$(grep -cP 'Read\(file_path=.*complexity-assessment-matrix' "$ERROR3_FILE" 2>/dev/null || echo "0")
[ "$MATCHES" -eq 0 ]
run_test "error-type-3: no executable Read() for complexity-assessment-matrix.md (found: $MATCHES)" $?

# --- Test 2: Decision documented in story Notes section ---
# The Notes section must contain a documented decision about the cross-skill reference
# Look for decision keywords after "AC3 Cross-Skill Reference Decision"
DECISION_DOC=$(sed -n '/AC3 Cross-Skill Reference Decision/,/^## /p' "$STORY_FILE" | grep -ciP '(intentional|stale|removed|retained|decision)')
[ "$DECISION_DOC" -ge 2 ]
run_test "Story Notes: AC3 decision documented with rationale (keyword matches: $DECISION_DOC)" $?

# --- Test 3: Outcome (a) OR Outcome (b) is implemented ---
# Outcome (a): SKILL.md has cross-skill Read() with inline comment
# Outcome (b): Read() removed from error-type-3 (already tested in Test 1) AND no cross-skill Read in SKILL.md

CROSS_SKILL_IN_SKILL=$(grep -cP 'Read\(file_path=.*designing-systems.*complexity-assessment-matrix' "$SKILL_FILE" 2>/dev/null || echo "0")

if [ "$CROSS_SKILL_IN_SKILL" -ge 1 ]; then
    # Outcome (a): Cross-skill Read() added to SKILL.md - must have inline comment
    HAS_COMMENT=$(grep -P 'Read\(file_path=.*complexity-assessment-matrix' "$SKILL_FILE" | grep -c 'cross-skill\|intentional\|designing-systems')
    [ "$HAS_COMMENT" -ge 1 ]
    run_test "Outcome (a): Cross-skill Read() in SKILL.md has inline comment" $?
    OUTCOME="a-intentional"
else
    # Outcome (b): Cross-skill Read() removed - verify it is not in error-type-3 either
    [ "$MATCHES" -eq 0 ]
    run_test "Outcome (b): Cross-skill Read() removed entirely (stale)" $?
    OUTCOME="b-stale"
fi

echo ""
echo "  Detected outcome: $OUTCOME"
echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[ $FAILED -eq 0 ] && exit 0 || exit 1
```

---

## Expected Results (Red Phase)

| Test | Expected | Reason |
|------|----------|--------|
| Test 1: executable Read() removed from error-type-3 | FAIL | Cross-skill Read() still present |
| Test 2: decision documented in Notes | FAIL | Decision not yet recorded |
| Test 3: outcome (a) or (b) implemented | FAIL | No resolution yet |

---

## AC3 Decision Matrix

| If Decision Is... | Then Verify... |
|-------------------|----------------|
| **Intentional** (keep) | SKILL.md has `Read(file_path="...designing-systems/.../complexity-assessment-matrix.md")` with inline comment explaining cross-skill dependency |
| **Stale** (remove) | error-type-3 has NO executable Read() for complexity-assessment-matrix.md; Notes section documents removal rationale |

---

## Verification Evidence

After implementation, re-run the script and paste output here:

```
(pending implementation)
```
