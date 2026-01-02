#!/bin/bash

# STORY-162 AC-4: Self-Monitoring Enhancement
# Test that sequential nature indicates if phases are skipped
#
# AC-4 Requirement:
# When Claude tries to mark "Phase 04 Step 3: code-reviewer" without marking
# "Phase 04 Step 1-2: refactoring-specialist", the sequential nature should
# indicate something is wrong
#
# Note: SKILL.md uses Phase 04 for Refactoring (story uses Phase 3)
#
# This test SHOULD FAIL initially (Red phase - TDD)
# Implementation needed: Ensure Phase 04 has granular sub-steps in sequential order

set -e

SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"

echo "TEST: AC-4 - Self-Monitoring (Sequential Enforcement)"
echo "===================================================="
echo ""

# Check if SKILL.md exists
if [ ! -f "$SKILL_FILE" ]; then
    echo "FAIL: $SKILL_FILE does not exist"
    exit 1
fi

# Extract TodoWrite array
TODOWRITE_CONTENT=$(sed -n '/^TodoWrite(/,/^)/p' "$SKILL_FILE")

echo "Checking Phase 04 sub-step sequencing..."
echo ""

# Find the positions of Phase 04 items (SKILL.md uses Phase 04 for Refactoring)
PHASE04_1_2_LINE=$(echo "$TODOWRITE_CONTENT" | grep -n "Phase 04 Step 1-2" | cut -d: -f1 || true)
PHASE04_3_LINE=$(echo "$TODOWRITE_CONTENT" | grep -n "Phase 04 Step 3" | cut -d: -f1 || true)

if [ -z "$PHASE04_1_2_LINE" ]; then
    echo "FAIL: 'Phase 04 Step 1-2: refactoring-specialist' item not found"
    exit 1
fi
echo "PASS: Found 'Phase 04 Step 1-2' at line $PHASE04_1_2_LINE"

if [ -z "$PHASE04_3_LINE" ]; then
    echo "FAIL: 'Phase 04 Step 3: code-reviewer' item not found"
    exit 1
fi
echo "PASS: Found 'Phase 04 Step 3' at line $PHASE04_3_LINE"

# Verify sequential ordering: Step 1-2 must come before Step 3
if [ "$PHASE04_1_2_LINE" -lt "$PHASE04_3_LINE" ]; then
    echo "PASS: 'Phase 04 Step 1-2' comes BEFORE 'Phase 04 Step 3' (correct sequential order)"
else
    echo "FAIL: 'Phase 04 Step 1-2' at line $PHASE04_1_2_LINE should come before 'Phase 04 Step 3' at line $PHASE04_3_LINE"
    exit 1
fi

echo ""

# Check for Phase 04 Step 5 as well (from AC-1)
PHASE04_5_LINE=$(echo "$TODOWRITE_CONTENT" | grep -n "Phase 04 Step 5" | cut -d: -f1 || true)
if [ -n "$PHASE04_5_LINE" ]; then
    echo "PASS: Found 'Phase 04 Step 5' at line $PHASE04_5_LINE"

    # Verify ordering: Step 3 must come before Step 5
    if [ "$PHASE04_3_LINE" -lt "$PHASE04_5_LINE" ]; then
        echo "PASS: 'Phase 04 Step 3' comes BEFORE 'Phase 04 Step 5' (correct sequential order)"
    else
        echo "FAIL: 'Phase 04 Step 3' should come before 'Phase 04 Step 5'"
        exit 1
    fi
else
    echo "INFO: 'Phase 04 Step 5' not found (may be optional in variant)"
fi

echo ""

# Verify the items have distinct activeForm descriptions
PHASE04_1_2_FORM=$(echo "$TODOWRITE_CONTENT" | grep "Phase 04 Step 1-2" | grep -o 'activeForm: "[^"]*"' || true)
PHASE04_3_FORM=$(echo "$TODOWRITE_CONTENT" | grep "Phase 04 Step 3" | grep -o 'activeForm: "[^"]*"' || true)

if [ "$PHASE04_1_2_FORM" != "$PHASE04_3_FORM" ]; then
    echo "PASS: Phase 04 Step 1-2 and Step 3 have different activeForm descriptions"
    echo "  Step 1-2: $PHASE04_1_2_FORM"
    echo "  Step 3:   $PHASE04_3_FORM"
else
    echo "FAIL: Phase 04 Step 1-2 and Step 3 have the same activeForm (should be different)"
    exit 1
fi

echo ""
echo "PASS: Sequential ordering enforces self-monitoring of Phase 04 sub-steps"
exit 0
