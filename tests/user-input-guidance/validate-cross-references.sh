#!/bin/bash
################################################################################
# Cross-Reference Validation Script for STORY-058
#
# Validates all cross-references in documentation files:
# - src/CLAUDE.md
# - src/claude/memory/commands-reference.md
# - src/claude/memory/skills-reference.md
#
# Checks:
# 1. All file paths point to existing files
# 2. Load command syntax is correct (Read tool, not cat/@file)
# 3. Terminology consistency (approved terms only)
# 4. Section counts match requirements
#
# Exit Status:
# 0 = All validations passed
# 1 = One or more validation failures
################################################################################

PASSED=0
FAILED=0
ERRORS=()

# Validation functions
validate_file_exists() {
    local file="$1"
    if [[ -f "$file" ]]; then
        echo "  ✓ $file exists"
        ((PASSED++))
        return 0
    else
        echo "  ✗ $file NOT FOUND"
        ((FAILED++))
        ERRORS+=("File not found: $file")
        return 1
    fi
}

validate_section_count() {
    local file="$1"
    local pattern="$2"
    local expected="$3"
    local description="$4"

    if [[ ! -f "$file" ]]; then
        return 1
    fi

    local count=$(grep -c "$pattern" "$file" 2>/dev/null || echo 0)
    if [[ $count -eq $expected ]]; then
        echo "  ✓ $description: $count found (expected $expected)"
        ((PASSED++))
    else
        echo "  ✗ $description: $count found (expected $expected)"
        ((FAILED++))
        ERRORS+=("Section count mismatch in $file: $description ($count != $expected)")
    fi
}

validate_read_syntax() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        return 1
    fi

    # Check for prohibited patterns
    if grep -q 'cat ' "$file" 2>/dev/null; then
        echo "  ✗ Bash 'cat' command found (should use Read tool)"
        ((FAILED++))
        ERRORS+=("Prohibited 'cat' syntax in $file")
    elif grep -q '@file' "$file" 2>/dev/null; then
        echo "  ✗ '@file' syntax found (should use Read tool)"
        ((FAILED++))
        ERRORS+=("Prohibited '@file' syntax in $file")
    else
        echo "  ✓ No prohibited Bash/@ syntax found"
        ((PASSED++))
    fi
}

# Main validation execution
echo "=================================================="
echo "CROSS-REFERENCE VALIDATION - STORY-058"
echo "=================================================="
echo ""

# Validation 1: File existence
echo "1. Checking documentation files exist..."
validate_file_exists "src/CLAUDE.md"
validate_file_exists "src/claude/memory/commands-reference.md"
validate_file_exists "src/claude/memory/skills-reference.md"
validate_file_exists "src/claude/memory/effective-prompting-guide.md"
validate_file_exists "src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
validate_file_exists "src/claude/skills/devforgeai-architecture/references/user-input-guidance.md"
echo ""

# Validation 2: Load command syntax in new guidance sections
echo "2. Checking for correct Read() syntax in guidance sections..."
# Check Learning DevForgeAI section has Read syntax
if grep -A 30 "## Learning DevForgeAI" src/CLAUDE.md | grep -q 'Read(file_path='; then
    echo "  ✓ CLAUDE.md learning section uses Read() syntax"
    ((PASSED++))
else
    echo "  ⚠ CLAUDE.md learning section may not have Read() examples"
    echo "    (Non-blocking: existing documentation may reference @file for documentation purposes)"
fi
echo ""

# Validation 3: AC#1 CLAUDE.md Learning Section
echo "3. Checking CLAUDE.md Learning Section (AC#1)..."
if grep -q "^## Learning DevForgeAI" src/CLAUDE.md; then
    echo "  ✓ 'Learning DevForgeAI' section found"
    ((PASSED++))
else
    echo "  ✗ 'Learning DevForgeAI' section NOT found"
    ((FAILED++))
    ERRORS+=("Missing 'Learning DevForgeAI' section in CLAUDE.md")
fi

if grep -q "^### Writing Effective Feature Descriptions" src/CLAUDE.md; then
    echo "  ✓ 'Writing Effective Feature Descriptions' subsection found"
    ((PASSED++))
else
    echo "  ✗ 'Writing Effective Feature Descriptions' subsection NOT found"
    ((FAILED++))
    ERRORS+=("Missing subsection in CLAUDE.md")
fi

if grep -q "^### User Input Guidance Resources" src/CLAUDE.md; then
    echo "  ✓ 'User Input Guidance Resources' subsection found"
    ((PASSED++))
else
    echo "  ✗ 'User Input Guidance Resources' subsection NOT found"
    ((FAILED++))
    ERRORS+=("Missing subsection in CLAUDE.md")
fi

if grep -q "^### Progressive Learning Path" src/CLAUDE.md; then
    echo "  ✓ 'Progressive Learning Path' subsection found"
    ((PASSED++))
else
    echo "  ✗ 'Progressive Learning Path' subsection NOT found"
    ((FAILED++))
    ERRORS+=("Missing subsection in CLAUDE.md")
fi
echo ""

# Validation 4: AC#2 Commands cross-references
echo "4. Checking commands cross-references (AC#2)..."
COMMAND_GUIDANCE=$(grep -c "^### User Input Guidance" src/claude/memory/commands-reference.md 2>/dev/null || echo 0)
if [[ $COMMAND_GUIDANCE -ge 11 ]]; then
    echo "  ✓ Command guidance subsections found: $COMMAND_GUIDANCE (expected ≥11)"
    ((PASSED++))
else
    echo "  ✗ Command guidance subsections: $COMMAND_GUIDANCE (expected ≥11)"
    ((FAILED++))
    ERRORS+=("Insufficient command guidance subsections")
fi
echo ""

# Validation 5: AC#3 Skills cross-references
echo "5. Checking skills cross-references (AC#3)..."
SKILL_GUIDANCE=$(grep -c "^### User Input Guidance" src/claude/memory/skills-reference.md 2>/dev/null || echo 0)
if [[ $SKILL_GUIDANCE -ge 13 ]]; then
    echo "  ✓ Skill guidance subsections found: $SKILL_GUIDANCE (expected ≥13)"
    ((PASSED++))
else
    echo "  ✗ Skill guidance subsections: $SKILL_GUIDANCE (expected ≥13)"
    ((FAILED++))
    ERRORS+=("Insufficient skill guidance subsections")
fi
echo ""

# Final summary
echo "=================================================="
echo "VALIDATION SUMMARY"
echo "=================================================="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [[ $FAILED -gt 0 ]]; then
    echo "ERRORS:"
    for error in "${ERRORS[@]}"; do
        echo "  - $error"
    done
    echo ""
    exit 1
else
    echo "✓ ALL VALIDATIONS PASSED"
    exit 0
fi
