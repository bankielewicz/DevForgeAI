#!/bin/bash
# Test AC-1: New Section in CLAUDE.md
# DOC-001: Add new section 'CRITICAL: No Deviation from Skill Phases' after Skill Execution Model section
# Expected: FAIL initially (before implementation)

CLAUDE_FILE="src/CLAUDE.md"

echo "=== AC-1: New Section After Skill Execution Model ==="

# Check if CLAUDE.md exists
if [ ! -f "$CLAUDE_FILE" ]; then
    echo "FAIL: Target file $CLAUDE_FILE does not exist"
    exit 1
fi

# Test 1: Check section header exists with exact format
if grep -q "## CRITICAL: No Deviation from Skill Phases" "$CLAUDE_FILE"; then
    echo "  [PASS] Section header '## CRITICAL: No Deviation from Skill Phases' found"
else
    echo "  [FAIL] Section header '## CRITICAL: No Deviation from Skill Phases' NOT found"
    exit 1
fi

# Test 2: Check section appears AFTER Skills Execution section
# Get line numbers for both sections
SKILLS_EXEC_LINE=$(grep -n "## Skills Execution" "$CLAUDE_FILE" | head -1 | cut -d: -f1)
CRITICAL_SECTION_LINE=$(grep -n "## CRITICAL: No Deviation from Skill Phases" "$CLAUDE_FILE" | head -1 | cut -d: -f1)

if [ -z "$SKILLS_EXEC_LINE" ]; then
    echo "  [FAIL] '## Skills Execution' section not found (prerequisite)"
    exit 1
fi

if [ -z "$CRITICAL_SECTION_LINE" ]; then
    echo "  [FAIL] '## CRITICAL: No Deviation from Skill Phases' section not found"
    exit 1
fi

if [ "$CRITICAL_SECTION_LINE" -gt "$SKILLS_EXEC_LINE" ]; then
    echo "  [PASS] New section appears AFTER Skills Execution section (line $SKILLS_EXEC_LINE < line $CRITICAL_SECTION_LINE)"
else
    echo "  [FAIL] New section (line $CRITICAL_SECTION_LINE) does NOT appear after Skills Execution (line $SKILLS_EXEC_LINE)"
    exit 1
fi

# Test 3: Check section appears BEFORE next major section (Conditional Rules)
CONDITIONAL_RULES_LINE=$(grep -n "## Conditional Rules" "$CLAUDE_FILE" | head -1 | cut -d: -f1)

if [ -n "$CONDITIONAL_RULES_LINE" ]; then
    if [ "$CRITICAL_SECTION_LINE" -lt "$CONDITIONAL_RULES_LINE" ]; then
        echo "  [PASS] New section appears BEFORE Conditional Rules section"
    else
        echo "  [FAIL] New section (line $CRITICAL_SECTION_LINE) appears AFTER Conditional Rules (line $CONDITIONAL_RULES_LINE)"
        exit 1
    fi
fi

echo "PASS: AC-1 - New section correctly positioned after Skills Execution"
exit 0
