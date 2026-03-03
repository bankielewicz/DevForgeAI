#!/bin/bash
# Test Suite: STORY-283 - Story Creation Automation for AC-TechSpec Traceability
# TDD Phase: RED (all tests should FAIL until implementation)
# Implementation Type: Slash Command / Skill modification (.md files)

# Configuration
TARGET_FILE=".claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
STORY_DIR="devforgeai/specs/Stories"
PASS_COUNT=0
FAIL_COUNT=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test utilities
pass_test() {
    echo -e "${GREEN}PASS${NC}: $1"
    PASS_COUNT=$((PASS_COUNT + 1))
}

fail_test() {
    echo -e "${RED}FAIL${NC}: $1"
    FAIL_COUNT=$((FAIL_COUNT + 1))
}

skip_test() {
    echo -e "${YELLOW}SKIP${NC}: $1"
}

# Header
echo "=============================================="
echo "  STORY-283: AC-TechSpec Traceability Tests"
echo "  TDD Phase: RED (expecting failures)"
echo "=============================================="
echo ""
echo "Target: $TARGET_FILE"
echo ""

# Verify target file exists
if [[ ! -f "$TARGET_FILE" ]]; then
    echo -e "${RED}ERROR${NC}: Target file not found: $TARGET_FILE"
    exit 1
fi

echo "--- AC#1: Auto-Generation During Story Creation ---"
echo ""

# Test 1.1: Keyword extraction section exists
test_ac1_keyword_extraction() {
    if grep -qiE "(keyword|extract).*(AC|acceptance.criteria).*(analysis|extract|parse)" "$TARGET_FILE" 2>/dev/null || \
       grep -qiE "AC.*(keyword|extract)" "$TARGET_FILE" 2>/dev/null; then
        pass_test "test_ac1_keyword_extraction: AC keyword extraction section found"
    else
        fail_test "test_ac1_keyword_extraction: No AC keyword extraction logic found"
    fi
}

# Test 1.2: implements_ac auto-population logic
test_ac1_implements_ac_auto_population() {
    if grep -qiE "(auto|automatic).*(implements_ac|traceability)" "$TARGET_FILE" 2>/dev/null || \
       grep -qiE "implements_ac.*(auto|generate|populate)" "$TARGET_FILE" 2>/dev/null; then
        pass_test "test_ac1_implements_ac_auto_population: Auto-population logic found"
    else
        fail_test "test_ac1_implements_ac_auto_population: No auto-population logic found"
    fi
}

# Test 1.3: Semantic analysis algorithm
test_ac1_semantic_analysis() {
    if grep -qiE "(semantic|similarity|match).*(AC|acceptance|criteria|COMP)" "$TARGET_FILE" 2>/dev/null; then
        pass_test "test_ac1_semantic_analysis: Semantic matching algorithm found"
    else
        fail_test "test_ac1_semantic_analysis: No semantic matching algorithm found"
    fi
}

# Test 1.4: SVC-001 and SVC-002 implementation
test_ac1_svc_implementation() {
    local svc001_found=false
    local svc002_found=false

    if grep -qiE "SVC-001|analyze.*AC.*content.*keyword" "$TARGET_FILE" 2>/dev/null; then
        svc001_found=true
    fi

    if grep -qiE "SVC-002|match.*COMP.*description.*AC" "$TARGET_FILE" 2>/dev/null; then
        svc002_found=true
    fi

    if [[ "$svc001_found" == "true" ]] && [[ "$svc002_found" == "true" ]]; then
        pass_test "test_ac1_svc_implementation: SVC-001 and SVC-002 implemented"
    else
        fail_test "test_ac1_svc_implementation: SVC-001/SVC-002 not implemented (SVC-001: $svc001_found, SVC-002: $svc002_found)"
    fi
}

echo ""
echo "--- AC#2: Cross-Reference with AC Section ---"
echo ""

# Test 2.1: Valid AC ID validation
test_ac2_valid_ac_id_validation() {
    if grep -qiE "(valid|verify|check|cross-reference).*(AC.*ID|implements_ac)" "$TARGET_FILE" 2>/dev/null || \
       grep -qiE "AC.*(valid|exist|reference)" "$TARGET_FILE" 2>/dev/null; then
        pass_test "test_ac2_valid_ac_id_validation: AC ID validation logic found"
    else
        fail_test "test_ac2_valid_ac_id_validation: No AC ID validation logic found"
    fi
}

# Test 2.2: Invalid AC ID rejection
test_ac2_invalid_ac_id_rejection() {
    if grep -qiE "(invalid|reject|error|warn).*(AC.*ID|implements_ac)" "$TARGET_FILE" 2>/dev/null; then
        pass_test "test_ac2_invalid_ac_id_rejection: Invalid AC ID handling found"
    else
        fail_test "test_ac2_invalid_ac_id_rejection: No invalid AC ID handling found"
    fi
}

# Test 2.3: SVC-003 implementation
test_ac2_svc003_implementation() {
    if grep -qiE "SVC-003|validate.*link.*AC|AC.*section.*valid" "$TARGET_FILE" 2>/dev/null; then
        pass_test "test_ac2_svc003_implementation: SVC-003 implemented"
    else
        fail_test "test_ac2_svc003_implementation: SVC-003 not implemented"
    fi
}

echo ""
echo "--- AC#3: Warning for Unlinked COMPs ---"
echo ""

# Test 3.1: Unlinked COMP detection
test_ac3_unlinked_comp_detection() {
    if grep -qiE "(unlinked|empty|missing).*(implements_ac|traceability|COMP)" "$TARGET_FILE" 2>/dev/null; then
        pass_test "test_ac3_unlinked_comp_detection: Unlinked COMP detection found"
    else
        fail_test "test_ac3_unlinked_comp_detection: No unlinked COMP detection found"
    fi
}

# Test 3.2: Warning message format
test_ac3_warning_message_format() {
    if grep -qE "COMP-.*has no AC traceability.*consider adding implements_ac" "$TARGET_FILE" 2>/dev/null || \
       grep -qiE "warn.*COMP.*traceability" "$TARGET_FILE" 2>/dev/null; then
        pass_test "test_ac3_warning_message_format: Warning message format found"
    else
        fail_test "test_ac3_warning_message_format: Warning message format not found"
    fi
}

# Test 3.3: SVC-004 implementation
test_ac3_svc004_implementation() {
    if grep -qiE "SVC-004|generate.*warning.*unlinked|warn.*COMP.*no.*link" "$TARGET_FILE" 2>/dev/null; then
        pass_test "test_ac3_svc004_implementation: SVC-004 implemented"
    else
        fail_test "test_ac3_svc004_implementation: SVC-004 not implemented"
    fi
}

echo ""
echo "--- AC#4: User Override Option ---"
echo ""

# Test 4.1: File format is editable (markdown)
test_ac4_file_format_editable() {
    # Check that story files are text/markdown format
    if [[ -d "$STORY_DIR" ]]; then
        local story_files
        story_files=$(find "$STORY_DIR" -name "*.story.md" -type f 2>/dev/null | head -5)

        if [[ -n "$story_files" ]]; then
            local all_text=true
            while IFS= read -r sf; do
                if ! file "$sf" | grep -qi "text"; then
                    all_text=false
                    break
                fi
            done <<< "$story_files"

            if [[ "$all_text" == "true" ]]; then
                pass_test "test_ac4_file_format_editable: Story files are editable text format"
            else
                fail_test "test_ac4_file_format_editable: Some story files are not text format"
            fi
        else
            skip_test "test_ac4_file_format_editable: No story files found to verify"
        fi
    else
        skip_test "test_ac4_file_format_editable: Story directory not found"
    fi
}

# Test 4.2: No readonly lock on implements_ac
test_ac4_no_readonly_lock() {
    if grep -qiE "(readonly|locked|immutable).*implements_ac" "$TARGET_FILE" 2>/dev/null; then
        fail_test "test_ac4_no_readonly_lock: Found lock mechanism on implements_ac"
    else
        pass_test "test_ac4_no_readonly_lock: No lock mechanism on implements_ac (editable)"
    fi
}

echo ""
echo "--- Business Rules ---"
echo ""

# Test BR-001: Best-effort generation
test_br001_best_effort() {
    if grep -qiE "(best.effort|uncertain|low.confidence).*(empty|skip)" "$TARGET_FILE" 2>/dev/null || \
       grep -qiE "empty.*(uncertain|low|unknown)" "$TARGET_FILE" 2>/dev/null; then
        pass_test "test_br001_best_effort: Best-effort behavior documented"
    else
        fail_test "test_br001_best_effort: Best-effort behavior not documented"
    fi
}

# Test BR-002: User override preserved
test_br002_user_override() {
    if grep -qiE "(preserve|maintain|respect).*(manual|user|override)" "$TARGET_FILE" 2>/dev/null; then
        pass_test "test_br002_user_override: User override preservation documented"
    else
        fail_test "test_br002_user_override: User override preservation not documented"
    fi
}

# Run all tests
echo "Running tests..."
echo ""

test_ac1_keyword_extraction
test_ac1_implements_ac_auto_population
test_ac1_semantic_analysis
test_ac1_svc_implementation

test_ac2_valid_ac_id_validation
test_ac2_invalid_ac_id_rejection
test_ac2_svc003_implementation

test_ac3_unlinked_comp_detection
test_ac3_warning_message_format
test_ac3_svc004_implementation

test_ac4_file_format_editable
test_ac4_no_readonly_lock

test_br001_best_effort
test_br002_user_override

# Summary
echo ""
echo "=============================================="
echo "  Test Summary"
echo "=============================================="
echo -e "  ${GREEN}PASS${NC}: $PASS_COUNT"
echo -e "  ${RED}FAIL${NC}: $FAIL_COUNT"
TOTAL=$((PASS_COUNT + FAIL_COUNT))
echo "  TOTAL: $TOTAL"
echo ""

if [[ $FAIL_COUNT -gt 0 ]]; then
    echo -e "${RED}TDD RED PHASE: Tests failing as expected${NC}"
    echo "Implementation pending for STORY-283"
    exit 1
else
    echo -e "${GREEN}ALL TESTS PASSING${NC}"
    echo "Ready for refactoring phase"
    exit 0
fi
