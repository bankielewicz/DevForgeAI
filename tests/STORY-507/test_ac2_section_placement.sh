#!/bin/bash
# Test: AC#2 - Section Placement is Correct
# Story: STORY-507
# Generated: 2026-02-28

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/designing-systems/assets/templates/epic-template.md"

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

echo "=== AC#2: Section Placement is Correct ==="
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file not found: $TARGET_FILE"
    exit 1
fi

# Get line numbers for each section
TECH_LINE=$(grep -n "^## Technical Considerations" "$TARGET_FILE" | head -1 | cut -d: -f1)
DECISION_LINE=$(grep -n "^## Decision Context" "$TARGET_FILE" | head -1 | cut -d: -f1)
DEPS_LINE=$(grep -n "^## Dependencies" "$TARGET_FILE" | head -1 | cut -d: -f1)

# === Act & Assert ===

# Test 1: Decision Context section exists (prerequisite for placement checks)
if [ -z "$DECISION_LINE" ]; then
    run_test "Decision Context section exists (required for placement check)" 1
    echo ""
    echo "Results: $PASSED passed, $FAILED failed"
    exit 1
fi
run_test "Decision Context section exists (required for placement check)" 0

# Test 2: Technical Considerations section exists
if [ -z "$TECH_LINE" ]; then
    run_test "Technical Considerations section exists (required for placement check)" 1
    echo ""
    echo "Results: $PASSED passed, $FAILED failed"
    exit 1
fi
run_test "Technical Considerations section exists (required for placement check)" 0

# Test 3: Dependencies section exists
if [ -z "$DEPS_LINE" ]; then
    run_test "Dependencies section exists (required for placement check)" 1
    echo ""
    echo "Results: $PASSED passed, $FAILED failed"
    exit 1
fi
run_test "Dependencies section exists (required for placement check)" 0

# Test 4: Decision Context appears AFTER Technical Considerations
if [ "$DECISION_LINE" -gt "$TECH_LINE" ]; then
    run_test "Decision Context (line $DECISION_LINE) appears after Technical Considerations (line $TECH_LINE)" 0
else
    run_test "Decision Context (line $DECISION_LINE) appears after Technical Considerations (line $TECH_LINE)" 1
fi

# Test 5: Decision Context appears BEFORE Dependencies
if [ "$DECISION_LINE" -lt "$DEPS_LINE" ]; then
    run_test "Decision Context (line $DECISION_LINE) appears before Dependencies (line $DEPS_LINE)" 0
else
    run_test "Decision Context (line $DECISION_LINE) appears before Dependencies (line $DEPS_LINE)" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
