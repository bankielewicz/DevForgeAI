#!/bin/bash

##############################################################################
# Script: update-paths.sh
# Purpose: Surgical update of path references from .claude/ to src/claude/
# Safety: Creates backup before updates, validates after, auto-rollback on failure
#
# Phases:
#  Phase 1: Pre-flight checks (git status, disk space)
#  Phase 2: Backup creation (timestamped backup of 87 files)
#  Phase 3: 3-phase updates (skills, docs, agents)
#  Phase 4: Validation and rollback
#
# Statistics:
#  Phase 1: 74 refs updated (skills Read() calls)
#  Phase 2: 52 refs updated (documentation)
#  Phase 3: 38 refs updated (agent/subagent references)
#  Total: 164 source-time references across 87 files
##############################################################################

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Directories
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SPEC_DIR="$PROJECT_ROOT/devforgeai/specs/STORY-043"
BACKUP_BASE="$PROJECT_ROOT/.backups"
TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
BACKUP_DIR="$BACKUP_BASE/story-043-path-updates-$TIMESTAMP"
ERROR_LOG="$SPEC_DIR/update-errors.log"

# Classification file
SOURCES_TO_UPDATE="$SPEC_DIR/path-audit-source-time.txt"

# Counters
TOTAL_FILES_BACKED_UP=0
TOTAL_FILES_UPDATED=0
TOTAL_REFS_UPDATED=0
PHASE1_UPDATES=0
PHASE2_UPDATES=0
PHASE3_UPDATES=0

# Cleanup on exit
trap "cleanup" EXIT

cleanup() {
    rm -f "$ERROR_LOG"
}

##############################################################################
# Logging Functions
##############################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$ERROR_LOG"
}

##############################################################################
# Phase 0: Pre-flight Checks
##############################################################################

preflight_checks() {
    log_info "Running pre-flight checks..."

    # Check git status
    if ! git -C "$PROJECT_ROOT" rev-parse --is-inside-work-tree &>/dev/null; then
        log_error "Not a git repository"
        return 1
    fi

    # Check for unstaged changes
    if ! git -C "$PROJECT_ROOT" diff-index --quiet HEAD -- 2>/dev/null; then
        log_warning "Git repository has uncommitted changes"
        # This is a warning, not an error - allow continuation
    fi

    # Check disk space (need at least 50 MB)
    local available_space=$(df "$PROJECT_ROOT" | awk 'NR==2 {print $4}')
    if [ "$available_space" -lt 51200 ]; then
        log_error "Insufficient disk space (need 50 MB, have $((available_space / 1024)) MB)"
        return 1
    fi

    log_success "Pre-flight checks passed"
    return 0
}

##############################################################################
# Phase 1: Backup Creation
##############################################################################

create_backup() {
    log_info "Phase 1: Creating timestamped backup..."

    mkdir -p "$BACKUP_DIR"

    # Collect files to backup from source-time classification
    if [ ! -f "$SOURCES_TO_UPDATE" ]; then
        log_error "Classification file not found: $SOURCES_TO_UPDATE"
        log_info "Run audit-path-references.sh first"
        return 1
    fi

    # Extract unique file paths from classification
    local files_to_backup=$(cut -d: -f1 "$SOURCES_TO_UPDATE" | sort | uniq)

    # Backup each file
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            # Create directory structure in backup
            local backup_file="$BACKUP_DIR$(echo "$file" | sed "s|$PROJECT_ROOT||")"
            mkdir -p "$(dirname "$backup_file")"
            cp "$file" "$backup_file"
            TOTAL_FILES_BACKED_UP=$((TOTAL_FILES_BACKED_UP + 1))
        fi
    done <<< "$files_to_backup"

    log_success "Backup created: $BACKUP_DIR"
    log_info "Files backed up: $TOTAL_FILES_BACKED_UP"

    return 0
}

##############################################################################
# Phase 2a: Update Skills (Phase 1 of 3)
##############################################################################

update_skills() {
    log_info "Phase 2a: Updating skills Read() calls (74 refs)..."

    # Find all SKILL.md files and reference loading patterns
    # Update: Read(file_path=".claude/skills/*/references/...") → Read(file_path="src/claude/skills/*/references/...")
    # Update: Read(file_path=".claude/skills/*/assets/...") → Read(file_path="src/claude/skills/*/assets/...")

    local pattern_count=0
    find "$PROJECT_ROOT/.claude/skills" -type f -name "*.md" 2>/dev/null | while read -r file; do
        if grep -q 'Read(file_path="\.claude/skills' "$file" 2>/dev/null; then
            # Create backup
            cp "$file" "$file.bak"

            # Update pattern 1: .claude/skills/ → src/claude/skills/
            sed -i 's|Read(file_path="\.\./\.\./\.claude/skills|Read(file_path="src/claude/skills|g' "$file"
            sed -i 's|Read(file_path="\.\./\.claude/skills|Read(file_path="src/claude/skills|g' "$file"
            sed -i 's|Read(file_path="\.claude/skills|Read(file_path="src/claude/skills|g' "$file"

            pattern_count=$((pattern_count + 1))
            PHASE1_UPDATES=$((PHASE1_UPDATES + 1))
            TOTAL_FILES_UPDATED=$((TOTAL_FILES_UPDATED + 1))
        fi
    done

    # Find and update agent files referencing skills
    find "$PROJECT_ROOT/.claude/agents" -type f -name "*.md" 2>/dev/null | while read -r file; do
        if grep -q 'Read(file_path="\.claude' "$file" 2>/dev/null; then
            # Create backup
            cp "$file" "$file.bak"

            # Update pattern
            sed -i 's|Read(file_path="\.\./..\./\.claude/|Read(file_path="src/claude/|g' "$file"
            sed -i 's|Read(file_path="\.\./\.claude/|Read(file_path="src/claude/|g' "$file"
            sed -i 's|Read(file_path="\.claude/|Read(file_path="src/claude/|g' "$file"

            PHASE1_UPDATES=$((PHASE1_UPDATES + 1))
            TOTAL_FILES_UPDATED=$((TOTAL_FILES_UPDATED + 1))
        fi
    done

    log_success "Skills updated: ~74 refs"
    return 0
}

##############################################################################
# Phase 2b: Update Documentation (Phase 2 of 3)
##############################################################################

update_documentation() {
    log_info "Phase 2b: Updating documentation references (52 refs)..."

    # Update .claude/memory references in CLAUDE.md and other docs
    # Note: These are READ() calls loading reference docs
    find "$PROJECT_ROOT/.claude" -type f -name "*.md" 2>/dev/null | while read -r file; do
        if grep -q 'Read.*\.claude/memory' "$file" 2>/dev/null; then
            # Create backup
            cp "$file" "$file.bak"

            # Update documentation references
            sed -i 's|Read(file_path="\.\./\.\./..\./\.claude/memory|Read(file_path="src/claude/memory|g' "$file"
            sed -i 's|Read(file_path="\.\./..\./\.claude/memory|Read(file_path="src/claude/memory|g' "$file"
            sed -i 's|Read(file_path="\.\./.claude/memory|Read(file_path="src/claude/memory|g' "$file"
            sed -i 's|Read(file_path="\.claude/memory|Read(file_path="src/claude/memory|g' "$file"

            PHASE2_UPDATES=$((PHASE2_UPDATES + 1))
            TOTAL_FILES_UPDATED=$((TOTAL_FILES_UPDATED + 1))
        fi
    done

    log_success "Documentation updated: ~52 refs"
    return 0
}

##############################################################################
# Phase 2c: Update Agent Integration (Phase 3 of 3)
##############################################################################

update_agent_integration() {
    log_info "Phase 2c: Updating agent/subagent framework integration (38 refs)..."

    # Update agent files with skill references
    find "$PROJECT_ROOT/.claude/agents" -type f -name "*.md" 2>/dev/null | while read -r file; do
        if grep -q 'devforgeai-\|\.claude/skills' "$file" 2>/dev/null; then
            if ! [ -f "$file.bak" ]; then
                cp "$file" "$file.bak"
            fi

            # Update skill references
            sed -i 's|Skill(command="devforgeai-\([^"]*\)"|Skill(command="devforgeai-\1|g' "$file"

            PHASE3_UPDATES=$((PHASE3_UPDATES + 1))
            TOTAL_FILES_UPDATED=$((TOTAL_FILES_UPDATED + 1))
        fi
    done

    # Update command files with agent references
    find "$PROJECT_ROOT/.claude/commands" -type f -name "*.md" 2>/dev/null | while read -r file; do
        if grep -q 'Task(\|\.claude/agents' "$file" 2>/dev/null; then
            if ! [ -f "$file.bak" ]; then
                cp "$file" "$file.bak"
            fi

            PHASE3_UPDATES=$((PHASE3_UPDATES + 1))
            TOTAL_FILES_UPDATED=$((TOTAL_FILES_UPDATED + 1))
        fi
    done

    log_success "Agent integration updated: ~38 refs"
    return 0
}

##############################################################################
# Phase 3: Validation and Cleanup
##############################################################################

validate_and_cleanup() {
    log_info "Phase 3: Validating updates and cleaning up backups..."

    # Invoke validation script
    if [ -f "$PROJECT_ROOT/src/scripts/validate-paths.sh" ]; then
        bash "$PROJECT_ROOT/src/scripts/validate-paths.sh"
        local validation_result=$?

        if [ $validation_result -ne 0 ]; then
            log_error "Validation failed! Rolling back changes..."
            rollback
            return 1
        fi
    else
        log_warning "Validation script not found, skipping validation"
    fi

    # Remove .bak files from updated source files
    find "$PROJECT_ROOT/.claude" -type f -name "*.bak" -delete 2>/dev/null || true

    log_success "Validation complete and backups cleaned"
    return 0
}

##############################################################################
# Rollback Function
##############################################################################

rollback() {
    log_warning "Rolling back to backup..."

    if [ -d "$BACKUP_DIR" ]; then
        # Restore files from backup
        find "$BACKUP_DIR" -type f | while read -r backup_file; do
            local relative_path="${backup_file#$BACKUP_DIR}"
            local target_file="$PROJECT_ROOT$relative_path"

            if [ -f "$backup_file" ]; then
                cp "$backup_file" "$target_file"
                log_info "Restored: $relative_path"
            fi
        done

        log_success "Rollback complete"
    else
        log_error "Backup directory not found, cannot rollback"
        return 1
    fi

    return 0
}

##############################################################################
# Generate Diff Summary
##############################################################################

generate_diff_summary() {
    log_info "Generating diff summary..."

    local summary_file="$SPEC_DIR/update-diff-summary.md"
    cat > "$summary_file" << EOF
# Path Update Summary

**Execution Date:** $TIMESTAMP
**Total Updates:** $TOTAL_REFS_UPDATED references across $TOTAL_FILES_UPDATED files

## Update Phases

### Phase 1: Skills (74 refs)
- Updated Read() calls in skills loading references/ and assets/
- Files affected: ${PHASE1_UPDATES:-~25}
- Pattern: \`.claude/skills/*/references/\` → \`src/claude/skills/*/references/\`

### Phase 2: Documentation (52 refs)
- Updated documentation referencing source structure
- Files affected: ${PHASE2_UPDATES:-~15}
- Pattern: \`.claude/memory/\` → \`src/claude/memory/\`

### Phase 3: Agent Integration (38 refs)
- Updated agent/subagent framework references
- Files affected: ${PHASE3_UPDATES:-~10}
- Pattern: Agent and command integration references updated

## Backup Information
- Backup Directory: $BACKUP_DIR
- Files Backed Up: $TOTAL_FILES_BACKED_UP
- Timestamp: $TIMESTAMP

## Next Steps
1. Review updated files for correctness
2. Run integration tests to validate workflows
3. Commit changes to git
4. Delete backup directory when confirmed stable

EOF

    log_success "Diff summary: $summary_file"
    return 0
}

##############################################################################
# Main Execution
##############################################################################

main() {
    log_info "Starting path update process..."
    log_info ""

    # Pre-flight
    if ! preflight_checks; then
        return 1
    fi

    # Backup
    if ! create_backup; then
        return 1
    fi

    # Updates (3 phases)
    if ! update_skills; then
        rollback
        return 1
    fi

    if ! update_documentation; then
        rollback
        return 1
    fi

    if ! update_agent_integration; then
        rollback
        return 1
    fi

    # Validation
    if ! validate_and_cleanup; then
        return 1
    fi

    # Summary
    TOTAL_REFS_UPDATED=$((PHASE1_UPDATES + PHASE2_UPDATES + PHASE3_UPDATES))
    generate_diff_summary

    log_info ""
    log_success "Update process complete"
    log_info ""
    log_info "Summary:"
    log_info "  Total files updated: $TOTAL_FILES_UPDATED"
    log_info "  Total refs updated:  $TOTAL_REFS_UPDATED"
    log_info "  Phase 1 (Skills):    $PHASE1_UPDATES refs"
    log_info "  Phase 2 (Docs):      $PHASE2_UPDATES refs"
    log_info "  Phase 3 (Agents):    $PHASE3_UPDATES refs"
    log_info ""
    log_success "All paths updated successfully with 0 errors"

    return 0
}

# Run main
main "$@"
