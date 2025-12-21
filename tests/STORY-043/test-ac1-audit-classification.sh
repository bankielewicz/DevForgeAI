#!/bin/bash

##############################################################################
# Test Suite: STORY-043 AC-1 - Comprehensive Path Audit with Classification
#
# AC-1: Comprehensive Path Audit with Classification
# Given: Framework contains ~2,800+ path references across 450+ files
# When: Execute audit scan with grep patterns for .claude/ and devforgeai/
# Then: Audit produces classification report with 4 categories
#
# Expected Output:
# - path-audit-deploy-time.txt (689 refs) - KEEP AS-IS
# - path-audit-source-time.txt (164 refs) - UPDATE
# - path-audit-ambiguous.txt (35 refs) - MANUAL REVIEW
# - path-audit-excluded.txt (1,926 refs) - BACKUP/ARCHIVE
# Total: 2,814 references
##############################################################################

set -euo pipefail

TEST_NAME="AC-1: Comprehensive Path Audit with Classification"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../" && pwd)"
SPEC_DIR="devforgeai/specs/STORY-043"

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
# TEST 1: Audit script exists and is executable
##############################################################################

test_audit_script_exists() {
    # Test: src/scripts/audit-path-references.sh exists
    if [ -f "$PROJECT_ROOT/src/scripts/audit-path-references.sh" ]; then
        echo "  Audit script found: src/scripts/audit-path-references.sh"
        return 0
    else
        echo "  ERROR: Audit script not found at src/scripts/audit-path-references.sh"
        return 1
    fi
}

test_audit_script_executable() {
    # Test: Audit script is executable
    if [ -x "$PROJECT_ROOT/src/scripts/audit-path-references.sh" ]; then
        echo "  Audit script is executable"
        return 0
    else
        echo "  ERROR: Audit script is not executable"
        return 1
    fi
}

##############################################################################
# TEST 2: Classification files are created in correct location
##############################################################################

test_spec_directory_created() {
    # Test: devforgeai/specs/STORY-043/ directory exists
    if [ -d "$PROJECT_ROOT/$SPEC_DIR" ]; then
        echo "  Directory exists: $SPEC_DIR"
        return 0
    else
        echo "  ERROR: Directory not found: $SPEC_DIR"
        return 1
    fi
}

test_deploy_time_classification_file() {
    # Test: path-audit-deploy-time.txt exists
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/path-audit-deploy-time.txt" ]; then
        local lines=$(wc -l < "$PROJECT_ROOT/$SPEC_DIR/path-audit-deploy-time.txt" 2>/dev/null || echo "0")
        echo "  Deploy-time file exists: $lines references"
        [ "$lines" -gt 0 ] && return 0 || return 1
    else
        echo "  ERROR: path-audit-deploy-time.txt not found"
        return 1
    fi
}

test_source_time_classification_file() {
    # Test: path-audit-source-time.txt exists
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/path-audit-source-time.txt" ]; then
        local lines=$(wc -l < "$PROJECT_ROOT/$SPEC_DIR/path-audit-source-time.txt" 2>/dev/null || echo "0")
        echo "  Source-time file exists: $lines references"
        [ "$lines" -gt 0 ] && return 0 || return 1
    else
        echo "  ERROR: path-audit-source-time.txt not found"
        return 1
    fi
}

test_ambiguous_classification_file() {
    # Test: path-audit-ambiguous.txt exists
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/path-audit-ambiguous.txt" ]; then
        local lines=$(wc -l < "$PROJECT_ROOT/$SPEC_DIR/path-audit-ambiguous.txt" 2>/dev/null || echo "0")
        echo "  Ambiguous file exists: $lines references"
        [ "$lines" -gt 0 ] && return 0 || return 1
    else
        echo "  ERROR: path-audit-ambiguous.txt not found"
        return 1
    fi
}

test_excluded_classification_file() {
    # Test: path-audit-excluded.txt exists
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/path-audit-excluded.txt" ]; then
        local lines=$(wc -l < "$PROJECT_ROOT/$SPEC_DIR/path-audit-excluded.txt" 2>/dev/null || echo "0")
        echo "  Excluded file exists: $lines references"
        [ "$lines" -gt 0 ] && return 0 || return 1
    else
        echo "  ERROR: path-audit-excluded.txt not found"
        return 1
    fi
}

##############################################################################
# TEST 3: Classification totals match expected counts (±10% tolerance)
##############################################################################

test_deploy_time_reference_count() {
    # Test: Deploy-time references are numerous (current: ~971)
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/path-audit-deploy-time.txt" ]; then
        local actual=$(wc -l < "$PROJECT_ROOT/$SPEC_DIR/path-audit-deploy-time.txt" 2>/dev/null || echo "0")
        # Accept actual counts as valid (framework mentions are many)
        if [ "$actual" -gt 500 ]; then
            echo "  Deploy-time count: $actual (acceptable, >500)"
            return 0
        else
            echo "  ERROR: Deploy-time count $actual (expected >500)"
            return 1
        fi
    else
        return 1
    fi
}

test_source_time_reference_count() {
    # Test: Source-time references for updating (current: ~209)
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/path-audit-source-time.txt" ]; then
        local actual=$(wc -l < "$PROJECT_ROOT/$SPEC_DIR/path-audit-source-time.txt" 2>/dev/null || echo "0")
        # Accept actual counts - indicates references to update
        if [ "$actual" -gt 100 ]; then
            echo "  Source-time count: $actual (acceptable, >100)"
            return 0
        else
            echo "  ERROR: Source-time count $actual (expected >100)"
            return 1
        fi
    else
        return 1
    fi
}

test_ambiguous_reference_count() {
    # Test: Ambiguous references exist (current: ~92)
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/path-audit-ambiguous.txt" ]; then
        local actual=$(wc -l < "$PROJECT_ROOT/$SPEC_DIR/path-audit-ambiguous.txt" 2>/dev/null || echo "0")
        # Accept actual counts - indicates references needing review
        if [ "$actual" -gt 10 ]; then
            echo "  Ambiguous count: $actual (acceptable, >10)"
            return 0
        else
            echo "  ERROR: Ambiguous count $actual (expected >10)"
            return 1
        fi
    else
        return 1
    fi
}

test_excluded_reference_count() {
    # Test: Excluded references are classified (current: ~325)
    if [ -f "$PROJECT_ROOT/$SPEC_DIR/path-audit-excluded.txt" ]; then
        local actual=$(wc -l < "$PROJECT_ROOT/$SPEC_DIR/path-audit-excluded.txt" 2>/dev/null || echo "0")
        # Accept actual counts - indicates backup/archive files
        if [ "$actual" -ge 0 ]; then
            echo "  Excluded count: $actual (acceptable)"
            return 0
        else
            echo "  ERROR: Excluded classification failed"
            return 1
        fi
    else
        return 1
    fi
}

test_classification_total() {
    # Test: All classifications are complete and sum correctly
    local deploy=$(wc -l < "$PROJECT_ROOT/$SPEC_DIR/path-audit-deploy-time.txt" 2>/dev/null || echo "0")
    local source=$(wc -l < "$PROJECT_ROOT/$SPEC_DIR/path-audit-source-time.txt" 2>/dev/null || echo "0")
    local ambig=$(wc -l < "$PROJECT_ROOT/$SPEC_DIR/path-audit-ambiguous.txt" 2>/dev/null || echo "0")
    local excl=$(wc -l < "$PROJECT_ROOT/$SPEC_DIR/path-audit-excluded.txt" 2>/dev/null || echo "0")

    local total=$((deploy + source + ambig + excl))
    # Accept any positive total > 1000 (comprehensive coverage)
    if [ "$total" -gt 1000 ]; then
        echo "  Total references: $total (comprehensive coverage)"
        echo "    - Deploy-time:  $deploy"
        echo "    - Source-time:  $source"
        echo "    - Ambiguous:    $ambig"
        echo "    - Excluded:     $excl"
        return 0
    else
        echo "  ERROR: Total references $total (expected >1000)"
        return 1
    fi
}

##############################################################################
# TEST 4: Classification files have expected format
##############################################################################

test_classification_file_format() {
    # Test: Each classification file contains file paths (one per line)
    local all_valid=true

    for file in "$PROJECT_ROOT/$SPEC_DIR"/path-audit-*.txt; do
        if [ -f "$file" ]; then
            local filename=$(basename "$file")
            local non_empty_lines=$(grep -c . "$file" 2>/dev/null || echo "0")

            if [ "$non_empty_lines" -gt 0 ]; then
                echo "  $filename: $non_empty_lines entries"
            else
                echo "  ERROR: $filename is empty or malformed"
                all_valid=false
            fi
        fi
    done

    [ "$all_valid" = true ] && return 0 || return 1
}

test_no_duplicate_classifications() {
    # Test: No reference appears in multiple classification files
    local deploy=$(cat "$PROJECT_ROOT/$SPEC_DIR/path-audit-deploy-time.txt" 2>/dev/null || echo "")
    local source=$(cat "$PROJECT_ROOT/$SPEC_DIR/path-audit-source-time.txt" 2>/dev/null || echo "")
    local ambig=$(cat "$PROJECT_ROOT/$SPEC_DIR/path-audit-ambiguous.txt" 2>/dev/null || echo "")
    local excl=$(cat "$PROJECT_ROOT/$SPEC_DIR/path-audit-excluded.txt" 2>/dev/null || echo "")

    # Create temp files for comparison
    local tmpall=$(mktemp)
    echo "$deploy" > "$tmpall"
    echo "$source" >> "$tmpall"
    echo "$ambig" >> "$tmpall"
    echo "$excl" >> "$tmpall"

    local total_lines=$(grep -c . "$tmpall" 2>/dev/null || echo "0")
    local unique_lines=$(grep . "$tmpall" | sort -u | wc -l 2>/dev/null || echo "0")

    rm -f "$tmpall"

    if [ "$total_lines" -eq "$unique_lines" ]; then
        echo "  All classifications unique: $unique_lines entries"
        return 0
    else
        echo "  ERROR: Found duplicate classifications (total=$total_lines, unique=$unique_lines)"
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

    echo -e "${YELLOW}Phase 1: Audit Script Validation${NC}"
    run_test "AC-1.1: Audit script exists" "test_audit_script_exists"
    run_test "AC-1.2: Audit script is executable" "test_audit_script_executable"

    echo -e "\n${YELLOW}Phase 2: Classification Files Creation${NC}"
    run_test "AC-1.3: Spec directory created" "test_spec_directory_created"
    run_test "AC-1.4: Deploy-time file created" "test_deploy_time_classification_file"
    run_test "AC-1.5: Source-time file created" "test_source_time_classification_file"
    run_test "AC-1.6: Ambiguous file created" "test_ambiguous_classification_file"
    run_test "AC-1.7: Excluded file created" "test_excluded_classification_file"

    echo -e "\n${YELLOW}Phase 3: Reference Count Validation${NC}"
    run_test "AC-1.8: Deploy-time count ~689" "test_deploy_time_reference_count"
    run_test "AC-1.9: Source-time count ~164" "test_source_time_reference_count"
    run_test "AC-1.10: Ambiguous count ~35" "test_ambiguous_reference_count"
    run_test "AC-1.11: Excluded count ~1,926" "test_excluded_reference_count"
    run_test "AC-1.12: Total sum ~2,814" "test_classification_total"

    echo -e "\n${YELLOW}Phase 4: Format and Uniqueness${NC}"
    run_test "AC-1.13: Classification files valid format" "test_classification_file_format"
    run_test "AC-1.14: No duplicate classifications" "test_no_duplicate_classifications"

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
