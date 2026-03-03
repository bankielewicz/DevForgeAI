#!/bin/bash
# Test: AC#5 - Existing FAILED Behavior Unchanged
# Story: STORY-345
# Status: RED (failing) - Test written before implementation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-qa/references/report-generation.md"

echo "=== AC#5: Existing FAILED Behavior Unchanged ==="
echo ""

# Test 1: Verify FAILED still generates gaps.json
echo "Test 1: FAILED status still generates gaps.json..."
if ! grep -q 'overall_status == "FAIL"' "$TARGET_FILE"; then
    echo "FAIL: FAILED status no longer triggers gap generation"
    echo "  Expected: IF overall_status == 'FAIL' still present"
    exit 1
fi

# Test 2: Verify CRITICAL severity has blocking: true
echo "Test 2: CRITICAL severity has blocking: true..."
if ! grep -q 'CRITICAL.*blocking.*true\|CRITICAL.*true' "$TARGET_FILE"; then
    echo "FAIL: CRITICAL severity not mapped to blocking: true"
    echo "  Expected: CRITICAL severity -> blocking: true"
    exit 1
fi

# Test 3: Verify HIGH severity has blocking: true
echo "Test 3: HIGH severity has blocking: true..."
if ! grep -q 'HIGH.*blocking.*true\|HIGH.*true' "$TARGET_FILE"; then
    echo "FAIL: HIGH severity not mapped to blocking: true"
    echo "  Expected: HIGH severity -> blocking: true"
    exit 1
fi

# Test 4: Verify qa_result FAILED documented
echo "Test 4: qa_result FAILED properly documented..."
if ! grep -q '"qa_result": "FAILED"\|qa_result.*FAILED' "$TARGET_FILE"; then
    echo "FAIL: qa_result FAILED not in schema example"
    echo "  Expected: Example showing qa_result: 'FAILED'"
    exit 1
fi

# Test 5: Verify gaps.json file path unchanged
echo "Test 5: gaps.json file path unchanged..."
if ! grep -q 'devforgeai/qa/reports/{story_id}-gaps.json\|{STORY-ID}-gaps.json' "$TARGET_FILE"; then
    echo "FAIL: gaps.json file path may have changed"
    echo "  Expected: devforgeai/qa/reports/{story_id}-gaps.json"
    exit 1
fi

# Test 6: Verify coverage_gaps, anti_pattern_violations, deferral_issues arrays exist
echo "Test 6: Existing gap categories preserved..."
for category in "coverage_gaps" "anti_pattern_violations" "deferral_issues"; do
    if ! grep -q "$category" "$TARGET_FILE"; then
        echo "FAIL: Gap category '$category' missing from schema"
        echo "  Expected: $category array in gaps.json"
        exit 1
    fi
done

echo ""
echo "PASS: AC#5 - Existing FAILED behavior unchanged"
exit 0
