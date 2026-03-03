#!/bin/bash
# Test AC#4: Coverage Analysis References Treelint Mapping
# STORY-378: Update devforgeai-qa Skill for Treelint
#
# Validates:
# - coverage-analyzer-integration-guide.md has Treelint context note
# - Note mentions "Treelint-enabled" and "AST-aware test-to-source mapping"
# - Uses **Treelint Integration:** delimiter (BR-003)
# - Note under 800 characters (NFR-001)
# - subagent-prompt-templates.md has Treelint context for coverage-analyzer template
# - subagent-prompt-templates.md has Treelint context for anti-pattern-scanner template
# - subagent-prompt-templates.md does NOT have Treelint for code-quality-auditor (BR-002)
#
# Expected: FAIL initially (TDD Red phase - no Treelint context in files)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
COVERAGE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-qa/references/coverage-analyzer-integration-guide.md"
TEMPLATES_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-qa/references/subagent-prompt-templates.md"

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() { TESTS_PASSED=$((TESTS_PASSED + 1)); echo "[PASS] $1"; }
fail_test() { TESTS_FAILED=$((TESTS_FAILED + 1)); echo "[FAIL] $1: $2"; }
run_test() { TESTS_RUN=$((TESTS_RUN + 1)); shift; "$@"; }

# Test 1: coverage-analyzer-integration-guide.md exists
test_coverage_file_exists() {
    if [ -f "$COVERAGE_FILE" ]; then pass_test "coverage-analyzer-integration-guide.md exists"
    else fail_test "coverage-analyzer-integration-guide.md exists" "File not found"; fi
}

# Test 2: Contains Treelint-enabled keyword
test_treelint_enabled() {
    if grep -q "Treelint-enabled" "$COVERAGE_FILE"; then
        pass_test "coverage-analyzer-integration-guide.md contains 'Treelint-enabled'"
    else
        fail_test "coverage-analyzer-integration-guide.md contains 'Treelint-enabled'" "Not found"
    fi
}

# Test 3: References AST-aware test-to-source mapping
test_ast_aware_mapping() {
    if grep -qi "AST-aware.*test-to-source\|test-to-source.*mapping" "$COVERAGE_FILE"; then
        pass_test "References AST-aware test-to-source mapping"
    else
        fail_test "References AST-aware test-to-source mapping" "No AST-aware test-to-source mapping reference found"
    fi
}

# Test 4: Uses **Treelint Integration:** delimiter in coverage file (BR-003)
test_coverage_delimiter() {
    if grep -q '\*\*Treelint Integration:\*\*' "$COVERAGE_FILE"; then
        pass_test "coverage-analyzer-integration-guide uses **Treelint Integration:** delimiter"
    else
        fail_test "coverage-analyzer-integration-guide uses **Treelint Integration:** delimiter" "Delimiter not found"
    fi
}

# Test 5: Treelint note under 800 characters (NFR-001)
test_note_size() {
    local note_content
    note_content=$(sed -n '/\*\*Treelint Integration:\*\*/,/^$/p' "$COVERAGE_FILE" | head -20)
    if [ -z "$note_content" ]; then
        fail_test "Treelint note under 800 chars" "No Treelint note found"
        return
    fi
    local chars; chars=$(echo "$note_content" | wc -c)
    if [ "$chars" -le 800 ]; then
        pass_test "Treelint note under 800 chars (actual: $chars)"
    else
        fail_test "Treelint note under 800 chars" "Note has $chars chars (max: 800)"
    fi
}

# Test 6: subagent-prompt-templates.md exists
test_templates_file_exists() {
    if [ -f "$TEMPLATES_FILE" ]; then pass_test "subagent-prompt-templates.md exists"
    else fail_test "subagent-prompt-templates.md exists" "File not found"; fi
}

# Test 7: subagent-prompt-templates.md has Treelint for coverage-analyzer
test_templates_coverage_analyzer() {
    # Check that coverage-analyzer template section has Treelint reference
    local section
    section=$(sed -n '/## Template.*coverage-analyzer/,/## Template/p' "$TEMPLATES_FILE" | head -n -1)
    if echo "$section" | grep -q "Treelint"; then
        pass_test "subagent-prompt-templates: coverage-analyzer has Treelint context"
    else
        fail_test "subagent-prompt-templates: coverage-analyzer has Treelint context" "No Treelint in coverage-analyzer template section"
    fi
}

# Test 8: subagent-prompt-templates.md has Treelint for anti-pattern-scanner
test_templates_anti_pattern() {
    local section
    section=$(sed -n '/## Template.*anti-pattern-scanner/,/## Template/p' "$TEMPLATES_FILE" | head -n -1)
    if echo "$section" | grep -q "Treelint"; then
        pass_test "subagent-prompt-templates: anti-pattern-scanner has Treelint context"
    else
        fail_test "subagent-prompt-templates: anti-pattern-scanner has Treelint context" "No Treelint in anti-pattern-scanner template section"
    fi
}

# Test 9: subagent-prompt-templates.md does NOT have Treelint for code-quality-auditor (BR-002)
test_templates_no_code_quality_auditor() {
    local section
    section=$(sed -n '/## Template.*code-quality-auditor/,/## Template/p' "$TEMPLATES_FILE" | head -n -1)
    if [ -z "$section" ]; then
        # Try alternate heading pattern
        section=$(sed -n '/code-quality-auditor/,/## /p' "$TEMPLATES_FILE" | head -30)
    fi
    local treelint_count
    treelint_count=$(echo "$section" | grep -ci "treelint")
    if [ "$treelint_count" -eq 0 ]; then
        pass_test "code-quality-auditor template has NO Treelint context (BR-002)"
    else
        fail_test "code-quality-auditor template has NO Treelint context (BR-002)" "Found $treelint_count Treelint references in code-quality-auditor section"
    fi
}

# Main execution
echo "======================================================="
echo "STORY-378 AC#4: Coverage Analysis Treelint Context"
echo "======================================================="
echo "Targets: $COVERAGE_FILE"
echo "         $TEMPLATES_FILE"
echo "-------------------------------------------------------"
echo ""

run_test "1" test_coverage_file_exists
run_test "2" test_treelint_enabled
run_test "3" test_ast_aware_mapping
run_test "4" test_coverage_delimiter
run_test "5" test_note_size
run_test "6" test_templates_file_exists
run_test "7" test_templates_coverage_analyzer
run_test "8" test_templates_anti_pattern
run_test "9" test_templates_no_code_quality_auditor

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
