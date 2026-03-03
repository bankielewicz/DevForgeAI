#!/bin/bash
# Test: AC#1 - Step 6 Added to Phase 1.5
# Story: STORY-518
# Generated: 2026-03-01

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-qa/SKILL.md"

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

echo "=== AC#1: Step 6 Added to Phase 1.5 ==="
echo ""

# Verify target file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file not found: $TARGET_FILE"
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# Test 1: Phase 1.5 contains an explicit step labeled for Test Integrity Verification
# The step must be its own numbered step (not embedded in another step)
grep -q "Step 1\.5\.[0-9].*Test Integrity Verification" "$TARGET_FILE"
run_test "Phase 1.5 contains dedicated numbered step for Test Integrity Verification" $?

# Test 2: Step 6 reads snapshot from devforgeai/qa/snapshots path
grep -q "devforgeai/qa/snapshots/.*red-phase-checksums\.json" "$TARGET_FILE"
run_test "Step reads red-phase-checksums.json from snapshots path" $?

# Test 3: SHA-256 comparison instruction (sha256sum command or SHA-256 reference)
grep -q "sha256sum" "$TARGET_FILE"
run_test "Contains sha256sum comparison instruction" $?

# Test 4: CRITICAL TEST TAMPERING finding for mismatches
grep -q "CRITICAL.*TEST TAMPERING" "$TARGET_FILE"
run_test "Contains CRITICAL TEST TAMPERING finding for mismatches" $?

# Test 5: test_integrity: PASS for all matches
grep -q "test_integrity.*PASS" "$TARGET_FILE"
run_test "Contains test_integrity: PASS result for all matches" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
