#!/bin/bash
# Test: STORY-445 - Create Multishot Examples Reference File
# Generated: 2026-02-18
# TDD Phase: RED (all tests expected to FAIL initially)

set -uo pipefail

PASSED=0
FAILED=0
TOTAL=0

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SRC_SKILL_DIR="$PROJECT_ROOT/src/claude/skills/discovering-requirements"
EXAMPLES_FILE="$SRC_SKILL_DIR/references/examples.md"
OUTPUT_TEMPLATES_FILE="$SRC_SKILL_DIR/references/output-templates.md"
DOMAIN_PATTERNS_FILE="$SRC_SKILL_DIR/references/domain-specific-patterns.md"
SKILL_FILE="$SRC_SKILL_DIR/SKILL.md"

run_test() {
    local name="$1"
    local result="$2"
    ((TOTAL++))
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=========================================="
echo "STORY-445: Multishot Examples Reference File"
echo "=========================================="
echo ""

# =============================================
# AC#1: examples.md exists with 2-3 multishot examples in XML <example> tags
# =============================================
echo "--- AC#1: examples.md file existence and structure ---"

# Test 1.1: File exists
test_result=0
[ -f "$EXAMPLES_FILE" ] || test_result=1
run_test "AC1: examples.md file exists" $test_result

# Test 1.2: Contains at least 2 <example> tags
test_result=0
count=$(grep -cE '<example[ >]' "$EXAMPLES_FILE" 2>/dev/null || echo "0")
[ "$count" -ge 2 ] || test_result=1
run_test "AC1: Contains at least 2 <example> tags (found: $count)" $test_result

# Test 1.3: Contains no more than 3 <example> tags
test_result=0
count=$(grep -cE '<example[ >]' "$EXAMPLES_FILE" 2>/dev/null || echo "0")
[ "$count" -le 3 ] || test_result=1
run_test "AC1: Contains no more than 3 <example> tags (found: $count)" $test_result

# Test 1.4: Each <example> has matching </example> closing tag
test_result=0
open_count=$(grep -cE '<example[ >]' "$EXAMPLES_FILE" 2>/dev/null || echo "0")
close_count=$(grep -c '</example>' "$EXAMPLES_FILE" 2>/dev/null || echo "0")
[ "$open_count" -eq "$close_count" ] && [ "$open_count" -gt 0 ] || test_result=1
run_test "AC1: All <example> tags properly closed (open=$open_count, close=$close_count)" $test_result

# =============================================
# AC#2: Examples cover three scenarios (discovery, epic decomposition, complexity)
# =============================================
echo ""
echo "--- AC#2: Three scenario coverage ---"

# Test 2.1: Contains discovery session / Phase 1 example
test_result=0
grep -qi 'discovery\|phase.1\|elicitation' "$EXAMPLES_FILE" 2>/dev/null || test_result=1
run_test "AC2: Contains discovery session (Phase 1) content" $test_result

# Test 2.2: Contains epic decomposition / Phase 2 example
test_result=0
grep -qi 'epic.decomposition\|phase.2\|decompos' "$EXAMPLES_FILE" 2>/dev/null || test_result=1
run_test "AC2: Contains epic decomposition (Phase 2) content" $test_result

# Test 2.3: Contains complexity scoring / Phase 3 example
test_result=0
grep -qi 'complexity.scor\|phase.3\|complexity.assess' "$EXAMPLES_FILE" 2>/dev/null || test_result=1
run_test "AC2: Contains complexity scoring (Phase 3) content" $test_result

# =============================================
# AC#3: Each example has <input> and <output> sections
# =============================================
echo ""
echo "--- AC#3: Input/Output sections in examples ---"

# Test 3.1: Contains <input> tags
test_result=0
input_count=$(grep -c '<input>' "$EXAMPLES_FILE" 2>/dev/null || echo "0")
[ "$input_count" -ge 2 ] || test_result=1
run_test "AC3: Contains at least 2 <input> sections (found: $input_count)" $test_result

# Test 3.2: Contains <output> tags
test_result=0
output_count=$(grep -c '<output>' "$EXAMPLES_FILE" 2>/dev/null || echo "0")
[ "$output_count" -ge 2 ] || test_result=1
run_test "AC3: Contains at least 2 <output> sections (found: $output_count)" $test_result

# Test 3.3: Input and output counts match (each example has both)
test_result=0
input_count=$(grep -c '<input>' "$EXAMPLES_FILE" 2>/dev/null || echo "0")
output_count=$(grep -c '<output>' "$EXAMPLES_FILE" 2>/dev/null || echo "0")
[ "$input_count" -eq "$output_count" ] && [ "$input_count" -gt 0 ] || test_result=1
run_test "AC3: Equal <input> and <output> counts (input=$input_count, output=$output_count)" $test_result

# Test 3.4: Closing tags present for input/output
test_result=0
input_close=$(grep -c '</input>' "$EXAMPLES_FILE" 2>/dev/null || echo "0")
output_close=$(grep -c '</output>' "$EXAMPLES_FILE" 2>/dev/null || echo "0")
[ "$input_close" -ge 2 ] && [ "$output_close" -ge 2 ] || test_result=1
run_test "AC3: Closing tags for <input> and <output> present" $test_result

# =============================================
# AC#4: output-templates.md has Completion Summary example
# =============================================
echo ""
echo "--- AC#4: Completion Summary in output-templates.md ---"

# Test 4.1: output-templates.md exists
test_result=0
[ -f "$OUTPUT_TEMPLATES_FILE" ] || test_result=1
run_test "AC4: output-templates.md file exists" $test_result

# Test 4.2: Contains Completion Summary section
test_result=0
grep -qi 'completion.summary' "$OUTPUT_TEMPLATES_FILE" 2>/dev/null || test_result=1
run_test "AC4: Contains 'Completion Summary' section" $test_result

# Test 4.3: Contains realistic data (numbers, percentages, or metrics)
test_result=0
grep -qE '[0-9]+%|[0-9]+ (stories|features|points|sprints)' "$OUTPUT_TEMPLATES_FILE" 2>/dev/null || test_result=1
run_test "AC4: Completion Summary contains realistic data (metrics/numbers)" $test_result

# =============================================
# AC#5: domain-specific-patterns.md has Usage Example section
# =============================================
echo ""
echo "--- AC#5: Usage Example in domain-specific-patterns.md ---"

# Test 5.1: domain-specific-patterns.md exists
test_result=0
[ -f "$DOMAIN_PATTERNS_FILE" ] || test_result=1
run_test "AC5: domain-specific-patterns.md file exists" $test_result

# Test 5.2: Contains "Usage Example" section
test_result=0
grep -qi 'usage.example' "$DOMAIN_PATTERNS_FILE" 2>/dev/null || test_result=1
run_test "AC5: Contains 'Usage Example' section" $test_result

# Test 5.3: Usage Example shows pattern guiding elicitation
test_result=0
grep -qi 'elicit\|pattern\|guide\|domain' "$DOMAIN_PATTERNS_FILE" 2>/dev/null || test_result=1
run_test "AC5: Usage Example demonstrates pattern-guided elicitation" $test_result

# =============================================
# AC#6: SKILL.md references examples.md with Read() directives
# =============================================
echo ""
echo "--- AC#6: SKILL.md references examples.md ---"

# Test 6.1: SKILL.md exists
test_result=0
[ -f "$SKILL_FILE" ] || test_result=1
run_test "AC6: SKILL.md file exists" $test_result

# Test 6.2: SKILL.md references examples.md
test_result=0
grep -q 'examples\.md' "$SKILL_FILE" 2>/dev/null || test_result=1
run_test "AC6: SKILL.md references examples.md" $test_result

# Test 6.3: SKILL.md contains Read() directive for examples.md
test_result=0
grep -q 'Read.*examples\.md' "$SKILL_FILE" 2>/dev/null || test_result=1
run_test "AC6: SKILL.md contains Read() directive for examples.md" $test_result

# =============================================
# Summary
# =============================================
echo ""
echo "=========================================="
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "=========================================="

[ $FAILED -eq 0 ] && exit 0 || exit 1
