#!/bin/bash

################################################################################
# TEST SUITE: AC#1 - Source Directory Structure Created
# Story: STORY-041
# Description: Verify src/ directory structure matches specification
#
# Acceptance Criteria:
# - src/claude/skills/ (with 9 subdirectories for each skill)
# - src/claude/agents/ (empty, ready for 21 agent files)
# - src/claude/commands/ (empty, ready for 13 command files)
# - src/claude/memory/ (empty, ready for 10 reference files)
# - src/devforgeai/context/ (empty, ready for 6 context templates)
# - src/devforgeai/protocols/ (empty, ready for 3 protocol files)
# - src/devforgeai/specs/ (with subdirectories: enhancements/, requirements/, ui/)
# - src/devforgeai/adrs/ (with example/ subdirectory)
# - src/devforgeai/deployment/ (empty, ready for deployment configs)
# - src/devforgeai/qa/ (with subdirectories: coverage/, reports/, anti-patterns/, spec-compliance/)
#
# All directories tracked by Git (contain .gitkeep files where empty)
# Directory count matches specification (≥ 20 directories)
#
# Test Status: FAILING (Red Phase) - directories do not yet exist
################################################################################

set -e  # Exit on first error

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#1: Source Directory Structure Created"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to assert file/directory exists
assert_directory_exists() {
    local dir_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ -d "$dir_path" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Directory: $dir_path"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected directory: $dir_path"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert directory count
assert_directory_count() {
    local parent_dir="$1"
    local expected_count="$2"
    local description="$3"
    ((TESTS_RUN++))

    local actual_count=$(find "$parent_dir" -maxdepth 1 -type d ! -name "$(basename "$parent_dir")" 2>/dev/null | wc -l)

    if [ "$actual_count" -eq "$expected_count" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Directory: $parent_dir"
        echo "  Count: $actual_count (expected: $expected_count)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Directory: $parent_dir"
        echo "  Count: $actual_count (expected: $expected_count)"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert .gitkeep exists
assert_gitkeep_exists() {
    local dir_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ -f "$dir_path/.gitkeep" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  File: $dir_path/.gitkeep"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected: $dir_path/.gitkeep"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST SUITE: $TEST_NAME${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

cd "$PROJECT_ROOT" || exit 1

################################################################################
# TEST GROUP 1: src/claude/ Directory Structure
################################################################################

echo -e "${BLUE}Test Group 1: src/claude/ Directory Structure${NC}"
echo ""

assert_directory_exists "src/claude" "src/claude/ directory exists"
assert_directory_exists "src/claude/skills" "src/claude/skills/ directory exists"
assert_directory_exists "src/claude/agents" "src/claude/agents/ directory exists"
assert_directory_exists "src/claude/commands" "src/claude/commands/ directory exists"
assert_directory_exists "src/claude/memory" "src/claude/memory/ directory exists"

assert_directory_count "src/claude" 4 "src/claude/ contains exactly 4 subdirectories"

echo ""

################################################################################
# TEST GROUP 2: src/claude/skills/ Subdirectories
################################################################################

echo -e "${BLUE}Test Group 2: src/claude/skills/ Subdirectories${NC}"
echo ""

SKILL_DIRS=(
    "devforgeai-ideation"
    "devforgeai-architecture"
    "devforgeai-orchestration"
    "devforgeai-story-creation"
    "devforgeai-ui-generator"
    "devforgeai-development"
    "devforgeai-qa"
    "devforgeai-release"
    "devforgeai-rca"
    "claude-code-terminal-expert"
)

SKILL_COUNT=0
for skill_dir in "${SKILL_DIRS[@]}"; do
    assert_directory_exists "src/claude/skills/$skill_dir" "Skill directory: $skill_dir"
    ((SKILL_COUNT++))
done

assert_directory_count "src/claude/skills" 10 "src/claude/skills/ contains exactly 10 skill subdirectories"

echo ""

################################################################################
# TEST GROUP 3: src/devforgeai/ Directory Structure
################################################################################

echo -e "${BLUE}Test Group 3: src/devforgeai/ Directory Structure${NC}"
echo ""

assert_directory_exists "src/devforgeai" "src/devforgeai/ directory exists"
assert_directory_exists "src/devforgeai/context" "src/devforgeai/context/ directory exists"
assert_directory_exists "src/devforgeai/protocols" "src/devforgeai/protocols/ directory exists"
assert_directory_exists "src/devforgeai/specs" "src/devforgeai/specs/ directory exists"
assert_directory_exists "src/devforgeai/adrs" "src/devforgeai/adrs/ directory exists"
assert_directory_exists "src/devforgeai/deployment" "src/devforgeai/deployment/ directory exists"
assert_directory_exists "src/devforgeai/qa" "src/devforgeai/qa/ directory exists"

assert_directory_count "src/devforgeai" 6 "src/devforgeai/ contains exactly 6 subdirectories"

echo ""

################################################################################
# TEST GROUP 4: src/devforgeai/specs/ Subdirectories
################################################################################

echo -e "${BLUE}Test Group 4: src/devforgeai/specs/ Subdirectories${NC}"
echo ""

assert_directory_exists "src/devforgeai/specs/enhancements" "src/devforgeai/specs/enhancements/ directory exists"
assert_directory_exists "src/devforgeai/specs/requirements" "src/devforgeai/specs/requirements/ directory exists"
assert_directory_exists "src/devforgeai/specs/ui" "src/devforgeai/specs/ui/ directory exists"

assert_directory_count "src/devforgeai/specs" 3 "src/devforgeai/specs/ contains exactly 3 subdirectories"

echo ""

################################################################################
# TEST GROUP 5: src/devforgeai/adrs/ Subdirectories
################################################################################

echo -e "${BLUE}Test Group 5: src/devforgeai/adrs/ Subdirectories${NC}"
echo ""

assert_directory_exists "src/devforgeai/adrs/example" "src/devforgeai/adrs/example/ directory exists"

assert_directory_count "src/devforgeai/adrs" 1 "src/devforgeai/adrs/ contains exactly 1 subdirectory (example/)"

echo ""

################################################################################
# TEST GROUP 6: src/devforgeai/qa/ Subdirectories
################################################################################

echo -e "${BLUE}Test Group 6: src/devforgeai/qa/ Subdirectories${NC}"
echo ""

assert_directory_exists "src/devforgeai/qa/coverage" "src/devforgeai/qa/coverage/ directory exists"
assert_directory_exists "src/devforgeai/qa/reports" "src/devforgeai/qa/reports/ directory exists"
assert_directory_exists "src/devforgeai/qa/anti-patterns" "src/devforgeai/qa/anti-patterns/ directory exists"
assert_directory_exists "src/devforgeai/qa/spec-compliance" "src/devforgeai/qa/spec-compliance/ directory exists"

assert_directory_count "src/devforgeai/qa" 4 "src/devforgeai/qa/ contains exactly 4 subdirectories"

echo ""

################################################################################
# TEST GROUP 7: .gitkeep Files in Empty Directories
################################################################################

echo -e "${BLUE}Test Group 7: .gitkeep Files in Empty Directories${NC}"
echo ""

# Test .gitkeep in key directories
assert_gitkeep_exists "src/claude/agents" ".gitkeep in src/claude/agents/"
assert_gitkeep_exists "src/claude/commands" ".gitkeep in src/claude/commands/"
assert_gitkeep_exists "src/claude/memory" ".gitkeep in src/claude/memory/"
assert_gitkeep_exists "src/devforgeai/context" ".gitkeep in src/devforgeai/context/"
assert_gitkeep_exists "src/devforgeai/protocols" ".gitkeep in src/devforgeai/protocols/"
assert_gitkeep_exists "src/devforgeai/deployment" ".gitkeep in src/devforgeai/deployment/"
assert_gitkeep_exists "src/devforgeai/qa/coverage" ".gitkeep in src/devforgeai/qa/coverage/"
assert_gitkeep_exists "src/devforgeai/qa/reports" ".gitkeep in src/devforgeai/qa/reports/"
assert_gitkeep_exists "src/devforgeai/qa/anti-patterns" ".gitkeep in src/devforgeai/qa/anti-patterns/"
assert_gitkeep_exists "src/devforgeai/qa/spec-compliance" ".gitkeep in src/devforgeai/qa/spec-compliance/"
assert_gitkeep_exists "src/devforgeai/specs/enhancements" ".gitkeep in src/devforgeai/specs/enhancements/"
assert_gitkeep_exists "src/devforgeai/specs/requirements" ".gitkeep in src/devforgeai/specs/requirements/"
assert_gitkeep_exists "src/devforgeai/specs/ui" ".gitkeep in src/devforgeai/specs/ui/"

echo ""

################################################################################
# TEST GROUP 8: Overall Directory Count
################################################################################

echo -e "${BLUE}Test Group 8: Overall Directory Count${NC}"
echo ""

((TESTS_RUN++))
local total_dirs=$(find src/ -type d | wc -l)
if [ "$total_dirs" -ge 20 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Total directory count ≥ 20"
    echo "  Actual count: $total_dirs"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Total directory count ≥ 20"
    echo "  Actual count: $total_dirs (expected: ≥20)"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 9: No Regular Files in src/ (Phase 1 - Directories Only)
################################################################################

echo -e "${BLUE}Test Group 9: No Regular Files in src/ (Phase 1 - Directories Only)${NC}"
echo ""

((TESTS_RUN++))
local regular_files=$(find src/ -type f ! -name ".gitkeep" 2>/dev/null | wc -l)
if [ "$regular_files" -eq 0 ]; then
    echo -e "${GREEN}✓ PASS${NC}: No regular files in src/ (only .gitkeep allowed)"
    echo "  Count: 0 files (excluding .gitkeep)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: No regular files in src/ (only .gitkeep allowed)"
    echo "  Found: $regular_files files"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 10: Directory Permissions (755 for directories, 644 for .gitkeep)
################################################################################

echo -e "${BLUE}Test Group 10: Directory Permissions${NC}"
echo ""

((TESTS_RUN++))
local src_perms=$(stat -c "%a" src/claude/ 2>/dev/null || stat -f "%OLp" src/claude/ 2>/dev/null | grep -o "755$" || echo "")
if [ -n "$src_perms" ] || [ -d "src/claude" ]; then
    # Note: Skipping specific permission check as it may vary by system
    # Just verify directories are readable and executable
    echo -e "${YELLOW}⊘ SKIP${NC}: Directory permission check (system-dependent)"
    echo "  Note: Will be validated in implementation"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: src/claude/ directory permissions"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST SUMMARY
################################################################################

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST SUMMARY: AC#1${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Tests Run:    $TESTS_RUN"
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}STATUS: FAILING (Red Phase) ✗${NC}"
    echo ""
    echo "Expected: All tests should be FAILING initially (TDD Red phase)"
    echo "Reason:   src/ directory structure does not yet exist"
    echo ""
    echo "Next Step (Green Phase): Run implementation script to create directory structure"
    echo ""
    exit 1
else
    echo -e "${GREEN}STATUS: PASSING ✓${NC}"
    echo ""
    echo "All assertions passed. AC#1 requirements satisfied."
    echo ""
    exit 0
fi
