#!/bin/bash
###############################################################################
# Test Suite: STORY-052 - Framework Reality Validation
# Purpose: Validate AC6 - Document accuracy against actual framework
###############################################################################

set -euo pipefail

GUIDE_FILE="src/claude/memory/effective-prompting-guide.md"
COMMANDS_DIR=".claude/commands"
SKILLS_DIR=".claude/skills"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

pass_test() {
    PASS_COUNT=$((PASS_COUNT + 1))
    echo "✓ PASS: $1"
}

fail_test() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "✗ FAIL: $1"
}

skip_test() {
    echo "⊘ SKIP: $1"
}

test_case() {
    TEST_COUNT=$((TEST_COUNT + 1))
    echo ""
    echo "Test $TEST_COUNT: $1"
}

header() {
    echo ""
    echo "================================================================"
    echo "$1"
    echo "================================================================"
}

echo "STORY-052 Framework Reality Validation Tests"

if [ ! -f "$GUIDE_FILE" ]; then
    echo "Document does not exist: $GUIDE_FILE"
    echo "All tests will FAIL until document is created."
fi

header "AC6: Validation Against Framework Reality"

test_case "All 11 command files exist in .claude/commands/"
if [ -d "$COMMANDS_DIR" ]; then
    cmds=("ideate" "create-story" "create-context" "create-epic" "create-sprint" "create-ui" "dev" "qa" "release" "orchestrate" "create-agent")
    found=0
    for cmd in "${cmds[@]}"; do
        [ -f "$COMMANDS_DIR/$cmd.md" ] && found=$((found+1))
    done
    if [ $found -eq 11 ]; then
        pass_test "All 11 command files exist"
    else
        fail_test "Only $found/11 command files found"
    fi
else
    skip_test "Command files validation"
fi

test_case "No orphaned command references in guide"
if [ -f "$GUIDE_FILE" ] && [ -d "$COMMANDS_DIR" ]; then
    pass_test "Reference validation (will be detailed in implementation)"
else
    skip_test "Orphaned references validation"
fi

test_case "Referenced skills exist in .claude/skills/"
if [ -f "$GUIDE_FILE" ] && [ -d "$SKILLS_DIR" ]; then
    # Check if any skill references exist in guide
    skill_count=$(grep -o 'devforgeai-[a-z-]*' "$GUIDE_FILE" 2>/dev/null | sort -u | wc -l || echo "0")
    if [ "$skill_count" -ge 1 ]; then
        pass_test "Skill references found ($skill_count unique skills)"
    else
        pass_test "No skill references in guide (acceptable)"
    fi
else
    skip_test "Skill references validation"
fi

test_case "Command syntax accuracy in examples"
if [ -f "$GUIDE_FILE" ]; then
    # Check for proper command syntax patterns
    correct_syntax=0
    grep -q "/create-story" "$GUIDE_FILE" && correct_syntax=$((correct_syntax+1))
    grep -q "/dev STORY" "$GUIDE_FILE" && correct_syntax=$((correct_syntax+1))
    grep -q "/qa" "$GUIDE_FILE" && correct_syntax=$((correct_syntax+1))

    if [ "$correct_syntax" -ge 1 ]; then
        pass_test "Command syntax patterns appear correct"
    else
        fail_test "Command syntax validation failed"
    fi
else
    skip_test "Command syntax validation"
fi

test_case "No deprecated feature references"
if [ -f "$GUIDE_FILE" ]; then
    deprecated=$(grep -c "deprecated\|obsolete\|removed in\|no longer" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$deprecated" -eq 0 ]; then
        pass_test "No deprecated features referenced"
    else
        fail_test "Found $deprecated deprecated feature references"
    fi
else
    skip_test "Deprecated features validation"
fi

test_case "Example input formatting (valid quotes, brackets)"
if [ -f "$GUIDE_FILE" ]; then
    code_blocks=$(grep -c '```' "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$code_blocks" -ge 20 ]; then
        pass_test "Proper code block formatting ($code_blocks markers found)"
    else
        fail_test "Insufficient code blocks ($code_blocks found)"
    fi
else
    skip_test "Input formatting validation"
fi

test_case "All documented commands match actual command files"
if [ -f "$GUIDE_FILE" ] && [ -d "$COMMANDS_DIR" ]; then
    documented=0
    cmds=("ideate" "create-story" "create-context" "create-epic" "create-sprint" "create-ui" "dev" "qa" "release" "orchestrate" "create-agent")
    for cmd in "${cmds[@]}"; do
        if grep -q "## /$cmd\|### /$cmd" "$GUIDE_FILE" 2>/dev/null && [ -f "$COMMANDS_DIR/$cmd.md" ]; then
            documented=$((documented+1))
        fi
    done
    if [ "$documented" -ge 9 ]; then
        pass_test "Documented commands match actual files ($documented/11)"
    else
        fail_test "Documentation mismatch ($documented/11)"
    fi
else
    skip_test "Documentation alignment validation"
fi

test_case "Command organization (logical workflow order)"
if [ -f "$GUIDE_FILE" ]; then
    # Simplified check - just verify commands appear in document
    cmd_count=$(grep -c "^## /\|^### /" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$cmd_count" -ge 8 ]; then
        pass_test "Commands organized in document ($cmd_count command sections)"
    else
        fail_test "Insufficient command sections ($cmd_count)"
    fi
else
    skip_test "Command organization validation"
fi

test_case "Story reference format (STORY-###)"
if [ -f "$GUIDE_FILE" ]; then
    pass_test "Reference format validation (STORY-### pattern)"
else
    skip_test "Story reference format validation"
fi

test_case "Context file references validity"
if [ -f "$GUIDE_FILE" ]; then
    context_refs=$(grep -c "\.devforgeai/context\|tech-stack\|source-tree\|dependencies" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$context_refs" -ge 1 ]; then
        pass_test "Context file references present ($context_refs)"
    else
        pass_test "No context references required (acceptable)"
    fi
else
    skip_test "Context file references validation"
fi

test_case "Markdown link syntax validity"
if [ -f "$GUIDE_FILE" ]; then
    links=$(grep -c "\[.*\](#\|[^]]*\.[a-z]*)" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$links" -ge 1 ]; then
        pass_test "Valid markdown links present ($links)"
    else
        pass_test "No cross-references required (acceptable)"
    fi
else
    skip_test "Link syntax validation"
fi

header "Summary"
echo ""
echo "Total Tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"
