#!/bin/bash

################################################################################
# Test: AC#4 & BR-003 - activeForm uses present continuous (-ing) tense
#
# Validates: All activeForm values in TodoWrite calls:
# - End with "-ing" (present continuous tense)
# - No exceptions in any phase
# - Examples: "Discovering", "Calculating", "Analyzing"
#
# Test Approach: Search all workflow files for activeForm values without -ing
# Expected: FAIL initially (no TodoWrite with activeForm in phases 1, 3, 5)
################################################################################

TEST_NAME="AC#4 & BR-003 - activeForm Present Continuous Tense"

DISCOVERY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/discovery-workflow.md"
COMPLEXITY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/complexity-assessment-workflow.md"
FEASIBILITY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/feasibility-analysis-workflow.md"

# Array to track failures
declare -a FAILURES

# Arrange: Validate all files exist
if [ ! -f "$DISCOVERY_FILE" ]; then
    FAILURES+=("Discovery workflow file not found")
fi

if [ ! -f "$COMPLEXITY_FILE" ]; then
    FAILURES+=("Complexity workflow file not found")
fi

if [ ! -f "$FEASIBILITY_FILE" ]; then
    FAILURES+=("Feasibility workflow file not found")
fi

if [ ${#FAILURES[@]} -gt 0 ]; then
    echo "FAIL: [$TEST_NAME] Missing workflow files:"
    for failure in "${FAILURES[@]}"; do
        echo "  - $failure"
    done
    exit 1
fi

# Act: Verify Phase 1 activeForm has -ing tense
# Expected: "Discovering problem space"
PHASE1_ACTIVEFORM=$(grep -i "activeForm.*Discovering" "$DISCOVERY_FILE")

if [ -z "$PHASE1_ACTIVEFORM" ]; then
    FAILURES+=("Phase 1: activeForm 'Discovering problem space' missing or not in present continuous")
fi

# Act: Verify Phase 3 activeForm has -ing tense
# Expected: "Calculating complexity score"
PHASE3_ACTIVEFORM=$(grep -i "activeForm.*Calculating" "$COMPLEXITY_FILE")

if [ -z "$PHASE3_ACTIVEFORM" ]; then
    FAILURES+=("Phase 3: activeForm 'Calculating complexity score' missing or not in present continuous")
fi

# Act: Verify Phase 5 activeForm has -ing tense
# Expected: "Analyzing constraints"
PHASE5_ACTIVEFORM=$(grep -i "activeForm.*Analyzing" "$FEASIBILITY_FILE")

if [ -z "$PHASE5_ACTIVEFORM" ]; then
    FAILURES+=("Phase 5: activeForm 'Analyzing constraints' missing or not in present continuous")
fi

# Assert: Check for any activeForm NOT ending in -ing (negative check)
# This is a secondary validation - look for any activeForm without -ing suffix
INVALID_FORMS=$(grep -h "activeForm" "$DISCOVERY_FILE" "$COMPLEXITY_FILE" "$FEASIBILITY_FILE" 2>/dev/null | grep -v -E "[Dd]iscovering|[Cc]alculating|[Aa]nalyzing|[a-zA-Z]+ing")

if [ ! -z "$INVALID_FORMS" ]; then
    FAILURES+=("Found activeForm values not in present continuous (-ing) tense: $INVALID_FORMS")
fi

# Assert: Check for any failures
if [ ${#FAILURES[@]} -gt 0 ]; then
    echo "FAIL: [$TEST_NAME] activeForm tense violations detected:"
    for failure in "${FAILURES[@]}"; do
        echo "  - $failure"
    done
    echo ""
    echo "  Expected: All activeForm end with '-ing' (present continuous)"
    echo "  Examples:"
    echo "    ✓ Discovering problem space"
    echo "    ✓ Calculating complexity score"
    echo "    ✓ Analyzing constraints"
    exit 1
fi

# All assertions passed
echo "PASS: [$TEST_NAME] All activeForm use present continuous tense"
echo "  Phase 1: activeForm: 'Discovering problem space' ✓"
echo "  Phase 3: activeForm: 'Calculating complexity score' ✓"
echo "  Phase 5: activeForm: 'Analyzing constraints' ✓"
exit 0
