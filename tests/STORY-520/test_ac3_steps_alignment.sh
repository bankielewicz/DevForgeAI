#!/bin/bash
# Test: AC#3 - Checklist Items Map to steps_required Entries
# Story: STORY-520
# Generated: 2026-03-01

set -euo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/SKILL.md"

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

echo "=== AC#3: Checklist Items Map to steps_required ==="
echo ""

# Extract Phase 1.5 Completion Checklist section
SECTION=$(awk '/^### Phase 1\.5 Completion Checklist/{found=1; next} found && /^##/{found=0} found{print}' "$TARGET_FILE")

if [ -z "$SECTION" ]; then
    run_test "Phase 1.5 Completion Checklist section exists (prerequisite)" 1
    echo ""
    echo "Results: $PASSED passed, $FAILED failed"
    exit 1
fi
run_test "Phase 1.5 Completion Checklist section exists" 0

# === Test 1: steps_required entry "diff_regression_detection" has corresponding checklist item ===
# The checklist must reference diff regression detection (Steps 1-5)
echo "$SECTION" | grep -qi "diff regression" && R=0 || R=1
run_test "Checklist maps to steps_required 'diff_regression_detection'" $R

# === Test 2: steps_required entry "test_integrity_verification" has corresponding checklist item ===
# The checklist must reference test integrity verification (snapshot/checksum)
echo "$SECTION" | grep -qi "test integrity" && R=0 || R=1
run_test "Checklist maps to steps_required 'test_integrity_verification'" $R

# === Test 3: Both steps_required entries are covered (comprehensive check) ===
DIFF_COUNT=$(echo "$SECTION" | grep -ci "diff regression" || true)
INTEGRITY_COUNT=$(echo "$SECTION" | grep -ci "test integrity\|checksum" || true)

if [ "$DIFF_COUNT" -ge 1 ] && [ "$INTEGRITY_COUNT" -ge 1 ]; then
    run_test "Both steps_required entries have at least one corresponding checklist item" 0
else
    run_test "Both steps_required entries have at least one corresponding checklist item (diff=$DIFF_COUNT, integrity=$INTEGRITY_COUNT)" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
