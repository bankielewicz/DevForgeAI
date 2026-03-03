#!/bin/bash
# Test: AC#3 - Manifest inserted at correct location
# Story: STORY-493
# Generated: 2026-02-23
set +e

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TEMPLATE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md"

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

echo "=== AC#3: Manifest inserted at correct location ==="

# Test 1: Manifest starts after YAML frontmatter (after line 7)
MANIFEST_START=$(grep -n "<!-- SECTION_MANIFEST" "$TEMPLATE_FILE" | head -1 | cut -d: -f1)
[ -n "$MANIFEST_START" ] && [ "$MANIFEST_START" -gt 7 ]
run_test "Manifest starts after YAML frontmatter (after line 7)" $?

# Test 2: Manifest ends before first ## section header (no content disruption)
FIRST_H2=$(grep -n "^## " "$TEMPLATE_FILE" | head -1 | cut -d: -f1)
MANIFEST_END=$(grep -n "END_SECTION_MANIFEST -->" "$TEMPLATE_FILE" | head -1 | cut -d: -f1)
[ -n "$MANIFEST_END" ] && [ -n "$FIRST_H2" ] && [ "$MANIFEST_END" -lt "$FIRST_H2" ]
run_test "Manifest ends before first ## section header" $?

# Test 3: NFR-001 - Manifest block is less than 150 lines
MANIFEST_LINES=$((MANIFEST_END - MANIFEST_START + 1))
[ "$MANIFEST_LINES" -lt 150 ]
run_test "NFR-001: Manifest block is less than 150 lines (actual: $MANIFEST_LINES)" $?

# Test 4: Existing template content not disrupted - check key sections still exist
grep -q "^## Description" "$TEMPLATE_FILE"
run_test "## Description section still exists" $?

grep -q "^## Acceptance Criteria" "$TEMPLATE_FILE"
run_test "## Acceptance Criteria section still exists" $?

grep -q "^## Definition of Done" "$TEMPLATE_FILE"
run_test "## Definition of Done section still exists" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
