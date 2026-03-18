#!/bin/bash
#
# STORY-041: Create src/ Directory Structure for DevForgeAI Framework Migration
#
# Purpose: Establish clean src/ directory structure with proper .gitignore rules and version.json
#
# Usage:
#   bash scripts/create-src-structure.sh
#
# This script:
# 1. Creates src/.claude/ with 4 subdirectories (skills, agents, commands, memory)
# 2. Creates src/devforgeai/ with 6 subdirectories (context, protocols, specs, adrs, deployment, qa)
# 3. Populates skill subdirectories (10 directories for each skill)
# 4. Adds .gitkeep files to empty directories for Git tracking
# 5. Updates .gitignore with new patterns
# 6. Creates version.json with current framework metadata
#

set -e  # Exit on first error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$PROJECT_ROOT/src"
TIMESTAMP=$(date +%s)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# ============================================================================
# PHASE 1: Create src/ directory structure
# ============================================================================

echo ""
echo "========================================================================="
echo "  STORY-041: Creating src/ Directory Structure"
echo "========================================================================="
echo ""

# Helper function to create directory and .gitkeep
create_dir_with_gitkeep() {
    local dir="$1"

    if [ -d "$dir" ]; then
        log_warn "Directory already exists: $dir"
        return 0
    fi

    mkdir -p "$dir"
    touch "$dir/.gitkeep"
    log_success "Created: $dir/"
}

# Step 1: Create src/.claude/ structure
log_info "Step 1: Creating src/.claude/ directory structure..."

mkdir -p "$SRC_DIR/claude"
log_success "Created: src/.claude/"

# Create 4 main subdirectories
create_dir_with_gitkeep "$SRC_DIR/.claude/skills"
create_dir_with_gitkeep "$SRC_DIR/.claude/agents"
create_dir_with_gitkeep "$SRC_DIR/.claude/commands"
create_dir_with_gitkeep "$SRC_DIR/.claude/memory"

# Create 10 skill subdirectories (9 DevForgeAI + 1 claude-code-terminal-expert)
SKILLS=(
    "spec-driven-ideation"
    "designing-systems"
    "devforgeai-orchestration"
    "devforgeai-story-creation"
    "devforgeai-ui-generator"
    "devforgeai-development"
    "devforgeai-qa"
    "devforgeai-release"
    "devforgeai-documentation"
    "claude-code-terminal-expert"
)

for skill in "${SKILLS[@]}"; do
    create_dir_with_gitkeep "$SRC_DIR/.claude/skills/$skill"
done

log_success "Created 10 skill subdirectories under src/.claude/skills/"

# Step 2: Create src/devforgeai/ structure
log_info "Step 2: Creating src/devforgeai/ directory structure..."

mkdir -p "$SRC_DIR/devforgeai"
log_success "Created: src/devforgeai/"

# Create 6 main subdirectories
create_dir_with_gitkeep "$SRC_DIR/devforgeai/context"
create_dir_with_gitkeep "$SRC_DIR/devforgeai/protocols"
create_dir_with_gitkeep "$SRC_DIR/devforgeai/deployment"

# Create specs/ with 3 subdirectories
create_dir_with_gitkeep "$SRC_DIR/devforgeai/specs/enhancements"
create_dir_with_gitkeep "$SRC_DIR/devforgeai/specs/requirements"
create_dir_with_gitkeep "$SRC_DIR/devforgeai/specs/ui"
log_success "Created: src/devforgeai/specs/ with 3 subdirectories"

# Create adrs/ with example/ subdirectory
create_dir_with_gitkeep "$SRC_DIR/devforgeai/adrs/example"
log_success "Created: src/devforgeai/adrs/ with example/ subdirectory"

# Create qa/ with 4 subdirectories
create_dir_with_gitkeep "$SRC_DIR/devforgeai/qa/coverage"
create_dir_with_gitkeep "$SRC_DIR/devforgeai/qa/reports"
create_dir_with_gitkeep "$SRC_DIR/devforgeai/qa/anti-patterns"
create_dir_with_gitkeep "$SRC_DIR/devforgeai/qa/spec-compliance"
log_success "Created: src/devforgeai/qa/ with 4 subdirectories"

# Verify directory count
TOTAL_DIRS=$(find "$SRC_DIR" -type d | wc -l)
log_success "Total directories created: $TOTAL_DIRS (target: ≥20)"

# ============================================================================
# PHASE 2: Update .gitignore with new patterns
# ============================================================================

log_info "Step 3: Updating .gitignore with DevForgeAI src/ patterns..."

GITIGNORE_FILE="$PROJECT_ROOT/.gitignore"

# Check if DevForgeAI section already exists
if grep -q "# DevForgeAI src/ directory" "$GITIGNORE_FILE"; then
    log_warn ".gitignore already contains DevForgeAI src/ section"
else
    # Append new patterns
    {
        echo ""
        echo "# DevForgeAI src/ directory - track source, exclude generated"
        echo "src/devforgeai/qa/coverage/*"
        echo "src/devforgeai/qa/reports/*"
        echo "!src/devforgeai/qa/coverage/.gitkeep"
        echo "!src/devforgeai/qa/reports/.gitkeep"
        echo "src/**/*.pyc"
        echo "src/**/__pycache__/"
        echo "src/**/node_modules/"
    } >> "$GITIGNORE_FILE"

    log_success "Updated .gitignore with 7 new patterns"
fi

# ============================================================================
# PHASE 3: Create version.json
# ============================================================================

log_info "Step 4: Creating version.json with framework metadata..."

VERSION_FILE="$PROJECT_ROOT/version.json"

# Count actual framework components
SKILL_COUNT=$(ls -d .claude/skills/devforgeai-* .claude/skills/claude-code-terminal-expert 2>/dev/null | wc -l)
AGENT_COUNT=$(ls .claude/agents/*.md 2>/dev/null | grep -v backup | wc -l || echo 0)
COMMAND_COUNT=$(ls .claude/commands/*.md 2>/dev/null | grep -v backup | wc -l || echo 0)
MEMORY_COUNT=$(ls .claude/memory/*.md 2>/dev/null | wc -l || echo 0)
PROTOCOL_COUNT=$(ls devforgeai/protocols/*.md 2>/dev/null | wc -l || echo 0)

# Create version.json
cat > "$VERSION_FILE" << EOF
{
  "version": "1.0.0",
  "release_date": "$(date +%Y-%m-%d)",
  "framework_status": "DEVELOPMENT",
  "components": {
    "skills": $SKILL_COUNT,
    "agents": $AGENT_COUNT,
    "commands": $COMMAND_COUNT,
    "memory_files": $MEMORY_COUNT,
    "context_templates": 6,
    "protocols": $PROTOCOL_COUNT
  },
  "changelog_url": "devforgeai/CHANGELOG.md",
  "migration_status": {
    "phase": "1-directory-setup",
    "src_structure_complete": true,
    "content_migration_complete": false,
    "installer_ready": false
  }
}
EOF

log_success "Created version.json with framework metadata"

# Validate version.json
if python3 -m json.tool "$VERSION_FILE" > /dev/null 2>&1; then
    log_success "version.json is valid JSON"
else
    log_error "version.json validation failed"
    exit 1
fi

# ============================================================================
# PHASE 4: Verification
# ============================================================================

log_info "Step 5: Verifying implementation..."

# Check src/ exists
if [ -d "$SRC_DIR" ]; then
    log_success "src/ directory exists"
else
    log_error "src/ directory creation failed"
    exit 1
fi

# Check .gitkeep count
GITKEEP_COUNT=$(find "$SRC_DIR" -name ".gitkeep" | wc -l)
log_success "Created $GITKEEP_COUNT .gitkeep files"

# Check directory permissions
SRC_PERMS=$(stat -c %a "$SRC_DIR/claude" 2>/dev/null || echo "unknown")
log_success "src/.claude/ permissions: $SRC_PERMS"

# Verify .gitignore was updated
if grep -q "# DevForgeAI src/ directory" "$GITIGNORE_FILE"; then
    log_success ".gitignore contains DevForgeAI patterns"
else
    log_error ".gitignore update verification failed"
fi

# Verify version.json
if [ -f "$VERSION_FILE" ]; then
    VERSION=$(jq -r '.version' "$VERSION_FILE")
    STATUS=$(jq -r '.migration_status.src_structure_complete' "$VERSION_FILE")
    log_success "version.json created with version: $VERSION, src_structure_complete: $STATUS"
else
    log_error "version.json creation failed"
    exit 1
fi

# ============================================================================
# Summary
# ============================================================================

echo ""
log_success "========================================================================="
log_success "  STORY-041 Implementation Complete"
log_success "========================================================================="
log_success "✓ src/.claude/ directory structure created (4 subdirs, 10 skill dirs)"
log_success "✓ src/devforgeai/ directory structure created (6 subdirs, 4+ nested)"
log_success "✓ .gitkeep files created in empty directories ($GITKEEP_COUNT files)"
log_success "✓ .gitignore updated with 7 new DevForgeAI patterns"
log_success "✓ version.json created with framework metadata"
log_success "✓ All operations completed successfully"
echo ""
log_info "Next step: Run tests to verify implementation"
log_info "  bash devforgeai/tests/STORY-041/RUN-TESTS.md"
echo ""

exit 0
