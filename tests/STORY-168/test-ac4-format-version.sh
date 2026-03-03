#!/bin/bash
#
# Test: AC#4 - Script Updates format_version
# Story: STORY-168 - RCA-012 Story Migration Script
#
# AC#4: Script Updates format_version
#   Given: a story with `format_version: "2.0"`
#   When: the migration script runs
#   Then: `format_version` should be updated to `"2.1"`
#
# Additional Requirements:
#   - Only updates 2.0 to 2.1, not other versions
#   - Preserves YAML frontmatter structure
#   - Works with quoted and unquoted versions
#
# Test Framework: Bash shell script with assertions
# Uses shared test library: test-lib.sh
#

set -euo pipefail

# Import shared test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

echo "========================================================================"
echo "Test Suite: AC#4 - Script Updates format_version"
echo "Story: STORY-168 - RCA-012 Story Migration Script"
echo "========================================================================"
echo ""

# Setup fixtures before tests
setup_fixtures

# ============================================================================
# Test 1: Script updates format_version from 2.0 to 2.1
# ============================================================================
test_should_update_format_version() {
    echo "Test 1: Updates format_version from 2.0 to 2.1"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-version-1.story.md"
    create_fixture_story_v20 "$test_file" "STORY-001"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")
    assert_contains "$content" 'format_version: "2.1"' "Should update format_version to 2.1"
}

# ============================================================================
# Test 2: Script removes old format_version 2.0
# ============================================================================
test_should_remove_old_format_version() {
    echo "Test 2: Removes old format_version 2.0 after update"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-version-2.story.md"
    create_fixture_story_v20 "$test_file" "STORY-002"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")
    assert_not_contains "$content" 'format_version: "2.0"' "Should not contain old format_version 2.0"
}

# ============================================================================
# Test 3: Script preserves YAML frontmatter structure
# ============================================================================
test_should_preserve_frontmatter_structure() {
    echo "Test 3: Preserves YAML frontmatter structure"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-version-3.story.md"
    create_fixture_story_v20 "$test_file" "STORY-003"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")

    # Check frontmatter still starts and ends with ---
    local first_line=$(head -n 1 "$test_file" | tr -d '\r')
    assert_equal "---" "$first_line" "Frontmatter should still start with ---"

    # Check other frontmatter fields preserved
    assert_contains "$content" "id: STORY-003" "Should preserve id field"
    assert_contains "$content" "status: Backlog" "Should preserve status field"
}

# ============================================================================
# Test 4: Script does not modify files already at v2.1
# ============================================================================
test_should_not_modify_v21_files() {
    echo "Test 4: Does not modify files already at v2.1"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-version-4.story.md"
    create_fixture_story_v21 "$test_file" "STORY-004"

    # Store original content
    local original_content=$(cat "$test_file")

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local new_content=$(cat "$test_file")

    # The file content should be unchanged (or minimally changed)
    assert_contains "$new_content" 'format_version: "2.1"' "Should still be at v2.1"
    assert_contains "$new_content" "### AC#1:" "Should preserve existing AC format"
}

# ============================================================================
# Test 5: Script handles format_version with single quotes
# ============================================================================
test_should_handle_single_quoted_version() {
    echo "Test 5: Handles format_version with single quotes"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-version-5.story.md"

    # Create file with single quotes
    cat > "$test_file" << 'EOF'
---
id: STORY-005
format_version: '2.0'
status: Backlog
---

### 1. [ ] Test Criteria
Content here
EOF

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")
    # Should work with either quote style in output
    if echo "$content" | grep -q 'format_version: "2.1"'; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}PASS${NC} Updated single-quoted format_version"
    elif echo "$content" | grep -q "format_version: '2.1'"; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}PASS${NC} Updated single-quoted format_version (preserved quote style)"
    else
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Did not update single-quoted format_version"
    fi
}

# ============================================================================
# Test 6: Script handles unquoted version
# ============================================================================
test_should_handle_unquoted_version() {
    echo "Test 6: Handles unquoted format_version value"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-version-6.story.md"

    # Create file without quotes
    cat > "$test_file" << 'EOF'
---
id: STORY-006
format_version: 2.0
status: Backlog
---

### 1. [ ] Test Criteria
Content here
EOF

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")
    # Check for version update (any quote style or no quotes)
    if echo "$content" | grep -qE 'format_version: "?2\.1"?'; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}PASS${NC} Updated unquoted format_version"
    else
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Did not update unquoted format_version"
    fi
}

# ============================================================================
# Test 7: Script does not modify other version-like strings
# ============================================================================
test_should_not_modify_other_version_strings() {
    echo "Test 7: Does not modify non-format_version strings"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-version-7.story.md"

    cat > "$test_file" << 'EOF'
---
id: STORY-007
format_version: "2.0"
api_version: "2.0"
status: Backlog
---

# Description
This uses API version 2.0 for compatibility.

### 1. [ ] Test Criteria
Content here
EOF

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")
    assert_contains "$content" 'api_version: "2.0"' "Should not modify api_version field"
    assert_contains "$content" "API version 2.0" "Should not modify version text in content"
}

# ============================================================================
# Cleanup and run tests
# ============================================================================

test_should_update_format_version
echo ""

test_should_remove_old_format_version
echo ""

test_should_preserve_frontmatter_structure
echo ""

test_should_not_modify_v21_files
echo ""

test_should_handle_single_quoted_version
echo ""

test_should_handle_unquoted_version
echo ""

test_should_not_modify_other_version_strings
echo ""

# Cleanup fixtures
cleanup_fixtures

# ============================================================================
# Print summary
# ============================================================================
print_test_summary "AC#4 Test Results Summary"
exit_with_result
