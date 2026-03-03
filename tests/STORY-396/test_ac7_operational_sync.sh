#!/bin/bash
# Test: AC#7 - Operational Path Synchronization
# Story: STORY-396
# Generated: 2026-02-13
# TDD Phase: RED (tests should FAIL before migration)

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

AGENTS=(
    "backend-architect"
    "frontend-developer"
    "code-reviewer"
    "refactoring-specialist"
    "integration-tester"
    "api-designer"
    "deployment-engineer"
    "security-auditor"
    "code-analyzer"
)

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "============================================"
echo "AC#7: Operational Sync Tests"
echo "Story: STORY-396"
echo "============================================"
echo ""

# --- Test 1: src/ files byte-identical to .claude/ files ---
echo "--- Test Group 1: Byte-identical sync (src/ to .claude/) ---"
for agent in "${AGENTS[@]}"; do
    SRC_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    OPS_FILE="$PROJECT_ROOT/.claude/agents/${agent}.md"
    if [ -f "$SRC_FILE" ] && [ -f "$OPS_FILE" ]; then
        if diff -q "$SRC_FILE" "$OPS_FILE" > /dev/null 2>&1; then
            run_test "${agent}.md src/ == .claude/ (byte-identical)" 0
        else
            run_test "${agent}.md src/ == .claude/ (DIFFER)" 1
        fi
    else
        run_test "${agent}.md src/ == .claude/ (one or both missing)" 1
    fi
done
echo ""

# --- Test 2: Reference directories synchronized ---
echo "--- Test Group 2: Reference directory sync ---"
for agent in "${AGENTS[@]}"; do
    SRC_REF="$PROJECT_ROOT/src/claude/agents/${agent}/references"
    OPS_REF="$PROJECT_ROOT/.claude/agents/${agent}/references"
    if [ -d "$SRC_REF" ]; then
        if [ -d "$OPS_REF" ]; then
            DIFF_COUNT=$(diff -rq "$SRC_REF" "$OPS_REF" 2>/dev/null | wc -l)
            if [ "$DIFF_COUNT" -eq 0 ]; then
                run_test "${agent}/references/ synced" 0
            else
                run_test "${agent}/references/ synced (${DIFF_COUNT} diffs)" 1
            fi
        else
            run_test "${agent}/references/ synced (.claude/ refs missing)" 1
        fi
    else
        echo "  SKIP: ${agent} has no src/ references/ directory"
    fi
done
echo ""

# --- Test 3: CLAUDE.md Subagent Registry updated ---
echo "--- Test Group 3: CLAUDE.md registry updated ---"
CLAUDE_MD="$PROJECT_ROOT/CLAUDE.md"
if [ -f "$CLAUDE_MD" ]; then
    if grep -q "Subagent Registry" "$CLAUDE_MD" 2>/dev/null; then
        run_test "CLAUDE.md has Subagent Registry section" 0
    else
        run_test "CLAUDE.md has Subagent Registry section" 1
    fi

    for agent in "${AGENTS[@]}"; do
        if grep -q "$agent" "$CLAUDE_MD" 2>/dev/null; then
            run_test "${agent} listed in CLAUDE.md registry" 0
        else
            run_test "${agent} listed in CLAUDE.md registry" 1
        fi
    done

    # Verify descriptions reflect migrated state
    if grep -qi "version.*2\.0\.0\|canonical template\|unified template" "$CLAUDE_MD" 2>/dev/null; then
        run_test "Registry descriptions reflect migrated state" 0
    else
        run_test "Registry descriptions reflect migrated state" 1
    fi
else
    run_test "CLAUDE.md exists" 1
fi
echo ""

# === Summary ===
echo "============================================"
echo "AC#7 Results: $PASSED passed, $FAILED failed"
echo "============================================"
if [ "$FAILED" -eq 0 ]; then exit 0; else exit 1; fi
