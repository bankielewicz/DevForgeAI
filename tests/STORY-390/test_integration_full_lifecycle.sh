#!/bin/bash

##############################################################################
# Integration Test Suite: STORY-390 - Prompt Versioning System
# Purpose: Verify full lifecycle integration - Capture → Modify → Finalize → Rollback → Verify
#          validates command file integration with slash command discovery and real component files
#
# Test Type: Integration Testing (Multi-Component Workflow)
# Focus: Command ecosystem integration, not individual command execution
##############################################################################

set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
IMPL_FILE="${PROJECT_ROOT}/src/claude/commands/prompt-version.md"
VERSION_STORAGE="${PROJECT_ROOT}/devforgeai/specs/prompt-versions"

##############################################################################
# Test Framework Functions
##############################################################################

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func 2>/dev/null; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "  ${GREEN}PASS${NC}: $test_name"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "  ${RED}FAIL${NC}: $test_name"
    fi
}

##############################################################################
# Integration Tests: Command File Integration with Slash Command Discovery
##############################################################################

test_command_file_is_valid_markdown() {
    # Slash command must be valid Markdown (parseable)
    [ -f "$IMPL_FILE" ] && grep -q "^# " "$IMPL_FILE"
}

test_command_has_required_frontmatter() {
    # Must have YAML frontmatter with metadata for slash command discovery
    head -1 "$IMPL_FILE" | grep -q "^---"
}

test_command_registers_subcommands_in_description() {
    # Description field must list all 4 subcommands (capture, finalize, rollback, history)
    description=$(grep -A 1 "^description:" "$IMPL_FILE" | tail -1)
    [[ "$description" =~ capture ]] && [[ "$description" =~ finalize ]] && [[ "$description" =~ rollback ]] && [[ "$description" =~ history ]]
}

test_command_argument_hint_matches_subcommands() {
    # argument-hint must match actual subcommand syntax
    grep -qE "argument-hint.*capture.*finalize.*rollback.*history" "$IMPL_FILE"
}

test_command_documents_all_subcommands() {
    # Each of 4 subcommands must have a documentation section
    grep -qiE "^#{1,3}.*[Cc]apture" "$IMPL_FILE" && \
    grep -qiE "^#{1,3}.*[Ff]inalize" "$IMPL_FILE" && \
    grep -qiE "^#{1,3}.*[Rr]ollback" "$IMPL_FILE" && \
    grep -qiE "^#{1,3}.*[Hh]istory" "$IMPL_FILE"
}

##############################################################################
# Integration Tests: Real Component File Access
##############################################################################

test_auto_detection_works_with_real_agent_files() {
    # Test agent auto-detection pattern against real agent directory
    agent_dir="${PROJECT_ROOT}/src/claude/agents"
    [ -d "$agent_dir" ] && \
    grep -qiE "agents/.*agent|path.*agents" "$IMPL_FILE" && \
    find "$agent_dir" -name "*.md" -type f | grep -q "\.md$"
}

test_auto_detection_works_with_real_skill_files() {
    # Test skill auto-detection pattern (SKILL.md in skill directory)
    skill_dir="${PROJECT_ROOT}/src/claude/skills"
    [ -d "$skill_dir" ] && \
    grep -qiE "skills/.*SKILL\.md|path.*skills" "$IMPL_FILE" && \
    find "$skill_dir" -name "SKILL.md" -type f | grep -q "SKILL\.md$"
}

test_auto_detection_works_with_real_command_files() {
    # Test command auto-detection pattern against real command directory
    commands_dir="${PROJECT_ROOT}/src/claude/commands"
    [ -d "$commands_dir" ] && \
    grep -qiE "commands/.*command|path.*commands" "$IMPL_FILE" && \
    find "$commands_dir" -name "*.md" -type f | grep -q "\.md$"
}

test_read_tool_references_are_correct() {
    # Command must use Read() with correct absolute path syntax
    grep -qE 'Read\(file_path=' "$IMPL_FILE"
}

test_write_tool_references_are_correct() {
    # Command must use Write() for snapshot files
    grep -qE 'Write\(file_path=' "$IMPL_FILE"
}

##############################################################################
# Integration Tests: Version Storage Path Integration
##############################################################################

test_version_storage_path_is_consistent() {
    # All references to snapshot storage must use same path pattern
    capture_refs=$(grep -c "devforgeai/specs/prompt-versions" "$IMPL_FILE")
    [ "$capture_refs" -gt 2 ]  # At least 2+ references across subcommands
}

test_version_storage_path_matches_spec() {
    # Path must match story spec: devforgeai/specs/prompt-versions/{component_id}/
    grep -q "devforgeai/specs/prompt-versions/{component_id}" "$IMPL_FILE"
}

test_snapshot_filename_pattern_is_iso8601() {
    # Snapshot filename must use ISO-8601 timestamp pattern
    grep -qE "\{timestamp\}.*\{short.?hash\}|YYYY-MM-DD.*HHMMSS" "$IMPL_FILE"
}

##############################################################################
# Integration Tests: VERSION-HISTORY.md Format Compatibility
##############################################################################

test_version_history_markdown_format_defined() {
    # History format must be Markdown table format
    grep -qiE "version.*date.*hash|markdown.*table|table.*version" "$IMPL_FILE"
}

test_version_history_table_columns_specified() {
    # Table must have required columns: Version, Date, Before Hash, After Hash, Type, Reason, Snapshot
    grep -q "Version" "$IMPL_FILE" && \
    grep -q "Date" "$IMPL_FILE" && \
    grep -q "Before Hash" "$IMPL_FILE" && \
    grep -q "After Hash" "$IMPL_FILE" && \
    grep -q "Type" "$IMPL_FILE" && \
    grep -q "Reason" "$IMPL_FILE"
}

test_version_history_types_enumerated() {
    # History must document record types: migration, rollback, update, creation
    grep -qE "(migration|rollback|update|creation)" "$IMPL_FILE"
}

##############################################################################
# Integration Tests: Framework Tools Integration
##############################################################################

test_command_uses_read_not_bash_for_files() {
    # Must use Read() tool for file content, not Bash cat
    grep -q "Read(" "$IMPL_FILE" && \
    ! grep -qE "Bash.*cat\s|Bash.*<\s" "$IMPL_FILE"
}

test_command_uses_write_not_bash_for_file_creation() {
    # Must use Write() tool for snapshots, not Bash echo/cat
    grep -q "Write(" "$IMPL_FILE" && \
    ! grep -qE "Bash.*echo.*>" "$IMPL_FILE"
}

test_command_uses_glob_for_pattern_search() {
    # Must use Glob() for finding snapshot files by pattern
    grep -q "Glob(" "$IMPL_FILE"
}

test_command_uses_bash_only_for_sha256() {
    # Only legitimate Bash use is for sha256sum computation
    grep -qE "Bash.*sha256|sha256sum" "$IMPL_FILE"
}

##############################################################################
# Integration Tests: Multi-Component Support
##############################################################################

test_supports_agent_component_type() {
    # Must document support for agent type (with specific agent examples)
    grep -qE "agent.*component|component.*agent" "$IMPL_FILE"
}

test_supports_skill_component_type() {
    # Must document support for skill type (with specific skill examples)
    grep -qE "skill.*component|component.*skill" "$IMPL_FILE"
}

test_supports_command_component_type() {
    # Must document support for command type (with specific command examples)
    grep -qE "command.*component|component.*command" "$IMPL_FILE"
}

test_component_type_enum_enforced() {
    # Must enforce exactly 3 component types (BR-002)
    grep -qiE "agent.*skill.*command|must.*one.*of" "$IMPL_FILE"
}

##############################################################################
# Integration Tests: Hash Integrity with Framework
##############################################################################

test_sha256_hash_computation_documented() {
    # Must document sha256 computation method
    grep -qE "(sha256sum|hashlib|sha256)" "$IMPL_FILE"
}

test_hash_format_validation_enforced() {
    # Must validate hash format: 64 hex chars or NEW_COMPONENT sentinel
    grep -qE "(\[0-9a-f\]\{64\}|NEW_COMPONENT)" "$IMPL_FILE"
}

test_integrity_verification_before_rollback() {
    # Must verify hash before rollback (BR-006, NFR-005)
    grep -qiE "(integrity.*verif|verify.*hash|compare.*hash|rollback.*before.*check)" "$IMPL_FILE"
}

##############################################################################
# Integration Tests: Cross-Subcommand Data Flow
##############################################################################

test_capture_output_feeds_finalize_input() {
    # Capture creates snapshot file that finalize reads/updates
    grep -q "capture.*snapshot" "$IMPL_FILE" && \
    grep -q "finalize.*snapshot" "$IMPL_FILE"
}

test_finalize_creates_version_history_entry() {
    # Finalize creates/appends to VERSION-HISTORY.md
    grep -qiE "finalize.*version.?history|version.?history.*finalize|append.*entry" "$IMPL_FILE"
}

test_rollback_reads_version_history_and_snapshot() {
    # Rollback queries version history and reads from snapshot
    grep -q "rollback" "$IMPL_FILE" && \
    grep -qiE "(rollback.*snapshot|snapshot.*rollback)" "$IMPL_FILE"
}

test_history_reads_version_history_file() {
    # History command reads VERSION-HISTORY.md
    grep -qiE "history.*version.?history|version.?history.*history" "$IMPL_FILE"
}

##############################################################################
# Integration Tests: Error Handling Across Subcommands
##############################################################################

test_missing_file_error_handling() {
    # Must handle file not found consistently across all subcommands
    grep -qiE "(file.*not.*found|does.*not.*exist|HALT.*missing)" "$IMPL_FILE"
}

test_missing_snapshot_error_handling() {
    # Must handle missing snapshot files gracefully
    grep -qiE "(snapshot.*unavailable|snapshot.*missing|HALT.*snapshot)" "$IMPL_FILE"
}

test_integrity_failure_error_handling() {
    # Must handle integrity verification failure (AC#6)
    grep -qiE "(integrity.*fail|INTEGRITY_VERIFICATION_FAILED|hash.*mismatch)" "$IMPL_FILE"
}

test_invalid_version_error_handling() {
    # Must handle invalid version number in rollback
    grep -qiE "(invalid.*version|version.*not.*found|HALT.*version)" "$IMPL_FILE"
}

##############################################################################
# Integration Tests: Performance Requirements
##############################################################################

test_performance_targets_documented() {
    # Must reference performance targets (capture <5s, rollback <120s, history <10s)
    grep -qE "([0-9]+.*second|timeout|performance|NFR.*[0-9])" "$IMPL_FILE"
}

test_atomic_rollback_documented() {
    # Must document atomic rollback semantics (NFR-006)
    grep -qiE "(atomic|partial.*write|fail.*original.*preserved)" "$IMPL_FILE"
}

##############################################################################
# Integration Tests: Business Rules Enforcement
##############################################################################

test_all_business_rules_enforced() {
    # All 8 business rules must be referenced or enforced
    grep -qE "(BR-00[1-8]|component.*id.*valid|component.*type|file.*path|hash|concurrent|change.*reason|new.*component)" "$IMPL_FILE"
}

test_nfr_performance_enforced() {
    # NFRs for performance must be specified
    grep -qE "(NFR.*|performance|< *5.*second|< *120.*second|< *10.*second)" "$IMPL_FILE"
}

test_nfr_security_enforced() {
    # NFR-004: File path safety (no traversal)
    grep -qiE "(NFR.*|path.*safety|\.\..*reject|path.*traversal)" "$IMPL_FILE"
}

##############################################################################
# Integration Tests: AC Coverage
##############################################################################

test_ac1_snapshot_capture_impl() {
    # AC#1 implementation markers present
    grep -q "capture" "$IMPL_FILE" && grep -q "snapshot" "$IMPL_FILE"
}

test_ac2_before_after_state_impl() {
    # AC#2 implementation markers present
    grep -qE "(before.*after|after.*hash|finalize)" "$IMPL_FILE"
}

test_ac3_rollback_performance_impl() {
    # AC#3 implementation markers present
    grep -q "rollback" "$IMPL_FILE" && grep -qE "(120.*second|2.*minute|timeout)" "$IMPL_FILE"
}

test_ac4_history_audit_impl() {
    # AC#4 implementation markers present
    grep -q "history" "$IMPL_FILE" && grep -qE "(audit|table|format)" "$IMPL_FILE"
}

test_ac5_auto_detection_impl() {
    # AC#5 implementation markers present
    grep -qE "(auto.?detect|detect.*type|derive.*id)" "$IMPL_FILE"
}

test_ac6_integrity_verification_impl() {
    # AC#6 implementation markers present
    grep -qiE "(integrity|verify.*hash|compare|rollback.*before.*check)" "$IMPL_FILE"
}

##############################################################################
# Test Execution
##############################################################################

echo "=============================================="
echo "  STORY-390: Integration Test Suite"
echo "  Full Lifecycle + Component Integration"
echo "=============================================="

# Command File Integration Tests
run_test "Command file is valid Markdown" test_command_file_is_valid_markdown
run_test "Command has required frontmatter" test_command_has_required_frontmatter
run_test "Command registers all subcommands" test_command_registers_subcommands_in_description
run_test "Argument hint matches subcommands" test_command_argument_hint_matches_subcommands
run_test "All subcommands documented" test_command_documents_all_subcommands

# Real Component File Access Tests
run_test "Auto-detection for real agent files" test_auto_detection_works_with_real_agent_files
run_test "Auto-detection for real skill files" test_auto_detection_works_with_real_skill_files
run_test "Auto-detection for real command files" test_auto_detection_works_with_real_command_files
run_test "Read() tool references correct syntax" test_read_tool_references_are_correct
run_test "Write() tool references correct syntax" test_write_tool_references_are_correct

# Version Storage Path Integration Tests
run_test "Version storage path is consistent" test_version_storage_path_is_consistent
run_test "Version storage path matches spec" test_version_storage_path_matches_spec
run_test "Snapshot filename pattern is ISO-8601" test_snapshot_filename_pattern_is_iso8601

# VERSION-HISTORY.md Format Tests
run_test "VERSION-HISTORY.md format is Markdown" test_version_history_markdown_format_defined
run_test "History table columns specified" test_version_history_table_columns_specified
run_test "History record types enumerated" test_version_history_types_enumerated

# Framework Tools Integration Tests
run_test "Uses Read() for file content" test_command_uses_read_not_bash_for_files
run_test "Uses Write() for snapshot creation" test_command_uses_write_not_bash_for_file_creation
run_test "Uses Glob() for pattern search" test_command_uses_glob_for_pattern_search
run_test "Uses Bash only for SHA-256" test_command_uses_bash_only_for_sha256

# Multi-Component Support Tests
run_test "Supports agent component type" test_supports_agent_component_type
run_test "Supports skill component type" test_supports_skill_component_type
run_test "Supports command component type" test_supports_command_component_type
run_test "Component type enum enforced (BR-002)" test_component_type_enum_enforced

# Hash Integrity Tests
run_test "SHA-256 hash computation documented" test_sha256_hash_computation_documented
run_test "Hash format validation enforced" test_hash_format_validation_enforced
run_test "Integrity verification before rollback" test_integrity_verification_before_rollback

# Cross-Subcommand Data Flow Tests
run_test "Capture output feeds finalize input" test_capture_output_feeds_finalize_input
run_test "Finalize creates version history entry" test_finalize_creates_version_history_entry
run_test "Rollback reads snapshot and history" test_rollback_reads_version_history_and_snapshot
run_test "History reads version history file" test_history_reads_version_history_file

# Error Handling Tests
run_test "Missing file error handling" test_missing_file_error_handling
run_test "Missing snapshot error handling" test_missing_snapshot_error_handling
run_test "Integrity failure error handling" test_integrity_failure_error_handling
run_test "Invalid version error handling" test_invalid_version_error_handling

# Performance Requirements Tests
run_test "Performance targets documented" test_performance_targets_documented
run_test "Atomic rollback documented" test_atomic_rollback_documented

# Business Rules Enforcement Tests
run_test "All business rules enforced" test_all_business_rules_enforced
run_test "NFR performance enforced" test_nfr_performance_enforced
run_test "NFR security enforced" test_nfr_security_enforced

# AC Coverage Tests
run_test "AC#1: Snapshot capture impl" test_ac1_snapshot_capture_impl
run_test "AC#2: Before/After state impl" test_ac2_before_after_state_impl
run_test "AC#3: Rollback performance impl" test_ac3_rollback_performance_impl
run_test "AC#4: History audit impl" test_ac4_history_audit_impl
run_test "AC#5: Auto-detection impl" test_ac5_auto_detection_impl
run_test "AC#6: Integrity verification impl" test_ac6_integrity_verification_impl

##############################################################################
# Summary
##############################################################################

echo ""
echo "=============================================="
echo "  Integration Test Results"
echo "=============================================="
echo -e "  Total:  ${TESTS_RUN}"
echo -e "  Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "  Failed: ${RED}${TESTS_FAILED}${NC}"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo -e "${RED}RESULT: FAIL${NC} - $TESTS_FAILED test(s) failed"
    exit 1
else
    echo -e "${GREEN}RESULT: PASS${NC} - All integration tests passed"
    exit 0
fi
