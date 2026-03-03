#!/bin/bash
# Test: AC#3 - Three Action Options Per Recommendation
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

echo "=== AC#3: Three Action Options Per Recommendation ==="

# Extract Phase 7.5 section for targeted testing
PHASE75_START=$(grep -n "Phase 7.5" "$TARGET_FILE" | head -1 | cut -d: -f1)

# Test 1: Create story now option exists
sed -n "${PHASE75_START:-1},\$p" "$TARGET_FILE" | grep -qi "Create story" 2>/dev/null
run_test "Create story now option exists" $?

# Test 2: Add to technical debt register option exists
sed -n "${PHASE75_START:-1},\$p" "$TARGET_FILE" | grep -qi "technical debt register" 2>/dev/null
run_test "Add to technical debt register option exists" $?

# Test 3: Skip option exists
sed -n "${PHASE75_START:-1},\$p" "$TARGET_FILE" | grep -qi "Skip" 2>/dev/null
run_test "Skip option exists" $?

# Test 4: /create-story command reference exists
sed -n "${PHASE75_START:-1},\$p" "$TARGET_FILE" | grep -q "/create-story" 2>/dev/null
run_test "References /create-story command" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
