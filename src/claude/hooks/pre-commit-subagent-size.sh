#!/bin/bash

################################################################################
# Pre-Commit Subagent Size Enforcement Hook
# STORY-335: Add Subagent Size Enforcement Mechanism
# ADR-012: Subagent Progressive Disclosure Architecture
#
# Purpose: Warn developers when subagent files exceed size thresholds to
#          prevent constitutional debt accumulation (81% violation rate
#          requiring EPIC-053 remediation).
#
# Usage:   Automatically invoked by git commit for staged subagent files
#          Can also be run manually: ./pre-commit-subagent-size.sh
#
# Exit Codes:
#   0 - Proceed (no violations OR warnings only)
#   1 - Halt (at least one file exceeds hard failure threshold)
#
# Thresholds (configurable via environment variables):
#   WARNING_THRESHOLD: 500 lines (soft limit - displays warning, proceeds)
#   FAIL_THRESHOLD:    600 lines (hard limit - blocks commit)
#
# Business Rules (ADR-012):
#   BR-001: Warning threshold (500) must be less than fail threshold (600)
#   BR-002: Only core .md files are checked, NOT files in references/
#   BR-003: Warnings exit 0, failures exit 1
#
# Reference: ADR-012 - Subagent Progressive Disclosure Architecture
# Created: 2026-01-31 (STORY-335)
################################################################################

set -o pipefail

# =============================================================================
# Configuration (environment variable overrides available per NFR-003)
# =============================================================================

WARNING_THRESHOLD="${SUBAGENT_WARNING_THRESHOLD:-500}"
FAIL_THRESHOLD="${SUBAGENT_FAIL_THRESHOLD:-600}"

# Directories to check (both operational and source)
# Both .claude/agents/ and src/claude/agents/ are checked for subagent files
AGENT_DIRS=(
    ".claude/agents/"
    "src/claude/agents/"
)

# =============================================================================
# Color codes for output
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# =============================================================================
# Threshold Validation (BR-001)
# =============================================================================

validate_thresholds() {
    # BR-001: Warning threshold must be less than fail threshold
    if [ "$WARNING_THRESHOLD" -ge "$FAIL_THRESHOLD" ]; then
        echo -e "${YELLOW}Warning: Invalid thresholds (WARNING_THRESHOLD >= FAIL_THRESHOLD)${NC}"
        echo "Using defaults: WARNING_THRESHOLD=500, FAIL_THRESHOLD=600"
        WARNING_THRESHOLD=500
        FAIL_THRESHOLD=600
    fi
}

# =============================================================================
# File Discovery
# =============================================================================

get_staged_agent_files() {
    # Get staged files that match agent directories
    # HOOK-001: Find all staged .md files in agents/ directories
    # HOOK-002: Exclude files in references/ subdirectories (BR-002)

    local staged_files=""

    # Get all staged .md files
    local all_staged=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null)

    if [ -z "$all_staged" ]; then
        return
    fi

    # Filter for agent files, excluding references/ using grep -v '/references/'
    # HOOK-002: BR-002 exclusion pattern - use grep -v for references/ filtering
    while IFS= read -r file; do
        # Check if file is in an agents directory
        for dir in "${AGENT_DIRS[@]}"; do
            if [[ "$file" == "$dir"*.md ]] || [[ "$file" == "$dir"*.md ]]; then
                staged_files+="$file"$'\n'
                break
            fi
        done
    done <<< "$all_staged"

    # Apply grep -v '/references/' exclusion pattern (BR-002)
    staged_files=$(echo -n "$staged_files" | grep -v '/references/' 2>/dev/null || true)

    # Remove trailing newline and echo
    echo -n "$staged_files" | head -c -1
}

# =============================================================================
# Size Checking
# =============================================================================

check_file_size() {
    local file="$1"

    if [ ! -f "$file" ]; then
        return 0
    fi

    # HOOK-003: Use wc -l for accurate line counting
    local line_count=$(wc -l < "$file" | tr -d ' ')

    echo "$line_count"
}

# =============================================================================
# Summary Table Builder (AC#5)
# =============================================================================

declare -a VIOLATION_FILES
declare -a VIOLATION_LINES
declare -a VIOLATION_THRESHOLDS
declare -a VIOLATION_STATUSES

add_violation() {
    local file="$1"
    local lines="$2"
    local threshold="$3"
    local status="$4"

    VIOLATION_FILES+=("$file")
    VIOLATION_LINES+=("$lines")
    VIOLATION_THRESHOLDS+=("$threshold")
    VIOLATION_STATUSES+=("$status")
}

build_summary_table() {
    local violation_count=${#VIOLATION_FILES[@]}

    if [ $violation_count -eq 0 ]; then
        return 0
    fi

    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  Subagent Size Violations${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # AC#5: Display summary table showing all violations
    printf "| %-45s | %-7s | %-10s | %-12s |\n" "File" "Lines" "Threshold" "Status"
    printf "|%s|%s|%s|%s|\n" "-----------------------------------------------" "---------" "------------" "--------------"

    for ((i=0; i<violation_count; i++)); do
        local file="${VIOLATION_FILES[$i]}"
        local lines="${VIOLATION_LINES[$i]}"
        local threshold="${VIOLATION_THRESHOLDS[$i]}"
        local status="${VIOLATION_STATUSES[$i]}"

        # Truncate filename if too long
        if [ ${#file} -gt 45 ]; then
            file="...${file: -42}"
        fi

        printf "| %-45s | %-7s | %-10s | %-12s |\n" "$file" "$lines" "$threshold" "$status"
    done

    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

display_recommendation() {
    echo -e "${BOLD}Recommendation:${NC}"
    echo "  Consider extracting content to a references/ subdirectory per ADR-012."
    echo "  Example: .claude/agents/my-agent/references/"
    echo ""
    echo "  See: devforgeai/specs/adrs/ADR-012-subagent-progressive-disclosure.md"
    echo ""
}

# =============================================================================
# Main Entry Point
# =============================================================================

main() {
    local has_failure=0
    local has_warning=0
    local files_checked=0

    # Validate thresholds
    validate_thresholds

    # Get staged agent files
    local staged_files=$(get_staged_agent_files)

    # Edge Case 1: No agent files modified
    if [ -z "$staged_files" ]; then
        exit 0
    fi

    # Reset violation arrays
    VIOLATION_FILES=()
    VIOLATION_LINES=()
    VIOLATION_THRESHOLDS=()
    VIOLATION_STATUSES=()

    # Check each file
    while IFS= read -r file; do
        if [ -z "$file" ]; then
            continue
        fi

        ((files_checked++))

        local line_count=$(check_file_size "$file")

        # Check against thresholds
        # BR-003: 600+ lines = failure (exit 1)
        if [ "$line_count" -ge "$FAIL_THRESHOLD" ]; then
            has_failure=1
            add_violation "$file" "$line_count" "$FAIL_THRESHOLD" "FAILED"

            # AC#2: Display error message for hard failure
            echo -e "${RED}FAILED: ${file} has ${line_count} lines (exceeds ${FAIL_THRESHOLD}-line maximum).${NC}"
            echo "Must refactor with progressive disclosure per ADR-012 before merge."
            echo ""

        # BR-003: 500-599 lines = warning (exit 0)
        elif [ "$line_count" -gt "$WARNING_THRESHOLD" ]; then
            has_warning=1
            add_violation "$file" "$line_count" "$WARNING_THRESHOLD" "WARNING"

            # AC#1: Display warning message for soft limit (500-line threshold)
            echo -e "${YELLOW}⚠️ WARNING: ${file} has ${line_count} lines (exceeds 500-line target).${NC}"
            echo "Consider extracting to references/ per ADR-012."
            echo ""
        fi

    done <<< "$staged_files"

    # Display summary table if there are violations
    if [ ${#VIOLATION_FILES[@]} -gt 0 ]; then
        build_summary_table
        display_recommendation
    fi

    # HOOK-004: Exit code determination
    # BR-003: Warnings do not block commits, failures block
    if [ $has_failure -eq 1 ]; then
        echo -e "${RED}Commit blocked: One or more subagent files exceed the ${FAIL_THRESHOLD}-line hard limit.${NC}"
        exit 1
    elif [ $has_warning -eq 1 ]; then
        echo -e "${YELLOW}Commit proceeding with warnings. Consider refactoring large subagents.${NC}"
        exit 0
    else
        # No violations
        exit 0
    fi
}

# Run main function
main "$@"
