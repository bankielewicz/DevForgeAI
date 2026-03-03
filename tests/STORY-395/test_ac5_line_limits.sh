#!/bin/bash
# Test: AC#5 - All Agent Files Within Size Limits
# Story: STORY-395
# Generated: 2026-02-13
# TDD Phase: RED (tests expected to FAIL before migration)
#
# Validates that each of the 10 agent files is between 100-500 lines,
# large agents (>400 lines) have been extracted to references/ directories,
# and core files after extraction are under 300 lines.

set -uo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
AGENTS_DIR="$PROJECT_ROOT/src/claude/agents"

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

# Agents known to need progressive disclosure extraction (>400 lines pre-migration)
LARGE_AGENTS=(
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
echo "  AC#5: Agent File Size Limits"
echo "  Testing 100-500 line range + extraction"
echo "=============================================="
echo ""

# --- Test Group 1: All agents between 100-500 lines ---
echo "--- Test Group 1: Line Count Range (100-500) ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "Line count range: ${agent} (file missing)" 1
        continue
    fi

    LINE_COUNT=$(wc -l < "$AGENT_FILE")

    # Check minimum (100 lines)
    if [ "$LINE_COUNT" -ge 100 ]; then
        run_test "Minimum 100 lines (actual: ${LINE_COUNT}): ${agent}" 0
    else
        run_test "Minimum 100 lines (actual: ${LINE_COUNT}): ${agent}" 1
    fi

    # Check maximum (500 lines)
    if [ "$LINE_COUNT" -le 500 ]; then
        run_test "Maximum 500 lines (actual: ${LINE_COUNT}): ${agent}" 0
    else
        run_test "Maximum 500 lines (actual: ${LINE_COUNT}): ${agent}" 1
    fi
done
echo ""

# --- Test Group 2: Progressive Disclosure (only needed if >400 lines) ---
echo "--- Test Group 2: Progressive Disclosure Extraction ---"
# Per AC#5: Only agents exceeding 400 lines require references/ extraction
# Agents that were condensed to ≤300 lines no longer need extraction
for agent in "${LARGE_AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    LINE_COUNT=$(wc -l < "$AGENT_FILE" 2>/dev/null || echo "0")
    REFS_DIR="$AGENTS_DIR/${agent}/references"

    if [ "$LINE_COUNT" -gt 400 ]; then
        # Agent needs extraction - check for references/ directory
        test -d "$REFS_DIR" && RC=0 || RC=1
        run_test "References directory exists (${LINE_COUNT}>400): ${agent}/references/" $RC

        if [ -d "$REFS_DIR" ]; then
            REF_COUNT=$(ls -1 "$REFS_DIR"/*.md 2>/dev/null | wc -l || echo "0")
            if [ "$REF_COUNT" -gt 0 ]; then
                run_test "Reference files present (${REF_COUNT} files): ${agent}" 0
            else
                run_test "Reference files present (0 files): ${agent}" 1
            fi
        else
            run_test "Reference files present: ${agent} (dir missing)" 1
        fi
    else
        # Agent is small enough - references/ directory is optional
        if [ -d "$REFS_DIR" ]; then
            run_test "References directory exists (optional, ${LINE_COUNT}≤400): ${agent}" 0
        else
            run_test "No extraction needed (${LINE_COUNT} lines ≤400): ${agent}" 0
        fi
    fi
done
echo ""

# --- Test Group 3: Core files under 300 lines after extraction ---
echo "--- Test Group 3: Core Files Under 300 Lines (Extracted Agents) ---"
for agent in "${LARGE_AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "Core under 300 lines: ${agent} (file missing)" 1
        continue
    fi

    LINE_COUNT=$(wc -l < "$AGENT_FILE")
    if [ "$LINE_COUNT" -le 300 ]; then
        run_test "Core file under 300 lines (actual: ${LINE_COUNT}): ${agent}" 0
    else
        run_test "Core file under 300 lines (actual: ${LINE_COUNT}): ${agent}" 1
    fi
done
echo ""

# --- Test Group 4: Reference file paths follow pattern (if directory exists) ---
echo "--- Test Group 4: Reference File Path Pattern ---"
for agent in "${LARGE_AGENTS[@]}"; do
    REFS_DIR="$AGENTS_DIR/${agent}/references"
    if [ ! -d "$REFS_DIR" ]; then
        # No references directory - this is OK for small agents
        run_test "Reference path pattern (no dir needed): ${agent}" 0
        continue
    fi

    ALL_VALID=true
    for ref_file in "$REFS_DIR"/*; do
        if [ -f "$ref_file" ]; then
            BASENAME=$(basename "$ref_file")
            if [[ ! "$BASENAME" == *.md ]]; then
                ALL_VALID=false
                break
            fi
        fi
    done

    if [ "$ALL_VALID" = true ]; then
        run_test "All reference files are .md: ${agent}" 0
    else
        run_test "All reference files are .md: ${agent}" 1
    fi
done
echo ""

# === Summary ===
echo "=============================================="
echo "  AC#5 Line Limits Results"
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
