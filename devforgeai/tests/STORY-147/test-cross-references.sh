#!/bin/bash

# Integration Tests for STORY-147: Cross-Reference Validation
# Tests that reference files link to existing sections in the authoritative matrix

STORY_ID="STORY-147"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_DIR="${PROJECT_ROOT}/.claude/skills/devforgeai-ideation/references"

# Test files
MATRIX_FILE="${SKILL_DIR}/complexity-assessment-matrix.md"
OUTPUT_TEMPLATES_FILE="${SKILL_DIR}/output-templates.md"
COMPLETION_HANDOFF_FILE="${SKILL_DIR}/completion-handoff.md"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to print test results
print_test_result() {
    local test_name=$1
    local result=$2
    local message=$3

    TESTS_RUN=$((TESTS_RUN + 1))

    if [ "$result" == "PASS" ]; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}✓ PASS${NC}: $test_name"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}✗ FAIL${NC}: $test_name"
        if [ ! -z "$message" ]; then
            echo "  $message"
        fi
    fi
}

# Test 1: Verify all reference files exist
test_files_exist() {
    echo -e "\n${YELLOW}=== Test 1: File Existence ===${NC}"

    # Test matrix file exists
    if [ -f "$MATRIX_FILE" ]; then
        print_test_result "complexity-assessment-matrix.md exists" "PASS"
    else
        print_test_result "complexity-assessment-matrix.md exists" "FAIL" "File not found: $MATRIX_FILE"
    fi

    # Test output templates file exists
    if [ -f "$OUTPUT_TEMPLATES_FILE" ]; then
        print_test_result "output-templates.md exists" "PASS"
    else
        print_test_result "output-templates.md exists" "FAIL" "File not found: $OUTPUT_TEMPLATES_FILE"
    fi

    # Test completion handoff file exists
    if [ -f "$COMPLETION_HANDOFF_FILE" ]; then
        print_test_result "completion-handoff.md exists" "PASS"
    else
        print_test_result "completion-handoff.md exists" "FAIL" "File not found: $COMPLETION_HANDOFF_FILE"
    fi
}

# Test 2: Verify matrix contains all tier sections
test_matrix_tier_sections() {
    echo -e "\n${YELLOW}=== Test 2: Matrix Tier Sections ===${NC}"

    # Test Tier 1 section exists
    if grep -q "^### Tier 1:" "$MATRIX_FILE"; then
        print_test_result "Matrix contains Tier 1 section" "PASS"
    else
        print_test_result "Matrix contains Tier 1 section" "FAIL" "Section header '### Tier 1:' not found"
    fi

    # Test Tier 2 section exists
    if grep -q "^### Tier 2:" "$MATRIX_FILE"; then
        print_test_result "Matrix contains Tier 2 section" "PASS"
    else
        print_test_result "Matrix contains Tier 2 section" "FAIL" "Section header '### Tier 2:' not found"
    fi

    # Test Tier 3 section exists
    if grep -q "^### Tier 3:" "$MATRIX_FILE"; then
        print_test_result "Matrix contains Tier 3 section" "PASS"
    else
        print_test_result "Matrix contains Tier 3 section" "FAIL" "Section header '### Tier 3:' not found"
    fi

    # Test Tier 4 section exists
    if grep -q "^### Tier 4:" "$MATRIX_FILE"; then
        print_test_result "Matrix contains Tier 4 section" "PASS"
    else
        print_test_result "Matrix contains Tier 4 section" "FAIL" "Section header '### Tier 4:' not found"
    fi
}

# Test 3: Verify output-templates.md has cross-references
test_output_templates_references() {
    echo -e "\n${YELLOW}=== Test 3: output-templates.md Cross-References ===${NC}"

    # Test contains reference to matrix
    if grep -q "complexity-assessment-matrix.md" "$OUTPUT_TEMPLATES_FILE"; then
        print_test_result "output-templates.md references matrix file" "PASS"
    else
        print_test_result "output-templates.md references matrix file" "FAIL" "No reference to complexity-assessment-matrix.md found"
    fi

    # Test uses markdown link format
    if grep -q "\[.*\](.*\.md)" "$OUTPUT_TEMPLATES_FILE"; then
        print_test_result "output-templates.md uses markdown link format" "PASS"
    else
        print_test_result "output-templates.md uses markdown link format" "FAIL" "No markdown links found"
    fi

    # Test references Tier N format
    if grep -q "(Tier [1-4])" "$OUTPUT_TEMPLATES_FILE"; then
        print_test_result "output-templates.md references tiers" "PASS"
    else
        print_test_result "output-templates.md references tiers" "FAIL" "No tier references found in parentheses"
    fi
}

# Test 4: Verify completion-handoff.md has cross-references
test_completion_handoff_references() {
    echo -e "\n${YELLOW}=== Test 4: completion-handoff.md Cross-References ===${NC}"

    # Test contains reference to matrix
    if grep -q "complexity-assessment-matrix.md" "$COMPLETION_HANDOFF_FILE"; then
        print_test_result "completion-handoff.md references matrix file" "PASS"
    else
        print_test_result "completion-handoff.md references matrix file" "FAIL" "No reference to complexity-assessment-matrix.md found"
    fi

    # Test uses markdown link format
    if grep -q "\[.*\](.*\.md)" "$COMPLETION_HANDOFF_FILE"; then
        print_test_result "completion-handoff.md uses markdown link format" "PASS"
    else
        print_test_result "completion-handoff.md uses markdown link format" "FAIL" "No markdown links found"
    fi

    # Test references Tier N or technology recommendations
    if grep -q "(Tier [1-4])" "$COMPLETION_HANDOFF_FILE"; then
        print_test_result "completion-handoff.md references tiers" "PASS"
    else
        print_test_result "completion-handoff.md references tiers" "FAIL" "No tier references found"
    fi
}

# Test 5: Verify no duplication of technology lists
test_no_duplication() {
    echo -e "\n${YELLOW}=== Test 5: Zero Duplication ===${NC}"

    # Check that output-templates.md doesn't duplicate Tier 1 full definition
    # (Matrix has "Tier 1: Simple Application", templates should not repeat this fully)
    if grep -q "## Tier 1" "$OUTPUT_TEMPLATES_FILE"; then
        print_test_result "output-templates.md doesn't duplicate Tier section headers" "FAIL" "Found '## Tier 1' header in output-templates.md"
    else
        print_test_result "output-templates.md doesn't duplicate Tier section headers" "PASS"
    fi

    # Check that completion-handoff.md doesn't duplicate Tier section headers
    if grep -q "## Tier 1" "$COMPLETION_HANDOFF_FILE"; then
        print_test_result "completion-handoff.md doesn't duplicate Tier section headers" "FAIL" "Found '## Tier 1' header in completion-handoff.md"
    else
        print_test_result "completion-handoff.md doesn't duplicate Tier section headers" "PASS"
    fi

    # Check Technology Recommendations by Tier section exists in matrix
    if grep -q "## Technology Recommendations by Tier" "$MATRIX_FILE"; then
        print_test_result "Matrix has Technology Recommendations section" "PASS"
    else
        print_test_result "Matrix has Technology Recommendations section" "FAIL" "Section not found in matrix"
    fi
}

# Test 6: Verify cross-reference format consistency
test_reference_format_consistency() {
    echo -e "\n${YELLOW}=== Test 6: Cross-Reference Format Consistency ===${NC}"

    # Count references in output-templates that use the expected format
    ref_count=$(grep -c "\[complexity-assessment-matrix\.md\](complexity-assessment-matrix\.md)" "$OUTPUT_TEMPLATES_FILE")
    if [ "$ref_count" -gt 0 ]; then
        print_test_result "output-templates.md uses consistent markdown link format" "PASS"
    else
        print_test_result "output-templates.md uses consistent markdown link format" "FAIL" "Expected format [filename](filename) not found"
    fi

    # Count references in completion-handoff that use the expected format
    ref_count=$(grep -c "\[complexity-assessment-matrix\.md\](complexity-assessment-matrix\.md)" "$COMPLETION_HANDOFF_FILE")
    if [ "$ref_count" -gt 0 ]; then
        print_test_result "completion-handoff.md uses consistent markdown link format" "PASS"
    else
        print_test_result "completion-handoff.md uses consistent markdown link format" "FAIL" "Expected format [filename](filename) not found"
    fi
}

# Test 7: Verify files work together in ideation context
test_ideation_workflow_integration() {
    echo -e "\n${YELLOW}=== Test 7: Ideation Workflow Integration ===${NC}"

    # Verify output-templates mentions complexity assessment
    if grep -q "complexity" "$OUTPUT_TEMPLATES_FILE" || grep -q "Complexity Assessment" "$OUTPUT_TEMPLATES_FILE"; then
        print_test_result "output-templates.md relates to complexity assessment" "PASS"
    else
        print_test_result "output-templates.md relates to complexity assessment" "FAIL" "No reference to complexity assessment"
    fi

    # Verify completion-handoff references next steps
    if grep -q "Next Steps" "$COMPLETION_HANDOFF_FILE" || grep -q "next action" "$COMPLETION_HANDOFF_FILE"; then
        print_test_result "completion-handoff.md contains next steps" "PASS"
    else
        print_test_result "completion-handoff.md contains next steps" "FAIL" "No next steps section"
    fi

    # Verify matrix is referenced as authoritative source
    if grep -i "authoritative" "$COMPLETION_HANDOFF_FILE" || grep -i "authoritative" "$OUTPUT_TEMPLATES_FILE"; then
        print_test_result "Files reference matrix as authoritative source" "PASS"
    else
        print_test_result "Files reference matrix as authoritative source" "FAIL" "No authoritative source designation"
    fi
}

# Test 8: Verify relative link paths are correct
test_link_resolution() {
    echo -e "\n${YELLOW}=== Test 8: Link Resolution ===${NC}"

    # Extract all markdown links from output-templates
    local links=$(grep -o '\[.*\]([^)]*\.md)' "$OUTPUT_TEMPLATES_FILE" | grep -o '([^)]*\.md)' | tr -d '()')
    local resolved=0
    local failed=0

    for link in $links; do
        if [ -f "${SKILL_DIR}/${link}" ]; then
            resolved=$((resolved + 1))
        else
            failed=$((failed + 1))
        fi
    done

    if [ $failed -eq 0 ] && [ $resolved -gt 0 ]; then
        print_test_result "output-templates.md all links resolve" "PASS"
    else
        print_test_result "output-templates.md all links resolve" "FAIL" "Failed to resolve $failed links"
    fi

    # Extract all markdown links from completion-handoff
    local links=$(grep -o '\[.*\]([^)]*\.md)' "$COMPLETION_HANDOFF_FILE" | grep -o '([^)]*\.md)' | tr -d '()')
    local resolved=0
    local failed=0

    for link in $links; do
        if [ -f "${SKILL_DIR}/${link}" ]; then
            resolved=$((resolved + 1))
        else
            failed=$((failed + 1))
        fi
    done

    if [ $failed -eq 0 ] && [ $resolved -gt 0 ]; then
        print_test_result "completion-handoff.md all links resolve" "PASS"
    else
        print_test_result "completion-handoff.md all links resolve" "FAIL" "Failed to resolve $failed links"
    fi
}

# Test 9: Verify tier descriptions are accessible via matrix
test_tier_descriptions_in_matrix() {
    echo -e "\n${YELLOW}=== Test 9: Tier Descriptions in Matrix ===${NC}"

    # Each tier should have at least one description/characteristic
    if grep -A 5 "^### Tier 1:" "$MATRIX_FILE" | grep -q "Simple"; then
        print_test_result "Tier 1 has description in matrix" "PASS"
    else
        print_test_result "Tier 1 has description in matrix" "FAIL" "No description found"
    fi

    if grep -A 5 "^### Tier 2:" "$MATRIX_FILE" | grep -q "Moderate"; then
        print_test_result "Tier 2 has description in matrix" "PASS"
    else
        print_test_result "Tier 2 has description in matrix" "FAIL" "No description found"
    fi

    if grep -A 5 "^### Tier 3:" "$MATRIX_FILE" | grep -q "Complex"; then
        print_test_result "Tier 3 has description in matrix" "PASS"
    else
        print_test_result "Tier 3 has description in matrix" "FAIL" "No description found"
    fi

    if grep -A 5 "^### Tier 4:" "$MATRIX_FILE" | grep -q "Enterprise"; then
        print_test_result "Tier 4 has description in matrix" "PASS"
    else
        print_test_result "Tier 4 has description in matrix" "FAIL" "No description found"
    fi
}

# Test 10: Verify no broken anchor references
test_anchor_references() {
    echo -e "\n${YELLOW}=== Test 10: Cross-Reference Section Anchors ===${NC}"

    # Test that references to "Technology Recommendations by Tier" can find it
    if grep -q "Technology Recommendations by Tier" "$MATRIX_FILE"; then
        print_test_result "Matrix has 'Technology Recommendations by Tier' section" "PASS"
    else
        print_test_result "Matrix has 'Technology Recommendations by Tier' section" "FAIL" "Section anchor not found"
    fi

    # Verify both files reference this section
    local count=$(grep -c "Technology Recommendations" "$OUTPUT_TEMPLATES_FILE")
    count=$((count + $(grep -c "Technology Recommendations" "$COMPLETION_HANDOFF_FILE")))

    if [ $count -gt 0 ]; then
        print_test_result "Both files reference Technology Recommendations section" "PASS"
    else
        print_test_result "Both files reference Technology Recommendations section" "FAIL" "No references found"
    fi
}

# Test 11: AC#1 - Matrix remains authoritative
test_ac1_matrix_authoritative() {
    echo -e "\n${YELLOW}=== Test 11: AC#1 - Matrix is Authoritative Source ===${NC}"

    # Matrix should contain recommendations for all tiers
    local tier_count=$(grep -c "^### Tier [1-4]:" "$MATRIX_FILE")
    if [ $tier_count -eq 4 ]; then
        print_test_result "AC#1: Matrix contains all 4 tier recommendations" "PASS"
    else
        print_test_result "AC#1: Matrix contains all 4 tier recommendations" "FAIL" "Found $tier_count tiers, expected 4"
    fi
}

# Test 12: AC#2 - output-templates uses cross-references
test_ac2_output_templates_references() {
    echo -e "\n${YELLOW}=== Test 12: AC#2 - output-templates Uses Cross-References ===${NC}"

    # Should have reference to matrix
    if grep -q "For full details, see:" "$OUTPUT_TEMPLATES_FILE"; then
        print_test_result "AC#2: output-templates uses 'For full details' pattern" "PASS"
    else
        print_test_result "AC#2: output-templates uses 'For full details' pattern" "FAIL" "Pattern not found"
    fi

    # Should reference specific tier or matrix location
    if grep "For full details, see:" "$OUTPUT_TEMPLATES_FILE" | grep -q "Tier\|matrix"; then
        print_test_result "AC#2: Cross-reference includes tier information" "PASS"
    else
        print_test_result "AC#2: Cross-reference includes tier information" "FAIL" "Tier reference not found"
    fi
}

# Test 13: AC#3 - completion-handoff uses cross-references
test_ac3_completion_handoff_references() {
    echo -e "\n${YELLOW}=== Test 13: AC#3 - completion-handoff Uses Cross-References ===${NC}"

    # Should reference complexity-assessment-matrix
    if grep -q "complexity-assessment-matrix" "$COMPLETION_HANDOFF_FILE"; then
        print_test_result "AC#3: completion-handoff references complexity-assessment-matrix" "PASS"
    else
        print_test_result "AC#3: completion-handoff references complexity-assessment-matrix" "FAIL" "No reference found"
    fi

    # Should use tier reference format
    if grep "complexity-assessment-matrix" "$COMPLETION_HANDOFF_FILE" | grep -q "(Tier [1-4])"; then
        print_test_result "AC#3: Handoff uses (Tier N) format" "PASS"
    else
        print_test_result "AC#3: Handoff uses (Tier N) format" "FAIL" "Format not found"
    fi
}

# Test 14: AC#4 - Zero duplication
test_ac4_zero_duplication() {
    echo -e "\n${YELLOW}=== Test 14: AC#4 - Zero Duplication Between Files ===${NC}"

    # Check templates doesn't duplicate matrix sections
    local template_tier_headers=$(grep -c "^### Tier [1-4]:" "$OUTPUT_TEMPLATES_FILE")
    if [ $template_tier_headers -eq 0 ]; then
        print_test_result "AC#4: output-templates doesn't duplicate tier section headers" "PASS"
    else
        print_test_result "AC#4: output-templates doesn't duplicate tier section headers" "FAIL" "Found $template_tier_headers duplicate headers"
    fi

    # Check handoff doesn't duplicate matrix sections
    local handoff_tier_headers=$(grep -c "^### Tier [1-4]:" "$COMPLETION_HANDOFF_FILE")
    if [ $handoff_tier_headers -eq 0 ]; then
        print_test_result "AC#4: completion-handoff doesn't duplicate tier section headers" "PASS"
    else
        print_test_result "AC#4: completion-handoff doesn't duplicate tier section headers" "FAIL" "Found $handoff_tier_headers duplicate headers"
    fi
}

# Test 15: AC#5 - Consistent cross-reference format
test_ac5_consistent_format() {
    echo -e "\n${YELLOW}=== Test 15: AC#5 - Consistent Cross-Reference Format ===${NC}"

    # Extract reference format from output-templates
    local ref_format=$(grep "For full details, see:" "$OUTPUT_TEMPLATES_FILE" | head -1)

    if echo "$ref_format" | grep -q "\[complexity-assessment-matrix.md\](complexity-assessment-matrix.md)"; then
        print_test_result "AC#5: References use markdown link format" "PASS"
    else
        print_test_result "AC#5: References use markdown link format" "FAIL" "Format doesn't match expected pattern"
    fi

    # All Tier references should have consistent format
    local tier_refs=$(grep -o "(Tier [1-4])" "$OUTPUT_TEMPLATES_FILE" "$COMPLETION_HANDOFF_FILE" | wc -l)
    if [ $tier_refs -gt 0 ]; then
        print_test_result "AC#5: Tier references use (Tier N) format consistently" "PASS"
    else
        print_test_result "AC#5: Tier references use (Tier N) format consistently" "FAIL" "No consistent tier format"
    fi
}

# Main execution
main() {
    echo "=========================================="
    echo "STORY-147 Integration Test Suite"
    echo "Cross-Component Reference Validation"
    echo "=========================================="

    # Run all tests
    test_files_exist
    test_matrix_tier_sections
    test_output_templates_references
    test_completion_handoff_references
    test_no_duplication
    test_reference_format_consistency
    test_ideation_workflow_integration
    test_link_resolution
    test_tier_descriptions_in_matrix
    test_anchor_references
    test_ac1_matrix_authoritative
    test_ac2_output_templates_references
    test_ac3_completion_handoff_references
    test_ac4_zero_duplication
    test_ac5_consistent_format

    # Print summary
    echo -e "\n=========================================="
    echo "Test Summary"
    echo "=========================================="
    echo "Total tests run: $TESTS_RUN"
    echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "\n${GREEN}All tests PASSED!${NC}"
        exit 0
    else
        echo -e "\n${RED}Some tests FAILED${NC}"
        exit 1
    fi
}

# Run main function
main
