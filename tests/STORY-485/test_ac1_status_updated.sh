#!/bin/bash
# Test: AC#1 - ADR Status Updated
# Story: STORY-485
# Generated: 2026-02-23

PASSED=0
FAILED=0
ADR_FILE="devforgeai/specs/adrs/ADR-012-subagent-progressive-disclosure.md"

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

echo "=== AC#1: ADR Status Updated ==="

# Test 1: Status field shows Accepted (not Proposed)
grep -q "^\*\*Status:\*\* Accepted" "$ADR_FILE"
run_test "test_should_show_accepted_status_when_adr_updated" $?

# Test 2: Acceptance date is 2026-02-22
grep -q "2026-02-22" "$ADR_FILE"
run_test "test_should_contain_acceptance_date_when_status_accepted" $?

# Test 3: Status is NOT Proposed
grep -q "^\*\*Status:\*\* Proposed" "$ADR_FILE"
PROPOSED_FOUND=$?
if [ "$PROPOSED_FOUND" -ne 0 ]; then
    run_test "test_should_not_have_proposed_status_when_accepted" 0
else
    run_test "test_should_not_have_proposed_status_when_accepted" 1
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
