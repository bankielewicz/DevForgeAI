#!/bin/bash
#
# Shared Test Library for STORY-169 Tests
# Phase Validation Checkpoint Testing Utilities
#
# Usage: source tests/STORY-169/test-lib.sh
#

# ============================================================================
# Color Constants
# ============================================================================
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'  # No Color

# ============================================================================
# Test Counters (Global)
# ============================================================================
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# ============================================================================
# Constants - Derive paths dynamically (no hardcoded absolute paths)
# ============================================================================
# Get directory where this test library is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate up to project root (tests/STORY-169 -> project root is 2 levels up)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

readonly PROJECT_ROOT
readonly SKILL_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md"
readonly PHASE_03_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/phases/phase-03-implementation.md"
readonly PHASE_04_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/phases/phase-04-refactoring.md"
readonly PHASE_05_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/phases/phase-05-integration.md"

# ============================================================================
# Assertion: assert_equal(expected, actual, message)
# ============================================================================
assert_equal() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ "$expected" == "$actual" ]]; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  Expected: $expected"
        echo "  Actual: $actual"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_file_exists(file, message)
# ============================================================================
assert_file_exists() {
    local file="$1"
    local message="${2:-File should exist: $file}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ -f "$file" ]]; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  File not found: $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_contains(haystack, needle, message)
# ============================================================================
assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-String should contain value}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if echo "$haystack" | grep -q -- "$needle"; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  Looking for: $needle"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_not_contains(haystack, needle, message)
# ============================================================================
assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-String should not contain value}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if ! echo "$haystack" | grep -q -- "$needle"; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  Should NOT contain: $needle"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_pattern_exists(file, pattern, message)
# Checks if a regex pattern exists in the file
# ============================================================================
assert_pattern_exists() {
    local file="$1"
    local pattern="$2"
    local message="${3:-Pattern should exist in file}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if grep -qE "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  Pattern not found: $pattern"
        echo "  In file: $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_section_exists(file, section_header, message)
# Checks if a markdown section header exists
# ============================================================================
assert_section_exists() {
    local file="$1"
    local section_header="$2"
    local message="${3:-Section should exist: $section_header}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if grep -q "^## $section_header\|^### $section_header" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  Section not found: $section_header"
        echo "  In file: $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_checkpoint_structure(file, phase_num, message)
# Verifies checkpoint follows the expected structure
# ============================================================================
assert_checkpoint_structure() {
    local file="$1"
    local phase_num="$2"
    local message="${3:-Checkpoint structure should be valid}"

    TESTS_RUN=$((TESTS_RUN + 1))

    local content
    content=$(cat "$file" 2>/dev/null)

    # Check for required checkpoint elements
    local has_verify_section=false
    local has_halt_logic=false
    local has_pass_logic=false

    if echo "$content" | grep -q "verify:"; then
        has_verify_section=true
    fi

    if echo "$content" | grep -qiE "(HALT|halt.*if|if.*fail)"; then
        has_halt_logic=true
    fi

    if echo "$content" | grep -qiE "(pass|proceed|Phase.*validation.*passed)"; then
        has_pass_logic=true
    fi

    if $has_verify_section || ($has_halt_logic && $has_pass_logic); then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  Missing checkpoint structure elements"
        echo "  Has verify section: $has_verify_section"
        echo "  Has HALT logic: $has_halt_logic"
        echo "  Has PASS logic: $has_pass_logic"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Helper: print_test_summary()
# ============================================================================
print_test_summary() {
    local suite_name="${1:-Test Results}"

    echo ""
    echo "========================================================================"
    echo "$suite_name"
    echo "========================================================================"
    echo "Tests run:    $TESTS_RUN"
    echo "Tests passed: $TESTS_PASSED"
    echo "Tests failed: $TESTS_FAILED"
    echo ""
}

# ============================================================================
# Helper: exit_with_result()
# ============================================================================
exit_with_result() {
    if [[ $TESTS_FAILED -gt 0 ]]; then
        echo -e "${RED}RESULT: FAILED${NC}"
        exit 1
    else
        echo -e "${GREEN}RESULT: PASSED${NC}"
        exit 0
    fi
}

# ============================================================================
# Helper: reset_test_counters()
# ============================================================================
reset_test_counters() {
    TESTS_RUN=0
    TESTS_PASSED=0
    TESTS_FAILED=0
}
