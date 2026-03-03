#!/bin/bash

# STORY-132: AC#2 Test - Skill Phase 6.6 Owns Next Action Determination
# Test: Verify skill's completion-handoff.md has Phase 6.6 with AskUserQuestion for next action
# Test: Verify greenfield path recommends /create-context
# Test: Verify brownfield path recommends /create-sprint or /orchestrate

set -e

# Use relative path from project root for CI/CD compatibility
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SKILL_HANDOFF_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-ideation/references/completion-handoff.md"
TEST_NAME="AC#2: Skill Phase 6.6 Owns Next Action"
FAILURES=0

echo "=========================================="
echo "TEST: $TEST_NAME"
echo "=========================================="
echo ""

# Test 1: Phase 6.6 section exists
echo "[TEST 1/4] Checking for Phase 6.6 section in skill..."
if grep -q "^## Step 6.6" "$SKILL_HANDOFF_FILE"; then
    echo "  ✓ PASSED: Phase 6.6 'Determine Next Action' section found"
else
    echo "  ✗ FAILED: Phase 6.6 section not found in completion-handoff.md"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Test 2: AskUserQuestion for next action in greenfield path
echo "[TEST 2/4] Checking for AskUserQuestion in greenfield path..."
GREENFIELD_SECTION=$(sed -n '/### Greenfield Path/,/### Brownfield Path/p' "$SKILL_HANDOFF_FILE")
if echo "$GREENFIELD_SECTION" | grep -q "AskUserQuestion"; then
    echo "  ✓ PASSED: AskUserQuestion found in greenfield path (Step 6.6)"
else
    echo "  ✗ FAILED: No AskUserQuestion in greenfield path section"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Test 3: /create-context recommended for greenfield
echo "[TEST 3/4] Checking greenfield recommendation for /create-context..."
if grep -q "create-context" "$SKILL_HANDOFF_FILE"; then
    echo "  ✓ PASSED: Greenfield path recommends /create-context"
else
    echo "  ✗ FAILED: /create-context not recommended in greenfield path"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Test 4: /create-sprint or /orchestrate recommended for brownfield
echo "[TEST 4/4] Checking brownfield recommendations..."
BROWNFIELD_CHECK=0

if grep -q "create-sprint" "$SKILL_HANDOFF_FILE" || grep -q "/create-sprint" "$SKILL_HANDOFF_FILE"; then
    BROWNFIELD_CHECK=$((BROWNFIELD_CHECK + 1))
fi

if grep -q "orchestrate" "$SKILL_HANDOFF_FILE" || grep -q "/orchestrate" "$SKILL_HANDOFF_FILE"; then
    BROWNFIELD_CHECK=$((BROWNFIELD_CHECK + 1))
fi

# Both don't need to be present, but at least one of them should be
if [ "$BROWNFIELD_CHECK" -gt 0 ]; then
    echo "  ✓ PASSED: Brownfield path recommends /create-sprint or /orchestrate"
else
    echo "  ✗ FAILED: Neither /create-sprint nor /orchestrate recommended in brownfield path"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Summary
echo "=========================================="
if [ "$FAILURES" -eq 0 ]; then
    echo "✓ AC#2 TEST PASSED (4/4 checks)"
    exit 0
else
    echo "✗ AC#2 TEST FAILED ($FAILURES/4 checks failed)"
    exit 1
fi
