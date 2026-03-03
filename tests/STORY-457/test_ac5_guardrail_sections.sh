#!/usr/bin/env bash
# STORY-457 AC#5: DO NOT guardrail section present in both commands
# Tests run against src/ tree per CLAUDE.md
set -euo pipefail

CMD1="src/claude/commands/validate-epic-coverage.md"
CMD2="src/claude/commands/create-missing-stories.md"
GOLD="src/claude/commands/create-story.md"
PASS=0
FAIL=0

assert_true() {
    local desc="$1"; shift
    if "$@" >/dev/null 2>&1; then
        echo "  PASS: $desc"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== AC#5: Lean Orchestration Enforcement DO NOT Guardrails ==="
echo ""

# Test 1: Gold standard has guardrail section (baseline)
echo "--- Gold Standard Baseline ---"
assert_true "create-story.md has guardrail section" grep -q 'Lean Orchestration Enforcement' "$GOLD"

# Test 2: validate-epic-coverage has guardrail section
echo "--- validate-epic-coverage ---"
assert_true "Has 'Lean Orchestration Enforcement' heading" grep -q 'Lean Orchestration Enforcement' "$CMD1"
assert_true "Has DO NOT section" grep -q 'DO NOT' "$CMD1"
assert_true "Has DO section" grep -q 'DO (' "$CMD1"

# Test 3: create-missing-stories has guardrail section
echo "--- create-missing-stories ---"
assert_true "Has 'Lean Orchestration Enforcement' heading" grep -q 'Lean Orchestration Enforcement' "$CMD2"
assert_true "Has DO NOT section" grep -q 'DO NOT' "$CMD2"
assert_true "Has DO section" grep -q 'DO (' "$CMD2"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
