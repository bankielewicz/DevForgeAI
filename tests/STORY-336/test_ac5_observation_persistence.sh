#!/bin/bash
# Test: AC#5 - Observation Persistence After Phase Completion
# Story: STORY-336
# Expected: FAIL (RED phase) - Persistence instructions not implemented yet

set -e

PHASE02=".claude/skills/devforgeai-development/phases/phase-02-test-first.md"
PHASE03=".claude/skills/devforgeai-development/phases/phase-03-implementation.md"
PHASE04=".claude/skills/devforgeai-development/phases/phase-04-refactoring.md"
TEST_NAME="AC5: Observation Persistence"

echo "=== $TEST_NAME ==="

# Test 1: Verify "append" semantics (not overwrite) documented
echo "Test 1: Checking for 'append' to observations array..."
FOUND_APPEND=false
for f in $PHASE02 $PHASE03 $PHASE04; do
    if grep -qi "append.*observations\|observations.*append" "$f"; then
        FOUND_APPEND=true
        break
    fi
done

if [ "$FOUND_APPEND" = true ]; then
    echo "  PASS: Append semantics found"
else
    echo "  FAIL: Append to observations[] not documented"
    exit 1
fi

# Test 2: Verify phase-state.json referenced in all phases
echo "Test 2: Checking phase-state.json referenced in all phases..."
for f in $PHASE02 $PHASE03 $PHASE04; do
    if ! grep -q "phase-state.json" "$f"; then
        echo "  FAIL: phase-state.json not referenced in $f"
        exit 1
    fi
done
echo "  PASS: phase-state.json referenced in all phases"

# Test 3: Verify observations array referenced
echo "Test 3: Checking observations[] array referenced..."
FOUND_OBS_ARRAY=false
for f in $PHASE02 $PHASE03 $PHASE04; do
    if grep -q "observations\[\]" "$f"; then
        FOUND_OBS_ARRAY=true
        break
    fi
done

if [ "$FOUND_OBS_ARRAY" = true ]; then
    echo "  PASS: observations[] array referenced"
else
    echo "  FAIL: observations[] array not referenced"
    exit 1
fi

# Test 4: Verify phase number in observation ID distinguishes phases
echo "Test 4: Checking phase number distinguishes observations..."
HAS_02=$(grep -c "OBS-02" "$PHASE02" 2>/dev/null || echo 0)
HAS_03=$(grep -c "OBS-03" "$PHASE03" 2>/dev/null || echo 0)
HAS_04=$(grep -c "OBS-04" "$PHASE04" 2>/dev/null || echo 0)

if [ "$HAS_02" -gt 0 ] && [ "$HAS_03" -gt 0 ] && [ "$HAS_04" -gt 0 ]; then
    echo "  PASS: Phase-specific ID patterns found (OBS-02, OBS-03, OBS-04)"
else
    echo "  FAIL: Phase-specific ID patterns missing"
    exit 1
fi

echo "=== All $TEST_NAME tests passed ==="
exit 0
