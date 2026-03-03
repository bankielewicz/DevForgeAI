#!/bin/bash
# Test: STORY-523 - Phase File Mandatory/Optional Restructure
# Generated: 2026-03-02
# TDD Phase: RED (all tests expected to FAIL)
#
# Tests verify that all 12 phase files follow consistent section structure:
#   ## Mandatory Steps -> ## Validation Checkpoint -> ## Pre-Exit Checklist -> ## Optional Captures -> ## Exit Gate

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

PHASES_DIR="src/claude/skills/implementing-stories/phases"

PHASE_FILES=(
    "phase-01-preflight.md"
    "phase-02-test-first.md"
    "phase-03-implementation.md"
    "phase-04-refactoring.md"
    "phase-04.5-ac-verification.md"
    "phase-05-integration.md"
    "phase-05.5-ac-verification.md"
    "phase-06-deferral.md"
    "phase-07-dod-update.md"
    "phase-08-git-workflow.md"
    "phase-09-feedback.md"
    "phase-10-result.md"
)

REQUIRED_SECTIONS=(
    "## Mandatory Steps"
    "## Validation Checkpoint"
    "## Pre-Exit Checklist"
    "## Optional Captures"
    "## Exit Gate"
)

run_test() {
    local name="$1"
    local result="$2"
    ((TOTAL++))
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

# ============================================================
# AC#1: All 12 files have all 5 required sections
# ============================================================
echo ""
echo "=== AC#1: Section Existence ==="
echo ""

for file in "${PHASE_FILES[@]}"; do
    filepath="${PHASES_DIR}/${file}"

    # Verify file exists first
    if [ ! -f "$filepath" ]; then
        run_test "${file} exists" 1
        continue
    fi

    for section in "${REQUIRED_SECTIONS[@]}"; do
        grep -q "^${section}$" "$filepath"
        run_test "${file} contains '${section}'" $?
    done
done

# ============================================================
# AC#1: Section ORDER is correct in all 12 files
# Mandatory Steps must come before Validation Checkpoint,
# which must come before Pre-Exit Checklist, etc.
# ============================================================
echo ""
echo "=== AC#1: Section Order ==="
echo ""

for file in "${PHASE_FILES[@]}"; do
    filepath="${PHASES_DIR}/${file}"

    if [ ! -f "$filepath" ]; then
        run_test "${file} section order (file missing)" 1
        continue
    fi

    # Extract line numbers for each section header
    line_mandatory=$(grep -n "^## Mandatory Steps$" "$filepath" | head -1 | cut -d: -f1)
    line_validation=$(grep -n "^## Validation Checkpoint$" "$filepath" | head -1 | cut -d: -f1)
    line_preexit=$(grep -n "^## Pre-Exit Checklist$" "$filepath" | head -1 | cut -d: -f1)
    line_optional=$(grep -n "^## Optional Captures$" "$filepath" | head -1 | cut -d: -f1)
    line_exit=$(grep -n "^## Exit Gate$" "$filepath" | head -1 | cut -d: -f1)

    # All sections must exist for order check
    if [ -z "$line_mandatory" ] || [ -z "$line_validation" ] || [ -z "$line_preexit" ] || [ -z "$line_optional" ] || [ -z "$line_exit" ]; then
        run_test "${file} section order (missing sections)" 1
        continue
    fi

    # Verify order: mandatory < validation < preexit < optional < exit
    order_ok=0
    if [ "$line_mandatory" -lt "$line_validation" ] && \
       [ "$line_validation" -lt "$line_preexit" ] && \
       [ "$line_preexit" -lt "$line_optional" ] && \
       [ "$line_optional" -lt "$line_exit" ]; then
        order_ok=0
    else
        order_ok=1
    fi
    run_test "${file} sections in correct order" $order_ok
done

# ============================================================
# AC#2: Phase 02 - Test integrity snapshot under Mandatory Steps with [MANDATORY] marker
# ============================================================
echo ""
echo "=== AC#2: Phase 02 Test Integrity Snapshot ==="
echo ""

PHASE02="${PHASES_DIR}/phase-02-test-first.md"

# Extract content between ## Mandatory Steps and next ## heading
if [ -f "$PHASE02" ]; then
    mandatory_section=$(sed -n '/^## Mandatory Steps$/,/^## /{ /^## Mandatory Steps$/d; /^## /d; p; }' "$PHASE02")

    # Test: snapshot steps exist in Mandatory Steps section
    echo "$mandatory_section" | grep -qi "test integrity snapshot"
    run_test "phase-02 Mandatory Steps contains test integrity snapshot" $?

    # Test: [MANDATORY] marker present in Mandatory Steps section
    echo "$mandatory_section" | grep -q "\[MANDATORY\]"
    run_test "phase-02 Mandatory Steps contains [MANDATORY] marker" $?
else
    run_test "phase-02 Mandatory Steps contains test integrity snapshot" 1
    run_test "phase-02 Mandatory Steps contains [MANDATORY] marker" 1
fi

# ============================================================
# AC#3: Phase 01 - Steps 11, 12, 13 under Mandatory Steps
# ============================================================
echo ""
echo "=== AC#3: Phase 01 Session Memory Steps ==="
echo ""

PHASE01="${PHASES_DIR}/phase-01-preflight.md"

if [ -f "$PHASE01" ]; then
    mandatory_section_01=$(sed -n '/^## Mandatory Steps$/,/^## /{ /^## Mandatory Steps$/d; /^## /d; p; }' "$PHASE01")

    # Test: session memory step exists in Mandatory Steps
    echo "$mandatory_section_01" | grep -qi "session memory"
    run_test "phase-01 Mandatory Steps contains session memory step" $?

    # Test: stale cleanup step exists in Mandatory Steps
    echo "$mandatory_section_01" | grep -qi "stale.*cleanup"
    run_test "phase-01 Mandatory Steps contains stale cleanup step" $?

    # Test: context preservation step exists in Mandatory Steps
    echo "$mandatory_section_01" | grep -qi "context preservation"
    run_test "phase-01 Mandatory Steps contains context preservation step" $?
else
    run_test "phase-01 Mandatory Steps contains session memory step" 1
    run_test "phase-01 Mandatory Steps contains stale cleanup step" 1
    run_test "phase-01 Mandatory Steps contains context preservation step" 1
fi

# ============================================================
# Summary
# ============================================================
echo ""
echo "============================================"
echo "  STORY-523 Test Results"
echo "  Total: $TOTAL | Passed: $PASSED | Failed: $FAILED"
echo "============================================"
echo ""

[ $FAILED -eq 0 ] && exit 0 || exit 1
