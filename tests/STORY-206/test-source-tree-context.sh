#!/bin/bash

##############################################################################
# Test Suite: STORY-206 - Update devforgeai-development Skill to Pass
#             source-tree.md Context to Subagents
#
# Purpose: Verify that the devforgeai-development skill properly reads and
#          passes source-tree.md context to test-automator subagent for
#          correct test file placement.
#
# TDD Status: RED (failing tests - before implementation)
#
# Acceptance Criteria:
#   AC#1: source-tree.md Read in Phase 1 (Red - Test First)
#   AC#2: Context Markers Set Before Subagent Invocation
#   AC#3: Context Available to test-automator
#   AC#4: Context Extraction Logic for Common Patterns
#   AC#5: Reference File Updated
#
# Files Under Test:
#   - .claude/skills/devforgeai-development/SKILL.md
#   - .claude/skills/devforgeai-development/references/tdd-red-phase.md
##############################################################################

# Do NOT use set -e - we want all tests to run even if some fail
# set -e

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

# File paths (absolute paths per source-tree.md constraints)
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_MD="${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md"
TDD_RED_PHASE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/references/tdd-red-phase.md"
PHASE_02_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/phases/phase-02-test-first.md"
SOURCE_TREE="${PROJECT_ROOT}/devforgeai/specs/context/source-tree.md"

##############################################################################
# Helper Functions
##############################################################################

run_test() {
    local test_name="$1"
    local test_description="$2"

    TESTS_RUN=$((TESTS_RUN + 1))

    echo ""
    echo -e "${YELLOW}Test $TESTS_RUN: $test_name${NC}"
    echo "Description: $test_description"
    echo "---"
}

assert_grep_match() {
    local pattern="$1"
    local file="$2"
    local test_name="$3"

    if grep -qE "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASSED${NC}: Pattern '$pattern' found in $file"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAILED${NC}: Pattern '$pattern' NOT found in $file"
        echo "Expected: Pattern matching '$pattern'"
        echo "Actual: Pattern not present"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_grep_multiline_match() {
    local pattern="$1"
    local file="$2"
    local test_name="$3"

    # Use perl for multiline matching since grep -P may not be available
    if perl -0777 -ne "exit(1) unless /$pattern/s" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASSED${NC}: Multiline pattern found in $file"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAILED${NC}: Multiline pattern NOT found in $file"
        echo "Expected: Pattern matching '$pattern'"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_file_exists() {
    local file="$1"

    if [[ -f "$file" ]]; then
        echo -e "${GREEN}PASSED${NC}: File $file exists"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAILED${NC}: File $file does not exist"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_pattern_before_task() {
    local context_pattern="$1"
    local task_pattern="$2"
    local file="$3"
    local test_name="$4"

    # Check that context_pattern appears before task_pattern in file
    local context_line=$(grep -n "$context_pattern" "$file" 2>/dev/null | head -1 | cut -d: -f1)
    local task_line=$(grep -n "$task_pattern" "$file" 2>/dev/null | head -1 | cut -d: -f1)

    if [[ -z "$context_line" ]]; then
        echo -e "${RED}FAILED${NC}: Context pattern '$context_pattern' not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi

    if [[ -z "$task_line" ]]; then
        echo -e "${RED}FAILED${NC}: Task pattern '$task_pattern' not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi

    if [[ "$context_line" -lt "$task_line" ]]; then
        echo -e "${GREEN}PASSED${NC}: Context (line $context_line) appears before Task (line $task_line)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAILED${NC}: Context (line $context_line) should appear BEFORE Task (line $task_line)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

##############################################################################
# Pre-flight Checks
##############################################################################

echo ""
echo "============================================================================"
echo "  STORY-206: Update devforgeai-development Skill to Pass source-tree.md"
echo "             Context to Subagents"
echo "============================================================================"
echo ""
echo "TDD Phase: RED (Tests written BEFORE implementation)"
echo ""
echo "Files under test:"
echo "  - $SKILL_MD"
echo "  - $TDD_RED_PHASE"
echo "  - $PHASE_02_FILE"
echo ""

# Verify source files exist
if [[ ! -f "$SKILL_MD" ]]; then
    echo -e "${RED}ERROR${NC}: SKILL.md not found at $SKILL_MD"
    exit 1
fi

if [[ ! -f "$TDD_RED_PHASE" ]]; then
    echo -e "${RED}ERROR${NC}: tdd-red-phase.md not found at $TDD_RED_PHASE"
    exit 1
fi

##############################################################################
# AC#1: source-tree.md Read in Phase 1 (Red - Test First)
##############################################################################

echo ""
echo "============================================================================"
echo "  AC#1: source-tree.md Read in Phase 1/Phase 2"
echo "============================================================================"

# Test 1.1: SKILL.md or phase files contain Read() for source-tree.md
run_test \
    "test_source_tree_read_in_skill" \
    "Verify SKILL.md or phase-02-test-first.md contains Read() call for source-tree.md"

# Check in main SKILL.md first
if grep -qE 'Read\s*\([^)]*source-tree\.md' "$SKILL_MD" 2>/dev/null; then
    echo -e "${GREEN}PASSED${NC}: Read() for source-tree.md found in SKILL.md"
    TESTS_PASSED=$((TESTS_PASSED + 1))
# Also check in phase-02 file
elif [[ -f "$PHASE_02_FILE" ]] && grep -qE 'Read\s*\([^)]*source-tree\.md' "$PHASE_02_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASSED${NC}: Read() for source-tree.md found in phase-02-test-first.md"
    TESTS_PASSED=$((TESTS_PASSED + 1))
# Also check in tdd-red-phase.md reference
elif grep -qE 'Read\s*\([^)]*source-tree\.md' "$TDD_RED_PHASE" 2>/dev/null; then
    echo -e "${GREEN}PASSED${NC}: Read() for source-tree.md found in tdd-red-phase.md"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Read() for source-tree.md NOT found in any Phase 02 files"
    echo "Expected: Read(file_path=\"devforgeai/specs/context/source-tree.md\")"
    echo "Searched in: SKILL.md, phase-02-test-first.md, tdd-red-phase.md"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

# Test 1.2: Read happens in Phase 1 or Phase 2 context
run_test \
    "test_source_tree_read_phase_context" \
    "Verify source-tree.md read is associated with Phase 01 or Phase 02"

# The Read should be near Phase 01 preflight or Phase 02 test-first content
if grep -qE '(Phase 0[12]|Pre-?[Ff]light|[Tt]est-?[Ff]irst)' "$SKILL_MD" 2>/dev/null && \
   grep -qE 'source-tree\.md' "$SKILL_MD" 2>/dev/null; then
    echo -e "${GREEN}PASSED${NC}: source-tree.md referenced in skill with Phase 01/02 context"
    TESTS_PASSED=$((TESTS_PASSED + 1))
elif [[ -f "$PHASE_02_FILE" ]] && grep -qE 'source-tree\.md' "$PHASE_02_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASSED${NC}: source-tree.md referenced in phase-02-test-first.md"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: source-tree.md not found in Phase 01/02 context"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

##############################################################################
# AC#2: Context Markers Set Before Subagent Invocation
##############################################################################

echo ""
echo "============================================================================"
echo "  AC#2: Context Markers Set Before Subagent Invocation"
echo "============================================================================"

# Test 2.1: Context markers template exists with Module Under Test
run_test \
    "test_context_marker_module_under_test" \
    "Verify context markers template contains 'Module Under Test:'"

assert_grep_match \
    "\*\*Module Under Test:\*\*|\\\$MODULE_UNDER_TEST|module_under_test" \
    "$TDD_RED_PHASE" \
    "Module Under Test marker"

# Test 2.2: Context markers template contains Expected Test Directory
run_test \
    "test_context_marker_expected_test_directory" \
    "Verify context markers template contains 'Expected Test Directory:'"

assert_grep_match \
    "\*\*Expected Test Directory:\*\*|\\\$EXPECTED_TEST_DIRECTORY|expected_test_directory" \
    "$TDD_RED_PHASE" \
    "Expected Test Directory marker"

# Test 2.3: Context markers template contains Constraint reference
run_test \
    "test_context_marker_constraint" \
    "Verify context markers template contains 'Constraint:' or source-tree reference"

assert_grep_match \
    "\*\*Constraint:\*\*|\\\$CONSTRAINT|source-tree\.md constraint" \
    "$TDD_RED_PHASE" \
    "Constraint marker"

##############################################################################
# AC#3: Context Available to test-automator
##############################################################################

echo ""
echo "============================================================================"
echo "  AC#3: Context Available to test-automator"
echo "============================================================================"

# Test 3.1: Context markers appear BEFORE Task(subagent_type="test-automator")
run_test \
    "test_context_before_task_invocation" \
    "Verify context markers appear BEFORE Task(subagent_type=\"test-automator\")"

# Look in tdd-red-phase.md for the ordering
if [[ -f "$TDD_RED_PHASE" ]]; then
    # Check if there's content about test directories/modules before the Task() call
    assert_pattern_before_task \
        "[Mm]odule.*[Tt]est\|[Tt]est.*[Dd]irectory\|source-tree" \
        'Task.*test-automator\|subagent_type.*test-automator' \
        "$TDD_RED_PHASE" \
        "Context before test-automator Task"
else
    echo -e "${RED}FAILED${NC}: Cannot verify ordering - tdd-red-phase.md not found"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    TESTS_RUN=$((TESTS_RUN + 1))
fi

# Test 3.2: Task prompt includes test directory context
run_test \
    "test_task_prompt_includes_directory_context" \
    "Verify Task(test-automator) prompt includes test directory context"

assert_grep_match \
    "source-tree\.md.*test file placement|test file placement.*source-tree|Place tests according to source-tree" \
    "$TDD_RED_PHASE" \
    "Task prompt test directory context"

# Test 3.3: Context files mentioned in subagent context
run_test \
    "test_context_files_in_subagent_context" \
    "Verify source-tree.md is listed in 'Context files available' for test-automator"

assert_grep_match \
    "source-tree\.md.*test file placement|devforgeai/specs/context/source-tree\.md" \
    "$TDD_RED_PHASE" \
    "source-tree.md in context files"

##############################################################################
# AC#4: Context Extraction Logic for Common Patterns
##############################################################################

echo ""
echo "============================================================================"
echo "  AC#4: Context Extraction Logic for Common Patterns"
echo "============================================================================"

# Test 4.1: installer/* -> installer/tests/ pattern documented
run_test \
    "test_pattern_installer_tests" \
    "Verify pattern matching documents: installer/* -> installer/tests/"

# Check in SKILL.md, phase files, or tdd-red-phase.md
if grep -qE 'installer/\*.*installer/tests|installer.*tests/' "$SKILL_MD" 2>/dev/null || \
   grep -qE 'installer/\*.*installer/tests|installer.*tests/' "$TDD_RED_PHASE" 2>/dev/null || \
   ( [[ -f "$PHASE_02_FILE" ]] && grep -qE 'installer/\*.*installer/tests|installer.*tests/' "$PHASE_02_FILE" 2>/dev/null ); then
    echo -e "${GREEN}PASSED${NC}: installer/* -> installer/tests/ pattern found"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Pattern installer/* -> installer/tests/ NOT documented"
    echo "Expected: Documentation of pattern: installer/* -> installer/tests/"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

# Test 4.2: .claude/scripts/devforgeai_cli/* pattern documented
run_test \
    "test_pattern_devforgeai_cli_tests" \
    "Verify pattern: .claude/scripts/devforgeai_cli/* -> .claude/scripts/devforgeai_cli/tests/"

if grep -qE '\.claude/scripts/devforgeai_cli.*tests|devforgeai_cli.*tests/' "$SKILL_MD" 2>/dev/null || \
   grep -qE '\.claude/scripts/devforgeai_cli.*tests|devforgeai_cli.*tests/' "$TDD_RED_PHASE" 2>/dev/null || \
   ( [[ -f "$PHASE_02_FILE" ]] && grep -qE '\.claude/scripts/devforgeai_cli.*tests|devforgeai_cli.*tests/' "$PHASE_02_FILE" 2>/dev/null ); then
    echo -e "${GREEN}PASSED${NC}: devforgeai_cli/* -> devforgeai_cli/tests/ pattern found"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Pattern devforgeai_cli/* -> devforgeai_cli/tests/ NOT documented"
    echo "Expected: Documentation of pattern: .claude/scripts/devforgeai_cli/* -> .../tests/"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

# Test 4.3: src/* -> tests/ (default) pattern documented
run_test \
    "test_pattern_src_default" \
    "Verify default pattern: src/* -> tests/"

if grep -qE 'src/\*.*tests/|default.*tests/' "$SKILL_MD" 2>/dev/null || \
   grep -qE 'src/\*.*tests/|default.*tests/' "$TDD_RED_PHASE" 2>/dev/null || \
   ( [[ -f "$PHASE_02_FILE" ]] && grep -qE 'src/\*.*tests/|default.*tests/' "$PHASE_02_FILE" 2>/dev/null ); then
    echo -e "${GREEN}PASSED${NC}: src/* -> tests/ (default) pattern found"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Default pattern src/* -> tests/ NOT documented"
    echo "Expected: Documentation of default pattern: src/* -> tests/"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

# Test 4.4: Pattern matching logic is algorithmic (not hardcoded)
run_test \
    "test_pattern_matching_algorithm" \
    "Verify pattern matching uses algorithmic approach (extract from source-tree.md)"

# Look for evidence of dynamic extraction vs hardcoded paths
if grep -qiE 'extract.*source-tree|parse.*source-tree|read.*source-tree.*pattern|from source-tree\.md' "$TDD_RED_PHASE" 2>/dev/null || \
   grep -qiE 'source-tree\.md.*line|per source-tree|according to source-tree' "$TDD_RED_PHASE" 2>/dev/null; then
    echo -e "${GREEN}PASSED${NC}: Pattern extraction from source-tree.md found"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: No evidence of dynamic pattern extraction from source-tree.md"
    echo "Expected: Reference to extracting test directory patterns from source-tree.md"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

##############################################################################
# AC#5: Reference File Updated
##############################################################################

echo ""
echo "============================================================================"
echo "  AC#5: Reference File Updated (tdd-red-phase.md)"
echo "============================================================================"

# Test 5.1: tdd-red-phase.md mentions source-tree.md context
run_test \
    "test_reference_mentions_source_tree" \
    "Verify tdd-red-phase.md mentions source-tree.md context"

assert_grep_match \
    'source-tree\.md' \
    "$TDD_RED_PHASE" \
    "source-tree.md mention in tdd-red-phase.md"

# Test 5.2: tdd-red-phase.md documents test file placement rules
run_test \
    "test_reference_documents_placement_rules" \
    "Verify tdd-red-phase.md documents test file placement rules"

assert_grep_match \
    "test file placement|test directory|tests/.*location|Place tests" \
    "$TDD_RED_PHASE" \
    "Test placement rules in tdd-red-phase.md"

# Test 5.3: tdd-red-phase.md has Step for reading source-tree.md (Step 0 or Step 1.x)
run_test \
    "test_reference_has_source_tree_step" \
    "Verify tdd-red-phase.md has a step for reading source-tree.md"

# Look for a numbered step that includes source-tree.md reading
if grep -qE 'Step [0-9].*source-tree|[0-9]\.[0-9].*source-tree|Read.*source-tree\.md' "$TDD_RED_PHASE" 2>/dev/null; then
    echo -e "${GREEN}PASSED${NC}: Step for reading source-tree.md found"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: No dedicated step for reading source-tree.md"
    echo "Expected: A numbered step like 'Step 0: Read source-tree.md' or 'Step 1.x: Load source-tree context'"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

# Test 5.4: Context section in test-automator Task prompt updated
run_test \
    "test_task_prompt_context_updated" \
    "Verify test-automator Task prompt includes source-tree.md in context files list"

# Look for an explicit context files section mentioning source-tree.md
if grep -qE 'Context files.*:.*source-tree|source-tree\.md.*test file placement' "$TDD_RED_PHASE" 2>/dev/null; then
    echo -e "${GREEN}PASSED${NC}: Task prompt context section includes source-tree.md"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Task prompt context section does not explicitly include source-tree.md"
    echo "Expected: 'Context files available:' section listing source-tree.md"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi
TESTS_RUN=$((TESTS_RUN + 1))

##############################################################################
# Summary Report
##############################################################################

echo ""
echo "============================================================================"
echo "  Test Summary Report - STORY-206"
echo "============================================================================"
echo ""
echo "Total Tests Run:    $TESTS_RUN"
echo -e "Tests Passed:       ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed:       ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}============================================================================"
    echo "  ALL TESTS PASSED"
    echo "============================================================================${NC}"
    echo ""
    echo "STORY-206 Implementation Status: COMPLETE"
    echo ""
    echo "Acceptance Criteria Verified:"
    echo "  [x] AC#1: source-tree.md Read in Phase 1 (Red - Test First)"
    echo "  [x] AC#2: Context Markers Set Before Subagent Invocation"
    echo "  [x] AC#3: Context Available to test-automator"
    echo "  [x] AC#4: Context Extraction Logic for Common Patterns"
    echo "  [x] AC#5: Reference File Updated"
    exit 0
else
    echo -e "${RED}============================================================================"
    echo "  TESTS FAILED - TDD RED PHASE (Expected before implementation)"
    echo "============================================================================${NC}"
    echo ""
    echo "STORY-206 Implementation Status: PENDING"
    echo ""
    echo "Required Changes:"
    echo "  1. Add Read() for source-tree.md in Phase 02 workflow"
    echo "  2. Add context markers template with:"
    echo "     - **Module Under Test:**"
    echo "     - **Expected Test Directory:**"
    echo "     - **Constraint:** (source-tree.md reference)"
    echo "  3. Place context markers BEFORE Task(test-automator) invocation"
    echo "  4. Document pattern matching logic:"
    echo "     - installer/* -> installer/tests/"
    echo "     - .claude/scripts/devforgeai_cli/* -> .../tests/"
    echo "     - src/* -> tests/ (default)"
    echo "  5. Update tdd-red-phase.md with source-tree.md context guidance"
    echo ""
    echo "Files to modify:"
    echo "  - $SKILL_MD (or phases/phase-02-test-first.md)"
    echo "  - $TDD_RED_PHASE"
    exit 1
fi
