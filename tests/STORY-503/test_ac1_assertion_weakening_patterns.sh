#!/bin/bash
# Test: AC#1 - Assertion Weakening Detection
# Story: STORY-503
# Generated: 2026-02-27

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/references/test-tampering-heuristics.md"

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

echo "=== AC#1: Assertion Weakening Detection ==="

# === Test 1: Reference file exists ===
test -f "$TARGET_FILE"
run_test "test-tampering-heuristics.md reference file exists" $?

# === Test 2: Contains assertion_weakening_patterns section ===
grep -q -i "assertion.weakening.pattern" "$TARGET_FILE" 2>/dev/null
run_test "Contains assertion_weakening_patterns section" $?

# === Test 3: Documents toBe to toBeTruthy pattern ===
grep -q "toBe.*toBeTruthy" "$TARGET_FILE" 2>/dev/null
run_test "Documents toBe to toBeTruthy weakening pattern" $?

# === Test 4: Documents assertEqual to assertIn pattern ===
grep -q "assertEqual.*assertIn" "$TARGET_FILE" 2>/dev/null
run_test "Documents assertEqual to assertIn weakening pattern" $?

# === Test 5: Documents assertEquals to assertTrue pattern ===
grep -q "assertEquals.*assertTrue" "$TARGET_FILE" 2>/dev/null
run_test "Documents assertEquals to assertTrue weakening pattern" $?

# === Test 6: Documents exact to contains pattern ===
grep -q -i "exact.*contains" "$TARGET_FILE" 2>/dev/null
run_test "Documents exact to contains weakening pattern" $?

# === Test 7: Documents strict to loose pattern ===
grep -q -i "strict.*loose" "$TARGET_FILE" 2>/dev/null
run_test "Documents strict to loose weakening pattern" $?

# === Test 8: All marked CRITICAL severity ===
grep -i "assertion.weakening" "$TARGET_FILE" 2>/dev/null | grep -q -i "critical"
run_test "Assertion weakening patterns marked CRITICAL severity" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
