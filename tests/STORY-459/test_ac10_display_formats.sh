#!/bin/bash
# Test: AC#10 - All display formats and output patterns preserved verbatim
# Story: STORY-459
# Generated: 2026-02-20
# Phase: TDD Red (tests MUST fail before implementation)
#
# Validates:
# - DoD Analysis table format preserved (category names, count format, percentage)
# - RESUME MODE banner preserved (triple-line borders)
# - Pre-flight status lines preserved (checkmark prefix)

set -uo pipefail

# === Test Configuration ===
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
COMMAND_FILE="${PROJECT_ROOT}/src/claude/commands/resume-dev.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/skills/implementing-stories/references/resume-detection.md"
PASSED=0
FAILED=0
TOTAL=0

# Combined content from both files for display format checks
get_combined_content() {
    local content=""
    if [ -f "$COMMAND_FILE" ]; then
        content=$(cat "$COMMAND_FILE")
    fi
    if [ -f "$REFERENCE_FILE" ]; then
        content="${content}$(cat "$REFERENCE_FILE")"
    fi
    echo "$content"
}

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

echo "=========================================="
echo "  AC#10: Display Format Preservation Tests"
echo "  Story: STORY-459"
echo "=========================================="
echo ""

# --- Pre-condition: At least command file exists ---
if [ ! -f "$COMMAND_FILE" ]; then
    echo "  FATAL: Command file not found: $COMMAND_FILE"
    exit 1
fi

COMBINED=$(get_combined_content)

# === DoD Analysis Table Format ===

# Test 1: DoD Analysis table header or section exists
echo "$COMBINED" | grep -q -i "DoD Analysis"
run_test "DoD Analysis table format preserved" $?

# Test 2: Category names preserved (Implementation, Quality, Testing, Documentation)
IMPL_FOUND=$(echo "$COMBINED" | grep -c -i "Implementation" || true)
QUAL_FOUND=$(echo "$COMBINED" | grep -c -i "Quality" || true)
TEST_FOUND=$(echo "$COMBINED" | grep -c -i "Testing" || true)
DOC_FOUND=$(echo "$COMBINED" | grep -c -i "Documentation" || true)
# All 4 categories must appear
test "$IMPL_FOUND" -ge 1 -a "$QUAL_FOUND" -ge 1 -a "$TEST_FOUND" -ge 1 -a "$DOC_FOUND" -ge 1
run_test "DoD categories preserved (Implementation, Quality, Testing, Documentation)" $?

# Test 3: Percentage or completion metric format preserved
echo "$COMBINED" | grep -q -E '(%|Completion|completion|percent)'
run_test "DoD Analysis completion percentage format preserved" $?

# === RESUME MODE Banner ===

# Test 4: RESUME MODE banner text exists
echo "$COMBINED" | grep -q "RESUME MODE"
run_test "RESUME MODE banner text preserved" $?

# Test 5: Triple-line border characters exist (used in banner formatting)
echo "$COMBINED" | grep -q -F "━━━"
run_test "RESUME MODE banner border characters preserved" $?

# === Pre-flight Status Lines ===

# Test 6: Pre-flight checkmark status line format preserved
# The original uses checkmark prefix for validation status
echo "$COMBINED" | grep -q -F "✓"
run_test "Pre-flight checkmark status line format preserved" $?

# Test 7: At least 3 pre-flight check descriptions exist
# Context validation, tech-stack, spec checks
PREFLIGHT_CHECKS=$(echo "$COMBINED" | grep -c "✓" || true)
test "$PREFLIGHT_CHECKS" -ge 3
run_test "At least 3 pre-flight check status lines preserved (found: $PREFLIGHT_CHECKS)" $?

# === Summary ===
echo ""
echo "=========================================="
echo "  Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "=========================================="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
