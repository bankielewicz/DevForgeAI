#!/bin/bash

# STORY-132: AC#3 Test - Command Shows Brief Confirmation Only
# Test: Verify command has Phase 3 that delegates to ideation-result-interpreter
# Test: Verify no AskUserQuestion in command after skill invocation (Phase 2.2)
# Test: Verify command displays brief summary without re-asking about next action

set -e

# Use relative path from project root for CI/CD compatibility
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
COMMAND_FILE="$PROJECT_ROOT/.claude/commands/ideate.md"
TEST_NAME="AC#3: Command Shows Brief Confirmation Only"
FAILURES=0

echo "=========================================="
echo "TEST: $TEST_NAME"
echo "=========================================="
echo ""

# Test 1: Phase 3 exists and delegates to ideation-result-interpreter
echo "[TEST 1/3] Checking for Phase 3: Result Interpretation..."
if grep -q "^## Phase 3" "$COMMAND_FILE"; then
    echo "  ✓ PASSED: Phase 3 'Result Interpretation' section exists"

    # Verify it mentions ideation-result-interpreter
    PHASE_3_CONTENT=$(sed -n '/^## Phase 3/,/^## /p' "$COMMAND_FILE")
    if echo "$PHASE_3_CONTENT" | grep -q "ideation-result-interpreter"; then
        echo "  ✓ PASSED: Phase 3 delegates to ideation-result-interpreter subagent"
    else
        echo "  ✗ FAILED: Phase 3 does not mention ideation-result-interpreter delegation"
        FAILURES=$((FAILURES + 1))
    fi
else
    echo "  ✗ FAILED: Phase 3 'Result Interpretation' section not found"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Test 2: No AskUserQuestion in Phase 2.2 (after skill invocation)
echo "[TEST 2/3] Verifying no AskUserQuestion after skill invocation (Phase 2.2)..."
PHASE_2_2_CONTENT=$(sed -n '/^## Phase 2\.2: Skill Invocation/,/^## /p' "$COMMAND_FILE")

# Count AskUserQuestion in Phase 2.2
PHASE_2_2_ASK_COUNT=$(echo "$PHASE_2_2_CONTENT" | grep -c "AskUserQuestion" || true)

if [ "$PHASE_2_2_ASK_COUNT" -eq 0 ]; then
    echo "  ✓ PASSED: No AskUserQuestion in Phase 2.2 post-skill section"
else
    echo "  ✗ FAILED: Found $PHASE_2_2_ASK_COUNT AskUserQuestion calls in Phase 2.2"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Test 3: Verify brief confirmation message exists
# The command should display result.display.template from the subagent
echo "[TEST 3/3] Checking for brief confirmation pattern after Phase 3..."
if grep -q "Display: result.display.template" "$COMMAND_FILE"; then
    echo "  ✓ PASSED: Command displays result template (brief confirmation pattern)"
elif grep -q "Display.*result" "$COMMAND_FILE"; then
    echo "  ✓ PASSED: Command displays result output (brief confirmation pattern)"
else
    echo "  ✗ FAILED: No clear confirmation display pattern found in Phase 3"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Summary
echo "=========================================="
if [ "$FAILURES" -eq 0 ]; then
    echo "✓ AC#3 TEST PASSED (3/3 checks)"
    exit 0
else
    echo "✗ AC#3 TEST FAILED ($FAILURES/3 checks failed)"
    exit 1
fi
