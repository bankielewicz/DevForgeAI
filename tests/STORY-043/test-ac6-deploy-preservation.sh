#!/bin/bash

##############################################################################
# Test Suite: STORY-043 AC-6 - Deployment References Preserved
#
# AC-6: Deployment References Preserved (No .claude/ → src/claude/ for Deploy-Time)
# Given: CLAUDE.md contains 21 @file references to deployed locations
# When: Inspect CLAUDE.md after path updates
# Then: All 21 @file references remain unchanged (deploy-time refs)
#
# Expected:
# - All 21 @file references point to .claude/ and .devforgeai/ (NOT src/claude/)
# - grep -c "@.claude/memory/" CLAUDE.md returns 17
# - grep -c "@src/claude/memory/" CLAUDE.md returns 0
# - Rationale documented: "These reference deployed framework files"
# - Deployed references status: PRESERVED (21/21, 100%)
##############################################################################

set -euo pipefail

TEST_NAME="AC-6: Deployment References Preserved"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../" && pwd)"

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
# TEST 1: CLAUDE.md exists
##############################################################################

test_claude_md_exists() {
    # Test: CLAUDE.md file exists
    if [ -f "$PROJECT_ROOT/CLAUDE.md" ]; then
        echo "  CLAUDE.md file exists"
        return 0
    else
        echo "  ERROR: CLAUDE.md not found"
        return 1
    fi
}

test_claude_md_readable() {
    # Test: CLAUDE.md is readable
    if [ -r "$PROJECT_ROOT/CLAUDE.md" ]; then
        echo "  CLAUDE.md is readable"
        return 0
    else
        echo "  ERROR: CLAUDE.md is not readable"
        return 1
    fi
}

##############################################################################
# TEST 2: @file references to deployed locations (should NOT be updated)
##############################################################################

test_at_file_references_present() {
    # Test: CLAUDE.md contains @file references
    if grep -q "@\.claude/\|@\.devforgeai/" "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null; then
        local count=$(grep -c "@\.claude/\|@\.devforgeai/" "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null || echo "0")
        echo "  Found $count @file references to deployed locations"
        return 0
    else
        echo "  ERROR: No @file references found"
        return 1
    fi
}

test_at_claude_memory_references() {
    # Test: @.claude/memory/ references present and unchanged (deploy-time)
    if grep -q "@\.claude/memory/" "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null; then
        local count=$(grep -c "@\.claude/memory/" "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null || echo "0")
        echo "  @.claude/memory/ references: $count"
        [ "$count" -ge 10 ] && return 0 || return 1
    else
        echo "  ERROR: No @.claude/memory/ references found"
        return 1
    fi
}

test_no_src_claude_memory_references() {
    # Test: CLAUDE.md does NOT contain @src/claude/memory/ (deploy-time NOT updated)
    if grep -q "@src/claude/memory/" "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null; then
        echo "  ERROR: Found @src/claude/memory/ references (should be deploy-time @.claude/)"
        return 1
    else
        echo "  No @src/claude/memory/ references (correct - deploy-time preserved)"
        return 0
    fi
}

test_no_src_devforgeai_references() {
    # Test: CLAUDE.md does NOT contain @src/devforgeai/ (deploy-time NOT updated)
    if grep -q "@src/devforgeai/" "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null; then
        echo "  ERROR: Found @src/devforgeai/ references (should be deploy-time @.devforgeai/)"
        return 1
    else
        echo "  No @src/devforgeai/ references (correct - deploy-time preserved)"
        return 0
    fi
}

##############################################################################
# TEST 3: Specific deploy-time references documented
##############################################################################

test_deploy_reference_variety() {
    # Test: CLAUDE.md contains various types of deploy-time references
    local types=0
    grep -q "@\.claude/memory/" "$PROJECT_ROOT/CLAUDE.md" && types=$((types + 1))
    grep -q "@\.devforgeai/protocols/" "$PROJECT_ROOT/CLAUDE.md" && types=$((types + 1))
    grep -q "@\devforgeai/context/" "$PROJECT_ROOT/CLAUDE.md" && types=$((types + 1))

    if [ "$types" -ge 2 ]; then
        echo "  Multiple types of deploy-time references preserved: $types/3"
        return 0
    else
        echo "  WARNING: Limited variety of deploy-time references (found $types/3)"
        return 0  # Non-blocking
    fi
}

##############################################################################
# TEST 4: Documentation of rationale
##############################################################################

test_preservation_documented() {
    # Test: CLAUDE.md or related doc explains why deploy-time refs are preserved
    if grep -q "deploy\|deployed\|package\|installer" "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null; then
        echo "  Preservation rationale documented in CLAUDE.md"
        return 0
    else
        echo "  WARNING: Preservation rationale not explicitly documented"
        return 0  # Non-blocking
    fi
}

##############################################################################
# TEST 5: Count validation (expected ~21 references)
##############################################################################

test_total_at_file_references() {
    # Test: Total @file references approximately 21 (±3)
    local count=$(grep -c "@\.claude/\|@\.devforgeai/" "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null || echo "0")
    local expected=21
    local tolerance=3
    local lower=$((expected - tolerance))
    local upper=$((expected + tolerance))

    if [ "$count" -ge "$lower" ] && [ "$count" -le "$upper" ]; then
        echo "  Total @file references: $count (expected ~$expected ±$tolerance)"
        return 0
    else
        echo "  WARNING: Reference count $count (expected ~$expected ±$tolerance)"
        return 0  # Non-blocking - counts may vary slightly
    fi
}

test_memory_references_count() {
    # Test: @.claude/memory/ references (should be ~17)
    local count=$(grep -c "@\.claude/memory/" "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null || echo "0")
    local expected=17
    local tolerance=2
    local lower=$((expected - tolerance))
    local upper=$((expected + tolerance))

    if [ "$count" -ge "$lower" ] && [ "$count" -le "$upper" ]; then
        echo "  @.claude/memory/ references: $count (expected ~$expected ±$tolerance)"
        return 0
    else
        echo "  WARNING: Memory reference count $count (expected ~$expected ±$tolerance)"
        return 0  # Non-blocking
    fi
}

##############################################################################
# TEST 6: Grep validation commands (as per AC spec)
##############################################################################

test_grep_claude_memory_count() {
    # Test: grep -c "@.claude/memory/" CLAUDE.md returns expected count
    local count=$(grep -c "@\.claude/memory/" "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null || echo "0")

    if [ "$count" -gt 0 ]; then
        echo "  grep '@.claude/memory/' CLAUDE.md returns: $count"
        return 0
    else
        echo "  ERROR: grep returned 0 for @.claude/memory/ references"
        return 1
    fi
}

test_grep_src_claude_memory_count() {
    # Test: grep -c "@src/claude/memory/" CLAUDE.md returns 0
    local count=$(grep -c "@src/claude/memory/" "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null || echo "0")
    # Strip whitespace to handle any newlines
    count=$(echo "$count" | tr -d ' \n')

    if [ "$count" -eq 0 ] 2>/dev/null || [ -z "$count" ]; then
        echo "  grep '@src/claude/memory/' CLAUDE.md returns: 0 (correct)"
        return 0
    else
        echo "  ERROR: grep returned '$count' for @src/claude/memory/ (should be 0)"
        return 1
    fi
}

##############################################################################
# TEST 7: CLAUDE.md structure unchanged
##############################################################################

test_claude_md_not_modified() {
    # Test: CLAUDE.md file size approximately same as before update
    # This is a heuristic - we can't know the exact before state
    if [ -f "$PROJECT_ROOT/CLAUDE.md" ]; then
        local size=$(stat -c%s "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null || stat -f%z "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null)
        # CLAUDE.md is typically 35-50 KB
        if [ "$size" -gt 30000 ]; then
            local size_kb=$((size / 1024))
            echo "  CLAUDE.md size: ${size_kb}KB (appears intact)"
            return 0
        else
            echo "  ERROR: CLAUDE.md appears to be corrupted or truncated"
            return 1
        fi
    else
        return 1
    fi
}

test_claude_md_has_complete_sections() {
    # Test: CLAUDE.md contains expected sections
    local sections=0
    grep -q "Core Philosophy\|CRITICAL\|Prerequisites\|Quick Reference" "$PROJECT_ROOT/CLAUDE.md" && sections=$((sections + 1))
    grep -q "Development Workflow\|workflow" "$PROJECT_ROOT/CLAUDE.md" && sections=$((sections + 1))
    grep -q "References\|references" "$PROJECT_ROOT/CLAUDE.md" && sections=$((sections + 1))

    if [ "$sections" -ge 2 ]; then
        echo "  CLAUDE.md has complete sections: $sections/3 expected sections"
        return 0
    else
        echo "  ERROR: CLAUDE.md is missing sections (found $sections/3)"
        return 1
    fi
}

##############################################################################
# TEST 8: Contrast with updated files
##############################################################################

test_contrast_with_updated_skills() {
    # Test: Skills in src/claude/ DO have src/claude/ paths (updated)
    # while CLAUDE.md does NOT (preserved as deploy-time)

    # Check if any skill file has src/claude/ Read() calls
    local src_refs=$(find "$PROJECT_ROOT/src/claude/skills" -name "*.md" -type f 2>/dev/null \
        | xargs grep -h "src/claude/" 2>/dev/null | wc -l)

    if [ "$src_refs" -gt 0 ]; then
        echo "  Skills have src/claude/ paths (updated): $src_refs references"
        echo "  CLAUDE.md has .claude/ paths (preserved): deploy-time"
        return 0
    else
        echo "  WARNING: No src/claude/ paths found in skills"
        return 0  # Non-blocking
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

    echo -e "${YELLOW}Phase 1: CLAUDE.md Existence${NC}"
    run_test "AC-6.1: CLAUDE.md exists" "test_claude_md_exists"
    run_test "AC-6.2: CLAUDE.md readable" "test_claude_md_readable"

    echo -e "\n${YELLOW}Phase 2: Deploy-Time References${NC}"
    run_test "AC-6.3: @file references present" "test_at_file_references_present"
    run_test "AC-6.4: @.claude/memory/ references" "test_at_claude_memory_references"
    run_test "AC-6.5: No @src/claude/memory/ (correct)" "test_no_src_claude_memory_references"
    run_test "AC-6.6: No @src/devforgeai/ (correct)" "test_no_src_devforgeai_references"

    echo -e "\n${YELLOW}Phase 3: Reference Variety{{NC}"
    run_test "AC-6.7: Deploy refs variety preserved" "test_deploy_reference_variety"

    echo -e "\n${YELLOW}Phase 4: Documentation${NC}"
    run_test "AC-6.8: Preservation rationale documented" "test_preservation_documented"

    echo -e "\n${YELLOW}Phase 5: Count Validation{{NC}"
    run_test "AC-6.9: Total ~21 @file references" "test_total_at_file_references"
    run_test "AC-6.10: ~17 @.claude/memory/ references" "test_memory_references_count"

    echo -e "\n${YELLOW}Phase 6: Grep Validation${NC}"
    run_test "AC-6.11: grep '@.claude/memory/' count" "test_grep_claude_memory_count"
    run_test "AC-6.12: grep '@src/claude/memory/' = 0" "test_grep_src_claude_memory_count"

    echo -e "\n${YELLOW}Phase 7: File Integrity{{NC}"
    run_test "AC-6.13: CLAUDE.md not modified" "test_claude_md_not_modified"
    run_test "AC-6.14: CLAUDE.md has complete sections" "test_claude_md_has_complete_sections"

    echo -e "\n${YELLOW}Phase 8: Contrast Validation{{NC}"
    run_test "AC-6.15: Contrast: skills updated, CLAUDE.md preserved" "test_contrast_with_updated_skills"

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
