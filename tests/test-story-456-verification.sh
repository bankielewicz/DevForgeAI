#!/bin/bash
# Test: STORY-456 - AC Verification Script
# Story: STORY-456 (documentation story - CoT guidance, per-phase loading, phase boundaries)
# Generated: 2026-02-19
# TDD Phase: RED - all tests FAIL against unmodified src/ files
#
# Usage: bash tests/test-story-456-verification.sh [project-root]
# Default project root: /mnt/c/Projects/DevForgeAI2

# === Test Configuration ===
PROJECT_ROOT="${1:-/mnt/c/Projects/DevForgeAI2}"
PASSED=0
FAILED=0

REQ_WORKFLOW="$PROJECT_ROOT/src/claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md"
SKILL_MD="$PROJECT_ROOT/src/claude/skills/discovering-requirements/SKILL.md"
EXAMPLES_MD="$PROJECT_ROOT/src/claude/skills/discovering-requirements/references/examples.md"

echo "=================================================="
echo "  STORY-456 Verification Tests"
echo "  Project root: $PROJECT_ROOT"
echo "=================================================="

# === Helper ===
run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

# === Preflight: Verify target files exist ===
echo ""
echo "--- Preflight: Target File Existence ---"

for f in "$REQ_WORKFLOW" "$SKILL_MD" "$EXAMPLES_MD"; do
    if [ ! -f "$f" ]; then
        echo "  ERROR: Required file not found: $f"
        echo "  ABORT: Cannot run tests without target files."
        exit 2
    fi
done
echo "  OK: All 3 target files found"

# ============================================================
# AC#1: CoT guidance in requirements-elicitation-workflow.md
# ============================================================
echo ""
echo "--- AC#1: CoT Guidance (requirements-elicitation-workflow.md) ---"

# Test: <thinking> opening tag present
grep -q "<thinking>" "$REQ_WORKFLOW"
run_test "AC1-T1: <thinking> opening tag present" $?

# Test: </thinking> closing tag present
grep -q "</thinking>" "$REQ_WORKFLOW"
run_test "AC1-T2: </thinking> closing tag present" $?

# Test: Prioritization factor "Business value" present
grep -q "Business value" "$REQ_WORKFLOW"
run_test "AC1-T3: Prioritization factor 'Business value' present" $?

# Test: Prioritization factor "Technical feasibility" present
grep -q "Technical feasibility" "$REQ_WORKFLOW"
run_test "AC1-T4: Prioritization factor 'Technical feasibility' present" $?

# Test: Prioritization factor "Dependencies" present
grep -q "Dependencies" "$REQ_WORKFLOW"
run_test "AC1-T5: Prioritization factor 'Dependencies' present" $?

# Test: Prioritization factor "User impact" present
grep -q "User impact" "$REQ_WORKFLOW"
run_test "AC1-T6: Prioritization factor 'User impact' present" $?

# Test: MoSCoW "Must-Have" present
grep -q "Must-Have" "$REQ_WORKFLOW"
run_test "AC1-T7: MoSCoW keyword 'Must-Have' present" $?

# Test: MoSCoW "Should-Have" present
grep -q "Should-Have" "$REQ_WORKFLOW"
run_test "AC1-T8: MoSCoW keyword 'Should-Have' present" $?

# Test: MoSCoW "Could-Have" present
grep -q "Could-Have" "$REQ_WORKFLOW"
run_test "AC1-T9: MoSCoW keyword 'Could-Have' present" $?

# Test: MoSCoW "Won't-Have" (apostrophe variant) present
grep -qE "Won.t-Have" "$REQ_WORKFLOW"
run_test "AC1-T10: MoSCoW keyword \"Won't-Have\" present" $?

# Test: No content deleted - line count >= 395 (baseline)
REQ_LINES=$(wc -l < "$REQ_WORKFLOW")
[ "$REQ_LINES" -ge 395 ]
run_test "AC1-T11: No content deleted (line count $REQ_LINES >= 395)" $?

# ============================================================
# AC#2: Per-phase loading in SKILL.md
# ============================================================
echo ""
echo "--- AC#2: Per-Phase Loading (SKILL.md) ---"

# Test: Phase 1 section has Read() with offset for examples.md
grep -A 50 "### Phase 1:" "$SKILL_MD" | grep -q "examples.md.*offset"
run_test "AC2-T1: Phase 1 section has Read(examples.md, offset=...)" $?

# Test: Phase 2 section has Read() with offset for examples.md
grep -A 50 "### Phase 2:" "$SKILL_MD" | grep -q "examples.md.*offset"
run_test "AC2-T2: Phase 2 section has Read(examples.md, offset=...)" $?

# Test: Phase 3 section has Read() with offset for examples.md
grep -A 50 "### Phase 3:" "$SKILL_MD" | grep -q "examples.md.*offset"
run_test "AC2-T3: Phase 3 section has Read(examples.md, offset=...)" $?

# Test: Total offset-based Read() calls for examples.md >= 3
OFFSET_COUNT=$(grep -c "examples\.md.*offset" "$SKILL_MD")
[ "$OFFSET_COUNT" -ge 3 ]
run_test "AC2-T4: At least 3 offset-based Read() calls for examples.md (found: $OFFSET_COUNT)" $?

# Test: Old single upfront load (without offset/limit) is REMOVED
# A line containing examples.md that does NOT contain offset or limit should not exist
UNQUALIFIED=$(grep "examples\.md" "$SKILL_MD" | grep -v "offset" | grep -v "limit" | grep -c "Read(")
[ "$UNQUALIFIED" -eq 0 ]
run_test "AC2-T5: Old single upfront load (no offset/limit) is removed (found: $UNQUALIFIED)" $?

# Test: SKILL.md line count < 500
SKILL_LINES=$(wc -l < "$SKILL_MD")
[ "$SKILL_LINES" -lt 500 ]
run_test "AC2-T6: SKILL.md line count $SKILL_LINES < 500" $?

# ============================================================
# AC#3: Phase boundary markers in examples.md
# ============================================================
echo ""
echo "--- AC#3: Phase Boundaries (examples.md) ---"

# Test: At least 3 <example> opening tags
EXAMPLE_OPEN=$(grep -c "<example " "$EXAMPLES_MD")
[ "$EXAMPLE_OPEN" -ge 3 ]
run_test "AC3-T1: At least 3 <example> opening tags (found: $EXAMPLE_OPEN)" $?

# Test: At least 3 </example> closing tags
EXAMPLE_CLOSE=$(grep -c "</example>" "$EXAMPLES_MD")
[ "$EXAMPLE_CLOSE" -ge 3 ]
run_test "AC3-T2: At least 3 </example> closing tags (found: $EXAMPLE_CLOSE)" $?

# Test: <example> and </example> counts are equal (balanced)
[ "$EXAMPLE_OPEN" -eq "$EXAMPLE_CLOSE" ]
run_test "AC3-T3: <example> tags balanced ($EXAMPLE_OPEN open = $EXAMPLE_CLOSE close)" $?
# Note: Opening tags use <example name="..."> format (with attributes)

# Test: At least 2 --- section separators
SEP_COUNT=$(grep -cE "^---$" "$EXAMPLES_MD")
[ "$SEP_COUNT" -ge 2 ]
run_test "AC3-T4: At least 2 '---' section separators (found: $SEP_COUNT)" $?

# Test: <example> tag appears within first 90 lines (Phase 1 boundary)
head -90 "$EXAMPLES_MD" | grep -q "<example "
run_test "AC3-T5: Phase 1 <example> tag appears within first 90 lines" $?

# Test: <example> tag appears between lines 85-235 (Phase 2 boundary)
sed -n '85,235p' "$EXAMPLES_MD" | grep -q "<example "
run_test "AC3-T6: Phase 2 <example> tag appears between lines 85-235" $?

# Test: <example> tag appears after line 230 (Phase 3 boundary)
tail -n +230 "$EXAMPLES_MD" | grep -q "<example "
run_test "AC3-T7: Phase 3 <example> tag appears after line 230" $?

# Test: File line count >= 320 (no deletions from 320-line baseline)
EXAMPLES_LINES=$(wc -l < "$EXAMPLES_MD")
[ "$EXAMPLES_LINES" -ge 320 ]
run_test "AC3-T8: No content deleted (line count $EXAMPLES_LINES >= 320)" $?

# ============================================================
# Summary
# ============================================================
echo ""
echo "=================================================="
TOTAL=$((PASSED + FAILED))
echo "  Results: $PASSED/$TOTAL passed, $FAILED failed"
echo "=================================================="

if [ "$FAILED" -gt 0 ]; then
    echo "  STATUS: FAIL (RED phase - implementation required)"
    exit 1
else
    echo "  STATUS: PASS (GREEN phase - all ACs verified)"
    exit 0
fi
