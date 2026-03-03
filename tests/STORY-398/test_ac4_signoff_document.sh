#!/bin/bash
# Test: AC#4 - Migration Completion Sign-Off Document Created
# Story: STORY-398
# Generated: 2026-02-13

set -euo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/devforgeai/specs/EPIC-062-migration-signoff.md"

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

echo "=== AC#4: Migration Sign-Off Document ==="
echo ""

# --- Arrange ---
# Target: EPIC-062-migration-signoff.md at documented path

# --- Act & Assert ---

# Test 1: Sign-off document exists
test -f "$TARGET_FILE"
run_test "EPIC-062-migration-signoff.md exists" $?

# Test 2: Contains executive summary section
grep -qi "executive summary" "$TARGET_FILE"
run_test "Contains executive summary section" $?

# Test 3: References total component counts (39 agents + 17 skills + 39 commands = 95)
grep -qE "(39 agents|17 skills|39 commands|95 components)" "$TARGET_FILE"
run_test "References total component counts" $?

# Test 4: Contains quality metrics section
grep -qi "quality metrics" "$TARGET_FILE"
run_test "Contains quality metrics section" $?

# Test 5: Contains regression test pass rate
grep -qi "regression.*pass\|pass.*rate.*100" "$TARGET_FILE"
run_test "Contains regression test pass rate" $?

# Test 6: Contains rollback capability confirmation
grep -qi "rollback.*capabilit\|rollback.*confirm\|rollback.*verif" "$TARGET_FILE"
run_test "Contains rollback capability confirmation" $?

# Test 7: Contains risk assessment section
grep -qi "risk assessment" "$TARGET_FILE"
run_test "Contains risk assessment section" $?

# Test 8: Contains sign-off statement with COMPLETE declaration
grep -q "EPIC-062 migration declared COMPLETE" "$TARGET_FILE"
run_test "Contains EPIC-062 COMPLETE declaration" $?

# Test 9: Sign-off statement includes date
grep -E "EPIC-062 migration declared COMPLETE" "$TARGET_FILE" | grep -qE '[0-9]{4}-[0-9]{2}-[0-9]{2}'
run_test "Sign-off statement includes ISO date" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
