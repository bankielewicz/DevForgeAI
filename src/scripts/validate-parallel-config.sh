#!/bin/bash
################################################################################
# STORY-108: Parallel Configuration Validation Script
#
# Validates devforgeai/config/parallel-orchestration.yaml against schema
# Exit codes: 0=valid, 1=invalid, 2=error
#
# Usage:
#   bash scripts/validate-parallel-config.sh [config-file]
#
# Default config: devforgeai/config/parallel-orchestration.yaml
################################################################################

set -u

# Config file path (default or user-provided)
CONFIG_FILE="${1:-devforgeai/config/parallel-orchestration.yaml}"
EXIT_CODE=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

################################################################################
# SVC-001: Validate Config File Exists and Has Valid YAML Structure
################################################################################

if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}ERROR: Config file not found: $CONFIG_FILE${NC}"
    echo "Expected location: devforgeai/config/parallel-orchestration.yaml"
    exit 2
fi

echo "Validating config: $CONFIG_FILE"

# Check required top-level fields
if ! grep -q "^version:" "$CONFIG_FILE"; then
    echo -e "${RED}ERROR: Missing required field: version${NC}"
    EXIT_CODE=1
fi

if ! grep -q "^default_profile:" "$CONFIG_FILE"; then
    echo -e "${RED}ERROR: Missing required field: default_profile${NC}"
    EXIT_CODE=1
fi

if ! grep -q "^profiles:" "$CONFIG_FILE"; then
    echo -e "${RED}ERROR: Missing required field: profiles${NC}"
    EXIT_CODE=1
fi

################################################################################
# SVC-002: Validate Required Keys Present Using Grep Patterns
################################################################################

# Extract all profile names (indented with 2 spaces, followed by colon)
PROFILES=$(grep -E "^  [a-z_]+:" "$CONFIG_FILE" | sed 's/://g' | awk '{print $1}' || true)

if [ -z "$PROFILES" ]; then
    echo -e "${RED}ERROR: No profiles defined in config${NC}"
    EXIT_CODE=1
else
    echo "Found profiles: $PROFILES"
fi

# Validate each profile has required fields
for profile in $PROFILES; do
    # Check max_concurrent_tasks field exists
    if ! grep -A 10 "^  $profile:" "$CONFIG_FILE" | grep -q "max_concurrent_tasks:"; then
        echo -e "${RED}ERROR: Profile '$profile' missing field: max_concurrent_tasks${NC}"
        EXIT_CODE=1
    fi

    # Check timeout_ms field exists
    if ! grep -A 10 "^  $profile:" "$CONFIG_FILE" | grep -q "timeout_ms:"; then
        echo -e "${RED}ERROR: Profile '$profile' missing field: timeout_ms${NC}"
        EXIT_CODE=1
    fi
done

################################################################################
# SVC-003: Validate Value Ranges Using Bash Arithmetic
################################################################################

# BR-001: Validate max_concurrent_tasks range (1-10)
for profile in $PROFILES; do
    MAX_TASKS=$(grep -A 10 "^  $profile:" "$CONFIG_FILE" | grep "max_concurrent_tasks:" | head -1 | awk '{print $2}' | sed 's/#.*//' | tr -d ' \r')

    if [ -n "$MAX_TASKS" ]; then
        if [ "$MAX_TASKS" -lt 1 ] 2>/dev/null || [ "$MAX_TASKS" -gt 10 ] 2>/dev/null; then
            echo -e "${RED}ERROR: Profile '$profile' has max_concurrent_tasks=$MAX_TASKS${NC}"
            echo -e "${RED}       Valid range: 1-10${NC}"
            echo -e "${RED}       Rationale: Maps to Anthropic subscription tier rate limits${NC}"
            EXIT_CODE=1
        fi
    fi
done

# BR-002: Validate timeout_ms range (1000-600000)
for profile in $PROFILES; do
    TIMEOUT=$(grep -A 10 "^  $profile:" "$CONFIG_FILE" | grep "timeout_ms:" | head -1 | awk '{print $2}' | sed 's/#.*//' | tr -d ' \r')

    if [ -n "$TIMEOUT" ]; then
        if [ "$TIMEOUT" -lt 1000 ] 2>/dev/null || [ "$TIMEOUT" -gt 600000 ] 2>/dev/null; then
            echo -e "${RED}ERROR: Profile '$profile' has timeout_ms=$TIMEOUT${NC}"
            echo -e "${RED}       Valid range: 1000-600000 (1 second to 10 minutes)${NC}"
            echo -e "${RED}       Rationale: Prevents indefinite hangs while allowing long operations${NC}"
            EXIT_CODE=1
        fi
    fi
done

################################################################################
# BR-003: Profile Preset Locking Check
################################################################################

# Check if user attempted to override preset profiles (pro/max/api)
# This is a WARNING, not a blocking error
for preset in pro max api; do
    if grep -q "^  $preset:" "$CONFIG_FILE"; then
        # Extract values for this preset
        TASKS=$(grep -A 10 "^  $preset:" "$CONFIG_FILE" | grep "max_concurrent_tasks:" | head -1 | awk '{print $2}' | sed 's/#.*//' | tr -d ' \r')
        TIMEOUT=$(grep -A 10 "^  $preset:" "$CONFIG_FILE" | grep "timeout_ms:" | head -1 | awk '{print $2}' | sed 's/#.*//' | tr -d ' \r')

        # Expected values for each preset
        case $preset in
            pro)
                EXPECTED_TASKS=4
                EXPECTED_TIMEOUT=120000
                ;;
            max)
                EXPECTED_TASKS=6
                EXPECTED_TIMEOUT=180000
                ;;
            api)
                EXPECTED_TASKS=8
                EXPECTED_TIMEOUT=300000
                ;;
        esac

        # Warn if values don't match expected presets
        if [ "$TASKS" != "$EXPECTED_TASKS" ] || [ "$TIMEOUT" != "$EXPECTED_TIMEOUT" ]; then
            echo -e "${YELLOW}WARNING: Preset profile '$preset' has non-standard values${NC}"
            echo -e "${YELLOW}         Expected: max_concurrent_tasks=$EXPECTED_TASKS, timeout_ms=$EXPECTED_TIMEOUT${NC}"
            echo -e "${YELLOW}         Actual:   max_concurrent_tasks=$TASKS, timeout_ms=$TIMEOUT${NC}"
            echo -e "${YELLOW}         Recommendation: Use 'custom' profile for non-standard configurations${NC}"
        fi
    fi
done

################################################################################
# Summary and Exit
################################################################################

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ Config validation passed${NC}"
    echo "Profiles validated: $PROFILES"
else
    echo -e "${RED}✗ Config validation failed${NC}"
    echo "Please fix errors and re-run validation"
fi

exit $EXIT_CODE
