#!/bin/bash
#
# Test: AC#4 - Commit message documents justification
#
# Tests that the commit message for orphaned file cleanup includes:
# 1. List of files affected
# 2. Action taken (integrated/deleted)
# 3. Justification for each file
#
# This test FAILS initially (no commit message yet)
#

set -e

# Test colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

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
echo "AC#4: Commit Message Documentation"
echo "========================================"
echo "Testing commit message format and content"
echo ""

# Get the latest commit message
LATEST_COMMIT_MSG=$(cd "$PROJECT_ROOT" && git log -1 --pretty=%B 2>/dev/null || echo "")

echo -e "${BLUE}Latest commit message:${NC}"
echo "$LATEST_COMMIT_MSG"
echo ""

# Test 1: Verify git repository is available
run_test \
    "test-ac4-git-repository-exists" \
    "cd '$PROJECT_ROOT' && git rev-parse --git-dir >/dev/null 2>&1" \
    "false"

# Test 2: Verify there are commits in the repository
run_test \
    "test-ac4-commits-exist" \
    "cd '$PROJECT_ROOT' && git log --oneline 2>/dev/null | head -1" \
    "false"

# Test 3: Commit message must mention the story (STORY-144)
# This test FAILS initially (commit doesn't exist yet)
run_test \
    "test-ac4-commit-mentions-story-id" \
    "cd '$PROJECT_ROOT' && git log --all --oneline | grep -q 'STORY-144'" \
    "true"

# Test 4: Commit message should mention 'orphaned' or 'resolve'
run_test \
    "test-ac4-commit-mentions-resolution-action" \
    "echo '$LATEST_COMMIT_MSG' | grep -q -i 'orphan\|resolve\|remove\|integrate'" \
    "true"

# Test 5: Commit message should mention at least one affected file
# Look for file mentions in format: user-input-integration-guide or brainstorm-data-mapping
run_test \
    "test-ac4-commit-lists-affected-files" \
    "echo '$LATEST_COMMIT_MSG' | grep -q -E 'user-input-integration-guide|brainstorm-data-mapping'" \
    "true"

# Test 6: Commit message should include action taken (INTEGRATED or DELETED)
run_test \
    "test-ac4-commit-documents-action" \
    "echo '$LATEST_COMMIT_MSG' | grep -q -i 'integrated\|deleted\|removed'" \
    "true"

# Test 7: Commit message should include justification
# Look for phrases indicating reasoning
run_test \
    "test-ac4-commit-includes-justification" \
    "echo '$LATEST_COMMIT_MSG' | grep -q -i 'reason\|justif\|because\|redundant\|valuable'" \
    "true"

# Test 8: Commit message format should follow conventional commits
# Pattern: type(scope): subject
run_test \
    "test-ac4-conventional-commit-format" \
    "cd '$PROJECT_ROOT' && git log -1 --pretty=%B | grep -E '^[a-z]+(\([^)]*\))?:' >/dev/null" \
    "true"

# Test 9: Verify commit was related to ideation skill changes
run_test \
    "test-ac4-commit-affects-ideation-skill" \
    "cd '$PROJECT_ROOT' && git log -1 --name-only | grep -q 'ideation'" \
    "true"

# Test 10: Both files should be mentioned if both were resolved
run_test \
    "test-ac4-both-files-documented" \
    "echo '$LATEST_COMMIT_MSG' | grep -q 'user-input-integration-guide' && echo '$LATEST_COMMIT_MSG' | grep -q 'brainstorm-data-mapping'" \
    "true"

# Test 11: Commit message should not be empty or single line without detail
run_test \
    "test-ac4-commit-has-sufficient-detail" \
    "[ \$(echo '$LATEST_COMMIT_MSG' | wc -l) -gt 2 ]" \
    "true"

# Test 12: Check commit scope matches story context (ideation)
run_test \
    "test-ac4-commit-scope-ideation" \
    "cd '$PROJECT_ROOT' && git log -1 --pretty=%B | grep -q -i 'ideation'" \
    "true"

echo ""
echo "========================================"
echo "Expected Commit Format"
echo "========================================"
echo "chore(ideation): resolve orphaned reference files"
echo ""
echo "- user-input-integration-guide.md: [INTEGRATED/DELETED] - [reason]"
echo "- brainstorm-data-mapping.md: [INTEGRATED/DELETED] - [reason]"
echo ""

echo "========================================"
echo "Summary: AC#4 Tests"
echo "========================================"
echo -e "Tests Run:    $TESTS_RUN"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo "========================================"

# Exit with failure count
exit $TESTS_FAILED
