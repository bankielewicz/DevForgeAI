#!/bin/bash
# Test: AC#7 - Operational Path Synchronization
# Story: STORY-395
# Generated: 2026-02-13
# TDD Phase: RED (tests expected to FAIL before migration)
#
# Validates that src/claude/agents/{agent}.md is byte-identical to
# .claude/agents/{agent}.md, reference directories are synchronized,
# and CLAUDE.md Subagent Registry is updated.

set -uo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
SRC_AGENTS_DIR="$PROJECT_ROOT/src/claude/agents"
OPS_AGENTS_DIR="$PROJECT_ROOT/.claude/agents"
CLAUDE_MD="$PROJECT_ROOT/CLAUDE.md"

AGENTS=(
    "anti-pattern-scanner"
    "context-validator"
    "context-preservation-validator"
    "coverage-analyzer"
    "code-quality-auditor"
    "deferral-validator"
    "dependency-graph-analyzer"
    "file-overlap-detector"
    "pattern-compliance-auditor"
    "tech-stack-detector"
)

# Agents expected to have reference directories after extraction
AGENTS_WITH_REFS=(
    "code-quality-auditor"
    "anti-pattern-scanner"
    "tech-stack-detector"
    "file-overlap-detector"
    "dependency-graph-analyzer"
)

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
echo "  AC#7: Operational Path Synchronization"
echo "  Testing src/ to .claude/ sync"
echo "=============================================="
echo ""

# --- Test Group 1: Agent files byte-identical between src/ and .claude/ ---
echo "--- Test Group 1: Byte-Identical Agent Files ---"
for agent in "${AGENTS[@]}"; do
    SRC_FILE="$SRC_AGENTS_DIR/${agent}.md"
    OPS_FILE="$OPS_AGENTS_DIR/${agent}.md"

    if [ ! -f "$SRC_FILE" ]; then
        run_test "Byte-identical: ${agent} (src file missing)" 1
        continue
    fi

    if [ ! -f "$OPS_FILE" ]; then
        run_test "Byte-identical: ${agent} (ops file missing)" 1
        continue
    fi

    diff -q "$SRC_FILE" "$OPS_FILE" > /dev/null 2>&1 && RC=0 || RC=1
    run_test "Byte-identical src/ to .claude/: ${agent}" $RC
done
echo ""

# --- Test Group 2: Reference directories synchronized (if they exist in src/) ---
echo "--- Test Group 2: Reference Directory Sync ---"
for agent in "${AGENTS_WITH_REFS[@]}"; do
    SRC_REFS="$SRC_AGENTS_DIR/${agent}/references"
    OPS_REFS="$OPS_AGENTS_DIR/${agent}/references"

    # Only check sync if src references directory actually exists
    if [ ! -d "$SRC_REFS" ]; then
        # No src references = no sync needed (agent is small enough)
        run_test "References not needed (src small): ${agent}" 0
        continue
    fi

    test -d "$OPS_REFS" && RC=0 || RC=1
    run_test "Ops references dir exists: ${agent}" $RC

    if [ -d "$OPS_REFS" ]; then
        for src_ref in "$SRC_REFS"/*.md; do
            if [ -f "$src_ref" ]; then
                BASENAME=$(basename "$src_ref")
                OPS_REF="$OPS_REFS/$BASENAME"
                if [ -f "$OPS_REF" ]; then
                    diff -q "$src_ref" "$OPS_REF" > /dev/null 2>&1 && RC=0 || RC=1
                    run_test "Reference synced: ${agent}/${BASENAME}" $RC
                else
                    run_test "Reference synced: ${agent}/${BASENAME} (ops missing)" 1
                fi
            fi
        done
    fi
done
echo ""

# --- Test Group 3: CLAUDE.md Subagent Registry Updated ---
echo "--- Test Group 3: CLAUDE.md Subagent Registry ---"

test -f "$CLAUDE_MD" && RC=0 || RC=1
run_test "CLAUDE.md exists" $RC

if [ -f "$CLAUDE_MD" ]; then
    grep -q "Subagent Registry" "$CLAUDE_MD" && RC=0 || RC=1
    run_test "Subagent Registry section exists" $RC

    for agent in "${AGENTS[@]}"; do
        grep -q "${agent}" "$CLAUDE_MD" && RC=0 || RC=1
        run_test "Agent in registry: ${agent}" $RC
    done

    for agent in "${AGENTS[@]}"; do
        REGISTRY_LINE=$(grep "${agent}" "$CLAUDE_MD" | head -1)
        if [ -n "$REGISTRY_LINE" ]; then
            DESC_LENGTH=${#REGISTRY_LINE}
            if [ "$DESC_LENGTH" -gt 40 ]; then
                run_test "Registry description substantive: ${agent}" 0
            else
                run_test "Registry description substantive: ${agent}" 1
            fi
        else
            run_test "Registry description substantive: ${agent} (not found)" 1
        fi
    done
else
    run_test "Subagent Registry section exists (CLAUDE.md missing)" 1
    for agent in "${AGENTS[@]}"; do
        run_test "Agent in registry: ${agent} (CLAUDE.md missing)" 1
        run_test "Registry description substantive: ${agent} (CLAUDE.md missing)" 1
    done
fi
echo ""

# === Summary ===
echo "=============================================="
echo "  AC#7 Operational Sync Results"
echo "=============================================="
echo "  Total:  $TOTAL"
echo "  Passed: $PASSED"
echo "  Failed: $FAILED"
echo "=============================================="

if [ "$FAILED" -eq 0 ]; then
    echo "  STATUS: ALL TESTS PASSED"
    exit 0
else
    echo "  STATUS: $FAILED TESTS FAILED"
    exit 1
fi
