#!/usr/bin/env bash
# STORY-375 AC#5: Results Stored in Research Directory
# TDD Red Phase - These tests MUST fail initially
# Tests verify:
#   - Research document created at devforgeai/specs/research/
#   - Document follows RESEARCH-NNN naming pattern
#   - All sections populated (methodology, data, analysis, conclusion)
#   - Measurement date and framework version recorded

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RESEARCH_DIR="$PROJECT_ROOT/devforgeai/specs/research"

# Find the research document
RESEARCH_FILE=""
for f in "$RESEARCH_DIR"/RESEARCH-*-treelint-token-validation*.md; do
    if [ -f "$f" ]; then
        RESEARCH_FILE="$f"
        break
    fi
done

PASS=0
FAIL=0
TOTAL=0

run_test() {
    local name="$1"
    local result="$2"
    TOTAL=$((TOTAL + 1))
    if [ "$result" -eq 0 ]; then
        PASS=$((PASS + 1))
        echo "  PASS: $name"
    else
        FAIL=$((FAIL + 1))
        echo "  FAIL: $name"
    fi
}

echo "=== AC#5: Results Stored in Research Directory ==="
echo ""

# Test 1: Research document exists in correct directory
if [ -n "$RESEARCH_FILE" ] && [ -f "$RESEARCH_FILE" ]; then
    run_test "Research document exists in devforgeai/specs/research/" 0
else
    run_test "Research document exists in devforgeai/specs/research/" 1
fi

# Guard: if no document, remaining tests fail by definition
if [ -z "$RESEARCH_FILE" ] || [ ! -f "$RESEARCH_FILE" ]; then
    run_test "Document follows RESEARCH-NNN-treelint-token-validation naming" 1
    run_test "Methodology section populated (not empty)" 1
    run_test "Data sections populated (baseline and Treelint)" 1
    run_test "Analysis section populated (not empty)" 1
    run_test "Conclusion section present" 1
    run_test "Measurement date recorded (ISO 8601 format)" 1
    run_test "Framework version recorded" 1
else
    # Test 2: Document follows RESEARCH-NNN naming pattern
    filename=$(basename "$RESEARCH_FILE")
    if echo "$filename" | grep -qE "^RESEARCH-[0-9]{3}-treelint-token-validation"; then
        run_test "Document follows RESEARCH-NNN-treelint-token-validation naming" 0
    else
        run_test "Document follows RESEARCH-NNN-treelint-token-validation naming" 1
    fi

    # Test 3: Methodology section populated (not empty)
    methodology_lines=$(sed -n '/## Methodology\|## Token Counting Methodology\|## Measurement Methodology/,/^## /p' "$RESEARCH_FILE" 2>/dev/null | wc -l)
    if [ "$methodology_lines" -gt 3 ]; then
        run_test "Methodology section populated (not empty)" 0
    else
        run_test "Methodology section populated (not empty)" 1
    fi

    # Test 4: Data sections populated (baseline + treelint)
    has_baseline=false
    has_treelint=false
    if grep -qi "## Baseline\|## Grep" "$RESEARCH_FILE" 2>/dev/null; then
        has_baseline=true
    fi
    if grep -qi "## Treelint" "$RESEARCH_FILE" 2>/dev/null; then
        has_treelint=true
    fi
    if $has_baseline && $has_treelint; then
        run_test "Data sections populated (baseline and Treelint)" 0
    else
        run_test "Data sections populated (baseline and Treelint)" 1
    fi

    # Test 5: Analysis section populated
    analysis_lines=$(sed -n '/## Analysis\|## Reduction Analysis\|## Comparison/,/^## /p' "$RESEARCH_FILE" 2>/dev/null | wc -l)
    if [ "$analysis_lines" -gt 3 ]; then
        run_test "Analysis section populated (not empty)" 0
    else
        run_test "Analysis section populated (not empty)" 1
    fi

    # Test 6: Conclusion section present
    if grep -qi "## Conclusion" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Conclusion section present" 0
    else
        run_test "Conclusion section present" 1
    fi

    # Test 7: Measurement date recorded
    if grep -qE "[0-9]{4}-[0-9]{2}-[0-9]{2}" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Measurement date recorded (ISO 8601 format)" 0
    else
        run_test "Measurement date recorded (ISO 8601 format)" 1
    fi

    # Test 8: Framework version recorded
    if grep -qi "version\|framework.*version\|devforgeai.*version" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Framework version recorded" 0
    else
        run_test "Framework version recorded" 1
    fi
fi

echo ""
echo "--- AC#5 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
