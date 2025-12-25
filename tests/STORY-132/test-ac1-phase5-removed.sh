#!/bin/bash

# STORY-132: AC#1 Test - Command Phase 5 Removed from /ideate
# Test: Verify no "Phase 5" header exists in ideate.md
# Test: Verify no "Verify Next Steps" text in ideate.md
# Test: Verify no "Ready to proceed" text in ideate.md
# Test: Verify no duplicate AskUserQuestion for next-action after skill returns

set -e

# Use relative path from project root for CI/CD compatibility
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
COMMAND_FILE="$PROJECT_ROOT/.claude/commands/ideate.md"
TEST_NAME="AC#1: Command Phase 5 Removed"
FAILURES=0

echo "=========================================="
echo "TEST: $TEST_NAME"
echo "=========================================="
echo ""

# Test 1: No "## Phase 5" header
echo "[TEST 1/4] Checking for '## Phase 5' header removal..."
if grep -q "^## Phase 5" "$COMMAND_FILE"; then
    echo "  ✗ FAILED: '## Phase 5' header still exists in ideate.md"
    FAILURES=$((FAILURES + 1))
else
    echo "  ✓ PASSED: No '## Phase 5' header found"
fi
echo ""

# Test 2: No "Verify Next Steps" text
echo "[TEST 2/4] Checking for 'Verify Next Steps' removal..."
if grep -i "Verify Next Steps" "$COMMAND_FILE"; then
    echo "  ✗ FAILED: 'Verify Next Steps' text still exists in ideate.md"
    FAILURES=$((FAILURES + 1))
else
    echo "  ✓ PASSED: No 'Verify Next Steps' text found"
fi
echo ""

# Test 3: No "Ready to proceed" text in next-action context
echo "[TEST 3/4] Checking for 'Ready to proceed' removal..."
if grep "Ready to proceed" "$COMMAND_FILE"; then
    echo "  ✗ FAILED: 'Ready to proceed' text still exists in ideate.md"
    FAILURES=$((FAILURES + 1))
else
    echo "  ✓ PASSED: No 'Ready to proceed' text found"
fi
echo ""

# Test 4: Verify no AskUserQuestion for next-action after Phase 2.2 skill return
echo "[TEST 4/4] Checking for duplicate AskUserQuestion after skill invocation..."
# Extract content from after "## Phase 2.2: Skill Invocation" to "## Phase 3" or end of file
# Count AskUserQuestion occurrences in that section
PHASE_2_2_CONTENT=$(sed -n '/^## Phase 2\.2: Skill Invocation/,/^## /p' "$COMMAND_FILE")

# Count total AskUserQuestion in this section
ASK_COUNT=$(echo "$PHASE_2_2_CONTENT" | grep -c "AskUserQuestion" || true)

# The only valid AskUserQuestion in command should be in Phase 0 and Phase 1 (brainstorm and business idea)
# Phase 2.2 should have 0 AskUserQuestion calls (skill handles next-action)
if [ "$ASK_COUNT" -gt 0 ]; then
    echo "  ✗ FAILED: Found $ASK_COUNT AskUserQuestion calls in Phase 2.2 (after skill invocation)"
    echo "    Phase 2.2 should NOT contain AskUserQuestion for next-action (skill handles this)"
    FAILURES=$((FAILURES + 1))
else
    echo "  ✓ PASSED: No duplicate AskUserQuestion in Phase 2.2 post-skill section"
fi
echo ""

# Summary
echo "=========================================="
if [ "$FAILURES" -eq 0 ]; then
    echo "✓ AC#1 TEST PASSED (4/4 checks)"
    exit 0
else
    echo "✗ AC#1 TEST FAILED ($FAILURES/4 checks failed)"
    exit 1
fi
