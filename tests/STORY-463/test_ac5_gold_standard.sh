#!/bin/bash
# Test: AC#5 - feedback-search.md follows gold standard lean orchestration pattern
# Story: STORY-463
# Generated: 2026-02-21
# TDD Phase: RED - these tests MUST FAIL before refactoring
# Reference: create-story.md gold standard pattern

PASSED=0
FAILED=0
TARGET="src/claude/commands/feedback-search.md"

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

echo "=== AC#5: Gold Standard Pattern (create-story.md conventions) ==="
echo "Target: $TARGET"
echo ""

if [ ! -f "$TARGET" ]; then
    echo "  ERROR: Target file not found: $TARGET"
    exit 1
fi

# === Test 1: Has "Lean Orchestration Enforcement" section ===
grep -q "Lean Orchestration Enforcement" "$TARGET"
run_test "Contains 'Lean Orchestration Enforcement' section" $?

# === Test 2: Has Phase 0 structure ===
grep -q "Phase 0" "$TARGET"
run_test "Contains 'Phase 0' (argument parsing phase)" $?

# === Test 3: Has Phase 1 structure ===
grep -q "Phase 1" "$TARGET"
run_test "Contains 'Phase 1' (skill invocation phase)" $?

# === Test 4: Has Phase 2 structure ===
grep -q "Phase 2" "$TARGET"
run_test "Contains 'Phase 2' (display results phase)" $?

# === Test 5: Has Error Handling table ===
grep -q "Error Handling" "$TARGET"
run_test "Contains 'Error Handling' table/section" $?

# === Test 6: Has References section ===
grep -q "^## References\|^# References\|## Reference" "$TARGET"
run_test "Contains 'References' section" $?

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[ $FAILED -eq 0 ] && exit 0 || exit 1
