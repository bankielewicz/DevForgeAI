#!/bin/bash

# STORY-162 Integration Test: All AC Together
# Comprehensive test validating all acceptance criteria work together
#
# This test runs all AC validations in sequence and provides
# a comprehensive report of TodoWrite tracker expansion status.

set -e

SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"

echo "STORY-162 Integration Test: Enhanced TodoWrite Tracker"
echo "====================================================="
echo ""

# Check SKILL.md exists
if [ ! -f "$SKILL_FILE" ]; then
    echo "ERROR: $SKILL_FILE does not exist"
    exit 1
fi

# Extract TodoWrite content
TODOWRITE_CONTENT=$(sed -n '/^TodoWrite(/,/^)/p' "$SKILL_FILE")

if [ -z "$TODOWRITE_CONTENT" ]; then
    echo "ERROR: TodoWrite section not found in $SKILL_FILE"
    exit 1
fi

echo "=== AC-1: Count Items (~15) ==="
ITEM_COUNT=$(echo "$TODOWRITE_CONTENT" | grep -c '{content:' || true)
echo "Item count: $ITEM_COUNT (expected ~15, tolerance ±2)"

if [ "$ITEM_COUNT" -ge 13 ] && [ "$ITEM_COUNT" -le 17 ]; then
    echo "Status: PASS"
    AC1_PASS=true
else
    echo "Status: FAIL"
    AC1_PASS=false
fi

echo ""
echo "=== AC-2: Phase 2 Sub-Step Granularity ==="

# Note: Implementation uses Phase 03 for Implementation (backend-architect + context-validator)
# AC-2 story refers to "Phase 2" (0-indexed), but SKILL.md uses Phase 03 (1-indexed)
PHASE03_1_2=$(echo "$TODOWRITE_CONTENT" | grep -i "Phase 03 Step 1-2" | grep -i "backend-architect\|frontend-developer" || true)
PHASE03_3=$(echo "$TODOWRITE_CONTENT" | grep -i "Phase 03 Step 3" | grep -i "context-validator" || true)
PHASE03_SINGLE=$(echo "$TODOWRITE_CONTENT" | grep -i "Execute Phase 03:" | grep -v "Step" | wc -l)

echo "Phase 03 Step 1-2 found: $([ -n "$PHASE03_1_2" ] && echo "YES" || echo "NO")"
echo "Phase 03 Step 3 found: $([ -n "$PHASE03_3" ] && echo "YES" || echo "NO")"
echo "Phase 03 single item (should be 0): $PHASE03_SINGLE"

if [ -n "$PHASE03_1_2" ] && [ -n "$PHASE03_3" ] && [ "$PHASE03_SINGLE" -eq 0 ]; then
    echo "Status: PASS"
    AC2_PASS=true
else
    echo "Status: FAIL"
    AC2_PASS=false
fi

echo ""
echo "=== AC-3: User Visibility (Unique ActiveForms) ==="

UNIQUE_FORMS=$(echo "$TODOWRITE_CONTENT" | grep -o 'activeForm: "[^"]*"' | sort -u | wc -l)
TOTAL_ITEMS=$(echo "$TODOWRITE_CONTENT" | grep -c 'activeForm:' || true)

echo "Unique activeForm descriptions: $UNIQUE_FORMS"
echo "Total items: $TOTAL_ITEMS"

if [ "$UNIQUE_FORMS" -ge 13 ] && [ "$TOTAL_ITEMS" -ge 13 ]; then
    echo "Status: PASS"
    AC3_PASS=true
else
    echo "Status: FAIL"
    AC3_PASS=false
fi

echo ""
echo "=== AC-4: Sequential Enforcement (Phase 04 Refactoring) ==="

# Note: Implementation uses Phase 04 for Refactoring (refactoring-specialist + code-reviewer)
# AC-4 story refers to "Phase 3" (0-indexed), but SKILL.md uses Phase 04 (1-indexed)
PHASE04_1_2_LINE=$(echo "$TODOWRITE_CONTENT" | grep -n "Phase 04 Step 1-2" | cut -d: -f1 || true)
PHASE04_3_LINE=$(echo "$TODOWRITE_CONTENT" | grep -n "Phase 04 Step 3" | cut -d: -f1 || true)

echo "Phase 04 Step 1-2 line: $PHASE04_1_2_LINE"
echo "Phase 04 Step 3 line: $PHASE04_3_LINE"

if [ -n "$PHASE04_1_2_LINE" ] && [ -n "$PHASE04_3_LINE" ] && [ "$PHASE04_1_2_LINE" -lt "$PHASE04_3_LINE" ]; then
    echo "Status: PASS (ordered: Step 1-2 before Step 3)"
    AC4_PASS=true
else
    echo "Status: FAIL (incorrect sequence)"
    AC4_PASS=false
fi

echo ""
echo "=== Summary ==="
echo "AC-1 (15 items): $([ "$AC1_PASS" = true ] && echo "PASS" || echo "FAIL")"
echo "AC-2 (Phase 2 granularity): $([ "$AC2_PASS" = true ] && echo "PASS" || echo "FAIL")"
echo "AC-3 (User visibility): $([ "$AC3_PASS" = true ] && echo "PASS" || echo "FAIL")"
echo "AC-4 (Sequential order): $([ "$AC4_PASS" = true ] && echo "PASS" || echo "FAIL")"

echo ""

# List all current items for reference
echo "=== Current TodoWrite Items ==="
echo "$TODOWRITE_CONTENT" | grep '{content:' | sed 's/.*{content: /  - /' | head -20

echo ""

if [ "$AC1_PASS" = true ] && [ "$AC2_PASS" = true ] && [ "$AC3_PASS" = true ] && [ "$AC4_PASS" = true ]; then
    echo "OVERALL: PASS - All acceptance criteria satisfied"
    exit 0
else
    echo "OVERALL: FAIL - One or more acceptance criteria not satisfied"
    exit 1
fi
