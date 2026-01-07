#!/bin/bash

##############################################################################
# Test Suite: STORY-240 - Release Skill Build Phase Integration
#
# Purpose: Validate that the devforgeai-release skill has been properly
# updated with Phase 0.1 (Tech Stack Detection) and Phase 0.2 (Build/Compile)
#
# TDD State: RED - All tests should FAIL initially because files don't exist
#
# Acceptance Criteria Tested:
#   AC#1: SKILL.md Phase Structure Updated
#   AC#2: Tech Stack Detection Reference Created
#   AC#3: Build Commands Reference Created
#   AC#4: Build Configuration Schema Created
#   AC#5: Workflow Integration Tested
#
# Technical Requirements:
#   NFR-001: SKILL.md < 1000 lines
#   NFR-002: Reference files < 500 lines each
#   NFR-003: Config file < 100 lines
##############################################################################

set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Directories
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../" && pwd)"

# Target files
SKILL_MD="$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md"
TECH_STACK_REF="$PROJECT_ROOT/.claude/skills/devforgeai-release/references/tech-stack-detection.md"
BUILD_COMMANDS_REF="$PROJECT_ROOT/.claude/skills/devforgeai-release/references/build-commands.md"
BUILD_CONFIG="$PROJECT_ROOT/devforgeai/deployment/build-config.yaml"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

##############################################################################
# Helper Functions
##############################################################################

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}  PASS${NC}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}  FAIL${NC}"
    fi
}

##############################################################################
# AC#1: SKILL.md Phase Structure Updated
##############################################################################

test_ac1_skill_md_exists() {
    # Arrange: Expected file location
    local expected_file="$SKILL_MD"

    # Act: Check if file exists
    if [ -f "$expected_file" ]; then
        echo "    SKILL.md exists at: $expected_file"
        return 0
    else
        echo "    ERROR: SKILL.md not found at: $expected_file"
        return 1
    fi
}

test_ac1_phase_01_exists() {
    # Arrange: Pattern to search for
    local pattern="Phase 0\.1.*Tech Stack Detection"

    # Act: Search for Phase 0.1 in SKILL.md
    if [ -f "$SKILL_MD" ]; then
        if grep -qiE "$pattern" "$SKILL_MD" 2>/dev/null; then
            echo "    Found: Phase 0.1: Tech Stack Detection"
            return 0
        else
            echo "    ERROR: Phase 0.1: Tech Stack Detection NOT found in SKILL.md"
            return 1
        fi
    else
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi
}

test_ac1_phase_02_exists() {
    # Arrange: Pattern to search for
    local pattern="Phase 0\.2.*Build"

    # Act: Search for Phase 0.2 in SKILL.md
    if [ -f "$SKILL_MD" ]; then
        if grep -qiE "$pattern" "$SKILL_MD" 2>/dev/null; then
            echo "    Found: Phase 0.2: Build/Compile"
            return 0
        else
            echo "    ERROR: Phase 0.2: Build/Compile NOT found in SKILL.md"
            return 1
        fi
    else
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi
}

test_ac1_phase_order_correct() {
    # Arrange: Phases must appear in order 0.1 before 0.2
    if [ ! -f "$SKILL_MD" ]; then
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi

    # Act: Get line numbers of Phase 0.1 and Phase 0.2
    local line_01=$(grep -niE "Phase 0\.1" "$SKILL_MD" 2>/dev/null | head -1 | cut -d: -f1)
    local line_02=$(grep -niE "Phase 0\.2" "$SKILL_MD" 2>/dev/null | head -1 | cut -d: -f1)

    # Assert: Phase 0.1 appears before Phase 0.2
    if [ -n "$line_01" ] && [ -n "$line_02" ] && [ "$line_01" -lt "$line_02" ]; then
        echo "    Phase 0.1 (line $line_01) appears before Phase 0.2 (line $line_02)"
        return 0
    else
        echo "    ERROR: Phase order incorrect or phases missing (0.1: line $line_01, 0.2: line $line_02)"
        return 1
    fi
}

test_ac1_phase_01_before_phase_1() {
    # Arrange: Phase 0.1/0.2 must appear before Phase 1 (Pre-Release)
    if [ ! -f "$SKILL_MD" ]; then
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi

    # Act: Get line numbers
    local line_01=$(grep -niE "Phase 0\.[12]" "$SKILL_MD" 2>/dev/null | head -1 | cut -d: -f1)
    local line_phase1=$(grep -niE "Phase 1[^0-9].*Pre-Release" "$SKILL_MD" 2>/dev/null | head -1 | cut -d: -f1)

    # Assert: Phase 0.x appears before Phase 1
    if [ -n "$line_01" ] && [ -n "$line_phase1" ] && [ "$line_01" -lt "$line_phase1" ]; then
        echo "    Build phases (line $line_01) appear before Pre-Release Phase 1 (line $line_phase1)"
        return 0
    else
        echo "    ERROR: Build phases must precede Phase 1: Pre-Release"
        return 1
    fi
}

##############################################################################
# AC#2: Tech Stack Detection Reference Created
##############################################################################

test_ac2_tech_stack_ref_exists() {
    # Arrange: Expected file location
    local expected_file="$TECH_STACK_REF"

    # Act: Check if file exists
    if [ -f "$expected_file" ]; then
        echo "    tech-stack-detection.md exists"
        return 0
    else
        echo "    ERROR: tech-stack-detection.md NOT found at:"
        echo "      $expected_file"
        return 1
    fi
}

test_ac2_detection_matrix_present() {
    # Arrange: Detection matrix must be documented
    if [ ! -f "$TECH_STACK_REF" ]; then
        echo "    ERROR: tech-stack-detection.md does not exist"
        return 1
    fi

    # Act: Search for detection matrix section
    if grep -qiE "(detection matrix|stack detection table|supported stacks)" "$TECH_STACK_REF" 2>/dev/null; then
        echo "    Found: Detection matrix documentation"
        return 0
    else
        echo "    ERROR: Detection matrix NOT documented in tech-stack-detection.md"
        return 1
    fi
}

test_ac2_techstackdetector_usage() {
    # Arrange: TechStackDetector usage examples must be present
    if [ ! -f "$TECH_STACK_REF" ]; then
        echo "    ERROR: tech-stack-detection.md does not exist"
        return 1
    fi

    # Act: Search for TechStackDetector references
    if grep -qE "(TechStackDetector|tech_stack_detector|detect_tech_stack)" "$TECH_STACK_REF" 2>/dev/null; then
        echo "    Found: TechStackDetector usage examples"
        return 0
    else
        echo "    ERROR: TechStackDetector usage NOT documented"
        return 1
    fi
}

test_ac2_tech_stack_ref_linked_in_skill() {
    # Arrange: SKILL.md must reference tech-stack-detection.md
    if [ ! -f "$SKILL_MD" ]; then
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi

    # Act: Search for reference link
    if grep -qE "tech-stack-detection\.md" "$SKILL_MD" 2>/dev/null; then
        echo "    Found: tech-stack-detection.md referenced in SKILL.md"
        return 0
    else
        echo "    ERROR: tech-stack-detection.md NOT referenced in SKILL.md"
        return 1
    fi
}

##############################################################################
# AC#3: Build Commands Reference Created
##############################################################################

test_ac3_build_commands_ref_exists() {
    # Arrange: Expected file location
    local expected_file="$BUILD_COMMANDS_REF"

    # Act: Check if file exists
    if [ -f "$expected_file" ]; then
        echo "    build-commands.md exists"
        return 0
    else
        echo "    ERROR: build-commands.md NOT found at:"
        echo "      $expected_file"
        return 1
    fi
}

test_ac3_build_command_templates() {
    # Arrange: Build command templates must be documented
    if [ ! -f "$BUILD_COMMANDS_REF" ]; then
        echo "    ERROR: build-commands.md does not exist"
        return 1
    fi

    # Act: Search for command templates (npm, dotnet, pip, etc.)
    local found=0
    for keyword in "npm" "dotnet" "pip" "cargo" "gradle" "maven" "build"; do
        if grep -qi "$keyword" "$BUILD_COMMANDS_REF" 2>/dev/null; then
            found=$((found + 1))
        fi
    done

    # Assert: At least 3 build systems documented
    if [ "$found" -ge 3 ]; then
        echo "    Found: $found build command templates"
        return 0
    else
        echo "    ERROR: Only $found build systems documented (expected >= 3)"
        return 1
    fi
}

test_ac3_buildexecutor_usage() {
    # Arrange: BuildExecutor usage examples must be present
    if [ ! -f "$BUILD_COMMANDS_REF" ]; then
        echo "    ERROR: build-commands.md does not exist"
        return 1
    fi

    # Act: Search for BuildExecutor references
    if grep -qE "(BuildExecutor|build_executor|execute_build)" "$BUILD_COMMANDS_REF" 2>/dev/null; then
        echo "    Found: BuildExecutor usage examples"
        return 0
    else
        echo "    ERROR: BuildExecutor usage NOT documented"
        return 1
    fi
}

test_ac3_build_commands_ref_linked_in_skill() {
    # Arrange: SKILL.md must reference build-commands.md
    if [ ! -f "$SKILL_MD" ]; then
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi

    # Act: Search for reference link
    if grep -qE "build-commands\.md" "$SKILL_MD" 2>/dev/null; then
        echo "    Found: build-commands.md referenced in SKILL.md"
        return 0
    else
        echo "    ERROR: build-commands.md NOT referenced in SKILL.md"
        return 1
    fi
}

##############################################################################
# AC#4: Build Configuration Schema Created
##############################################################################

test_ac4_build_config_exists() {
    # Arrange: Expected file location
    local expected_file="$BUILD_CONFIG"

    # Act: Check if file exists
    if [ -f "$expected_file" ]; then
        echo "    build-config.yaml exists"
        return 0
    else
        echo "    ERROR: build-config.yaml NOT found at:"
        echo "      $expected_file"
        return 1
    fi
}

test_ac4_build_enabled_key() {
    # Arrange: build.enabled key must exist with default true
    if [ ! -f "$BUILD_CONFIG" ]; then
        echo "    ERROR: build-config.yaml does not exist"
        return 1
    fi

    # Act: Search for build.enabled
    if grep -qE "(enabled|build\.enabled)" "$BUILD_CONFIG" 2>/dev/null; then
        echo "    Found: build.enabled configuration key"
        return 0
    else
        echo "    ERROR: build.enabled key NOT found"
        return 1
    fi
}

test_ac4_build_timeout_key() {
    # Arrange: build.timeout_ms key must exist
    if [ ! -f "$BUILD_CONFIG" ]; then
        echo "    ERROR: build-config.yaml does not exist"
        return 1
    fi

    # Act: Search for timeout configuration
    if grep -qE "(timeout_ms|timeout)" "$BUILD_CONFIG" 2>/dev/null; then
        echo "    Found: timeout configuration key"
        return 0
    else
        echo "    ERROR: timeout_ms key NOT found"
        return 1
    fi
}

test_ac4_cross_platform_targets_key() {
    # Arrange: build.cross_platform_targets key must exist
    if [ ! -f "$BUILD_CONFIG" ]; then
        echo "    ERROR: build-config.yaml does not exist"
        return 1
    fi

    # Act: Search for cross_platform_targets
    if grep -qE "(cross_platform_targets|targets)" "$BUILD_CONFIG" 2>/dev/null; then
        echo "    Found: cross_platform_targets configuration"
        return 0
    else
        echo "    ERROR: cross_platform_targets key NOT found"
        return 1
    fi
}

test_ac4_skip_stacks_key() {
    # Arrange: build.skip_stacks key must exist
    if [ ! -f "$BUILD_CONFIG" ]; then
        echo "    ERROR: build-config.yaml does not exist"
        return 1
    fi

    # Act: Search for skip_stacks
    if grep -qE "skip_stacks" "$BUILD_CONFIG" 2>/dev/null; then
        echo "    Found: skip_stacks configuration"
        return 0
    else
        echo "    ERROR: skip_stacks key NOT found"
        return 1
    fi
}

test_ac4_fail_on_build_error_key() {
    # Arrange: build.fail_on_build_error key must exist
    if [ ! -f "$BUILD_CONFIG" ]; then
        echo "    ERROR: build-config.yaml does not exist"
        return 1
    fi

    # Act: Search for fail_on_build_error
    if grep -qE "fail_on_build_error" "$BUILD_CONFIG" 2>/dev/null; then
        echo "    Found: fail_on_build_error configuration"
        return 0
    else
        echo "    ERROR: fail_on_build_error key NOT found"
        return 1
    fi
}

test_ac4_config_has_comments() {
    # Arrange: Config should have documentation comments
    if [ ! -f "$BUILD_CONFIG" ]; then
        echo "    ERROR: build-config.yaml does not exist"
        return 1
    fi

    # Act: Count comment lines
    local comment_count=$(grep -cE "^\s*#" "$BUILD_CONFIG" 2>/dev/null || echo "0")

    # Assert: At least 5 comment lines
    if [ "$comment_count" -ge 5 ]; then
        echo "    Found: $comment_count documentation comments"
        return 0
    else
        echo "    ERROR: Only $comment_count comments (expected >= 5)"
        return 1
    fi
}

test_ac4_config_valid_yaml() {
    # Arrange: Config must be valid YAML
    if [ ! -f "$BUILD_CONFIG" ]; then
        echo "    ERROR: build-config.yaml does not exist"
        return 1
    fi

    # Act: Validate YAML with Python
    if python3 -c "import yaml; yaml.safe_load(open('$BUILD_CONFIG'))" 2>/dev/null; then
        echo "    YAML syntax is valid"
        return 0
    else
        echo "    ERROR: Invalid YAML syntax in build-config.yaml"
        return 1
    fi
}

##############################################################################
# AC#5: Workflow Integration Tested
##############################################################################

test_ac5_phase_01_documented() {
    # Arrange: Phase 0.1 workflow must be documented
    if [ ! -f "$SKILL_MD" ]; then
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi

    # Act: Check for Phase 0.1 section content
    local section_content=$(sed -n '/Phase 0\.1/,/Phase 0\.2/p' "$SKILL_MD" 2>/dev/null | wc -l)

    # Assert: At least 5 lines of content
    if [ "$section_content" -ge 5 ]; then
        echo "    Phase 0.1 section has $section_content lines of documentation"
        return 0
    else
        echo "    ERROR: Phase 0.1 section too short ($section_content lines)"
        return 1
    fi
}

test_ac5_phase_02_documented() {
    # Arrange: Phase 0.2 workflow must be documented
    if [ ! -f "$SKILL_MD" ]; then
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi

    # Act: Check for Phase 0.2 section with build content
    if grep -qiE "Phase 0\.2" "$SKILL_MD" 2>/dev/null && \
       grep -qiE "(build|compile|npm|dotnet)" "$SKILL_MD" 2>/dev/null; then
        echo "    Phase 0.2 documented with build commands"
        return 0
    else
        echo "    ERROR: Phase 0.2 build workflow not properly documented"
        return 1
    fi
}

test_ac5_buildresult_passing() {
    # Arrange: BuildResult must be passed to Phase 1
    if [ ! -f "$SKILL_MD" ]; then
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi

    # Act: Search for BuildResult references
    if grep -qE "(BuildResult|build_result|build result)" "$SKILL_MD" 2>/dev/null; then
        echo "    Found: BuildResult passing documented"
        return 0
    else
        echo "    ERROR: BuildResult passing to Phase 1 NOT documented"
        return 1
    fi
}

test_ac5_config_loading_documented() {
    # Arrange: Config loading must be documented before Phase 0.1
    if [ ! -f "$SKILL_MD" ]; then
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi

    # Act: Search for config loading reference
    if grep -qE "(build-config\.yaml|load.*config|configuration)" "$SKILL_MD" 2>/dev/null; then
        echo "    Found: Configuration loading documented"
        return 0
    else
        echo "    ERROR: build-config.yaml loading NOT documented"
        return 1
    fi
}

##############################################################################
# NFR Tests: Non-Functional Requirements
##############################################################################

test_nfr001_skill_md_under_1000_lines() {
    # Arrange: SKILL.md must remain < 1000 lines
    if [ ! -f "$SKILL_MD" ]; then
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi

    # Act: Count lines
    local line_count=$(wc -l < "$SKILL_MD" 2>/dev/null || echo "0")

    # Assert: Under 1000 lines
    if [ "$line_count" -lt 1000 ]; then
        echo "    SKILL.md has $line_count lines (< 1000 limit)"
        return 0
    else
        echo "    ERROR: SKILL.md has $line_count lines (exceeds 1000 limit)"
        return 1
    fi
}

test_nfr002_tech_stack_ref_under_500_lines() {
    # Arrange: Reference file must be < 500 lines
    if [ ! -f "$TECH_STACK_REF" ]; then
        echo "    ERROR: tech-stack-detection.md does not exist"
        return 1
    fi

    # Act: Count lines
    local line_count=$(wc -l < "$TECH_STACK_REF" 2>/dev/null || echo "0")

    # Assert: Under 500 lines
    if [ "$line_count" -lt 500 ]; then
        echo "    tech-stack-detection.md has $line_count lines (< 500 limit)"
        return 0
    else
        echo "    ERROR: tech-stack-detection.md has $line_count lines (exceeds 500 limit)"
        return 1
    fi
}

test_nfr002_build_commands_ref_under_500_lines() {
    # Arrange: Reference file must be < 500 lines
    if [ ! -f "$BUILD_COMMANDS_REF" ]; then
        echo "    ERROR: build-commands.md does not exist"
        return 1
    fi

    # Act: Count lines
    local line_count=$(wc -l < "$BUILD_COMMANDS_REF" 2>/dev/null || echo "0")

    # Assert: Under 500 lines
    if [ "$line_count" -lt 500 ]; then
        echo "    build-commands.md has $line_count lines (< 500 limit)"
        return 0
    else
        echo "    ERROR: build-commands.md has $line_count lines (exceeds 500 limit)"
        return 1
    fi
}

test_nfr003_config_under_100_lines() {
    # Arrange: Config file must be < 100 lines
    if [ ! -f "$BUILD_CONFIG" ]; then
        echo "    ERROR: build-config.yaml does not exist"
        return 1
    fi

    # Act: Count lines
    local line_count=$(wc -l < "$BUILD_CONFIG" 2>/dev/null || echo "0")

    # Assert: Under 100 lines
    if [ "$line_count" -lt 100 ]; then
        echo "    build-config.yaml has $line_count lines (< 100 limit)"
        return 0
    else
        echo "    ERROR: build-config.yaml has $line_count lines (exceeds 100 limit)"
        return 1
    fi
}

##############################################################################
# Business Rule Tests
##############################################################################

test_br001_build_before_existing_phases() {
    # Arrange: Build phase must execute before existing release phases
    if [ ! -f "$SKILL_MD" ]; then
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi

    # Act: Verify phase ordering in SKILL.md
    local phase_01_line=$(grep -nE "Phase 0\.1" "$SKILL_MD" 2>/dev/null | head -1 | cut -d: -f1 || echo "999999")
    local phase_1_line=$(grep -nE "Phase 1[^0-9]" "$SKILL_MD" 2>/dev/null | head -1 | cut -d: -f1 || echo "0")

    if [ -n "$phase_01_line" ] && [ -n "$phase_1_line" ] && [ "$phase_01_line" -lt "$phase_1_line" ]; then
        echo "    BR-001: Build phases precede existing phases"
        return 0
    else
        echo "    ERROR: BR-001 violated: Build phases must precede existing phases"
        return 1
    fi
}

test_br002_build_disabled_documentation() {
    # Arrange: Build disable behavior must be documented
    if [ ! -f "$SKILL_MD" ]; then
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi

    # Act: Search for skip/disable documentation
    if grep -qiE "(skip|disable|enabled.*false)" "$SKILL_MD" 2>/dev/null; then
        echo "    BR-002: Build disable behavior documented"
        return 0
    else
        echo "    ERROR: BR-002 violated: Build disable behavior NOT documented"
        return 1
    fi
}

test_br003_buildresult_available() {
    # Arrange: BuildResult must be available to subsequent phases
    if [ ! -f "$SKILL_MD" ]; then
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi

    # Act: Search for result passing documentation
    if grep -qiE "(result|output|pass.*phase)" "$SKILL_MD" 2>/dev/null; then
        echo "    BR-003: Build results passed to subsequent phases"
        return 0
    else
        echo "    ERROR: BR-003 violated: Build result passing NOT documented"
        return 1
    fi
}

test_br004_reference_files_required() {
    # Arrange: SKILL.md must document that reference files are required
    if [ ! -f "$SKILL_MD" ]; then
        echo "    ERROR: SKILL.md does not exist"
        return 1
    fi

    # Act: Check for reference file mentions
    local ref_count=$(grep -cE "references/" "$SKILL_MD" 2>/dev/null || echo "0")

    if [ "$ref_count" -ge 2 ]; then
        echo "    BR-004: Reference files documented ($ref_count references)"
        return 0
    else
        echo "    ERROR: BR-004 violated: Reference files not properly documented"
        return 1
    fi
}

##############################################################################
# Main Test Execution
##############################################################################

main() {
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}  STORY-240: Release Skill Build Phase Integration${NC}"
    echo -e "${BLUE}  Test Suite (TDD RED State - Expect Failures)${NC}"
    echo -e "${BLUE}================================================================${NC}"
    echo ""
    echo "Start time: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Project root: $PROJECT_ROOT"
    echo ""

    # AC#1: SKILL.md Phase Structure Updated
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    echo -e "${YELLOW}AC#1: SKILL.md Phase Structure Updated${NC}"
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    run_test "AC1.1: SKILL.md exists" "test_ac1_skill_md_exists"
    run_test "AC1.2: Phase 0.1 exists (Tech Stack Detection)" "test_ac1_phase_01_exists"
    run_test "AC1.3: Phase 0.2 exists (Build/Compile)" "test_ac1_phase_02_exists"
    run_test "AC1.4: Phase order correct (0.1 before 0.2)" "test_ac1_phase_order_correct"
    run_test "AC1.5: Build phases before Phase 1" "test_ac1_phase_01_before_phase_1"

    # AC#2: Tech Stack Detection Reference Created
    echo ""
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    echo -e "${YELLOW}AC#2: Tech Stack Detection Reference Created${NC}"
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    run_test "AC2.1: tech-stack-detection.md exists" "test_ac2_tech_stack_ref_exists"
    run_test "AC2.2: Detection matrix documented" "test_ac2_detection_matrix_present"
    run_test "AC2.3: TechStackDetector usage examples" "test_ac2_techstackdetector_usage"
    run_test "AC2.4: Reference linked in SKILL.md" "test_ac2_tech_stack_ref_linked_in_skill"

    # AC#3: Build Commands Reference Created
    echo ""
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    echo -e "${YELLOW}AC#3: Build Commands Reference Created${NC}"
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    run_test "AC3.1: build-commands.md exists" "test_ac3_build_commands_ref_exists"
    run_test "AC3.2: Build command templates present" "test_ac3_build_command_templates"
    run_test "AC3.3: BuildExecutor usage examples" "test_ac3_buildexecutor_usage"
    run_test "AC3.4: Reference linked in SKILL.md" "test_ac3_build_commands_ref_linked_in_skill"

    # AC#4: Build Configuration Schema Created
    echo ""
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    echo -e "${YELLOW}AC#4: Build Configuration Schema Created${NC}"
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    run_test "AC4.1: build-config.yaml exists" "test_ac4_build_config_exists"
    run_test "AC4.2: build.enabled key present" "test_ac4_build_enabled_key"
    run_test "AC4.3: build.timeout_ms key present" "test_ac4_build_timeout_key"
    run_test "AC4.4: cross_platform_targets key present" "test_ac4_cross_platform_targets_key"
    run_test "AC4.5: skip_stacks key present" "test_ac4_skip_stacks_key"
    run_test "AC4.6: fail_on_build_error key present" "test_ac4_fail_on_build_error_key"
    run_test "AC4.7: Config has documentation comments" "test_ac4_config_has_comments"
    run_test "AC4.8: Config is valid YAML" "test_ac4_config_valid_yaml"

    # AC#5: Workflow Integration Tested
    echo ""
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    echo -e "${YELLOW}AC#5: Workflow Integration Tested${NC}"
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    run_test "AC5.1: Phase 0.1 workflow documented" "test_ac5_phase_01_documented"
    run_test "AC5.2: Phase 0.2 workflow documented" "test_ac5_phase_02_documented"
    run_test "AC5.3: BuildResult passing documented" "test_ac5_buildresult_passing"
    run_test "AC5.4: Config loading documented" "test_ac5_config_loading_documented"

    # NFR Tests
    echo ""
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    echo -e "${YELLOW}Non-Functional Requirements (NFR)${NC}"
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    run_test "NFR-001: SKILL.md < 1000 lines" "test_nfr001_skill_md_under_1000_lines"
    run_test "NFR-002a: tech-stack-detection.md < 500 lines" "test_nfr002_tech_stack_ref_under_500_lines"
    run_test "NFR-002b: build-commands.md < 500 lines" "test_nfr002_build_commands_ref_under_500_lines"
    run_test "NFR-003: build-config.yaml < 100 lines" "test_nfr003_config_under_100_lines"

    # Business Rules
    echo ""
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    echo -e "${YELLOW}Business Rules (BR)${NC}"
    echo -e "${YELLOW}--------------------------------------------------------------${NC}"
    run_test "BR-001: Build phases before existing phases" "test_br001_build_before_existing_phases"
    run_test "BR-002: Build disable behavior documented" "test_br002_build_disabled_documentation"
    run_test "BR-003: BuildResult available to phases" "test_br003_buildresult_available"
    run_test "BR-004: Reference files requirement documented" "test_br004_reference_files_required"

    # Summary
    echo ""
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}  TEST EXECUTION SUMMARY${NC}"
    echo -e "${BLUE}================================================================${NC}"
    echo ""
    echo -e "Tests run:    ${BLUE}$TESTS_RUN${NC}"
    echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
    echo ""

    local pass_rate=0
    if [ "$TESTS_RUN" -gt 0 ]; then
        pass_rate=$((TESTS_PASSED * 100 / TESTS_RUN))
    fi
    echo -e "Pass rate: ${pass_rate}%"
    echo ""

    if [ "$TESTS_FAILED" -eq 0 ]; then
        echo -e "${GREEN}================================================================${NC}"
        echo -e "${GREEN}  ALL TESTS PASSED - Story implementation complete!${NC}"
        echo -e "${GREEN}================================================================${NC}"
        exit 0
    else
        echo -e "${RED}================================================================${NC}"
        echo -e "${RED}  TESTS FAILED - TDD RED state (expected before implementation)${NC}"
        echo -e "${RED}================================================================${NC}"
        echo ""
        echo "Next steps:"
        echo "  1. Implement Phase 0.1 and Phase 0.2 in SKILL.md"
        echo "  2. Create tech-stack-detection.md reference"
        echo "  3. Create build-commands.md reference"
        echo "  4. Create build-config.yaml configuration"
        echo "  5. Re-run tests until all pass (TDD GREEN)"
        echo ""
        echo "End time: $(date '+%Y-%m-%d %H:%M:%S')"
        exit 1
    fi
}

# Run main
main "$@"
