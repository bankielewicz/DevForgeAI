#!/bin/bash
# Test: AC#3 - Trade Secrets Section Covers Code and Algorithm Protection
# Story: STORY-545
# Generated: 2026-03-05
# TDD Phase: RED - These tests MUST fail before implementation

# === Test Configuration ===
PASSED=0
FAILED=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

REFERENCE_FILE="$PROJECT_ROOT/src/claude/skills/advising-legal/references/ip-protection-checklist.md"

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

echo "=== AC#3: Trade Secrets Section Covers Code and Algorithm Protection ==="
echo ""

# === Arrange ===
# Reference file must exist

# === Act & Assert ===

# Test 1: Reference file exists (prerequisite)
test -f "$REFERENCE_FILE"
run_test "Reference file exists" $?

# Test 2: Software-specific example - algorithms
grep -qi "algorithm" "$REFERENCE_FILE" 2>/dev/null
run_test "Covers software-specific example: algorithms" $?

# Test 3: Software-specific example - model weights
grep -qi "model weight" "$REFERENCE_FILE" 2>/dev/null
run_test "Covers software-specific example: model weights" $?

# Test 4: Software-specific example - database schemas
grep -qi "database schema" "$REFERENCE_FILE" 2>/dev/null
run_test "Covers software-specific example: database schemas" $?

# Test 5: Software-specific example - business logic
grep -qi "business logic" "$REFERENCE_FILE" 2>/dev/null
run_test "Covers software-specific example: business logic" $?

# Test 6: Protective measure - NDAs
grep -qi "NDA" "$REFERENCE_FILE" 2>/dev/null
run_test "Lists protective measure: NDAs" $?

# Test 7: Protective measure - access controls
grep -qi "access control" "$REFERENCE_FILE" 2>/dev/null
run_test "Lists protective measure: access controls" $?

# Test 8: Public disclosure warning
grep -qiE "public.*disclos|disclos.*public|lost.*disclos|disclos.*lost" "$REFERENCE_FILE" 2>/dev/null
run_test "Warns protection is lost if publicly disclosed" $?

# Test 9: Attorney consultation recommendation for NDA
grep -qiE "attorney|lawyer|legal counsel|legal professional" "$REFERENCE_FILE" 2>/dev/null
run_test "Recommends attorney consultation for NDA drafting" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
