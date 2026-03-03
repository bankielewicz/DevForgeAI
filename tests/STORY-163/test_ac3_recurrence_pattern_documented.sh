#!/bin/bash
################################################################################
# Test: AC-3 Recurrence Pattern Documented
#
# Given: both RCA documents (RCA-009 and RCA-011)
# When: I compare root cause sections
# Then: both should explicitly note this is a recurring pattern requiring systemic fix
#
# TDD Red Phase: This test FAILS until implementation is complete
################################################################################

set -euo pipefail

# Test configuration
RCA_009_FILE="/mnt/c/Projects/DevForgeAI2/devforgeai/RCA/RCA-009-skill-execution-incomplete-workflow.md"
RCA_011_FILE="/mnt/c/Projects/DevForgeAI2/devforgeai/RCA/RCA-011-mandatory-tdd-phase-skipping.md"
TEST_NAME="test_ac3_recurrence_pattern_documented"

echo "Test: AC-3 Recurrence Pattern Documented"
echo "========================================="
echo ""

# Check both files exist
if [ ! -f "$RCA_009_FILE" ]; then
    echo "FAIL: RCA-009 file does not exist at $RCA_009_FILE"
    exit 1
fi

if [ ! -f "$RCA_011_FILE" ]; then
    echo "FAIL: RCA-011 file does not exist at $RCA_011_FILE"
    exit 1
fi

echo "Checking RCA-009 for recurrence documentation..."

# In RCA-009, check that Root Cause section mentions recurrence/recurring pattern
RCA_009_CONTENT=$(cat "$RCA_009_FILE")

if grep -qi "recurring\|recurrence\|pattern" <<< "$RCA_009_CONTENT"; then
    echo "✓ RCA-009 mentions recurring/recurrence/pattern"
else
    echo "✗ RCA-009 does not mention recurring pattern"
    exit 1
fi

# In RCA-009, check for reference to systemic issue/fix
if grep -qi "systemic" <<< "$RCA_009_CONTENT"; then
    echo "✓ RCA-009 mentions systemic issue"
else
    echo "✗ RCA-009 does not mention systemic issue"
fi

echo ""
echo "Checking RCA-011 for recurrence documentation..."

# In RCA-011, check that Conclusion section mentions systemic issue
RCA_011_CONTENT=$(cat "$RCA_011_FILE")

if grep -qi "systemic" <<< "$RCA_011_CONTENT"; then
    echo "✓ RCA-011 mentions systemic issue"
else
    echo "✗ RCA-011 does not mention systemic issue"
    exit 1
fi

# In RCA-011, check for recurring/pattern language
if grep -qi "recurring\|recurrence\|same root cause" <<< "$RCA_011_CONTENT"; then
    echo "✓ RCA-011 mentions recurrence pattern"
else
    echo "✗ RCA-011 does not mention recurrence pattern"
    exit 1
fi

echo ""

# Verify both documents reference the same root cause (visual markers ignored, no enforcement)
if grep -qi "visual.*MANDATORY\|MANDATORY.*marker\|enforcement" "$RCA_009_FILE" && \
   grep -qi "visual.*MANDATORY\|MANDATORY.*marker\|enforcement" "$RCA_011_FILE"; then
    echo "✓ Both documents explain the root cause (visual markers ignored, lack of enforcement)"
    echo ""
    echo "PASS: AC-3 Recurrence pattern is documented in both RCA documents"
    exit 0
else
    echo "⚠ One or both documents may not fully explain the root cause"
    echo ""
    echo "PARTIAL: RCA documents mention systemic issue but may lack detail on root cause"
    exit 1
fi
