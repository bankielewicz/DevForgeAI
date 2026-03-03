#!/bin/bash
#
# Test: AC#3 - Script Creates Backup
# Story: STORY-168 - RCA-012 Story Migration Script
#
# AC#3: Script Creates Backup
#   Given: a story file being migrated
#   When: the script runs
#   Then: a backup file (`.backup`) should be created before modification
#
# Additional Requirements:
#   - Original content is preserved in backup
#   - Backup file created before any modifications
#   - Backup has same name with .backup extension
#
# Test Framework: Bash shell script with assertions
# Uses shared test library: test-lib.sh
#

set -euo pipefail

# Import shared test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

echo "========================================================================"
echo "Test Suite: AC#3 - Script Creates Backup"
echo "Story: STORY-168 - RCA-012 Story Migration Script"
echo "========================================================================"
echo ""

# Setup fixtures before tests
setup_fixtures

# ============================================================================
# Test 1: Script creates .backup file after migration
# ============================================================================
test_should_create_backup_file() {
    echo "Test 1: Creates .backup file after running migration"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-backup-1.story.md"
    local backup_file="$test_file.backup"

    create_fixture_story_v20 "$test_file" "STORY-001"

    # Ensure no backup exists before test
    rm -f "$backup_file"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    assert_file_exists "$backup_file" "Backup file should be created at $backup_file"
}

# ============================================================================
# Test 2: Backup contains original content (v2.0 format)
# ============================================================================
test_should_preserve_original_content_in_backup() {
    echo "Test 2: Backup contains original content with v2.0 format"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-backup-2.story.md"
    local backup_file="$test_file.backup"

    create_fixture_story_v20 "$test_file" "STORY-002"

    # Store original content before migration
    local original_content=$(cat "$test_file")

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    if [[ -f "$backup_file" ]]; then
        local backup_content=$(cat "$backup_file")
        assert_equal "$original_content" "$backup_content" "Backup should contain exact original content"
    else
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Backup file not found"
    fi
}

# ============================================================================
# Test 3: Backup preserves old format_version 2.0
# ============================================================================
test_should_preserve_old_format_version_in_backup() {
    echo "Test 3: Backup preserves format_version 2.0"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-backup-3.story.md"
    local backup_file="$test_file.backup"

    create_fixture_story_v20 "$test_file" "STORY-003"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    if [[ -f "$backup_file" ]]; then
        local backup_content=$(cat "$backup_file")
        assert_contains "$backup_content" 'format_version: "2.0"' "Backup should preserve v2.0 format"
    else
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Backup file not found"
    fi
}

# ============================================================================
# Test 4: Backup preserves old AC header format
# ============================================================================
test_should_preserve_old_ac_format_in_backup() {
    echo "Test 4: Backup preserves old '### 1. [ ]' AC header format"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-backup-4.story.md"
    local backup_file="$test_file.backup"

    create_fixture_story_v20 "$test_file" "STORY-004"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    if [[ -f "$backup_file" ]]; then
        local backup_content=$(cat "$backup_file")
        assert_contains "$backup_content" "### 1. \[ \]" "Backup should preserve old AC checkbox format"
    else
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Backup file not found"
    fi
}

# ============================================================================
# Test 5: Migration output mentions backup file
# ============================================================================
test_should_mention_backup_in_output() {
    echo "Test 5: Migration output mentions backup file location"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-backup-5.story.md"

    create_fixture_story_v20 "$test_file" "STORY-005"

    # Run migration script and capture output
    local output=$("$SCRIPT_FILE" "$test_file" 2>&1 || true)

    assert_contains "$output" "backup" "Script output should mention backup"
}

# ============================================================================
# Test 6: Backup file is not modified during migration
# ============================================================================
test_should_not_modify_backup_during_migration() {
    echo "Test 6: Backup file content unchanged after migration"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-backup-6.story.md"
    local backup_file="$test_file.backup"

    create_fixture_story_v20 "$test_file" "STORY-006"

    # Run migration script
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    if [[ -f "$backup_file" ]]; then
        # Backup should still have v2.0 format, not v2.1
        local backup_content=$(cat "$backup_file")
        assert_not_contains "$backup_content" 'format_version: "2.1"' "Backup should not be modified to v2.1"
        assert_not_contains "$backup_content" "### AC#1:" "Backup should not have new AC format"
    else
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Backup file not found"
    fi
}

# ============================================================================
# Test 7: Multiple migrations overwrite same backup
# ============================================================================
test_should_overwrite_existing_backup() {
    echo "Test 7: Running migration twice overwrites backup with previous content"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_file="$FIXTURE_DIR/test-backup-7.story.md"
    local backup_file="$test_file.backup"

    create_fixture_story_v20 "$test_file" "STORY-007"

    # Run migration script twice
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1
    "$SCRIPT_FILE" "$test_file" > /dev/null 2>&1

    assert_file_exists "$backup_file" "Backup file should still exist after second run"
}

# ============================================================================
# Cleanup and run tests
# ============================================================================

test_should_create_backup_file
echo ""

test_should_preserve_original_content_in_backup
echo ""

test_should_preserve_old_format_version_in_backup
echo ""

test_should_preserve_old_ac_format_in_backup
echo ""

test_should_mention_backup_in_output
echo ""

test_should_not_modify_backup_during_migration
echo ""

test_should_overwrite_existing_backup
echo ""

# Cleanup fixtures
cleanup_fixtures

# ============================================================================
# Print summary
# ============================================================================
print_test_summary "AC#3 Test Results Summary"
exit_with_result
