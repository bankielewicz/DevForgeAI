#!/bin/bash
# Test: AC#4 - Zero Regression in Existing Implementation and Review Workflows
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
echo "AC#4: Zero Regression Tests"
echo "Story: STORY-396"
echo "============================================"
echo ""

# --- Test 1: YAML frontmatter valid (starts with --- and has closing ---) ---
echo "--- Test Group 1: YAML frontmatter validity ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    if [ -f "$AGENT_FILE" ]; then
        FIRST_LINE=$(head -1 "$AGENT_FILE")
        HAS_CLOSING=$(awk '/^---/{c++} c==2{print "yes"; exit}' "$AGENT_FILE")
        if [ "$FIRST_LINE" = "---" ] && [ "$HAS_CLOSING" = "yes" ]; then
            run_test "${agent} has valid YAML frontmatter" 0
        else
            run_test "${agent} has valid YAML frontmatter" 1
        fi
    else
        run_test "${agent} has valid YAML frontmatter (file missing)" 1
    fi
done
echo ""

# --- Test 2: Tool declarations preserved per agent ---
echo "--- Test Group 2: Tool declarations preserved ---"

# backend-architect: Read, Write, Edit, Grep, Glob, Bash
AGENT_FILE="$PROJECT_ROOT/src/claude/agents/backend-architect.md"
if [ -f "$AGENT_FILE" ]; then
    for tool in "Read" "Write" "Edit" "Grep" "Glob" "Bash"; do
        if grep -q "$tool" "$AGENT_FILE" 2>/dev/null; then
            run_test "backend-architect preserves tool: $tool" 0
        else
            run_test "backend-architect preserves tool: $tool" 1
        fi
    done
else
    for tool in "Read" "Write" "Edit" "Grep" "Glob" "Bash"; do
        run_test "backend-architect preserves tool: $tool (file missing)" 1
    done
fi

# frontend-developer: Bash(npm:*)
AGENT_FILE="$PROJECT_ROOT/src/claude/agents/frontend-developer.md"
if [ -f "$AGENT_FILE" ]; then
    if grep -q 'Bash(npm:\*)' "$AGENT_FILE" 2>/dev/null; then
        run_test "frontend-developer preserves Bash(npm:*)" 0
    else
        run_test "frontend-developer preserves Bash(npm:*)" 1
    fi
else
    run_test "frontend-developer preserves Bash(npm:*) (file missing)" 1
fi

# code-reviewer: Bash(git:*)
AGENT_FILE="$PROJECT_ROOT/src/claude/agents/code-reviewer.md"
if [ -f "$AGENT_FILE" ]; then
    if grep -q 'Bash(git:\*)' "$AGENT_FILE" 2>/dev/null; then
        run_test "code-reviewer preserves Bash(git:*)" 0
    else
        run_test "code-reviewer preserves Bash(git:*)" 1
    fi
else
    run_test "code-reviewer preserves Bash(git:*) (file missing)" 1
fi

# deployment-engineer: 6 Bash-scoped tools
AGENT_FILE="$PROJECT_ROOT/src/claude/agents/deployment-engineer.md"
if [ -f "$AGENT_FILE" ]; then
    for tool in 'Bash(kubectl:\*)' 'Bash(docker:\*)' 'Bash(terraform:\*)' 'Bash(ansible:\*)' 'Bash(helm:\*)' 'Bash(git:\*)'; do
        if grep -q "$tool" "$AGENT_FILE" 2>/dev/null; then
            run_test "deployment-engineer preserves $tool" 0
        else
            run_test "deployment-engineer preserves $tool" 1
        fi
    done
else
    run_test "deployment-engineer tools (file missing)" 1
fi

# security-auditor: audit-specific tools
AGENT_FILE="$PROJECT_ROOT/src/claude/agents/security-auditor.md"
if [ -f "$AGENT_FILE" ]; then
    if grep -q 'Bash(npm:audit)' "$AGENT_FILE" 2>/dev/null; then
        run_test "security-auditor preserves Bash(npm:audit)" 0
    else
        run_test "security-auditor preserves Bash(npm:audit)" 1
    fi
    if grep -q 'Bash(pip:check)' "$AGENT_FILE" 2>/dev/null; then
        run_test "security-auditor preserves Bash(pip:check)" 0
    else
        run_test "security-auditor preserves Bash(pip:check)" 1
    fi
else
    run_test "security-auditor tools (file missing)" 1
fi

# code-analyzer: exactly Read, Glob, Grep (no Write/Edit/Bash in tools)
AGENT_FILE="$PROJECT_ROOT/src/claude/agents/code-analyzer.md"
if [ -f "$AGENT_FILE" ]; then
    for tool in "Read" "Glob" "Grep"; do
        if grep -q "$tool" "$AGENT_FILE" 2>/dev/null; then
            run_test "code-analyzer preserves read-only tool: $tool" 0
        else
            run_test "code-analyzer preserves read-only tool: $tool" 1
        fi
    done
    # Verify tools line does not contain Write, Edit, or Bash
    TOOLS_LINE=$(grep "^tools:" "$AGENT_FILE" 2>/dev/null || echo "")
    if [ -n "$TOOLS_LINE" ]; then
        if echo "$TOOLS_LINE" | grep -q "Write\|Edit\|Bash" 2>/dev/null; then
            run_test "code-analyzer has no Write/Edit/Bash in tools" 1
        else
            run_test "code-analyzer has no Write/Edit/Bash in tools" 0
        fi
    else
        run_test "code-analyzer has no Write/Edit/Bash in tools (no tools line)" 1
    fi
fi
echo ""

# --- Test 3: Agent-specific functionality preserved ---
echo "--- Test Group 3: Agent-specific functionality ---"

AGENT_FILE="$PROJECT_ROOT/src/claude/agents/backend-architect.md"
if [ -f "$AGENT_FILE" ]; then
    if grep -qi "clean architecture\|layer.*separation\|domain.*application.*infrastructure" "$AGENT_FILE" 2>/dev/null; then
        run_test "backend-architect: Clean architecture enforcement" 0
    else
        run_test "backend-architect: Clean architecture enforcement" 1
    fi
fi

AGENT_FILE="$PROJECT_ROOT/src/claude/agents/code-reviewer.md"
if [ -f "$AGENT_FILE" ]; then
    if grep -qi "Critical.*High.*Medium.*Low\|severity.*classif" "$AGENT_FILE" 2>/dev/null; then
        run_test "code-reviewer: severity classification" 0
    else
        run_test "code-reviewer: severity classification" 1
    fi
fi

AGENT_FILE="$PROJECT_ROOT/src/claude/agents/refactoring-specialist.md"
if [ -f "$AGENT_FILE" ]; then
    if grep -qi "Martin Fowler\|cyclomatic complexity\|code smell" "$AGENT_FILE" 2>/dev/null; then
        run_test "refactoring-specialist: refactoring patterns" 0
    else
        run_test "refactoring-specialist: refactoring patterns" 1
    fi
fi

AGENT_FILE="$PROJECT_ROOT/src/claude/agents/api-designer.md"
if [ -f "$AGENT_FILE" ]; then
    if grep -q "RCA-006" "$AGENT_FILE" 2>/dev/null; then
        run_test "api-designer: RCA-006 section preserved" 0
    else
        run_test "api-designer: RCA-006 section preserved" 1
    fi
fi

AGENT_FILE="$PROJECT_ROOT/src/claude/agents/security-auditor.md"
if [ -f "$AGENT_FILE" ]; then
    if grep -qi "OWASP" "$AGENT_FILE" 2>/dev/null; then
        run_test "security-auditor: OWASP Top 10" 0
    else
        run_test "security-auditor: OWASP Top 10" 1
    fi
fi
echo ""

# --- Test 4: Proactive triggers preserved ---
echo "--- Test Group 4: Proactive triggers ---"
AGENT_FILE="$PROJECT_ROOT/src/claude/agents/code-reviewer.md"
if [ -f "$AGENT_FILE" ]; then
    if grep -q "proactive_triggers\|proactive-triggers" "$AGENT_FILE" 2>/dev/null; then
        run_test "code-reviewer: proactive triggers present" 0
    else
        run_test "code-reviewer: proactive triggers present" 1
    fi
fi
echo ""

# === Summary ===
echo "============================================"
echo "AC#4 Results: $PASSED passed, $FAILED failed"
echo "============================================"
if [ "$FAILED" -eq 0 ]; then exit 0; else exit 1; fi
