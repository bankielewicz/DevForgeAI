#!/bin/bash
# =============================================================================
# STORY-214: Mandatory Deviation Consent Protocol - AC Verification Tests
# =============================================================================
#
# Purpose: Verify documentation structure in SKILL.md per acceptance criteria
# Test Type: TDD Red Phase - Structural validation (grep-based)
#
# Acceptance Criteria Covered:
#   AC#1: Protocol section header exists
#   AC#2: AskUserQuestion template with three options documented
#   AC#3: Subagent omission deviation documented
#   AC#4: Documentation requirements for approved deviations
#   AC#5: RCA recommendation for deviations (optional, not blocking)
#
# Technical Specification Requirements:
#   DOC-001: Section header "## Workflow Deviation Protocol"
#   DOC-002: Three deviation types (phase skipping, subagent omission, out-of-sequence)
#   DOC-003: AskUserQuestion pattern present
#   DOC-004: "Follow workflow" option processing
#   DOC-005: "Skip with documentation" option processing
#   DOC-006: "User override" option processing
#   BR-001: Protocol mandates AskUserQuestion
#   BR-002: Timestamp requirement documented
#   NFR-001: Uses HALT terminology from architecture-constraints.md
#   NFR-002: Section under 100 lines
#
# =============================================================================

# Note: Do NOT use set -e - we want all tests to run even if some fail

# Configuration
SKILL_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-development/SKILL.md"
TEST_RESULTS_FILE="/mnt/c/Projects/DevForgeAI2/tests/STORY-214/test-results.log"

# Use files to track counts (avoid subshell variable scope issues)
PASS_COUNT_FILE=$(mktemp)
FAIL_COUNT_FILE=$(mktemp)
echo "0" > "$PASS_COUNT_FILE"
echo "0" > "$FAIL_COUNT_FILE"

# Cleanup temp files at end (no trap - handle manually)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initialize test results log
echo "STORY-214 Test Results - $(date)" > "$TEST_RESULTS_FILE"
echo "============================================" >> "$TEST_RESULTS_FILE"

# Helper function to record test result
record_test() {
    local test_id="$1"
    local test_name="$2"
    local status="$3"
    local details="$4"

    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}[PASS]${NC} $test_id: $test_name"
        echo "[PASS] $test_id: $test_name" >> "$TEST_RESULTS_FILE"
        echo $(( $(cat "$PASS_COUNT_FILE") + 1 )) > "$PASS_COUNT_FILE"
    else
        echo -e "${RED}[FAIL]${NC} $test_id: $test_name"
        echo "[FAIL] $test_id: $test_name" >> "$TEST_RESULTS_FILE"
        echo "       Details: $details" >> "$TEST_RESULTS_FILE"
        echo $(( $(cat "$FAIL_COUNT_FILE") + 1 )) > "$FAIL_COUNT_FILE"
    fi
}

# =============================================================================
# AC#1: Workflow Deviation Protocol Section
# =============================================================================
echo ""
echo "=== AC#1: Workflow Deviation Protocol Section ==="

# TEST-001: DOC-001 - Protocol section header exists
test_doc_001() {
    if grep -q "^## Workflow Deviation Protocol" "$SKILL_FILE"; then
        record_test "TEST-001" "DOC-001: Protocol section header exists" "PASS" ""
    else
        record_test "TEST-001" "DOC-001: Protocol section header exists" "FAIL" \
            "Expected '## Workflow Deviation Protocol' header not found in SKILL.md"
    fi
}

# =============================================================================
# AC#2: AskUserQuestion Enforcement for Phase Skipping
# =============================================================================
echo ""
echo "=== AC#2: AskUserQuestion Enforcement for Phase Skipping ==="

# TEST-002: DOC-003 - AskUserQuestion pattern present in deviation section
test_doc_003() {
    if grep -q "AskUserQuestion" "$SKILL_FILE" && \
       grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -q "AskUserQuestion"; then
        record_test "TEST-002" "DOC-003: AskUserQuestion pattern in deviation section" "PASS" ""
    else
        record_test "TEST-002" "DOC-003: AskUserQuestion pattern in deviation section" "FAIL" \
            "AskUserQuestion not found within Workflow Deviation Protocol section"
    fi
}

# TEST-003: Option "Follow workflow" documented
test_option_follow_workflow() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "Follow workflow"; then
        record_test "TEST-003" "DOC-004: 'Follow workflow' option documented" "PASS" ""
    else
        record_test "TEST-003" "DOC-004: 'Follow workflow' option documented" "FAIL" \
            "'Follow workflow' option not found in deviation protocol section"
    fi
}

# TEST-004: Option "Skip with documentation" documented
test_option_skip_with_doc() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "Skip with documentation"; then
        record_test "TEST-004" "DOC-005: 'Skip with documentation' option documented" "PASS" ""
    else
        record_test "TEST-004" "DOC-005: 'Skip with documentation' option documented" "FAIL" \
            "'Skip with documentation' option not found in deviation protocol section"
    fi
}

# TEST-005: Option "User override" documented
test_option_user_override() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "User override"; then
        record_test "TEST-005" "DOC-006: 'User override' option documented" "PASS" ""
    else
        record_test "TEST-005" "DOC-006: 'User override' option documented" "FAIL" \
            "'User override' option not found in deviation protocol section"
    fi
}

# =============================================================================
# AC#3: AskUserQuestion Enforcement for Subagent Omission
# =============================================================================
echo ""
echo "=== AC#3: Subagent Omission Deviation ==="

# TEST-006: DOC-002 - Deviation types documented (phase skipping)
test_deviation_type_phase() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "phase skip"; then
        record_test "TEST-006" "DOC-002a: Phase skipping deviation type documented" "PASS" ""
    else
        record_test "TEST-006" "DOC-002a: Phase skipping deviation type documented" "FAIL" \
            "Phase skipping deviation type not found in protocol section"
    fi
}

# TEST-007: DOC-002 - Deviation types documented (subagent omission)
test_deviation_type_subagent() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "subagent omission\|subagent skip"; then
        record_test "TEST-007" "DOC-002b: Subagent omission deviation type documented" "PASS" ""
    else
        record_test "TEST-007" "DOC-002b: Subagent omission deviation type documented" "FAIL" \
            "Subagent omission deviation type not found in protocol section"
    fi
}

# TEST-008: DOC-002 - Deviation types documented (out-of-sequence)
test_deviation_type_sequence() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "out-of-sequence\|sequence\|order"; then
        record_test "TEST-008" "DOC-002c: Out-of-sequence deviation type documented" "PASS" ""
    else
        record_test "TEST-008" "DOC-002c: Out-of-sequence deviation type documented" "FAIL" \
            "Out-of-sequence deviation type not found in protocol section"
    fi
}

# TEST-009: MANDATORY distinction for subagent omission
test_mandatory_subagent() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "MANDATORY\|mandatory"; then
        record_test "TEST-009" "AC#3: MANDATORY distinction for subagent omission" "PASS" ""
    else
        record_test "TEST-009" "AC#3: MANDATORY distinction for subagent omission" "FAIL" \
            "MANDATORY terminology not found in deviation protocol section"
    fi
}

# =============================================================================
# AC#4: Documentation Requirement for Approved Deviations
# =============================================================================
echo ""
echo "=== AC#4: Documentation Requirements for Approved Deviations ==="

# TEST-010: BR-002 - Timestamp requirement documented
test_timestamp_requirement() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "timestamp"; then
        record_test "TEST-010" "BR-002: Timestamp requirement documented" "PASS" ""
    else
        record_test "TEST-010" "BR-002: Timestamp requirement documented" "FAIL" \
            "Timestamp requirement not found in deviation protocol section"
    fi
}

# TEST-011: Implementation Notes section referenced
test_implementation_notes() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "Implementation Notes"; then
        record_test "TEST-011" "AC#4: Implementation Notes section referenced" "PASS" ""
    else
        record_test "TEST-011" "AC#4: Implementation Notes section referenced" "FAIL" \
            "Implementation Notes section not referenced in deviation protocol"
    fi
}

# TEST-012: Story file update requirement
test_story_file_update() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "story file\|story.md"; then
        record_test "TEST-012" "AC#4: Story file update requirement documented" "PASS" ""
    else
        record_test "TEST-012" "AC#4: Story file update requirement documented" "FAIL" \
            "Story file update requirement not found in protocol section"
    fi
}

# =============================================================================
# AC#5: RCA Trigger for Documented Deviations
# =============================================================================
echo ""
echo "=== AC#5: RCA Recommendation for Deviations ==="

# TEST-013: RCA recommendation documented
test_rca_recommendation() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "rca\|root cause"; then
        record_test "TEST-013" "AC#5: RCA recommendation documented" "PASS" ""
    else
        record_test "TEST-013" "AC#5: RCA recommendation documented" "FAIL" \
            "RCA recommendation not found in deviation protocol section"
    fi
}

# TEST-014: Optional/not blocking nature clarified
test_rca_optional() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "optional\|not blocking\|recommended"; then
        record_test "TEST-014" "AC#5: Optional nature of RCA clarified" "PASS" ""
    else
        record_test "TEST-014" "AC#5: Optional nature of RCA clarified" "FAIL" \
            "Optional/not blocking nature of RCA not clarified in protocol section"
    fi
}

# =============================================================================
# Non-Functional Requirements
# =============================================================================
echo ""
echo "=== Non-Functional Requirements ==="

# TEST-015: NFR-001 - HALT terminology used
test_halt_terminology() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "HALT"; then
        record_test "TEST-015" "NFR-001: HALT terminology from architecture-constraints.md" "PASS" ""
    else
        record_test "TEST-015" "NFR-001: HALT terminology from architecture-constraints.md" "FAIL" \
            "HALT terminology not found in deviation protocol section"
    fi
}

# TEST-016: NFR-002 - Section under 100 lines
test_section_line_count() {
    # Extract section and count lines (from header to next ## or end)
    local section_start
    section_start=$(grep -n "^## Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | cut -d: -f1)

    if [ -z "$section_start" ]; then
        record_test "TEST-016" "NFR-002: Section under 100 lines" "FAIL" \
            "Cannot check line count - section header not found"
        return
    fi

    # Find next ## section header after deviation protocol
    local next_section
    next_section=$(tail -n +"$((section_start + 1))" "$SKILL_FILE" | grep -n "^## " | head -1 | cut -d: -f1)

    local line_count
    if [ -z "$next_section" ]; then
        # Section goes to end of file
        local total_lines
        total_lines=$(wc -l < "$SKILL_FILE")
        line_count=$((total_lines - section_start + 1))
    else
        line_count=$next_section
    fi

    if [ "$line_count" -lt 100 ]; then
        record_test "TEST-016" "NFR-002: Section under 100 lines (actual: $line_count)" "PASS" ""
    else
        record_test "TEST-016" "NFR-002: Section under 100 lines" "FAIL" \
            "Section is $line_count lines (exceeds 100 line limit)"
    fi
}

# TEST-017: BR-001 - Protocol mandates AskUserQuestion before any deviation
test_mandatory_askuser() {
    if grep -A 100 "Workflow Deviation Protocol" "$SKILL_FILE" 2>/dev/null | grep -qi "MUST.*AskUserQuestion\|AskUserQuestion.*MUST\|mandatory.*AskUserQuestion\|AskUserQuestion.*mandatory"; then
        record_test "TEST-017" "BR-001: Protocol mandates AskUserQuestion" "PASS" ""
    else
        record_test "TEST-017" "BR-001: Protocol mandates AskUserQuestion" "FAIL" \
            "Mandatory AskUserQuestion requirement not clearly stated"
    fi
}

# =============================================================================
# Execute All Tests
# =============================================================================
echo ""
echo "============================================"
echo "Executing STORY-214 Test Suite"
echo "============================================"
echo ""

# Run all tests
test_doc_001
test_doc_003
test_option_follow_workflow
test_option_skip_with_doc
test_option_user_override
test_deviation_type_phase
test_deviation_type_subagent
test_deviation_type_sequence
test_mandatory_subagent
test_timestamp_requirement
test_implementation_notes
test_story_file_update
test_rca_recommendation
test_rca_optional
test_halt_terminology
test_section_line_count
test_mandatory_askuser

# =============================================================================
# Summary
# =============================================================================
PASS_COUNT=$(cat "$PASS_COUNT_FILE" | tr -d '\n')
FAIL_COUNT=$(cat "$FAIL_COUNT_FILE" | tr -d '\n')
TOTAL=$((PASS_COUNT + FAIL_COUNT))

echo ""
echo "============================================"
echo "Test Summary"
echo "============================================"
echo -e "Passed: ${GREEN}${PASS_COUNT}${NC}"
echo -e "Failed: ${RED}${FAIL_COUNT}${NC}"
echo "Total:  ${TOTAL}"
echo ""

# Write summary to log
echo "" >> "$TEST_RESULTS_FILE"
echo "============================================" >> "$TEST_RESULTS_FILE"
echo "Summary: $PASS_COUNT passed, $FAIL_COUNT failed" >> "$TEST_RESULTS_FILE"

# Cleanup temp files
rm -f "$PASS_COUNT_FILE" "$FAIL_COUNT_FILE"

# Exit with appropriate code for TDD Red phase
if [ "${FAIL_COUNT}" -gt 0 ]; then
    echo -e "${YELLOW}TDD Red Phase: Tests failing as expected (no implementation yet)${NC}"
    exit 1
else
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
fi
