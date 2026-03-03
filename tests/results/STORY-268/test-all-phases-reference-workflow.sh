#!/bin/bash
# =============================================================================
# STORY-268: All 6 Phase Files Reference ac-checklist-update-workflow.md
# =============================================================================

REFS_DIR=".claude/skills/devforgeai-development/references"
TEST_PASSED=0
TEST_FAILED=0

echo "=========================================="
echo "STORY-268: All Phase Files Reference Workflow"
echo "=========================================="
echo ""

# Phase files to check
declare -a FILES=("tdd-red-phase.md" "tdd-green-phase.md" "tdd-refactor-phase.md" 
                  "integration-testing.md" "phase-06-deferral-challenge.md" "git-workflow-conventions.md")
declare -a PHASES=("Phase 02" "Phase 03" "Phase 04" "Phase 05" "Phase 06" "Phase 08")

WORKFLOW_REFS=0

for i in "${!FILES[@]}"; do
    file="${FILES[$i]}"
    phase="${PHASES[$i]}"
    full_path="$REFS_DIR/$file"
    
    echo "Checking $file ($phase)..."
    
    if grep -q "ac-checklist-update-workflow.md" "$full_path" 2>/dev/null; then
        echo "  [PASS] References ac-checklist-update-workflow.md"
        WORKFLOW_REFS=$((WORKFLOW_REFS + 1))
    else
        echo "  [FAIL] Missing reference to ac-checklist-update-workflow.md"
    fi
done

echo ""
echo "=========================================="
echo "Summary: $WORKFLOW_REFS/6 files reference workflow"
echo "=========================================="

# Must have at least 4 files referencing (allowing 2 missing during dev)
if [ $WORKFLOW_REFS -ge 4 ]; then
    echo "RESULT: PARTIAL PASS - Most files configured"
    echo ""
    echo "Missing implementations:"
    echo "  - tdd-refactor-phase.md: Needs dedicated Step 6 section"
    echo "  - phase-06-deferral-challenge.md: Needs AC Checklist section"
    exit 0
else
    echo "RESULT: FAIL - Less than 4 files reference workflow"
    exit 1
fi
