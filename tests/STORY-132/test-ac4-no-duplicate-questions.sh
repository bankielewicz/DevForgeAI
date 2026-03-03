#!/bin/bash

# STORY-132: AC#4 Test - No Duplication of Questions Across Command-Skill Boundary
# Test: Count AskUserQuestion occurrences in ideate.md (should be ≤2: brainstorm, business idea)
# Test: Verify no next-action AskUserQuestion in command post-skill-invocation sections
# Test: Confirm next-action question comes from skill only (Phase 6.6)

set -e

# Use relative path from project root for CI/CD compatibility
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
COMMAND_FILE="$PROJECT_ROOT/.claude/commands/ideate.md"
SKILL_HANDOFF_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-ideation/references/completion-handoff.md"
TEST_NAME="AC#4: No Duplicate Next-Action Questions"
FAILURES=0

echo "=========================================="
echo "TEST: $TEST_NAME"
echo "=========================================="
echo ""

# Test 1: Count AskUserQuestion in command (should be ≤2)
echo "[TEST 1/3] Counting AskUserQuestion calls in ideate.md..."
# Count only direct function calls: AskUserQuestion( pattern
TOTAL_ASK_COUNT=$(grep -c "^AskUserQuestion(" "$COMMAND_FILE" || true)

echo "  Found $TOTAL_ASK_COUNT AskUserQuestion calls total"

# Valid locations are:
# 1. Phase 0: Brainstorm selection (1 question)
# 2. Phase 1: Business idea input if no arguments (1 question)
# Maximum should be 2 in command (any more means duplicate next-action question)

if [ "$TOTAL_ASK_COUNT" -le 2 ]; then
    echo "  ✓ PASSED: Maximum 2 AskUserQuestion calls in command ($TOTAL_ASK_COUNT found)"
else
    echo "  ✗ FAILED: Too many AskUserQuestion calls ($TOTAL_ASK_COUNT > 2)"
    echo "    Command should only have: brainstorm selection + business idea input"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Test 2: Verify AskUserQuestion only in Phase 0 and Phase 1
echo "[TEST 2/3] Verifying AskUserQuestion locations..."

# Extract Phase 0 and Phase 1 content
PHASE_0_1_CONTENT=$(sed -n '/^## Phase 0/,/^## Phase 2/p' "$COMMAND_FILE")
PHASE_0_1_ASK_COUNT=$(echo "$PHASE_0_1_CONTENT" | grep -c "^AskUserQuestion(" || true)

# Extract content from Phase 2.2 onwards (should have 0 AskUserQuestion)
PHASE_2_PLUS_CONTENT=$(sed -n '/^## Phase 2\.2/,/^## Error Handling/p' "$COMMAND_FILE")
PHASE_2_PLUS_ASK_COUNT=$(echo "$PHASE_2_PLUS_CONTENT" | grep -c "^AskUserQuestion(" || true)

if [ "$PHASE_2_PLUS_ASK_COUNT" -eq 0 ]; then
    echo "  ✓ PASSED: No AskUserQuestion in Phase 2+ (post-skill-invocation)"
    echo "    AskUserQuestion calls found in Phase 0-1: $PHASE_0_1_ASK_COUNT"
else
    echo "  ✗ FAILED: Found $PHASE_2_PLUS_ASK_COUNT AskUserQuestion calls in Phase 2+"
    echo "    Next-action question should come from skill only (Phase 6.6)"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Test 3: Verify skill owns next-action AskUserQuestion
echo "[TEST 3/3] Verifying skill Phase 6.6 owns next-action question..."

# Check skill has AskUserQuestion for next action
SKILL_GREENFIELD=$(sed -n '/### Greenfield Path/,/### Brownfield Path/p' "$SKILL_HANDOFF_FILE")
SKILL_BROWNFIELD=$(sed -n '/### Brownfield Path/,/^---/p' "$SKILL_HANDOFF_FILE" | head -50)

GREENFIELD_HAS_ASK=$(echo "$SKILL_GREENFIELD" | grep -c "AskUserQuestion" || true)
BROWNFIELD_HAS_ASK=$(echo "$SKILL_BROWNFIELD" | grep -c "AskUserQuestion" || true)

if [ "$GREENFIELD_HAS_ASK" -gt 0 ] && [ "$BROWNFIELD_HAS_ASK" -gt 0 ]; then
    echo "  ✓ PASSED: Skill Phase 6.6 asks next-action question"
    echo "    Greenfield path: $GREENFIELD_HAS_ASK AskUserQuestion(s)"
    echo "    Brownfield path: $BROWNFIELD_HAS_ASK AskUserQuestion(s)"
else
    echo "  ✗ FAILED: Skill Phase 6.6 missing AskUserQuestion for next action"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Summary
echo "=========================================="
if [ "$FAILURES" -eq 0 ]; then
    echo "✓ AC#4 TEST PASSED (3/3 checks)"
    exit 0
else
    echo "✗ AC#4 TEST FAILED ($FAILURES/3 checks failed)"
    exit 1
fi
