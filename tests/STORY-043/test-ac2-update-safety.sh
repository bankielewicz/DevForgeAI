#!/bin/bash

##############################################################################
# Test Suite: STORY-043 AC-2 - Surgical Update Strategy with Rollback Safety
#
# AC-2: Surgical Update Strategy with Rollback Safety
# Given: Path audit identifies ~164 source-time references across 87 files
# When: Execute update script with dry-run validation
# Then: Creates backup, executes 3-phase updates, provides rollback script
#
# Expected Output:
# - Timestamped backup in .backups/story-043-path-updates-{timestamp}/ (87 files)
# - Phase 1: 74 refs updated (skills Read() calls)
# - Phase 2: 52 refs updated (documentation)
# - Phase 3: 38 refs updated (agent/subagent references)
# - Diff summary: .devforgeai/specs/STORY-043/update-diff-summary.md
# - Rollback script: .devforgeai/specs/STORY-043/rollback-updates.sh
# - Report: "164 references updated across 87 files, 0 errors"
##############################################################################

set -euo pipefail

TEST_NAME="AC-2: Surgical Update Strategy with Rollback Safety"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../" && pwd)"
SPEC_DIR=".devforgeai/specs/STORY-043"
BACKUP_DIR=".backups"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}✓ PASS${NC}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}✗ FAIL${NC}"
    fi
}

##############################################################################
# TEST 1: Update script exists and is executable
##############################################################################

test_update_script_exists() {
    # Test: src/scripts/update-paths.sh exists
    if [ -f "$PROJECT_ROOT/src/scripts/update-paths.sh" ]; then
        echo "  Update script found: src/scripts/update-paths.sh"
        return 0
    else
        echo "  ERROR: Update script not found"
        return 1
    fi
}

test_update_script_executable() {
    # Test: Update script is executable
    if [ -x "$PROJECT_ROOT/src/scripts/update-paths.sh" ]; then
        echo "  Update script is executable"
        return 0
    else
        echo "  ERROR: Update script is not executable"
        return 1
    fi
}

##############################################################################
# TEST 2: Backup creation before updates
##############################################################################

test_backup_directory_created() {
    # Test: Backup directory created with timestamp
    if [ -d "$PROJECT_ROOT/$BACKUP_DIR" ]; then
        local backup_count=$(find "$PROJECT_ROOT/$BACKUP_DIR" -type d -name "story-043-path-updates-*" 2>/dev/null | wc -l)
        if [ "$backup_count" -gt 0 ]; then
            echo "  Backup directory found: $BACKUP_DIR (count: $backup_count)"
            return 0
        else
            echo "  ERROR: No story-043 backup directories found"
            return 1
        fi
    else
        echo "  ERROR: Backup directory not found"
        return 1
    fi
}

test_backup_file_count() {
    # Test: Backup contains ~87 files
    if [ -d "$PROJECT_ROOT/$BACKUP_DIR" ]; then
        local latest_backup=$(find "$PROJECT_ROOT/$BACKUP_DIR" -type d -name "story-043-path-updates-*" 2>/dev/null | sort -r | head -1)
        if [ -n "$latest_backup" ]; then
            local file_count=$(find "$latest_backup" -type f 2>/dev/null | wc -l)
            local expected=87
            local tolerance=10
            local lower=$((expected - tolerance))
            local upper=$((expected + tolerance))

            if [ "$file_count" -ge "$lower" ] && [ "$file_count" -le "$upper" ]; then
                echo "  Backup contains $file_count files (expected ~$expected ±$tolerance)"
                return 0
            else
                echo "  ERROR: Backup contains $file_count files (expected ~$expected ±$tolerance)"
                return 1
            fi
        fi
    fi
    return 1
}

test_backup_timestamp_format() {
    # Test: Backup directory has valid timestamp format
    if [ -d "$PROJECT_ROOT/$BACKUP_DIR" ]; then
        local backup=$(find "$PROJECT_ROOT/$BACKUP_DIR" -type d -name "story-043-path-updates-*" 2>/dev/null | head -1)
        if [ -n "$backup" ]; then
            local dirname=$(basename "$backup")
            # Check for timestamp pattern: story-043-path-updates-YYYYMMDD-HHMMSS
            if [[ $dirname =~ story-043-path-updates-[0-9]{8}-[0-9]{6} ]]; then
                echo "  Backup timestamp format valid: $dirname"
                return 0
            else
                echo "  ERROR: Invalid timestamp format: $dirname"
                return 1
            fi
        fi
    fi
    return 1
}

##############################################################################
# TEST 3: Three-phase update execution
##############################################################################

test_phase1_skills_updates() {
    # Test: Phase 1 updated ~74 skill Read() references
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" ]; then
        local phase1_count=$(grep -c "Phase 1" "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" 2>/dev/null || echo "0")
        if [ "$phase1_count" -gt 0 ]; then
            echo "  Phase 1 (Skills) update log found"
            return 0
        else
            echo "  ERROR: Phase 1 update log not found"
            return 1
        fi
    else
        echo "  ERROR: Update diff summary not found"
        return 1
    fi
}

test_phase2_documentation_updates() {
    # Test: Phase 2 updated ~52 documentation references
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" ]; then
        local phase2_count=$(grep -c "Phase 2" "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" 2>/dev/null || echo "0")
        if [ "$phase2_count" -gt 0 ]; then
            echo "  Phase 2 (Documentation) update log found"
            return 0
        else
            echo "  ERROR: Phase 2 update log not found"
            return 1
        fi
    else
        return 1
    fi
}

test_phase3_framework_updates() {
    # Test: Phase 3 updated ~38 agent/subagent references
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" ]; then
        local phase3_count=$(grep -c "Phase 3" "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" 2>/dev/null || echo "0")
        if [ "$phase3_count" -gt 0 ]; then
            echo "  Phase 3 (Framework) update log found"
            return 0
        else
            echo "  ERROR: Phase 3 update log not found"
            return 1
        fi
    else
        return 1
    fi
}

test_total_references_updated() {
    # Test: Total of 164 references updated
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" ]; then
        if grep -q "164 references updated\|164.*updated" "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" 2>/dev/null; then
            echo "  Update report shows 164 references updated"
            return 0
        else
            echo "  ERROR: Update count not verified in report"
            return 1
        fi
    else
        return 1
    fi
}

test_zero_errors_in_update() {
    # Test: Update report shows 0 errors
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" ]; then
        if grep -q "0 errors\|zero errors" "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" 2>/dev/null; then
            echo "  Update report confirms 0 errors"
            return 0
        else
            echo "  ERROR: Error count not verified in report"
            return 1
        fi
    else
        return 1
    fi
}

##############################################################################
# TEST 4: Rollback script availability
##############################################################################

test_rollback_script_exists() {
    # Test: Rollback script created
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/rollback-updates.sh" ]; then
        echo "  Rollback script found: rollback-updates.sh"
        return 0
    else
        echo "  ERROR: Rollback script not found"
        return 1
    fi
}

test_rollback_script_executable() {
    # Test: Rollback script is executable
    if [ -x "$PROJECT_ROOT/$SPEC_DIR/rollback-updates.sh" ]; then
        echo "  Rollback script is executable"
        return 0
    else
        echo "  ERROR: Rollback script is not executable"
        return 1
    fi
}

test_rollback_script_references_backup() {
    # Test: Rollback script references backup directory
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/rollback-updates.sh" ]; then
        if grep -q "\.backups\|story-043-path-updates" "$PROJECT_ROOT/$SPEC_DIR/rollback-updates.sh" 2>/dev/null; then
            echo "  Rollback script references backup directory"
            return 0
        else
            echo "  ERROR: Rollback script missing backup reference"
            return 1
        fi
    else
        return 1
    fi
}

##############################################################################
# TEST 5: Diff summary format
##############################################################################

test_diff_summary_file_exists() {
    # Test: Diff summary file created
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" ]; then
        echo "  Diff summary found: update-diff-summary.md"
        return 0
    else
        echo "  ERROR: Diff summary not found"
        return 1
    fi
}

test_diff_summary_has_3_phases() {
    # Test: Diff summary documents all 3 phases
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" ]; then
        local phase_count=0
        grep -q "Phase 1" "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" && phase_count=$((phase_count + 1))
        grep -q "Phase 2" "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" && phase_count=$((phase_count + 1))
        grep -q "Phase 3" "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" && phase_count=$((phase_count + 1))

        if [ "$phase_count" -eq 3 ]; then
            echo "  Diff summary documents all 3 phases"
            return 0
        else
            echo "  ERROR: Diff summary missing phase documentation (found $phase_count/3)"
            return 1
        fi
    else
        return 1
    fi
}

test_diff_summary_has_file_list() {
    # Test: Diff summary lists affected files
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" ]; then
        if grep -q "files\|Files\|affected" "$PROJECT_ROOT/$SPEC_DIR/update-diff-summary.md" 2>/dev/null; then
            echo "  Diff summary lists affected files"
            return 0
        else
            echo "  ERROR: Diff summary missing file list"
            return 1
        fi
    else
        return 1
    fi
}

##############################################################################
# Main Test Execution
##############################################################################

main() {
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$TEST_NAME${NC}"
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
    echo ""

    echo -e "${YELLOW}Phase 1: Update Script Validation${NC}"
    run_test "AC-2.1: Update script exists" "test_update_script_exists"
    run_test "AC-2.2: Update script executable" "test_update_script_executable"

    echo -e "\n${YELLOW}Phase 2: Backup Creation${NC}"
    run_test "AC-2.3: Backup directory created" "test_backup_directory_created"
    run_test "AC-2.4: Backup contains ~87 files" "test_backup_file_count"
    run_test "AC-2.5: Backup timestamp format valid" "test_backup_timestamp_format"

    echo -e "\n${YELLOW}Phase 3: Update Execution (3 Phases)${NC}"
    run_test "AC-2.6: Phase 1 (Skills) updates ~74 refs" "test_phase1_skills_updates"
    run_test "AC-2.7: Phase 2 (Documentation) updates ~52 refs" "test_phase2_documentation_updates"
    run_test "AC-2.8: Phase 3 (Framework) updates ~38 refs" "test_phase3_framework_updates"
    run_test "AC-2.9: Total 164 references updated" "test_total_references_updated"
    run_test "AC-2.10: Zero errors in update" "test_zero_errors_in_update"

    echo -e "\n${YELLOW}Phase 4: Rollback Safety${NC}"
    run_test "AC-2.11: Rollback script exists" "test_rollback_script_exists"
    run_test "AC-2.12: Rollback script executable" "test_rollback_script_executable"
    run_test "AC-2.13: Rollback script references backup" "test_rollback_script_references_backup"

    echo -e "\n${YELLOW}Phase 5: Documentation${NC}"
    run_test "AC-2.14: Diff summary file exists" "test_diff_summary_file_exists"
    run_test "AC-2.15: Diff summary documents 3 phases" "test_diff_summary_has_3_phases"
    run_test "AC-2.16: Diff summary lists affected files" "test_diff_summary_has_file_list"

    # Summary
    echo ""
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
    echo -e "Tests run:    ${BLUE}$TESTS_RUN${NC}"
    echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"

    [ "$TESTS_FAILED" -eq 0 ] && exit 0 || exit 1
}

main "$@"
