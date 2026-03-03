#!/usr/bin/env bash
# STORY-404 AC#4: Aggregated report format identical to single-pass
# TDD Red Phase - These tests MUST fail before implementation
#
# Validates that the ac-compliance-verifier specification documents:
# - Report aggregation after chunked verification
# - total_acs field correctly represents all ACs
# - ACs maintained in document order
# - overall_status correctly determined across chunks
# - Output JSON schema matches existing single-pass schema
#
# Expected: FAIL initially (chunking logic not yet in verifier spec)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VERIFIER_FILE="${PROJECT_ROOT}/src/claude/agents/ac-compliance-verifier.md"

PASS=0
FAIL=0
TOTAL=0

run_test() {
    local name="$1"
    local result="$2"
    TOTAL=$((TOTAL + 1))
    if [ "$result" -eq 0 ]; then
        PASS=$((PASS + 1))
        echo "  PASS: $name"
    else
        FAIL=$((FAIL + 1))
        echo "  FAIL: $name"
    fi
}

echo "=== AC#4: Aggregated Report Format Identical to Single-Pass ==="
echo ""

# Test 1: Verifier source file exists
if [ -f "$VERIFIER_FILE" ]; then
    run_test "Verifier source file exists" 0
else
    run_test "Verifier source file exists" 1
    echo "--- AC#4 Results: $PASS/$TOTAL passed, $FAIL failed ---"
    exit 1
fi

# Test 2: Spec documents report aggregation from chunked results
if grep -qiP 'aggregat|merge.*chunk.*result|combine.*chunk|assemble.*report|consolidat.*chunk' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec documents report aggregation from chunks" 0
else
    run_test "Spec documents report aggregation from chunks" 1
fi

# Test 3: Spec ensures total_acs reflects all ACs (not just chunk count)
if grep -qiP 'total_acs.*correct|total_acs.*all|total_acs.*sum|count.*all.*ACs' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec ensures total_acs reflects all ACs" 0
else
    run_test "Spec ensures total_acs reflects all ACs" 1
fi

# Test 4: Spec ensures ACs maintained in document order
if grep -qiP 'document order|original order|preserve.*order|maintain.*order|sequential.*order' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec ensures ACs maintained in document order" 0
else
    run_test "Spec ensures ACs maintained in document order" 1
fi

# Test 5: Spec documents overall_status determination across chunks
if grep -qiP 'overall_status.*chunk|status.*across.*chunk|determine.*overall.*status|PASS.*PARTIAL.*FAIL.*chunk' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec documents overall_status determination across chunks" 0
else
    run_test "Spec documents overall_status determination across chunks" 1
fi

# Test 6: Spec states output schema matches single-pass (identical format)
if grep -qiP 'identical.*schema|same.*schema|schema.*unchanged|format.*identical|match.*single.pass' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec states output schema matches single-pass format" 0
else
    run_test "Spec states output schema matches single-pass format" 1
fi

echo ""
echo "--- AC#4 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
