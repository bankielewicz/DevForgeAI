#!/bin/bash
# STORY-215 AC-1: Pre-Skill Execution Checklist Added to CLAUDE.md
# Tests that the section exists after "Skills Execution" section
# Expected: FAIL initially (file not yet modified)

# Note: Not using set -e to allow all tests to run even when some fail

CLAUDE_MD="/mnt/c/Projects/DevForgeAI2/CLAUDE.md"
TEST_NAME="AC-1: Pre-Skill Execution Checklist Section Placement"
PASS_COUNT=0
FAIL_COUNT=0

echo "=================================================="
echo "STORY-215 Test: $TEST_NAME"
echo "=================================================="

# Test 1: Verify CLAUDE.md exists
echo -n "Test 1.1: CLAUDE.md exists... "
if [ -f "$CLAUDE_MD" ]; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - File not found: $CLAUDE_MD"
    ((FAIL_COUNT++))
    exit 1
fi

# Test 2: Verify "Skills Execution" section exists
echo -n "Test 1.2: Skills Execution section exists... "
if grep -q "^## Skills Execution" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing '## Skills Execution' section"
    ((FAIL_COUNT++))
fi

# Test 3: Verify "### Pre-Skill Execution Checklist" subsection exists
echo -n "Test 1.3: Pre-Skill Execution Checklist subsection exists... "
if grep -q "^### Pre-Skill Execution Checklist" "$CLAUDE_MD"; then
    echo "PASS"
    ((PASS_COUNT++))
else
    echo "FAIL - Missing '### Pre-Skill Execution Checklist' subsection"
    ((FAIL_COUNT++))
fi

# Test 4: Verify checklist appears AFTER "Skills Execution" section
# Get line numbers and verify order
echo -n "Test 1.4: Checklist appears after Skills Execution section... "
SKILLS_LINE=$(grep -n "^## Skills Execution" "$CLAUDE_MD" | head -1 | cut -d: -f1)
CHECKLIST_LINE=$(grep -n "^### Pre-Skill Execution Checklist" "$CLAUDE_MD" | head -1 | cut -d: -f1)

if [ -n "$SKILLS_LINE" ] && [ -n "$CHECKLIST_LINE" ]; then
    if [ "$CHECKLIST_LINE" -gt "$SKILLS_LINE" ]; then
        echo "PASS (Skills Execution: line $SKILLS_LINE, Checklist: line $CHECKLIST_LINE)"
        ((PASS_COUNT++))
    else
        echo "FAIL - Checklist (line $CHECKLIST_LINE) must appear after Skills Execution (line $SKILLS_LINE)"
        ((FAIL_COUNT++))
    fi
else
    echo "FAIL - Could not determine line positions (Skills: $SKILLS_LINE, Checklist: $CHECKLIST_LINE)"
    ((FAIL_COUNT++))
fi

# Test 5: Verify checklist is a subsection of Skills Execution (before next ## section)
echo -n "Test 1.5: Checklist is subsection of Skills Execution... "
if [ -n "$SKILLS_LINE" ] && [ -n "$CHECKLIST_LINE" ]; then
    # Find the next ## section after Skills Execution
    NEXT_SECTION_LINE=$(awk -v start="$SKILLS_LINE" 'NR > start && /^## [^#]/ {print NR; exit}' "$CLAUDE_MD")

    if [ -n "$NEXT_SECTION_LINE" ]; then
        if [ "$CHECKLIST_LINE" -lt "$NEXT_SECTION_LINE" ]; then
            echo "PASS (Checklist at line $CHECKLIST_LINE is before next section at line $NEXT_SECTION_LINE)"
            ((PASS_COUNT++))
        else
            echo "FAIL - Checklist (line $CHECKLIST_LINE) must be before next section (line $NEXT_SECTION_LINE)"
            ((FAIL_COUNT++))
        fi
    else
        # No next section found - checklist is at end, which is acceptable
        echo "PASS (Checklist is in final section)"
        ((PASS_COUNT++))
    fi
else
    echo "FAIL - Could not validate section structure"
    ((FAIL_COUNT++))
fi

echo ""
echo "=================================================="
echo "Results: $PASS_COUNT passed, $FAIL_COUNT failed"
echo "=================================================="

if [ $FAIL_COUNT -gt 0 ]; then
    echo "AC-1 FAILED: Pre-Skill Execution Checklist not properly placed in CLAUDE.md"
    exit 1
else
    echo "AC-1 PASSED: Pre-Skill Execution Checklist correctly placed in CLAUDE.md"
    exit 0
fi
