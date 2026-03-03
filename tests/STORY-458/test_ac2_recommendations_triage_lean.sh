#!/bin/bash
# Test: AC#2 - recommendations-triage.md reduced to lean orchestration pattern
# Story: STORY-458
# Generated: 2026-02-20
# Expected: FAIL (TDD Red phase - refactoring not yet done)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

TARGET_FILE="${PROJECT_ROOT}/src/claude/commands/recommendations-triage.md"

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

echo "=============================================="
echo "  AC#2: recommendations-triage.md Lean Orchestration"
echo "  Story: STORY-458"
echo "=============================================="
echo ""

# --- Pre-check: File exists ---
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FATAL: Target file not found: $TARGET_FILE"
    echo ""
    echo "Results: 0 passed, 4 failed out of 4 tests"
    exit 1
fi

# === Test 1: Line count <=80 ===
LINE_COUNT=$(wc -l < "$TARGET_FILE")
test_result=0
if [ "$LINE_COUNT" -le 80 ]; then
    test_result=0
else
    test_result=1
fi
run_test "Line count <= 80 (actual: ${LINE_COUNT})" "$test_result"

# === Test 2: Code blocks <=2 before Skill() invocation ===
SKILL_LINE=$(grep -n 'Skill(command=' "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -z "$SKILL_LINE" ]; then
    BLOCKS_BEFORE_SKILL=$(grep -c '```' "$TARGET_FILE" || true)
    BLOCKS_BEFORE_SKILL=$(( BLOCKS_BEFORE_SKILL / 2 ))
    run_test "Code blocks <= 2 before Skill() (no Skill() found, ${BLOCKS_BEFORE_SKILL} total blocks)" 1
else
    BLOCKS_BEFORE_SKILL=$(head -n "$((SKILL_LINE - 1))" "$TARGET_FILE" | grep -c '```' || true)
    BLOCKS_BEFORE_SKILL=$(( BLOCKS_BEFORE_SKILL / 2 ))
    test_result=0
    if [ "$BLOCKS_BEFORE_SKILL" -le 2 ]; then
        test_result=0
    else
        test_result=1
    fi
    run_test "Code blocks <= 2 before Skill() (actual: ${BLOCKS_BEFORE_SKILL})" "$test_result"
fi

# === Test 3: Contains exactly 1 Skill() invocation ===
SKILL_COUNT=$(grep -c 'Skill(command=' "$TARGET_FILE" || true)
test_result=0
if [ "$SKILL_COUNT" -eq 1 ]; then
    test_result=0
else
    test_result=1
fi
run_test "Contains exactly 1 Skill() invocation (actual: ${SKILL_COUNT})" "$test_result"

# === Test 4: Write NOT in allowed-tools frontmatter ===
# Extract the allowed-tools line from YAML frontmatter (between --- delimiters)
FRONTMATTER=$(sed -n '/^---$/,/^---$/p' "$TARGET_FILE")
ALLOWED_TOOLS_LINE=$(echo "$FRONTMATTER" | grep '^allowed-tools:' || true)
test_result=0
if [ -z "$ALLOWED_TOOLS_LINE" ]; then
    # No allowed-tools line found - could be acceptable if frontmatter structure changed
    test_result=1
    run_test "Write NOT in allowed-tools (no allowed-tools line found)" "$test_result"
else
    if echo "$ALLOWED_TOOLS_LINE" | grep -q 'Write'; then
        test_result=1
    else
        test_result=0
    fi
    run_test "Write NOT in allowed-tools (line: ${ALLOWED_TOOLS_LINE})" "$test_result"
fi

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
