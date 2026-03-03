#!/bin/bash
#
# Test: AC#2 - Script Performs Find/Replace
# Story: STORY-168 - RCA-012 Story Migration Script
#
# AC#2: Script Performs Find/Replace
#   Given: a story with old format `### 1. [ ] Title`
#   When: I run the migration script on that story
#   Then: the AC headers should change to `### AC#1: Title`
#
# Additional Requirements:
#   - Works for numbered ACs (1-9+)
#   - Preserves the AC title after transformation
#   - Only transforms AC header lines, not other content
#
# Test Framework: Bash shell script with assertions
# Uses shared test library: test-lib.sh
#

set -euo pipefail

# Import shared test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

echo "========================================================================"
echo "Test Suite: AC#2 - Script Performs Find/Replace"
echo "Story: STORY-168 - RCA-012 Story Migration Script"
echo "========================================================================"
echo ""

# Setup fixtures before tests
setup_fixtures

# ============================================================================
# Test 1: Script converts `### 1. [ ] Title` to `### AC#1: Title`
# ============================================================================
test_should_convert_first_ac_format() {
    echo "Test 1: Converts '### 1. [ ] Title' to '### AC#1: Title'"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-story-1.story.md"
    create_fixture_story_v20 "$test_file" "STORY-001"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")
    assert_contains "$content" "### AC#1: First Acceptance Criteria" "Should convert AC#1 format"
}

# ============================================================================
# Test 2: Script converts `### 2. [ ] Title` to `### AC#2: Title`
# ============================================================================
test_should_convert_second_ac_format() {
    echo "Test 2: Converts '### 2. [ ] Title' to '### AC#2: Title'"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-story-2.story.md"
    create_fixture_story_v20 "$test_file" "STORY-002"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")
    assert_contains "$content" "### AC#2: Second Acceptance Criteria" "Should convert AC#2 format"
}

# ============================================================================
# Test 3: Script converts multiple AC headers in one file
# ============================================================================
test_should_convert_all_ac_headers() {
    echo "Test 3: Converts all AC headers in one file"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-story-3.story.md"
    create_fixture_story_v20 "$test_file" "STORY-003"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")

    # Count number of AC# headers after migration
    local ac_count=$(echo "$content" | grep -c "### AC#[0-9]:" || true)

    assert_equal "3" "$ac_count" "Should have converted all 3 AC headers"
}

# ============================================================================
# Test 4: Script removes checkbox notation `[ ]` from headers
# ============================================================================
test_should_remove_checkbox_notation() {
    echo "Test 4: Removes checkbox notation '[ ]' from headers"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-story-4.story.md"
    create_fixture_story_v20 "$test_file" "STORY-004"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")
    assert_not_contains "$content" "### [0-9]\. \[ \]" "Should not contain old checkbox format in headers"
}

# ============================================================================
# Test 5: Script preserves AC title text after colon
# ============================================================================
test_should_preserve_ac_title() {
    echo "Test 5: Preserves AC title text after transformation"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-story-5.story.md"
    create_fixture_story_v20 "$test_file" "STORY-005"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")
    assert_contains "$content" "First Acceptance Criteria" "Should preserve first AC title"
    assert_contains "$content" "Second Acceptance Criteria" "Should preserve second AC title"
    assert_contains "$content" "Third Acceptance Criteria" "Should preserve third AC title"
}

# ============================================================================
# Test 6: Script handles double-digit AC numbers (10+)
# ============================================================================
test_should_handle_double_digit_ac_numbers() {
    echo "Test 6: Handles double-digit AC numbers (10+)"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-story-6.story.md"

    # Create file with AC#10
    cat > "$test_file" << 'EOF'
---
id: STORY-006
format_version: "2.0"
---

### 10. [ ] Tenth Acceptance Criteria
Some content

### 11. [ ] Eleventh Acceptance Criteria
More content
EOF

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")
    assert_contains "$content" "### AC#10: Tenth Acceptance Criteria" "Should handle AC#10"
    assert_contains "$content" "### AC#11: Eleventh Acceptance Criteria" "Should handle AC#11"
}

# ============================================================================
# Test 7: Script does not modify non-AC header lines
# ============================================================================
test_should_not_modify_non_ac_lines() {
    echo "Test 7: Does not modify non-AC header lines"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-story-7.story.md"
    create_fixture_story_v20 "$test_file" "STORY-007"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")
    # Definition of Done checkboxes should remain unchanged
    assert_contains "$content" "- \[ \] Tests passing" "Should preserve DoD checkboxes"
}

# ============================================================================
# Test 8: Script does not modify Given/When/Then content
# ============================================================================
test_should_preserve_gherkin_content() {
    echo "Test 8: Preserves Given/When/Then content unchanged"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-story-8.story.md"
    create_fixture_story_v20 "$test_file" "STORY-008"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")
    assert_contains "$content" "Given a precondition" "Should preserve Given statements"
    assert_contains "$content" "When an action is taken" "Should preserve When statements"
    assert_contains "$content" "Then an outcome occurs" "Should preserve Then statements"
}

# ============================================================================
# Cleanup and run tests
# ============================================================================

test_should_convert_first_ac_format
echo ""

test_should_convert_second_ac_format
echo ""

test_should_convert_all_ac_headers
echo ""

test_should_remove_checkbox_notation
echo ""

test_should_preserve_ac_title
echo ""

test_should_handle_double_digit_ac_numbers
echo ""

test_should_not_modify_non_ac_lines
echo ""

test_should_preserve_gherkin_content
echo ""

# Cleanup fixtures
cleanup_fixtures

# ============================================================================
# Print summary
# ============================================================================
print_test_summary "AC#2 Test Results Summary"
exit_with_result
