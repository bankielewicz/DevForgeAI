#!/bin/bash
# STORY-516 Integration Tests
# Verify cross-component consistency of Phase 07 DoD update workflow

PHASE_FILE="src/claude/skills/implementing-stories/phases/phase-07-dod-update.md"
PASS=0
FAIL=0

echo "=== STORY-516 Integration Tests ==="
echo ""

# --------------------------------------------------------------------------
# TEST 1: TDD Workflow Summary subsection appears AFTER flat DoD items
#         in the Format Requirements example block
# --------------------------------------------------------------------------
echo "TEST 1: TDD Workflow Summary appears AFTER flat DoD items in format example"

# Strategy: In the CORRECT format example (lines 114-127), extract the line
# numbers of the first "- [x]" item and "### TDD Workflow Summary".
# The TDD line must come AFTER the DoD items.

DOD_ITEM_LINE=$(grep -n '^\- \[x\] Unit tests written' "$PHASE_FILE" | head -1 | cut -d: -f1)
TDD_SUMMARY_LINE=$(grep -n '^### TDD Workflow Summary' "$PHASE_FILE" | head -1 | cut -d: -f1)

if [ -z "$DOD_ITEM_LINE" ] || [ -z "$TDD_SUMMARY_LINE" ]; then
    echo "  FAIL - Could not find DoD item line ($DOD_ITEM_LINE) or TDD Summary line ($TDD_SUMMARY_LINE)"
    FAIL=$((FAIL + 1))
elif [ "$TDD_SUMMARY_LINE" -gt "$DOD_ITEM_LINE" ]; then
    echo "  PASS - TDD Workflow Summary (line $TDD_SUMMARY_LINE) appears after DoD items (line $DOD_ITEM_LINE)"
    PASS=$((PASS + 1))
else
    echo "  FAIL - TDD Workflow Summary (line $TDD_SUMMARY_LINE) appears BEFORE DoD items (line $DOD_ITEM_LINE)"
    FAIL=$((FAIL + 1))
fi

echo ""

# --------------------------------------------------------------------------
# TEST 2: Step numbering is sequential (Steps 1, 2, 3, 4, 4.5, 5)
# --------------------------------------------------------------------------
echo "TEST 2: Step numbering remains sequential (1, 2, 3, 4, 4.5, 5)"

# Extract step numbers from the phase workflow section
STEPS=$(grep -oP '^\d+\.5?\.' "$PHASE_FILE" | tr -d '.' | sort -V | tr '\n' ' ')

# Check that we find steps 1, 2, 3, 4, 45, 5 in order
FOUND_1=$(grep -c '^1\. ' "$PHASE_FILE")
FOUND_2=$(grep -c '^2\. ' "$PHASE_FILE")
FOUND_3=$(grep -c '^3\. ' "$PHASE_FILE")
FOUND_4=$(grep -c '^4\. ' "$PHASE_FILE")
FOUND_45=$(grep -c '^4\.5\. ' "$PHASE_FILE")
FOUND_5=$(grep -c '^5\. ' "$PHASE_FILE")

if [ "$FOUND_1" -ge 1 ] && [ "$FOUND_2" -ge 1 ] && [ "$FOUND_3" -ge 1 ] && \
   [ "$FOUND_4" -ge 1 ] && [ "$FOUND_45" -ge 1 ] && [ "$FOUND_5" -ge 1 ]; then
    echo "  PASS - All steps found: 1($FOUND_1) 2($FOUND_2) 3($FOUND_3) 4($FOUND_4) 4.5($FOUND_45) 5($FOUND_5)"
    PASS=$((PASS + 1))
else
    echo "  FAIL - Missing steps: 1($FOUND_1) 2($FOUND_2) 3($FOUND_3) 4($FOUND_4) 4.5($FOUND_45) 5($FOUND_5)"
    FAIL=$((FAIL + 1))
fi

echo ""

# --------------------------------------------------------------------------
# TEST 3: Step 4.5 appears between Step 4 and Step 5 (line ordering)
# --------------------------------------------------------------------------
echo "TEST 3: Step 4.5 is positioned between Step 4 and Step 5"

STEP4_LINE=$(grep -n '^4\. ' "$PHASE_FILE" | head -1 | cut -d: -f1)
STEP45_LINE=$(grep -n '^4\.5\. ' "$PHASE_FILE" | head -1 | cut -d: -f1)
STEP5_LINE=$(grep -n '^5\. ' "$PHASE_FILE" | head -1 | cut -d: -f1)

if [ -z "$STEP4_LINE" ] || [ -z "$STEP45_LINE" ] || [ -z "$STEP5_LINE" ]; then
    echo "  FAIL - Could not find step lines: 4($STEP4_LINE) 4.5($STEP45_LINE) 5($STEP5_LINE)"
    FAIL=$((FAIL + 1))
elif [ "$STEP4_LINE" -lt "$STEP45_LINE" ] && [ "$STEP45_LINE" -lt "$STEP5_LINE" ]; then
    echo "  PASS - Step 4 (line $STEP4_LINE) < Step 4.5 (line $STEP45_LINE) < Step 5 (line $STEP5_LINE)"
    PASS=$((PASS + 1))
else
    echo "  FAIL - Wrong ordering: 4(line $STEP4_LINE) 4.5(line $STEP45_LINE) 5(line $STEP5_LINE)"
    FAIL=$((FAIL + 1))
fi

echo ""

# --------------------------------------------------------------------------
# SUMMARY
# --------------------------------------------------------------------------
TOTAL=$((PASS + FAIL))
echo "=== Results: $PASS/$TOTAL passed, $FAIL failed ==="

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
