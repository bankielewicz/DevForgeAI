#!/bin/bash
#
# Shared Test Library for STORY-168 Tests
# Migration Script Testing Utilities
#
# Usage: source tests/STORY-168/test-lib.sh
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

# Navigate up to project root (tests/STORY-168 -> project root is 2 levels up)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

readonly PROJECT_ROOT
readonly SCRIPT_PATH=".claude/scripts/migrate-ac-headers.sh"
readonly SCRIPT_FILE="${PROJECT_ROOT}/${SCRIPT_PATH}"
readonly FIXTURE_DIR="${PROJECT_ROOT}/tests/STORY-168/fixtures"

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
# Assertion: assert_not_empty(value, message)
# Verifies value is not empty string.
# ============================================================================
assert_not_empty() {
    local value="$1"
    local message="${2:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ -n "$value" ]]; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
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
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  File not found: $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_file_not_exists(file, message)
# Verifies file does NOT exist at given path.
# ============================================================================
assert_file_not_exists() {
    local file="$1"
    local message="${2:-File should not exist: $file}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ ! -f "$file" ]]; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  File unexpectedly exists: $file"
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
# Verifies needle string does NOT exist in haystack.
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
# Assertion: assert_executable(file, message)
# Verifies file is executable.
# ============================================================================
assert_executable() {
    local file="$1"
    local message="${2:-File should be executable: $file}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ -x "$file" ]]; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  File not executable: $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_exit_code(expected, actual, message)
# Verifies command exit code matches expected.
# ============================================================================
assert_exit_code() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Exit code should match}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ "$expected" -eq "$actual" ]]; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  Expected exit code: $expected"
        echo "  Actual exit code: $actual"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Helper: create_fixture_story(file_path, format_version)
# Creates a test story file with old v2.0 format
# ============================================================================
create_fixture_story_v20() {
    local file_path="$1"
    local story_id="${2:-STORY-TEST}"

    mkdir -p "$(dirname "$file_path")"

    cat > "$file_path" << 'EOF'
---
id: ${story_id}
title: "Test Story"
format_version: "2.0"
status: Backlog
---

# ${story_id}: Test Story

## Acceptance Criteria

### 1. [ ] First Acceptance Criteria
Given a precondition
When an action is taken
Then an outcome occurs

### 2. [ ] Second Acceptance Criteria
Given another precondition
When another action is taken
Then another outcome occurs

### 3. [ ] Third Acceptance Criteria
Given yet another precondition
When yet another action is taken
Then yet another outcome occurs

## Definition of Done
- [ ] Tests passing
EOF

    # Replace variable placeholders
    sed -i "s/\${story_id}/$story_id/g" "$file_path"
}

# ============================================================================
# Helper: create_fixture_story_v21(file_path, story_id)
# Creates a test story file with new v2.1 format (already migrated)
# ============================================================================
create_fixture_story_v21() {
    local file_path="$1"
    local story_id="${2:-STORY-TEST}"

    mkdir -p "$(dirname "$file_path")"

    cat > "$file_path" << 'EOF'
---
id: ${story_id}
title: "Already Migrated Story"
format_version: "2.1"
status: Backlog
---

# ${story_id}: Already Migrated Story

## Acceptance Criteria

### AC#1: First Acceptance Criteria
Given a precondition
When an action is taken
Then an outcome occurs

### AC#2: Second Acceptance Criteria
Given another precondition
When another action is taken
Then another outcome occurs

## Definition of Done
- [ ] Tests passing
EOF

    # Replace variable placeholders
    sed -i "s/\${story_id}/$story_id/g" "$file_path"
}

# ============================================================================
# Helper: cleanup_fixtures()
# Removes all fixture files and directories
# ============================================================================
cleanup_fixtures() {
    if [[ -d "$FIXTURE_DIR" ]]; then
        rm -rf "$FIXTURE_DIR"
    fi
}

# ============================================================================
# Helper: setup_fixtures()
# Creates fixture directory
# ============================================================================
setup_fixtures() {
    cleanup_fixtures
    mkdir -p "$FIXTURE_DIR"
}

# ============================================================================
# Helper: print_test_summary()
# Prints formatted test results summary
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
# Prints final PASSED/FAILED message and exits with appropriate code
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
# ============================================================================
reset_test_counters() {
    TESTS_RUN=0
    TESTS_PASSED=0
    TESTS_FAILED=0
}
