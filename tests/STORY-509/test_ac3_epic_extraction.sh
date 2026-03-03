#!/bin/bash
# Test: AC#3 - Epic Creation Can Extract design_decisions
# Story: STORY-509
# Generated: 2026-02-28

PASSED=0
FAILED=0

TARGET_FILE="src/claude/skills/designing-systems/references/epic-management.md"

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

echo "=== AC#3: Epic Creation Extracts design_decisions ==="
echo "Target: $TARGET_FILE"
echo ""

if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# Test 1: epic-management.md references design_decisions extraction
grep -qi "design_decisions" "$TARGET_FILE" 2>/dev/null; run_test "epic-management.md references design_decisions" $?

# Test 2: epic-management.md references threat_model extraction
grep -qi "threat_model" "$TARGET_FILE" 2>/dev/null; run_test "epic-management.md references threat_model" $?

# Test 3: extraction step exists that pulls design_decisions from requirements
grep -i "design_decisions" "$TARGET_FILE" 2>/dev/null | grep -qi -E "extract|populate|copy|map|transfer" 2>/dev/null; run_test "extraction step exists for design_decisions from requirements" $?

# Test 4: extraction step exists for threat_model
grep -i "threat_model" "$TARGET_FILE" 2>/dev/null | grep -qi -E "extract|populate|copy|map|transfer" 2>/dev/null; run_test "extraction step exists for threat_model from requirements" $?

# Summary
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
