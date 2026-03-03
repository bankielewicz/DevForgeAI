#!/bin/bash
# Test: AC#2 - Reference file exists and contains all 6 required sections
# Story: STORY-463
# Generated: 2026-02-21
# TDD Phase: RED - these tests MUST FAIL before refactoring

PASSED=0
FAILED=0
REF_FILE="src/claude/skills/devforgeai-feedback/references/feedback-search-help.md"

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

echo "=== AC#2: Reference File Exists and Contains All 6 Sections ==="
echo "Target: $REF_FILE"
echo ""

# === Test 1: Reference file exists ===
[ -f "$REF_FILE" ]
run_test "Reference file exists at src/claude/skills/devforgeai-feedback/references/feedback-search-help.md" $?

# === Tests 2-7: Required sections present ===
SECTIONS=(
    "Query Formats"
    "Filter Options"
    "Pagination"
    "Result Sorting"
    "Examples"
    "Troubleshooting"
)

if [ -f "$REF_FILE" ]; then
    for SECTION in "${SECTIONS[@]}"; do
        grep -q "$SECTION" "$REF_FILE"
        run_test "Reference file contains section: '$SECTION'" $?
    done
else
    echo "  SKIP: Section checks (file missing)"
    for i in "${!SECTIONS[@]}"; do
        ((FAILED++))
    done
fi

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[ $FAILED -eq 0 ] && exit 0 || exit 1
