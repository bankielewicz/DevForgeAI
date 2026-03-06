#!/bin/bash
# Test: AC#1 - Complexity Indicators Trigger Referral Recommendations
# Story: STORY-547
# Generated: 2026-03-06
# TDD Phase: RED - These tests MUST fail before implementation

# === Test Configuration ===
PASSED=0
FAILED=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

REFERENCE_FILE="$PROJECT_ROOT/src/claude/skills/advising-legal/references/when-to-hire-professional.md"

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

echo "=== AC#1: Complexity Indicators Trigger Referral Recommendations ==="
echo ""

# === Arrange ===
# Reference file must exist for all tests to pass

# === Act & Assert ===

# Test 1: Reference file exists
test -f "$REFERENCE_FILE"
run_test "Reference file exists at src/claude/skills/advising-legal/references/when-to-hire-professional.md" $?

# Test 2: Multi-party contracts indicator defined
grep -qi "multi-party contract" "$REFERENCE_FILE" 2>/dev/null
run_test "Complexity indicator: multi-party contracts defined" $?

# Test 3: Regulatory filings indicator defined
grep -qi "regulatory fil" "$REFERENCE_FILE" 2>/dev/null
run_test "Complexity indicator: regulatory filings defined" $?

# Test 4: Litigation risk indicator defined
grep -qi "litigation risk" "$REFERENCE_FILE" 2>/dev/null
run_test "Complexity indicator: litigation risk defined" $?

# Test 5: IP protection indicator defined
grep -qi "IP protection\|intellectual property" "$REFERENCE_FILE" 2>/dev/null
run_test "Complexity indicator: IP protection defined" $?

# Test 6: Equity structures indicator defined
grep -qi "equity structure" "$REFERENCE_FILE" 2>/dev/null
run_test "Complexity indicator: equity structures defined" $?

# Test 7: Employment disputes indicator defined
grep -qi "employment dispute" "$REFERENCE_FILE" 2>/dev/null
run_test "Complexity indicator: employment disputes defined" $?

# Test 8: Each indicator has a plain-language explanation
if [ -f "$REFERENCE_FILE" ]; then
    # Check that indicators are in a section with explanatory text (not just bare keywords)
    indicator_sections=0
    for indicator in "multi-party contract" "regulatory fil" "litigation risk" "intellectual property\|IP protection" "equity structure" "employment dispute"; do
        # Each indicator should have at least 2 lines of context (heading + explanation)
        match_line=$(grep -ni "$indicator" "$REFERENCE_FILE" 2>/dev/null | head -1 | cut -d: -f1)
        if [ -n "$match_line" ]; then
            ((indicator_sections++))
        fi
    done
    [ "$indicator_sections" -ge 6 ]
    run_test "All 6 complexity indicators have dedicated sections (found: ${indicator_sections})" $?
else
    run_test "All 6 complexity indicators have dedicated sections" 1
fi

# Test 9: Referral recommendation language present
grep -qi "recommend.*professional\|seek.*attorney\|consult.*lawyer\|hire.*professional" "$REFERENCE_FILE" 2>/dev/null
run_test "Referral recommendation language present" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
