#!/bin/bash
#
# DevForgeAI Pre-Commit Hook Installer
#
# Installs pre-commit hook that validates:
# - DoD completion (prevents autonomous deferrals)
# - Story file format
# - User approval markers
#
# Based on industry patterns: pre-commit.com, SpecDriven AI
#

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  DevForgeAI Pre-Commit Hook Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if in Git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a Git repository"
    echo ""
    echo "Initialize Git first:"
    echo "  git init"
    echo "  git add ."
    echo "  git commit -m 'Initial commit'"
    echo ""
    exit 1
fi

# Check if Python available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 not found"
    echo ""
    echo "Install Python 3.8 or higher"
    exit 1
fi

# Check if DevForgeAI CLI validators available
if [ ! -f ".claude/scripts/devforgeai_cli/validators/dod_validator.py" ]; then
    echo "❌ Error: DevForgeAI CLI not found"
    echo ""
    echo "Expected location: .claude/scripts/devforgeai_cli/"
    echo ""
    echo "Install DevForgeAI CLI first:"
    echo "  pip install -e .claude/scripts/"
    exit 1
fi

echo "Installing pre-commit hook..."
echo ""

# Create pre-commit hook
cat > .git/hooks/pre-commit <<'EOF'
#!/bin/bash
#
# DevForgeAI Pre-Commit Validation Hook
#
# Validates story files before commit to prevent:
# - Autonomous deferrals (DoD [x] but Impl [ ] without user approval)
# - Missing Implementation Notes
# - Invalid deferral justifications
#
# To bypass (NOT RECOMMENDED): git commit --no-verify
#

echo ""
echo "🔍 DevForgeAI Validators Running..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Find story files in staging area
STORY_FILES=$(git diff --cached --name-only | grep '\.story\.md$' || true)

if [ -z "$STORY_FILES" ]; then
    echo "  No story files to validate"
    echo "✅ Pre-commit validation passed"
    echo ""
    exit 0
fi

# Validate each story file
VALIDATION_FAILED=0

for file in $STORY_FILES; do
    echo "  📋 Validating: $file"

    # Run DoD validator
    if python3 .claude/scripts/devforgeai_cli/validators/dod_validator.py "$file"; then
        echo "     ✅ Passed"
    else
        echo "     ❌ Failed"
        VALIDATION_FAILED=1
    fi
done

echo ""

if [ $VALIDATION_FAILED -eq 1 ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "❌ COMMIT BLOCKED - Fix violations"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "One or more story files have validation errors."
    echo "Fix the violations shown above before committing."
    echo ""
    echo "To bypass validation (NOT RECOMMENDED):"
    echo "  git commit --no-verify"
    echo ""
    exit 1
fi

echo "✅ All validators passed - commit allowed"
echo ""
exit 0
EOF

# Make hook executable
chmod +x .git/hooks/pre-commit

echo "✅ Pre-commit hook installed successfully"
echo ""
echo "Location: .git/hooks/pre-commit"
echo ""
echo "The hook will automatically run on 'git commit' and validate:"
echo "  • DoD completion status"
echo "  • Autonomous deferral detection"
echo "  • User approval markers for deferrals"
echo "  • Story/ADR reference validation"
echo ""
echo "To test the hook:"
echo "  git add .ai_docs/Stories/STORY-XXX.story.md"
echo "  git commit -m 'Test commit'"
echo ""
echo "To bypass validation (not recommended):"
echo "  git commit --no-verify"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
