#!/bin/bash

################################################################################
# MASTER TEST RUNNER: STORY-152 Comprehensive Test Suite
#
# Runs all STORY-152 acceptance criteria and technical specification tests
# Provides consolidated results and coverage summary
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Results tracking
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0
FAILED_TESTS=()

echo ""
echo "================================================================================"
echo "STORY-152: Unified Story Change Log Tracking with Subagent Attribution"
echo "COMPREHENSIVE TEST SUITE RUNNER"
echo "================================================================================"
echo ""

# Function to run a test file and track results
run_test_file() {
    local test_file="$1"
    local test_name=$(basename "$test_file" .sh)

    echo -e "${BLUE}Running: $test_name${NC}"
    echo "----------"

    if bash "$test_file"; then
        # Extract pass/fail counts from test output
        local pass_count=$(grep "^PASSED:" "$test_file" 2>/dev/null | grep -o "[0-9]*" || echo "0")
        TOTAL_PASSED=$((TOTAL_PASSED + pass_count))
        echo ""
    else
        local fail_count=$(grep "^FAILED:" "$test_file" 2>/dev/null | grep -o "[0-9]*" || echo "1")
        TOTAL_FAILED=$((TOTAL_FAILED + fail_count))
        FAILED_TESTS+=("$test_name")
        echo ""
    fi
}

# Test execution order (by acceptance criteria)
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════${NC}"
echo "ACCEPTANCE CRITERIA TESTS"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""

echo "AC#1: Story Template Updated with Change Log Section"
echo "========================================================"
bash "$SCRIPT_DIR/test-ac1-story-template-changelog-section.sh" || TOTAL_FAILED=$((TOTAL_FAILED + 1))
echo ""

echo "AC#2: Shared Changelog Reference Guide Created"
echo "=============================================="
bash "$SCRIPT_DIR/test-ac2-changelog-reference-guide.sh" || TOTAL_FAILED=$((TOTAL_FAILED + 1))
echo ""

echo "AC#3: devforgeai-development Skill Appends Changelog Entries"
echo "==========================================================="
bash "$SCRIPT_DIR/test-ac3-dev-skill-changelog-integration.sh" || TOTAL_FAILED=$((TOTAL_FAILED + 1))
echo ""

echo "AC#4: devforgeai-qa Skill Appends Changelog Entry"
echo "================================================="
bash "$SCRIPT_DIR/test-ac4-qa-skill-changelog-integration.sh" || TOTAL_FAILED=$((TOTAL_FAILED + 1))
echo ""

echo "AC#5: devforgeai-release Skill Appends Changelog and Archives Story"
echo "=================================================================="
bash "$SCRIPT_DIR/test-ac5-release-skill-changelog-integration.sh" || TOTAL_FAILED=$((TOTAL_FAILED + 1))
echo ""

echo "AC#6: Project CHANGELOG.md Created with Keep a Changelog Format"
echo "=============================================================="
bash "$SCRIPT_DIR/test-ac6-project-changelog-format.sh" || TOTAL_FAILED=$((TOTAL_FAILED + 1))
echo ""

echo "AC#7: Backward Compatible with Existing Stories"
echo "=============================================="
bash "$SCRIPT_DIR/test-ac7-backward-compatibility.sh" || TOTAL_FAILED=$((TOTAL_FAILED + 1))
echo ""

# Technical specification tests
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════${NC}"
echo "TECHNICAL SPECIFICATION VALIDATION TESTS"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""

echo "Data Model: Changelog Entry Format Validation"
echo "============================================="
bash "$SCRIPT_DIR/test-changelog-entry-format-validation.sh" || TOTAL_FAILED=$((TOTAL_FAILED + 1))
echo ""

echo "Service: Story Template Version 2.5"
echo "==================================="
bash "$SCRIPT_DIR/test-story-template-version.sh" || TOTAL_FAILED=$((TOTAL_FAILED + 1))
echo ""

# Summary Report
echo ""
echo "================================================================================"
echo "TEST EXECUTION SUMMARY"
echo "================================================================================"
echo ""

# Count total tests by scanning all test files for TEST count
for test_file in "$SCRIPT_DIR"/test-*.sh; do
    # Count "TEST N:" occurrences in each file
    COUNT=$(grep -c "^TEST [0-9]*:" "$test_file" 2>/dev/null) || COUNT=0
    TOTAL_TESTS=$((TOTAL_TESTS + COUNT))
done

echo "Tests Executed: $TOTAL_TESTS"
echo ""

# Calculate results from actual test executions
RESULTS_PASS=0
RESULTS_FAIL=0

for test_file in "$SCRIPT_DIR"/test-*.sh; do
    if bash "$test_file" > /dev/null 2>&1; then
        RESULTS_PASS=$((RESULTS_PASS + 1))
    else
        RESULTS_FAIL=$((RESULTS_FAIL + 1))
    fi
done

echo -e "Test Groups Passed:  ${GREEN}${RESULTS_PASS}${NC}"
echo -e "Test Groups Failed:  ${RED}${RESULTS_FAIL}${NC}"
echo "Total Test Groups:   $((RESULTS_PASS + RESULTS_FAIL))"
echo ""

# Coverage Analysis
echo "Coverage Analysis by Test Type:"
echo "==============================="
echo "Acceptance Criteria Tests: 7 test suites"
echo "  - AC#1: Story Template"
echo "  - AC#2: Changelog Guide"
echo "  - AC#3: Dev Skill Integration"
echo "  - AC#4: QA Skill Integration"
echo "  - AC#5: Release Skill Integration"
echo "  - AC#6: Project CHANGELOG"
echo "  - AC#7: Backward Compatibility"
echo ""
echo "Technical Specification Tests: 2 test suites"
echo "  - Entry Format Validation"
echo "  - Template Version Update"
echo ""

# Files Being Tested
echo "Test Coverage - Files Validated:"
echo "================================"
echo "Core Implementation Files:"
echo "  - .claude/references/changelog-update-guide.md"
echo "  - .claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
echo "  - .claude/skills/devforgeai-development/SKILL.md"
echo "  - .claude/skills/devforgeai-development/references/dod-update-workflow.md"
echo "  - .claude/skills/devforgeai-qa/SKILL.md"
echo "  - .claude/skills/devforgeai-release/SKILL.md"
echo "  - devforgeai/specs/context/source-tree.md"
echo "  - CHANGELOG.md (project root - creation validated)"
echo ""

# Final Result
echo "================================================================================"
if [ $RESULTS_FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TEST SUITES PASSED${NC}"
    echo "================================================================================"
    echo ""
    echo "STORY-152 is ready for implementation (TDD Red Phase Complete)"
    echo ""
    echo "Next Steps:"
    echo "1. Implement Story Template changes (AC#1)"
    echo "2. Create Changelog Reference Guide (AC#2)"
    echo "3. Update Dev Skill with changelog appends (AC#3)"
    echo "4. Update QA Skill with changelog appends (AC#4)"
    echo "5. Update Release Skill with changelog appends (AC#5)"
    echo "6. Create project CHANGELOG.md template (AC#6)"
    echo "7. Add backward compatibility logic (AC#7)"
    echo ""
    exit 0
else
    echo -e "${RED}✗ SOME TEST SUITES FAILED${NC}"
    echo "================================================================================"
    echo ""
    echo "Failed Tests:"
    for failed_test in "${FAILED_TESTS[@]}"; do
        echo "  - $failed_test"
    done
    echo ""
    echo "Review failed test output above for details."
    echo ""
    exit 1
fi
