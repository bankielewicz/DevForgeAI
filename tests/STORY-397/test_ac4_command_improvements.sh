#!/bin/bash
# Test: AC#4 - All 39 Command Files Reviewed and Improved
# Story: STORY-397
# Generated: 2026-02-13
# TDD Phase: RED (tests should FAIL before implementation)
#
# Validates that all command files use consistent parameter documentation
# format, include example invocations, specify skill delegation patterns,
# and follow the standardized command template structure.

set -uo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
COMMANDS_DIR="${PROJECT_ROOT}/src/claude/commands"

# All 39+ command files (discovered dynamically, then checked)
# We verify at least 39 command files exist per AC#4 scope
EXPECTED_MIN_COMMANDS=39

# Required command template sections
COMMAND_SECTIONS=(
    "## Purpose"
    "## Parameters"
    "## Examples"
    "## Skill Delegation"
    "## Error Handling"
)

# === Helper Functions ===
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

# === Test Suite ===
echo "============================================================"
echo "  AC#4: Command File Improvements (39 Commands)"
echo "  Story: STORY-397 | Phase: RED"
echo "============================================================"
echo ""

# --- Test Group 1: Minimum 39 command files exist ---
echo "--- Test Group 1: Command File Count ---"
COMMAND_FILES=()
while IFS= read -r -d '' file; do
    COMMAND_FILES+=("$file")
done < <(find "$COMMANDS_DIR" -maxdepth 1 -name "*.md" -type f -print0 2>/dev/null)
COMMAND_COUNT=${#COMMAND_FILES[@]}
echo "  Found ${COMMAND_COUNT} command files in src/claude/commands/"
if [ "$COMMAND_COUNT" -ge "$EXPECTED_MIN_COMMANDS" ] 2>/dev/null; then
    run_test "At least ${EXPECTED_MIN_COMMANDS} command files exist (found ${COMMAND_COUNT})" 0
else
    run_test "At least ${EXPECTED_MIN_COMMANDS} command files exist (found ${COMMAND_COUNT})" 1
fi
echo ""

# --- Test Group 2: YAML Frontmatter with description and argument-hint ---
echo "--- Test Group 2: YAML Frontmatter Completeness ---"
for file in "${COMMAND_FILES[@]}"; do
    BASENAME=$(basename "$file")
    if [ -f "$file" ]; then
        # Check frontmatter starts with ---
        if head -1 "$file" | grep -q '^---$'; then
            run_test "YAML frontmatter present: ${BASENAME}" 0
        else
            run_test "YAML frontmatter present: ${BASENAME}" 1
        fi

        # Check description: field
        if grep -q '^description:' "$file" 2>/dev/null; then
            run_test "description: field in ${BASENAME}" 0
        else
            run_test "description: field in ${BASENAME}" 1
        fi

        # Check argument-hint: field
        if grep -q '^argument-hint:' "$file" 2>/dev/null; then
            run_test "argument-hint: field in ${BASENAME}" 0
        else
            run_test "argument-hint: field in ${BASENAME}" 1
        fi
    fi
done
echo ""

# --- Test Group 3: Required command template sections ---
echo "--- Test Group 3: Standardized Section Headers ---"
for file in "${COMMAND_FILES[@]}"; do
    BASENAME=$(basename "$file")
    if [ -f "$file" ]; then
        for section in "${COMMAND_SECTIONS[@]}"; do
            if grep -q "^${section}" "$file" 2>/dev/null; then
                run_test "Section '${section}' in ${BASENAME}" 0
            else
                run_test "Section '${section}' in ${BASENAME}" 1
            fi
        done
    fi
done
echo ""

# --- Test Group 4: Example invocations present ---
echo "--- Test Group 4: Example Invocations ---"
for file in "${COMMAND_FILES[@]}"; do
    BASENAME=$(basename "$file")
    if [ -f "$file" ]; then
        # Check Examples section has actual command examples (code blocks or inline code)
        EXAMPLES_SECTION=$(awk '/^## Examples/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$file")
        EXAMPLE_FOUND=1
        if echo "$EXAMPLES_SECTION" | grep -qE '(```|`/[a-z]|Skill\(|/[a-z]+-?[a-z]*)'; then
            EXAMPLE_FOUND=0
        fi
        run_test "Example invocation in Examples: ${BASENAME}" $EXAMPLE_FOUND
    fi
done
echo ""

# --- Test Group 5: Skill delegation patterns specified ---
echo "--- Test Group 5: Skill Delegation Clarity ---"
for file in "${COMMAND_FILES[@]}"; do
    BASENAME=$(basename "$file")
    if [ -f "$file" ]; then
        # Check Skill Delegation section references a skill or subagent
        DELEGATION_SECTION=$(awk '/^## Skill Delegation/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$file")
        DELEGATION_FOUND=1
        if echo "$DELEGATION_SECTION" | grep -qiE '(Skill\(|Task\(|devforgeai-|subagent|skill)'; then
            DELEGATION_FOUND=0
        fi
        run_test "Skill delegation specified: ${BASENAME}" $DELEGATION_FOUND
    fi
done
echo ""

# --- Test Group 6: Consistent parameter documentation format ---
echo "--- Test Group 6: Parameter Documentation Format ---"
for file in "${COMMAND_FILES[@]}"; do
    BASENAME=$(basename "$file")
    if [ -f "$file" ]; then
        # Check Parameters section has structured format
        # Look for table format (|) or list format (-)
        PARAMS_SECTION=$(awk '/^## Parameters/{found=1; next} found && /^## [A-Z]/{exit} found{print}' "$file")
        PARAMS_FOUND=1
        if echo "$PARAMS_SECTION" | grep -qE '(\|.*\||- |`\$ARGUMENTS`)'; then
            PARAMS_FOUND=0
        fi
        run_test "Structured parameter docs: ${BASENAME}" $PARAMS_FOUND
    fi
done
echo ""

# --- Test Group 7: Zero interface changes (command signatures preserved) ---
echo "--- Test Group 7: Command Signature Preservation ---"
for file in "${COMMAND_FILES[@]}"; do
    BASENAME=$(basename "$file")
    if [ -f "$file" ]; then
        # Verify $ARGUMENTS placeholder still present (signature contract)
        if grep -q '\$ARGUMENTS' "$file" 2>/dev/null; then
            run_test "\$ARGUMENTS placeholder present: ${BASENAME}" 0
        else
            run_test "\$ARGUMENTS placeholder present: ${BASENAME}" 1
        fi
    fi
done
echo ""

# === Summary ===
echo "============================================================"
echo "  AC#4 Results: ${PASSED} passed, ${FAILED} failed (${TOTAL} total)"
echo "============================================================"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
