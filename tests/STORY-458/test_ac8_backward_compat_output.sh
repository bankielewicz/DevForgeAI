#!/bin/bash
# Test: AC#8 - Backward-compatible output for all command modes
# Story: STORY-458
# Generated: 2026-02-20
# Expected: FAIL (TDD Red phase - error types must be preserved in command or skill references)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

CMD_SPRINT="${PROJECT_ROOT}/src/claude/commands/create-sprint.md"
CMD_TRIAGE="${PROJECT_ROOT}/src/claude/commands/recommendations-triage.md"
SPRINT_WORKFLOW="${PROJECT_ROOT}/src/claude/skills/devforgeai-orchestration/references/sprint-command-workflow.md"
TRIAGE_WORKFLOW="${PROJECT_ROOT}/src/claude/skills/devforgeai-feedback/references/triage-workflow.md"

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

# Search in both command and skill reference files for a pattern
search_sprint_files() {
    local pattern="$1"
    local found=1
    if [ -f "$CMD_SPRINT" ] && grep -qi "$pattern" "$CMD_SPRINT"; then
        found=0
    elif [ -f "$SPRINT_WORKFLOW" ] && grep -qi "$pattern" "$SPRINT_WORKFLOW"; then
        found=0
    fi
    return $found
}

search_triage_files() {
    local pattern="$1"
    local found=1
    if [ -f "$CMD_TRIAGE" ] && grep -qi "$pattern" "$CMD_TRIAGE"; then
        found=0
    elif [ -f "$TRIAGE_WORKFLOW" ] && grep -qi "$pattern" "$TRIAGE_WORKFLOW"; then
        found=0
    fi
    return $found
}

echo "=============================================="
echo "  AC#8: Backward-Compatible Output"
echo "  Story: STORY-458"
echo "=============================================="
echo ""

# === Sprint: 5 error types preserved (in command or skill reference) ===
echo "  --- Sprint Error Types ---"

# Error Type 1: No Args
test_result=0
if search_sprint_files 'no arg\|no.*argument\|missing.*name\|prompt.*name'; then
    test_result=0
else
    test_result=1
fi
run_test "Sprint error: No Args / Missing Name handling" "$test_result"

# Error Type 2: No Epics
test_result=0
if search_sprint_files 'no epic\|no.*epics.*found\|epic.*not found'; then
    test_result=0
else
    test_result=1
fi
run_test "Sprint error: No Epics Found handling" "$test_result"

# Error Type 3: No Backlog
test_result=0
if search_sprint_files 'no backlog\|no.*stories.*backlog\|backlog.*empty\|no.*stories.*available'; then
    test_result=0
else
    test_result=1
fi
run_test "Sprint error: No Backlog Stories handling" "$test_result"

# Error Type 4: Selection Cancelled
test_result=0
if search_sprint_files 'cancel\|abort\|selection.*cancel'; then
    test_result=0
else
    test_result=1
fi
run_test "Sprint error: Selection Cancelled handling" "$test_result"

# Error Type 5: Skill Failed
test_result=0
if search_sprint_files 'skill.*fail\|fail.*skill\|error.*skill\|skill.*error'; then
    test_result=0
else
    test_result=1
fi
run_test "Sprint error: Skill Failed handling" "$test_result"

echo ""
echo "  --- Triage Error Types ---"

# Triage Error Type 1: Queue File Not Found
test_result=0
if search_triage_files 'queue.*not found\|queue.*missing\|file.*not found.*queue'; then
    test_result=0
else
    test_result=1
fi
run_test "Triage error: Queue File Not Found handling" "$test_result"

# Triage Error Type 2: Story Creation Failed
test_result=0
if search_triage_files 'story creation.*fail\|fail.*story.*creat\|creation.*error'; then
    test_result=0
else
    test_result=1
fi
run_test "Triage error: Story Creation Failed handling" "$test_result"

# Triage Error Type 3: Queue Write Failed
test_result=0
if search_triage_files 'queue.*write.*fail\|write.*fail.*queue\|update.*fail.*queue\|queue.*update.*fail'; then
    test_result=0
else
    test_result=1
fi
run_test "Triage error: Queue Write Failed handling" "$test_result"

echo ""
echo "  --- Help Text Sections ---"

# Help text must be preserved somewhere (command or skill reference)
test_result=0
if search_sprint_files 'quick reference\|Quick Reference'; then
    test_result=0
else
    test_result=1
fi
run_test "Sprint: Quick Reference section preserved" "$test_result"

test_result=0
if search_sprint_files 'error handling\|Error Handling'; then
    test_result=0
else
    test_result=1
fi
run_test "Sprint: Error Handling section preserved" "$test_result"

test_result=0
if search_triage_files 'quick reference\|Quick Reference'; then
    test_result=0
else
    test_result=1
fi
run_test "Triage: Quick Reference section preserved" "$test_result"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
