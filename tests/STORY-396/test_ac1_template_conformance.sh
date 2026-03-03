#!/bin/bash
# Test: AC#1 - All 9 Agents Conform to Canonical Template Structure
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

# 8 H2 required sections + YAML frontmatter + H1 title = 10 total
REQUIRED_SECTIONS=(
    "## Purpose"
    "## When Invoked"
    "## Input/Output Specification"
    "## Constraints and Boundaries"
    "## Workflow"
    "## Success Criteria"
    "## Output Format"
    "## Examples"
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
echo "AC#1: Template Conformance Tests"
echo "Story: STORY-396"
echo "============================================"
echo ""

# --- Test 1: All 9 agent files exist in src/ ---
echo "--- Test Group 1: Agent files exist in src/ ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    if [ -f "$AGENT_FILE" ]; then
        run_test "src/claude/agents/${agent}.md exists" 0
    else
        run_test "src/claude/agents/${agent}.md exists" 1
    fi
done
echo ""

# --- Test 2: YAML frontmatter contains version: "2.0.0" ---
echo "--- Test Group 2: version 2.0.0 in YAML frontmatter ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    if [ -f "$AGENT_FILE" ]; then
        if grep -q 'version:.*"2\.0\.0"' "$AGENT_FILE" 2>/dev/null; then
            run_test "${agent} has version: \"2.0.0\"" 0
        else
            run_test "${agent} has version: \"2.0.0\"" 1
        fi
    else
        run_test "${agent} has version: \"2.0.0\" (file missing)" 1
    fi
done
echo ""

# --- Test 3: All 10 required sections present ---
echo "--- Test Group 3: 10 required canonical template sections ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    if [ -f "$AGENT_FILE" ]; then
        MISSING=0
        for section in "${REQUIRED_SECTIONS[@]}"; do
            if ! grep -q "^${section}" "$AGENT_FILE" 2>/dev/null; then
                MISSING=$((MISSING + 1))
            fi
        done
        # Also check for YAML frontmatter (section 1) and Title H1 (section 2)
        FIRST_LINE=$(head -1 "$AGENT_FILE")
        if [ "$FIRST_LINE" != "---" ]; then
            MISSING=$((MISSING + 1))
        fi
        if ! grep -q "^# " "$AGENT_FILE" 2>/dev/null; then
            MISSING=$((MISSING + 1))
        fi
        if [ "$MISSING" -eq 0 ]; then
            run_test "${agent} has all 10 required sections" 0
        else
            run_test "${agent} has all 10 required sections (missing $MISSING)" 1
        fi
    else
        run_test "${agent} has all 10 required sections (file missing)" 1
    fi
done
echo ""

# --- Test 4: YAML frontmatter contains required fields (name, description, tools, model) ---
echo "--- Test Group 4: YAML frontmatter required fields ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    if [ -f "$AGENT_FILE" ]; then
        MISSING_FIELDS=0
        for field in "name:" "description:" "tools:" "model:"; do
            if ! grep -q "^${field}" "$AGENT_FILE" 2>/dev/null; then
                MISSING_FIELDS=$((MISSING_FIELDS + 1))
            fi
        done
        if [ "$MISSING_FIELDS" -eq 0 ]; then
            run_test "${agent} has required YAML fields (name, description, tools, model)" 0
        else
            run_test "${agent} has required YAML fields (missing $MISSING_FIELDS)" 1
        fi
    else
        run_test "${agent} has required YAML fields (file missing)" 1
    fi
done
echo ""

# === Summary ===
echo "============================================"
echo "AC#1 Results: $PASSED passed, $FAILED failed"
echo "============================================"
if [ "$FAILED" -eq 0 ]; then exit 0; else exit 1; fi
