#!/bin/bash
# Test AC#3: Parallel Validators Have Treelint Context
# STORY-378: Update devforgeai-qa Skill for Treelint
#
# Validates:
# - parallel-validation.md has Treelint context for test-automator
# - parallel-validation.md has Treelint context for code-reviewer
# - parallel-validation.md has Treelint context for security-auditor
# - Each uses **Treelint Integration:** delimiter (BR-003)
# - Notes are outside context_summary blocks (BR-004)
# - Existing parallel execution pattern preserved (BR-001)
#
# Expected: FAIL initially (TDD Red phase - no Treelint context in file)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
PARALLEL_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-qa/references/parallel-validation.md"

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() { TESTS_PASSED=$((TESTS_PASSED + 1)); echo "[PASS] $1"; }
fail_test() { TESTS_FAILED=$((TESTS_FAILED + 1)); echo "[FAIL] $1: $2"; }
run_test() { TESTS_RUN=$((TESTS_RUN + 1)); shift; "$@"; }

# Test 1: File exists
test_file_exists() {
    if [ -f "$PARALLEL_FILE" ]; then pass_test "parallel-validation.md exists"
    else fail_test "parallel-validation.md exists" "File not found"; fi
}

# Test 2: Contains Treelint context for test-automator
test_test_automator_treelint() {
    if grep -q "Treelint" "$PARALLEL_FILE" && grep -q "test-automator" "$PARALLEL_FILE"; then
        # Verify Treelint appears in proximity to test-automator Task() invocation
        local count
        count=$(grep -c "Treelint" "$PARALLEL_FILE")
        if [ "$count" -ge 1 ]; then
            pass_test "test-automator has Treelint context"
        else
            fail_test "test-automator has Treelint context" "No Treelint reference found"
        fi
    else
        fail_test "test-automator has Treelint context" "Missing Treelint or test-automator reference"
    fi
}

# Test 3: Contains Treelint context for code-reviewer
test_code_reviewer_treelint() {
    # Check that Treelint appears at least 2 times (for multiple subagents)
    local treelint_count
    treelint_count=$(grep -c "Treelint" "$PARALLEL_FILE")
    if [ "$treelint_count" -ge 2 ]; then
        pass_test "code-reviewer has Treelint context (count: $treelint_count)"
    else
        fail_test "code-reviewer has Treelint context" "Only $treelint_count Treelint references (need >= 2 for multiple subagents)"
    fi
}

# Test 4: Contains Treelint context for security-auditor
test_security_auditor_treelint() {
    # Need at least 3 Treelint references for all 3 parallel validators
    local treelint_count
    treelint_count=$(grep -c "Treelint" "$PARALLEL_FILE")
    if [ "$treelint_count" -ge 3 ]; then
        pass_test "security-auditor has Treelint context (count: $treelint_count)"
    else
        fail_test "security-auditor has Treelint context" "Only $treelint_count Treelint references (need >= 3 for all 3 validators)"
    fi
}

# Test 5: Uses **Treelint Integration:** delimiter (BR-003)
test_delimiter() {
    local delimiter_count
    delimiter_count=$(grep -c '\*\*Treelint Integration:\*\*' "$PARALLEL_FILE")
    if [ "$delimiter_count" -ge 3 ]; then
        pass_test "Uses **Treelint Integration:** delimiter ($delimiter_count instances for 3 validators)"
    else
        fail_test "Uses **Treelint Integration:** delimiter" "Found $delimiter_count instances (need >= 3 for 3 validators)"
    fi
}

# Test 6: Treelint notes are NOT inside context_summary string literals (BR-004)
test_outside_context_summary() {
    # Extract content between context_summary quotes and check for Treelint
    local inside_summary
    inside_summary=$(sed -n '/context_summary.*=.*"""/,/"""/p' "$PARALLEL_FILE" | grep -c "Treelint")
    if [ "$inside_summary" -eq 0 ]; then
        pass_test "Treelint notes outside context_summary blocks (BR-004)"
    else
        fail_test "Treelint notes outside context_summary blocks (BR-004)" "Found $inside_summary Treelint references inside context_summary"
    fi
}

# Test 7: Existing parallel pattern preserved (BR-001)
test_parallel_pattern_preserved() {
    if grep -q "test-automator" "$PARALLEL_FILE" && grep -q "code-reviewer" "$PARALLEL_FILE" && grep -q "security-auditor" "$PARALLEL_FILE"; then
        pass_test "Existing parallel validation pattern preserved"
    else
        fail_test "Existing parallel validation pattern preserved" "Missing one or more original subagent references"
    fi
}

# Test 8: Each Treelint note under 800 characters (NFR-001)
test_note_sizes() {
    local oversize=0
    while IFS= read -r line_num; do
        local note
        note=$(sed -n "${line_num},/^$/p" "$PARALLEL_FILE" | head -20)
        local chars; chars=$(echo "$note" | wc -c)
        if [ "$chars" -gt 800 ]; then
            oversize=$((oversize + 1))
        fi
    done < <(grep -n '\*\*Treelint Integration:\*\*' "$PARALLEL_FILE" | cut -d: -f1)
    if [ "$oversize" -eq 0 ]; then
        pass_test "All Treelint notes under 800 chars (NFR-001)"
    else
        fail_test "All Treelint notes under 800 chars" "$oversize notes exceed 800 characters"
    fi
}

# Main execution
echo "======================================================="
echo "STORY-378 AC#3: Parallel Validators Treelint Context"
echo "======================================================="
echo "Target: $PARALLEL_FILE"
echo "-------------------------------------------------------"
echo ""

run_test "1" test_file_exists
run_test "2" test_test_automator_treelint
run_test "3" test_code_reviewer_treelint
run_test "4" test_security_auditor_treelint
run_test "5" test_delimiter
run_test "6" test_outside_context_summary
run_test "7" test_parallel_pattern_preserved
run_test "8" test_note_sizes

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
