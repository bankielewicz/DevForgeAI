#!/bin/bash
# Test: AC#4 - Zero Regression in Existing Validation Workflows
# Story: STORY-395
# Generated: 2026-02-13
# TDD Phase: RED (tests expected to FAIL before migration)
#
# Validates that YAML frontmatter is valid, tool declarations are preserved,
# integration declarations preserved, proactive triggers unchanged, and
# agent-specific functionality preserved after migration.

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

# Helper: extract YAML frontmatter (between first two --- lines)
extract_frontmatter() {
    local file="$1"
    sed -n '2,/^---$/p' "$file" | head -n -1
}

echo "=============================================="
echo "  AC#4: Zero Regression Validation"
echo "  Testing YAML, tools, integrations, triggers"
echo "=============================================="
echo ""

# --- Test Group 1: YAML Frontmatter Valid and Parseable ---
echo "--- Test Group 1: YAML Frontmatter Valid ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "YAML frontmatter valid: ${agent} (file missing)" 1
        continue
    fi

    # Check frontmatter starts with ---
    FIRST_LINE=$(head -1 "$AGENT_FILE")
    if [ "$FIRST_LINE" = "---" ]; then
        CLOSE_LINE=$(sed -n '2,${/^---$/=}' "$AGENT_FILE" | head -1)
        if [ -n "$CLOSE_LINE" ]; then
            run_test "YAML frontmatter valid (delimiters): ${agent}" 0
        else
            run_test "YAML frontmatter valid (delimiters): ${agent}" 1
        fi
    else
        run_test "YAML frontmatter valid (delimiters): ${agent}" 1
    fi

    # Check required fields
    FRONTMATTER=$(extract_frontmatter "$AGENT_FILE" 2>/dev/null || echo "")
    echo "$FRONTMATTER" | grep -q "^name:" && RC=0 || RC=1
    run_test "YAML has 'name' field: ${agent}" $RC

    echo "$FRONTMATTER" | grep -q "^description:" && RC=0 || RC=1
    run_test "YAML has 'description' field: ${agent}" $RC
done
echo ""

# --- Test Group 2: Tool Declarations Preserved ---
echo "--- Test Group 2: Tool Declarations Preserved ---"

declare -A EXPECTED_TOOLS
EXPECTED_TOOLS["anti-pattern-scanner"]="Read Grep Glob"
EXPECTED_TOOLS["context-validator"]="Read Grep Glob"
EXPECTED_TOOLS["context-preservation-validator"]="Read Glob Grep"
EXPECTED_TOOLS["coverage-analyzer"]="Read Grep Glob"
EXPECTED_TOOLS["code-quality-auditor"]="Read"
EXPECTED_TOOLS["deferral-validator"]="Read"
EXPECTED_TOOLS["dependency-graph-analyzer"]="Read Glob Grep"
EXPECTED_TOOLS["file-overlap-detector"]="Read Glob Grep"
EXPECTED_TOOLS["pattern-compliance-auditor"]="Read Grep Glob"
EXPECTED_TOOLS["tech-stack-detector"]="Read Glob Grep"

for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "Tools preserved: ${agent} (file missing)" 1
        continue
    fi

    FRONTMATTER=$(extract_frontmatter "$AGENT_FILE" 2>/dev/null || echo "")

    echo "$FRONTMATTER" | grep -q "^tools:" && RC=0 || RC=1
    run_test "Tools field exists: ${agent}" $RC

    for tool in ${EXPECTED_TOOLS[$agent]}; do
        echo "$FRONTMATTER" | grep -q "$tool" && RC=0 || RC=1
        run_test "Tool '${tool}' present: ${agent}" $RC
    done
done
echo ""

# --- Test Group 3: Integration Declarations Preserved ---
echo "--- Test Group 3: Integration Declarations Preserved ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "Integration preserved: ${agent} (file missing)" 1
        continue
    fi

    grep -qiE '(integration|works with|invoked.by|skill|devforgeai-)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "Integration references present: ${agent}" $RC
done
echo ""

# --- Test Group 4: Proactive Triggers Present ---
echo "--- Test Group 4: Proactive Triggers Present ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "Proactive triggers: ${agent} (file missing)" 1
        continue
    fi

    grep -qiE '(trigger|proactive|invok|when to use|automatically)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "Trigger documentation present: ${agent}" $RC
done
echo ""

# --- Test Group 5: Agent-Specific Functionality Preserved ---
echo "--- Test Group 5: Agent-Specific Functionality ---"

# anti-pattern-scanner
AGENT_FILE="$AGENTS_DIR/anti-pattern-scanner.md"
if [ -f "$AGENT_FILE" ]; then
    grep -qiE '(detection|categor)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "anti-pattern-scanner: detection categories present" $RC
    grep -qiE '(severity|blocking|critical|high)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "anti-pattern-scanner: severity-based blocking present" $RC
else
    run_test "anti-pattern-scanner: detection categories (file missing)" 1
    run_test "anti-pattern-scanner: severity-based blocking (file missing)" 1
fi

# context-validator
AGENT_FILE="$AGENTS_DIR/context-validator.md"
if [ -f "$AGENT_FILE" ]; then
    grep -qiE '(context.file|tech-stack|source-tree|dependencies|coding-standards|architecture-constraints|anti-patterns)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "context-validator: context file references present" $RC
else
    run_test "context-validator: context file references (file missing)" 1
fi

# context-preservation-validator
AGENT_FILE="$AGENTS_DIR/context-preservation-validator.md"
if [ -f "$AGENT_FILE" ]; then
    grep -qiE '(provenance|chain|linkage|non.blocking)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "context-preservation-validator: provenance validation present" $RC
else
    run_test "context-preservation-validator: provenance validation (file missing)" 1
fi

# coverage-analyzer
AGENT_FILE="$AGENTS_DIR/coverage-analyzer.md"
if [ -f "$AGENT_FILE" ]; then
    grep -qE '95' "$AGENT_FILE" && RC=0 || RC=1
    run_test "coverage-analyzer: 95% threshold present" $RC
    grep -qE '85' "$AGENT_FILE" && RC=0 || RC=1
    run_test "coverage-analyzer: 85% threshold present" $RC
    grep -qE '80' "$AGENT_FILE" && RC=0 || RC=1
    run_test "coverage-analyzer: 80% threshold present" $RC
else
    run_test "coverage-analyzer: 95% threshold (file missing)" 1
    run_test "coverage-analyzer: 85% threshold (file missing)" 1
    run_test "coverage-analyzer: 80% threshold (file missing)" 1
fi

# code-quality-auditor
AGENT_FILE="$AGENTS_DIR/code-quality-auditor.md"
if [ -f "$AGENT_FILE" ]; then
    grep -qiE '(cyclomatic|complexity)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "code-quality-auditor: cyclomatic complexity present" $RC
    grep -qiE '(duplicat|duplication)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "code-quality-auditor: duplication detection present" $RC
    grep -qiE '(maintainability)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "code-quality-auditor: maintainability index present" $RC
else
    run_test "code-quality-auditor: cyclomatic complexity (file missing)" 1
    run_test "code-quality-auditor: duplication detection (file missing)" 1
    run_test "code-quality-auditor: maintainability index (file missing)" 1
fi

# deferral-validator
AGENT_FILE="$AGENTS_DIR/deferral-validator.md"
if [ -f "$AGENT_FILE" ]; then
    grep -qiE '(circular|deferral)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "deferral-validator: circular deferral detection present" $RC
    grep -qiE '(ADR|architecture.decision)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "deferral-validator: ADR reference validation present" $RC
else
    run_test "deferral-validator: circular deferral detection (file missing)" 1
    run_test "deferral-validator: ADR reference validation (file missing)" 1
fi

# dependency-graph-analyzer
AGENT_FILE="$AGENTS_DIR/dependency-graph-analyzer.md"
if [ -f "$AGENT_FILE" ]; then
    grep -qiE '(transitive|resolution)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "dependency-graph-analyzer: transitive resolution present" $RC
    grep -qiE '(cycle|circular)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "dependency-graph-analyzer: cycle detection present" $RC
else
    run_test "dependency-graph-analyzer: transitive resolution (file missing)" 1
    run_test "dependency-graph-analyzer: cycle detection (file missing)" 1
fi

# file-overlap-detector
AGENT_FILE="$AGENTS_DIR/file-overlap-detector.md"
if [ -f "$AGENT_FILE" ]; then
    grep -qiE '(pre.flight|spec.based)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "file-overlap-detector: spec-based pre-flight present" $RC
    grep -qiE '(post.flight|git.based)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "file-overlap-detector: git-based post-flight present" $RC
else
    run_test "file-overlap-detector: spec-based pre-flight (file missing)" 1
    run_test "file-overlap-detector: git-based post-flight (file missing)" 1
fi

# pattern-compliance-auditor
AGENT_FILE="$AGENTS_DIR/pattern-compliance-auditor.md"
if [ -f "$AGENT_FILE" ]; then
    grep -qiE '(lean.orchestration|violation|compliance)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "pattern-compliance-auditor: lean orchestration references present" $RC
else
    run_test "pattern-compliance-auditor: lean orchestration references (file missing)" 1
fi

# tech-stack-detector
AGENT_FILE="$AGENTS_DIR/tech-stack-detector.md"
if [ -f "$AGENT_FILE" ]; then
    grep -qiE '(technology|detect|tech-stack)' "$AGENT_FILE" && RC=0 || RC=1
    run_test "tech-stack-detector: technology detection references present" $RC
else
    run_test "tech-stack-detector: technology detection references (file missing)" 1
fi

echo ""

# === Summary ===
echo "=============================================="
echo "  AC#4 Zero Regression Results"
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
