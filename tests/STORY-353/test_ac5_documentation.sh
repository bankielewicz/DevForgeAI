#!/bin/bash
# Test AC#5: Results Documented in Research File
# STORY-353: Validate Token Reduction with A/B Test
# Status: RED (failing) - Implementation required

set -e

RESEARCH_FILE="devforgeai/specs/research/RESEARCH-007-token-reduction-validation.research.md"

echo "=== AC#5: Documentation Validation ==="

# Test 1: Research file exists
test_research_file_exists() {
    echo "Test: RESEARCH-007 file exists"
    if [[ ! -f "$RESEARCH_FILE" ]]; then
        echo "FAIL: $RESEARCH_FILE does not exist"
        exit 1
    fi
    echo "PASS: Research file exists"
}

# Test 2: Methodology section exists
test_methodology_section() {
    echo "Test: Methodology section exists"
    if ! grep -qi "Methodology" "$RESEARCH_FILE"; then
        echo "FAIL: No Methodology section found"
        exit 1
    fi
    echo "PASS: Methodology section exists"
}

# Test 3: Methodology describes test setup
test_methodology_content() {
    echo "Test: Methodology describes test setup, codebase, queries"
    local methodology_content
    methodology_content=$(sed -n '/Methodology/,/^## /p' "$RESEARCH_FILE" | head -n -1)

    if [[ -z "$methodology_content" ]] || [[ ${#methodology_content} -lt 100 ]]; then
        echo "FAIL: Methodology section is too short (< 100 chars)"
        exit 1
    fi
    echo "PASS: Methodology section has content"
}

# Test 4: Raw Data section exists with table
test_raw_data_section() {
    echo "Test: Raw Data section exists with table"
    if ! grep -qi "Raw Data" "$RESEARCH_FILE"; then
        echo "FAIL: No Raw Data section found"
        exit 1
    fi

    # Check for table format (| query | grep_tokens | treelint_tokens | reduction |)
    if ! grep -q "|.*|.*|.*|" "$RESEARCH_FILE"; then
        echo "FAIL: No data table found in Raw Data section"
        exit 1
    fi
    echo "PASS: Raw Data section exists with table"
}

# Test 5: Analysis section exists
test_analysis_section() {
    echo "Test: Analysis section exists"
    if ! grep -qi "Analysis" "$RESEARCH_FILE"; then
        echo "FAIL: No Analysis section found"
        exit 1
    fi
    echo "PASS: Analysis section exists"
}

# Test 6: Conclusion section exists with pass/fail
test_conclusion_section() {
    echo "Test: Conclusion section exists with pass/fail determination"
    if ! grep -qi "Conclusion" "$RESEARCH_FILE"; then
        echo "FAIL: No Conclusion section found"
        exit 1
    fi

    # Must contain PASS or FAIL determination
    if ! grep -qi "PASS\|FAIL\|validated\|invalidated" "$RESEARCH_FILE"; then
        echo "FAIL: No pass/fail determination in Conclusion"
        exit 1
    fi
    echo "PASS: Conclusion section has pass/fail"
}

# Test 7: 40% target mentioned
test_target_mentioned() {
    echo "Test: 40% reduction target mentioned"
    if ! grep -q "40%" "$RESEARCH_FILE"; then
        echo "FAIL: 40% target not mentioned"
        exit 1
    fi
    echo "PASS: 40% target documented"
}

# Test 8: Recommendations section exists
test_recommendations_section() {
    echo "Test: Recommendations section exists"
    if ! grep -qi "Recommendation" "$RESEARCH_FILE"; then
        echo "FAIL: No Recommendations section found"
        exit 1
    fi
    echo "PASS: Recommendations section exists"
}

# Run all tests
test_research_file_exists
test_methodology_section
test_methodology_content
test_raw_data_section
test_analysis_section
test_conclusion_section
test_target_mentioned
test_recommendations_section

echo ""
echo "=== All AC#5 tests passed ==="
