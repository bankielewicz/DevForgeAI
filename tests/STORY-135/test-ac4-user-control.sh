#!/bin/bash
# STORY-135 AC#4: User Maintains Control Over Architecture Skill Execution
# Tests that user has complete control and no automatic execution occurs

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
echo "STORY-135 AC#4: User Control"
echo "========================================"
echo ""

# Test 1: completion-handoff.md uses AskUserQuestion for next action
echo -n "Test 4.1: completion-handoff.md uses AskUserQuestion for next action... "
result=$(grep -q 'AskUserQuestion' "$PROJECT_ROOT/.claude/skills/devforgeai-ideation/references/completion-handoff.md" 2>/dev/null && echo "found" || true)
if [ "$result" = "found" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected AskUserQuestion in completion-handoff.md for user control"
    ((FAIL_COUNT++))
fi

# Test 2: Command exits cleanly after display (no forced workflow)
echo -n "Test 4.2: ideate.md has clean exit (Command Complete section)... "
result=$(grep -E 'Command Complete|Command responsibilities' "$PROJECT_ROOT/.claude/commands/ideate.md" 2>/dev/null || true)
if [ -n "$result" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected Command Complete section in ideate.md"
    ((FAIL_COUNT++))
fi

# Test 3: No forced workflow after ideation
echo -n "Test 4.3: No automatic workflow chaining in ideate.md... "
# Check for patterns like "THEN invoke" or "THEN Skill(" which would indicate forced workflow
result=$(grep -iE 'THEN\s+(invoke|Skill\s*\()' "$PROJECT_ROOT/.claude/commands/ideate.md" 2>/dev/null || true)
if [ -z "$result" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Found forced workflow pattern in ideate.md"
    ((FAIL_COUNT++))
fi

# Test 4: W3 compliance - no auto-chaining in artifact-generation.md
echo -n "Test 4.4: W3 compliance verified (no skill auto-chaining)... "
result=$(grep -E 'Skill\s*\(\s*command\s*=\s*["'"'"']devforgeai-architecture' "$PROJECT_ROOT/.claude/skills/devforgeai-ideation/references/artifact-generation.md" 2>/dev/null || true)
if [ -z "$result" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  W3 violation: artifact-generation.md auto-invokes architecture"
    ((FAIL_COUNT++))
fi

echo ""
echo "========================================"
echo "AC#4 Results: $PASS_COUNT passed, $FAIL_COUNT failed"
echo "========================================"

if [ $FAIL_COUNT -gt 0 ]; then
    exit 1
fi
exit 0
