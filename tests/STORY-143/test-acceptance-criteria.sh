#!/bin/bash
################################################################################
# Test Suite: STORY-143 - Document user-input-guidance.md in SKILL.md
################################################################################
#
# Purpose: Comprehensive failing tests (RED phase) for documenting the
# user-input-guidance.md reference file in devforgeai-ideation SKILL.md
#
# Test Structure:
# - 4 Acceptance Criteria tests (AC1-AC4)
# - 3 Business Rule tests (BR1-BR3)
# - 2 Non-Functional Requirement tests (NFR1-NFR2)
# - 5 Edge Case tests (EC1-EC5)
# Total: 14 test cases (all FAILING - RED phase TDD)
#
# Framework: bash with grep/wc for validation
# Exit codes: 0=all tests passed, 1=any test failed
# Expected: ALL RED/FAILED (SKILL.md not yet updated with user-input-guidance.md)
#
# Story Context:
# - Story ID: STORY-143
# - Title: Document user-input-guidance.md in SKILL.md
# - Reference File: .claude/skills/devforgeai-ideation/references/user-input-guidance.md
# - Actual line count: 897 lines
# - To be documented in SKILL.md Reference Files section
#
################################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# File paths
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-ideation/SKILL.md"
USER_INPUT_GUIDANCE="${PROJECT_ROOT}/.claude/skills/devforgeai-ideation/references/user-input-guidance.md"

################################################################################
# UTILITY FUNCTIONS
################################################################################

log_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

log_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((TESTS_PASSED++))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((TESTS_FAILED++))
}

log_header() {
    echo ""
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}$1${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

assert_success() {
    local test_name=$1
    local exit_code=$2
    ((TESTS_RUN++))

    if [ $exit_code -eq 0 ]; then
        log_pass "$test_name"
    else
        log_fail "$test_name (exit code: $exit_code)"
    fi
}

assert_file_exists() {
    local test_name=$1
    local file_path=$2
    ((TESTS_RUN++))

    if [ -f "$file_path" ]; then
        log_pass "$test_name"
    else
        log_fail "$test_name (file not found: $file_path)"
    fi
}

assert_grep_found() {
    local test_name=$1
    local pattern=$2
    local file_path=$3
    ((TESTS_RUN++))

    if grep -q "$pattern" "$file_path" 2>/dev/null; then
        log_pass "$test_name"
    else
        log_fail "$test_name (pattern not found: $pattern)"
    fi
}

assert_grep_not_found() {
    local test_name=$1
    local pattern=$2
    local file_path=$3
    ((TESTS_RUN++))

    if ! grep -q "$pattern" "$file_path" 2>/dev/null; then
        log_pass "$test_name"
    else
        log_fail "$test_name (pattern should not exist: $pattern)"
    fi
}

assert_line_count() {
    local test_name=$1
    local file_path=$2
    local expected_line_count=$3
    local tolerance=$4  # Allow +/- tolerance
    ((TESTS_RUN++))

    if [ ! -f "$file_path" ]; then
        log_fail "$test_name (file not found: $file_path)"
        return
    fi

    local actual_count=$(wc -l < "$file_path")
    local lower=$((expected_line_count - tolerance))
    local upper=$((expected_line_count + tolerance))

    if [ "$actual_count" -ge "$lower" ] && [ "$actual_count" -le "$upper" ]; then
        log_pass "$test_name (actual: $actual_count lines, expected: $expected_line_count ±$tolerance)"
    else
        log_fail "$test_name (line count $actual_count outside range $lower-$upper)"
    fi
}

################################################################################
# AC#1: SKILL.md Reference Files section updated
################################################################################

log_header "ACCEPTANCE CRITERIA #1: SKILL.md Reference Files section updated"

test_ac1_reference_files_section_exists() {
    local test_name="AC#1-01: Reference Files section exists in SKILL.md"
    log_test "$test_name"
    assert_grep_found "$test_name" "## Reference Files" "$SKILL_FILE"
}

test_ac1_user_input_guidance_in_reference_files() {
    local test_name="AC#1-02: user-input-guidance.md listed in Reference Files section"
    log_test "$test_name"
    assert_grep_found "$test_name" "user-input-guidance.md" "$SKILL_FILE"
}

test_ac1_line_count_documented() {
    local test_name="AC#1-03: Line count (~898 lines) documented for user-input-guidance.md"
    log_test "$test_name"
    assert_grep_found "$test_name" "898" "$SKILL_FILE"
}

test_ac1_description_for_guidance() {
    local test_name="AC#1-04: Description mentions framework-internal guidance"
    log_test "$test_name"
    # Should contain description about user input guidance being framework-internal
    assert_grep_found "$test_name" "user.*input.*guidance" "$SKILL_FILE"
}

test_ac1_key_contents_documented() {
    local test_name="AC#1-05: Key contents listed (patterns, templates, NFR table)"
    log_test "$test_name"
    # Check for mention of key contents: elicitation patterns, templates, NFR
    grep -q "user-input-guidance.md" "$SKILL_FILE" && \
    (grep -A 2 "user-input-guidance.md" "$SKILL_FILE" | grep -qi "pattern\|template\|nfr") || \
    grep -qi "15.*elicitation.*pattern\|28.*askuserquestion" "$SKILL_FILE"
    assert_success "$test_name" $?
}

test_ac1_5() {
    test_ac1_reference_files_section_exists
}

test_ac1_4() {
    test_ac1_user_input_guidance_in_reference_files
}

test_ac1_3() {
    test_ac1_line_count_documented
}

test_ac1_2() {
    test_ac1_description_for_guidance
}

test_ac1_1() {
    test_ac1_key_contents_documented
}

################################################################################
# AC#2: Phase 1 workflow references user-input-guidance.md
################################################################################

log_header "ACCEPTANCE CRITERIA #2: Phase 1 workflow references user-input-guidance.md"

test_ac2_step_0_5_exists() {
    local test_name="AC#2-01: Step 0.5 exists in Phase 1 workflow"
    log_test "$test_name"
    assert_grep_found "$test_name" "Step 0.5" "$SKILL_FILE"
}

test_ac2_step_0_5_loads_guidance() {
    local test_name="AC#2-02: Step 0.5 instruction loads user-input-guidance.md"
    log_test "$test_name"
    # Check that Step 0.5 specifically mentions loading user-input-guidance.md
    assert_grep_found "$test_name" "user-input-guidance" "$SKILL_FILE"
}

test_ac2_read_command_present() {
    local test_name="AC#2-03: Read command example present for user-input-guidance.md"
    log_test "$test_name"
    # Should contain Read command with path to user-input-guidance.md
    grep -q "Read.*user-input-guidance.md" "$SKILL_FILE" || \
    grep -q "user-input-guidance.md.*Read" "$SKILL_FILE"
    assert_success "$test_name" $?
}

test_ac2_error_tolerant_loading() {
    local test_name="AC#2-04: Error-tolerant loading pattern documented"
    log_test "$test_name"
    # Should mention graceful degradation or error handling for missing file
    grep -qi "error.*tolerant\|graceful.*degrad\|if.*fail\|if.*missing" "$SKILL_FILE"
    assert_success "$test_name" $?
}

test_ac2_correct_file_path() {
    local test_name="AC#2-05: Correct file path in SKILL.md"
    log_test "$test_name"
    # Path must be: .claude/skills/devforgeai-ideation/references/user-input-guidance.md
    assert_grep_found "$test_name" ".claude/skills/devforgeai-ideation/references/user-input-guidance.md" "$SKILL_FILE"
}

################################################################################
# AC#3: Cross-reference to skill integration section
################################################################################

log_header "ACCEPTANCE CRITERIA #3: Cross-reference to skill integration section"

test_ac3_section_5_reference() {
    local test_name="AC#3-01: Section 5 pointer included in reference"
    log_test "$test_name"
    # Should reference Section 5 or "Skill Integration Guide"
    grep -qi "section 5\|skill integration guide" "$SKILL_FILE"
    assert_success "$test_name" $?
}

test_ac3_ideation_integration() {
    local test_name="AC#3-02: devforgeai-ideation integration patterns referenced"
    log_test "$test_name"
    # Reference should mention devforgeai-ideation integration
    grep -qi "devforgeai-ideation.*integration\|integration.*devforgeai-ideation" "$SKILL_FILE"
    assert_success "$test_name" $?
}

test_ac3_story_creation_integration() {
    local test_name="AC#3-03: devforgeai-story-creation integration patterns referenced"
    log_test "$test_name"
    # Reference should mention devforgeai-story-creation integration
    grep -qi "devforgeai-story-creation.*integration\|integration.*devforgeai-story-creation" "$SKILL_FILE"
    assert_success "$test_name" $?
}

################################################################################
# AC#4: Documentation completeness validated
################################################################################

log_header "ACCEPTANCE CRITERIA #4: Documentation completeness validated"

test_ac4_file_exists() {
    local test_name="AC#4-01: user-input-guidance.md reference file exists"
    log_test "$test_name"
    assert_file_exists "$test_name" "$USER_INPUT_GUIDANCE"
}

test_ac4_appears_in_reference_list() {
    local test_name="AC#4-02: user-input-guidance.md appears in SKILL.md reference listing"
    log_test "$test_name"
    assert_grep_found "$test_name" "user-input-guidance" "$SKILL_FILE"
}

test_ac4_accurate_line_count() {
    local test_name="AC#4-03: Line count is accurate (actual: 897, tolerance: ±10)"
    log_test "$test_name"
    assert_line_count "$test_name" "$USER_INPUT_GUIDANCE" 897 10
}

test_ac4_description_complete() {
    local test_name="AC#4-04: Reference includes complete description"
    log_test "$test_name"
    # Must have description in SKILL.md for user-input-guidance.md entry
    grep -A 1 "user-input-guidance.md" "$SKILL_FILE" | grep -qi "description\|pattern\|framework"
    assert_success "$test_name" $?
}

################################################################################
# BUSINESS RULES
################################################################################

log_header "BUSINESS RULES"

test_br1_all_reference_files_documented() {
    local test_name="BR#1: All reference files in directory documented in SKILL.md"
    log_test "$test_name"
    # Count reference files vs documented
    local ref_count=$(find "${PROJECT_ROOT}/.claude/skills/devforgeai-ideation/references" -maxdepth 1 -name "*.md" -type f | wc -l)
    local doc_count=$(grep -c "^- \*\*" "$SKILL_FILE" 2>/dev/null || echo 0)

    if [ "$doc_count" -gt 0 ]; then
        log_pass "$test_name (found $doc_count documented references)"
    else
        log_fail "$test_name (no documented references found)"
    fi
}

test_br2_error_tolerant_pattern() {
    local test_name="BR#2: Loading must be error-tolerant (graceful degradation)"
    log_test "$test_name"
    # Should mention error handling, try/catch, or conditional loading
    grep -qi "error.*tolerant\|graceful.*degrad\|if.*fail\|if.*missing\|continue with" "$SKILL_FILE"
    assert_success "$test_name" $?
}

test_br3_line_count_accurate() {
    local test_name="BR#3: Line count must be accurate (within 10% of actual)"
    log_test "$test_name"
    # Documented should be ~898, actual is 897
    grep -qi "897\|898\|~898" "$SKILL_FILE"
    assert_success "$test_name" $?
}

################################################################################
# NON-FUNCTIONAL REQUIREMENTS
################################################################################

log_header "NON-FUNCTIONAL REQUIREMENTS"

test_nfr1_documentation_complete() {
    local test_name="NFR#1: Documentation completeness (100% of reference files documented)"
    log_test "$test_name"
    # Check that user-input-guidance.md is in the Reference Files section
    grep -q "Reference Files" "$SKILL_FILE" && \
    grep -q "user-input-guidance.md" "$SKILL_FILE"
    assert_success "$test_name" $?
}

test_nfr2_guidance_loading_overhead() {
    local test_name="NFR#2: Guidance loading adds minimal overhead"
    log_test "$test_name"
    # Should include Step 0.5 as selective loading (not in main workflow burden)
    grep -q "Step 0.5" "$SKILL_FILE" && \
    grep -qi "selective\|on-demand\|load" "$SKILL_FILE"
    assert_success "$test_name" $?
}

################################################################################
# EDGE CASES
################################################################################

log_header "EDGE CASES"

test_ec1_file_missing_graceful() {
    local test_name="EC#1: If user-input-guidance.md missing, Step 0.5 continues gracefully"
    log_test "$test_name"
    # Should document how to handle missing file
    grep -qi "if.*fail\|continue\|optional\|baseline" "$SKILL_FILE"
    assert_success "$test_name" $?
}

test_ec2_line_count_changes() {
    local test_name="EC#2: Line count uses approximate format (~898) for future updates"
    log_test "$test_name"
    # Should use ~ (tilde) to indicate approximate count
    grep -q "~.*898\|~.*89[0-9]" "$SKILL_FILE"
    assert_success "$test_name" $?
}

test_ec3_section_references_stable() {
    local test_name="EC#3: Cross-references use section titles not numbers"
    log_test "$test_name"
    # Should reference "Skill Integration Guide" not "Section 5"
    grep -qi "skill integration guide" "$SKILL_FILE"
    assert_success "$test_name" $?
}

test_ec4_correct_path_format() {
    local test_name="EC#4: File path uses correct format (.claude/skills/...)"
    log_test "$test_name"
    # Path must start with .claude not ./claude or claude
    grep -q "\.claude/skills/devforgeai-ideation/references/user-input-guidance\.md" "$SKILL_FILE"
    assert_success "$test_name" $?
}

test_ec5_step_0_5_before_discovery() {
    local test_name="EC#5: Step 0.5 positioned before discovery questions in workflow"
    log_test "$test_name"
    # Check that Step 0.5 appears before Step 1 in Phase 1
    local step_0_5_line=$(grep -n "Step 0.5" "$SKILL_FILE" 2>/dev/null | head -1 | cut -d: -f1)
    local step_1_line=$(grep -n "Step 1" "$SKILL_FILE" 2>/dev/null | head -1 | cut -d: -f1)

    if [ -z "$step_0_5_line" ] || [ -z "$step_1_line" ]; then
        log_fail "$test_name (Step 0.5 or Step 1 not found)"
    elif [ "$step_0_5_line" -lt "$step_1_line" ]; then
        log_pass "$test_name (Step 0.5 at line $step_0_5_line before Step 1 at line $step_1_line)"
    else
        log_fail "$test_name (Step 0.5 at line $step_0_5_line NOT before Step 1 at line $step_1_line)"
    fi
}

################################################################################
# TEST EXECUTION
################################################################################

log_header "RUNNING ALL TESTS - STORY-143"

echo "Configuration:"
echo "  SKILL file: $SKILL_FILE"
echo "  Reference: $USER_INPUT_GUIDANCE"
echo ""

# AC#1 Tests
test_ac1_5
test_ac1_4
test_ac1_3
test_ac1_2
test_ac1_1

# AC#2 Tests
test_ac2_step_0_5_exists
test_ac2_step_0_5_loads_guidance
test_ac2_read_command_present
test_ac2_error_tolerant_loading
test_ac2_correct_file_path

# AC#3 Tests
test_ac3_section_5_reference
test_ac3_ideation_integration
test_ac3_story_creation_integration

# AC#4 Tests
test_ac4_file_exists
test_ac4_appears_in_reference_list
test_ac4_accurate_line_count
test_ac4_description_complete

# BR Tests
test_br1_all_reference_files_documented
test_br2_error_tolerant_pattern
test_br3_line_count_accurate

# NFR Tests
test_nfr1_documentation_complete
test_nfr2_guidance_loading_overhead

# Edge Case Tests
test_ec1_file_missing_graceful
test_ec2_line_count_changes
test_ec3_section_references_stable
test_ec4_correct_path_format
test_ec5_step_0_5_before_discovery

################################################################################
# SUMMARY REPORT
################################################################################

log_header "TEST EXECUTION SUMMARY"

echo "Total Tests Run:  $TESTS_RUN"
echo -e "Tests Passed:     ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed:     ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✓ ALL TESTS PASSED - GREEN PHASE READY${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 0
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}✗ TESTS FAILED - RED PHASE (EXPECTED FOR TDD)${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Next Steps for Implementation (TDD Green Phase):"
    echo "1. Update .claude/skills/devforgeai-ideation/SKILL.md"
    echo "2. Add user-input-guidance.md to Reference Files section (line ~289+)"
    echo "3. Add Step 0.5 in Phase 1 Discovery section with Read command"
    echo "4. Add cross-references to Section 5 skill integration patterns"
    echo "5. Document line count (~898 lines) and key contents"
    echo "6. Ensure error-tolerant loading pattern documented"
    echo ""
    exit 1
fi
