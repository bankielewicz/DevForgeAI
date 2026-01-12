#!/bin/bash
#
# STORY-204: Test Suite for File-Generation Subagents source-tree.md Validation
#
# Purpose: Verify all file-generation subagents have proper source-tree.md validation
#          following the pattern established by STORY-203 (test-automator)
#
# Test Strategy:
#   - AC#1: Verify audit produces list of 8 file-generation subagents
#   - AC#2: Verify source-tree.md reference in References section
#   - AC#3: Verify Pre-Generation Validation section exists
#   - AC#4: Verify HALT pattern present in validation section
#   - AC#5: Verify no regressions (existing functionality preserved)
#
# TDD Phase: RED - All tests should FAIL initially (subagents not yet modified)
#
# Author: claude/test-automator
# Date: 2026-01-12
# Story: STORY-204-file-generation-subagents-source-tree-validation

# Note: No set -e to allow all tests to run even if some fail

# Configuration
AGENTS_DIR="/mnt/c/Projects/DevForgeAI2/.claude/agents"
PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=0

# ANSI colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test result tracking
declare -a FAILED_TESTS

# File-generation subagents to test (7 subagents - test-automator covered by STORY-203)
# Per AC#1 expected subagents list
SUBAGENTS=(
    "story-requirements-analyst.md"
    "api-designer.md"
    "documentation-writer.md"
    "refactoring-specialist.md"
    "backend-architect.md"
    "frontend-developer.md"
    "agent-generator.md"
)

# ============================================================================
# Test Utility Functions
# ============================================================================

log_test_start() {
    local test_name="$1"
    echo -e "\n${YELLOW}[TEST]${NC} $test_name"
}

log_pass() {
    local message="$1"
    echo -e "${GREEN}[PASS]${NC} $message"
    ((PASS_COUNT++))
    ((TOTAL_TESTS++))
}

log_fail() {
    local message="$1"
    echo -e "${RED}[FAIL]${NC} $message"
    ((FAIL_COUNT++))
    ((TOTAL_TESTS++))
    FAILED_TESTS+=("$message")
}

# ============================================================================
# AC#1: Identify All File-Generation Subagents
# ============================================================================

test_ac1_subagent_audit_count() {
    log_test_start "AC#1: Verify file-generation subagent count is 8 (including test-automator)"

    # Count subagents with Write or Edit in their tools field
    local count=0

    for agent_file in "$AGENTS_DIR"/*.md; do
        # Skip backup files
        [[ "$agent_file" == *.backup* ]] && continue

        # Check if agent has Write or Edit tool in YAML frontmatter
        if grep -q "^tools:.*Write\|^tools:.*Edit" "$agent_file" 2>/dev/null; then
            ((count++))
        fi
    done

    # Per AC#1, expected 8 file-generation subagents
    if [[ $count -ge 8 ]]; then
        log_pass "Found $count file-generation subagents (expected >= 8)"
    else
        log_fail "Found only $count file-generation subagents (expected >= 8)"
    fi
}

test_ac1_subagent_list_complete() {
    log_test_start "AC#1: Verify all 7 target subagents exist"

    local missing=0

    for subagent in "${SUBAGENTS[@]}"; do
        if [[ -f "$AGENTS_DIR/$subagent" ]]; then
            echo "  Found: $subagent"
        else
            echo "  MISSING: $subagent"
            ((missing++))
        fi
    done

    if [[ $missing -eq 0 ]]; then
        log_pass "All 7 target subagents exist"
    else
        log_fail "Missing $missing target subagents"
    fi
}

# ============================================================================
# AC#2: Add source-tree.md to References Section
# ============================================================================

test_ac2_source_tree_in_references() {
    log_test_start "AC#2: Verify source-tree.md in References section of each subagent"

    local failures=0

    for subagent in "${SUBAGENTS[@]}"; do
        local file_path="$AGENTS_DIR/$subagent"

        if [[ ! -f "$file_path" ]]; then
            echo "  SKIP: $subagent (file not found)"
            continue
        fi

        # Check for source-tree.md reference in References section
        # Pattern: "Source Tree:" followed by source-tree.md path (with optional leading "- ")
        if grep -qE "(^|\- )\*\*Source Tree:\*\*.*source-tree\.md" "$file_path" 2>/dev/null; then
            echo "  OK: $subagent has source-tree.md in References"
        else
            echo "  MISSING: $subagent lacks source-tree.md in References section"
            ((failures++))
        fi
    done

    if [[ $failures -eq 0 ]]; then
        log_pass "All subagents have source-tree.md in References section"
    else
        log_fail "$failures subagents missing source-tree.md in References section"
    fi
}

test_ac2_source_tree_reference_format() {
    log_test_start "AC#2: Verify source-tree.md reference follows correct format"

    # Expected format per AC#2:
    # - **Source Tree:** `devforgeai/specs/context/source-tree.md` (file location constraints)

    local correct_format=0
    local incorrect_format=0

    for subagent in "${SUBAGENTS[@]}"; do
        local file_path="$AGENTS_DIR/$subagent"

        if [[ ! -f "$file_path" ]]; then
            continue
        fi

        # Check for exact format: **Source Tree:** `devforgeai/specs/context/source-tree.md`
        if grep -qE '^\- \*\*Source Tree:\*\* `devforgeai/specs/context/source-tree\.md`' "$file_path" 2>/dev/null; then
            echo "  OK: $subagent has correct format"
            ((correct_format++))
        else
            echo "  INCORRECT: $subagent has wrong format or missing"
            ((incorrect_format++))
        fi
    done

    if [[ $incorrect_format -eq 0 ]]; then
        log_pass "All subagents have correct source-tree.md reference format"
    else
        log_fail "$incorrect_format subagents have incorrect source-tree.md reference format"
    fi
}

# ============================================================================
# AC#3: Add Pre-Generation Validation Section
# ============================================================================

test_ac3_pre_generation_validation_section_exists() {
    log_test_start "AC#3: Verify Pre-Generation Validation section exists in each subagent"

    local missing=0

    for subagent in "${SUBAGENTS[@]}"; do
        local file_path="$AGENTS_DIR/$subagent"

        if [[ ! -f "$file_path" ]]; then
            echo "  SKIP: $subagent (file not found)"
            continue
        fi

        # Check for Pre-Generation Validation section header
        if grep -qE "^#+.*Pre-Generation Validation|^\*\*Pre-Generation Validation:" "$file_path" 2>/dev/null; then
            echo "  OK: $subagent has Pre-Generation Validation section"
        else
            echo "  MISSING: $subagent lacks Pre-Generation Validation section"
            ((missing++))
        fi
    done

    if [[ $missing -eq 0 ]]; then
        log_pass "All subagents have Pre-Generation Validation section"
    else
        log_fail "$missing subagents missing Pre-Generation Validation section"
    fi
}

test_ac3_pre_generation_validation_reads_source_tree() {
    log_test_start "AC#3: Verify Pre-Generation Validation reads source-tree.md"

    local failures=0

    for subagent in "${SUBAGENTS[@]}"; do
        local file_path="$AGENTS_DIR/$subagent"

        if [[ ! -f "$file_path" ]]; then
            continue
        fi

        # Check for Read(file_path="devforgeai/specs/context/source-tree.md") in validation section
        if grep -qE 'Read\(file_path.*source-tree\.md' "$file_path" 2>/dev/null; then
            echo "  OK: $subagent reads source-tree.md"
        else
            echo "  MISSING: $subagent does not read source-tree.md in validation"
            ((failures++))
        fi
    done

    if [[ $failures -eq 0 ]]; then
        log_pass "All subagents read source-tree.md in Pre-Generation Validation"
    else
        log_fail "$failures subagents do not read source-tree.md in Pre-Generation Validation"
    fi
}

# ============================================================================
# AC#4: Apply Pattern to Each Subagent (HALT Pattern)
# ============================================================================

test_ac4_halt_pattern_present() {
    log_test_start "AC#4: Verify HALT pattern present in validation section"

    local missing=0

    for subagent in "${SUBAGENTS[@]}"; do
        local file_path="$AGENTS_DIR/$subagent"

        if [[ ! -f "$file_path" ]]; then
            continue
        fi

        # Check for HALT pattern with source-tree constraint violation message
        if grep -qiE "HALT.*validation|SOURCE-TREE.*CONSTRAINT.*VIOLATION" "$file_path" 2>/dev/null; then
            echo "  OK: $subagent has HALT pattern"
        else
            echo "  MISSING: $subagent lacks HALT pattern"
            ((missing++))
        fi
    done

    if [[ $missing -eq 0 ]]; then
        log_pass "All subagents have HALT pattern in validation section"
    else
        log_fail "$missing subagents missing HALT pattern"
    fi
}

test_ac4_constraint_violation_error_message() {
    log_test_start "AC#4: Verify constraint violation error message format"

    # Expected pattern per AC#3 template:
    # SOURCE-TREE CONSTRAINT VIOLATION
    # Expected directory: {expected_directory}
    # Attempted location: {file_path}

    local failures=0

    for subagent in "${SUBAGENTS[@]}"; do
        local file_path="$AGENTS_DIR/$subagent"

        if [[ ! -f "$file_path" ]]; then
            continue
        fi

        # Check for complete error message components
        local has_violation_header=false
        local has_expected_dir=false
        local has_attempted_loc=false

        grep -qi "SOURCE-TREE.*CONSTRAINT.*VIOLATION\|CONSTRAINT.*VIOLATION" "$file_path" && has_violation_header=true
        grep -qi "Expected.*director" "$file_path" && has_expected_dir=true
        grep -qi "Attempted.*location\|Attempted.*path" "$file_path" && has_attempted_loc=true

        if $has_violation_header && $has_expected_dir && $has_attempted_loc; then
            echo "  OK: $subagent has complete error message format"
        else
            echo "  INCOMPLETE: $subagent error message missing components"
            ((failures++))
        fi
    done

    if [[ $failures -eq 0 ]]; then
        log_pass "All subagents have complete constraint violation error message"
    else
        log_fail "$failures subagents have incomplete error message format"
    fi
}

test_ac4_customized_output_type() {
    log_test_start "AC#4: Verify validation pattern customized for each subagent's output type"

    # Each subagent should have customized validation for its output type
    # Per AC#4 table:
    #   story-requirements-analyst: devforgeai/specs/Stories/
    #   api-designer: devforgeai/specs/analysis/ or docs/api/
    #   documentation-writer: docs/ or .claude/memory/
    #   refactoring-specialist: Per source-tree.md module patterns
    #   backend-architect: Per source-tree.md module patterns
    #   frontend-developer: Per source-tree.md frontend patterns
    #   agent-generator: .claude/agents/

    declare -A EXPECTED_PATTERNS
    EXPECTED_PATTERNS["story-requirements-analyst.md"]="devforgeai/specs/Stories"
    EXPECTED_PATTERNS["api-designer.md"]="devforgeai/specs/analysis|docs/api"
    EXPECTED_PATTERNS["documentation-writer.md"]="docs/|\.claude/memory"
    EXPECTED_PATTERNS["refactoring-specialist.md"]="source-tree"
    EXPECTED_PATTERNS["backend-architect.md"]="source-tree"
    EXPECTED_PATTERNS["frontend-developer.md"]="source-tree|frontend"
    EXPECTED_PATTERNS["agent-generator.md"]=".claude/agents"

    local failures=0

    for subagent in "${SUBAGENTS[@]}"; do
        local file_path="$AGENTS_DIR/$subagent"
        local expected_pattern="${EXPECTED_PATTERNS[$subagent]}"

        if [[ ! -f "$file_path" ]]; then
            continue
        fi

        # Check if validation section mentions the expected pattern
        if grep -qiE "$expected_pattern" "$file_path" 2>/dev/null; then
            echo "  OK: $subagent has customized output type validation"
        else
            echo "  MISSING: $subagent lacks customized output type (expected: $expected_pattern)"
            ((failures++))
        fi
    done

    if [[ $failures -eq 0 ]]; then
        log_pass "All subagents have customized output type validation"
    else
        log_fail "$failures subagents missing customized output type validation"
    fi
}

# ============================================================================
# AC#5: Verify No Existing Subagents Modified Incorrectly
# ============================================================================

test_ac5_yaml_frontmatter_valid() {
    log_test_start "AC#5: Verify YAML frontmatter remains valid"

    local failures=0

    for subagent in "${SUBAGENTS[@]}"; do
        local file_path="$AGENTS_DIR/$subagent"

        if [[ ! -f "$file_path" ]]; then
            continue
        fi

        # Check YAML frontmatter structure (starts with ---, has name:, description:, ends with ---)
        if head -20 "$file_path" | grep -qE "^---$" && \
           head -20 "$file_path" | grep -qE "^name:" && \
           head -20 "$file_path" | grep -qE "^description:"; then
            echo "  OK: $subagent has valid YAML frontmatter"
        else
            echo "  INVALID: $subagent has broken YAML frontmatter"
            ((failures++))
        fi
    done

    if [[ $failures -eq 0 ]]; then
        log_pass "All subagents have valid YAML frontmatter"
    else
        log_fail "$failures subagents have invalid YAML frontmatter"
    fi
}

test_ac5_tools_field_intact() {
    log_test_start "AC#5: Verify tools field not corrupted"

    # Verify each subagent still has its original tools (at least one key tool)
    # Note: tools field format is `tools: [Tool1, Tool2]` or `tools: Tool1, Tool2`
    declare -A KEY_TOOLS
    KEY_TOOLS["story-requirements-analyst.md"]="Read"
    KEY_TOOLS["api-designer.md"]="Write"
    KEY_TOOLS["documentation-writer.md"]="Write"
    KEY_TOOLS["refactoring-specialist.md"]="Edit"
    KEY_TOOLS["backend-architect.md"]="Write"
    KEY_TOOLS["frontend-developer.md"]="Write"
    KEY_TOOLS["agent-generator.md"]="Write"

    local failures=0

    for subagent in "${SUBAGENTS[@]}"; do
        local file_path="$AGENTS_DIR/$subagent"
        local key_tool="${KEY_TOOLS[$subagent]}"

        if [[ ! -f "$file_path" ]]; then
            continue
        fi

        # Check if tools field exists and contains at least the key tool
        if head -15 "$file_path" | grep -qE "^tools:.*$key_tool"; then
            echo "  OK: $subagent has expected tools"
        else
            echo "  CORRUPTED: $subagent tools field may be corrupted (missing $key_tool)"
            ((failures++))
        fi
    done

    if [[ $failures -eq 0 ]]; then
        log_pass "All subagents have intact tools field"
    else
        log_fail "$failures subagents may have corrupted tools field"
    fi
}

test_ac5_existing_sections_preserved() {
    log_test_start "AC#5: Verify existing sections preserved (Purpose, Workflow, Success Criteria)"

    local failures=0

    for subagent in "${SUBAGENTS[@]}"; do
        local file_path="$AGENTS_DIR/$subagent"

        if [[ ! -f "$file_path" ]]; then
            continue
        fi

        # Check for standard sections that should exist
        local has_purpose=false
        local has_workflow=false

        grep -qiE "^#+.*Purpose|^## Purpose" "$file_path" && has_purpose=true
        grep -qiE "^#+.*Workflow|^## Workflow" "$file_path" && has_workflow=true

        if $has_purpose && $has_workflow; then
            echo "  OK: $subagent has core sections preserved"
        else
            echo "  BROKEN: $subagent missing core sections (Purpose: $has_purpose, Workflow: $has_workflow)"
            ((failures++))
        fi
    done

    if [[ $failures -eq 0 ]]; then
        log_pass "All subagents have existing sections preserved"
    else
        log_fail "$failures subagents have missing core sections"
    fi
}

# ============================================================================
# NFR-002: Verify Pattern Consistency Across All Subagents
# ============================================================================

test_nfr002_pattern_consistency() {
    log_test_start "NFR-002: Verify validation pattern consistent across all subagents"

    # All subagents should have the same Pre-Generation Validation template structure
    local template_elements=(
        "Pre-Generation Validation"
        "source-tree.md"
        "HALT"
        "Expected.*director"
        "Attempted.*location|Attempted.*path"
    )

    local inconsistencies=0

    for subagent in "${SUBAGENTS[@]}"; do
        local file_path="$AGENTS_DIR/$subagent"
        local missing_elements=0

        if [[ ! -f "$file_path" ]]; then
            continue
        fi

        for element in "${template_elements[@]}"; do
            if ! grep -qiE "$element" "$file_path" 2>/dev/null; then
                ((missing_elements++))
            fi
        done

        if [[ $missing_elements -gt 0 ]]; then
            echo "  INCONSISTENT: $subagent missing $missing_elements template elements"
            ((inconsistencies++))
        else
            echo "  OK: $subagent has all template elements"
        fi
    done

    if [[ $inconsistencies -eq 0 ]]; then
        log_pass "All subagents have consistent validation pattern"
    else
        log_fail "$inconsistencies subagents have inconsistent validation pattern"
    fi
}

# ============================================================================
# BR-001: All file-generation subagents MUST validate against source-tree.md
# ============================================================================

test_br001_all_file_generators_validate() {
    log_test_start "BR-001: All file-generation subagents validate against source-tree.md"

    local non_compliant=0

    for subagent in "${SUBAGENTS[@]}"; do
        local file_path="$AGENTS_DIR/$subagent"

        if [[ ! -f "$file_path" ]]; then
            continue
        fi

        # Check for complete validation chain:
        # 1. Reads source-tree.md
        # 2. Has validation section
        # 3. Has HALT on violation
        local reads_source_tree=false
        local has_validation=false
        local has_halt=false

        grep -qE 'Read\(file_path.*source-tree\.md' "$file_path" && reads_source_tree=true
        grep -qiE "Pre-Generation Validation" "$file_path" && has_validation=true
        grep -qiE "HALT" "$file_path" && has_halt=true

        if $reads_source_tree && $has_validation && $has_halt; then
            echo "  COMPLIANT: $subagent validates against source-tree.md"
        else
            echo "  NON-COMPLIANT: $subagent (reads: $reads_source_tree, validation: $has_validation, halt: $has_halt)"
            ((non_compliant++))
        fi
    done

    if [[ $non_compliant -eq 0 ]]; then
        log_pass "All file-generation subagents validate against source-tree.md"
    else
        log_fail "$non_compliant subagents do not validate against source-tree.md"
    fi
}

# ============================================================================
# Test Runner
# ============================================================================

run_all_tests() {
    echo "============================================================"
    echo "STORY-204: File-Generation Subagents source-tree.md Validation"
    echo "============================================================"
    echo ""
    echo "TDD Phase: RED (Tests should FAIL initially)"
    echo "Test Date: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Agents Directory: $AGENTS_DIR"
    echo ""
    echo "Target Subagents (7):"
    for subagent in "${SUBAGENTS[@]}"; do
        echo "  - $subagent"
    done
    echo ""
    echo "============================================================"
    echo "Running Tests..."
    echo "============================================================"

    # AC#1 Tests
    test_ac1_subagent_audit_count
    test_ac1_subagent_list_complete

    # AC#2 Tests
    test_ac2_source_tree_in_references
    test_ac2_source_tree_reference_format

    # AC#3 Tests
    test_ac3_pre_generation_validation_section_exists
    test_ac3_pre_generation_validation_reads_source_tree

    # AC#4 Tests
    test_ac4_halt_pattern_present
    test_ac4_constraint_violation_error_message
    test_ac4_customized_output_type

    # AC#5 Tests
    test_ac5_yaml_frontmatter_valid
    test_ac5_tools_field_intact
    test_ac5_existing_sections_preserved

    # NFR-002 Test
    test_nfr002_pattern_consistency

    # BR-001 Test
    test_br001_all_file_generators_validate

    echo ""
    echo "============================================================"
    echo "Test Summary"
    echo "============================================================"
    echo ""
    echo -e "Total Tests: $TOTAL_TESTS"
    echo -e "Passed: ${GREEN}$PASS_COUNT${NC}"
    echo -e "Failed: ${RED}$FAIL_COUNT${NC}"
    echo ""

    if [[ ${#FAILED_TESTS[@]} -gt 0 ]]; then
        echo "Failed Tests:"
        for test in "${FAILED_TESTS[@]}"; do
            echo -e "  ${RED}- $test${NC}"
        done
        echo ""
    fi

    if [[ $FAIL_COUNT -eq 0 ]]; then
        echo -e "${GREEN}ALL TESTS PASSED!${NC}"
        echo "TDD Phase: GREEN (Ready to proceed)"
        exit 0
    else
        echo -e "${RED}$FAIL_COUNT TESTS FAILED${NC}"
        echo "TDD Phase: RED (Implementation needed)"
        exit 1
    fi
}

# Run all tests
run_all_tests
