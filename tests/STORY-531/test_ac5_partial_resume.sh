#!/bin/bash
# Test: AC#5 - Partial Completion and Resume
# Story: STORY-531
# Generated: 2026-03-04

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
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

echo "=== AC#5: Partial Completion and Resume ==="

# Test 1: Resume section exists with correct heading
grep -q "^## 5\. Partial Completion and Resume$" "$REF_FILE" 2>/dev/null
run_test "Section '## 5. Partial Completion and Resume' exists" $?

# Extract resume section (between ## 5 and ## 6 or ---)
RESUME_SECTION=$(sed -n '/^## 5\. Partial Completion and Resume$/,/^## [0-9]/p' "$REF_FILE" | head -n -1)

# Test 2: Detection subsection defines complete vs incomplete identification
echo "$RESUME_SECTION" | grep -q "^### Detection$"
run_test "Resume section has ### Detection subsection" $?

echo "$RESUME_SECTION" | grep -qi "complete vs incomplete\|which are complete"
run_test "Detection defines complete vs incomplete block identification" $?

echo "$RESUME_SECTION" | grep -qi "TODO\|empty\|missing"
run_test "Detection identifies incomplete markers (TODO/empty/missing)" $?

# Test 3: Resume offers interaction with specific options (shown in code block)
echo "$RESUME_SECTION" | grep -qi "Continue from first incomplete block"
run_test "Resume offers 'Continue from first incomplete block' option" $?

echo "$RESUME_SECTION" | grep -qi "Review all blocks"
run_test "Resume offers 'Review all blocks' option" $?

echo "$RESUME_SECTION" | grep -qi "Start fresh"
run_test "Resume offers 'Start fresh' option" $?

# Test 4: Preservation Rules subsection explicitly states completed blocks never overwritten
echo "$RESUME_SECTION" | grep -q "^### Preservation Rules$"
run_test "Resume section has ### Preservation Rules subsection" $?

PRESERVATION=$(echo "$RESUME_SECTION" | sed -n '/^### Preservation Rules$/,/^### \|^---$/p')
echo "$PRESERVATION" | grep -qi "completed blocks are never overwritten"
run_test "Preservation rules: completed blocks are never overwritten during resume" $?

# Test 5: Incremental save pattern documented for interruption safety
echo "$RESUME_SECTION" | grep -qi "written after each block"
run_test "Resume documents write-per-block for interruption safety" $?

echo "$RESUME_SECTION" | grep -qi "minimize data loss"
run_test "Resume documents minimize data loss rationale" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
