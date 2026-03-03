#!/bin/bash
# Test Runner: STORY-530 - Phase File TaskCreate Integration
# Generated: 2026-03-03
#
# Runs all 4 test files for STORY-530 acceptance criteria.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

TOTAL_PASS=0
TOTAL_FAIL=0

echo "=============================================="
echo "  STORY-530: Phase File TaskCreate Integration"
echo "=============================================="
echo ""

# AC#1: Section Presence (pytest)
echo "--- AC#1: Section Presence (pytest) ---"
cd "$PROJECT_ROOT"
export PYTHONPATH=".:$PYTHONPATH"
if python3 -m pytest "$SCRIPT_DIR/test_ac1_section_presence.py" -v --tb=short 2>&1; then
    ((TOTAL_PASS++))
else
    ((TOTAL_FAIL++))
fi
echo ""

# AC#2: Phase Filtering (bash)
echo "--- AC#2: Phase Filtering (bash) ---"
if bash "$SCRIPT_DIR/test_ac2_phase_filtering.sh" 2>&1; then
    ((TOTAL_PASS++))
else
    ((TOTAL_FAIL++))
fi
echo ""

# AC#3: TaskUpdate (bash)
echo "--- AC#3: TaskUpdate Completion (bash) ---"
if bash "$SCRIPT_DIR/test_ac3_taskupdate.sh" 2>&1; then
    ((TOTAL_PASS++))
else
    ((TOTAL_FAIL++))
fi
echo ""

# AC#4: Error Handling (pytest)
echo "--- AC#4: Error Handling (pytest) ---"
cd "$PROJECT_ROOT"
if python3 -m pytest "$SCRIPT_DIR/test_ac4_error_handling.py" -v --tb=short 2>&1; then
    ((TOTAL_PASS++))
else
    ((TOTAL_FAIL++))
fi
echo ""

echo "=============================================="
echo "  Summary: $TOTAL_PASS AC suites passed, $TOTAL_FAIL AC suites failed"
echo "=============================================="
[ "$TOTAL_FAIL" -eq 0 ] && exit 0 || exit 1
