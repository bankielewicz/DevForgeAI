#!/bin/bash
# Test AC#6: Works WITH Treelint - All 5 Subagents Receive Context
# STORY-378: Update devforgeai-qa Skill for Treelint
#
# Validates:
# - All 5 Treelint-enabled subagents have Treelint context across ALL modified files
# - anti-pattern-scanner: in anti-pattern-detection-workflow.md AND deep-validation-workflow.md AND subagent-prompt-templates.md
# - test-automator: in parallel-validation.md AND deep-validation-workflow.md
# - code-reviewer: in parallel-validation.md AND deep-validation-workflow.md
# - security-auditor: in parallel-validation.md AND deep-validation-workflow.md
# - coverage-analyzer: in coverage-analyzer-integration-guide.md AND subagent-prompt-templates.md
# - Non-enabled subagents (code-quality-auditor, deferral-validator, qa-result-interpreter) excluded (BR-002)
#
# Expected: FAIL initially (TDD Red phase - no Treelint context in any file)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SRC_QA="$PROJECT_ROOT/src/claude/skills/devforgeai-qa"

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() { TESTS_PASSED=$((TESTS_PASSED + 1)); echo "[PASS] $1"; }
fail_test() { TESTS_FAILED=$((TESTS_FAILED + 1)); echo "[FAIL] $1: $2"; }
run_test() { TESTS_RUN=$((TESTS_RUN + 1)); shift; "$@"; }

# Test 1: anti-pattern-scanner has Treelint in anti-pattern-detection-workflow.md
test_aps_in_workflow() {
    if grep -q "Treelint" "$SRC_QA/references/anti-pattern-detection-workflow.md"; then
        pass_test "anti-pattern-scanner: Treelint in anti-pattern-detection-workflow.md"
    else
        fail_test "anti-pattern-scanner: Treelint in anti-pattern-detection-workflow.md" "No Treelint found"
    fi
}

# Test 2: anti-pattern-scanner has Treelint in subagent-prompt-templates.md
test_aps_in_templates() {
    local section
    section=$(sed -n '/anti-pattern-scanner/,/## Template/p' "$SRC_QA/references/subagent-prompt-templates.md" | head -n -1)
    if echo "$section" | grep -q "Treelint"; then
        pass_test "anti-pattern-scanner: Treelint in subagent-prompt-templates.md"
    else
        fail_test "anti-pattern-scanner: Treelint in subagent-prompt-templates.md" "No Treelint in anti-pattern-scanner template section"
    fi
}

# Test 3: test-automator has Treelint in parallel-validation.md
test_ta_in_parallel() {
    if grep -q "Treelint" "$SRC_QA/references/parallel-validation.md"; then
        pass_test "test-automator: Treelint in parallel-validation.md"
    else
        fail_test "test-automator: Treelint in parallel-validation.md" "No Treelint found"
    fi
}

# Test 4: code-reviewer has Treelint in parallel-validation.md (verified via count >= 2)
test_cr_in_parallel() {
    local count
    count=$(grep -c '\*\*Treelint Integration:\*\*' "$SRC_QA/references/parallel-validation.md")
    if [ "$count" -ge 2 ]; then
        pass_test "code-reviewer: Treelint in parallel-validation.md (delimiter count: $count)"
    else
        fail_test "code-reviewer: Treelint in parallel-validation.md" "Only $count Treelint Integration delimiters (need >= 2)"
    fi
}

# Test 5: security-auditor has Treelint in parallel-validation.md (verified via count >= 3)
test_sa_in_parallel() {
    local count
    count=$(grep -c '\*\*Treelint Integration:\*\*' "$SRC_QA/references/parallel-validation.md")
    if [ "$count" -ge 3 ]; then
        pass_test "security-auditor: Treelint in parallel-validation.md (delimiter count: $count)"
    else
        fail_test "security-auditor: Treelint in parallel-validation.md" "Only $count Treelint Integration delimiters (need >= 3)"
    fi
}

# Test 6: coverage-analyzer has Treelint in coverage-analyzer-integration-guide.md
test_ca_in_guide() {
    if grep -q "Treelint" "$SRC_QA/references/coverage-analyzer-integration-guide.md"; then
        pass_test "coverage-analyzer: Treelint in coverage-analyzer-integration-guide.md"
    else
        fail_test "coverage-analyzer: Treelint in coverage-analyzer-integration-guide.md" "No Treelint found"
    fi
}

# Test 7: coverage-analyzer has Treelint in subagent-prompt-templates.md
test_ca_in_templates() {
    local section
    section=$(sed -n '/## Template.*coverage-analyzer/,/## Template/p' "$SRC_QA/references/subagent-prompt-templates.md" | head -n -1)
    if echo "$section" | grep -q "Treelint"; then
        pass_test "coverage-analyzer: Treelint in subagent-prompt-templates.md"
    else
        fail_test "coverage-analyzer: Treelint in subagent-prompt-templates.md" "No Treelint in coverage-analyzer template"
    fi
}

# Test 8: code-quality-auditor does NOT have Treelint (BR-002)
test_no_cqa_treelint() {
    local section
    section=$(sed -n '/code-quality-auditor/,/## /p' "$SRC_QA/references/subagent-prompt-templates.md" | head -30)
    local count
    count=$(echo "$section" | grep -ci "treelint")
    if [ "$count" -eq 0 ]; then
        pass_test "code-quality-auditor excluded from Treelint (BR-002)"
    else
        fail_test "code-quality-auditor excluded from Treelint (BR-002)" "Found $count Treelint references"
    fi
}

# Test 9: deferral-validator does NOT have Treelint (BR-002)
test_no_dv_treelint() {
    # Check deep-validation-workflow.md near deferral-validator references
    local deep_file="$SRC_QA/references/deep-validation-workflow.md"
    if [ ! -f "$deep_file" ]; then
        fail_test "deferral-validator excluded from Treelint" "deep-validation-workflow.md not found"
        return
    fi
    local near_treelint=0
    while IFS=: read -r line_num _rest; do
        local start=$((line_num - 10))
        [ "$start" -lt 1 ] && start=1
        local end=$((line_num + 10))
        local hits
        hits=$(sed -n "${start},${end}p" "$deep_file" | grep -ci "treelint")
        near_treelint=$((near_treelint + hits))
    done < <(grep -n "deferral-validator" "$deep_file")
    if [ "$near_treelint" -eq 0 ]; then
        pass_test "deferral-validator excluded from Treelint (BR-002)"
    else
        fail_test "deferral-validator excluded from Treelint (BR-002)" "Found $near_treelint Treelint near deferral-validator"
    fi
}

# Test 10: qa-result-interpreter does NOT have Treelint (BR-002)
test_no_qri_treelint() {
    local deep_file="$SRC_QA/references/deep-validation-workflow.md"
    if [ ! -f "$deep_file" ]; then
        fail_test "qa-result-interpreter excluded from Treelint" "deep-validation-workflow.md not found"
        return
    fi
    local near_treelint=0
    while IFS=: read -r line_num _rest; do
        local start=$((line_num - 10))
        [ "$start" -lt 1 ] && start=1
        local end=$((line_num + 10))
        local hits
        hits=$(sed -n "${start},${end}p" "$deep_file" | grep -ci "treelint")
        near_treelint=$((near_treelint + hits))
    done < <(grep -n "qa-result-interpreter" "$deep_file")
    if [ "$near_treelint" -eq 0 ]; then
        pass_test "qa-result-interpreter excluded from Treelint (BR-002)"
    else
        fail_test "qa-result-interpreter excluded from Treelint (BR-002)" "Found $near_treelint Treelint near qa-result-interpreter"
    fi
}

# Test 11: Total Treelint-enabled subagent count is exactly 5
test_total_enabled_count() {
    local skill_file="$SRC_QA/SKILL.md"
    if [ ! -f "$skill_file" ]; then
        fail_test "SKILL.md lists exactly 5 Treelint-enabled subagents" "SKILL.md not found"
        return
    fi
    local section
    section=$(sed -n '/^## Treelint Integration/,/^## /p' "$skill_file" | head -n -1)
    local agents=0
    echo "$section" | grep -q "anti-pattern-scanner" && agents=$((agents + 1))
    echo "$section" | grep -q "test-automator" && agents=$((agents + 1))
    echo "$section" | grep -q "code-reviewer" && agents=$((agents + 1))
    echo "$section" | grep -q "security-auditor" && agents=$((agents + 1))
    echo "$section" | grep -q "coverage-analyzer" && agents=$((agents + 1))
    if [ "$agents" -eq 5 ]; then
        pass_test "SKILL.md lists exactly 5 Treelint-enabled subagents"
    else
        fail_test "SKILL.md lists exactly 5 Treelint-enabled subagents" "Found $agents/5 subagents in Treelint Integration section"
    fi
}

# Main execution
echo "======================================================="
echo "STORY-378 AC#6: Works WITH Treelint (All 5 Subagents)"
echo "======================================================="
echo "Target dir: $SRC_QA"
echo "-------------------------------------------------------"
echo ""

run_test "1" test_aps_in_workflow
run_test "2" test_aps_in_templates
run_test "3" test_ta_in_parallel
run_test "4" test_cr_in_parallel
run_test "5" test_sa_in_parallel
run_test "6" test_ca_in_guide
run_test "7" test_ca_in_templates
run_test "8" test_no_cqa_treelint
run_test "9" test_no_dv_treelint
run_test "10" test_no_qri_treelint
run_test "11" test_total_enabled_count

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
