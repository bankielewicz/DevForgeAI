#!/bin/bash
################################################################################
# Test: AC-2 RCA-011 Cross-Reference
#
# Given: devforgeai/RCA/RCA-011-mandatory-tdd-phase-skipping.md
# When: I review the "Related RCAs" section
# Then: it should include reference to RCA-009 with relationship explanation
#
# TDD Red Phase: This test FAILS until implementation is complete
################################################################################

set -euo pipefail

# Test configuration
RCA_011_FILE="/mnt/c/Projects/DevForgeAI2/devforgeai/RCA/RCA-011-mandatory-tdd-phase-skipping.md"
TEST_NAME="test_ac2_rca011_cross_reference"

echo "Test: AC-2 RCA-011 Cross-Reference"
echo "===================================="
echo "File: $RCA_011_FILE"
echo ""

# Check that file exists
if [ ! -f "$RCA_011_FILE" ]; then
    echo "FAIL: RCA-011 file does not exist"
    exit 1
fi

# Extract the Related RCAs section (use grep with context)
RELATED_RCAS_SECTION=$(grep -A 10 "^## Related RCAs" "$RCA_011_FILE" | head -n 8)

if [ -z "$RELATED_RCAS_SECTION" ]; then
    echo "FAIL: Related RCAs section not found in RCA-011"
    echo ""
    echo "The document should contain a '## Related RCAs' section"
    exit 1
fi

echo "Found Related RCAs section:"
echo "---"
echo "$RELATED_RCAS_SECTION"
echo "---"
echo ""

# Verify required elements in Related RCAs section
required_elements=(
    "RCA-009"
    "same root cause"
    "Incomplete Skill Workflow"
)

all_found=true
for element in "${required_elements[@]}"; do
    if grep -qi "$element" <<< "$RELATED_RCAS_SECTION"; then
        echo "✓ Found: '$element'"
    else
        echo "✗ Missing: '$element'"
        all_found=false
    fi
done

echo ""

if [ "$all_found" = true ]; then
    echo "PASS: AC-2 RCA-011 includes complete cross-reference to RCA-009"
    exit 0
else
    echo "FAIL: RCA-011 Related RCAs section missing required information"
    exit 1
fi
