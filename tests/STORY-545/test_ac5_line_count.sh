#!/bin/bash
# Test: AC#5 - Reference File Stays Under Line Limit with Progressive Disclosure
# Story: STORY-545
# Generated: 2026-03-05
# TDD Phase: RED - These tests MUST fail before implementation

# === Test Configuration ===
PASSED=0
FAILED=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

REFERENCE_FILE="$PROJECT_ROOT/src/claude/skills/advising-legal/references/ip-protection-checklist.md"

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

echo "=== AC#5: Reference File Under Line Limit with Progressive Disclosure ==="
echo ""

# === Arrange ===
# Reference file must exist

# === Act & Assert ===

# Test 1: Reference file exists (prerequisite)
test -f "$REFERENCE_FILE"
run_test "Reference file exists" $?

# Test 2: File is under 1,000 lines
if [ -f "$REFERENCE_FILE" ]; then
    line_count=$(wc -l < "$REFERENCE_FILE")
    [ "$line_count" -lt 1000 ]
    run_test "Reference file under 1,000 lines (actual: ${line_count})" $?
else
    run_test "Reference file under 1,000 lines" 1
fi

# Test 3: Progressive disclosure - uses markdown headings for structure
if [ -f "$REFERENCE_FILE" ]; then
    heading_count=$(grep -c "^#" "$REFERENCE_FILE")
    [ "$heading_count" -ge 4 ]
    run_test "Uses progressive disclosure with markdown headings (found: ${heading_count})" $?
else
    run_test "Uses progressive disclosure with markdown headings" 1
fi

# Test 4: Uses external links instead of reproducing legal text
if [ -f "$REFERENCE_FILE" ]; then
    link_count=$(grep -cE "https?://" "$REFERENCE_FILE")
    [ "$link_count" -ge 1 ]
    run_test "Contains external professional resource links (found: ${link_count})" $?
else
    run_test "Contains external professional resource links" 1
fi

# Test 5: File is not trivially small (has substantive content)
if [ -f "$REFERENCE_FILE" ]; then
    line_count=$(wc -l < "$REFERENCE_FILE")
    [ "$line_count" -ge 50 ]
    run_test "Reference file has substantive content (>= 50 lines, actual: ${line_count})" $?
else
    run_test "Reference file has substantive content (>= 50 lines)" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
