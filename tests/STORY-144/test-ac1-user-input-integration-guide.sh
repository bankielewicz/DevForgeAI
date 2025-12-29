#!/bin/bash
#
# Test: AC#1 - user-input-integration-guide.md reviewed and resolved
#
# Tests that user-input-integration-guide.md is either:
# 1. Integrated into user-input-guidance.md Section 5, OR
# 2. Deleted with documented reason in commit message, OR
# 3. Time-boxed decision made (default: delete)
#
# These tests will FAIL initially (file still exists as orphan)
#

set -e

# Test colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
ORPHANED_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-ideation/references/user-input-integration-guide.md"
TARGET_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-ideation/references/user-input-guidance.md"

# Track test results
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to run a test
run_test() {
    local test_name=$1
    local test_command=$2
    local should_fail=$3  # "true" if test should fail initially

    TESTS_RUN=$((TESTS_RUN + 1))

    echo -e "\n${YELLOW}[TEST $TESTS_RUN]${NC} $test_name"

    if eval "$test_command" 2>/dev/null; then
        if [ "$should_fail" == "true" ]; then
            echo -e "${RED}✗ FAILED${NC} (Expected to fail in Red phase)"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        else
            echo -e "${GREEN}✓ PASSED${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        fi
    else
        if [ "$should_fail" == "true" ]; then
            echo -e "${GREEN}✓ PASSED${NC} (Expected failure in Red phase)"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}✗ FAILED${NC}"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    fi
}

echo "========================================"
echo "AC#1: user-input-integration-guide.md"
echo "========================================"
echo "Testing file resolution: Delete OR Integrate"

# Test 1: File must not exist as orphaned reference (after resolution)
# This test FAILS initially because file exists
run_test \
    "test-ac1-file-deleted-or-integrated" \
    "[ ! -f '$ORPHANED_FILE' ]" \
    "true"

# Test 2: If file was deleted, orphaned filename should not appear in SKILL.md
# This test FAILS initially because file is referenced
run_test \
    "test-ac1-file-not-referenced-in-skill" \
    "! grep -q 'user-input-integration-guide' '$PROJECT_ROOT/.claude/skills/devforgeai-ideation/SKILL.md'" \
    "true"

# Test 3: If file was integrated into user-input-guidance.md, content should exist there
# This test FAILS initially because content not integrated yet
run_test \
    "test-ac1-content-preserved-in-target" \
    "[ -f '$TARGET_FILE' ] && grep -q 'Step 0 Implementation' '$TARGET_FILE'" \
    "true"

# Test 4: Verify user-input-guidance.md exists (target file)
# This test PASSES because target file should exist
run_test \
    "test-ac1-target-file-exists" \
    "[ -f '$TARGET_FILE' ]" \
    "false"

# Test 5: If integrated, verify content sections are preserved
# This test FAILS initially - content not integrated
run_test \
    "test-ac1-integration-preserves-load-mechanism" \
    "grep -q 'Load Mechanism' '$TARGET_FILE' && grep -q 'Error Handling' '$TARGET_FILE'" \
    "true"

# Test 6: Verify file is in expected location (prerequisite)
# This test PASSES to verify file exists before resolution
run_test \
    "test-ac1-orphaned-file-path-exists-initially" \
    "[ -f '$ORPHANED_FILE' ]" \
    "false"

# Test 7: Verify no dangling references after deletion
# This test FAILS initially - file still referenced
run_test \
    "test-ac1-no-dangling-references" \
    "! find '$PROJECT_ROOT/.claude/skills/devforgeai-ideation' -name '*.md' -exec grep -l 'user-input-integration-guide' {} \;" \
    "true"

# Test 8: Content sections should be intact in target if integrated
# Verify key section headers are preserved
run_test \
    "test-ac1-section-headers-preserved" \
    "if [ -f '$TARGET_FILE' ]; then
        grep -q 'Section 5' '$TARGET_FILE' || grep -q 'Integration Guide' '$TARGET_FILE'
    else
        false
    fi" \
    "true"

echo ""
echo "========================================"
echo "Summary: AC#1 Tests"
echo "========================================"
echo -e "Tests Run:    $TESTS_RUN"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo "========================================"

# Exit with failure count
exit $TESTS_FAILED
