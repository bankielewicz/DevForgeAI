#!/bin/bash
##############################################################################
# Test Suite: STORY-370 AC#4 - Integration with refactoring-specialist
# Purpose: Verify refactoring-specialist queries deps before refactoring
#          and logs impact scope (callers/callees count)
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
AGENT_FILE="${PROJECT_ROOT}/src/claude/agents/refactoring-specialist.md"
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

# AC#4 Test 1: refactoring-specialist.md references treelint deps command
test_agent_references_deps_command() {
    grep -q 'treelint deps' "$AGENT_FILE"
}

# AC#4 Test 2: refactoring-specialist queries deps BEFORE refactoring
test_query_before_refactoring() {
    grep -q 'before.*refactor\|impact.*analysis\|pre-refactor' "$AGENT_FILE"
}

# AC#4 Test 3: Callers list used to identify affected call sites
test_callers_identify_impact() {
    grep -q 'callers\|call sites\|affected.*functions' "$AGENT_FILE"
}

# AC#4 Test 4: Impact scope logged with caller count
test_impact_caller_count_logged() {
    grep -q 'caller.*count\|number.*callers\|caller_count' "$AGENT_FILE"
}

# AC#4 Test 5: Impact scope logged with callee count
test_impact_callee_count_logged() {
    grep -q 'callee.*count\|number.*callees\|callee_count' "$AGENT_FILE"
}

# AC#4 Test 6: Affected files listed in impact analysis
test_affected_files_listed() {
    grep -q 'affected.*files\|impacted.*files\|file.*paths' "$AGENT_FILE"
}

# AC#4 Test 7: Reference to dependency query service in refactoring workflow
test_dependency_query_ref_in_agent() {
    grep -q 'treelint-dependency-query\|dependency.*query\|deps.*calls' "$AGENT_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-370 AC#4: Refactoring-specialist integration"
echo "============================================================"

run_test "refactoring-specialist references treelint deps" test_agent_references_deps_command
run_test "Queries deps BEFORE refactoring" test_query_before_refactoring
run_test "Callers used to identify impact" test_callers_identify_impact
run_test "Impact scope logs caller count" test_impact_caller_count_logged
run_test "Impact scope logs callee count" test_impact_callee_count_logged
run_test "Affected files listed in impact" test_affected_files_listed
run_test "Dependency query referenced in agent" test_dependency_query_ref_in_agent

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
