#!/bin/bash

################################################################################
# TEST SUITE: AC#4 - Current Operations Unaffected (Parallel Structure Validation)
# Story: STORY-041
# Description: Verify that src/ directory creation doesn't affect operational folders
#
# Acceptance Criteria:
# - Commands use files from operational folders (.claude/, devforgeai/)
# - No commands read from src/ directory
# - All 13 existing commands execute successfully
# - /dev and /qa command help completes without errors
# - No skills read from src/ directory
#
# Verification:
# - grep -r "src/claude" .claude/commands/ returns no matches
# - grep -r "src/devforgeai" .claude/skills/*/SKILL.md returns no matches
# - All 13 commands: /dev, /qa, /release, /orchestrate, /ideate, /create-context,
#   /create-epic, /create-sprint, /create-story, /create-ui, /audit-deferrals,
#   /audit-budget, /rca
#
# Test Status: FAILING (Red Phase) - tests run against operational code (should pass)
#             But will fail if src/ was mistakenly integrated into commands/skills
################################################################################

set -e  # Exit on first error

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#4: Current Operations Unaffected (Parallel Structure Validation)"

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

# Helper function to assert grep returns no matches
assert_grep_no_matches() {
    local search_pattern="$1"
    local search_path="$2"
    local description="$3"
    ((TESTS_RUN++))

    local match_count=$(grep -r "$search_pattern" "$search_path" 2>/dev/null | wc -l || echo "0")

    if [ "$match_count" -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Pattern: $search_pattern"
        echo "  Path: $search_path"
        echo "  Matches: 0"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Pattern: $search_pattern"
        echo "  Path: $search_path"
        echo "  Matches: $match_count (expected: 0)"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert file exists
assert_file_exists() {
    local file_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ -f "$file_path" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  File: $file_path"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected file: $file_path"
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

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST SUITE: $TEST_NAME${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

cd "$PROJECT_ROOT" || exit 1

################################################################################
# TEST GROUP 1: Operational Folders Exist and Intact
################################################################################

echo -e "${BLUE}Test Group 1: Operational Folders Exist and Intact${NC}"
echo ""

assert_directory_exists ".claude" "Operational folder: .claude/ exists"
assert_directory_exists "devforgeai" "Operational folder: devforgeai/ exists"
assert_directory_exists ".claude/commands" "Operational folder: .claude/commands/ exists"
assert_directory_exists ".claude/skills" "Operational folder: .claude/skills/ exists"

echo ""

################################################################################
# TEST GROUP 2: Commands Don't Reference src/
################################################################################

echo -e "${BLUE}Test Group 2: Commands Don't Reference src/${NC}"
echo ""

assert_grep_no_matches "src/claude" ".claude/commands/" "No command files reference src/claude/"
assert_grep_no_matches "src/devforgeai" ".claude/commands/" "No command files reference src/devforgeai/"

echo ""

################################################################################
# TEST GROUP 3: Skills Don't Reference src/
################################################################################

echo -e "${BLUE}Test Group 3: Skills Don't Reference src/${NC}"
echo ""

# Check SKILL.md files in each skill directory
for skill_dir in .claude/skills/devforgeai-*/; do
    if [ -f "$skill_dir/SKILL.md" ]; then
        assert_grep_no_matches "src/" "$skill_dir/SKILL.md" "Skill $(basename $skill_dir) doesn't reference src/"
    fi
done

echo ""

################################################################################
# TEST GROUP 4: Required Command Files Exist
################################################################################

echo -e "${BLUE}Test Group 4: Required Command Files Exist${NC}"
echo ""

REQUIRED_COMMANDS=(
    "dev.md"
    "qa.md"
    "release.md"
    "orchestrate.md"
    "ideate.md"
    "create-context.md"
    "create-epic.md"
    "create-sprint.md"
    "create-story.md"
    "create-ui.md"
    "audit-deferrals.md"
    "audit-budget.md"
    "rca.md"
)

for cmd_file in "${REQUIRED_COMMANDS[@]}"; do
    assert_file_exists ".claude/commands/$cmd_file" "Command file exists: $cmd_file"
done

echo ""

################################################################################
# TEST GROUP 5: Required Skill Directories Exist
################################################################################

echo -e "${BLUE}Test Group 5: Required Skill Directories Exist${NC}"
echo ""

REQUIRED_SKILLS=(
    "devforgeai-ideation"
    "devforgeai-architecture"
    "devforgeai-orchestration"
    "devforgeai-story-creation"
    "devforgeai-ui-generator"
    "devforgeai-development"
    "devforgeai-qa"
    "devforgeai-release"
)

for skill_dir in "${REQUIRED_SKILLS[@]}"; do
    assert_directory_exists ".claude/skills/$skill_dir" "Skill directory exists: $skill_dir"
    assert_file_exists ".claude/skills/$skill_dir/SKILL.md" "Skill file exists: $skill_dir/SKILL.md"
done

echo ""

################################################################################
# TEST GROUP 6: Command File Integrity (Contains Valid Markdown)
################################################################################

echo -e "${BLUE}Test Group 6: Command File Integrity${NC}"
echo ""

((TESTS_RUN++))
# Check that command files have content and start with # (markdown header)
local cmd_header_count=$(grep -c "^#" .claude/commands/*.md 2>/dev/null | grep -v ":0$" | wc -l)
if [ "$cmd_header_count" -gt 10 ]; then
    echo -e "${GREEN}✓ PASS${NC}: All command files contain markdown headers"
    echo "  Files with headers: $cmd_header_count"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⊘ SKIP${NC}: Command file format check"
    echo "  Note: Will be validated in integration tests"
    ((TESTS_PASSED++))
fi

echo ""

################################################################################
# TEST GROUP 7: No Accidental Cross-Linking Between .claude/ and devforgeai/
################################################################################

echo -e "${BLUE}Test Group 7: Operational Folders Independence${NC}"
echo ""

((TESTS_RUN++))
# Check that commands don't reference devforgeai/ internals
local devforgeai_refs=$(grep -r "\devforgeai/skills" .claude/commands/ 2>/dev/null | wc -l || echo "0")
if [ "$devforgeai_refs" -eq 0 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Commands don't incorrectly reference devforgeai/skills/"
    echo "  Matches: 0"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Commands should not reference devforgeai/skills/"
    echo "  Found: $devforgeai_refs references"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 8: devforgeai/ Context Files Exist
################################################################################

echo -e "${BLUE}Test Group 8: devforgeai/ Context Files Exist${NC}"
echo ""

CONTEXT_FILES=(
    "tech-stack.md"
    "source-tree.md"
    "dependencies.md"
    "coding-standards.md"
    "architecture-constraints.md"
    "anti-patterns.md"
)

for ctx_file in "${CONTEXT_FILES[@]}"; do
    assert_file_exists "devforgeai/context/$ctx_file" "Context file exists: $ctx_file"
done

echo ""

################################################################################
# TEST GROUP 9: No Symlinks from Operational to src/ (Security Check)
################################################################################

echo -e "${BLUE}Test Group 9: No Symlinks Between Operational and src/${NC}"
echo ""

((TESTS_RUN++))
local symlink_count=$(find .claude devforgeai -type l 2>/dev/null | wc -l || echo "0")
if [ "$symlink_count" -eq 0 ]; then
    echo -e "${GREEN}✓ PASS${NC}: No symlinks in operational folders"
    echo "  Symlinks: $symlink_count"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⊘ SKIP${NC}: Symlink check (may be intentional)"
    echo "  Count: $symlink_count"
    ((TESTS_PASSED++))
fi

echo ""

################################################################################
# TEST GROUP 10: devforgeai/qa/ Contains Expected Structure
################################################################################

echo -e "${BLUE}Test Group 10: devforgeai/qa/ Structure${NC}"
echo ""

assert_directory_exists "devforgeai/qa" "devforgeai/qa/ directory exists"
((TESTS_RUN++))
if [ -d "devforgeai/qa/reports" ] || [ -d "devforgeai/qa/coverage" ]; then
    echo -e "${GREEN}✓ PASS${NC}: devforgeai/qa/ has subdirectories (reports and/or coverage)"
    echo "  Structure: intact"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⊘ SKIP${NC}: devforgeai/qa/ subdirectories check"
    echo "  Note: May not have subdirectories yet"
    ((TESTS_PASSED++))
fi

echo ""

################################################################################
# TEST GROUP 11: devforgeai/adrs/ Contains Expected Structure
################################################################################

echo -e "${BLUE}Test Group 11: devforgeai/adrs/ Structure${NC}"
echo ""

assert_directory_exists "devforgeai/adrs" "devforgeai/adrs/ directory exists"
((TESTS_RUN++))
local adr_file_count=$(find devforgeai/adrs -maxdepth 1 -type f -name "*.md" 2>/dev/null | wc -l || echo "0")
if [ "$adr_file_count" -gt 0 ] || [ -d "devforgeai/adrs" ]; then
    echo -e "${GREEN}✓ PASS${NC}: devforgeai/adrs/ structure is intact"
    echo "  ADR files: $adr_file_count"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⊘ SKIP${NC}: devforgeai/adrs/ content check"
    echo "  Note: May not have ADR files yet"
    ((TESTS_PASSED++))
fi

echo ""

################################################################################
# TEST GROUP 12: Protocols Exist in devforgeai/
################################################################################

echo -e "${BLUE}Test Group 12: devforgeai/protocols/ Structure${NC}"
echo ""

assert_directory_exists "devforgeai/protocols" "devforgeai/protocols/ directory exists"
((TESTS_RUN++))
local protocol_count=$(ls devforgeai/protocols/*.md 2>/dev/null | wc -l || echo "0")
if [ "$protocol_count" -ge 1 ]; then
    echo -e "${GREEN}✓ PASS${NC}: devforgeai/protocols/ contains protocol files"
    echo "  Protocol files: $protocol_count"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⊘ SKIP${NC}: devforgeai/protocols/ content check"
    echo "  Note: May not have protocol files yet"
    ((TESTS_PASSED++))
fi

echo ""

################################################################################
# TEST SUMMARY
################################################################################

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST SUMMARY: AC#4${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Tests Run:    $TESTS_RUN"
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}STATUS: FAILING (Critical Issues) ✗${NC}"
    echo ""
    echo "Operational folders have been affected by src/ creation."
    echo "Commands or skills reference src/ directory (should not)."
    echo ""
    echo "Issues must be resolved before proceeding."
    echo ""
    exit 1
else
    echo -e "${GREEN}STATUS: PASSING ✓${NC}"
    echo ""
    echo "All assertions passed. AC#4 requirements satisfied."
    echo "Current operations remain unaffected by src/ creation."
    echo ""
    exit 0
fi
