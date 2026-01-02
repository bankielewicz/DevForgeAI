#!/bin/bash
################################################################################
# Test: AC-1 RCA-009 Status Updated
#
# Given: devforgeai/RCA/RCA-009-skill-execution-incomplete-workflow.md
# When: I review the status line (line 7)
# Then: it should show "Recurred - See RCA-011 (2025-11-19, STORY-044, same root cause)"
#
# TDD Red Phase: This test FAILS until implementation is complete
################################################################################

set -euo pipefail

# Test configuration
RCA_009_FILE="/mnt/c/Projects/DevForgeAI2/devforgeai/RCA/RCA-009-skill-execution-incomplete-workflow.md"
EXPECTED_STATUS="**Status:** Recurred - See RCA-011 (2025-11-19, STORY-044, same root cause)"
TEST_NAME="test_ac1_rca009_status_updated"

echo "Test: AC-1 RCA-009 Status Updated"
echo "=================================="
echo "File: $RCA_009_FILE"
echo ""

# Check that file exists
if [ ! -f "$RCA_009_FILE" ]; then
    echo "FAIL: RCA-009 file does not exist"
    exit 1
fi

# Extract line 7 from RCA-009
STATUS_LINE=$(sed -n '7p' "$RCA_009_FILE")

echo "Expected status line:"
echo "  $EXPECTED_STATUS"
echo ""
echo "Actual status line:"
echo "  $STATUS_LINE"
echo ""

# Verify the status line contains the required text
if grep -q "Recurred - See RCA-011" <<< "$STATUS_LINE"; then
    if grep -q "2025-11-19" <<< "$STATUS_LINE"; then
        if grep -q "STORY-044" <<< "$STATUS_LINE"; then
            if grep -q "same root cause" <<< "$STATUS_LINE"; then
                echo "PASS: AC-1 Status line correctly updated with RCA-011 reference"
                exit 0
            fi
        fi
    fi
fi

echo "FAIL: Status line does not contain all required elements"
echo "  Required elements:"
echo "    - 'Recurred - See RCA-011'"
echo "    - '2025-11-19'"
echo "    - 'STORY-044'"
echo "    - 'same root cause'"
exit 1
