#!/bin/bash
# AC#1 Verification Script - STORY-454
# Phase output tags upgraded to nested XML with production instructions
# Run from project root: bash src/tests/results/STORY-454/test-ac1-phase-output-tags.sh

SKILL_FILE="src/claude/skills/discovering-requirements/SKILL.md"
PASSED=0
FAILED=0

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

echo "=== AC#1: Phase Output Tags Upgraded to Nested XML Structure ==="
echo "Target: $SKILL_FILE"
echo ""

# Test 1: phase-1-output contains nested XML child elements (not comma-separated)
grep -q '<problem-statement>' "$SKILL_FILE"
run_test "phase-1-output contains <problem-statement> nested element" $?

# Test 2: phase-1-output contains at least 4 nested child elements
count=$(grep -c '<\(problem-statement\|personas\|scope-boundaries\|project-type\)>' "$SKILL_FILE")
[ "$count" -ge 4 ]
run_test "phase-1-output has >= 4 nested XML child elements (found: $count)" $?

# Test 3: phase-2-output contains nested XML child elements
grep -q '<functional-requirements>' "$SKILL_FILE"
run_test "phase-2-output contains <functional-requirements> nested element" $?

# Test 4: phase-2-output contains at least 4 nested child elements
count=$(grep -c '<\(functional-requirements\|nfr-requirements\|data-models\|integrations\)>' "$SKILL_FILE")
[ "$count" -ge 4 ]
run_test "phase-2-output has >= 4 nested XML child elements (found: $count)" $?

# Test 5: phase-3-output contains nested XML child elements
grep -q '<requirements-md-path>' "$SKILL_FILE"
run_test "phase-3-output contains <requirements-md-path> nested element" $?

# Test 6: phase-3-output contains at least 4 nested child elements
count=$(grep -c '<\(requirements-md-path\|yaml-schema-valid\|completion-summary\|next-action\)>' "$SKILL_FILE")
[ "$count" -ge 4 ]
run_test "phase-3-output has >= 4 nested XML child elements (found: $count)" $?

# Test 7: Production instruction line before each phase output tag
count=$(grep -c 'produce your output' "$SKILL_FILE")
[ "$count" -ge 3 ]
run_test "Production instruction present for >= 3 phase output blocks (found: $count)" $?

# Test 8: No phase-4-output tag exists (removed or merged)
! grep -q '<phase-4-output>' "$SKILL_FILE"
run_test "No standalone phase-4-output tag exists" $?

# Test 9: No underscore-delimited XML tags within phase-N-output blocks
# Extract only lines between phase-N-output tags and check for underscores
underscore_in_phase_tags=$(sed -n '/<phase-[0-9]-output>/,/<\/phase-[0-9]-output>/p' "$SKILL_FILE" | grep -c '<[a-z]*_[a-z]*>')
[ "$underscore_in_phase_tags" -eq 0 ]
run_test "No underscore-delimited XML element names within phase output tags (found: $underscore_in_phase_tags)" $?

# Test 10: SKILL.md line count <= 500
line_count=$(wc -l < "$SKILL_FILE")
[ "$line_count" -le 500 ]
run_test "SKILL.md line count <= 500 (actual: $line_count)" $?

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="

if [ "$FAILED" -gt 0 ]; then
    exit 1
else
    exit 0
fi
