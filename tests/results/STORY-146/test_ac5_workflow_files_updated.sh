#!/bin/bash

################################################################################
# Test: AC#5 - Workflow files updated with TodoWrite instructions
#
# Validates: Three workflow reference files include TodoWrite instructions:
# - discovery-workflow.md (Phase 1)
# - complexity-assessment-workflow.md (Phase 3)
# - feasibility-analysis-workflow.md (Phase 5)
#
# Test Approach: Verify each file contains TodoWrite keyword
# Expected: FAIL initially (TodoWrite not yet added to these files)
################################################################################

TEST_NAME="AC#5 - Workflow Files Updated with TodoWrite"

DISCOVERY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/discovery-workflow.md"
COMPLEXITY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/complexity-assessment-workflow.md"
FEASIBILITY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/feasibility-analysis-workflow.md"

# Array to track failures
declare -a FAILURES

# Arrange: Validate all files exist
if [ ! -f "$DISCOVERY_FILE" ]; then
    FAILURES+=("discovery-workflow.md not found")
fi

if [ ! -f "$COMPLEXITY_FILE" ]; then
    FAILURES+=("complexity-assessment-workflow.md not found")
fi

if [ ! -f "$FEASIBILITY_FILE" ]; then
    FAILURES+=("feasibility-analysis-workflow.md not found")
fi

if [ ${#FAILURES[@]} -gt 0 ]; then
    echo "FAIL: [$TEST_NAME] Missing workflow files:"
    for failure in "${FAILURES[@]}"; do
        echo "  - $failure"
    done
    exit 1
fi

# Act: Check discovery-workflow.md includes TodoWrite
DISCOVERY_TODOWRITE=$(grep -c "TodoWrite" "$DISCOVERY_FILE")

if [ "$DISCOVERY_TODOWRITE" -lt 1 ]; then
    FAILURES+=("discovery-workflow.md does not include TodoWrite keyword")
fi

# Act: Check complexity-assessment-workflow.md includes TodoWrite
COMPLEXITY_TODOWRITE=$(grep -c "TodoWrite" "$COMPLEXITY_FILE")

if [ "$COMPLEXITY_TODOWRITE" -lt 1 ]; then
    FAILURES+=("complexity-assessment-workflow.md does not include TodoWrite keyword")
fi

# Act: Check feasibility-analysis-workflow.md includes TodoWrite
FEASIBILITY_TODOWRITE=$(grep -c "TodoWrite" "$FEASIBILITY_FILE")

if [ "$FEASIBILITY_TODOWRITE" -lt 1 ]; then
    FAILURES+=("feasibility-analysis-workflow.md does not include TodoWrite keyword")
fi

# Assert: Check for any failures
if [ ${#FAILURES[@]} -gt 0 ]; then
    echo "FAIL: [$TEST_NAME] Workflow files missing TodoWrite instructions:"
    for failure in "${FAILURES[@]}"; do
        echo "  - $failure"
    done
    echo ""
    echo "  Required updates:"
    echo "    1. Add TodoWrite call at start of each phase"
    echo "    2. Add TodoWrite completion at end of each phase"
    exit 1
fi

# Verify count of TodoWrite instances (should be at least 2 per file: start + end)
echo "Discovery TodoWrite instances: $DISCOVERY_TODOWRITE"
echo "Complexity TodoWrite instances: $COMPLEXITY_TODOWRITE"
echo "Feasibility TodoWrite instances: $FEASIBILITY_TODOWRITE"

TOTAL_TODOWRITE=$((DISCOVERY_TODOWRITE + COMPLEXITY_TODOWRITE + FEASIBILITY_TODOWRITE))

if [ "$TOTAL_TODOWRITE" -lt 6 ]; then
    echo ""
    echo "FAIL: [$TEST_NAME] Insufficient TodoWrite instances"
    echo "  Found: $TOTAL_TODOWRITE TodoWrite calls (expected minimum: 6)"
    echo "  Each phase needs: 1 start + 1 end = 2 TodoWrite calls"
    echo "  3 phases × 2 calls = 6 minimum total"
    exit 1
fi

# All assertions passed
echo "PASS: [$TEST_NAME] All workflow files updated with TodoWrite"
echo "  discovery-workflow.md: $DISCOVERY_TODOWRITE TodoWrite instance(s)"
echo "  complexity-assessment-workflow.md: $COMPLEXITY_TODOWRITE TodoWrite instance(s)"
echo "  feasibility-analysis-workflow.md: $FEASIBILITY_TODOWRITE TodoWrite instance(s)"
echo "  Total: $TOTAL_TODOWRITE TodoWrite instance(s)"
exit 0
