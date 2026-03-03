#!/bin/bash
# Test: AC#2 - Anomaly Investigation Guidance
# Story: STORY-484
# Verifies: test-automator.md contains investigation guidance for passing RED phase tests

set -uo pipefail

TARGET_FILE="src/claude/agents/test-automator.md"
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

echo "=== AC#2: Anomaly Investigation Guidance ==="
echo "Target: $TARGET_FILE"
echo ""

run_test "Contains guidance to check existing code satisfies the test" \
    "existing code already satisfies"

run_test "Contains guidance to verify assertion specificity" \
    "assertion specificity"

run_test "Contains guidance to confirm test targets new behavior" \
    "targets new.*behavior"

echo ""
echo "Results: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
