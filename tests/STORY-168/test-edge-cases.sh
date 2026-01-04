#!/bin/bash
#
# Test: Edge Cases - Migration Script Robustness
# Story: STORY-168 - RCA-012 Story Migration Script
#
# Edge Cases from Story:
#   1. No matching patterns - Script should not error if story already in v2.1 format
#   2. Permission issues - Script should check write permissions
#   3. Non-story files - Script should only process .story.md files
#   4. Idempotency - Running twice should be safe (no harm)
#
# Test Framework: Bash shell script with assertions
# Uses shared test library: test-lib.sh
#

set -euo pipefail

# Import shared test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

echo "========================================================================"
echo "Test Suite: Edge Cases - Migration Script Robustness"
echo "Story: STORY-168 - RCA-012 Story Migration Script"
echo "========================================================================"
echo ""

# Setup fixtures before tests
setup_fixtures

# ============================================================================
# Edge Case 1: No matching patterns (already v2.1)
# ============================================================================
test_should_handle_already_v21_format() {
    echo "Edge Case 1: Handles files already in v2.1 format"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/edge-v21.story.md"
    create_fixture_story_v21 "$test_file" "STORY-V21"

    # Store original content
    local original_content=$(cat "$test_file")

    # Run migration script
    set +e
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1
    local exit_code=$?
    set -e

    # Should complete without error
    assert_exit_code 0 "$exit_code" "Script should not error on v2.1 files"

    # Content should be essentially unchanged
    local new_content=$(cat "$test_file")
    assert_contains "$new_content" 'format_version: "2.1"' "Should still have v2.1 format"
    assert_contains "$new_content" "### AC#1:" "Should still have new AC format"
}

# ============================================================================
# Edge Case 2: Idempotency - Running twice is safe
# ============================================================================
test_should_be_idempotent() {
    echo "Edge Case 2: Running twice is idempotent (safe)"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/edge-idempotent.story.md"
    create_fixture_story_v20 "$test_file" "STORY-IDEM"

    # Run migration script twice
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    # Store content after first run
    local content_after_first=$(cat "$test_file")

    # Run again
    set +e
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1
    local exit_code=$?
    set -e

    # Should complete without error
    assert_exit_code 0 "$exit_code" "Second run should not error"

    # Content should be same after second run
    local content_after_second=$(cat "$test_file")
    assert_equal "$content_after_first" "$content_after_second" "Content should be unchanged after second run"
}

# ============================================================================
# Edge Case 3: No double transformation of AC headers
# ============================================================================
test_should_not_double_transform_headers() {
    echo "Edge Case 3: Does not double-transform AC headers"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/edge-double.story.md"
    create_fixture_story_v20 "$test_file" "STORY-DBL"

    # Run migration script twice
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")

    # Should not have malformed headers like "### AC#AC#1:"
    assert_not_contains "$content" "### AC#AC#" "Should not have double AC# prefix"

    # Should have exactly the expected format
    assert_contains "$content" "### AC#1: First Acceptance Criteria" "Should have correct AC format"
}

# ============================================================================
# Edge Case 4: File not found error handling
# ============================================================================
test_should_handle_file_not_found() {
    echo "Edge Case 4: Handles file not found error"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local nonexistent_file="$FIXTURE_DIR/does-not-exist.story.md"

    # Run migration script on non-existent file
    local output
    local exit_code
    set +e
    output=$("$SCRIPT_FILE" "$nonexistent_file" 2>&1)
    exit_code=$?
    set -e

    # Should report error
    assert_exit_code 1 "$exit_code" "Should exit with error for non-existent file"
    assert_contains "$output" "Error\|not found\|No such file" "Should report file not found error"
}

# ============================================================================
# Edge Case 5: Mixed content file (v2.0 format with some already-migrated sections)
# ============================================================================
test_should_handle_mixed_format_file() {
    echo "Edge Case 5: Handles file with mixed format (partial migration)"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/edge-mixed.story.md"

    # Create file with mixed format (unlikely but possible)
    cat > "$test_file" << 'EOF'
---
id: STORY-MIXED
format_version: "2.0"
status: Backlog
---

### 1. [ ] Old Format AC
Content

### AC#2: Already Migrated AC
Content

### 3. [ ] Another Old Format AC
Content
EOF

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")

    # Should convert old format
    assert_contains "$content" "### AC#1: Old Format AC" "Should convert old format AC"
    assert_contains "$content" "### AC#3: Another Old Format AC" "Should convert other old format AC"

    # Should not double-convert already migrated
    assert_contains "$content" "### AC#2: Already Migrated AC" "Should preserve already-migrated AC"
    assert_not_contains "$content" "### AC#AC#2:" "Should not double-prefix already-migrated AC"
}

# ============================================================================
# Edge Case 6: File with special characters in title
# ============================================================================
test_should_handle_special_characters_in_title() {
    echo "Edge Case 6: Handles special characters in AC titles"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/edge-special.story.md"

    cat > "$test_file" << 'EOF'
---
id: STORY-SPECIAL
format_version: "2.0"
status: Backlog
---

### 1. [ ] AC with "quotes" and 'apostrophes'
Content

### 2. [ ] AC with $dollar and @symbols
Content

### 3. [ ] AC with (parentheses) and [brackets]
Content
EOF

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")

    assert_contains "$content" '### AC#1: AC with "quotes"' "Should preserve quotes in title"
    assert_contains "$content" '### AC#2: AC with $dollar' "Should preserve special characters"
    assert_contains "$content" "### AC#3: AC with (parentheses)" "Should preserve parentheses"
}

# ============================================================================
# Edge Case 7: Very large AC number
# ============================================================================
test_should_handle_large_ac_numbers() {
    echo "Edge Case 7: Handles large AC numbers (99+)"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/edge-large.story.md"

    cat > "$test_file" << 'EOF'
---
id: STORY-LARGE
format_version: "2.0"
status: Backlog
---

### 99. [ ] Ninety-Ninth AC
Content

### 100. [ ] One Hundredth AC
Content
EOF

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    local content=$(cat "$test_file")

    assert_contains "$content" "### AC#99: Ninety-Ninth AC" "Should handle AC#99"
    assert_contains "$content" "### AC#100: One Hundredth AC" "Should handle AC#100"
}

# ============================================================================
# Edge Case 8: Windows line endings (CRLF)
# ============================================================================
test_should_handle_crlf_line_endings() {
    echo "Edge Case 8: Handles Windows line endings (CRLF)"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/edge-crlf.story.md"

    # Create file and convert to CRLF
    create_fixture_story_v20 "$test_file" "STORY-CRLF"

    # Convert to Windows line endings if unix2dos is available
    if command -v unix2dos &> /dev/null; then
        unix2dos "$test_file" 2>/dev/null
    elif command -v sed &> /dev/null; then
        sed -i 's/$/\r/' "$test_file"
    fi

    # Run migration script
    set +e
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1
    local exit_code=$?
    set -e

    assert_exit_code 0 "$exit_code" "Should handle CRLF line endings without error"
}

# ============================================================================
# Edge Case 9: Empty file
# ============================================================================
test_should_handle_empty_file() {
    echo "Edge Case 9: Handles empty file"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/edge-empty.story.md"

    # Create empty file
    touch "$test_file"

    # Run migration script
    set +e
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1
    local exit_code=$?
    set -e

    # Should not crash on empty file
    assert_exit_code 0 "$exit_code" "Should handle empty file without error"
}

# ============================================================================
# Edge Case 10: File with no AC headers
# ============================================================================
test_should_handle_file_without_ac_headers() {
    echo "Edge Case 10: Handles file with no AC headers"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/edge-no-ac.story.md"

    cat > "$test_file" << 'EOF'
---
id: STORY-NO-AC
format_version: "2.0"
status: Backlog
---

# Story without AC headers

Just some content here.
No acceptance criteria defined yet.
EOF

    # Run migration script
    set +e
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1
    local exit_code=$?
    set -e

    # Should complete without error
    assert_exit_code 0 "$exit_code" "Should handle file without AC headers"

    # Should still update format_version
    local content=$(cat "$test_file")
    assert_contains "$content" 'format_version: "2.1"' "Should still update format_version"
}

# ============================================================================
# Cleanup and run tests
# ============================================================================

test_should_handle_already_v21_format
echo ""

test_should_be_idempotent
echo ""

test_should_not_double_transform_headers
echo ""

test_should_handle_file_not_found
echo ""

test_should_handle_mixed_format_file
echo ""

test_should_handle_special_characters_in_title
echo ""

test_should_handle_large_ac_numbers
echo ""

test_should_handle_crlf_line_endings
echo ""

test_should_handle_empty_file
echo ""

test_should_handle_file_without_ac_headers
echo ""

# Cleanup fixtures
cleanup_fixtures

# ============================================================================
# Print summary
# ============================================================================
print_test_summary "Edge Cases Test Results Summary"
exit_with_result
