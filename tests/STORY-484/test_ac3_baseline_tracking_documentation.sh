#!/bin/bash
# Test: AC#3 - Baseline Tracking Documentation
# Story: STORY-484
# Verifies: tdd-red-phase.md contains baseline tracking documentation

set -uo pipefail

TARGET_FILE="src/claude/skills/implementing-stories/references/tdd-red-phase.md"
PASS=0
FAIL=0

run_test() {
    local description="$1"
    local pattern="$2"
    if grep -q "$pattern" "$TARGET_FILE" 2>/dev/null; then
        echo "PASS: $description"
        ((PASS++))
    else
        echo "FAIL: $description"
        ((FAIL++))
    fi
}

echo "=== AC#3: Baseline Tracking Documentation ==="
echo "Target: $TARGET_FILE"
echo ""

run_test "Contains baseline recording requirement" \
    "pre-implementation test results.*recorded as a baseline"

run_test "Contains justification requirement for passing tests" \
    "tests passing at baseline require explicit justification"

run_test "Contains Baseline Tracking section" \
    "Baseline.*Tracking"

echo ""
echo "Results: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
