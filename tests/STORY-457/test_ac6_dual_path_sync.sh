#!/usr/bin/env bash
# STORY-457 AC#6: Dual-path architecture maintained
# Files must exist identically in both src/claude/ and .claude/ trees
set -euo pipefail

PASS=0
FAIL=0

assert_sync() {
    local desc="$1" src_file="$2" ops_file="$3"
    if [ ! -f "$src_file" ]; then
        echo "  FAIL: $desc - src file missing: $src_file"
        FAIL=$((FAIL + 1))
        return
    fi
    if [ ! -f "$ops_file" ]; then
        echo "  FAIL: $desc - operational file missing: $ops_file"
        FAIL=$((FAIL + 1))
        return
    fi
    if diff -q "$src_file" "$ops_file" >/dev/null 2>&1; then
        echo "  PASS: $desc (files identical)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc (files differ)"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== AC#6: Dual-Path Architecture Sync ==="
echo ""

# Test 1: Commands synced
echo "--- Commands ---"
assert_sync "validate-epic-coverage.md" \
    "src/claude/commands/validate-epic-coverage.md" \
    ".claude/commands/validate-epic-coverage.md"

assert_sync "create-missing-stories.md" \
    "src/claude/commands/create-missing-stories.md" \
    ".claude/commands/create-missing-stories.md"

# Test 2: Skill synced
echo "--- Skill ---"
assert_sync "validating-epic-coverage SKILL.md" \
    "src/claude/skills/validating-epic-coverage/SKILL.md" \
    ".claude/skills/validating-epic-coverage/SKILL.md"

# Test 3: Subagent synced
echo "--- Subagent ---"
assert_sync "epic-coverage-result-interpreter.md" \
    "src/claude/agents/epic-coverage-result-interpreter.md" \
    ".claude/agents/epic-coverage-result-interpreter.md"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
