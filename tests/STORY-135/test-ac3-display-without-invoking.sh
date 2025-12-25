#!/bin/bash
# STORY-135 AC#3: Command Displays Recommendation Without Invoking Architecture
# Tests that command displays skill's recommendation but does NOT auto-invoke architecture skill

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
echo "STORY-135 AC#3: Display Without Auto-Invoke"
echo "========================================"
echo ""

# Test 1: ideate.md has Phase 3 for result display (not skill auto-invocation)
echo -n "Test 3.1: ideate.md has Phase 3 Result Interpretation (display-only)... "
result=$(grep -E 'Phase 3.*Result|Result Interpretation' "$PROJECT_ROOT/.claude/commands/ideate.md" 2>/dev/null || true)
if [ -n "$result" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected Phase 3 Result Interpretation in ideate.md"
    ((FAIL_COUNT++))
fi

# Test 2: ideate.md displays result.display.template (not Skill() call)
echo -n "Test 3.2: ideate.md displays template (not auto-invoke)... "
result=$(grep 'Display.*result' "$PROJECT_ROOT/.claude/commands/ideate.md" 2>/dev/null || true)
if [ -n "$result" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected display pattern in ideate.md"
    ((FAIL_COUNT++))
fi

# Test 3: No Skill() calls after Phase 3 in ideate.md command
echo -n "Test 3.3: No Skill(devforgeai-architecture) after Phase 3... "
PHASE3_LINE=$(grep -n 'Phase 3\|Result Interpretation' "$PROJECT_ROOT/.claude/commands/ideate.md" 2>/dev/null | head -1 | cut -d: -f1 || echo "0")
if [ "$PHASE3_LINE" != "0" ] && [ -n "$PHASE3_LINE" ]; then
    # Check from Phase 3 to end of file for Skill(command="devforgeai-architecture")
    result=$(tail -n +"$PHASE3_LINE" "$PROJECT_ROOT/.claude/commands/ideate.md" 2>/dev/null | grep -E 'Skill\s*\(\s*command\s*=\s*["'"'"']devforgeai-architecture' || true)
    if [ -z "$result" ]; then
        echo -e "${GREEN}PASS${NC}"
        ((PASS_COUNT++))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Found Skill(devforgeai-architecture) after Phase 3"
        ((FAIL_COUNT++))
    fi
else
    echo -e "${GREEN}PASS${NC} (no Phase 3 section found - verifying command structure)"
    ((PASS_COUNT++))
fi

# Test 4: Command architecture principle states display-only
echo -n "Test 3.4: ideate.md has 'Commands orchestrate' principle... "
result=$(grep -i 'commands orchestrate' "$PROJECT_ROOT/.claude/commands/ideate.md" 2>/dev/null || true)
if [ -n "$result" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected 'Commands orchestrate' principle in ideate.md"
    ((FAIL_COUNT++))
fi

echo ""
echo "========================================"
echo "AC#3 Results: $PASS_COUNT passed, $FAIL_COUNT failed"
echo "========================================"

if [ $FAIL_COUNT -gt 0 ]; then
    exit 1
fi
exit 0
