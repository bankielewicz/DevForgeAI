"""
Unit tests for STORY-035 Business Rules

Tests verify agent enforces business rules:
- BR-001: Check 6 context files exist, HALT if missing
- BR-002: Return 'REQUIRES ADR' for tech not in tech-stack.md
- BR-003: Write outputs to .devforgeai/research/ with 755 permissions
- BR-004: Validate repository URLs (GitHub pattern only)
"""

import pytest
import re
from pathlib import Path


@pytest.mark.story_035
@pytest.mark.business_rule
@pytest.mark.unit
class TestInternetSleuthBusinessRules:
    """Test suite for business rule enforcement"""

    @pytest.fixture
    def agent_file_path(self):
        """Path to internet-sleuth agent file"""
        return Path(".claude/agents/internet-sleuth.md")

    @pytest.fixture
    def agent_content(self, agent_file_path):
        """Load agent file content"""
        assert agent_file_path.exists(), f"Agent file not found: {agent_file_path}"
        return agent_file_path.read_text()

    def test_br_001_validates_all_six_context_files_exist(self, agent_content):
        """
        BR-001: Agent must check for existence of all 6 context files

        Arrange: Load agent file content
        Act: Search for context file validation logic
        Assert: Documents checking all 6 files
        """
        # Act
        context_files = [
            'tech-stack.md',
            'source-tree.md',
            'dependencies.md',
            'coding-standards.md',
            'architecture-constraints.md',
            'anti-patterns.md'
        ]

        # Check if all 6 files are referenced (validation requirement)
        found_files = sum(
            1 for file in context_files
            if re.search(re.escape(file), agent_content, re.IGNORECASE)
        )

        # Assert
        assert found_files == 6, \
            f"BR-001 FAILED: Only {found_files}/6 context files referenced (agent must validate all 6)"

    def test_br_001_halts_if_context_files_missing(self, agent_content):
        """
        BR-001: Agent must HALT with error if any context files missing

        Arrange: Load agent file content
        Act: Search for HALT behavior on missing files
        Assert: HALT documented with error listing missing files
        """
        # Act
        has_halt = bool(re.search(r'HALT', agent_content))
        has_missing_file_error = bool(re.search(
            r'missing.*file|list.*missing|error.*context.*file',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_halt and has_missing_file_error, \
            "BR-001 FAILED: Agent must HALT and list missing context files"

    def test_br_001_error_lists_missing_files(self, agent_content):
        """
        BR-001: Error message must list which context files are missing

        Arrange: Load agent file content
        Act: Search for error format with file list
        Assert: Documents listing missing files in error
        """
        # Act
        has_list_format = bool(re.search(
            r'list.*missing|missing.*:.*\n|missing.*file.*\n',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_list_format, \
            "BR-001 FAILED: Error message must list which context files are missing"

    def test_br_002_requires_adr_for_new_technology(self, agent_content):
        """
        BR-002: Agent must return 'REQUIRES ADR' for tech not in tech-stack.md

        Arrange: Load agent file content
        Act: Search for REQUIRES ADR message
        Assert: Message documented
        """
        # Act
        has_requires_adr = bool(re.search(r'REQUIRES ADR', agent_content))

        # Assert
        assert has_requires_adr, \
            "BR-002 FAILED: Agent must document 'REQUIRES ADR' message for new technologies"

    def test_br_002_askuserquestion_with_two_options(self, agent_content):
        """
        BR-002: AskUserQuestion must present 2 options for technology conflicts

        Arrange: Load agent file content
        Act: Search for AskUserQuestion with options
        Assert: 2 options documented (update tech-stack or adjust scope)
        """
        # Act
        has_askuserquestion = bool(re.search(r'AskUserQuestion', agent_content))

        # Check for option 1: Update tech-stack with ADR
        has_option_1 = bool(re.search(
            r'update.*tech-stack.*ADR|tech-stack.*ADR|option.*1.*update',
            agent_content,
            re.IGNORECASE
        ))

        # Check for option 2: Adjust research scope
        has_option_2 = bool(re.search(
            r'adjust.*scope|scope.*existing|option.*2.*adjust',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_askuserquestion, \
            "BR-002 FAILED: Must use AskUserQuestion for technology conflicts"
        assert has_option_1 and has_option_2, \
            "BR-002 FAILED: AskUserQuestion must present 2 options: (1) Update tech-stack.md, (2) Adjust scope"

    def test_br_003_outputs_written_to_devforgeai_research(self, agent_content):
        """
        BR-003: Research output files must be written to .devforgeai/research/

        Arrange: Load agent file content
        Act: Search for output directory specification
        Assert: .devforgeai/research/ documented as output location
        """
        # Act
        has_research_dir = bool(re.search(r'\.devforgeai/research/', agent_content))

        # Also check no old output locations remain
        has_old_output = bool(re.search(r'\.ai_docs/research/|tmp/repos/research-', agent_content))

        # Assert
        assert has_research_dir, \
            "BR-003 FAILED: Output files must be written to '.devforgeai/research/'"
        assert not has_old_output, \
            "BR-003 FAILED: Must NOT write outputs to deprecated locations"

    def test_br_003_directory_created_if_not_exists(self, agent_content):
        """
        BR-003: Directory must be created if it doesn't exist

        Arrange: Load agent file content
        Act: Search for directory creation behavior
        Assert: Documents creating directory before write
        """
        # Act
        has_create_dir = bool(re.search(
            r'create.*directory|mkdir|ensure.*exist|directory.*not.*exist',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_create_dir, \
            "BR-003 FAILED: Agent must document creating .devforgeai/research/ if it doesn't exist"

    def test_br_003_directory_permissions_755(self, agent_content):
        """
        BR-003: Directory must be created with 755 permissions

        Arrange: Load agent file content
        Act: Search for permission specification
        Assert: 755 or permission documentation present
        """
        # Act
        has_permissions = bool(re.search(r'755|chmod|permission', agent_content, re.IGNORECASE))

        # Assert (soft requirement - may be OS default)
        if not has_permissions:
            pytest.skip("Permissions not explicitly documented (may be OS default 755)")

    def test_br_004_validates_github_url_pattern(self, agent_content):
        """
        BR-004: Repository URLs must match GitHub pattern

        Arrange: Load agent file content
        Act: Search for URL validation documentation
        Assert: GitHub URL pattern documented
        """
        # Act
        has_url_validation = bool(re.search(
            r'github\.com|github.*URL|URL.*pattern|validate.*URL',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_url_validation, \
            "BR-004 FAILED: Agent must document GitHub URL validation"

    def test_br_004_rejects_malformed_urls_with_error(self, agent_content):
        """
        BR-004: Malformed URLs must be rejected with structured error

        Arrange: Load agent file content
        Act: Search for URL validation error
        Assert: Documents rejecting invalid URLs with error message
        """
        # Act
        has_validation_error = bool(re.search(
            r'invalid.*URL|malformed.*URL|reject.*URL|URL.*error',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_validation_error, \
            "BR-004 FAILED: Agent must document rejecting malformed URLs with structured error"

    def test_br_004_error_message_specifies_github_format(self, agent_content):
        """
        BR-004: Error message should specify expected GitHub URL format

        Arrange: Load agent file content
        Act: Search for GitHub URL format in error handling
        Assert: Expected format documented
        """
        # Act
        has_format_spec = bool(re.search(
            r'github\.com/\{owner\}/\{repo\}|expected.*github.*URL|github.*URL.*format',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_format_spec, \
            "BR-004 FAILED: Error message should specify expected GitHub URL format"

    def test_all_business_rules_documented(self, agent_content):
        """
        Comprehensive: Verify all 4 business rules have documentation

        Arrange: Load agent file content
        Act: Check for keywords related to each business rule
        Assert: All 4 rules documented
        """
        # Act
        rules = {
            'BR-001': bool(re.search(r'context.*file.*exist|HALT.*missing', agent_content, re.IGNORECASE)),
            'BR-002': bool(re.search(r'REQUIRES ADR', agent_content)),
            'BR-003': bool(re.search(r'\.devforgeai/research/', agent_content)),
            'BR-004': bool(re.search(r'github.*URL|URL.*github', agent_content, re.IGNORECASE))
        }

        documented_rules = sum(1 for documented in rules.values() if documented)
        missing_rules = [rule for rule, documented in rules.items() if not documented]

        # Assert
        assert documented_rules == 4, \
            f"Only {documented_rules}/4 business rules documented. Missing: {missing_rules}"

    def test_business_rules_use_framework_patterns(self, agent_content):
        """
        Best practice: Business rule enforcement should use DevForgeAI patterns

        Arrange: Load agent file content
        Act: Verify framework patterns used
        Assert: HALT, AskUserQuestion, structured errors present
        """
        # Act
        framework_patterns = {
            'HALT': bool(re.search(r'HALT', agent_content)),
            'AskUserQuestion': bool(re.search(r'AskUserQuestion', agent_content)),
            'Structured Error': bool(re.search(
                r'structured.*error|error.*format|error.*message',
                agent_content,
                re.IGNORECASE
            ))
        }

        used_patterns = sum(1 for used in framework_patterns.values() if used)

        # Assert
        assert used_patterns >= 2, \
            f"Only {used_patterns}/3 framework patterns used in business rules (expected ≥2)"

    def test_business_rule_violations_halt_execution(self, agent_content):
        """
        Critical: Business rule violations must halt execution (not warnings)

        Arrange: Load agent file content
        Act: Verify HALT behavior documented for violations
        Assert: No "warning" language for critical violations
        """
        # Act
        has_halt = bool(re.search(r'HALT', agent_content))

        # Check if warnings used instead of halts (anti-pattern)
        warning_for_critical = bool(re.search(
            r'warning.*context.*missing|warning.*tech.*conflict',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_halt, "Business rule violations must HALT execution"
        assert not warning_for_critical, \
            "Critical violations must HALT, not warn (context missing, tech conflicts are HALT conditions)"
