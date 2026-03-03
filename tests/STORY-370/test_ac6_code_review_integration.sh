#!/bin/bash
##############################################################################
# Test Suite: STORY-370 AC#6 - Integration with code-reviewer
# Purpose: Verify code-reviewer queries deps for modified functions and
#          includes Dependency Impact section in review reports
# Phase: TDD Red - All tests expected to FAIL before implementation
##############################################################################

set -o pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENT_FILE="${PROJECT_ROOT}/src/claude/agents/code-reviewer.md"
REF_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-development/references/treelint-dependency-query.md"

run_test() {
    local test_name=$1
    local test_func=$2
    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n[Test $TESTS_RUN] $test_name"
    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}PASSED${NC}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAILED${NC}"
    fi
}

# AC#6 Test 1: code-reviewer.md references treelint deps command
test_code_reviewer_references_deps() {
    grep -q 'treelint deps' "$AGENT_FILE"
}

# AC#6 Test 2: code-reviewer queries deps for modified functions
test_query_modified_functions() {
    grep -q 'modified.*function\|changed.*function\|function.*modif' "$AGENT_FILE"
}

# AC#6 Test 3: Callers validated for compatibility with changes
test_callers_validated_compatibility() {
    grep -q 'callers.*compat\|upstream.*callers\|broken.*call' "$AGENT_FILE"
}

# AC#6 Test 4: Broken call sites flagged in review report
test_broken_call_sites_flagged() {
    grep -q 'broken.*call\|flag.*call.*site\|incompatible.*caller' "$AGENT_FILE"
}

# AC#6 Test 5: Dependency Impact section in review report
test_dependency_impact_section() {
    grep -q 'Dependency Impact\|dependency.*impact\|Impact.*Analysis' "$AGENT_FILE"
}

# AC#6 Test 6: Review report lists callers for modified functions
test_review_lists_callers() {
    grep -q 'callers.*list\|list.*callers\|callers.*report' "$AGENT_FILE"
}

# AC#6 Test 7: Review report lists callees for modified functions
test_review_lists_callees() {
    grep -q 'callees.*list\|list.*callees\|callees.*report' "$AGENT_FILE"
}

# AC#6 Test 8: Reference to dependency query service in code-reviewer
test_dependency_query_ref_in_reviewer() {
    grep -q 'treelint-dependency-query\|dependency.*query\|deps.*calls' "$AGENT_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-370 AC#6: Code-reviewer integration"
echo "============================================================"

run_test "code-reviewer references treelint deps" test_code_reviewer_references_deps
run_test "Queries deps for modified functions" test_query_modified_functions
run_test "Callers validated for compatibility" test_callers_validated_compatibility
run_test "Broken call sites flagged" test_broken_call_sites_flagged
run_test "Dependency Impact section in report" test_dependency_impact_section
run_test "Review report lists callers" test_review_lists_callers
run_test "Review report lists callees" test_review_lists_callees
run_test "Dependency query referenced in reviewer" test_dependency_query_ref_in_reviewer

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
