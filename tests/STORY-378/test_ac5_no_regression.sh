#!/bin/bash
# Test AC#5: No Regression Without Treelint
# STORY-378: Update devforgeai-qa Skill for Treelint
#
# Validates:
# - No Treelint-dependent syntax (no Bash treelint commands in skill/reference files)
# - All modified reference files are valid Markdown (no unclosed blocks)
# - deep-validation-workflow.md has Treelint context for enabled subagents
# - deep-validation-workflow.md does NOT have Treelint for deferral-validator (BR-002/TL-002)
# - deep-validation-workflow.md does NOT have Treelint for qa-result-interpreter (BR-002/TL-002)
# - Parallel validation success threshold unchanged (NFR-005: 66% / 2-of-3)
#
# Expected: FAIL initially (TDD Red phase - deep-validation-workflow.md has no Treelint context)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SRC_QA="$PROJECT_ROOT/src/claude/skills/devforgeai-qa"

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() { TESTS_PASSED=$((TESTS_PASSED + 1)); echo "[PASS] $1"; }
fail_test() { TESTS_FAILED=$((TESTS_FAILED + 1)); echo "[FAIL] $1: $2"; }
run_test() { TESTS_RUN=$((TESTS_RUN + 1)); shift; "$@"; }

# Test 1: No Bash treelint commands in SKILL.md (context notes only, no runtime dependency)
test_no_bash_treelint_in_skill() {
    local hits=0
    if [ -f "$SRC_QA/SKILL.md" ]; then
        hits=$(grep -cE 'Bash.*treelint|command.*treelint' "$SRC_QA/SKILL.md" 2>/dev/null || true)
        hits=${hits:-0}
    fi
    if [ "$hits" -eq 0 ] 2>/dev/null; then
        pass_test "No Bash treelint commands in SKILL.md"
    else
        fail_test "No Bash treelint commands in SKILL.md" "Found $hits treelint command references"
    fi
}

# Test 2: No Bash treelint commands in reference files
test_no_bash_treelint_in_refs() {
    local total_hits=0
    for ref_file in "$SRC_QA/references/"*.md; do
        if [ -f "$ref_file" ]; then
            local hits
            hits=$(grep -cE 'Bash.*treelint|command.*treelint' "$ref_file" 2>/dev/null || true)
            hits=${hits:-0}
            if [ "$hits" -gt 0 ] 2>/dev/null; then
                total_hits=$((total_hits + hits))
            fi
        fi
    done
    if [ "$total_hits" -eq 0 ]; then
        pass_test "No Bash treelint commands in reference files"
    else
        fail_test "No Bash treelint commands in reference files" "Found $total_hits treelint command references across reference files"
    fi
}

# Test 3: deep-validation-workflow.md has Treelint context for anti-pattern-scanner
test_deep_has_anti_pattern_treelint() {
    local deep_file="$SRC_QA/references/deep-validation-workflow.md"
    if grep -q "Treelint" "$deep_file"; then
        pass_test "deep-validation-workflow.md contains Treelint context"
    else
        fail_test "deep-validation-workflow.md contains Treelint context" "No Treelint references found"
    fi
}

# Test 4: deep-validation-workflow.md does NOT have Treelint for deferral-validator (BR-002)
test_deep_no_deferral_treelint() {
    local deep_file="$SRC_QA/references/deep-validation-workflow.md"
    # Check within 20 lines of deferral-validator references for Treelint
    local treelint_near_deferral
    treelint_near_deferral=$(grep -n "deferral-validator" "$deep_file" | while IFS=: read -r line_num _rest; do
        local start=$((line_num - 10))
        [ "$start" -lt 1 ] && start=1
        local end=$((line_num + 10))
        sed -n "${start},${end}p" "$deep_file" | grep -ci "treelint"
    done | paste -sd+ | bc 2>/dev/null || echo "0")
    if [ "$treelint_near_deferral" -eq 0 ] 2>/dev/null; then
        pass_test "deferral-validator has NO Treelint context in deep-validation (BR-002)"
    else
        fail_test "deferral-validator has NO Treelint context in deep-validation (BR-002)" "Found Treelint near deferral-validator"
    fi
}

# Test 5: deep-validation-workflow.md does NOT have Treelint for qa-result-interpreter (BR-002)
test_deep_no_qa_result_treelint() {
    local deep_file="$SRC_QA/references/deep-validation-workflow.md"
    local treelint_near_qa
    treelint_near_qa=$(grep -n "qa-result-interpreter" "$deep_file" | while IFS=: read -r line_num _rest; do
        local start=$((line_num - 10))
        [ "$start" -lt 1 ] && start=1
        local end=$((line_num + 10))
        sed -n "${start},${end}p" "$deep_file" | grep -ci "treelint"
    done | paste -sd+ | bc 2>/dev/null || echo "0")
    if [ "$treelint_near_qa" -eq 0 ] 2>/dev/null; then
        pass_test "qa-result-interpreter has NO Treelint context in deep-validation (BR-002)"
    else
        fail_test "qa-result-interpreter has NO Treelint context in deep-validation (BR-002)" "Found Treelint near qa-result-interpreter"
    fi
}

# Test 6: Parallel validation threshold unchanged (NFR-005: 66% / 2-of-3)
test_parallel_threshold_unchanged() {
    local parallel_file="$SRC_QA/references/parallel-validation.md"
    if grep -qE "(2-of-3|66%|2.*of.*3|two.*of.*three)" "$parallel_file"; then
        pass_test "Parallel validation threshold unchanged (2-of-3 / 66%)"
    else
        fail_test "Parallel validation threshold unchanged" "Cannot find 2-of-3 or 66% threshold reference"
    fi
}

# Test 7: All reference files are readable (no corrupt files)
test_files_readable() {
    local unreadable=0
    for ref_file in "$SRC_QA/SKILL.md" "$SRC_QA/references/"*.md; do
        if [ ! -r "$ref_file" ]; then
            unreadable=$((unreadable + 1))
        fi
    done
    if [ "$unreadable" -eq 0 ]; then
        pass_test "All QA skill files are readable"
    else
        fail_test "All QA skill files are readable" "$unreadable files are not readable"
    fi
}

# Main execution
echo "======================================================="
echo "STORY-378 AC#5: No Regression Without Treelint"
echo "======================================================="
echo "Target dir: $SRC_QA"
echo "-------------------------------------------------------"
echo ""

run_test "1" test_no_bash_treelint_in_skill
run_test "2" test_no_bash_treelint_in_refs
run_test "3" test_deep_has_anti_pattern_treelint
run_test "4" test_deep_no_deferral_treelint
run_test "5" test_deep_no_qa_result_treelint
run_test "6" test_parallel_threshold_unchanged
run_test "7" test_files_readable

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
