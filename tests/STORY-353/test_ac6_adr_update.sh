#!/bin/bash
# Test AC#6: ADR-013 Validation Criteria Updated
# STORY-353: Validate Token Reduction with A/B Test
# Status: RED (failing) - Implementation required

set -e

ADR_FILE="devforgeai/specs/adrs/ADR-013-treelint-integration.md"
RESEARCH_FILE="devforgeai/specs/research/RESEARCH-007-token-reduction-validation.research.md"

echo "=== AC#6: ADR Update Validation ==="

# Test 1: ADR-013 exists
test_adr_exists() {
    echo "Test: ADR-013 file exists"
    if [[ ! -f "$ADR_FILE" ]]; then
        echo "FAIL: $ADR_FILE does not exist"
        exit 1
    fi
    echo "PASS: ADR-013 exists"
}

# Test 2: Validation Criteria section exists
test_validation_section_exists() {
    echo "Test: Validation Criteria section exists in ADR-013"
    if ! grep -qi "Validation Criteria\|Validation Results" "$ADR_FILE"; then
        echo "FAIL: No Validation Criteria section found"
        exit 1
    fi
    echo "PASS: Validation Criteria section exists"
}

# Test 3: Token reduction row has actual measured value (not placeholder)
test_token_reduction_measured() {
    echo "Test: Token reduction has actual measured value"

    # Check for a percentage value (e.g., "45%", "52.3%")
    if ! grep -qE "[0-9]+\.?[0-9]*%" "$ADR_FILE"; then
        echo "FAIL: No measured percentage value found in ADR"
        exit 1
    fi

    # Check it's not just the target placeholder "40%"
    local percentages
    percentages=$(grep -oE "[0-9]+\.?[0-9]*%" "$ADR_FILE" | grep -v "^40%$" | head -1)
    if [[ -z "$percentages" ]]; then
        echo "FAIL: Only placeholder 40% found, no actual measurement"
        exit 1
    fi
    echo "PASS: Actual measurement found: $percentages"
}

# Test 4: Reference to RESEARCH-007 exists
test_research_reference() {
    echo "Test: Reference to RESEARCH-007 exists in ADR-013"
    if ! grep -qi "RESEARCH-007\|token-reduction-validation" "$ADR_FILE"; then
        echo "FAIL: No reference to RESEARCH-007 found"
        exit 1
    fi
    echo "PASS: Reference to RESEARCH-007 found"
}

# Test 5: Status indicates validation complete (VALIDATED or INVALIDATED)
test_validation_status() {
    echo "Test: Validation status updated"
    if ! grep -qi "VALIDATED\|PASSED\|CONFIRMED\|INVALIDATED\|FAILED" "$ADR_FILE"; then
        echo "FAIL: No validation status (VALIDATED/INVALIDATED) found"
        exit 1
    fi
    echo "PASS: Validation status present"
}

# Test 6: Updated date reflects recent change
test_updated_date() {
    echo "Test: ADR has been recently updated"

    # Check for Last Updated or Updated field
    if ! grep -qi "Last Updated\|Updated:" "$ADR_FILE"; then
        echo "WARN: No Last Updated field found (non-blocking)"
    else
        echo "PASS: Last Updated field present"
    fi
}

# Test 7: Cross-reference consistency check
test_cross_reference_consistency() {
    echo "Test: ADR measurement matches RESEARCH-007 conclusion"

    if [[ ! -f "$RESEARCH_FILE" ]]; then
        echo "SKIP: Research file not yet created"
        return 0
    fi

    # Extract conclusion from research (PASS or FAIL)
    local research_conclusion
    if grep -qi "hypothesis.*validated\|PASS" "$RESEARCH_FILE"; then
        research_conclusion="PASS"
    elif grep -qi "hypothesis.*invalidated\|FAIL" "$RESEARCH_FILE"; then
        research_conclusion="FAIL"
    else
        echo "WARN: Cannot determine research conclusion"
        return 0
    fi

    # ADR should reflect same conclusion
    if [[ "$research_conclusion" == "PASS" ]]; then
        if grep -qi "VALIDATED\|PASSED\|CONFIRMED" "$ADR_FILE"; then
            echo "PASS: ADR reflects validated status consistent with research"
        else
            echo "FAIL: Research shows PASS but ADR doesn't reflect VALIDATED"
            exit 1
        fi
    else
        if grep -qi "INVALIDATED\|FAILED\|NOT.*VALIDATED" "$ADR_FILE"; then
            echo "PASS: ADR reflects invalidated status consistent with research"
        else
            echo "FAIL: Research shows FAIL but ADR doesn't reflect INVALIDATED"
            exit 1
        fi
    fi
}

# Run all tests
test_adr_exists
test_validation_section_exists
test_token_reduction_measured
test_research_reference
test_validation_status
test_updated_date
test_cross_reference_consistency

echo ""
echo "=== All AC#6 tests passed ==="
