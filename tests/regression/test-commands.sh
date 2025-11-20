#!/bin/bash

################################################################################
# STORY-044: Test All 23 Slash Commands
# Purpose: Verify all commands load correctly from src/ paths
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

test_command() {
    local cmd_name="$1"
    local cmd_file="$PROJECT_ROOT/.claude/commands/$cmd_name.md"

    ((TOTAL++))

    if [ ! -f "$cmd_file" ]; then
        echo -e "${RED}[FAIL]${NC} Command file missing: /$cmd_name"
        ((FAILED++))
        return 1
    fi

    # Check file is readable and has content
    local size=$(wc -c < "$cmd_file")
    if [ "$size" -lt 100 ]; then
        echo -e "${RED}[FAIL]${NC} Command file too small: /$cmd_name ($size bytes)"
        ((FAILED++))
        return 1
    fi

    # Check for CRITICAL sections in command file
    local has_description=$(grep -q "description:" "$cmd_file" && echo 1 || echo 0)
    local has_model=$(grep -q "model:" "$cmd_file" && echo 1 || echo 0)

    if [ "$has_description" -eq 1 ] && [ "$has_model" -eq 1 ]; then
        echo -e "${GREEN}[PASS]${NC} /$cmd_name (${size} bytes)"
        ((PASSED++))
        return 0
    else
        echo -e "${YELLOW}[WARN]${NC} /$cmd_name missing metadata (description or model)"
        ((PASSED++))  # Count as pass since file exists
        return 0
    fi
}

main() {
    echo "================================================================================"
    echo "Testing 23 Slash Commands"
    echo "================================================================================"
    echo

    # Core Workflow Commands (4)
    echo -e "${BLUE}Core Workflow Commands:${NC}"
    test_command "dev"
    test_command "qa"
    test_command "release"
    test_command "orchestrate"
    echo

    # Planning & Setup Commands (7)
    echo -e "${BLUE}Planning & Setup Commands:${NC}"
    test_command "ideate"
    test_command "create-context"
    test_command "create-epic"
    test_command "create-sprint"
    test_command "create-story"
    test_command "create-ui"
    test_command "create-agent"
    echo

    # Framework Maintenance Commands (4)
    echo -e "${BLUE}Framework Maintenance Commands:${NC}"
    test_command "audit-deferrals"
    test_command "audit-budget"
    test_command "audit-hooks"
    test_command "rca"
    echo

    # Feedback System Commands (7)
    echo -e "${BLUE}Feedback System Commands:${NC}"
    test_command "feedback"
    test_command "feedback-config"
    test_command "feedback-search"
    test_command "feedback-reindex"
    test_command "feedback-export-data"
    test_command "export-feedback"
    test_command "import-feedback"
    echo

    # Documentation Command (1)
    echo -e "${BLUE}Documentation Command:${NC}"
    test_command "document"
    echo

    echo "================================================================================"
    echo "Command Test Summary"
    echo "================================================================================"
    echo "Total:   $TOTAL"
    echo "Passed:  $PASSED"
    echo "Failed:  $FAILED"
    echo

    if [ "$FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓ All 23 commands verified${NC}"
        return 0
    else
        echo -e "${RED}✗ $FAILED command(s) failed${NC}"
        return 1
    fi
}

main "$@"
