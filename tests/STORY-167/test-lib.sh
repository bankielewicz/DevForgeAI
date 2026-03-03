#!/bin/bash
#
# Shared Test Library for STORY-167 Tests
# Centralizes common assertion functions and utilities
# 
# Usage: source tests/STORY-167/test-lib.sh
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
# Constants
# ============================================================================
readonly TEMPLATE_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
readonly FRONTMATTER_LINES=10
readonly CHANGELOG_SECTION_MARKER="STORY TEMPLATE CHANGELOG"

# ============================================================================
# Assertion: assert_equal(expected, actual, message)
# Compares expected with actual value. Increments test counter.
# ============================================================================
assert_equal() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ "$expected" == "$actual" ]]; then
        echo -e "${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $message"
        echo "  Expected: $expected"
        echo "  Actual: $actual"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_not_empty(value, message)
# Verifies value is not empty string.
# ============================================================================
assert_not_empty() {
    local value="$1"
    local message="${2:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ -n "$value" ]]; then
        echo -e "${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $message"
        echo "  Value is empty"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_file_exists(file, message)
# Verifies file exists at given path.
# ============================================================================
assert_file_exists() {
    local file="$1"
    local message="${2:-File should exist: $file}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ -f "$file" ]]; then
        echo -e "${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $message"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_contains(haystack, needle, message)
# Verifies needle string exists in haystack (supports regex).
# ============================================================================
assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-String should contain value}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if echo "$haystack" | grep -q "$needle"; then
        echo -e "${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $message"
        echo "  Looking for: $needle"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Helper: extract_frontmatter(file_path)
# Extracts YAML frontmatter from file (first N lines)
# Usage: frontmatter=$(extract_frontmatter "$file")
# ============================================================================
extract_frontmatter() {
    local file="$1"
    if [[ -f "$file" ]]; then
        head -n "$FRONTMATTER_LINES" "$file"
    fi
}

# ============================================================================
# Helper: extract_field(file_path, field_name)
# Extracts YAML field value from file using grep/cut
# Usage: version=$(extract_field "$file" "template_version")
# Pattern: field_name: "value" OR field_name: value
# ============================================================================
extract_field() {
    local file="$1"
    local field_name="$2"
    
    if [[ -f "$file" ]]; then
        grep -o "${field_name}:\s*\"[^\"]*\"" "$file" | head -n 1 | cut -d'"' -f2 || echo ""
    else
        echo ""
    fi
}

# ============================================================================
# Helper: extract_first_occurrence(file_path, pattern)
# Extracts first match of regex pattern from file
# Usage: version=$(extract_first_occurrence "$file" 'template_version:\s*"[^"]*"')
# ============================================================================
extract_first_occurrence() {
    local file="$1"
    local pattern="$2"
    
    if [[ -f "$file" ]]; then
        grep -o "$pattern" "$file" | head -n 1 || echo ""
    else
        echo ""
    fi
}

# ============================================================================
# Helper: get_file_content(file_path)
# Safely reads entire file content or returns empty string
# Usage: content=$(get_file_content "$file")
# ============================================================================
get_file_content() {
    local file="$1"
    if [[ -f "$file" ]]; then
        cat "$file"
    fi
}

# ============================================================================
# Helper: validate_semantic_version(version_string)
# Validates version follows semantic versioning (X.Y or X.Y.Z)
# Usage: if validate_semantic_version "$version"; then ...
# ============================================================================
validate_semantic_version() {
    local version="$1"
    if [[ $version =~ ^[0-9]+\.[0-9]+(\.[0-9]+)?$ ]]; then
        return 0  # Valid
    else
        return 1  # Invalid
    fi
}

# ============================================================================
# Helper: validate_iso8601_date(date_string)
# Validates date follows ISO 8601 format (YYYY-MM-DD)
# Usage: if validate_iso8601_date "$date"; then ...
# ============================================================================
validate_iso8601_date() {
    local date="$1"
    if [[ $date =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        return 0  # Valid
    else
        return 1  # Invalid
    fi
}

# ============================================================================
# Helper: print_test_summary()
# Prints formatted test results summary
# Usage: print_test_summary "Test Suite Name"
# ============================================================================
print_test_summary() {
    local suite_name="${1:-Test Results}"
    
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
# Prints final PASSED/FAILED message and exits with appropriate code
# Usage: exit_with_result
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
# Resets test counters for starting new test run
# Usage: reset_test_counters
# ============================================================================
reset_test_counters() {
    TESTS_RUN=0
    TESTS_PASSED=0
    TESTS_FAILED=0
}
