#!/bin/bash
# STORY-135 AC#2: Skill Phase 6.6 Displays Recommended Next Action
# Tests that the skill displays "Run `/create-context [project-name]`" as recommended next action

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
echo "STORY-135 AC#2: Skill Displays Next Action"
echo "========================================"
echo ""

# Test 1: completion-handoff.md contains "/create-context" recommendation text
echo -n "Test 2.1: completion-handoff.md contains /create-context recommendation... "
result=$(grep -q '/create-context' "$PROJECT_ROOT/.claude/skills/devforgeai-ideation/references/completion-handoff.md" 2>/dev/null && echo "found" || true)
if [ "$result" = "found" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected /create-context recommendation in completion-handoff.md"
    ((FAIL_COUNT++))
fi

# Test 2: completion-handoff.md shows "Run `/create-context" text format
echo -n "Test 2.2: completion-handoff.md has 'Run /create-context' format... "
result=$(grep 'Run.*\/create-context' "$PROJECT_ROOT/.claude/skills/devforgeai-ideation/references/completion-handoff.md" 2>/dev/null || true)
if [ -n "$result" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected 'Run /create-context' format in completion-handoff.md"
    ((FAIL_COUNT++))
fi

# Test 3: Phase 6.6 or Step 6.6 exists in completion-handoff.md
echo -n "Test 2.3: completion-handoff.md has Step 6.6 for next action determination... "
result=$(grep -E 'Step 6\.6|Phase 6\.6' "$PROJECT_ROOT/.claude/skills/devforgeai-ideation/references/completion-handoff.md" 2>/dev/null || true)
if [ -n "$result" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected Step 6.6 or Phase 6.6 in completion-handoff.md"
    ((FAIL_COUNT++))
fi

# Test 4: Greenfield path shows /create-context recommendation
echo -n "Test 2.4: Greenfield path recommends /create-context... "
result=$(grep -A 5 -i 'greenfield' "$PROJECT_ROOT/.claude/skills/devforgeai-ideation/references/completion-handoff.md" 2>/dev/null | grep '/create-context' || true)
if [ -n "$result" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected greenfield path to recommend /create-context"
    ((FAIL_COUNT++))
fi

echo ""
echo "========================================"
echo "AC#2 Results: $PASS_COUNT passed, $FAIL_COUNT failed"
echo "========================================"

if [ $FAIL_COUNT -gt 0 ]; then
    exit 1
fi
exit 0
