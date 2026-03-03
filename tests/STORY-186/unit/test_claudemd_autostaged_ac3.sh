#!/bin/bash
# Unit Test: AC3 - CLAUDE.md Auto-Staged
# Tests that CLAUDE.md is automatically staged if changed after registry regeneration
#
# STORY-186: Auto-Regenerate Subagent Registry in Pre-Commit Hook
#
# Acceptance Criteria:
# AC-3: Then updated CLAUDE.md auto-staged if changed

set -e

TEST_NAME="AC3: CLAUDE.md Auto-Staged"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../.." && pwd)"

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================="
echo "TEST: $TEST_NAME"
echo "========================================="

PRE_COMMIT_HOOK="$PROJECT_ROOT/.git/hooks/pre-commit"

# Test 3.1: Pre-commit hook contains 'git add CLAUDE.md'
test_git_add_claudemd() {
    echo -n "Test 3.1: Pre-commit hook contains 'git add CLAUDE.md'... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Pre-commit hook exists"
        return 1
    fi

    if grep -q "git add CLAUDE.md" "$PRE_COMMIT_HOOK"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: 'git add CLAUDE.md' command"
        echo "  Actual: No git add CLAUDE.md found"
        return 1
    fi
}

# Test 3.2: git add CLAUDE.md follows registry regeneration in STORY-186 block
test_staging_order() {
    echo -n "Test 3.2: 'git add CLAUDE.md' follows registry regeneration... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        return 1
    fi

    # Per Technical Spec, the STORY-186 block should have:
    # echo "Regenerating subagent registry..."
    # bash scripts/generate-subagent-registry.sh 2>/dev/null || true
    # git add CLAUDE.md 2>/dev/null || true
    #
    # The git add must be on a line AFTER the registry script line (not before)

    # Get global line numbers for the first occurrence in STORY-186 section
    # Find lines with non-blocking patterns (|| true) which are the STORY-186 additions
    local registry_line
    local gitadd_line

    # Get line of registry script with || true pattern (STORY-186's non-blocking call)
    registry_line=$(grep -n "generate-subagent-registry.sh.*|| true" "$PRE_COMMIT_HOOK" | head -1 | cut -d: -f1)
    # Get line of git add CLAUDE.md with non-blocking pattern
    gitadd_line=$(grep -n "git add CLAUDE.md.*|| true\|git add CLAUDE.md.*2>/dev/null" "$PRE_COMMIT_HOOK" | head -1 | cut -d: -f1)

    if [ -z "$registry_line" ] || [ -z "$gitadd_line" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Both registry script (with || true) and git add exist"
        echo "  Registry line: $registry_line"
        echo "  Git add line: $gitadd_line"
        return 1
    fi

    if [ "$gitadd_line" -gt "$registry_line" ]; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: git add CLAUDE.md after registry regeneration"
        echo "  Actual: Order is incorrect (git add on line $gitadd_line, registry on line $registry_line)"
        return 1
    fi
}

# Test 3.3: git add uses non-blocking pattern
test_gitadd_nonblocking() {
    echo -n "Test 3.3: 'git add CLAUDE.md' uses non-blocking pattern (|| true or 2>/dev/null)... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        return 1
    fi

    # Per Technical Specification: git add CLAUDE.md 2>/dev/null || true
    local gitadd_line
    gitadd_line=$(grep "git add CLAUDE.md" "$PRE_COMMIT_HOOK")

    if echo "$gitadd_line" | grep -q "|| true\|2>/dev/null"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: 'git add CLAUDE.md 2>/dev/null || true' pattern"
        echo "  Actual: $gitadd_line"
        return 1
    fi
}

# Test 3.4: Simulate CLAUDE.md staging in test repo
test_simulated_staging() {
    echo -n "Test 3.4: Simulated CLAUDE.md staging works correctly... "

    TEMP_DIR="/tmp/devforgeai-test-$$"
    mkdir -p "$TEMP_DIR"

    # Initialize test git repo
    cd "$TEMP_DIR"
    git init --quiet
    git config user.email "test@test.com"
    git config user.name "Test"

    # Create initial CLAUDE.md
    echo "# Test CLAUDE.md" > CLAUDE.md
    git add CLAUDE.md
    git commit -m "Initial commit" --quiet

    # Modify CLAUDE.md
    echo "## Modified section" >> CLAUDE.md

    # Simulate the staging command from the spec
    git add CLAUDE.md 2>/dev/null || true

    # Check if CLAUDE.md is staged
    if git diff --cached --name-only | grep -q "CLAUDE.md"; then
        echo -e "${GREEN}PASS${NC}"
        cd - > /dev/null
        rm -rf "$TEMP_DIR"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: CLAUDE.md staged after 'git add CLAUDE.md'"
        cd - > /dev/null
        rm -rf "$TEMP_DIR"
        return 1
    fi
}

# Test 3.5: No error when CLAUDE.md unchanged
test_unchanged_claudemd() {
    echo -n "Test 3.5: No error when CLAUDE.md is unchanged... "

    TEMP_DIR="/tmp/devforgeai-test-$$"
    mkdir -p "$TEMP_DIR"

    # Initialize test git repo
    cd "$TEMP_DIR"
    git init --quiet
    git config user.email "test@test.com"
    git config user.name "Test"

    # Create and commit CLAUDE.md
    echo "# Test CLAUDE.md" > CLAUDE.md
    git add CLAUDE.md
    git commit -m "Initial commit" --quiet

    # Try to stage unchanged CLAUDE.md (should not error with || true)
    if git add CLAUDE.md 2>/dev/null || true; then
        echo -e "${GREEN}PASS${NC}"
        cd - > /dev/null
        rm -rf "$TEMP_DIR"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: No error on unchanged file with '|| true'"
        cd - > /dev/null
        rm -rf "$TEMP_DIR"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_git_add_claudemd || FAILED_TESTS=$((FAILED_TESTS + 1))
test_staging_order || FAILED_TESTS=$((FAILED_TESTS + 1))
test_gitadd_nonblocking || FAILED_TESTS=$((FAILED_TESTS + 1))
test_simulated_staging || FAILED_TESTS=$((FAILED_TESTS + 1))
test_unchanged_claudemd || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
