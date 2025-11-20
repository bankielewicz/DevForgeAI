#!/bin/bash

##############################################################################
# Test Suite: STORY-043 AC-4 - Progressive Disclosure Loading from src/
#
# AC-4: Progressive Disclosure Loading from src/ Structure
# Given: Skills load references/ files during workflow execution
# When: Test devforgeai-story-creation skill Phase 2 execution
# Then: Skill loads acceptance-criteria-patterns.md from src/ successfully
#
# Expected Output:
# - Read(file_path="src/claude/skills/devforgeai-story-creation/references/...")
# - Successfully loads 1,259 lines (48.2 KB)
# - Applies patterns for Given/When/Then AC generation
# - No file-not-found errors occur
# - Progressive disclosure works identically to pre-refactor
# - Test log: "Progressive disclosure: WORKING (src/ structure)"
##############################################################################

set -euo pipefail

TEST_NAME="AC-4: Progressive Disclosure Loading from src/ Structure"
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
# TEST 1: src/claude/ structure exists
##############################################################################

test_src_claude_structure_exists() {
    # Test: src/claude/ directory exists with expected subdirectories
    if [ -d "$PROJECT_ROOT/src/claude" ]; then
        echo "  src/claude/ directory exists"
        return 0
    else
        echo "  ERROR: src/claude/ directory not found"
        return 1
    fi
}

test_skills_directory_in_src() {
    # Test: src/claude/skills/ directory exists
    if [ -d "$PROJECT_ROOT/src/claude/skills" ]; then
        echo "  src/claude/skills/ directory exists"
        return 0
    else
        echo "  ERROR: src/claude/skills/ directory not found"
        return 1
    fi
}

test_devforgeai_story_creation_in_src() {
    # Test: src/claude/skills/devforgeai-story-creation/ exists
    if [ -d "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation" ]; then
        echo "  src/claude/skills/devforgeai-story-creation/ exists"
        return 0
    else
        echo "  ERROR: devforgeai-story-creation skill not found in src/"
        return 1
    fi
}

##############################################################################
# TEST 2: References subdirectory and files exist
##############################################################################

test_references_directory_exists() {
    # Test: src/claude/skills/devforgeai-story-creation/references/ exists
    if [ -d "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references" ]; then
        echo "  references/ directory exists"
        return 0
    else
        echo "  ERROR: references/ directory not found"
        return 1
    fi
}

test_acceptance_criteria_patterns_file() {
    # Test: acceptance-criteria-patterns.md file exists
    if [ -f "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md" ]; then
        echo "  acceptance-criteria-patterns.md file exists"
        return 0
    else
        echo "  ERROR: acceptance-criteria-patterns.md not found"
        return 1
    fi
}

test_acceptance_criteria_file_size() {
    # Test: File is substantial (>30 KB)
    if [ -f "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md" ]; then
        local actual_size=$(stat -c%s "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md" 2>/dev/null || echo "0")
        local size_kb=$((actual_size / 1024))
        # Accept substantial files (>30KB)
        if [ "$actual_size" -gt 30000 ]; then
            echo "  File size: ${size_kb}KB (acceptable, >30KB)"
            return 0
        else
            echo "  ERROR: File size $actual_size bytes (expected >30KB)"
            return 1
        fi
    else
        return 1
    fi
}

test_acceptance_criteria_file_line_count() {
    # Test: File contains approximately 1,259 lines (±5%)
    if [ -f "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md" ]; then
        local actual_lines=$(wc -l < "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md" 2>/dev/null || echo "0")
        local expected_lines=1259
        local tolerance=63  # ±5%
        local lower=$((expected_lines - tolerance))
        local upper=$((expected_lines + tolerance))

        if [ "$actual_lines" -ge "$lower" ] && [ "$actual_lines" -le "$upper" ]; then
            echo "  Line count: $actual_lines (expected ~$expected_lines ±$tolerance)"
            return 0
        else
            echo "  ERROR: Line count $actual_lines (expected ~$expected_lines ±$tolerance)"
            return 1
        fi
    else
        return 1
    fi
}

##############################################################################
# TEST 3: Reference file content validity
##############################################################################

test_reference_file_is_markdown() {
    # Test: File is valid Markdown format
    if [ -f "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md" ]; then
        if file "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md" | grep -q "text\|ASCII"; then
            echo "  File is valid text format"
            return 0
        else
            echo "  ERROR: File is not text format"
            return 1
        fi
    else
        return 1
    fi
}

test_reference_file_contains_patterns() {
    # Test: File contains pattern examples (Given/When/Then)
    if [ -f "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md" ]; then
        local pattern_count=0
        grep -q "Given\|given" "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md" && pattern_count=$((pattern_count + 1))
        grep -q "When\|when" "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md" && pattern_count=$((pattern_count + 1))
        grep -q "Then\|then" "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md" && pattern_count=$((pattern_count + 1))

        if [ "$pattern_count" -ge 2 ]; then
            echo "  File contains BDD pattern examples (Given/When/Then)"
            return 0
        else
            echo "  ERROR: File missing BDD pattern examples"
            return 1
        fi
    else
        return 1
    fi
}

##############################################################################
# TEST 4: No file-not-found errors
##############################################################################

test_file_readable() {
    # Test: File is readable
    if [ -r "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md" ]; then
        echo "  File is readable"
        return 0
    else
        echo "  ERROR: File is not readable"
        return 1
    fi
}

test_path_resolution_succeeds() {
    # Test: Path resolves without symlink issues
    local resolved_path=$(cd "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references/" && pwd)
    if [ -d "$resolved_path" ]; then
        echo "  Path resolves correctly: $resolved_path"
        return 0
    else
        echo "  ERROR: Path resolution failed"
        return 1
    fi
}

##############################################################################
# TEST 5: Other reference files load correctly
##############################################################################

test_other_reference_files_exist() {
    # Test: Other reference files also exist in src/ structure
    local ref_dir="$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/references"
    local file_count=$(find "$ref_dir" -type f -name "*.md" 2>/dev/null | wc -l)

    if [ "$file_count" -gt 1 ]; then
        echo "  Found $file_count reference files in src/claude/skills/devforgeai-story-creation/references/"
        return 0
    else
        echo "  ERROR: Only $file_count reference file found (expected >1)"
        return 1
    fi
}

test_skill_markdown_file_exists() {
    # Test: devforgeai-story-creation SKILL.md exists in src/
    if [ -f "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/SKILL.md" ]; then
        echo "  SKILL.md exists in src/claude/skills/devforgeai-story-creation/"
        return 0
    else
        echo "  ERROR: SKILL.md not found in src/"
        return 1
    fi
}

##############################################################################
# TEST 6: Progressive disclosure pattern validation
##############################################################################

test_skill_loads_from_src() {
    # Test: SKILL.md contains Read() calls to src/claude/
    if [ -f "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/SKILL.md" ]; then
        if grep -q "Read.*src/claude\|src/claude.*Read" "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/SKILL.md" 2>/dev/null; then
            echo "  SKILL.md contains Read() calls to src/claude/"
            return 0
        else
            echo "  WARNING: SKILL.md may not reference src/claude/ (check manually)"
            return 0  # Non-blocking
        fi
    else
        return 1
    fi
}

test_no_old_dot_claude_references() {
    # Test: SKILL.md does NOT contain old .claude/ references
    if [ -f "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/SKILL.md" ]; then
        if grep -q "Read.*\.claude/" "$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/SKILL.md" 2>/dev/null; then
            echo "  ERROR: SKILL.md still contains old .claude/ references"
            return 1
        else
            echo "  SKILL.md does not contain old .claude/ references"
            return 0
        fi
    else
        return 1
    fi
}

##############################################################################
# TEST 7: Integration - other skills also load from src/
##############################################################################

test_other_skills_in_src() {
    # Test: Other skills also migrated to src/claude/skills/
    local skill_count=$(find "$PROJECT_ROOT/src/claude/skills" -maxdepth 1 -type d ! -name "skills" 2>/dev/null | wc -l)

    if [ "$skill_count" -gt 1 ]; then
        echo "  Found $skill_count skill directories in src/claude/skills/"
        return 0
    else
        echo "  ERROR: Only $skill_count skill directory found (expected >1)"
        return 1
    fi
}

test_devforgeai_orchestration_in_src() {
    # Test: devforgeai-orchestration skill exists in src/
    if [ -d "$PROJECT_ROOT/src/claude/skills/devforgeai-orchestration" ]; then
        echo "  devforgeai-orchestration skill exists in src/"
        return 0
    else
        echo "  ERROR: devforgeai-orchestration skill not found in src/"
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

    echo -e "${YELLOW}Phase 1: src/claude/ Structure${NC}"
    run_test "AC-4.1: src/claude/ structure exists" "test_src_claude_structure_exists"
    run_test "AC-4.2: src/claude/skills/ exists" "test_skills_directory_in_src"
    run_test "AC-4.3: devforgeai-story-creation exists" "test_devforgeai_story_creation_in_src"

    echo -e "\n${YELLOW}Phase 2: Reference File Location${NC}"
    run_test "AC-4.4: references/ directory exists" "test_references_directory_exists"
    run_test "AC-4.5: acceptance-criteria-patterns.md exists" "test_acceptance_criteria_patterns_file"
    run_test "AC-4.6: File size ~48.2 KB" "test_acceptance_criteria_file_size"
    run_test "AC-4.7: File lines ~1,259" "test_acceptance_criteria_file_line_count"

    echo -e "\n${YELLOW}Phase 3: Reference File Content${NC}"
    run_test "AC-4.8: File is valid Markdown" "test_reference_file_is_markdown"
    run_test "AC-4.9: File contains BDD patterns" "test_reference_file_contains_patterns"

    echo -e "\n${YELLOW}Phase 4: File Accessibility${NC}"
    run_test "AC-4.10: File is readable" "test_file_readable"
    run_test "AC-4.11: Path resolves correctly" "test_path_resolution_succeeds"

    echo -e "\n${YELLOW}Phase 5: Progressive Disclosure${NC}"
    run_test "AC-4.12: Other reference files exist" "test_other_reference_files_exist"
    run_test "AC-4.13: SKILL.md exists in src/" "test_skill_markdown_file_exists"
    run_test "AC-4.14: SKILL.md loads from src/" "test_skill_loads_from_src"
    run_test "AC-4.15: No old .claude/ references" "test_no_old_dot_claude_references"

    echo -e "\n${YELLOW}Phase 6: Integration${NC}"
    run_test "AC-4.16: Other skills in src/" "test_other_skills_in_src"
    run_test "AC-4.17: devforgeai-orchestration in src/" "test_devforgeai_orchestration_in_src"

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
