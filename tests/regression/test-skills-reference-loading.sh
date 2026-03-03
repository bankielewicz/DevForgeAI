#!/bin/bash

################################################################################
# STORY-044: Test 14 DevForgeAI Skills Reference Loading
# Purpose: Verify skills can load reference files from src/ paths
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
WARNINGS=0

test_skill() {
    local skill_name="$1"
    local skill_dir="$PROJECT_ROOT/.claude/skills/$skill_name"
    local skill_file="$skill_dir/SKILL.md"

    ((TOTAL++))

    # Test 1: Skill file exists
    if [ ! -f "$skill_file" ]; then
        echo -e "${RED}[FAIL]${NC} Skill file missing: $skill_name"
        ((FAILED++))
        return 1
    fi

    # Test 2: Skill file has content
    local size=$(wc -c < "$skill_file")
    if [ "$size" -lt 100 ]; then
        echo -e "${RED}[FAIL]${NC} Skill file too small: $skill_name ($size bytes)"
        ((FAILED++))
        return 1
    fi

    # Test 3: Check for reference directory
    if [ -d "$skill_dir/references" ]; then
        local ref_files=$(find "$skill_dir/references" -type f -name "*.md" 2>/dev/null | wc -l)
        if [ "$ref_files" -gt 0 ]; then
            echo -e "${GREEN}[PASS]${NC} $skill_name ($size bytes, $ref_files reference files)"
            ((PASSED++))
        else
            echo -e "${YELLOW}[WARN]${NC} $skill_name has empty references directory"
            ((WARNINGS++))
            ((PASSED++))
        fi
    else
        # References directory not required for all skills
        echo -e "${GREEN}[PASS]${NC} $skill_name ($size bytes, no references directory)"
        ((PASSED++))
    fi

    # Test 4: Verify reference files are readable (spot check)
    if [ -d "$skill_dir/references" ]; then
        local first_ref=$(find "$skill_dir/references" -type f -name "*.md" | head -1)
        if [ -n "$first_ref" ]; then
            local ref_size=$(wc -c < "$first_ref")
            if [ "$ref_size" -lt 50 ]; then
                echo -e "${YELLOW}[WARN]${NC}   Reference file too small: $(basename "$first_ref") ($ref_size bytes)"
                ((WARNINGS++))
            fi
        fi
    fi

    return 0
}

main() {
    echo "================================================================================"
    echo "Testing 14 DevForgeAI Skills Reference Loading"
    echo "================================================================================"
    echo

    # List of 14 DevForgeAI skills
    local skills=(
        "devforgeai-architecture"
        "devforgeai-development"
        "devforgeai-documentation"
        "devforgeai-feedback"
        "devforgeai-ideation"
        "devforgeai-mcp-cli-converter"
        "devforgeai-orchestration"
        "devforgeai-qa"
        "devforgeai-release"
        "devforgeai-rca"
        "devforgeai-story-creation"
        "devforgeai-subagent-creation"
        "devforgeai-ui-generator"
    )

    echo -e "${BLUE}DevForgeAI Skills:${NC}"
    for skill in "${skills[@]}"; do
        test_skill "$skill"
    done
    echo

    # Test claude-code-terminal-expert skill
    echo -e "${BLUE}Infrastructure Skill:${NC}"
    test_skill "claude-code-terminal-expert"
    echo

    echo "================================================================================"
    echo "Skills Reference Loading Summary"
    echo "================================================================================"
    echo "Total:    $TOTAL"
    echo "Passed:   $PASSED"
    echo "Failed:   $FAILED"
    echo "Warnings: $WARNINGS"
    echo

    if [ "$FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓ All 14 skills verified${NC}"
        if [ "$WARNINGS" -gt 0 ]; then
            echo -e "${YELLOW}Note: $WARNINGS warning(s) found${NC}"
        fi
        return 0
    else
        echo -e "${RED}✗ $FAILED skill(s) failed${NC}"
        return 1
    fi
}

main "$@"
