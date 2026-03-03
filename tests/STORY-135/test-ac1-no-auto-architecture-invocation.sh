#!/bin/bash
# STORY-135 AC#1: Remove Auto-Architecture Invocation from Command
# Tests that the /ideate command does NOT auto-invoke devforgeai-architecture skill

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PASS_COUNT=0
FAIL_COUNT=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "========================================"
echo "STORY-135 AC#1: No Auto-Architecture Invocation"
echo "========================================"
echo ""

# Test 1: ideate.md command has NO Skill() calls for architecture
echo -n "Test 1.1: ideate.md has no Skill(devforgeai-architecture) calls... "
result=$(grep -E 'Skill\s*\(\s*command\s*=\s*["'"'"']devforgeai-architecture' "$PROJECT_ROOT/.claude/commands/ideate.md" 2>/dev/null || true)
if [ -z "$result" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Found auto-invocation pattern in ideate.md"
    ((FAIL_COUNT++))
fi

# Test 2: ideate.md command has NO Task() calls for architecture
echo -n "Test 1.2: ideate.md has no Task() calls for architecture... "
result=$(grep -E 'Task\s*\(.*architecture' "$PROJECT_ROOT/.claude/commands/ideate.md" 2>/dev/null || true)
if [ -z "$result" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Found Task() call for architecture in ideate.md"
    ((FAIL_COUNT++))
fi

# Test 3: artifact-generation.md has NO auto-invocation
echo -n "Test 1.3: artifact-generation.md has no auto Skill(devforgeai-architecture)... "
result=$(grep -E 'Skill\s*\(\s*command\s*=\s*["'"'"']devforgeai-architecture' "$PROJECT_ROOT/.claude/skills/devforgeai-ideation/references/artifact-generation.md" 2>/dev/null || true)
if [ -z "$result" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Found auto-invocation in artifact-generation.md - violates W3 compliance"
    ((FAIL_COUNT++))
fi

# Test 4: ideate.md references completion-handoff.md for next action (not auto-invoke)
echo -n "Test 1.4: ideate.md uses result-interpreter for display (not auto-invoke)... "
result=$(grep -q 'ideation-result-interpreter' "$PROJECT_ROOT/.claude/commands/ideate.md" 2>/dev/null && echo "found" || true)
if [ "$result" = "found" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected ideation-result-interpreter pattern for display-only"
    ((FAIL_COUNT++))
fi

echo ""
echo "========================================"
echo "AC#1 Results: $PASS_COUNT passed, $FAIL_COUNT failed"
echo "========================================"

if [ $FAIL_COUNT -gt 0 ]; then
    exit 1
fi
exit 0
