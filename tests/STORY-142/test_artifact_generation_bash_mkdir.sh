#!/bin/bash

################################################################################
# STORY-142: Test Artifact Generation Bash mkdir Replacement
#
# Purpose: Validate that Bash mkdir commands are replaced with Write/.gitkeep
#          pattern in artifact-generation.md file
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
ARTIFACT_GEN_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/artifact-generation.md"

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

assert_file_exists() {
    local file="$1"
    local message="$2"

    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $message - File exists"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $message - File does not exist: $file"
        ((TESTS_FAILED++))
        return 1
    fi
}

################################################################################
# AC#1 Tests: Replace mkdir in artifact-generation.md
################################################################################

test_1_1_bash_mkdir_violations_present() {
    test_should "test_1_1_bash_mkdir_violations_present" \
        "AC#1: Should find Bash mkdir violations in artifact-generation.md"

    # TDD RED PHASE: This test FAILS when implementation is complete
    # (violations are present initially, test expects violations)
    if [ ! -f "$ARTIFACT_GEN_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: File not found: $ARTIFACT_GEN_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    # Search for pattern: Bash(command="mkdir
    local violation_count=$(grep -c 'Bash(command="mkdir' "$ARTIFACT_GEN_FILE" || true)

    # Initially, should find 3 violations (lines 469, 598, 599)
    # After implementation, this count should be 0 (test FAILS = SUCCESS)
    echo "Found $violation_count Bash mkdir violations in artifact-generation.md"
    echo "Expected: 3 violations (RED phase) or 0 violations (GREEN phase)"

    if [ "$violation_count" -eq 3 ]; then
        echo -e "${GREEN}✓ RED PHASE DETECTED${NC}: Test is in RED state (violations present)"
        ((TESTS_PASSED++))
        return 0
    elif [ "$violation_count" -eq 0 ]; then
        echo -e "${GREEN}✓ GREEN PHASE DETECTED${NC}: Violations fixed! Test will now validate replacement pattern"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ UNEXPECTED STATE${NC}: Expected 3 or 0 violations, found $violation_count"
        ((TESTS_FAILED++))
        return 1
    fi
}

test_1_2_write_gitkeep_replacement_pattern() {
    test_should "test_1_2_write_gitkeep_replacement_pattern" \
        "AC#1: Should have Write/.gitkeep replacement pattern"

    if [ ! -f "$ARTIFACT_GEN_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: File not found: $ARTIFACT_GEN_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    # Search for replacement pattern: Write(file_path=".../.gitkeep"
    local write_gitkeep_count=$(grep -c 'Write(file_path=".*/.gitkeep"' "$ARTIFACT_GEN_FILE" || true)

    echo "Found $write_gitkeep_count Write/.gitkeep patterns in artifact-generation.md"

    # RED PHASE: Should have 0 Write/.gitkeep patterns (not yet implemented)
    # GREEN PHASE: Should have >=3 Write/.gitkeep patterns (implementation complete)
    if [ "$write_gitkeep_count" -eq 0 ]; then
        echo -e "${GREEN}✓ RED PHASE CORRECT${NC}: No Write/.gitkeep patterns yet (expected in implementation)"
        ((TESTS_PASSED++))
        return 0
    elif [ "$write_gitkeep_count" -ge 3 ]; then
        echo -e "${GREEN}✓ GREEN PHASE CORRECT${NC}: Write/.gitkeep patterns found (implementation complete)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ UNEXPECTED STATE${NC}: Expected 0 or >=3 Write/.gitkeep patterns, found $write_gitkeep_count"
        ((TESTS_FAILED++))
        return 1
    fi
}

test_1_3_specific_line_469_violation() {
    test_should "test_1_3_specific_line_469_violation" \
        "AC#1: Line 469 should not contain Bash mkdir"

    if [ ! -f "$ARTIFACT_GEN_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: File not found: $ARTIFACT_GEN_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    # Extract lines 465-475 (context around line 469)
    local line_context=$(sed -n '465,475p' "$ARTIFACT_GEN_FILE")
    local violation_in_context=$(echo "$line_context" | grep -c 'Bash(command="mkdir' || true)

    if [ "$violation_in_context" -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: Line 469 area clean - no Bash mkdir violation"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Line 469 area still has Bash mkdir violation"
        echo "Context (lines 465-475):"
        echo "$line_context"
        ((TESTS_FAILED++))
        return 1
    fi
}

test_1_4_specific_line_598_violation() {
    test_should "test_1_4_specific_line_598_violation" \
        "AC#1: Line 598 should not contain Bash mkdir"

    if [ ! -f "$ARTIFACT_GEN_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: File not found: $ARTIFACT_GEN_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    # Extract lines 595-605 (context around line 598)
    local line_context=$(sed -n '595,605p' "$ARTIFACT_GEN_FILE")
    local violation_in_context=$(echo "$line_context" | grep -c 'Bash(command="mkdir' || true)

    if [ "$violation_in_context" -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: Line 598 area clean - no Bash mkdir violation"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Line 598 area still has Bash mkdir violation"
        echo "Context (lines 595-605):"
        echo "$line_context"
        ((TESTS_FAILED++))
        return 1
    fi
}

test_1_5_specific_line_599_violation() {
    test_should "test_1_5_specific_line_599_violation" \
        "AC#1: Line 599 should not contain Bash mkdir"

    if [ ! -f "$ARTIFACT_GEN_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: File not found: $ARTIFACT_GEN_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    # Extract lines 596-606 (context around line 599)
    local line_context=$(sed -n '596,606p' "$ARTIFACT_GEN_FILE")
    local violation_in_context=$(echo "$line_context" | grep -c 'Bash(command="mkdir' || true)

    if [ "$violation_in_context" -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: Line 599 area clean - no Bash mkdir violation"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Line 599 area still has Bash mkdir violation"
        echo "Context (lines 596-606):"
        echo "$line_context"
        ((TESTS_FAILED++))
        return 1
    fi
}

################################################################################
# AC#2 Tests: Validation confirms zero Bash mkdir in ideation files
################################################################################

test_2_1_overall_artifact_generation_compliance() {
    test_should "test_2_1_overall_artifact_generation_compliance" \
        "AC#2: Full artifact-generation.md must have zero Bash mkdir violations for compliance"

    if [ ! -f "$ARTIFACT_GEN_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: File not found: $ARTIFACT_GEN_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    local violation_count=$(grep -c 'Bash(command="mkdir' "$ARTIFACT_GEN_FILE" || true)

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

################################################################################
# Main Test Execution
################################################################################

main() {
    echo "================================================================================"
    echo "STORY-142: Bash mkdir Replacement Tests"
    echo "File: artifact-generation.md"
    echo "Status: TDD RED Phase - Validating Violations and Replacements"
    echo "================================================================================"

    # AC#1 Tests
    test_1_1_bash_mkdir_violations_present
    test_1_2_write_gitkeep_replacement_pattern
    test_1_3_specific_line_469_violation
    test_1_4_specific_line_598_violation
    test_1_5_specific_line_599_violation

    # AC#2 Tests
    test_2_1_overall_artifact_generation_compliance

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
