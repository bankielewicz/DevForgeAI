#!/usr/bin/env bash
# Integration test: STORY-518 - Phase 1.5 structure integrity
# Verifies QA SKILL.md Phase 1.5 has correct structure in both src/ and operational paths.
# Exit 0 on PASS, exit 1 on FAIL.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC_SKILL="$PROJECT_ROOT/src/claude/skills/devforgeai-qa/SKILL.md"
OPS_SKILL="$PROJECT_ROOT/.claude/skills/devforgeai-qa/SKILL.md"

PASS=0
FAIL=0

fail() {
    echo "FAIL: $1"
    FAIL=$((FAIL + 1))
}

pass() {
    echo "PASS: $1"
    PASS=$((PASS + 1))
}

# --- Test 1: Phase 1.5 has exactly 6 steps (Step 1.5.1 through 1.5.6) ---
STEP_COUNT=$(grep -c '^### Step 1\.5\.' "$SRC_SKILL")
if [ "$STEP_COUNT" -eq 6 ]; then
    pass "Phase 1.5 has exactly 6 steps (found $STEP_COUNT)"
else
    fail "Phase 1.5 expected 6 steps, found $STEP_COUNT"
fi

# --- Test 2: Phase 1.5 Completion Checklist references test integrity verification ---
# Look for "test integrity verification" within the Phase 1.5 Completion Checklist
if grep -q 'test integrity verification' "$SRC_SKILL"; then
    pass "Phase 1.5 Completion Checklist references test integrity verification"
else
    fail "Phase 1.5 Completion Checklist missing 'test integrity verification' reference"
fi

# --- Test 3: Both src/ and operational files contain test_integrity_verification ---
SRC_HAS_TIV=$(grep -c 'test_integrity_verification' "$SRC_SKILL" || true)
OPS_HAS_TIV=$(grep -c 'test_integrity_verification' "$OPS_SKILL" || true)

if [ "$SRC_HAS_TIV" -gt 0 ] && [ "$OPS_HAS_TIV" -gt 0 ]; then
    pass "Both src/ and operational files contain 'test_integrity_verification'"
else
    fail "test_integrity_verification missing: src=$SRC_HAS_TIV ops=$OPS_HAS_TIV"
fi

# --- Test 4: Both src/ and operational files contain pre-STORY-502 ---
SRC_HAS_PRE=$(grep -c 'pre-STORY-502' "$SRC_SKILL" || true)
OPS_HAS_PRE=$(grep -c 'pre-STORY-502' "$OPS_SKILL" || true)

if [ "$SRC_HAS_PRE" -gt 0 ] && [ "$OPS_HAS_PRE" -gt 0 ]; then
    pass "Both src/ and operational files contain 'pre-STORY-502'"
else
    fail "pre-STORY-502 missing: src=$SRC_HAS_PRE ops=$OPS_HAS_PRE"
fi

# --- Summary ---
echo ""
echo "=== Integration Test Summary ==="
echo "PASSED: $PASS"
echo "FAILED: $FAIL"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi

exit 0
