#!/bin/bash

##############################################################################
# Test Suite: STORY-390 AC#5 - Component ID Auto-Detection from File Path
# Purpose: Verify agents/ maps to agent type, skills/*/SKILL.md maps to skill
#          type, commands/ maps to command type, unknown paths rejected
#
# Implementation: src/claude/commands/prompt-version.md (Slash Command)
# Test Type: Structural + Pattern (Markdown Command Testing Pattern)
#
# All tests MUST FAIL (TDD RED) until implementation exists.
##############################################################################

set -o pipefail

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

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
IMPL_FILE="${PROJECT_ROOT}/src/claude/commands/prompt-version.md"

##############################################################################
# Test Framework Functions
##############################################################################

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func 2>/dev/null; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "  ${GREEN}PASS${NC}: $test_name"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "  ${RED}FAIL${NC}: $test_name"
    fi
}

##############################################################################
# AC#5 Tests: Component ID Auto-Detection from File Path
##############################################################################

# --- Structural Tests ---

test_implementation_file_exists() {
    [ -f "$IMPL_FILE" ]
}

test_has_auto_detection_section() {
    # Must have a section documenting auto-detection logic
    grep -qiE "^#{1,3}.*(auto.?detect|path.*detect|component.*detect)" "$IMPL_FILE"
}

# --- Pattern Tests: Agent Detection ---

test_detects_agent_type_from_agents_path() {
    # src/claude/agents/*.md -> type: agent
    grep -qiE "(agents/.*agent|agents.*type.*agent|path.*agents.*=.*agent)" "$IMPL_FILE"
}

test_derives_agent_component_id_from_filename() {
    # Agent component_id derived from filename (e.g., test-automator from test-automator.md)
    grep -qiE "(test-automator|filename.*component_id|derive.*id.*filename)" "$IMPL_FILE"
}

# --- Pattern Tests: Skill Detection ---

test_detects_skill_type_from_skills_path() {
    # src/claude/skills/*/SKILL.md -> type: skill
    grep -qiE "(skills/.*skill|skills.*type.*skill|path.*skills.*=.*skill)" "$IMPL_FILE"
}

test_derives_skill_component_id_from_directory() {
    # Skill component_id derived from directory name (e.g., devforgeai-development from devforgeai-development/SKILL.md)
    grep -qiE "(SKILL\.md|directory.*component_id|skill.*directory.*name)" "$IMPL_FILE"
}

# --- Pattern Tests: Command Detection ---

test_detects_command_type_from_commands_path() {
    # src/claude/commands/*.md -> type: command
    grep -qiE "(commands/.*command|commands.*type.*command|path.*commands.*=.*command)" "$IMPL_FILE"
}

test_derives_command_component_id_from_filename() {
    # Command component_id derived from filename (e.g., dev from dev.md)
    grep -qiE "(command.*filename|derive.*command.*id|command.*component_id)" "$IMPL_FILE"
}

# --- Pattern Tests: File Validation ---

test_validates_file_exists_via_read() {
    # Must validate file exists using Read() tool
    grep -qiE "(Read\(.*file_path|validate.*file.*exists|file.*exist)" "$IMPL_FILE"
}

# --- Pattern Tests: Error Handling ---

test_rejects_unknown_path_pattern() {
    # Must reject paths not matching any known component pattern
    grep -qiE "(unknown.*path|invalid.*path|not.*match.*pattern|reject.*path)" "$IMPL_FILE"
}

test_lists_valid_path_patterns_on_rejection() {
    # Error must list valid path patterns
    grep -qiE "(valid.*path.*pattern|accepted.*pattern|expected.*path)" "$IMPL_FILE"
}

# --- Business Rule Tests ---

test_br001_component_id_lowercase_hyphen() {
    # BR-001: Component ID must be lowercase, hyphen-separated
    grep -qiE "(lowercase|hyphen.?separated|\[a-z\])" "$IMPL_FILE"
}

test_br002_component_type_enum() {
    # BR-002: Component type must be agent|skill|command
    grep -qiE "(agent.*skill.*command|type.*agent|type.*skill|type.*command)" "$IMPL_FILE"
}

test_br003_path_must_start_with_src_claude() {
    # BR-003: File paths must start with src/claude/
    grep -qiE "(src/claude/.*prefix|must.*start.*src/claude|path.*src/claude)" "$IMPL_FILE"
}

test_br003_path_must_end_with_md() {
    # BR-003: File paths must end with .md extension
    grep -qiE "(\.md.*extension|end.*\.md|\.md.*required)" "$IMPL_FILE"
}

# --- Edge Case Tests ---

test_handles_path_with_nested_directories() {
    # Must handle skill paths with nested directory structure (skills/name/SKILL.md)
    grep -qiE "(skills/.*SKILL\.md|nested.*directory)" "$IMPL_FILE"
}

test_handles_path_traversal_rejection() {
    # NFR-004: Must reject paths with ../ (path traversal)
    grep -qiE "(path.*traversal|\.\./.*reject|\.\..*forbidden)" "$IMPL_FILE"
}

test_handles_absolute_path_outside_project() {
    # NFR-004: Must reject absolute paths outside project root
    grep -qiE "(absolute.*path.*reject|outside.*project.*root)" "$IMPL_FILE"
}

test_handles_multiple_path_formats() {
    # Must handle both forward slashes and be consistent
    grep -qiE "(src/claude/agents/|src/claude/skills/|src/claude/commands/)" "$IMPL_FILE"
}

test_handles_component_renamed_between_versions() {
    # Edge case: component renamed or moved between versions
    grep -qiE "(renamed|moved|PATH_CHANGED|path.*mismatch)" "$IMPL_FILE"
}

##############################################################################
# Test Execution
##############################################################################

echo "=============================================="
echo "  STORY-390 AC#5: Component ID Auto-Detection"
echo "  TDD Phase: RED (tests must fail)"
echo "=============================================="

# Structural Tests
run_test "Implementation file exists" test_implementation_file_exists
run_test "Has auto-detection section" test_has_auto_detection_section

# Pattern Tests: Agent Detection
run_test "Detects agent type from agents/ path" test_detects_agent_type_from_agents_path
run_test "Derives agent component_id from filename" test_derives_agent_component_id_from_filename

# Pattern Tests: Skill Detection
run_test "Detects skill type from skills/ path" test_detects_skill_type_from_skills_path
run_test "Derives skill component_id from directory" test_derives_skill_component_id_from_directory

# Pattern Tests: Command Detection
run_test "Detects command type from commands/ path" test_detects_command_type_from_commands_path
run_test "Derives command component_id from filename" test_derives_command_component_id_from_filename

# Pattern Tests: Validation
run_test "Validates file exists via Read()" test_validates_file_exists_via_read

# Pattern Tests: Error Handling
run_test "Rejects unknown path pattern" test_rejects_unknown_path_pattern
run_test "Lists valid path patterns on rejection" test_lists_valid_path_patterns_on_rejection

# Business Rule Tests
run_test "BR-001: Component ID lowercase hyphen" test_br001_component_id_lowercase_hyphen
run_test "BR-002: Component type enum" test_br002_component_type_enum
run_test "BR-003: Path starts with src/claude/" test_br003_path_must_start_with_src_claude
run_test "BR-003: Path ends with .md" test_br003_path_must_end_with_md

# Edge Case Tests
run_test "Handles nested directory paths" test_handles_path_with_nested_directories
run_test "Handles path traversal rejection" test_handles_path_traversal_rejection
run_test "Handles absolute path outside project" test_handles_absolute_path_outside_project
run_test "Handles multiple path formats" test_handles_multiple_path_formats
run_test "Handles renamed components" test_handles_component_renamed_between_versions

##############################################################################
# Summary
##############################################################################

echo ""
echo "=============================================="
echo "  AC#5 Test Results"
echo "=============================================="
echo -e "  Total:  ${TESTS_RUN}"
echo -e "  Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "  Failed: ${RED}${TESTS_FAILED}${NC}"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo -e "${RED}RESULT: FAIL${NC} - $TESTS_FAILED test(s) failed (TDD RED confirmed)"
    exit 1
else
    echo -e "${GREEN}RESULT: PASS${NC} - All tests passed"
    exit 0
fi
