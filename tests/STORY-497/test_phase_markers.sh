#!/bin/bash
# Test: Phase Marker Protocol for Release Skill
# Story: STORY-497
# Generated: 2026-02-24
# TDD Phase: RED (all tests expected to FAIL against current SKILL.md)

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-release/SKILL.md"

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

echo "============================================"
echo "STORY-497: Phase Marker Protocol Tests"
echo "Target: $TARGET_FILE"
echo "============================================"
echo ""

# Verify target file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "FATAL: Target file not found: $TARGET_FILE"
    exit 2
fi

# === AC#1: Pre-Flight Glob() Verification at Phase Entry ===
echo "--- AC#1: Pre-Flight Glob() at Phase Entry ---"

# Test 1.1: Phases 2-7 must have Glob check for previous phase marker
COUNT=$(grep -c 'Glob(pattern="devforgeai/workflows/\.release-phase-' "$TARGET_FILE" 2>/dev/null | tail -1)
COUNT=${COUNT:-0}
[ "$COUNT" -ge 6 ]
run_test "AC1: At least 6 Glob checks for prior phase markers (phases 2-7), found $COUNT" $?

# Test 1.2: HALT message when marker missing
grep -q 'HALT.*missing.*marker\|HALT.*prerequisite.*phase\|HALT.*prior phase' "$TARGET_FILE" 2>/dev/null
run_test "AC1: HALT message for missing prerequisite phase marker" $?

echo ""

# === AC#2: CHECKPOINT MANDATORY Markers ===
echo "--- AC#2: CHECKPOINT MANDATORY Markers ---"

# Test 2.1: Exactly 7 CHECKPOINT: MANDATORY markers (one per phase)
COUNT=$(grep -c 'CHECKPOINT: MANDATORY' "$TARGET_FILE" 2>/dev/null | tail -1)
COUNT=${COUNT:-0}
[ "$COUNT" -eq 7 ]
run_test "AC2: Exactly 7 CHECKPOINT: MANDATORY markers, found $COUNT" $?

# Test 2.2: Each CHECKPOINT is followed by a Read() call
# Check that Read() appears within 3 lines after each CHECKPOINT
CHECKPOINT_LINES=$(grep -n 'CHECKPOINT: MANDATORY' "$TARGET_FILE" 2>/dev/null | cut -d: -f1)
ALL_HAVE_READ=true
for LINE in $CHECKPOINT_LINES; do
    END=$((LINE + 3))
    sed -n "${LINE},${END}p" "$TARGET_FILE" | grep -q 'Read(file_path='
    if [ $? -ne 0 ]; then
        ALL_HAVE_READ=false
        break
    fi
done
[ "$ALL_HAVE_READ" = "true" ] && [ -n "$CHECKPOINT_LINES" ]
run_test "AC2: Read() follows each CHECKPOINT: MANDATORY marker" $?

echo ""

# === AC#3: Marker File Write at Phase Exit ===
echo "--- AC#3: Marker File Write at Phase Exit ---"

# Test 3.1: All 7 phases write a .release-phase-N.marker file
COUNT=$(grep -c 'Write(file_path="devforgeai/workflows/\.release-phase-' "$TARGET_FILE" 2>/dev/null | tail -1)
COUNT=${COUNT:-0}
[ "$COUNT" -ge 7 ]
run_test "AC3: At least 7 marker Write() calls (one per phase), found $COUNT" $?

# Test 3.2: Marker content includes required fields (phase, status, reason, timestamp)
grep -q 'status:.*complete\|status:.*skipped' "$TARGET_FILE" 2>/dev/null
run_test "AC3: Marker content includes status field" $?

grep -q 'reason:' "$TARGET_FILE" 2>/dev/null
run_test "AC3: Marker content includes reason field" $?

grep -q 'timestamp:' "$TARGET_FILE" 2>/dev/null
run_test "AC3: Marker content includes timestamp field" $?

echo ""

# === AC#4: Skipped Phases Write Markers with status=skipped ===
echo "--- AC#4: Skipped Phase Markers ---"

grep -q 'status: skipped' "$TARGET_FILE" 2>/dev/null
run_test "AC4: At least one skip path writes marker with 'status: skipped'" $?

grep -q 'status: skipped' "$TARGET_FILE" 2>/dev/null && grep -q 'reason:.*skip\|reason:.*not applicable\|reason:.*N/A' "$TARGET_FILE" 2>/dev/null
run_test "AC4: Skipped marker includes reason for skipping" $?

echo ""

# === AC#5: Phase 1 Stale Marker Cleanup ===
echo "--- AC#5: Phase 1 Stale Marker Cleanup ---"

grep -q 'Glob(pattern="devforgeai/workflows/\.release-phase-\*\.marker")' "$TARGET_FILE" 2>/dev/null
run_test "AC5: Phase 1 checks for stale .release-phase-*.marker files" $?

grep -q 'stale.*marker\|cleanup.*marker\|previous.*release.*marker' "$TARGET_FILE" 2>/dev/null
run_test "AC5: Phase 1 references stale marker cleanup" $?

echo ""

# === AC#6: Pattern Matches QA Skill (3 mechanisms per phase) ===
echo "--- AC#6: All 3 Mechanisms Per Phase ---"

# For each phase 1-7, check all three mechanisms exist
for PHASE_NUM in 1 2 3 4 5 6 7; do
    # Extract section for this phase (between Phase N and Phase N+1 headers)
    NEXT=$((PHASE_NUM + 1))
    PHASE_SECTION=$(sed -n "/Phase ${PHASE_NUM}[^0-9]/,/Phase ${NEXT}[^0-9]\|^---$/p" "$TARGET_FILE" 2>/dev/null)

    HAS_CHECKPOINT=false
    HAS_WRITE=false

    echo "$PHASE_SECTION" | grep -q 'CHECKPOINT: MANDATORY' && HAS_CHECKPOINT=true
    echo "$PHASE_SECTION" | grep -q 'Write(file_path="devforgeai/workflows/\.release-phase-' && HAS_WRITE=true

    [ "$HAS_CHECKPOINT" = "true" ] && [ "$HAS_WRITE" = "true" ]
    run_test "AC6: Phase $PHASE_NUM has CHECKPOINT + Write markers" $?
done

echo ""

# === Summary ===
echo "============================================"
echo "Results: $PASSED passed, $FAILED failed"
echo "Total:   $((PASSED + FAILED)) tests"
echo "============================================"

[ $FAILED -eq 0 ] && exit 0 || exit 1
