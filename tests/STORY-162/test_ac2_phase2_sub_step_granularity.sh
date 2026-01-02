#!/bin/bash

# STORY-162 AC-2: Sub-Step Granularity
# Test that Claude must mark 2 separate items for Phase 03 (Implementation) execution
#
# AC-2 Requirement:
# When Claude executes Phase 03 (Implementation), Claude must mark 2 separate items:
# - "Execute Phase 03 Step 1-2: backend-architect OR frontend-developer"
# - "Execute Phase 03 Step 3: context-validator"
#
# Note: Story uses Phase 2 (0-indexed), SKILL.md uses Phase 03 (1-indexed)
# Phase 03 in SKILL.md = Implementation phase (backend-architect + context-validator)
#
# This test SHOULD FAIL initially (Red phase - TDD)
# Implementation needed: Break Phase 03 into 2 granular sub-steps

set -e

SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"

echo "TEST: AC-2 - Phase 2 Sub-Step Granularity"
echo "=========================================="
echo ""

# Check if SKILL.md exists
if [ ! -f "$SKILL_FILE" ]; then
    echo "FAIL: $SKILL_FILE does not exist"
    exit 1
fi

# Extract TodoWrite array section
TODOWRITE_CONTENT=$(sed -n '/^TodoWrite(/,/^)/p' "$SKILL_FILE")

echo "Checking for Phase 2 sub-step items..."
echo ""

# Check for Phase 03 Step 1-2: backend-architect OR frontend-developer
# (Phase 03 in SKILL.md = Implementation phase)
PHASE03_STEP1_2=$(echo "$TODOWRITE_CONTENT" | grep -i "Phase 03 Step 1-2.*backend-architect\|Phase 03 Step 1-2.*frontend-developer" || true)
if [ -z "$PHASE03_STEP1_2" ]; then
    echo "FAIL: Missing 'Phase 03 Step 1-2: backend-architect OR frontend-developer' item"
    exit 1
fi
echo "PASS: Found 'Phase 03 Step 1-2: backend-architect OR frontend-developer'"

# Check for Phase 03 Step 3: context-validator
PHASE03_STEP3=$(echo "$TODOWRITE_CONTENT" | grep -i "Phase 03 Step 3.*context-validator" || true)
if [ -z "$PHASE03_STEP3" ]; then
    echo "FAIL: Missing 'Phase 03 Step 3: context-validator' item"
    exit 1
fi
echo "PASS: Found 'Phase 03 Step 3: context-validator'"

# Ensure Phase 03 is NOT a single combined item (should have sub-steps)
PHASE03_SINGLE=$(echo "$TODOWRITE_CONTENT" | grep -i "Execute Phase 03:" | grep -v "Step" | wc -l)
if [ "$PHASE03_SINGLE" -gt 0 ]; then
    echo "FAIL: Phase 03 still exists as a single combined item (should be broken into sub-steps)"
    echo "  Found: $(echo "$TODOWRITE_CONTENT" | grep -i "Execute Phase 03:" | grep -v "Step" || true)"
    exit 1
fi

echo ""
echo "PASS: Phase 03 (Implementation) is broken into 2 separate sub-step items"
exit 0
