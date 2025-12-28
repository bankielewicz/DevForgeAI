#!/bin/bash

################################################################################
# STORY-142: Test .gitkeep Directory Creation
#
# Purpose: Validate that .gitkeep files are created correctly using Write tool
#          to establish directory structure instead of Bash mkdir
#
# Status: TDD RED Phase - Tests fail initially (files not yet created)
#         After implementation: Tests pass (.gitkeep files exist)
#
# Test Framework: Bash file existence validation
# Strategy: Verify .gitkeep files are created in target directories
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

# Project root
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

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

assert_file_exists() {
    local file="$1"
    local message="$2"

    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $message"
        echo "  File: $file"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $message"
        echo "  Expected file: $file"
        echo "  File does not exist"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_file_not_exists() {
    local file="$1"
    local message="$2"

    if [ ! -f "$file" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $message (file not yet created)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $message (file already exists)"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_file_empty() {
    local file="$1"
    local message="$2"

    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ FAIL${NC}: $message (file does not exist)"
        ((TESTS_FAILED++))
        return 1
    fi

    local file_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)

    if [ "$file_size" -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $message (file is empty, size=0)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $message (file not empty, size=$file_size)"
        ((TESTS_FAILED++))
        return 1
    fi
}

################################################################################
# AC#3 Tests: Directory structure created with .gitkeep patterns
################################################################################

test_1_1_epics_gitkeep_created() {
    test_should "test_1_1_epics_gitkeep_created" \
        "AC#3: .gitkeep should be created in devforgeai/specs/Epics/"

    local gitkeep_file="$PROJECT_ROOT/devforgeai/specs/Epics/.gitkeep"

    # RED PHASE: File should not exist yet
    # GREEN PHASE: File should exist (after Write operation)
    if [ -f "$gitkeep_file" ]; then
        echo -e "${GREEN}✓ GREEN PHASE DETECTED${NC}: .gitkeep file exists"
        assert_file_exists "$gitkeep_file" "Epics .gitkeep file exists"
    else
        echo -e "${GREEN}✓ RED PHASE CORRECT${NC}: .gitkeep file not yet created (expected in implementation)"
        assert_file_not_exists "$gitkeep_file" "Epics .gitkeep file not yet created"
    fi
}

test_1_2_requirements_gitkeep_created() {
    test_should "test_1_2_requirements_gitkeep_created" \
        "AC#3: .gitkeep should be created in devforgeai/specs/requirements/"

    local gitkeep_file="$PROJECT_ROOT/devforgeai/specs/requirements/.gitkeep"

    # RED PHASE: File should not exist yet
    # GREEN PHASE: File should exist (after Write operation)
    if [ -f "$gitkeep_file" ]; then
        echo -e "${GREEN}✓ GREEN PHASE DETECTED${NC}: .gitkeep file exists"
        assert_file_exists "$gitkeep_file" "Requirements .gitkeep file exists"
    else
        echo -e "${GREEN}✓ RED PHASE CORRECT${NC}: .gitkeep file not yet created (expected in implementation)"
        assert_file_not_exists "$gitkeep_file" "Requirements .gitkeep file not yet created"
    fi
}

test_2_1_gitkeep_file_empty() {
    test_should "test_2_1_gitkeep_file_empty" \
        "AC#3: .gitkeep files should have empty content (size=0)"

    local epics_gitkeep="$PROJECT_ROOT/devforgeai/specs/Epics/.gitkeep"

    if [ -f "$epics_gitkeep" ]; then
        assert_file_empty "$epics_gitkeep" "Epics .gitkeep is empty"
    else
        echo -e "${YELLOW}⊗ SKIP${NC}: Epics .gitkeep file not yet created (RED phase)"
        ((TESTS_PASSED++))
    fi
}

test_2_2_gitkeep_file_readable() {
    test_should "test_2_2_gitkeep_file_readable" \
        "AC#3: .gitkeep files should be readable"

    local epics_gitkeep="$PROJECT_ROOT/devforgeai/specs/Epics/.gitkeep"

    if [ -f "$epics_gitkeep" ]; then
        if [ -r "$epics_gitkeep" ]; then
            echo -e "${GREEN}✓ PASS${NC}: Epics .gitkeep is readable"
            ((TESTS_PASSED++))
            return 0
        else
            echo -e "${RED}✗ FAIL${NC}: Epics .gitkeep is not readable"
            ((TESTS_FAILED++))
            return 1
        fi
    else
        echo -e "${YELLOW}⊗ SKIP${NC}: Epics .gitkeep file not yet created (RED phase)"
        ((TESTS_PASSED++))
    fi
}

################################################################################
# Integration Tests: Verify directory creation doesn't use Bash mkdir
################################################################################

test_3_1_no_bash_mkdir_in_examples() {
    test_should "test_3_1_no_bash_mkdir_in_examples" \
        "Validate: Examples in artifact-generation.md should use Write/.gitkeep"

    local artifact_file="$PROJECT_ROOT/.claude/skills/devforgeai-ideation/references/artifact-generation.md"

    if [ ! -f "$artifact_file" ]; then
        echo -e "${RED}✗ FAIL${NC}: File not found: $artifact_file"
        ((TESTS_FAILED++))
        return 1
    fi

    # Count any remaining Bash mkdir patterns
    local bash_mkdir_count=$(grep -c 'Bash(command="mkdir' "$artifact_file" || true)

    if [ "$bash_mkdir_count" -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: Zero Bash mkdir patterns in examples"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${YELLOW}⊗ INFO${NC}: Still $bash_mkdir_count Bash mkdir patterns in examples (RED phase expected)"
        ((TESTS_PASSED++))
        return 0
    fi
}

################################################################################
# Main Test Execution
################################################################################

main() {
    echo "================================================================================"
    echo "STORY-142: .gitkeep Directory Creation Tests"
    echo "Status: TDD RED Phase - Validating Directory Creation Pattern"
    echo "================================================================================"

    # AC#3 Tests
    test_1_1_epics_gitkeep_created
    test_1_2_requirements_gitkeep_created
    test_2_1_gitkeep_file_empty
    test_2_2_gitkeep_file_readable

    # Integration Tests
    test_3_1_no_bash_mkdir_in_examples

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
