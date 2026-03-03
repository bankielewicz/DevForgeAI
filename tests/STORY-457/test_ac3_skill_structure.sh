#!/usr/bin/env bash
# STORY-457 AC#3: New validating-epic-coverage skill created with full pipeline logic
# Tests run against src/ tree per CLAUDE.md
set -euo pipefail

SKILL_FILE="src/claude/skills/validating-epic-coverage/SKILL.md"
SKILL_DIR="src/claude/skills/validating-epic-coverage"
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

assert_less_equal() {
    local desc="$1" actual="$2" max="$3"
    if [ "$actual" -le "$max" ]; then
        echo "  PASS: $desc ($actual <= $max)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc ($actual > $max)"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== AC#3: validating-epic-coverage Skill Structure ==="
echo ""

# Test 1: Skill file exists at correct path
echo "--- File Existence ---"
assert_true "SKILL.md exists" test -f "$SKILL_FILE"

# Test 2: Directory uses gerund naming per ADR-017
echo "--- Gerund Naming ---"
assert_true "Directory uses gerund naming (validating-)" test -d "$SKILL_DIR"

# Test 3: Line count <= 500
echo "--- Line Count ---"
if [ -f "$SKILL_FILE" ]; then
    LINE_COUNT=$(wc -l < "$SKILL_FILE")
    assert_less_equal "SKILL.md <= 500 lines" "$LINE_COUNT" 500
else
    echo "  FAIL: Cannot count lines - file missing"
    FAIL=$((FAIL + 1))
fi

# Test 4: Progressive disclosure with references/ directory
echo "--- Progressive Disclosure ---"
assert_true "references/ directory exists" test -d "$SKILL_DIR/references"

# Test 5: YAML frontmatter with required fields
echo "--- YAML Frontmatter ---"
if [ -f "$SKILL_FILE" ]; then
    assert_true "Has name field" grep -q '^name:' "$SKILL_FILE"
    assert_true "Has description field" grep -q '^description:' "$SKILL_FILE"
    assert_true "Name is validating-epic-coverage" grep -q 'name: validating-epic-coverage' "$SKILL_FILE"
else
    echo "  FAIL: Cannot check frontmatter - file missing"
    FAIL=$((FAIL + 1))
fi

# Test 6: Contains extracted business logic
echo "--- Business Logic Extraction ---"
if [ -f "$SKILL_FILE" ]; then
    assert_true "Contains gap-detector.sh reference" grep -q 'gap-detector.sh' "$SKILL_FILE"
    assert_true "Contains generate-report.sh reference" grep -q 'generate-report.sh' "$SKILL_FILE"
    assert_true "Contains coverage calculation" grep -qi 'coverage' "$SKILL_FILE"
    assert_true "Contains edge case: empty epic" grep -qi 'no features\|empty epic\|total_features.*0' "$SKILL_FILE"
    assert_true "Contains edge case: 100% coverage" grep -qi '100%.*coverage\|no gaps\|missing_features.*0' "$SKILL_FILE"
else
    echo "  FAIL: Cannot check business logic - file missing"
    FAIL=$((FAIL + 1))
fi

# Test 7: Mode awareness (interactive/quiet/CI)
echo "--- Mode Awareness ---"
if [ -f "$SKILL_FILE" ]; then
    # Check skill or references for mode awareness
    MODE_FOUND=$(grep -rl 'interactive\|quiet\|PROMPT_MODE' "$SKILL_DIR" 2>/dev/null | wc -l || true)
    if [ "$MODE_FOUND" -gt 0 ]; then
        echo "  PASS: Mode awareness found ($MODE_FOUND files)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: No mode awareness found in skill directory"
        FAIL=$((FAIL + 1))
    fi
fi

# Test 8: Batch creation context markers
echo "--- Batch Context Markers ---"
if [ -f "$SKILL_FILE" ]; then
    MARKERS_DIR="$SKILL_DIR"
    assert_true "Has Batch Mode marker" grep -rq 'Batch Mode' "$MARKERS_DIR"
    assert_true "Has Batch Index marker" grep -rq 'Batch Index' "$MARKERS_DIR"
    assert_true "Has Batch Total marker" grep -rq 'Batch Total' "$MARKERS_DIR"
    assert_true "Has Created From marker" grep -rq 'Created From' "$MARKERS_DIR"
else
    echo "  FAIL: Cannot check markers - file missing"
    FAIL=$((FAIL + 1))
fi

# Test 9: Shell-safe escaping (BR-003)
echo "--- Shell-safe Escaping ---"
if [ -f "$SKILL_FILE" ]; then
    ESCAPE_FOUND=$(grep -rl 'shell.safe\|escape\|escap' "$SKILL_DIR" 2>/dev/null | wc -l || true)
    if [ "$ESCAPE_FOUND" -gt 0 ]; then
        echo "  PASS: Shell-safe escaping found ($ESCAPE_FOUND files)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: No shell-safe escaping found"
        FAIL=$((FAIL + 1))
    fi
fi

# Test 10: Batch failure isolation (BR-004)
echo "--- Batch Failure Isolation ---"
if [ -f "$SKILL_FILE" ]; then
    assert_true "Has TRY/CATCH or error isolation" grep -rqi 'TRY\|CATCH\|failure.*isol\|continue.*next' "$SKILL_DIR"
fi

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
