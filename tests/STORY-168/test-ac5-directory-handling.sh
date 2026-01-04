#!/bin/bash
#
# Test: AC#5 - Script Handles Multiple Stories
# Story: STORY-168 - RCA-012 Story Migration Script
#
# AC#5: Script Handles Multiple Stories
#   Given: a directory with multiple stories
#   When: I run the script with a directory path
#   Then: all `.story.md` files should be migrated
#
# Additional Requirements:
#   - Processes only .story.md files
#   - Creates backup for each file
#   - Provides summary of migrated files
#
# Test Framework: Bash shell script with assertions
# Uses shared test library: test-lib.sh
#

set -euo pipefail

# Import shared test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

echo "========================================================================"
echo "Test Suite: AC#5 - Script Handles Multiple Stories"
echo "Story: STORY-168 - RCA-012 Story Migration Script"
echo "========================================================================"
echo ""

# Setup fixtures before tests
setup_fixtures

# ============================================================================
# Test 1: Script accepts directory path argument
# ============================================================================
test_should_accept_directory_argument() {
    echo "Test 1: Script accepts directory path as argument"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_dir="$FIXTURE_DIR/stories"
    mkdir -p "$test_dir"
    create_fixture_story_v20 "$test_dir/STORY-001.story.md" "STORY-001"

    # Run migration script on directory
    set +e
    "$SCRIPT_FILE" "$test_dir" > /dev/null 2>&1
    local exit_code=$?
    set -e

    assert_exit_code 0 "$exit_code" "Script should exit successfully when given a directory"
}

# ============================================================================
# Test 2: Script migrates all .story.md files in directory
# ============================================================================
test_should_migrate_all_story_files() {
    echo "Test 2: Migrates all .story.md files in directory"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_dir="$FIXTURE_DIR/multi-stories"
    mkdir -p "$test_dir"

    # Create multiple story files
    create_fixture_story_v20 "$test_dir/STORY-001.story.md" "STORY-001"
    create_fixture_story_v20 "$test_dir/STORY-002.story.md" "STORY-002"
    create_fixture_story_v20 "$test_dir/STORY-003.story.md" "STORY-003"

    # Run migration script on directory
    "$SCRIPT_FILE" "$test_dir" > /dev/null 2>&1

    # Check all files were migrated
    local story1_content=$(cat "$test_dir/STORY-001.story.md")
    local story2_content=$(cat "$test_dir/STORY-002.story.md")
    local story3_content=$(cat "$test_dir/STORY-003.story.md")

    assert_contains "$story1_content" "### AC#1:" "STORY-001 should be migrated"
    assert_contains "$story2_content" "### AC#1:" "STORY-002 should be migrated"
    assert_contains "$story3_content" "### AC#1:" "STORY-003 should be migrated"
}

# ============================================================================
# Test 3: Script creates backup for each file
# ============================================================================
test_should_create_backup_for_each_file() {
    echo "Test 3: Creates backup for each migrated file"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_dir="$FIXTURE_DIR/backup-stories"
    mkdir -p "$test_dir"

    # Create multiple story files
    create_fixture_story_v20 "$test_dir/STORY-010.story.md" "STORY-010"
    create_fixture_story_v20 "$test_dir/STORY-011.story.md" "STORY-011"

    # Run migration script on directory
    "$SCRIPT_FILE" "$test_dir" > /dev/null 2>&1

    # Check backup files exist
    assert_file_exists "$test_dir/STORY-010.story.md.backup" "Backup for STORY-010 should exist"
    assert_file_exists "$test_dir/STORY-011.story.md.backup" "Backup for STORY-011 should exist"
}

# ============================================================================
# Test 4: Script ignores non-.story.md files
# ============================================================================
test_should_ignore_non_story_files() {
    echo "Test 4: Ignores non-.story.md files"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_dir="$FIXTURE_DIR/mixed-files"
    mkdir -p "$test_dir"

    # Create story file
    create_fixture_story_v20 "$test_dir/STORY-020.story.md" "STORY-020"

    # Create non-story files with similar content
    cat > "$test_dir/README.md" << 'EOF'
### 1. [ ] This should NOT be changed
format_version: "2.0"
EOF

    cat > "$test_dir/notes.txt" << 'EOF'
### 1. [ ] This should NOT be changed
format_version: "2.0"
EOF

    # Run migration script on directory
    "$SCRIPT_FILE" "$test_dir" > /dev/null 2>&1

    # Check story file was migrated
    local story_content=$(cat "$test_dir/STORY-020.story.md")
    assert_contains "$story_content" "### AC#1:" "Story file should be migrated"

    # Check non-story files were NOT modified
    local readme_content=$(cat "$test_dir/README.md")
    local notes_content=$(cat "$test_dir/notes.txt")

    assert_contains "$readme_content" "### 1. \[ \]" "README.md should not be modified"
    assert_contains "$notes_content" "### 1. \[ \]" "notes.txt should not be modified"
}

# ============================================================================
# Test 5: Script handles empty directory gracefully
# ============================================================================
test_should_handle_empty_directory() {
    echo "Test 5: Handles empty directory gracefully"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_dir="$FIXTURE_DIR/empty-dir"
    mkdir -p "$test_dir"

    # Run migration script on empty directory
    set +e
    local output=$("$SCRIPT_FILE" "$test_dir" 2>&1)
    local exit_code=$?
    set -e

    # Should complete without error
    assert_exit_code 0 "$exit_code" "Script should handle empty directory without error"
}

# ============================================================================
# Test 6: Script handles directory with only v2.1 files
# ============================================================================
test_should_handle_already_migrated_directory() {
    echo "Test 6: Handles directory with only v2.1 files"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_dir="$FIXTURE_DIR/v21-only"
    mkdir -p "$test_dir"

    # Create v2.1 files only
    create_fixture_story_v21 "$test_dir/STORY-030.story.md" "STORY-030"
    create_fixture_story_v21 "$test_dir/STORY-031.story.md" "STORY-031"

    # Run migration script on directory
    set +e
    "$SCRIPT_FILE" "$test_dir" > /dev/null 2>&1
    local exit_code=$?
    set -e

    assert_exit_code 0 "$exit_code" "Script should handle already-migrated directory without error"
}

# ============================================================================
# Test 7: Script provides migration summary
# ============================================================================
test_should_provide_migration_summary() {
    echo "Test 7: Provides migration summary output"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_dir="$FIXTURE_DIR/summary-test"
    mkdir -p "$test_dir"

    create_fixture_story_v20 "$test_dir/STORY-040.story.md" "STORY-040"

    # Run migration script and capture output
    local output=$("$SCRIPT_FILE" "$test_dir" 2>&1 || true)

    # Check for migration completion message
    if echo "$output" | grep -qi "migrat" || echo "$output" | grep -qi "complete"; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}PASS${NC} Script provides migration summary"
    else
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script should provide migration summary"
    fi
}

# ============================================================================
# Test 8: Script handles subdirectories correctly (non-recursive)
# ============================================================================
test_should_not_recurse_into_subdirectories() {
    echo "Test 8: Does not recurse into subdirectories (processes top-level only)"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found"
        return
    fi

    local test_dir="$FIXTURE_DIR/nested"
    mkdir -p "$test_dir/subdir"

    # Create story in root and subdirectory
    create_fixture_story_v20 "$test_dir/STORY-050.story.md" "STORY-050"
    create_fixture_story_v20 "$test_dir/subdir/STORY-051.story.md" "STORY-051"

    # Run migration script on parent directory only
    "$SCRIPT_FILE" "$test_dir" > /dev/null 2>&1

    # Check root file was migrated
    local root_content=$(cat "$test_dir/STORY-050.story.md")
    assert_contains "$root_content" "### AC#1:" "Root-level story should be migrated"

    # Check subdirectory file was NOT migrated (per spec, script uses *.story.md glob)
    local sub_content=$(cat "$test_dir/subdir/STORY-051.story.md")
    # Note: Based on technical spec, script uses "$TARGET"/*.story.md which is non-recursive
    assert_contains "$sub_content" "### 1. \[ \]" "Subdirectory story should not be migrated (non-recursive)"
}

# ============================================================================
# Cleanup and run tests
# ============================================================================

test_should_accept_directory_argument
echo ""

test_should_migrate_all_story_files
echo ""

test_should_create_backup_for_each_file
echo ""

test_should_ignore_non_story_files
echo ""

test_should_handle_empty_directory
echo ""

test_should_handle_already_migrated_directory
echo ""

test_should_provide_migration_summary
echo ""

test_should_not_recurse_into_subdirectories
echo ""

# Cleanup fixtures
cleanup_fixtures

# ============================================================================
# Print summary
# ============================================================================
print_test_summary "AC#5 Test Results Summary"
exit_with_result
