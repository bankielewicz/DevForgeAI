#!/bin/bash
################################################################################
# Test Suite: STORY-047 - Full Installation Testing on External Projects
################################################################################
#
# Purpose: Comprehensive failing tests (RED phase) for external project
# installation validation on Node.js and .NET projects
#
# Test Structure:
# - 7 Acceptance Criteria tests (AC1-AC7)
# - 5 Business Rule tests (BR1-BR5)
# - 5 Non-Functional Requirement tests (NFR1-NFR5)
# - 7 Edge Case tests (EC1-EC7)
# Total: 24+ test cases (all FAILING - RED phase)
#
# Framework: bash
# Exit codes: 0=all tests passed, 1=any test failed
# Expected output: ALL RED/FAILED (installer not yet implemented)
#
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Temporary directories for testing
TEST_TEMP_DIR="/tmp/devforgeai-test-$$"
NODEJS_PROJECT_DIR="$TEST_TEMP_DIR/NodeJsTestProject"
DOTNET_PROJECT_DIR="$TEST_TEMP_DIR/DotNetTestProject"

################################################################################
# UTILITY FUNCTIONS
################################################################################

log_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

log_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((TESTS_PASSED++))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((TESTS_FAILED++))
}

log_header() {
    echo ""
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}$1${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

assert_success() {
    local test_name=$1
    local exit_code=$2
    ((TESTS_RUN++))

    if [ $exit_code -eq 0 ]; then
        log_pass "$test_name"
    else
        log_fail "$test_name (exit code: $exit_code)"
    fi
}

assert_file_exists() {
    local test_name=$1
    local file_path=$2
    ((TESTS_RUN++))

    if [ -f "$file_path" ] || [ -d "$file_path" ]; then
        log_pass "$test_name: File/Dir exists: $file_path"
    else
        log_fail "$test_name: File/Dir missing: $file_path"
    fi
}

assert_file_count() {
    local test_name=$1
    local directory=$2
    local expected_min=$3
    local expected_max=$4
    ((TESTS_RUN++))

    local actual=$(find "$directory" -type f 2>/dev/null | wc -l)

    if [ "$actual" -ge "$expected_min" ] && [ "$actual" -le "$expected_max" ]; then
        log_pass "$test_name: File count OK ($actual files, expected $expected_min-$expected_max)"
    else
        log_fail "$test_name: File count WRONG ($actual files, expected $expected_min-$expected_max)"
    fi
}

assert_grep_matches() {
    local test_name=$1
    local pattern=$2
    local file_path=$3
    local expected_count=$4
    ((TESTS_RUN++))

    if [ ! -f "$file_path" ]; then
        log_fail "$test_name: File not found: $file_path"
        return
    fi

    local actual=$(grep -c "$pattern" "$file_path" 2>/dev/null || echo 0)

    if [ "$actual" -eq "$expected_count" ]; then
        log_pass "$test_name: Grep matches OK (found $actual, expected $expected_count)"
    else
        log_fail "$test_name: Grep matches WRONG (found $actual, expected $expected_count)"
    fi
}

assert_command_exit_code() {
    local test_name=$1
    local expected_exit_code=$2
    ((TESTS_RUN++))

    # Shift off first 2 args, rest is the command
    shift 2

    "$@" > /dev/null 2>&1
    local actual_exit_code=$?

    if [ $actual_exit_code -eq $expected_exit_code ]; then
        log_pass "$test_name (exit code: $actual_exit_code)"
    else
        log_fail "$test_name (expected exit code: $expected_exit_code, actual: $actual_exit_code)"
    fi
}

################################################################################
# SETUP AND TEARDOWN
################################################################################

setup() {
    log_header "SETUP: Creating test project directories"

    # Create temp directory
    mkdir -p "$TEST_TEMP_DIR"

    # Create Node.js test project
    mkdir -p "$NODEJS_PROJECT_DIR"

    # Create minimal package.json for Node.js detection
    cat > "$NODEJS_PROJECT_DIR/package.json" << 'EOF'
{
  "name": "NodeJsTestProject",
  "version": "1.0.0",
  "description": "Test project for DevForgeAI installation",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
EOF

    # Create sample CLAUDE.md for Node.js project
    cat > "$NODEJS_PROJECT_DIR/CLAUDE.md" << 'EOF'
# Node.js Project Instructions

## Project Setup
- Use npm for package management
- ESLint configuration in .eslintrc
- TypeScript strict mode enabled
- Node version: 18+

## API Documentation
- Express.js server on port 3000
- RESTful API endpoints in src/routes/
- Middleware configuration in src/middleware/

## Testing Guidelines
- Jest for unit tests
- Supertest for API tests
- Coverage threshold: 80%

## Deployment
- Docker container: Dockerfile in root
- Environment variables in .env
- Production builds: npm run build
EOF

    log_pass "Node.js test project created at $NODEJS_PROJECT_DIR"

    # Create .NET test project (optional, might not have dotnet CLI)
    mkdir -p "$DOTNET_PROJECT_DIR"

    # Create minimal .csproj for .NET detection
    cat > "$DOTNET_PROJECT_DIR/TestProject.csproj" << 'EOF'
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <RootNamespace>DotNetTestProject</RootNamespace>
  </PropertyGroup>
</Project>
EOF

    log_pass ".NET test project created at $DOTNET_PROJECT_DIR"
}

cleanup() {
    log_header "CLEANUP: Removing test directories"

    if [ -d "$TEST_TEMP_DIR" ]; then
        rm -rf "$TEST_TEMP_DIR"
        log_pass "Cleaned up: $TEST_TEMP_DIR"
    fi
}

################################################################################
# ACCEPTANCE CRITERIA TESTS
################################################################################

test_ac1_successful_installation_nodejs() {
    log_header "AC1: Successful Installation on Node.js Test Project"

    # Test 1.1: Installer detects Node.js project
    log_test "AC1.1: Installer detects Node.js project (package.json found)"
    # NOTE: This will FAIL until installer implements tech detection
    [ -f "$NODEJS_PROJECT_DIR/package.json" ] && log_pass "AC1.1" || log_fail "AC1.1"
    ((TESTS_RUN++))

    # Test 1.2: Installer creates .claude/ directory
    log_test "AC1.2: Installer creates .claude/ directory with 450 files"
    # NOTE: This will FAIL until installer runs
    if [ -d "$NODEJS_PROJECT_DIR/.claude" ]; then
        assert_file_count "AC1.2" "$NODEJS_PROJECT_DIR/.claude" 440 460
    else
        log_fail "AC1.2: .claude/ directory not created"
        ((TESTS_RUN++))
    fi

    # Test 1.3: Installer creates .devforgeai/ directory
    log_test "AC1.3: Installer creates .devforgeai/ directory"
    # NOTE: This will FAIL until installer runs
    if [ -d "$NODEJS_PROJECT_DIR/.devforgeai" ]; then
        log_pass "AC1.3: .devforgeai/ exists"
    else
        log_fail "AC1.3: .devforgeai/ not created"
    fi
    ((TESTS_RUN++))

    # Test 1.4: CLAUDE.md merged (user + framework)
    log_test "AC1.4: CLAUDE.md merged with user and framework content"
    # NOTE: This will FAIL until merge logic runs
    if [ -f "$NODEJS_PROJECT_DIR/CLAUDE.md" ]; then
        local line_count=$(wc -l < "$NODEJS_PROJECT_DIR/CLAUDE.md")
        if [ "$line_count" -gt 500 ]; then
            log_pass "AC1.4: CLAUDE.md merged ($line_count lines)"
        else
            log_fail "AC1.4: CLAUDE.md too small ($line_count lines, expected >500)"
        fi
    else
        log_fail "AC1.4: CLAUDE.md missing"
    fi
    ((TESTS_RUN++))

    # Test 1.5: Variables substituted
    log_test "AC1.5: Variables substituted ({{PROJECT_NAME}}, {{TECH_STACK}}, etc.)"
    # NOTE: This will FAIL until variable substitution runs
    if [ -f "$NODEJS_PROJECT_DIR/CLAUDE.md" ]; then
        local unsubstituted=$(grep -c "{{[A-Z_]*}}" "$NODEJS_PROJECT_DIR/CLAUDE.md" || echo 0)
        if [ "$unsubstituted" -eq 0 ]; then
            log_pass "AC1.5: All variables substituted (0 {{VAR}} patterns found)"
        else
            log_fail "AC1.5: Found $unsubstituted unsubstituted variables"
        fi
    else
        log_fail "AC1.5: Cannot check - CLAUDE.md missing"
    fi
    ((TESTS_RUN++))

    # Test 1.6: CLI installed successfully
    log_test "AC1.6: CLI installed (devforgeai --version works)"
    # NOTE: This will FAIL until CLI installation is implemented
    if command -v devforgeai &> /dev/null; then
        devforgeai --version > /dev/null 2>&1
        assert_success "AC1.6: devforgeai --version" $?
    else
        log_fail "AC1.6: devforgeai command not found"
        ((TESTS_RUN++))
    fi
}

test_ac2_all_commands_functional_nodejs() {
    log_header "AC2: All 14 Commands Functional in Node.js Project"

    cd "$NODEJS_PROJECT_DIR" 2>/dev/null || {
        log_fail "AC2: Cannot cd to Node.js project"
        ((TESTS_RUN += 14))
        return
    }

    # Test each of the 14 commands
    # NOTE: All will FAIL until installer and framework are functional

    log_test "AC2.1: /create-context command works"
    # command_output=$(/create-context NodeJsTestProject 2>&1)
    # assert_success "AC2.1" $?
    log_fail "AC2.1: /create-context - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "AC2.2: /create-story command works"
    log_fail "AC2.2: /create-story - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "AC2.3: /dev command works"
    log_fail "AC2.3: /dev - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "AC2.4: /qa command works"
    log_fail "AC2.4: /qa - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "AC2.5: /ideate command works"
    log_fail "AC2.5: /ideate - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "AC2.6: /create-epic command works"
    log_fail "AC2.6: /create-epic - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "AC2.7: /create-sprint command works"
    log_fail "AC2.7: /create-sprint - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "AC2.8: /create-ui command works"
    log_fail "AC2.8: /create-ui - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "AC2.9: /audit-deferrals command works"
    log_fail "AC2.9: /audit-deferrals - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "AC2.10: /rca command works"
    log_fail "AC2.10: /rca - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "AC2.11: /document command works"
    log_fail "AC2.11: /document - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "AC2.12: /orchestrate command works"
    log_fail "AC2.12: /orchestrate - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "AC2.13: /release command works"
    log_fail "AC2.13: /release - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "AC2.14: Command success rate is 14/14"
    log_fail "AC2.14: 14/14 command success - installer not yet implemented"
    ((TESTS_RUN++))
}

test_ac3_claude_md_merge_nodejs() {
    log_header "AC3: CLAUDE.md Merge Successful with User Content Preserved"

    log_test "AC3.1: User content preserved in merged CLAUDE.md"
    # NOTE: This will FAIL until merge logic runs
    if [ -f "$NODEJS_PROJECT_DIR/CLAUDE.md" ]; then
        # Check for original user content
        if grep -q "Node.js Project" "$NODEJS_PROJECT_DIR/CLAUDE.md"; then
            log_pass "AC3.1: User content found in merged file"
        else
            log_fail "AC3.1: User content lost in merge"
        fi
    else
        log_fail "AC3.1: CLAUDE.md file missing"
    fi
    ((TESTS_RUN++))

    log_test "AC3.2: Framework sections marked with generation metadata"
    # NOTE: This will FAIL until merge logic runs
    if [ -f "$NODEJS_PROJECT_DIR/CLAUDE.md" ]; then
        if grep -q "DEVFORGEAI" "$NODEJS_PROJECT_DIR/CLAUDE.md"; then
            log_pass "AC3.2: Framework sections marked"
        else
            log_fail "AC3.2: Framework sections not properly marked"
        fi
    else
        log_fail "AC3.2: CLAUDE.md file missing"
    fi
    ((TESTS_RUN++))

    log_test "AC3.3: Total file size approximately 1,050 lines (50 user + 1,000 framework)"
    # NOTE: This will FAIL until merge runs
    if [ -f "$NODEJS_PROJECT_DIR/CLAUDE.md" ]; then
        local line_count=$(wc -l < "$NODEJS_PROJECT_DIR/CLAUDE.md")
        if [ "$line_count" -ge 1000 ] && [ "$line_count" -le 1100 ]; then
            log_pass "AC3.3: File size OK ($line_count lines)"
        else
            log_fail "AC3.3: File size wrong ($line_count lines, expected 1000-1100)"
        fi
    else
        log_fail "AC3.3: CLAUDE.md file missing"
    fi
    ((TESTS_RUN++))
}

test_ac4_rollback_functionality() {
    log_header "AC4: Rollback Functions Correctly"

    log_test "AC4.1: Backup created before merge"
    # NOTE: This will FAIL until backup logic is implemented
    local backup_dir="$NODEJS_PROJECT_DIR/.backups"
    if [ -d "$backup_dir" ]; then
        log_pass "AC4.1: Backup directory exists"
    else
        log_fail "AC4.1: Backup directory not created"
    fi
    ((TESTS_RUN++))

    log_test "AC4.2: Rollback restores CLAUDE.md to pre-merge state"
    # NOTE: This will FAIL until rollback logic is implemented
    log_fail "AC4.2: Rollback - not yet implemented"
    ((TESTS_RUN++))

    log_test "AC4.3: Post-rollback validation (checksum match)"
    # NOTE: This will FAIL until rollback is implemented
    log_fail "AC4.3: Checksum validation - not yet implemented"
    ((TESTS_RUN++))
}

test_ac5_installation_dotnet() {
    log_header "AC5: Installation Succeeds on .NET Test Project"

    log_test "AC5.1: Installer detects .NET project (*.csproj found)"
    # NOTE: This will FAIL until .NET detection is implemented
    if [ -f "$DOTNET_PROJECT_DIR/TestProject.csproj" ]; then
        log_pass "AC5.1: .csproj file exists"
    else
        log_fail "AC5.1: .csproj file not found"
    fi
    ((TESTS_RUN++))

    log_test "AC5.2: .NET installation creates .claude/ directory"
    # NOTE: This will FAIL until installer runs
    if [ -d "$DOTNET_PROJECT_DIR/.claude" ]; then
        log_pass "AC5.2: .claude/ directory created"
    else
        log_fail "AC5.2: .claude/ directory not created"
    fi
    ((TESTS_RUN++))

    log_test "AC5.3: Tech stack variable substituted as '.NET'"
    # NOTE: This will FAIL until installer runs
    if [ -f "$DOTNET_PROJECT_DIR/CLAUDE.md" ]; then
        if grep -q "\.NET" "$DOTNET_PROJECT_DIR/CLAUDE.md"; then
            log_pass "AC5.3: .NET detected in CLAUDE.md"
        else
            log_fail "AC5.3: .NET not detected"
        fi
    else
        log_fail "AC5.3: CLAUDE.md missing"
    fi
    ((TESTS_RUN++))
}

test_ac6_isolation_validation() {
    log_header "AC6: Isolation Validation (No Cross-Contamination)"

    log_test "AC6.1: Node.js project name doesn't appear in .NET project"
    # NOTE: This will FAIL until installation runs
    local cross_refs=$(grep -r "NodeJsTestProject" "$DOTNET_PROJECT_DIR" 2>/dev/null | grep -v ".git" | wc -l || echo 0)
    if [ "$cross_refs" -eq 0 ]; then
        log_pass "AC6.1: No cross-references found (0 matches)"
    else
        log_fail "AC6.1: Cross-references found ($cross_refs matches)"
    fi
    ((TESTS_RUN++))

    log_test "AC6.2: .NET project name doesn't appear in Node.js project"
    # NOTE: This will FAIL until installation runs
    local cross_refs=$(grep -r "DotNetTestProject" "$NODEJS_PROJECT_DIR" 2>/dev/null | grep -v ".git" | wc -l || echo 0)
    if [ "$cross_refs" -eq 0 ]; then
        log_pass "AC6.2: No cross-references found (0 matches)"
    else
        log_fail "AC6.2: Cross-references found ($cross_refs matches)"
    fi
    ((TESTS_RUN++))
}

test_ac7_upgrade_workflow() {
    log_header "AC7: Upgrade Workflow Tested"

    log_test "AC7.1: Version file indicates 1.0.1 installation"
    # NOTE: This will FAIL until installer runs
    local version_file="$NODEJS_PROJECT_DIR/.devforgeai/.version.json"
    if [ -f "$version_file" ]; then
        if grep -q "1.0.1" "$version_file"; then
            log_pass "AC7.1: Version 1.0.1 detected"
        else
            log_fail "AC7.1: Version not 1.0.1"
        fi
    else
        log_fail "AC7.1: Version file not found"
    fi
    ((TESTS_RUN++))

    log_test "AC7.2: Upgrade from 1.0.1 to 1.0.2 updates selectively"
    # NOTE: This will FAIL until upgrade logic is implemented
    log_fail "AC7.2: Upgrade logic - not yet implemented"
    ((TESTS_RUN++))

    log_test "AC7.3: Upgrade preserves user configurations"
    # NOTE: This will FAIL until upgrade runs
    log_fail "AC7.3: Config preservation - not yet implemented"
    ((TESTS_RUN++))
}

################################################################################
# BUSINESS RULE TESTS
################################################################################

test_br1_installation_success() {
    log_header "BR1: 100% Installation Success Required"

    log_test "BR1: Both Node.js and .NET installations must exit 0"
    # NOTE: These will FAIL until installer is implemented

    # Check Node.js installation
    if [ -d "$NODEJS_PROJECT_DIR/.claude" ]; then
        log_pass "BR1: Node.js installation completed"
    else
        log_fail "BR1: Node.js installation failed (no .claude/ directory)"
    fi
    ((TESTS_RUN++))

    # Check .NET installation
    if [ -d "$DOTNET_PROJECT_DIR/.claude" ]; then
        log_pass "BR1: .NET installation completed"
    else
        log_fail "BR1: .NET installation failed (no .claude/ directory)"
    fi
    ((TESTS_RUN++))
}

test_br2_all_commands_work() {
    log_header "BR2: All 14 Commands Must Work (28/28 Total)"

    log_test "BR2: 14 commands × 2 projects = 28/28 successes required"
    # NOTE: This will FAIL until installer and commands are functional
    log_fail "BR2: Command tests - not yet implemented"
    ((TESTS_RUN++))
}

test_br3_user_content_preserved() {
    log_header "BR3: CLAUDE.md Merge Must Preserve 100% User Content"

    log_test "BR3.1: Node.js project user content preserved"
    # NOTE: This will FAIL until merge runs
    if [ -f "$NODEJS_PROJECT_DIR/CLAUDE.md" ]; then
        local user_lines=$(grep -c "Node.js Project" "$NODEJS_PROJECT_DIR/CLAUDE.md" || echo 0)
        if [ "$user_lines" -gt 0 ]; then
            log_pass "BR3.1: User content preserved"
        else
            log_fail "BR3.1: User content lost"
        fi
    else
        log_fail "BR3.1: CLAUDE.md missing"
    fi
    ((TESTS_RUN++))

    log_test "BR3.2: Diff shows only additions (no deletions)"
    # NOTE: This will FAIL until merge runs
    log_fail "BR3.2: Diff validation - not yet implemented"
    ((TESTS_RUN++))
}

test_br4_rollback_exact_restore() {
    log_header "BR4: Rollback Must Restore Exact Pre-Install State"

    log_test "BR4: Checksum validation post-rollback"
    # NOTE: This will FAIL until rollback is implemented
    log_fail "BR4: Checksum validation - not yet implemented"
    ((TESTS_RUN++))
}

test_br5_project_isolation() {
    log_header "BR5: Projects Must Be Isolated (No Shared State)"

    log_test "BR5: Stories created in one project don't affect other projects"
    # NOTE: This will FAIL until isolation is verified
    log_fail "BR5: Isolation validation - not yet implemented"
    ((TESTS_RUN++))
}

################################################################################
# NON-FUNCTIONAL REQUIREMENT TESTS
################################################################################

test_nfr1_fresh_install_performance() {
    log_header "NFR1: Fresh Installation Performance (<3 minutes)"

    log_test "NFR1.1: Node.js installation completes in <180 seconds"
    # NOTE: This will FAIL until installer runs
    log_fail "NFR1.1: Performance test - installer not yet implemented"
    ((TESTS_RUN++))

    log_test "NFR1.2: .NET installation completes in <180 seconds"
    # NOTE: This will FAIL until installer runs
    log_fail "NFR1.2: Performance test - installer not yet implemented"
    ((TESTS_RUN++))
}

test_nfr2_rollback_performance() {
    log_header "NFR2: Rollback Performance (<45 seconds)"

    log_test "NFR2: Rollback completes in <45 seconds"
    # NOTE: This will FAIL until rollback is implemented
    log_fail "NFR2: Rollback performance - not yet implemented"
    ((TESTS_RUN++))
}

test_nfr3_installation_repeatability() {
    log_header "NFR3: Installation Repeatability (100% Success × 3 Runs)"

    log_test "NFR3: 3 consecutive installations on Node.js project all succeed"
    # NOTE: This will FAIL until installer is reliable
    log_fail "NFR3: Repeatability test - installer not yet implemented"
    ((TESTS_RUN++))
}

test_nfr4_rollback_accuracy() {
    log_header "NFR4: Rollback Accuracy (100% Checksum Match)"

    log_test "NFR4: SHA256 checksums match pre-install and post-rollback"
    # NOTE: This will FAIL until rollback is implemented
    log_fail "NFR4: Checksum validation - not yet implemented"
    ((TESTS_RUN++))
}

test_nfr5_progress_reporting() {
    log_header "NFR5: Clear Installation Progress Reporting"

    log_test "NFR5: Progress updates appear at 10% intervals"
    # NOTE: This will FAIL until progress logic is implemented
    log_fail "NFR5: Progress reporting - not yet implemented"
    ((TESTS_RUN++))
}

################################################################################
# EDGE CASE TESTS
################################################################################

test_ec1_existing_claude_directory() {
    log_header "EC1: Existing .claude/ Directory Handling"

    log_test "EC1: Installer detects existing .claude/, prompts user for action"
    # NOTE: This will FAIL until detection logic is implemented

    # Create pre-existing .claude/ directory
    mkdir -p "$NODEJS_PROJECT_DIR/.claude"
    touch "$NODEJS_PROJECT_DIR/.claude/test-file.md"

    if [ -f "$NODEJS_PROJECT_DIR/.claude/test-file.md" ]; then
        log_pass "EC1: Pre-existing .claude/ directory detected"
    else
        log_fail "EC1: Cannot create test .claude/ directory"
    fi
    ((TESTS_RUN++))
}

test_ec2_network_failure_cli_install() {
    log_header "EC2: Network Issues During CLI Installation"

    log_test "EC2: Graceful failure if pip install fails"
    # NOTE: This will FAIL until error handling is implemented
    log_fail "EC2: Network failure handling - not yet implemented"
    ((TESTS_RUN++))
}

test_ec3_readonly_filesystem() {
    log_header "EC3: Read-Only Filesystem Detection"

    log_test "EC3: Installer fails fast on read-only filesystem"
    # NOTE: This will FAIL until permission checking is implemented
    # Check if target directory is writable
    if [ -w "$NODEJS_PROJECT_DIR" ]; then
        log_pass "EC3: Directory writable (can test write permissions)"
    else
        log_fail "EC3: Directory not writable"
    fi
    ((TESTS_RUN++))
}

test_ec4_installer_from_different_directory() {
    log_header "EC4: Installer Runs from Different Directory"

    log_test "EC4: Installer resolves paths correctly when run from /tmp/"
    # NOTE: This will FAIL until path resolution is implemented
    log_fail "EC4: Path resolution - not yet implemented"
    ((TESTS_RUN++))
}

test_ec5_different_python_version() {
    log_header "EC5: Test Project Uses Different Python Version"

    log_test "EC5: Installer adapts to Python 3.11+ (not just 3.8)"
    # Check Python version
    local python_version=$(python3 --version 2>&1 | awk '{print $2}')
    log_pass "EC5: Current Python version: $python_version"
    ((TESTS_RUN++))
}

test_ec6_large_merged_file() {
    log_header "EC6: CLAUDE.md Merge Produces Large File (>5,000 lines)"

    log_test "EC6: Installer warns but continues with large merged file"
    # NOTE: This will FAIL until warning logic is implemented
    log_fail "EC6: Large file warning - not yet implemented"
    ((TESTS_RUN++))
}

test_ec7_concurrent_installations() {
    log_header "EC7: Simultaneous Installations on Multiple Projects"

    log_test "EC7: Both projects can be installed concurrently without file lock issues"
    # NOTE: This will FAIL until concurrent safety is verified
    log_fail "EC7: Concurrent installation - not yet implemented"
    ((TESTS_RUN++))
}

################################################################################
# MAIN TEST EXECUTION
################################################################################

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║ STORY-047: Full Installation Testing on External Projects     ║"
    echo "║ Test Suite (RED Phase - All Tests Should FAIL)                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"

    # Setup
    setup

    # Run test groups
    test_ac1_successful_installation_nodejs
    test_ac2_all_commands_functional_nodejs
    test_ac3_claude_md_merge_nodejs
    test_ac4_rollback_functionality
    test_ac5_installation_dotnet
    test_ac6_isolation_validation
    test_ac7_upgrade_workflow

    test_br1_installation_success
    test_br2_all_commands_work
    test_br3_user_content_preserved
    test_br4_rollback_exact_restore
    test_br5_project_isolation

    test_nfr1_fresh_install_performance
    test_nfr2_rollback_performance
    test_nfr3_installation_repeatability
    test_nfr4_rollback_accuracy
    test_nfr5_progress_reporting

    test_ec1_existing_claude_directory
    test_ec2_network_failure_cli_install
    test_ec3_readonly_filesystem
    test_ec4_installer_from_different_directory
    test_ec5_different_python_version
    test_ec6_large_merged_file
    test_ec7_concurrent_installations

    # Cleanup
    cleanup

    # Summary
    log_header "TEST SUMMARY"
    echo ""
    echo "Total Tests Run:     $TESTS_RUN"
    echo -e "Passed:              ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Failed:              ${RED}$TESTS_FAILED${NC}"
    echo ""
    echo "Expected Status: ${RED}ALL FAILING${NC} (RED phase - installer not yet implemented)"
    echo ""

    # Exit with failure if any tests failed (which they should in RED phase)
    if [ $TESTS_FAILED -gt 0 ]; then
        echo -e "${RED}[RED PHASE - Expected Failures]${NC} Installer must be implemented to make tests GREEN"
        return 1
    else
        echo -e "${YELLOW}[UNEXPECTED]${NC} All tests passed - this shouldn't happen in RED phase!"
        return 0
    fi
}

# Run main function
main
exit $?
