#!/bin/bash
# Test: AC#1 - Phase 7.5 Added to RCA Skill
# Story: STORY-489
# Generated: 2026-02-23

set -e

PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/devforgeai-rca/SKILL.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#1: Phase 7.5 Added to RCA Skill ==="

# Test 1: Phase 7.5 section exists in SKILL.md
grep -q "Phase 7.5" "$TARGET_FILE" 2>/dev/null
run_test "Phase 7.5 section exists in SKILL.md" $?

# Test 2: Phase 7.5 contains Recommendation-to-Story Pipeline title
grep -q "Recommendation-to-Story Pipeline" "$TARGET_FILE" 2>/dev/null
run_test "Phase 7.5 has Recommendation-to-Story Pipeline title" $?

# Test 3: Phase 7.5 appears AFTER Phase 7
PHASE7_LINE=$(grep -n "Phase 7" "$TARGET_FILE" | grep -v "Phase 7.5" | head -1 | cut -d: -f1)
PHASE75_LINE=$(grep -n "Phase 7.5" "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -n "$PHASE7_LINE" ] && [ -n "$PHASE75_LINE" ] && [ "$PHASE75_LINE" -gt "$PHASE7_LINE" ]; then
    run_test "Phase 7.5 appears after Phase 7" 0
else
    run_test "Phase 7.5 appears after Phase 7" 1
fi

# Test 4: Phase 7.5 appears BEFORE Error Handling section
ERROR_LINE=$(grep -n "Error Handling" "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -n "$PHASE75_LINE" ] && [ -n "$ERROR_LINE" ] && [ "$PHASE75_LINE" -lt "$ERROR_LINE" ]; then
    run_test "Phase 7.5 appears before Error Handling section" 0
else
    run_test "Phase 7.5 appears before Error Handling section" 1
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
