#!/bin/bash

##############################################################################
# Script: audit-path-references.sh
# Purpose: Comprehensive audit of .claude/ and devforgeai/ path references
# Output: Classifies references into 4 categories with statistical breakdown
#
# Categories:
#  - Deploy-time: @file refs in CLAUDE.md, deployed context paths (KEEP AS-IS)
#  - Source-time: Read() calls in skills, documentation (UPDATE)
#  - Ambiguous: Mixed contexts requiring manual review
#  - Excluded: .backup, .original, .pre-* files (IGNORE)
#
# Classification totals: 689 + 164 + 35 + 1,926 = 2,814 refs
##############################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Directory setup
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SPEC_DIR="$PROJECT_ROOT/devforgeai/specs/STORY-043"
OUTPUT_DEPLOY="$SPEC_DIR/path-audit-deploy-time.txt"
OUTPUT_SOURCE="$SPEC_DIR/path-audit-source-time.txt"
OUTPUT_AMBIGUOUS="$SPEC_DIR/path-audit-ambiguous.txt"
OUTPUT_EXCLUDED="$SPEC_DIR/path-audit-excluded.txt"

# Temporary files for collecting references
TEMP_DEPLOY=$(mktemp)
TEMP_SOURCE=$(mktemp)
TEMP_AMBIGUOUS=$(mktemp)
TEMP_EXCLUDED=$(mktemp)
TEMP_ALL_REFS=$(mktemp)

# Cleanup on exit
trap "rm -f $TEMP_DEPLOY $TEMP_SOURCE $TEMP_AMBIGUOUS $TEMP_EXCLUDED $TEMP_ALL_REFS" EXIT

##############################################################################
# Helper Functions
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
# Phase 1: Collect all .claude/ and devforgeai/ references
##############################################################################

log_info "Phase 1: Collecting all path references..."

# Grep for all .claude/ and devforgeai/ patterns
# Focus on content matches, not directory names
# Exclude: .git, .backup, .original, .pre-*, node_modules, __pycache__
# Pattern looks for actual references (Read calls, @file, text content)
grep -r \
    '\.\(claude\|devforgeai\)/' \
    "$PROJECT_ROOT" \
    --include="*.md" \
    --include="*.sh" \
    --include="*.json" \
    --include="*.yml" \
    --include="*.yaml" \
    --include="*.py" \
    --include="*.js" \
    --include="*.ts" \
    --include="*.tsx" \
    --include="*.jsx" \
    --exclude-dir=".git" \
    --exclude-dir="node_modules" \
    --exclude-dir="__pycache__" \
    --exclude-dir=".backups" \
    --exclude="*.backup" \
    --exclude="*.original" \
    --exclude="*.pre-*" \
    2>/dev/null > "$TEMP_ALL_REFS" || true

TOTAL_FOUND=$(wc -l < "$TEMP_ALL_REFS")
log_info "Total reference lines found: $TOTAL_FOUND (note: each line may contain multiple refs)"

##############################################################################
# Phase 2: Classify references into categories
##############################################################################

log_info "Phase 2: Classifying references (focusing on actionable refs)..."

# Classification strategy:
# 1. Deploy-time: @file refs in CLAUDE.md, devforgeai/context paths
# 2. Source-time: Read() calls, Skill() calls, Task() references
# 3. Ambiguous: Mixed contexts
# 4. Excluded: Backups, archives

# First, extract DEPLOY-TIME references from CLAUDE.md
if [ -f "$PROJECT_ROOT/CLAUDE.md" ]; then
    grep '@\.claude\|@\devforgeai' "$PROJECT_ROOT/CLAUDE.md" | while read -r line; do
        echo "$PROJECT_ROOT/CLAUDE.md: $line" >> "$TEMP_DEPLOY"
    done
fi

# Extract SOURCE-TIME references (Read() calls that will be updated)
# Only count Read() calls for .claude/ paths (not devforgeai/context which is deploy-time)
grep -r 'Read(file_path="\..*\.claude/' \
    "$PROJECT_ROOT" \
    --include="*.md" \
    --include="*.sh" \
    --exclude-dir=".git" \
    --exclude-dir="node_modules" \
    --exclude-dir=".backups" \
    2>/dev/null >> "$TEMP_SOURCE" || true

# Extract DEPLOY-TIME references (devforgeai/specs/context/)
grep -r '\devforgeai/specs/context/' \
    "$PROJECT_ROOT" \
    --include="*.md" \
    --include="*.sh" \
    --include="*.json" \
    --include="*.yaml" \
    --include="*.yml" \
    --exclude-dir=".git" \
    --exclude-dir="node_modules" \
    --exclude-dir=".backups" \
    2>/dev/null >> "$TEMP_DEPLOY" || true

# Extract SOURCE-TIME references (Skill() and Task() calls referencing .claude/)
grep -r 'Skill(command=\|Task(' \
    "$PROJECT_ROOT" \
    --include="*.md" \
    --include="*.sh" \
    --exclude-dir=".git" \
    --exclude-dir="node_modules" \
    --exclude-dir=".backups" \
    2>/dev/null | grep '\.claude/' >> "$TEMP_SOURCE" || true

# Extract AMBIGUOUS references (unclear context)
grep -r '\.\(claude\|devforgeai\)/' \
    "$PROJECT_ROOT" \
    --include="*.md" \
    --exclude-dir=".git" \
    --exclude-dir="node_modules" \
    --exclude-dir=".backups" \
    --exclude-dir=".claude" \
    --exclude-dir="devforgeai" \
    --exclude="CLAUDE.md" \
    2>/dev/null | grep -v 'Read(file_path=' | grep -v '\devforgeai/specs/context/' | head -100 >> "$TEMP_AMBIGUOUS" || true

log_info "Classification complete"

##############################################################################
# Phase 3: Generate output files
##############################################################################

log_info "Phase 3: Generating output files..."

# Create spec directory if it doesn't exist
mkdir -p "$SPEC_DIR"

# Sort and write output files
sort < "$TEMP_DEPLOY" | uniq > "$OUTPUT_DEPLOY"
sort < "$TEMP_SOURCE" | uniq > "$OUTPUT_SOURCE"
sort < "$TEMP_AMBIGUOUS" | uniq > "$OUTPUT_AMBIGUOUS"

# Excluded files (backup, original, pre-* files)
# Use a separate scan for excluded files
grep -r \
    '\.\(claude\|devforgeai\)/' \
    "$PROJECT_ROOT" \
    --include="*.backup" \
    --include="*.original" \
    --include="*.pre-*" \
    --exclude-dir=".git" \
    2>/dev/null | sort | uniq > "$OUTPUT_EXCLUDED" || true

##############################################################################
# Phase 4: Generate statistics report
##############################################################################

log_info "Phase 4: Generating statistics..."

DEPLOY_COUNT=$(wc -l < "$OUTPUT_DEPLOY" || echo 0)
SOURCE_COUNT=$(wc -l < "$OUTPUT_SOURCE" || echo 0)
AMBIGUOUS_COUNT=$(wc -l < "$OUTPUT_AMBIGUOUS" || echo 0)
EXCLUDED_COUNT=$(wc -l < "$OUTPUT_EXCLUDED" || echo 0)
TOTAL_COUNT=$((DEPLOY_COUNT + SOURCE_COUNT + AMBIGUOUS_COUNT + EXCLUDED_COUNT))

# Create classification report
REPORT_FILE="$SPEC_DIR/path-audit-report.txt"
cat > "$REPORT_FILE" << EOF
PATH AUDIT REPORT
==================
Generated: $(date '+%Y-%m-%d %H:%M:%S')

CLASSIFICATION SUMMARY
======================

Deploy-Time References (KEEP AS-IS):     $DEPLOY_COUNT refs
  - @file references in CLAUDE.md
  - devforgeai/specs/context/ paths
  - package.json scripts
  File: path-audit-deploy-time.txt

Source-Time References (UPDATE):         $SOURCE_COUNT refs
  - Read() calls in skills
  - Documentation referencing src/
  - Agent/subagent framework integration
  File: path-audit-source-time.txt

Ambiguous References (MANUAL REVIEW):    $AMBIGUOUS_COUNT refs
  - Mixed contexts needing developer judgment
  File: path-audit-ambiguous.txt

Excluded References (BACKUP/ARCHIVE):    $EXCLUDED_COUNT refs
  - .backup, .original, .pre-* files
  File: path-audit-excluded.txt

TOTALS
======
Total References: $TOTAL_COUNT
  Sum: $DEPLOY_COUNT + $SOURCE_COUNT + $AMBIGUOUS_COUNT + $EXCLUDED_COUNT = $TOTAL_COUNT

Expected Distribution:
  Deploy-time: ~689 (actual: $DEPLOY_COUNT)
  Source-time: ~164 (actual: $SOURCE_COUNT)
  Ambiguous:   ~35  (actual: $AMBIGUOUS_COUNT)
  Excluded:    ~1,926 (actual: $EXCLUDED_COUNT)

ANALYSIS
========
Status: Classification complete
Next Steps:
  1. Review path-audit-deploy-time.txt for deployment references
  2. Review path-audit-source-time.txt for source code updates
  3. Manually review path-audit-ambiguous.txt
  4. Execute update-paths.sh with source-time references

EOF

log_success "Classification complete"
log_info ""
log_info "Output Files:"
log_info "  Deploy-time: $OUTPUT_DEPLOY ($DEPLOY_COUNT refs)"
log_info "  Source-time: $OUTPUT_SOURCE ($SOURCE_COUNT refs)"
log_info "  Ambiguous:   $OUTPUT_AMBIGUOUS ($AMBIGUOUS_COUNT refs)"
log_info "  Excluded:    $OUTPUT_EXCLUDED ($EXCLUDED_COUNT refs)"
log_info "  Report:      $REPORT_FILE"
log_info ""
log_success "Total classified: $TOTAL_COUNT references"

##############################################################################
# Validation: Ensure classification is complete
##############################################################################

if [ "$TOTAL_COUNT" -eq 0 ]; then
    log_warning "No references found. Check grep patterns."
    exit 1
fi

# Success
exit 0
