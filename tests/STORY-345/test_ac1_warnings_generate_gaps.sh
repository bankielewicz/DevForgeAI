#!/bin/bash
# Test: AC#1 - gaps.json Generated for PASS WITH WARNINGS
# Story: STORY-345
# Status: RED (failing) - Test written before implementation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-qa/references/report-generation.md"

echo "=== AC#1: gaps.json Generated for PASS WITH WARNINGS ==="
echo ""

# Test 1: Verify generation trigger EXPLICITLY includes PASS WITH WARNINGS
echo "Test 1: Step 3.5 generation condition includes PASS WITH WARNINGS..."
STEP_35=$(sed -n '/## Step 3.5/,/## Step 3.6/p' "$TARGET_FILE")

# The current implementation only checks for FAIL
# STORY-345 requires: IF overall_status == "FAIL" OR overall_status == "PASS WITH WARNINGS"
if echo "$STEP_35" | grep -qE 'IF overall_status == "FAIL":$'; then
    # Check if PASS WITH WARNINGS is ALSO in the condition
    if ! echo "$STEP_35" | grep -qE 'overall_status == "PASS WITH WARNINGS".*gaps_data|IF.*FAIL.*OR.*PASS WITH WARNINGS'; then
        echo "FAIL: Step 3.5 only generates gaps.json for FAIL, not PASS WITH WARNINGS"
        echo "  Current: IF overall_status == 'FAIL':"
        echo "  Required: IF overall_status == 'FAIL' OR overall_status == 'PASS WITH WARNINGS':"
        exit 1
    fi
fi

# Test 2: Verify PASS WITH WARNINGS is in generation block (not just archive block)
echo "Test 2: PASS WITH WARNINGS creates gaps.json (not just archives)..."
# Step 3.5 should create gaps, Step 3.6 archives. Both "PASS WITH WARNINGS" and "Write" must be in Step 3.5
HAS_WARNINGS_TRIGGER=$(echo "$STEP_35" | grep -c 'PASS WITH WARNINGS')
HAS_WRITE=$(echo "$STEP_35" | grep -c 'Write.*gaps\.json')
if [[ "$HAS_WARNINGS_TRIGGER" -eq 0 ]] || [[ "$HAS_WRITE" -eq 0 ]]; then
    echo "FAIL: Step 3.5 missing PASS WITH WARNINGS trigger or Write command"
    echo "  PASS WITH WARNINGS occurrences: $HAS_WARNINGS_TRIGGER"
    echo "  Write gaps.json occurrences: $HAS_WRITE"
    exit 1
fi

# Test 3: Verify qa_result can be set to "PASS WITH WARNINGS" in gaps_data
echo "Test 3: gaps_data includes qa_result = PASS WITH WARNINGS..."
if ! echo "$STEP_35" | grep -qE '"qa_result".*"PASS WITH WARNINGS"|qa_result.*PASS WITH WARNINGS'; then
    echo "FAIL: gaps_data does not show qa_result set to PASS WITH WARNINGS"
    echo "  Expected: qa_result: 'PASS WITH WARNINGS' when warnings present"
    exit 1
fi

echo ""
echo "PASS: AC#1 - gaps.json generation triggers for PASS WITH WARNINGS"
exit 0
