#!/bin/bash
# Test AC#1: SKILL.md Documents Treelint Integration
# STORY-378: Update devforgeai-qa Skill for Treelint
#
# Validates:
# - SKILL.md contains "## Treelint Integration" section heading
# - Section has step-to-subagent mapping table with Steps 2.1, 2.2, 2.4
# - Table lists all 5 Treelint-enabled subagents
# - Section mentions token reduction benefit (40-80%)
# - Section states automatic detection/fallback
# - Section references shared Treelint reference file path
# - Section size under 2000 characters (NFR-002)
#
# Expected: FAIL initially (TDD Red phase - SKILL.md has no Treelint Integration section)

# Configuration - tests run against src/ tree per CLAUDE.md
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-qa/SKILL.md"

# Test tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() { TESTS_PASSED=$((TESTS_PASSED + 1)); echo "[PASS] $1"; }
fail_test() { TESTS_FAILED=$((TESTS_FAILED + 1)); echo "[FAIL] $1: $2"; }
run_test() { TESTS_RUN=$((TESTS_RUN + 1)); shift; "$@"; }

# Extract Treelint Integration section content
get_section() {
    sed -n '/^## Treelint Integration/,/^## /p' "$SKILL_FILE" | head -n -1
}

# Test 1: SKILL.md file exists
test_skill_file_exists() {
    if [ -f "$SKILL_FILE" ]; then pass_test "SKILL.md file exists"
    else fail_test "SKILL.md file exists" "File not found: $SKILL_FILE"; fi
}

# Test 2: Contains Treelint Integration section heading
test_treelint_heading() {
    if grep -q "^## Treelint Integration" "$SKILL_FILE"; then
        pass_test "Contains Treelint Integration section heading"
    else
        fail_test "Contains Treelint Integration section heading" "No '## Treelint Integration' heading found"
    fi
}

# Test 3: Step-to-subagent mapping table exists with Step 2.1
test_step_2_1_mapping() {
    local section; section=$(get_section)
    if echo "$section" | grep -q "2\.1.*anti-pattern-scanner"; then
        pass_test "Table maps Step 2.1 to anti-pattern-scanner"
    else
        fail_test "Table maps Step 2.1 to anti-pattern-scanner" "No Step 2.1 -> anti-pattern-scanner mapping found"
    fi
}

# Test 4: Table maps Step 2.2 to test-automator, code-reviewer, security-auditor
test_step_2_2_mapping() {
    local section; section=$(get_section)
    local found=0
    echo "$section" | grep -q "2\.2.*test-automator" && found=$((found + 1))
    echo "$section" | grep -q "2\.2.*code-reviewer" && found=$((found + 1))
    echo "$section" | grep -q "2\.2.*security-auditor" && found=$((found + 1))
    if [ "$found" -eq 3 ]; then
        pass_test "Table maps Step 2.2 to test-automator, code-reviewer, security-auditor"
    else
        fail_test "Table maps Step 2.2 to test-automator, code-reviewer, security-auditor" "Only $found/3 subagents found for Step 2.2"
    fi
}

# Test 5: Table maps Step 2.4 to coverage-analyzer
test_step_2_4_mapping() {
    local section; section=$(get_section)
    if echo "$section" | grep -q "2\.4.*coverage-analyzer"; then
        pass_test "Table maps Step 2.4 to coverage-analyzer"
    else
        fail_test "Table maps Step 2.4 to coverage-analyzer" "No Step 2.4 -> coverage-analyzer mapping found"
    fi
}

# Test 6: Mentions token reduction benefit (40-80%)
test_token_reduction() {
    local section; section=$(get_section)
    if echo "$section" | grep -qE "(40-80%|token.*(reduction|saving))"; then
        pass_test "Mentions token reduction benefit"
    else
        fail_test "Mentions token reduction benefit" "No token reduction (40-80%) mentioned"
    fi
}

# Test 7: States automatic detection
test_automatic_detection() {
    local section; section=$(get_section)
    if echo "$section" | grep -qi "automatic.*detect\|detect.*automatic\|auto.*fallback"; then
        pass_test "States automatic detection and fallback"
    else
        fail_test "States automatic detection and fallback" "No automatic detection statement found"
    fi
}

# Test 8: References shared Treelint reference file path
test_shared_reference_path() {
    local section; section=$(get_section)
    if echo "$section" | grep -q "treelint-search-patterns"; then
        pass_test "References shared Treelint reference file path"
    else
        fail_test "References shared Treelint reference file path" "No treelint-search-patterns reference found"
    fi
}

# Test 9: Section size under 2000 characters (NFR-002)
test_section_size() {
    local section; section=$(get_section)
    if [ -z "$section" ]; then
        fail_test "Section size under 2000 chars" "Section not found"
        return
    fi
    local chars; chars=$(echo "$section" | wc -c)
    if [ "$chars" -le 2000 ]; then
        pass_test "Section size under 2000 chars (actual: $chars)"
    else
        fail_test "Section size under 2000 chars" "Section has $chars characters (max: 2000)"
    fi
}

# Main execution
echo "=============================================="
echo "STORY-378 AC#1: SKILL.md Treelint Integration"
echo "=============================================="
echo "Target: $SKILL_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_skill_file_exists
run_test "2" test_treelint_heading
run_test "3" test_step_2_1_mapping
run_test "4" test_step_2_2_mapping
run_test "5" test_step_2_4_mapping
run_test "6" test_token_reduction
run_test "7" test_automatic_detection
run_test "8" test_shared_reference_path
run_test "9" test_section_size

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi
