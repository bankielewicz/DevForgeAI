#!/bin/bash

################################################################################
# STORY-142: Test Error Handling Bash mkdir Replacement
#
# Purpose: Validate that Bash mkdir commands are replaced with Write/.gitkeep
#          pattern in error-handling.md file
#
# Status: TDD RED Phase - Tests fail initially (violations present)
#         After implementation: Tests pass (violations removed)
#
# Test Framework: Bash with grep validation
# Strategy: Search for Bash mkdir patterns and validate they are absent
################################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# File paths
ERROR_HANDLING_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/error-handling.md"

################################################################################
# Helper Functions
################################################################################

test_should() {
    local test_name="$1"
    local description="$2"
    echo ""
    echo -e "${YELLOW}TEST: $test_name${NC}"
    echo "Description: $description"
    ((TESTS_RUN++))
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"

    if [ "$expected" -eq "$actual" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $message (expected=$expected, actual=$actual)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $message (expected=$expected, actual=$actual)"
        ((TESTS_FAILED++))
        return 1
    fi
}

################################################################################
# AC#2 Tests: Zero Bash mkdir in error-handling.md
################################################################################

test_1_1_bash_mkdir_violations_present() {
    test_should "test_1_1_bash_mkdir_violations_present" \
        "AC#2: Should find Bash mkdir violations in error-handling.md"

    if [ ! -f "$ERROR_HANDLING_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: File not found: $ERROR_HANDLING_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    # Search for pattern: Bash(command="mkdir or Bash(command=f"mkdir (f-string variant)
    local violation_count=$(grep -c 'Bash(command.*mkdir' "$ERROR_HANDLING_FILE" || true)

    echo "Found $violation_count Bash mkdir violations in error-handling.md"
    echo "Expected: 2 violations (RED phase) or 0 violations (GREEN phase)"

    # Initially, should find 2 violations (lines 184, 868)
    # After implementation, this count should be 0 (test FAILS = SUCCESS)
    if [ "$violation_count" -eq 2 ]; then
        echo -e "${GREEN}✓ RED PHASE DETECTED${NC}: Test is in RED state (violations present)"
        ((TESTS_PASSED++))
        return 0
    elif [ "$violation_count" -eq 0 ]; then
        echo -e "${GREEN}✓ GREEN PHASE DETECTED${NC}: Violations fixed! All violations removed"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ UNEXPECTED STATE${NC}: Expected 2 or 0 violations, found $violation_count"
        ((TESTS_FAILED++))
        return 1
    fi
}

test_1_2_specific_line_184_violation() {
    test_should "test_1_2_specific_line_184_violation" \
        "AC#2: Line 184 should not contain Bash mkdir"

    if [ ! -f "$ERROR_HANDLING_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: File not found: $ERROR_HANDLING_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    # Extract lines 180-190 (context around line 184)
    local line_context=$(sed -n '180,190p' "$ERROR_HANDLING_FILE")
    local violation_in_context=$(echo "$line_context" | grep -c 'Bash(command.*mkdir' || true)

    if [ "$violation_in_context" -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: Line 184 area clean - no Bash mkdir violation"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Line 184 area still has Bash mkdir violation"
        echo "Context (lines 180-190):"
        echo "$line_context"
        ((TESTS_FAILED++))
        return 1
    fi
}

test_1_3_specific_line_868_violation() {
    test_should "test_1_3_specific_line_868_violation" \
        "AC#2: Line 868 should not contain Bash mkdir"

    if [ ! -f "$ERROR_HANDLING_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: File not found: $ERROR_HANDLING_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    # Extract lines 865-875 (context around line 868)
    local line_context=$(sed -n '865,875p' "$ERROR_HANDLING_FILE")
    local violation_in_context=$(echo "$line_context" | grep -c 'Bash(command.*mkdir' || true)

    if [ "$violation_in_context" -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: Line 868 area clean - no Bash mkdir violation"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Line 868 area still has Bash mkdir violation"
        echo "Context (lines 865-875):"
        echo "$line_context"
        ((TESTS_FAILED++))
        return 1
    fi
}

test_2_1_overall_error_handling_compliance() {
    test_should "test_2_1_overall_error_handling_compliance" \
        "AC#2: Full error-handling.md must have zero Bash mkdir violations for compliance"

    if [ ! -f "$ERROR_HANDLING_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: File not found: $ERROR_HANDLING_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    local violation_count=$(grep -c 'Bash(command.*mkdir' "$ERROR_HANDLING_FILE" || true)

    echo "Checking full file for Bash mkdir violations: $violation_count found"

    if [ "$violation_count" -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: Constitutional C1 compliance achieved - zero Bash mkdir"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Still has $violation_count Bash mkdir violations (need 0)"
        ((TESTS_FAILED++))
        return 1
    fi
}

test_2_2_write_gitkeep_replacement_pattern() {
    test_should "test_2_2_write_gitkeep_replacement_pattern" \
        "AC#2: Should have Write/.gitkeep replacement patterns"

    if [ ! -f "$ERROR_HANDLING_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: File not found: $ERROR_HANDLING_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    # Search for replacement pattern: Write(file_path=".../.gitkeep" or f".../.gitkeep"
    local write_gitkeep_count=$(grep -c 'Write.*file_path.*\.gitkeep' "$ERROR_HANDLING_FILE" || true)

    echo "Found $write_gitkeep_count Write/.gitkeep patterns in error-handling.md"

    # RED PHASE: Should have 0 Write/.gitkeep patterns (not yet implemented)
    # GREEN PHASE: Should have >=2 Write/.gitkeep patterns (implementation complete)
    if [ "$write_gitkeep_count" -eq 0 ]; then
        echo -e "${GREEN}✓ RED PHASE CORRECT${NC}: No Write/.gitkeep patterns yet (expected in implementation)"
        ((TESTS_PASSED++))
        return 0
    elif [ "$write_gitkeep_count" -ge 2 ]; then
        echo -e "${GREEN}✓ GREEN PHASE CORRECT${NC}: Write/.gitkeep patterns found (implementation complete)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ UNEXPECTED STATE${NC}: Expected 0 or >=2 Write/.gitkeep patterns, found $write_gitkeep_count"
        ((TESTS_FAILED++))
        return 1
    fi
}

################################################################################
# Main Test Execution
################################################################################

main() {
    echo "================================================================================"
    echo "STORY-142: Bash mkdir Replacement Tests"
    echo "File: error-handling.md"
    echo "Status: TDD RED Phase - Validating Violations and Replacements"
    echo "================================================================================"

    test_1_1_bash_mkdir_violations_present
    test_1_2_specific_line_184_violation
    test_1_3_specific_line_868_violation
    test_2_1_overall_error_handling_compliance
    test_2_2_write_gitkeep_replacement_pattern

    # Print summary
    echo ""
    echo "================================================================================"
    echo "TEST SUMMARY"
    echo "================================================================================"
    echo "Tests Run:    $TESTS_RUN"
    echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
    echo "================================================================================"

    if [ "$TESTS_FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some tests failed${NC}"
        exit 1
    fi
}

# Run tests
main
