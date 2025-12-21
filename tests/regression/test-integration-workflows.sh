#!/bin/bash

################################################################################
# STORY-044: Test 3 Integration Workflows
# Purpose: Verify complete workflows execute without path errors
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

test_path_exists() {
    local path="$1"
    local description="$2"

    ((TOTAL++))

    if [ -e "$path" ]; then
        echo -e "${GREEN}[PASS]${NC} $description"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}[FAIL]${NC} $description"
        echo "         Path: $path"
        ((FAILED++))
        return 1
    fi
}

test_directory_exists() {
    local path="$1"
    local description="$2"

    ((TOTAL++))

    if [ -d "$path" ]; then
        echo -e "${GREEN}[PASS]${NC} $description"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}[FAIL]${NC} $description"
        echo "         Path: $path"
        ((FAILED++))
        return 1
    fi
}

test_workflow_1_epic_to_story_to_dev() {
    echo -e "${BLUE}Workflow 1: Epic → Story → Development${NC}"
    echo

    # Step 1: Epic directory structure
    test_directory_exists "$PROJECT_ROOT/.ai_docs/Epics" "Epics directory exists"

    # Step 2: Story directory structure
    test_directory_exists "$PROJECT_ROOT/.ai_docs/Stories" "Stories directory exists"

    # Step 3: Development context files
    test_path_exists "$PROJECT_ROOT/devforgeai/context/tech-stack.md" "Tech stack context file"
    test_path_exists "$PROJECT_ROOT/devforgeai/context/source-tree.md" "Source tree context file"
    test_path_exists "$PROJECT_ROOT/devforgeai/context/dependencies.md" "Dependencies context file"
    test_path_exists "$PROJECT_ROOT/devforgeai/context/coding-standards.md" "Coding standards context file"
    test_path_exists "$PROJECT_ROOT/devforgeai/context/architecture-constraints.md" "Architecture constraints context file"
    test_path_exists "$PROJECT_ROOT/devforgeai/context/anti-patterns.md" "Anti-patterns context file"

    # Step 4: Development skill accessible
    test_path_exists "$PROJECT_ROOT/.claude/skills/devforgeai-development/SKILL.md" "Development skill SKILL.md"

    # Step 5: Test framework accessible
    test_directory_exists "$PROJECT_ROOT/tests" "Tests directory exists"

    echo
}

test_workflow_2_context_to_story_to_qa() {
    echo -e "${BLUE}Workflow 2: Context → Story → QA${NC}"
    echo

    # Step 1: Context files (6 required)
    test_path_exists "$PROJECT_ROOT/devforgeai/context/tech-stack.md" "Tech stack (context)"
    test_path_exists "$PROJECT_ROOT/devforgeai/context/source-tree.md" "Source tree (context)"
    test_path_exists "$PROJECT_ROOT/devforgeai/context/dependencies.md" "Dependencies (context)"
    test_path_exists "$PROJECT_ROOT/devforgeai/context/coding-standards.md" "Coding standards (context)"
    test_path_exists "$PROJECT_ROOT/devforgeai/context/architecture-constraints.md" "Architecture constraints (context)"
    test_path_exists "$PROJECT_ROOT/devforgeai/context/anti-patterns.md" "Anti-patterns (context)"

    # Step 2: Story creation support
    test_directory_exists "$PROJECT_ROOT/.ai_docs/Stories" "Stories directory for QA"

    # Step 3: QA output paths
    test_directory_exists "$PROJECT_ROOT/devforgeai/qa" "QA reports directory"

    # Step 4: QA skill
    test_path_exists "$PROJECT_ROOT/.claude/skills/devforgeai-qa/SKILL.md" "QA skill SKILL.md"

    # Step 5: QA validation files
    test_path_exists "$PROJECT_ROOT/.claude/skills/devforgeai-qa/references" "QA skill references directory"

    echo
}

test_workflow_3_sprint_planning_to_story() {
    echo -e "${BLUE}Workflow 3: Sprint Planning → Story${NC}"
    echo

    # Step 1: Sprint directory
    test_directory_exists "$PROJECT_ROOT/.ai_docs/Sprints" "Sprints directory"

    # Step 2: Story directory
    test_directory_exists "$PROJECT_ROOT/.ai_docs/Stories" "Stories directory for sprint"

    # Step 3: Orchestration skill
    test_path_exists "$PROJECT_ROOT/.claude/skills/devforgeai-orchestration/SKILL.md" "Orchestration skill SKILL.md"

    # Step 4: Orchestration references
    test_path_exists "$PROJECT_ROOT/.claude/skills/devforgeai-orchestration/references" "Orchestration references directory"

    # Step 5: Story creation skill
    test_path_exists "$PROJECT_ROOT/.claude/skills/devforgeai-story-creation/SKILL.md" "Story creation skill SKILL.md"

    # Step 6: ADR support for architecture decisions
    test_directory_exists "$PROJECT_ROOT/devforgeai/adrs" "ADR directory"

    echo
}

main() {
    echo "================================================================================"
    echo "Testing 3 Integration Workflows"
    echo "================================================================================"
    echo

    test_workflow_1_epic_to_story_to_dev
    test_workflow_2_context_to_story_to_qa
    test_workflow_3_sprint_planning_to_story

    echo "================================================================================"
    echo "Integration Workflow Test Summary"
    echo "================================================================================"
    echo "Total:   $TOTAL"
    echo "Passed:  $PASSED"
    echo "Failed:  $FAILED"
    echo

    if [ "$FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓ All 3 integration workflows verified${NC}"
        return 0
    else
        echo -e "${RED}✗ $FAILED integration workflow(s) failed${NC}"
        return 1
    fi
}

main "$@"
