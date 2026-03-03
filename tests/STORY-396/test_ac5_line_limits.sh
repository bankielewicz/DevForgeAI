#!/bin/bash
# Test: AC#5 - All Agent Files Within Size Limits
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
echo "AC#5: Size Limits Tests"
echo "Story: STORY-396"
echo "============================================"
echo ""

# --- Test 1: All 9 agents within 100-500 line range ---
echo "--- Test Group 1: 100-500 line range ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    if [ -f "$AGENT_FILE" ]; then
        LINE_COUNT=$(wc -l < "$AGENT_FILE")
        if [ "$LINE_COUNT" -ge 100 ] && [ "$LINE_COUNT" -le 500 ]; then
            run_test "${agent} is ${LINE_COUNT} lines (100-500 range)" 0
        else
            run_test "${agent} is ${LINE_COUNT} lines (OUTSIDE 100-500 range)" 1
        fi
    else
        run_test "${agent} within 100-500 lines (file missing)" 1
    fi
done
echo ""

# --- Test 2: Agents >400 lines have references/ directories ---
echo "--- Test Group 2: >400 lines have references/ ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    if [ -f "$AGENT_FILE" ]; then
        LINE_COUNT=$(wc -l < "$AGENT_FILE")
        if [ "$LINE_COUNT" -gt 400 ]; then
            REF_DIR="$PROJECT_ROOT/src/claude/agents/${agent}/references"
            if [ -d "$REF_DIR" ]; then
                run_test "${agent} (${LINE_COUNT} lines >400) has references/ dir" 0
            else
                run_test "${agent} (${LINE_COUNT} lines >400) has references/ dir" 1
            fi
        else
            echo "  SKIP: ${agent} is ${LINE_COUNT} lines (<=400, references/ optional)"
        fi
    else
        run_test "${agent} >400 line check (file missing)" 1
    fi
done
echo ""

# --- Test 3: Core files <=300 lines after extraction ---
echo "--- Test Group 3: Core files <=300 lines ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    REF_DIR="$PROJECT_ROOT/src/claude/agents/${agent}/references"
    if [ -f "$AGENT_FILE" ] && [ -d "$REF_DIR" ]; then
        LINE_COUNT=$(wc -l < "$AGENT_FILE")
        if [ "$LINE_COUNT" -le 300 ]; then
            run_test "${agent} core file is ${LINE_COUNT} lines (<=300 with refs)" 0
        else
            run_test "${agent} core file is ${LINE_COUNT} lines (>300 with refs)" 1
        fi
    elif [ -f "$AGENT_FILE" ]; then
        echo "  SKIP: ${agent} has no references/ dir (core <=300 not applicable)"
    else
        run_test "${agent} core <=300 lines (file missing)" 1
    fi
done
echo ""

# --- Test 4: Reference file paths follow pattern ---
echo "--- Test Group 4: Reference file path pattern ---"
for agent in "${AGENTS[@]}"; do
    REF_DIR="$PROJECT_ROOT/src/claude/agents/${agent}/references"
    if [ -d "$REF_DIR" ]; then
        NON_MD=$(find "$REF_DIR" -type f ! -name "*.md" 2>/dev/null | wc -l)
        if [ "$NON_MD" -eq 0 ]; then
            run_test "${agent} references/ contains only .md files" 0
        else
            run_test "${agent} references/ contains non-.md files ($NON_MD)" 1
        fi
    fi
done
echo ""

# === Summary ===
echo "============================================"
echo "AC#5 Results: $PASSED passed, $FAILED failed"
echo "============================================"
if [ "$FAILED" -eq 0 ]; then exit 0; else exit 1; fi
