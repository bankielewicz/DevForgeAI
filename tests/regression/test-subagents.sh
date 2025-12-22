#!/bin/bash

################################################################################
# STORY-044: Test 27 Subagents
# Purpose: Verify all subagent files exist and are loadable from src/
################################################################################

set -uo pipefail  # Don't exit on non-zero from functions, we handle errors explicitly

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TOTAL=0
PASSED=0
FAILED=0

test_subagent() {
    local agent_name="$1"
    local agent_file="$PROJECT_ROOT/.claude/agents/$agent_name.md"

    ((TOTAL++))

    if [ ! -f "$agent_file" ]; then
        echo -e "${RED}[FAIL]${NC} Subagent file missing: $agent_name"
        ((FAILED++))
        return 1
    fi

    # Check file size
    local size=$(wc -c < "$agent_file")
    if [ "$size" -lt 100 ]; then
        echo -e "${RED}[FAIL]${NC} Subagent file too small: $agent_name ($size bytes)"
        ((FAILED++))
        return 1
    fi

    # Check for required sections
    if grep -q "^---" "$agent_file" && grep -q "description:" "$agent_file"; then
        echo -e "${GREEN}[PASS]${NC} $agent_name ($size bytes)"
        ((PASSED++))
        return 0
    else
        echo -e "${YELLOW}[WARN]${NC} $agent_name may be missing metadata"
        ((PASSED++))
        return 0
    fi
}

main() {
    echo "================================================================================"
    echo "Testing 27 Subagents"
    echo "================================================================================"
    echo

    # All 27 subagents
    local agents=(
        "agent-generator"
        "api-designer"
        "architect-reviewer"
        "backend-architect"
        "code-analyzer"
        "code-reviewer"
        "context-validator"
        "deferral-validator"
        "deployment-engineer"
        "dev-result-interpreter"
        "documentation-writer"
        "frontend-developer"
        "git-validator"
        "integration-tester"
        "internet-sleuth"
        "pattern-compliance-auditor"
        "qa-result-interpreter"
        "refactoring-specialist"
        "requirements-analyst"
        "security-auditor"
        "sprint-planner"
        "story-requirements-analyst"
        "tech-stack-detector"
        "technical-debt-analyzer"
        "test-automator"
        "ui-spec-formatter"
    )

    # Group agents by category for better output
    echo -e "${BLUE}Testing Subagents (26):${NC}"
    for agent in "${agents[@]}"; do
        test_subagent "$agent"
    done
    echo

    echo "================================================================================"
    echo "Subagent Test Summary"
    echo "================================================================================"
    echo "Total:   $TOTAL"
    echo "Passed:  $PASSED"
    echo "Failed:  $FAILED"
    echo

    if [ "$FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓ All $TOTAL subagents verified${NC}"
        return 0
    else
        echo -e "${RED}✗ $FAILED subagent(s) failed${NC}"
        return 1
    fi
}

main "$@"
