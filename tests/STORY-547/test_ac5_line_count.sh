#!/bin/bash
# Test: AC#5 - Reference File Length and Progressive Disclosure
# Story: STORY-547
# Generated: 2026-03-06
# TDD Phase: RED - These tests MUST fail before implementation

# === Test Configuration ===
PASSED=0
FAILED=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

REFERENCE_FILE="$PROJECT_ROOT/src/claude/skills/advising-legal/references/when-to-hire-professional.md"

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

echo "=== AC#5: Reference File Length and Progressive Disclosure ==="
echo ""

# === Act & Assert ===

# Test 1: Reference file exists
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

# Test 3: Progressive disclosure - summary appears first
if [ -f "$REFERENCE_FILE" ]; then
    # First content heading should be a summary/overview/quick reference
    first_h2=$(grep -n "^## " "$REFERENCE_FILE" 2>/dev/null | head -1)
    echo "$first_h2" | grep -qiE "summary|overview|quick|at a glance|disclaimer"
    run_test "Progressive disclosure: summary/overview appears first" $?
else
    run_test "Progressive disclosure: summary/overview appears first" 1
fi

# Test 4: Navigation headers present (at least 4 major sections)
if [ -f "$REFERENCE_FILE" ]; then
    heading_count=$(grep -c "^## " "$REFERENCE_FILE")
    [ "$heading_count" -ge 4 ]
    run_test "Navigation headers present (found: ${heading_count} H2 sections, need >= 4)" $?
else
    run_test "Navigation headers present" 1
fi

# Test 5: File has substantive content (>= 100 lines)
if [ -f "$REFERENCE_FILE" ]; then
    line_count=$(wc -l < "$REFERENCE_FILE")
    [ "$line_count" -ge 100 ]
    run_test "File has substantive content (>= 100 lines, actual: ${line_count})" $?
else
    run_test "File has substantive content (>= 100 lines)" 1
fi

# Test 6: Contains external resource links
if [ -f "$REFERENCE_FILE" ]; then
    link_count=$(grep -cE "https?://" "$REFERENCE_FILE")
    [ "$link_count" -ge 1 ]
    run_test "Contains external resource links (found: ${link_count})" $?
else
    run_test "Contains external resource links" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
