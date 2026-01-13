#!/bin/bash

###############################################################################
# STORY-209: Document Phase Resumption Protocol for Interrupted Workflows
# Test File: Documentation Validation Tests
#
# Purpose: Validate the structure and content of the Phase Resumption Protocol
#          documentation in .claude/skills/devforgeai-development/SKILL.md
#
# Test Framework: Bash with grep/pattern validation
# Test Type: Documentation Specification Tests (non-executable validation)
# Status: TDD Red Phase - All tests should FAIL initially
#
# This test file validates that all 5 acceptance criteria are properly
# documented in the SKILL.md file with correct structure, section headers,
# and key content patterns.
###############################################################################

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Target file to validate
TARGET_FILE=".claude/skills/devforgeai-development/SKILL.md"

###############################################################################
# Helper Functions
###############################################################################

test_start() {
    local test_name="$1"
    echo -e "\n${YELLOW}[TEST]${NC} $test_name"
    ((TESTS_RUN++))
}

test_pass() {
    local test_name="$1"
    echo -e "${GREEN}✓ PASS${NC}: $test_name"
    ((TESTS_PASSED++))
}

test_fail() {
    local test_name="$1"
    local reason="$2"
    echo -e "${RED}✗ FAIL${NC}: $test_name"
    if [ -n "$reason" ]; then
        echo -e "  Reason: $reason"
    fi
    ((TESTS_FAILED++))
}

# Helper: Check if section header exists with case-insensitive match
section_exists() {
    local section_name="$1"
    local file="$2"
    grep -qiE "^(#{1,4}) .*(${section_name})" "$file"
}

# Helper: Check if file contains pattern (case-insensitive)
contains_pattern() {
    local pattern="$1"
    local file="$2"
    grep -qi "$pattern" "$file"
}

# Helper: Check if file contains exact text pattern (case-sensitive)
contains_text() {
    local text="$1"
    local file="$2"
    grep -q "$text" "$file"
}

# Helper: Count number of matching lines
count_matches() {
    local pattern="$1"
    local file="$2"
    grep -c "$pattern" "$file" 2>/dev/null || echo "0"
}

###############################################################################
# Pre-Validation: File Existence
###############################################################################

echo "=========================================================================="
echo "STORY-209: Phase Resumption Protocol Documentation Tests"
echo "=========================================================================="
echo ""
echo "Target file: $TARGET_FILE"
echo ""

if [ ! -f "$TARGET_FILE" ]; then
    echo -e "${RED}ERROR${NC}: Target file not found: $TARGET_FILE"
    echo "Tests cannot proceed."
    exit 1
fi

echo -e "${GREEN}✓${NC} Target file exists"
echo ""

###############################################################################
# AC#1: User Detection Indicators Documented
###############################################################################

echo "=========================================================================="
echo "AC#1: User Detection Indicators Documented"
echo "=========================================================================="

test_start "AC#1.1: Section 'User Detection Indicators' exists"
if section_exists "User Detection Indicators" "$TARGET_FILE"; then
    test_pass "AC#1.1: Section 'User Detection Indicators' exists"
else
    test_fail "AC#1.1: Section 'User Detection Indicators' exists" \
        "Section header not found - expected pattern: ### User Detection Indicators"
fi

test_start "AC#1.2: TodoWrite list shows phases as 'pending' or 'in_progress' indicator documented"
if contains_pattern "TodoWrite.*pending\|in_progress\|phases" "$TARGET_FILE"; then
    test_pass "AC#1.2: TodoWrite pending/in_progress indicator documented"
else
    test_fail "AC#1.2: TodoWrite pending/in_progress indicator documented" \
        "Pattern 'TodoWrite' combined with 'pending' or 'in_progress' not found"
fi

test_start "AC#1.3: DoD completion indicator (<100% but workflow declared complete) documented"
if contains_pattern "DoD.*completion\|Definition.*Done.*100" "$TARGET_FILE"; then
    test_pass "AC#1.3: DoD completion indicator documented"
else
    test_fail "AC#1.3: DoD completion indicator documented" \
        "Pattern about DoD completion percentage not found"
fi

test_start "AC#1.4: Story status indicator documented"
if contains_pattern "status.*not.*updated\|story.*status" "$TARGET_FILE"; then
    test_pass "AC#1.4: Story status indicator documented"
else
    test_fail "AC#1.4: Story status indicator documented" \
        "Pattern about story status update detection not found"
fi

test_start "AC#1.5: Git commit detection indicator documented"
if contains_pattern "git.*commit\|no.*git.*commit" "$TARGET_FILE"; then
    test_pass "AC#1.5: Git commit detection indicator documented"
else
    test_fail "AC#1.5: Git commit detection indicator documented" \
        "Pattern about git commit detection not found"
fi

###############################################################################
# AC#2: User Recovery Command Documented
###############################################################################

echo ""
echo "=========================================================================="
echo "AC#2: User Recovery Command Documented"
echo "=========================================================================="

test_start "AC#2.1: Section 'User Recovery Command' exists"
if section_exists "User Recovery Command" "$TARGET_FILE"; then
    test_pass "AC#2.1: Section 'User Recovery Command' exists"
else
    test_fail "AC#2.1: Section 'User Recovery Command' exists" \
        "Section header not found - expected pattern: ### User Recovery Command"
fi

test_start "AC#2.2: Code block with recovery command template documented"
if contains_pattern "Continue.*\/dev.*STORY\|Resume.*execution" "$TARGET_FILE"; then
    test_pass "AC#2.2: Code block with recovery command template documented"
else
    test_fail "AC#2.2: Code block with recovery command template documented" \
        "Recovery command template pattern not found"
fi

test_start "AC#2.3: References to pending phases list in recovery command"
if contains_pattern "pending.*phase\|phase.*pending\|remaining.*phase" "$TARGET_FILE"; then
    test_pass "AC#2.3: References to pending phases list in recovery command"
else
    test_fail "AC#2.3: References to pending phases list in recovery command" \
        "Pattern about pending/remaining phases not found"
fi

test_start "AC#2.4: 'Resume execution now' or similar action phrase documented"
if contains_pattern "resume.*execution\|proceed.*now\|continue.*now" "$TARGET_FILE"; then
    test_pass "AC#2.4: 'Resume execution now' or similar action phrase documented"
else
    test_fail "AC#2.4: 'Resume execution now' or similar action phrase documented" \
        "Action phrase pattern not found"
fi

###############################################################################
# AC#3: Claude Resumption Steps Documented
###############################################################################

echo ""
echo "=========================================================================="
echo "AC#3: Claude Resumption Steps Documented"
echo "=========================================================================="

test_start "AC#3.1: Section 'Claude Resumption Steps' exists"
if section_exists "Claude Resumption Steps" "$TARGET_FILE"; then
    test_pass "AC#3.1: Section 'Claude Resumption Steps' exists"
else
    test_fail "AC#3.1: Section 'Claude Resumption Steps' exists" \
        "Section header not found - expected pattern: ### Claude Resumption Steps"
fi

test_start "AC#3.2: Step 1 - Check TodoWrite State documented"
if contains_pattern "1.*Check.*TodoWrite\|TodoWrite.*state\|step.*1" "$TARGET_FILE"; then
    test_pass "AC#3.2: Step 1 - Check TodoWrite State documented"
else
    test_fail "AC#3.2: Step 1 - Check TodoWrite State documented" \
        "Step 1 pattern not found"
fi

test_start "AC#3.3: Step 2 - Verify Previous Phases documented"
if contains_pattern "2.*Verify.*[Pp]revious\|[Pp]revious.*[Pp]hase.*verif\|step.*2" "$TARGET_FILE"; then
    test_pass "AC#3.3: Step 2 - Verify Previous Phases documented"
else
    test_fail "AC#3.3: Step 2 - Verify Previous Phases documented" \
        "Step 2 pattern not found"
fi

test_start "AC#3.4: Step 3 - Load Phase Reference documented"
if contains_pattern "3.*Load.*[Pp]hase.*[Rr]eference\|[Pp]hase.*reference.*load\|step.*3" "$TARGET_FILE"; then
    test_pass "AC#3.4: Step 3 - Load Phase Reference documented"
else
    test_fail "AC#3.4: Step 3 - Load Phase Reference documented" \
        "Step 3 pattern not found"
fi

test_start "AC#3.5: Step 4 - Execute Remaining Phases documented"
if contains_pattern "4.*Execute.*[Rr]emaining\|[Rr]emaining.*[Pp]hase.*execute\|step.*4" "$TARGET_FILE"; then
    test_pass "AC#3.5: Step 4 - Execute Remaining Phases documented"
else
    test_fail "AC#3.5: Step 4 - Execute Remaining Phases documented" \
        "Step 4 pattern not found"
fi

test_start "AC#3.6: Step 5 - Final Validation documented"
if contains_pattern "5.*[Ff]inal.*[Vv]alid\|[Vv]alid.*final\|step.*5" "$TARGET_FILE"; then
    test_pass "AC#3.6: Step 5 - Final Validation documented"
else
    test_fail "AC#3.6: Step 5 - Final Validation documented" \
        "Step 5 pattern not found"
fi

test_start "AC#3.7: Six numbered steps exist (1-6)"
if contains_pattern "^[[:space:]]*[0-9]\." "$TARGET_FILE"; then
    step_count=$(grep -c "^[[:space:]]*[0-9]\." "$TARGET_FILE")
    if [ "$step_count" -ge 5 ]; then
        test_pass "AC#3.7: Multiple numbered steps documented (found: $step_count)"
    else
        test_fail "AC#3.7: Multiple numbered steps documented" \
            "Expected 5+ numbered steps, found: $step_count"
    fi
else
    test_fail "AC#3.7: Multiple numbered steps documented" \
        "No numbered step patterns found"
fi

###############################################################################
# AC#4: Resumption Validation Checklist
###############################################################################

echo ""
echo "=========================================================================="
echo "AC#4: Resumption Validation Checklist"
echo "=========================================================================="

test_start "AC#4.1: Checklist section exists"
if contains_pattern "checklist\|[Vv]alid.*[Pp]re-[Ff]light\|[Pp]re-[Ff]light" "$TARGET_FILE"; then
    test_pass "AC#4.1: Checklist section exists"
else
    test_fail "AC#4.1: Checklist section exists" \
        "Checklist or pre-flight validation section not found"
fi

test_start "AC#4.2: User confirmed resumption checklist item"
if contains_pattern "user.*confirm\|confirm.*resumption\|approved.*resumption" "$TARGET_FILE"; then
    test_pass "AC#4.2: User confirmed resumption checklist item"
else
    test_fail "AC#4.2: User confirmed resumption checklist item" \
        "User confirmation checklist item not found"
fi

test_start "AC#4.3: Previous phases completion evidence checklist item"
if contains_pattern "completion.*evidence\|evidence.*previous\|previous.*phase.*complet" "$TARGET_FILE"; then
    test_pass "AC#4.3: Previous phases completion evidence checklist item"
else
    test_fail "AC#4.3: Previous phases completion evidence checklist item" \
        "Completion evidence checklist item not found"
fi

test_start "AC#4.4: No conflicting git changes checklist item"
if contains_pattern "conflicting.*git\|git.*conflict\|no.*git" "$TARGET_FILE"; then
    test_pass "AC#4.4: No conflicting git changes checklist item"
else
    test_fail "AC#4.4: No conflicting git changes checklist item" \
        "Git conflict/changes checklist item not found"
fi

test_start "AC#4.5: Story file readable checklist item"
if contains_pattern "story.*file.*readable\|readable.*story\|story.*exist" "$TARGET_FILE"; then
    test_pass "AC#4.5: Story file readable checklist item"
else
    test_fail "AC#4.5: Story file readable checklist item" \
        "Story file readability/existence checklist item not found"
fi

###############################################################################
# AC#5: Fresh Start vs Resume Recommendation
###############################################################################

echo ""
echo "=========================================================================="
echo "AC#5: Fresh Start vs Resume Recommendation"
echo "=========================================================================="

test_start "AC#5.1: Decision guidance section exists"
if contains_pattern "fresh.*start\|decision.*matrix\|recommendation\|when.*to.*resume" "$TARGET_FILE"; then
    test_pass "AC#5.1: Decision guidance section exists"
else
    test_fail "AC#5.1: Decision guidance section exists" \
        "Decision guidance/matrix section not found"
fi

test_start "AC#5.2: 'Start fresh' recommendation documented"
if contains_pattern "[Ss]tart.*fresh\|fresh.*start\|start.*over" "$TARGET_FILE"; then
    test_pass "AC#5.2: 'Start fresh' recommendation documented"
else
    test_fail "AC#5.2: 'Start fresh' recommendation documented" \
        "Start fresh recommendation not found"
fi

test_start "AC#5.3: Recommendation when state is unclear"
if contains_pattern "unclear.*state\|state.*unclear\|uncertain" "$TARGET_FILE"; then
    test_pass "AC#5.3: Recommendation when state is unclear"
else
    test_fail "AC#5.3: Recommendation when state is unclear" \
        "Unclear state recommendation not found"
fi

test_start "AC#5.4: Table or matrix format for scenarios"
if contains_pattern "^[|].*[|]$\|scenario\|condition" "$TARGET_FILE"; then
    test_pass "AC#5.4: Table or decision format for scenarios documented"
else
    test_fail "AC#5.4: Table or decision format for scenarios" \
        "Table/matrix format with scenarios not found (expected Markdown table with | separators)"
fi

###############################################################################
# Summary
###############################################################################

echo ""
echo "=========================================================================="
echo "TEST SUMMARY"
echo "=========================================================================="
echo ""
echo "Tests run:     $TESTS_RUN"
echo "Tests passed:  ${GREEN}$TESTS_PASSED${NC}"
echo "Tests failed:  ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    echo ""
    echo "Phase Resumption Protocol documentation is complete and well-structured."
    exit 0
else
    echo -e "${RED}$TESTS_FAILED test(s) failed.${NC}"
    echo ""
    echo "The Phase Resumption Protocol documentation is incomplete."
    echo "The following sections need to be added to $TARGET_FILE:"
    echo ""
    echo "1. User Detection Indicators"
    echo "   - Document the indicators users will notice when workflow interrupted"
    echo "   - Include TodoWrite status changes"
    echo "   - Include DoD completion percentage checks"
    echo "   - Include story status verification"
    echo "   - Include git commit detection"
    echo ""
    echo "2. User Recovery Command"
    echo "   - Provide template command for resuming /dev"
    echo "   - Include references to pending phases"
    echo "   - Include action phrase like 'Resume execution now'"
    echo ""
    echo "3. Claude Resumption Steps"
    echo "   - Document 5-6 numbered steps Claude must follow"
    echo "   - Include: Check TodoWrite, Verify Previous Phases, Load Reference,"
    echo "     Execute Remaining, Final Validation"
    echo ""
    echo "4. Resumption Validation Checklist"
    echo "   - Document checklist items for pre-flight validation"
    echo "   - Include: user confirmation, completion evidence, git conflicts,"
    echo "     story file readability"
    echo ""
    echo "5. Fresh Start vs Resume Recommendation"
    echo "   - Document decision guidance matrix"
    echo "   - Include 'Start fresh' recommendation for unclear state"
    echo "   - Include scenarios/conditions for each recommendation"
    echo ""
    exit 1
fi
