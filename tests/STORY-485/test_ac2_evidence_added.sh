#!/bin/bash
# Test: AC#2 - Implementation Evidence Added
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

echo "=== AC#2: Implementation Evidence Added ==="

# Test 1: Implementation Evidence section exists
grep -q "## Implementation Evidence" "$ADR_FILE"
run_test "test_should_have_implementation_evidence_section_when_accepted" $?

# Test 2: At least 20 agent citations (lines containing .md agent references)
AGENT_COUNT=$(grep -c "\.claude/agents/.*\.md" "$ADR_FILE" 2>/dev/null || echo "0")
if [ "$AGENT_COUNT" -ge 20 ]; then
    run_test "test_should_cite_at_least_20_agents_when_evidence_added" 0
else
    echo "    (Found $AGENT_COUNT agent citations, need >= 20)"
    run_test "test_should_cite_at_least_20_agents_when_evidence_added" 1
fi

# Test 3: Citations include specific file references (not just agent names)
grep -q "references/" "$ADR_FILE"
run_test "test_should_include_specific_file_references_when_evidence_cited" $?

# Test 4: Evidence references progressive disclosure pattern usage
grep -qi "progressive.disclosure" "$ADR_FILE" | head -1 > /dev/null 2>&1
# Check within Implementation Evidence section specifically
EVIDENCE_SECTION=$(sed -n '/## Implementation Evidence/,/^## /p' "$ADR_FILE" 2>/dev/null)
if echo "$EVIDENCE_SECTION" | grep -qi "progressive.disclosure"; then
    run_test "test_should_reference_progressive_disclosure_in_evidence_section" 0
else
    run_test "test_should_reference_progressive_disclosure_in_evidence_section" 1
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
