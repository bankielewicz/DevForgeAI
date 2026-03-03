#!/bin/bash
# Test: AC#2 - Phase Filtering Logic
# Story: STORY-530
# Generated: 2026-03-03
#
# Validates that TaskCreate calls are generated ONLY for current phase steps.
# E.g., Phase 03 creates only Step 03.* tasks.
# Step ID in subject uses dotted format: "Step 03.1: {description}".

set -uo pipefail

PASSED=0
FAILED=0
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PHASES_DIR="$PROJECT_ROOT/src/claude/skills/implementing-stories/phases"

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

echo "=== AC#2: Phase Filtering Tests ==="
echo ""

# Phase number mapping (file -> expected phase ID)
declare -A PHASE_MAP
PHASE_MAP["phase-01-preflight.md"]="01"
PHASE_MAP["phase-02-test-first.md"]="02"
PHASE_MAP["phase-03-implementation.md"]="03"
PHASE_MAP["phase-04-refactoring.md"]="04"
PHASE_MAP["phase-04.5-ac-verification.md"]="4.5"
PHASE_MAP["phase-05-integration.md"]="05"
PHASE_MAP["phase-05.5-ac-verification.md"]="5.5"
PHASE_MAP["phase-06-deferral.md"]="06"
PHASE_MAP["phase-07-dod-update.md"]="07"
PHASE_MAP["phase-08-git-workflow.md"]="08"
PHASE_MAP["phase-09-feedback.md"]="09"
PHASE_MAP["phase-10-result.md"]="10"

# Test 1: Each phase file references ONLY its own phase steps in TaskCreate
echo "--- Test Group: Phase-specific step references ---"
for file in "${!PHASE_MAP[@]}"; do
    phase_id="${PHASE_MAP[$file]}"
    filepath="$PHASES_DIR/$file"

    if [ ! -f "$filepath" ]; then
        run_test "$file exists" 1
        continue
    fi

    # Extract the Progressive Task Disclosure section
    section=$(sed -n '/^## Progressive Task Disclosure/,/^## /p' "$filepath" | head -n -1)

    # Test: Section must contain TaskCreate
    echo "$section" | grep -q "TaskCreate" 2>/dev/null
    run_test "$file contains TaskCreate in Progressive Task Disclosure" $?

    # Test: Section must reference the correct phase step ID pattern (e.g., "Step 03.")
    echo "$section" | grep -q "Step ${phase_id}\." 2>/dev/null
    run_test "$file references Step ${phase_id}.* pattern" $?
done

# Test 2: Dotted format validation - Step IDs use "Step NN.N:" format
echo ""
echo "--- Test Group: Dotted step ID format ---"
for file in "${!PHASE_MAP[@]}"; do
    phase_id="${PHASE_MAP[$file]}"
    filepath="$PHASES_DIR/$file"

    [ ! -f "$filepath" ] && continue

    section=$(sed -n '/^## Progressive Task Disclosure/,/^## /p' "$filepath" | head -n -1)

    # Step ID must use dotted format: "Step 03.1:" or "Step 4.5.1:"
    echo "$section" | grep -qE "Step ${phase_id}\.[0-9]" 2>/dev/null
    run_test "$file uses dotted format Step ${phase_id}.N" $?
done

# Test 3: No cross-phase step references in TaskCreate section
echo ""
echo "--- Test Group: No cross-phase step leakage ---"
for file in "${!PHASE_MAP[@]}"; do
    phase_id="${PHASE_MAP[$file]}"
    filepath="$PHASES_DIR/$file"

    [ ! -f "$filepath" ] && continue

    section=$(sed -n '/^## Progressive Task Disclosure/,/^## /p' "$filepath" | head -n -1)

    # Check that no OTHER phase step IDs appear in TaskCreate context
    # Build list of other phase IDs
    leak_found=0
    for other_file in "${!PHASE_MAP[@]}"; do
        other_id="${PHASE_MAP[$other_file]}"
        [ "$other_id" = "$phase_id" ] && continue
        # Check for "Step OtherID." pattern in the section
        if echo "$section" | grep -qE "Step ${other_id}\.[0-9]" 2>/dev/null; then
            leak_found=1
            echo "    WARNING: $file contains cross-phase reference to Step ${other_id}"
        fi
    done
    run_test "$file has no cross-phase step references" $((leak_found))
done

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
