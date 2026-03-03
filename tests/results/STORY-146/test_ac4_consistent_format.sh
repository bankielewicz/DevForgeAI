#!/bin/bash

################################################################################
# Test: AC#4 - All 6 phases have consistent TodoWrite pattern
#
# Validates: All TodoWrite follow consistent format:
# - Format: "Phase N: [Phase Name]"
# - Consistent across all 6 phases (1, 2, 3, 4, 5, 6)
#
# Test Approach: Verify each phase file has TodoWrite matching pattern
# Expected: FAIL initially (no implementation in phases 1, 3, 5 yet)
################################################################################

TEST_NAME="AC#4 - Consistent TodoWrite Format"

DISCOVERY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/discovery-workflow.md"
COMPLEXITY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/complexity-assessment-workflow.md"
FEASIBILITY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/feasibility-analysis-workflow.md"

# Array to track failures
declare -a FAILURES

# Arrange: Validate all files exist
if [ ! -f "$DISCOVERY_FILE" ]; then
    FAILURES+=("Discovery workflow file not found: $DISCOVERY_FILE")
fi

if [ ! -f "$COMPLEXITY_FILE" ]; then
    FAILURES+=("Complexity workflow file not found: $COMPLEXITY_FILE")
fi

if [ ! -f "$FEASIBILITY_FILE" ]; then
    FAILURES+=("Feasibility workflow file not found: $FEASIBILITY_FILE")
fi

# Exit if files missing
if [ ${#FAILURES[@]} -gt 0 ]; then
    echo "FAIL: [$TEST_NAME] Missing workflow files:"
    for failure in "${FAILURES[@]}"; do
        echo "  - $failure"
    done
    exit 1
fi

# Act: Check each file for TodoWrite with Phase N: format
# Note: TodoWrite is multi-line JSON format, so check for:
# 1. TodoWrite keyword present
# 2. Phase content format present within TodoWrite block

# Phase 1: Discovery & Problem Understanding
# Check for TodoWrite block containing Phase 1 content
PHASE1_HAS_TODOWRITE=$(grep -c "TodoWrite" "$DISCOVERY_FILE")
PHASE1_HAS_CONTENT=$(grep -c '"content": "Phase 1: Discovery & Problem Understanding"' "$DISCOVERY_FILE")

if [ "$PHASE1_HAS_TODOWRITE" -eq 0 ] || [ "$PHASE1_HAS_CONTENT" -eq 0 ]; then
    FAILURES+=("Phase 1: TodoWrite format 'Phase 1: Discovery & Problem Understanding' not found")
fi

# Phase 3: Complexity Assessment
PHASE3_HAS_TODOWRITE=$(grep -c "TodoWrite" "$COMPLEXITY_FILE")
PHASE3_HAS_CONTENT=$(grep -c '"content": "Phase 3: Complexity Assessment"' "$COMPLEXITY_FILE")

if [ "$PHASE3_HAS_TODOWRITE" -eq 0 ] || [ "$PHASE3_HAS_CONTENT" -eq 0 ]; then
    FAILURES+=("Phase 3: TodoWrite format 'Phase 3: Complexity Assessment' not found")
fi

# Phase 5: Feasibility & Constraints Analysis
PHASE5_HAS_TODOWRITE=$(grep -c "TodoWrite" "$FEASIBILITY_FILE")
PHASE5_HAS_CONTENT=$(grep -c '"content": "Phase 5: Feasibility & Constraints Analysis"' "$FEASIBILITY_FILE")

if [ "$PHASE5_HAS_TODOWRITE" -eq 0 ] || [ "$PHASE5_HAS_CONTENT" -eq 0 ]; then
    FAILURES+=("Phase 5: TodoWrite format 'Phase 5: Feasibility & Constraints Analysis' not found")
fi

# Assert: Check for any failures
if [ ${#FAILURES[@]} -gt 0 ]; then
    echo "FAIL: [$TEST_NAME] TodoWrite format inconsistencies detected:"
    for failure in "${FAILURES[@]}"; do
        echo "  - $failure"
    done
    echo ""
    echo "  Expected format: 'Phase N: [Phase Name]'"
    exit 1
fi

# All assertions passed
echo "PASS: [$TEST_NAME] All phases use consistent TodoWrite format"
echo "  Phase 1: Phase 1: Discovery & Problem Understanding"
echo "  Phase 3: Phase 3: Complexity Assessment"
echo "  Phase 5: Phase 5: Feasibility & Constraints Analysis"
echo "  Format: 'Phase N: [Phase Name]' ✓"
exit 0
