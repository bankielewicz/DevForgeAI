#!/bin/bash
# Test: AC#3 - Rollback Capability Verified Through Live Exercise
# Story: STORY-398
# Generated: 2026-02-13

set -euo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/devforgeai/feedback/ai-analysis/STORY-398/rollback-validation.md"

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

echo "=== AC#3: Rollback Capability Verified ==="
echo ""

# --- Arrange ---
# Target: rollback-validation.md at documented path

# --- Act & Assert ---

# Test 1: rollback-validation.md file exists
test -f "$TARGET_FILE"
run_test "rollback-validation.md exists" $?

# Test 2: Contains git commit hash (7+ hex chars)
grep -qE '[0-9a-f]{7,40}' "$TARGET_FILE"
run_test "Contains git commit hash" $?

# Test 3: Contains rollback success confirmation
grep -qi "rollback.*succeed\|rollback.*success\|revert.*success" "$TARGET_FILE"
run_test "Rollback succeeded confirmation present" $?

# Test 4: Component was re-migrated after rollback
grep -qi "re-migrat\|forward.fix\|restored.*migrated" "$TARGET_FILE"
run_test "Component re-migrated after rollback test" $?

# Test 5: Contains timestamp documentation
grep -qE '[0-9]{4}-[0-9]{2}-[0-9]{2}' "$TARGET_FILE"
run_test "Contains timestamp (date format)" $?

# Test 6: Post-rollback functionality confirmed
grep -qi "function.*correct\|post.rollback.*pass\|test.*pass" "$TARGET_FILE"
run_test "Post-rollback functionality confirmed" $?

# Test 7: No dangling references documented
grep -qi "no.*dangling\|no.*broken.*depend\|dependencies.*intact" "$TARGET_FILE"
run_test "No dangling references confirmed" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
