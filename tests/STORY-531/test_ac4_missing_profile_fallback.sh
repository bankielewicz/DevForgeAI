#!/bin/bash
# Test: AC#4 - Missing Adaptive Profile Fallback
# Story: STORY-531
# Generated: 2026-03-04

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/planning-business/SKILL.md"
REF_FILE="$PROJECT_ROOT/src/claude/skills/planning-business/references/lean-canvas-workflow.md"

PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED+1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED+1))
    fi
}

echo "=== AC#4: Missing Adaptive Profile Fallback ==="

# Test 1: SKILL.md has a dedicated fallback section (bold header, not just a mention)
grep -q "^\*\*Adaptive Profile Fallback:\*\*$" "$SKILL_FILE" 2>/dev/null
run_test "SKILL.md has dedicated **Adaptive Profile Fallback:** section" $?

# Test 2: Fallback paragraph specifies defaults to intermediate
# Extract multi-line fallback paragraph (between the header and the next bold header)
FALLBACK_SECTION=$(sed -n '/^\*\*Adaptive Profile Fallback:\*\*$/,/^\*\*[0-9A-Z]/p' "$SKILL_FILE" | head -n -1)
echo "$FALLBACK_SECTION" | grep -qi "defaults to intermediate"
run_test "Fallback section specifies 'defaults to intermediate'" $?

# Test 3: Specific warning text for missing profile is documented
grep -q "No adaptive profile found, defaulting to intermediate depth" "$SKILL_FILE" 2>/dev/null
run_test "SKILL.md documents exact warning: 'No adaptive profile found, defaulting to intermediate depth'" $?

# Test 4: Fallback confirms full 9-block workflow completes regardless of profile
echo "$FALLBACK_SECTION" | grep -qi "9-block workflow completes"
run_test "Fallback confirms full 9-block workflow completes without error" $?

# Test 5: Reference file states intermediate is default when no profile available
INTERMEDIATE_SECTION=$(sed -n '/^### Intermediate$/,/^### /p' "$REF_FILE" | head -n -1)
echo "$INTERMEDIATE_SECTION" | grep -qi "default level when no profile"
run_test "Reference file Intermediate section states default when no profile" $?

# Test 6: SKILL.md workflow step explicitly handles missing profile in Phase 1 workflow
grep -q "default to intermediate question depth" "$SKILL_FILE" 2>/dev/null
run_test "SKILL.md Phase 1 workflow handles missing profile with default to intermediate" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
