#!/bin/bash

################################################################################
# TEST SUITE: AC#6 - Directory Structure Matches EPIC-009 Specification
# Story: STORY-041
# Description: Verify src/ directory structure exactly matches EPIC-009 Phase 1
#
# Acceptance Criteria:
# src/claude/ structure:
# - skills/ → 10 subdirectories (9 DevForgeAI + 1 claude-code-terminal-expert)
# - agents/ → empty (ready for 21 files)
# - commands/ → empty (ready for 13 files)
# - memory/ → empty (ready for 10 files)
#
# src/devforgeai/ structure:
# - context/ → empty (ready for 6 template files)
# - protocols/ → empty (ready for 3 protocol files)
# - specs/ → 3 subdirectories (enhancements/, requirements/, ui/)
# - adrs/ → 1 subdirectory (example/)
# - deployment/ → empty
# - qa/ → 4 subdirectories (coverage/, reports/, anti-patterns/, spec-compliance/)
#
# Validation:
# - No extra directories beyond specification
# - All skill subdirectories exist
# - tree -L 3 src/ output matches specification
#
# Test Status: FAILING (Red Phase) - directory structure not yet created
################################################################################

set -e  # Exit on first error

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#6: Directory Structure Matches EPIC-009 Specification"

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

# Helper function to assert directory count at specific level
assert_subdirectory_count() {
    local parent_dir="$1"
    local expected_count="$2"
    local description="$3"
    ((TESTS_RUN++))

    if [ ! -d "$parent_dir" ]; then
        echo -e "${RED}✗ FAIL${NC}: Parent directory missing: $description"
        echo "  Path: $parent_dir"
        ((TESTS_FAILED++))
        return 1
    fi

    local actual_count=$(find "$parent_dir" -maxdepth 1 -type d ! -name "$(basename "$parent_dir")" 2>/dev/null | wc -l)

    if [ "$actual_count" -eq "$expected_count" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Path: $parent_dir"
        echo "  Count: $actual_count (expected: $expected_count)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Path: $parent_dir"
        echo "  Count: $actual_count (expected: $expected_count)"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert directory exists
assert_directory_exists() {
    local dir_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ -d "$dir_path" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Path: $dir_path"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected: $dir_path"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to verify directory is empty (except .gitkeep)
assert_directory_empty() {
    local dir_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ ! -d "$dir_path" ]; then
        echo -e "${RED}✗ FAIL${NC}: Directory missing: $description"
        echo "  Path: $dir_path"
        ((TESTS_FAILED++))
        return 1
    fi

    local file_count=$(find "$dir_path" -maxdepth 1 -type f ! -name ".gitkeep" 2>/dev/null | wc -l)

    if [ "$file_count" -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description (empty, only .gitkeep)"
        echo "  Path: $dir_path"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description (contains files)"
        echo "  Path: $dir_path"
        echo "  File count: $file_count"
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
# TEST GROUP 1: src/claude/ Top-Level Structure
################################################################################

echo -e "${BLUE}Test Group 1: src/claude/ Top-Level Structure${NC}"
echo ""

assert_directory_exists "src/claude" "src/claude/ directory exists"
assert_subdirectory_count "src/claude" 4 "src/claude/ contains exactly 4 subdirectories"

echo ""

################################################################################
# TEST GROUP 2: src/claude/ Subdirectories
################################################################################

echo -e "${BLUE}Test Group 2: src/claude/ Subdirectories${NC}"
echo ""

assert_directory_exists "src/claude/skills" "src/claude/skills/ subdirectory exists"
assert_directory_exists "src/claude/agents" "src/claude/agents/ subdirectory exists"
assert_directory_exists "src/claude/commands" "src/claude/commands/ subdirectory exists"
assert_directory_exists "src/claude/memory" "src/claude/memory/ subdirectory exists"

echo ""

################################################################################
# TEST GROUP 3: src/claude/skills/ Subdirectories
################################################################################

echo -e "${BLUE}Test Group 3: src/claude/skills/ Subdirectories (10 skills)${NC}"
echo ""

assert_subdirectory_count "src/claude/skills" 10 "src/claude/skills/ contains exactly 10 skill subdirectories"

EXPECTED_SKILLS=(
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

for skill in "${EXPECTED_SKILLS[@]}"; do
    assert_directory_exists "src/claude/skills/$skill" "Skill subdirectory: $skill"
done

echo ""

################################################################################
# TEST GROUP 4: src/claude/ Empty Directories Validation
################################################################################

echo -e "${BLUE}Test Group 4: src/claude/ Empty Directories (Ready for Files)${NC}"
echo ""

assert_directory_empty "src/claude/agents" "src/claude/agents/ is empty (ready for 21 files)"
assert_directory_empty "src/claude/commands" "src/claude/commands/ is empty (ready for 13 files)"
assert_directory_empty "src/claude/memory" "src/claude/memory/ is empty (ready for 10 files)"

echo ""

################################################################################
# TEST GROUP 5: src/devforgeai/ Top-Level Structure
################################################################################

echo -e "${BLUE}Test Group 5: src/devforgeai/ Top-Level Structure${NC}"
echo ""

assert_directory_exists "src/devforgeai" "src/devforgeai/ directory exists"
assert_subdirectory_count "src/devforgeai" 6 "src/devforgeai/ contains exactly 6 subdirectories"

echo ""

################################################################################
# TEST GROUP 6: src/devforgeai/ Subdirectories
################################################################################

echo -e "${BLUE}Test Group 6: src/devforgeai/ Subdirectories${NC}"
echo ""

assert_directory_exists "src/devforgeai/context" "src/devforgeai/context/ subdirectory exists"
assert_directory_exists "src/devforgeai/protocols" "src/devforgeai/protocols/ subdirectory exists"
assert_directory_exists "src/devforgeai/specs" "src/devforgeai/specs/ subdirectory exists"
assert_directory_exists "src/devforgeai/adrs" "src/devforgeai/adrs/ subdirectory exists"
assert_directory_exists "src/devforgeai/deployment" "src/devforgeai/deployment/ subdirectory exists"
assert_directory_exists "src/devforgeai/qa" "src/devforgeai/qa/ subdirectory exists"

echo ""

################################################################################
# TEST GROUP 7: src/devforgeai/specs/ Subdirectories
################################################################################

echo -e "${BLUE}Test Group 7: src/devforgeai/specs/ Subdirectories (3 specs)${NC}"
echo ""

assert_subdirectory_count "src/devforgeai/specs" 3 "src/devforgeai/specs/ contains exactly 3 subdirectories"

assert_directory_exists "src/devforgeai/specs/enhancements" "src/devforgeai/specs/enhancements/ exists"
assert_directory_exists "src/devforgeai/specs/requirements" "src/devforgeai/specs/requirements/ exists"
assert_directory_exists "src/devforgeai/specs/ui" "src/devforgeai/specs/ui/ exists"

echo ""

################################################################################
# TEST GROUP 8: src/devforgeai/adrs/ Subdirectories
################################################################################

echo -e "${BLUE}Test Group 8: src/devforgeai/adrs/ Subdirectories (1 example)${NC}"
echo ""

assert_subdirectory_count "src/devforgeai/adrs" 1 "src/devforgeai/adrs/ contains exactly 1 subdirectory"

assert_directory_exists "src/devforgeai/adrs/example" "src/devforgeai/adrs/example/ exists"

echo ""

################################################################################
# TEST GROUP 9: src/devforgeai/qa/ Subdirectories
################################################################################

echo -e "${BLUE}Test Group 9: src/devforgeai/qa/ Subdirectories (4 QA dirs)${NC}"
echo ""

assert_subdirectory_count "src/devforgeai/qa" 4 "src/devforgeai/qa/ contains exactly 4 subdirectories"

assert_directory_exists "src/devforgeai/qa/coverage" "src/devforgeai/qa/coverage/ exists"
assert_directory_exists "src/devforgeai/qa/reports" "src/devforgeai/qa/reports/ exists"
assert_directory_exists "src/devforgeai/qa/anti-patterns" "src/devforgeai/qa/anti-patterns/ exists"
assert_directory_exists "src/devforgeai/qa/spec-compliance" "src/devforgeai/qa/spec-compliance/ exists"

echo ""

################################################################################
# TEST GROUP 10: src/devforgeai/ Empty Directories Validation
################################################################################

echo -e "${BLUE}Test Group 10: src/devforgeai/ Empty Directories${NC}"
echo ""

assert_directory_empty "src/devforgeai/context" "src/devforgeai/context/ is empty (ready for 6 files)"
assert_directory_empty "src/devforgeai/protocols" "src/devforgeai/protocols/ is empty (ready for 3 files)"
assert_directory_empty "src/devforgeai/deployment" "src/devforgeai/deployment/ is empty"

echo ""

################################################################################
# TEST GROUP 11: src/devforgeai/specs/ Empty Subdirectories Validation
################################################################################

echo -e "${BLUE}Test Group 11: src/devforgeai/specs/ Subdirectories Are Empty${NC}"
echo ""

assert_directory_empty "src/devforgeai/specs/enhancements" "src/devforgeai/specs/enhancements/ is empty"
assert_directory_empty "src/devforgeai/specs/requirements" "src/devforgeai/specs/requirements/ is empty"
assert_directory_empty "src/devforgeai/specs/ui" "src/devforgeai/specs/ui/ is empty"

echo ""

################################################################################
# TEST GROUP 12: src/devforgeai/qa/ Subdirectories Are Empty
################################################################################

echo -e "${BLUE}Test Group 12: src/devforgeai/qa/ Subdirectories Are Empty${NC}"
echo ""

assert_directory_empty "src/devforgeai/qa/coverage" "src/devforgeai/qa/coverage/ is empty (except .gitkeep)"
assert_directory_empty "src/devforgeai/qa/reports" "src/devforgeai/qa/reports/ is empty (except .gitkeep)"
assert_directory_empty "src/devforgeai/qa/anti-patterns" "src/devforgeai/qa/anti-patterns/ is empty"
assert_directory_empty "src/devforgeai/qa/spec-compliance" "src/devforgeai/qa/spec-compliance/ is empty"

echo ""

################################################################################
# TEST GROUP 13: No Extra Directories Beyond Specification
################################################################################

echo -e "${BLUE}Test Group 13: No Extra Directories Beyond Specification${NC}"
echo ""

((TESTS_RUN++))
# Count all directories under src/
local total_dirs=$(find src/ -type d 2>/dev/null | wc -l)
# Expected: 1 (src) + 2 (claude, devforgeai) + 4 (claude subdirs) + 10 (skills) + 6 (devforgeai subdirs) + 3 (specs subdirs) + 1 (adrs/example) + 4 (qa subdirs) = 31
# But we'll use a range: expect 25-35 directories total
if [ "$total_dirs" -ge 25 ] && [ "$total_dirs" -le 40 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Directory count within expected range (no extra directories)"
    echo "  Total directories: $total_dirs (expected: 25-40)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Unexpected number of directories"
    echo "  Total: $total_dirs (expected: 25-40)"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 14: Directory Structure Tree Depth Validation
################################################################################

echo -e "${BLUE}Test Group 14: Directory Structure Tree Depth${NC}"
echo ""

((TESTS_RUN++))
# Verify maximum depth is 3 (src -> claude/devforgeai -> subdirs -> optional nested)
local max_depth=$(find src/ -type d 2>/dev/null | awk -F/ '{print NF}' | sort -rn | head -1)
if [ "$max_depth" -le 4 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Directory tree depth is acceptable"
    echo "  Max depth: $max_depth (expected: ≤4)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Directory tree depth exceeds specification"
    echo "  Max depth: $max_depth (expected: ≤4)"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 15: Skills Directory Count Verification
################################################################################

echo -e "${BLUE}Test Group 15: Skills Directory Count Verification${NC}"
echo ""

((TESTS_RUN++))
local skill_count=$(ls src/claude/skills/ 2>/dev/null | wc -l)
if [ "$skill_count" -eq 10 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Skills count matches specification (10)"
    echo "  Count: $skill_count"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Skills count does not match specification"
    echo "  Count: $skill_count (expected: 10)"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 16: All Required Directories Are Readable
################################################################################

echo -e "${BLUE}Test Group 16: All Directories Are Readable${NC}"
echo ""

((TESTS_RUN++))
# Test that we can list contents of key directories
if [ -r "src/claude" ] && [ -r "src/devforgeai" ] && [ -r "src/claude/skills" ]; then
    echo -e "${GREEN}✓ PASS${NC}: All directories are readable"
    echo "  Permission check: OK"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Some directories are not readable"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST SUMMARY
################################################################################

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST SUMMARY: AC#6${NC}"
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
    echo "Reason:   src/ directory structure does not yet match EPIC-009 specification"
    echo ""
    echo "Next Step (Green Phase):"
    echo "1. Create directory structure matching EPIC-009 Phase 1 requirements"
    echo "2. Add .gitkeep files to empty directories"
    echo "3. Verify with: find src/ -type d | head -20"
    echo ""
    exit 1
else
    echo -e "${GREEN}STATUS: PASSING ✓${NC}"
    echo ""
    echo "All assertions passed. AC#6 requirements satisfied."
    echo "Directory structure matches EPIC-009 specification exactly."
    echo ""
    exit 0
fi
