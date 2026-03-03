#!/bin/bash
# Test: AC#6 - Reference file preserves all examples, troubleshooting, and performance metrics
# Story: STORY-463
# Generated: 2026-02-21
# TDD Phase: RED - these tests MUST FAIL before refactoring (reference file doesn't exist yet)

PASSED=0
FAILED=0
REF_FILE="src/claude/skills/devforgeai-feedback/references/feedback-search-help.md"

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

echo "=== AC#6: Reference File Backward Compatibility (Examples, Troubleshooting, Performance) ==="
echo "Target: $REF_FILE"
echo ""

if [ ! -f "$REF_FILE" ]; then
    echo "  ERROR: Reference file not found: $REF_FILE"
    echo "  (Expected to fail - reference file not yet created)"
    # Count all expected failures
    EXPECTED_FAILURES=9
    echo "  Marking $EXPECTED_FAILURES tests as FAILED (file missing)"
    FAILED=$EXPECTED_FAILURES
    echo ""
    echo "=== Results: $PASSED passed, $FAILED failed ==="
    exit 1
fi

# === Tests 1-5: All 5 examples present ===
for i in 1 2 3 4 5; do
    grep -q "Example $i" "$REF_FILE"
    run_test "Reference file contains 'Example $i'" $?
done

# === Tests 6-8: All 3 troubleshooting scenarios present ===
# Check for 3 distinct troubleshooting entries (numbered or bulleted)
TROUBLE_COUNT=$(grep -c "^### \|^## \|^\*\*[0-9]\." "$REF_FILE" || true)
# Simpler: check Troubleshooting section has at least 3 distinct problem entries
TROUBLE_SECTION=$(sed -n '/^## Troubleshooting/,$ p' "$REF_FILE" 2>/dev/null || echo "")

# Check for common troubleshooting entry patterns
echo "$TROUBLE_SECTION" | grep -q "No results found\|no results\|No results"
run_test "Troubleshooting scenario 1 present (No results found)" $?

echo "$TROUBLE_SECTION" | grep -q "performance slow\|Search performance\|>2s"
run_test "Troubleshooting scenario 2 present (Search performance slow)" $?

echo "$TROUBLE_SECTION" | grep -q "Pagination\|pagination\|wrong page"
run_test "Troubleshooting scenario 3 present (Pagination wrong page count)" $?

# === Test 9: Performance metrics present ===
grep -qi "performance\|metric\|ms\|millisecond\|speed\|latency" "$REF_FILE"
run_test "Reference file contains Performance metrics" $?

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[ $FAILED -eq 0 ] && exit 0 || exit 1
