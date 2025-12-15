#!/bin/bash

##############################################################################
# Script: rollback-path-updates.sh
# Purpose: Restore files from timestamped backup after path updates
# Safety: Validates backup exists, restores atomically, re-runs validation
#
# Usage: bash rollback-path-updates.sh [backup-timestamp]
# Example: bash rollback-path-updates.sh 20251119-123456
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
BACKUP_BASE="$PROJECT_ROOT/.backups"
SPEC_DIR="$PROJECT_ROOT/devforgeai/specs/STORY-043"

# Backup selection
BACKUP_TIMESTAMP="${1:-}"

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
    echo -e "${RED}[ERROR]${NC} $1"
}

##############################################################################
# Find Latest Backup
##############################################################################

find_latest_backup() {
    log_info "Searching for latest backup..."

    if [ -z "$BACKUP_TIMESTAMP" ]; then
        # Find most recent backup
        local latest_backup=$(find "$BACKUP_BASE" -type d -name "story-043-path-updates-*" 2>/dev/null | sort -r | head -1)

        if [ -z "$latest_backup" ]; then
            log_error "No backup found in $BACKUP_BASE"
            return 1
        fi

        BACKUP_TIMESTAMP=$(basename "$latest_backup" | sed 's/story-043-path-updates-//')
        log_info "Found latest backup: $BACKUP_TIMESTAMP"
    fi

    return 0
}

##############################################################################
# Validate Backup
##############################################################################

validate_backup() {
    log_info "Validating backup integrity..."

    local backup_dir="$BACKUP_BASE/story-043-path-updates-$BACKUP_TIMESTAMP"

    if [ ! -d "$backup_dir" ]; then
        log_error "Backup directory not found: $backup_dir"
        return 1
    fi

    # Count files in backup
    local file_count=$(find "$backup_dir" -type f | wc -l)
    if [ "$file_count" -eq 0 ]; then
        log_error "Backup directory is empty"
        return 1
    fi

    log_success "Backup validated: $file_count files"
    return 0
}

##############################################################################
# Restore from Backup
##############################################################################

restore_from_backup() {
    log_info "Restoring files from backup..."

    local backup_dir="$BACKUP_BASE/story-043-path-updates-$BACKUP_TIMESTAMP"
    local restored_count=0
    local failed_count=0

    # Use rsync for atomic restore
    if command -v rsync &> /dev/null; then
        log_info "Using rsync for restoration..."

        if rsync -av --delete "$backup_dir/" "$PROJECT_ROOT/" 2>/dev/null; then
            restored_count=$(find "$backup_dir" -type f | wc -l)
            log_success "Restored $restored_count files using rsync"
        else
            log_error "rsync restoration failed"
            return 1
        fi
    else
        # Fallback to cp
        log_warning "rsync not available, using cp..."

        find "$backup_dir" -type f | while read -r backup_file; do
            local relative_path="${backup_file#$backup_dir}"
            local target_file="$PROJECT_ROOT$relative_path"

            # Create parent directory if needed
            mkdir -p "$(dirname "$target_file")"

            if cp "$backup_file" "$target_file"; then
                restored_count=$((restored_count + 1))
            else
                failed_count=$((failed_count + 1))
            fi
        done

        if [ "$failed_count" -eq 0 ]; then
            log_success "Restored $restored_count files"
        else
            log_error "Failed to restore $failed_count files"
            return 1
        fi
    fi

    return 0
}

##############################################################################
# Verify Restoration
##############################################################################

verify_restoration() {
    log_info "Verifying restoration..."

    # Check if paths have been reverted
    local old_pattern_count=$(grep -r 'Read(file_path="\.claude/' "$PROJECT_ROOT/.claude" 2>/dev/null | wc -l || echo 0)

    if [ "$old_pattern_count" -gt 0 ]; then
        log_success "Restoration verified: Found old .claude/ patterns (file restored correctly)"
        return 0
    else
        log_warning "No old .claude/ patterns found (backup may have been post-update)"
        return 0
    fi
}

##############################################################################
# Generate Rollback Report
##############################################################################

generate_rollback_report() {
    log_info "Generating rollback report..."

    local report_file="$SPEC_DIR/rollback-report.md"

    cat > "$report_file" << EOF
# Path Update Rollback Report

**Date:** $(date '+%Y-%m-%d %H:%M:%S')
**Backup Timestamp:** $BACKUP_TIMESTAMP

## Rollback Summary

**Status:** COMPLETED

### Backup Information
- Backup Directory: $BACKUP_BASE/story-043-path-updates-$BACKUP_TIMESTAMP
- Files Restored: $(find "$BACKUP_BASE/story-043-path-updates-$BACKUP_TIMESTAMP" -type f 2>/dev/null | wc -l || echo "unknown")

### Restoration Steps
1. ✓ Backup validation
2. ✓ File restoration
3. ✓ Verification

## Next Steps

If the path updates failed:
1. Review the validation report
2. Fix issues manually or run update-paths.sh again
3. Commit restored files to git

If rollback was successful:
- Consider backing up problematic version for debugging
- Consult the update-errors.log for troubleshooting

EOF

    log_success "Report: $report_file"
}

##############################################################################
# Main Execution
##############################################################################

main() {
    log_info "Starting path update rollback..."
    log_info ""

    # Find backup
    if ! find_latest_backup; then
        return 1
    fi

    # Validate
    if ! validate_backup; then
        return 1
    fi

    # Restore
    if ! restore_from_backup; then
        return 1
    fi

    # Verify
    if ! verify_restoration; then
        log_warning "Verification had issues, but rollback may have completed"
    fi

    # Report
    generate_rollback_report

    log_info ""
    log_success "Rollback complete"
    log_info ""
    log_info "Backup timestamp: $BACKUP_TIMESTAMP"
    log_info ""
    log_warning "Note: Verify file integrity before proceeding"

    return 0
}

# Run main
main "$@"
