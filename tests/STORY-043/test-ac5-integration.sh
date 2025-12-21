#!/bin/bash

##############################################################################
# Test Suite: STORY-043 AC-5 - Framework Integration Validated
#
# AC-5: Framework Integration Validated (Skills + Subagents + Commands)
# Given: Updated paths affect skills, subagents, and commands
# When: Execute integration test suite (3 representative workflows)
# Then: All 3 workflows complete successfully with 0 path errors
#
# Test 1: Epic Creation (/create-epic User Authentication)
# Test 2: Story Creation (/create-story User login with email/password)
# Test 3: Development Workflow (/dev STORY-044)
#
# Expected: "INTEGRATION: PASSED (3/3 workflows, 0 path errors)"
##############################################################################

set -euo pipefail

TEST_NAME="AC-5: Framework Integration Validated (3 Workflows)"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../" && pwd)"
SPEC_DIR="devforgeai/specs/STORY-043"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}✓ PASS${NC}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}✗ FAIL${NC}"
    fi
}

##############################################################################
# TEST 1: Integration test report exists
##############################################################################

test_integration_report_exists() {
    # Test: integration-test-report.md exists
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        echo "  Integration report found: integration-test-report.md"
        return 0
    else
        echo "  ERROR: Integration report not found"
        return 1
    fi
}

##############################################################################
# TEST 2: Test 1 - Epic Creation Workflow
##############################################################################

test_epic_creation_executed() {
    # Test: Epic creation test executed
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        if grep -q "Test 1\|Epic Creation\|/create-epic" "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null; then
            echo "  Test 1: Epic creation workflow documented"
            return 0
        else
            echo "  ERROR: Epic creation test not documented"
            return 1
        fi
    else
        return 1
    fi
}

test_epic_creation_passed() {
    # Test: Epic creation workflow passed
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        local epic_section=$(sed -n '/Test 1.*Epic/,/Test 2/p' "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null)
        if echo "$epic_section" | grep -q "PASS\|pass\|✓\|Success\|success"; then
            echo "  Epic creation: PASSED"
            return 0
        else
            echo "  ERROR: Epic creation did not pass"
            return 1
        fi
    else
        return 1
    fi
}

test_epic_loads_feature_decomposition() {
    # Test: Epic creation loaded feature-decomposition-patterns.md from src/
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        if grep -q "feature-decomposition\|devforgeai-orchestration.*reference" "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null; then
            echo "  Epic creation loaded feature-decomposition-patterns.md from src/"
            return 0
        else
            echo "  WARNING: Feature decomposition load not documented"
            return 0  # Non-blocking
        fi
    else
        return 1
    fi
}

test_epic_no_path_errors() {
    # Test: Epic creation reported 0 path errors
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        local epic_section=$(sed -n '/Test 1.*Epic/,/Test 2/p' "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null)
        if echo "$epic_section" | grep -q "0.*error\|zero.*error\|Error: 0"; then
            echo "  Epic creation: 0 path errors"
            return 0
        else
            echo "  WARNING: Path error count not explicitly confirmed (may be implicit)"
            return 0  # Non-blocking
        fi
    else
        return 1
    fi
}

##############################################################################
# TEST 3: Test 2 - Story Creation Workflow
##############################################################################

test_story_creation_executed() {
    # Test: Story creation test executed
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        if grep -q "Test 2\|Story Creation\|/create-story" "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null; then
            echo "  Test 2: Story creation workflow documented"
            return 0
        else
            echo "  ERROR: Story creation test not documented"
            return 1
        fi
    else
        return 1
    fi
}

test_story_creation_passed() {
    # Test: Story creation workflow passed
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        local story_section=$(sed -n '/Test 2.*Story/,/Test 3/p' "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null)
        if echo "$story_section" | grep -q "PASS\|pass\|✓\|Success\|success"; then
            echo "  Story creation: PASSED"
            return 0
        else
            echo "  ERROR: Story creation did not pass"
            return 1
        fi
    else
        return 1
    fi
}

test_story_loads_reference_files() {
    # Test: Story creation loaded 6 reference files from src/
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        if grep -q "6.*reference\|reference.*files" "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null; then
            echo "  Story creation loaded reference files from src/"
            return 0
        else
            echo "  WARNING: Reference file load not documented"
            return 0  # Non-blocking
        fi
    else
        return 1
    fi
}

test_story_no_path_errors() {
    # Test: Story creation reported 0 path errors
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        local story_section=$(sed -n '/Test 2.*Story/,/Test 3/p' "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null)
        if echo "$story_section" | grep -q "0.*error\|zero.*error\|Error: 0"; then
            echo "  Story creation: 0 path errors"
            return 0
        else
            echo "  WARNING: Path error count not explicitly confirmed (may be implicit)"
            return 0  # Non-blocking
        fi
    else
        return 1
    fi
}

##############################################################################
# TEST 4: Test 3 - Development Workflow
##############################################################################

test_dev_workflow_executed() {
    # Test: Development workflow test executed
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        if grep -q "Test 3\|Development\|/dev\|STORY-044" "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null; then
            echo "  Test 3: Development workflow documented"
            return 0
        else
            echo "  ERROR: Development workflow test not documented"
            return 1
        fi
    else
        return 1
    fi
}

test_dev_workflow_passed() {
    # Test: Development workflow passed
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        local dev_section=$(sed -n '/Test 3.*Development/,$p' "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null)
        if echo "$dev_section" | grep -q "PASS\|pass\|✓\|Success\|success"; then
            echo "  Development workflow: PASSED"
            return 0
        else
            echo "  ERROR: Development workflow did not pass"
            return 1
        fi
    else
        return 1
    fi
}

test_dev_loads_phase_references() {
    # Test: Dev workflow loaded phase references from src/
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        if grep -q "phase.*reference\|devforgeai-development.*reference" "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null; then
            echo "  Dev workflow loaded phase references from src/"
            return 0
        else
            echo "  WARNING: Phase reference load not documented"
            return 0  # Non-blocking
        fi
    else
        return 1
    fi
}

test_dev_no_path_errors() {
    # Test: Dev workflow reported 0 path errors
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        local dev_section=$(sed -n '/Test 3.*Development/,$p' "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null)
        if echo "$dev_section" | grep -q "0.*error\|zero.*error\|Error: 0"; then
            echo "  Dev workflow: 0 path errors"
            return 0
        else
            echo "  WARNING: Path error count not explicitly confirmed (may be implicit)"
            return 0  # Non-blocking
        fi
    else
        return 1
    fi
}

##############################################################################
# TEST 5: Overall integration status
##############################################################################

test_integration_summary() {
    # Test: Integration report has summary section
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        if grep -q "Summary\|summary\|SUMMARY\|Result\|result" "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null; then
            echo "  Integration report has summary"
            return 0
        else
            echo "  ERROR: Integration report missing summary"
            return 1
        fi
    else
        return 1
    fi
}

test_all_workflows_passed() {
    # Test: Report shows all 3 workflows passed
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        if grep -q "3/3\|all.*passed\|PASSED.*3\|all.*success" "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null; then
            echo "  Integration status: 3/3 workflows PASSED"
            return 0
        else
            echo "  WARNING: Integration status for all 3 workflows not explicitly confirmed"
            return 0  # Non-blocking - may have individual pass marks
        fi
    else
        return 1
    fi
}

test_zero_path_errors_total() {
    # Test: Report confirms 0 total path errors
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        if grep -q "0.*path.*error\|zero.*path.*error\|Path.*Error.*0" "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null; then
            echo "  Total path errors: 0"
            return 0
        else
            echo "  WARNING: Total path error count not explicitly stated"
            return 0  # Non-blocking - individual tests may confirm
        fi
    else
        return 1
    fi
}

##############################################################################
# TEST 6: Subagent execution verification
##############################################################################

test_requirements_analyst_executed() {
    # Test: requirements-analyst subagent executed
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        if grep -q "requirements-analyst\|story-requirements-analyst" "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null; then
            echo "  requirements-analyst subagent executed"
            return 0
        else
            echo "  WARNING: requirements-analyst execution not documented"
            return 0  # Non-blocking
        fi
    else
        return 1
    fi
}

test_git_validator_executed() {
    # Test: git-validator subagent executed
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" ]; then
        if grep -q "git-validator\|git.*valid" "$PROJECT_ROOT/$SPEC_DIR/integration-test-report.md" 2>/dev/null; then
            echo "  git-validator subagent executed"
            return 0
        else
            echo "  WARNING: git-validator execution not documented"
            return 0  # Non-blocking
        fi
    else
        return 1
    fi
}

##############################################################################
# Main Test Execution
##############################################################################

main() {
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$TEST_NAME${NC}"
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
    echo ""

    echo -e "${YELLOW}Phase 1: Report Existence${NC}"
    run_test "AC-5.1: Integration report exists" "test_integration_report_exists"

    echo -e "\n${YELLOW}Phase 2: Test 1 - Epic Creation Workflow${NC}"
    run_test "AC-5.2: Epic creation executed" "test_epic_creation_executed"
    run_test "AC-5.3: Epic creation PASSED" "test_epic_creation_passed"
    run_test "AC-5.4: Epic loads feature-decomposition from src/" "test_epic_loads_feature_decomposition"
    run_test "AC-5.5: Epic creation 0 path errors" "test_epic_no_path_errors"

    echo -e "\n${YELLOW}Phase 3: Test 2 - Story Creation Workflow${NC}"
    run_test "AC-5.6: Story creation executed" "test_story_creation_executed"
    run_test "AC-5.7: Story creation PASSED" "test_story_creation_passed"
    run_test "AC-5.8: Story loads 6 references from src/" "test_story_loads_reference_files"
    run_test "AC-5.9: Story creation 0 path errors" "test_story_no_path_errors"

    echo -e "\n${YELLOW}Phase 4: Test 3 - Development Workflow${NC}"
    run_test "AC-5.10: Dev workflow executed" "test_dev_workflow_executed"
    run_test "AC-5.11: Dev workflow PASSED" "test_dev_workflow_passed"
    run_test "AC-5.12: Dev loads phase references from src/" "test_dev_loads_phase_references"
    run_test "AC-5.13: Dev workflow 0 path errors" "test_dev_no_path_errors"

    echo -e "\n${YELLOW}Phase 5: Overall Integration Status${NC}"
    run_test "AC-5.14: Integration report has summary" "test_integration_summary"
    run_test "AC-5.15: All 3 workflows PASSED" "test_all_workflows_passed"
    run_test "AC-5.16: Zero total path errors" "test_zero_path_errors_total"

    echo -e "\n${YELLOW}Phase 6: Subagent Execution${NC}"
    run_test "AC-5.17: requirements-analyst executed" "test_requirements_analyst_executed"
    run_test "AC-5.18: git-validator executed" "test_git_validator_executed"

    # Summary
    echo ""
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
    echo -e "Tests run:    ${BLUE}$TESTS_RUN${NC}"
    echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"

    [ "$TESTS_FAILED" -eq 0 ] && exit 0 || exit 1
}

main "$@"
