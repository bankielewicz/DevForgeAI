#!/bin/bash
# Test: AC#1 - Decision Documented in EPIC-082
# Story: STORY-481
# Generated: 2026-02-23
# Description: Verifies that EPIC-082 epic file contains a finalized DECISION (not just
#              a recommendation) for the subagent reference loading mechanism, with rationale.

# === Test Configuration ===
PASSED=0
FAILED=0

EPIC_FILE="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Epics/EPIC-082-domain-reference-generation.epic.md"

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

echo "=== AC#1: Decision Documented in EPIC-082 ==="
echo "Target: $EPIC_FILE"
echo ""

# === Arrange ===
# Verify target file exists
if [ ! -f "$EPIC_FILE" ]; then
    echo "  ERROR: Target file does not exist: $EPIC_FILE"
    echo "Results: 0 passed, 1 failed (file missing)"
    exit 1
fi

# === Act & Assert ===

# Test 1: Epic file must contain a DECISION section (not just "Approach A recommended")
# Pattern: A heading or label with the word DECISION (uppercase) to mark finalization
grep -q "DECISION" "$EPIC_FILE"
run_test "EPIC-082 contains DECISION marker (uppercase, not just recommendation)" $?

# Test 2: Decision must specify one of the three valid approaches by name
# The decision must explicitly name the chosen mechanism
grep -qE "(orchestration-driven|opt-in|auto-load)" "$EPIC_FILE"
run_test "EPIC-082 specifies chosen approach (orchestration-driven, opt-in, or auto-load)" $?

# Test 3: Decision section must include rationale (not just a label)
# Check for a rationale/reason keyword near the decision
grep -q "Rationale" "$EPIC_FILE"
run_test "EPIC-082 contains Rationale section for the decision" $?

# Test 4: The decision must be marked as DECIDED or SELECTED (not RECOMMENDED or PARTIALLY RESOLVED)
# Previous state was "Approach A (orchestration-driven) recommended" - must now be finalized
grep -q "## Reference Loading Decision" "$EPIC_FILE"
run_test "EPIC-082 contains '## Reference Loading Decision' section heading" $?

# Test 5: The word "RECOMMENDED" must not be the only qualifier (decision must supersede recommendation)
# Check that the file does not still have "PARTIALLY RESOLVED" status for this decision
grep -v "PARTIALLY RESOLVED" "$EPIC_FILE" | grep -q "DECISION"
run_test "Decision is not still marked as PARTIALLY RESOLVED" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
