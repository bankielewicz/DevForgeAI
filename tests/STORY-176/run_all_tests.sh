#!/bin/bash
###############################################################################
# Test Runner: STORY-176 - Add Slash Command Exclusions to Anti-Pattern Scanner
# Purpose: Execute all acceptance criteria tests
# TDD Phase: RED (tests should FAIL until implementation)
###############################################################################

set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../.."  # Navigate to project root

echo "============================================================"
echo "STORY-176: Add Slash Command Exclusions to Anti-Pattern Scanner"
echo "============================================================"
echo ""
echo "Running all acceptance criteria tests..."
echo "Expected: ALL tests should FAIL (TDD RED phase)"
echo ""

TOTAL_TESTS=0
TOTAL_PASS=0
TOTAL_FAIL=0

run_test() {
    local test_file="$1"
    local test_name="$2"

    echo ""
    echo "------------------------------------------------------------"
    echo "Running: $test_name"
    echo "------------------------------------------------------------"

    if bash "$test_file" 2>&1; then
        echo ""
        echo "Result: PASSED"
        TOTAL_PASS=$((TOTAL_PASS + 1))
    else
        echo ""
        echo "Result: FAILED (expected in RED phase)"
        TOTAL_FAIL=$((TOTAL_FAIL + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

# Run all AC tests
run_test "$SCRIPT_DIR/test_ac1_exclusions_section.sh" "AC#1: Exclusions Section Added"
run_test "$SCRIPT_DIR/test_ac2_command_files_excluded.sh" "AC#2: Command Files Excluded from Structure Validation"
run_test "$SCRIPT_DIR/test_ac3_skill_files_excluded.sh" "AC#3: Skill Files Excluded from Code Smell Detection"
run_test "$SCRIPT_DIR/test_ac4_prereport_verification.sh" "AC#4: Pre-Report Verification"
run_test "$SCRIPT_DIR/test_ac5_skip_security_code_examples.sh" "AC#5: Skip Security Scanning on Code Examples"
run_test "$SCRIPT_DIR/test_ac6_zero_false_positives.sh" "AC#6: Zero False Positives"

echo ""
echo "============================================================"
echo "STORY-176 Test Summary"
echo "============================================================"
echo ""
echo "Total Test Suites: $TOTAL_TESTS"
echo "Passed Suites: $TOTAL_PASS"
echo "Failed Suites: $TOTAL_FAIL"
echo ""

if [ $TOTAL_FAIL -gt 0 ]; then
    echo "STATUS: TDD RED PHASE"
    echo ""
    echo "All tests are failing as expected. This is correct for TDD."
    echo ""
    echo "Next Steps:"
    echo "1. Implement ## Exclusions section in anti-pattern-scanner.md"
    echo "2. Add ## Pre-Report Verification section"
    echo "3. Update Phase 3 to skip .claude/commands/*.md files"
    echo "4. Update Phase 5 to skip .claude/skills/**/*.md files"
    echo "5. Update Phase 6 to skip fenced code blocks"
    echo "6. Document zero false positive expectation"
    echo ""
    exit 1
else
    echo "STATUS: TDD GREEN PHASE"
    echo ""
    echo "All tests passing! Implementation complete."
    exit 0
fi
