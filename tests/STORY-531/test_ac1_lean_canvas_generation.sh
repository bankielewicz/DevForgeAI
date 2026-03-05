#!/bin/bash
# Test: AC#1 - Complete Lean Canvas Generation
# Story: STORY-531
# Generated: 2026-03-04

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/planning-business/SKILL.md"
REF_FILE="$PROJECT_ROOT/src/claude/skills/planning-business/references/lean-canvas-workflow.md"

PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED+1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED+1))
    fi
}

echo "=== AC#1: Complete Lean Canvas Generation ==="

# Test 1: SKILL.md exists
test -f "$SKILL_FILE"
run_test "SKILL.md exists" $?

# Test 2: Reference file exists
test -f "$REF_FILE"
run_test "lean-canvas-workflow.md exists" $?

# Test 3: SKILL.md defines a Lean Canvas phase with AskUserQuestion interaction
grep -q "### Phase 1: Lean Canvas" "$SKILL_FILE" 2>/dev/null
run_test "SKILL.md defines Phase 1: Lean Canvas" $?

grep -q "AskUserQuestion" "$SKILL_FILE" 2>/dev/null
run_test "SKILL.md references AskUserQuestion interaction pattern" $?

# Test 4: Output path is referenced in SKILL.md
grep -q "devforgeai/specs/business/business-plan/lean-canvas.md" "$SKILL_FILE" 2>/dev/null
run_test "SKILL.md references output path lean-canvas.md" $?

# Test 5: Reference file Section 3 contains all 9 blocks in the table
SECTION3=$(sed -n '/^## 3\. /,/^## [0-9]/p' "$REF_FILE" | head -n -1)

BLOCK_ORDER=("Problem" "Customer Segments" "Unique Value Proposition" "Solution" "Channels" "Revenue Streams" "Cost Structure" "Key Metrics" "Unfair Advantage")

for block in "${BLOCK_ORDER[@]}"; do
    echo "$SECTION3" | grep -q "| $block |"
    run_test "Section 3 contains block in table: $block" $?
done

# Test 6: Verify exactly 9 data rows in the block table (exclude header row starting with | Block)
TABLE_BLOCK_COUNT=$(echo "$SECTION3" | grep "^| " | grep -cv "^| Block " 2>/dev/null || true)
test "$TABLE_BLOCK_COUNT" -eq 9
run_test "Section 3 block table has exactly 9 data entries (got $TABLE_BLOCK_COUNT)" $?

# Test 7: AskUserQuestion appears in reference file workflow
grep -q "AskUserQuestion" "$REF_FILE" 2>/dev/null
run_test "Reference file uses AskUserQuestion for block interaction" $?

# Test 8: Output format section (Section 6) has 9 ## block headers
OUTPUT_HEADERS=$(sed -n '/^## 6\. Output Format/,/^## [0-9]/p' "$REF_FILE" | grep -c "^## [A-Z]" 2>/dev/null || true)
test "$OUTPUT_HEADERS" -eq 9
run_test "Output format section has 9 ## block headers (got $OUTPUT_HEADERS)" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
