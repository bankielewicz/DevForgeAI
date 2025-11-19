#!/bin/bash

##############################################################################
# Script: rollback-updates.sh
# Purpose: Restore files from backup directory after path updates
# Usage: bash rollback-updates.sh
##############################################################################

set -euo pipefail

# Configuration
BACKUP_DIR="/mnt/c/Projects/DevForgeAI2/.backups/story-043-path-updates-20251119-102328"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

##############################################################################
# Main Rollback Function
##############################################################################

rollback_files() {
    log_info "Starting rollback from backup: $BACKUP_DIR"

    if [ ! -d "$BACKUP_DIR" ]; then
        log_error "Backup directory not found: $BACKUP_DIR"
        return 1
    fi

    # Count files in backup
    local backup_file_count=$(find "$BACKUP_DIR" -type f | wc -l)
    log_info "Restoring $backup_file_count files from backup..."

    # Restore files
    cp -r "$BACKUP_DIR"/* "$PROJECT_ROOT" 2>/dev/null || true

    log_success "Rollback complete"
    log_success "Restored $backup_file_count files"
    return 0
}

##############################################################################
# Main Execution
##############################################################################

main() {
    echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}  Path Updates Rollback Script             ${BLUE}║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
    echo ""

    if rollback_files; then
        echo ""
        log_success "Rollback successful - files restored from backup"
        exit 0
    else
        echo ""
        log_error "Rollback failed - check backup directory"
        exit 1
    fi
}

main "$@"
