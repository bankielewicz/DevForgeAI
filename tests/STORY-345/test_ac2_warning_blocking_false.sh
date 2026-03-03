#!/bin/bash
# Test: AC#2 - Warning Items Have blocking: false
# Story: STORY-345
# Status: RED (failing) - Test written before implementation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-qa/references/report-generation.md"

echo "=== AC#2: Warning Items Have blocking: false ==="
echo ""

# Test 1: Verify Step 3.5 includes MEDIUM/LOW violations in gap generation
echo "Test 1: Step 3.5 includes MEDIUM/LOW violations..."
STEP_35=$(sed -n '/## Step 3.5/,/## Step 3.6/p' "$TARGET_FILE")

# Current implementation only processes critical_violations + high_violations
# STORY-345 requires: Also include medium_violations and low_violations
if echo "$STEP_35" | grep -q 'FOR EACH violation in (critical_violations + high_violations):'; then
    if ! echo "$STEP_35" | grep -qE 'medium_violations|low_violations'; then
        echo "FAIL: Step 3.5 only processes CRITICAL/HIGH, not MEDIUM/LOW"
        echo "  Current: FOR EACH violation in (critical_violations + high_violations)"
        echo "  Required: Also process medium_violations and low_violations with blocking: false"
        exit 1
    fi
fi

# Test 2: Verify warning violations have explicit blocking: false assignment
echo "Test 2: Warning violations assigned blocking: false..."
if ! echo "$STEP_35" | grep -qE 'medium.*blocking.*false|low.*blocking.*false' -i; then
    echo "FAIL: No explicit blocking: false for MEDIUM/LOW in gap generation loop"
    echo "  Expected: Warning items explicitly set blocking: false"
    exit 1
fi

# Test 3: Verify gaps.json example shows non-blocking warning item
echo "Test 3: Schema example shows warning with blocking: false..."
SCHEMA=$(sed -n '/### gaps.json Schema/,/### /p' "$TARGET_FILE")
if ! echo "$SCHEMA" | grep -qE '"blocking": false'; then
    echo "FAIL: Schema example does not include blocking: false example"
    echo "  Expected: Example gap entry with blocking: false for warning item"
    exit 1
fi

echo ""
echo "PASS: AC#2 - Warning items correctly have blocking: false"
exit 0
