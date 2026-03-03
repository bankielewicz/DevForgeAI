#!/bin/bash
# Test: AC#3 - Implementation Guidance Section Added
# Story: STORY-481
# Generated: 2026-02-23
# Description: Verifies that EPIC-082 features have clear implementation guidance
#              referencing the selected reference loading mechanism.

# === Test Configuration ===
PASSED=0
FAILED=0

EPIC_FILE="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Epics/EPIC-082-domain-reference-generation.epic.md"

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

echo "=== AC#3: Implementation Guidance Section Added ==="
echo "Target: $EPIC_FILE"
echo ""

# === Arrange ===
# Verify target file exists
if [ ! -f "$EPIC_FILE" ]; then
    echo "  ERROR: Target file does not exist: $EPIC_FILE"
    echo "Results: 0 passed, 1 failed (file missing)"
    exit 1
fi

# === Act & Assert ===

# Test 1: Epic file must contain an Implementation Guidance section
grep -q "## Implementation Guidance" "$EPIC_FILE"
run_test "EPIC-082 contains '## Implementation Guidance' section" $?

# Test 2: Implementation guidance must reference the loading mechanism by name
# The guidance must tie each feature to the decided loading approach
grep -qE "reference loading mechanism" "$EPIC_FILE"
run_test "Implementation guidance references 'reference loading mechanism'" $?

# Test 3: Implementation guidance must reference the ADR decision
# Features should point stories/implementers to the ADR for details
grep -q "ADR-022" "$EPIC_FILE"
run_test "Implementation guidance references ADR-022 decision document" $?

# Test 4: Implementation guidance must cover at least one named EPIC-082 feature
# (not just a generic paragraph — must show feature-specific context)
# Features in EPIC-082 scope include domain reference generation
grep -q "domain reference" "$EPIC_FILE"
run_test "Implementation guidance covers domain reference feature context" $?

# Test 5: The guidance section must appear after the decision section
# Validate ordering: DECISION section line number < Implementation Guidance line number
DECISION_LINE=$(grep -n "## Reference Loading Decision" "$EPIC_FILE" | head -1 | cut -d: -f1)
GUIDANCE_LINE=$(grep -n "## Implementation Guidance" "$EPIC_FILE" | head -1 | cut -d: -f1)

if [ -n "$DECISION_LINE" ] && [ -n "$GUIDANCE_LINE" ]; then
    [ "$GUIDANCE_LINE" -gt "$DECISION_LINE" ]
    run_test "Implementation Guidance section appears after Reference Loading Decision section" $?
else
    echo "  FAIL: Implementation Guidance section appears after Reference Loading Decision section (one or both sections missing)"
    ((FAILED++))
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
