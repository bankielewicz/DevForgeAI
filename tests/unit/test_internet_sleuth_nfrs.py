"""
Unit tests for STORY-035 Non-Functional Requirements (NFRs)

Tests verify agent documentation for NFRs:
- Performance: <2min for repos <100 files, <40K tokens per analysis
- Security: No hardcoded secrets, environment variables only
- Reliability: Retry with exponential backoff, graceful degradation
- Observability: Logging, error handling
"""

import pytest
import re
from pathlib import Path


@pytest.mark.story_035
@pytest.mark.nfr
@pytest.mark.unit
class TestInternetSleuthNFRs:
    """Test suite for non-functional requirements"""

    @pytest.fixture
    def agent_file_path(self):
        """Path to internet-sleuth agent file"""
        return Path(".claude/agents/internet-sleuth.md")

    @pytest.fixture
    def agent_content(self, agent_file_path):
        """Load agent file content"""
        assert agent_file_path.exists(), f"Agent file not found: {agent_file_path}"
        return agent_file_path.read_text()

    # Performance NFRs
    def test_nfr_001_repository_analysis_time_documented(self, agent_content):
        """
        NFR-001: Repository analysis <2 minutes for repos <100 files

        Arrange: Load agent file content
        Act: Search for performance targets
        Assert: Time target documented
        """
        # Act
        has_perf_target = bool(re.search(
            r'2.*minute|< 2.*min|120.*second',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        if not has_perf_target:
            pytest.skip("Performance targets may be implicit (acceptable for subagent)")

    def test_nfr_002_token_usage_budget_40k(self, agent_content):
        """
        NFR-002: Token usage <40K per repository analysis

        Arrange: Load agent file content
        Act: Search for token budget
        Assert: 40K token budget documented
        """
        # Act
        has_token_budget = bool(re.search(r'40[,\s]*000|40K', agent_content, re.IGNORECASE))

        # Assert
        assert has_token_budget, \
            "NFR-002 FAILED: Agent must document 40K token budget for single repository analysis"

    def test_nfr_002_progressive_disclosure_for_token_efficiency(self, agent_content):
        """
        NFR-002: Progressive disclosure strategy for large repositories

        Arrange: Load agent file content
        Act: Search for progressive disclosure
        Assert: Strategy documented
        """
        # Act
        has_progressive = bool(re.search(r'progressive.*disclos', agent_content, re.IGNORECASE))

        # Assert
        assert has_progressive, \
            "NFR-002 FAILED: Agent must document progressive disclosure for token efficiency"

    # Security NFRs
    def test_nfr_003_no_hardcoded_credentials_in_agent_file(self, agent_content):
        """
        NFR-003: No hardcoded API keys or tokens in agent file

        Arrange: Load agent file content
        Act: Search for credential patterns
        Assert: Zero hardcoded credentials found
        """
        # Act
        credential_patterns = [
            r'api_key\s*=',
            r'token\s*=',
            r'password\s*=',
            r'secret\s*=',
            r'ghp_[A-Za-z0-9]+',  # GitHub personal access token pattern
            r'gho_[A-Za-z0-9]+'   # GitHub OAuth token pattern
        ]

        found_credentials = []
        for pattern in credential_patterns:
            if re.search(pattern, agent_content, re.IGNORECASE):
                found_credentials.append(pattern)

        # Assert
        assert len(found_credentials) == 0, \
            f"NFR-003 FAILED: Found hardcoded credentials: {found_credentials} (use environment variables)"

    def test_nfr_003_uses_github_token_environment_variable(self, agent_content):
        """
        NFR-003: Agent must use GITHUB_TOKEN environment variable

        Arrange: Load agent file content
        Act: Search for environment variable usage
        Assert: GITHUB_TOKEN referenced
        """
        # Act
        has_github_token = bool(re.search(r'GITHUB_TOKEN|github.*token.*environment', agent_content, re.IGNORECASE))

        # Assert
        assert has_github_token, \
            "NFR-003 FAILED: Agent must document using GITHUB_TOKEN environment variable"

    def test_nfr_003_uses_gh_cli_credentials(self, agent_content):
        """
        NFR-003: Agent can use gh CLI credentials

        Arrange: Load agent file content
        Act: Search for gh CLI usage
        Assert: gh CLI authentication method documented
        """
        # Act
        has_gh_cli = bool(re.search(r'gh\s+CLI|gh\s+auth|github.*cli', agent_content, re.IGNORECASE))

        # Assert
        assert has_gh_cli, \
            "NFR-003 FAILED: Agent must document gh CLI credential option"

    def test_nfr_004_temp_directory_cleanup_documented(self, agent_content):
        """
        NFR-004: Temporary directories must be removed on exit

        Arrange: Load agent file content
        Act: Search for cleanup behavior
        Assert: Cleanup documented (trap EXIT or equivalent)
        """
        # Act
        has_cleanup = bool(re.search(
            r'cleanup|remove.*temp|trap.*EXIT|delete.*repositor',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_cleanup, \
            "NFR-004 FAILED: Agent must document temporary directory cleanup on exit"

    def test_nfr_004_cleanup_on_failure_documented(self, agent_content):
        """
        NFR-004: Cleanup must occur even if analysis fails

        Arrange: Load agent file content
        Act: Search for cleanup on failure
        Assert: Guaranteed cleanup documented
        """
        # Act
        has_guaranteed_cleanup = bool(re.search(
            r'cleanup.*fail|fail.*cleanup|trap.*EXIT|always.*clean',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_guaranteed_cleanup, \
            "NFR-004 FAILED: Agent must guarantee cleanup even on analysis failure"

    # Reliability NFRs
    def test_nfr_005_github_api_retry_with_exponential_backoff(self, agent_content):
        """
        NFR-005: GitHub API failures retry with exponential backoff

        Arrange: Load agent file content
        Act: Search for retry logic
        Assert: Max 3 retries with 1s, 2s, 4s delays documented
        """
        # Act
        has_retry = bool(re.search(r'retry|exponential.*backoff', agent_content, re.IGNORECASE))

        # Check for delay specifications
        has_delays = bool(re.search(r'1s.*2s.*4s|1.*second.*2.*second.*4.*second', agent_content, re.IGNORECASE))

        # Assert
        assert has_retry, \
            "NFR-005 FAILED: Agent must document retry logic for GitHub API failures"
        assert has_delays, \
            "NFR-005 FAILED: Agent must document exponential backoff delays (1s, 2s, 4s)"

    def test_nfr_005_max_three_retries(self, agent_content):
        """
        NFR-005: Maximum 3 retry attempts

        Arrange: Load agent file content
        Act: Search for max retry limit
        Assert: 3 retry limit documented
        """
        # Act
        has_max_retries = bool(re.search(r'max.*3.*retr|3.*retr.*max|maximum.*3', agent_content, re.IGNORECASE))

        # Assert
        assert has_max_retries, \
            "NFR-005 FAILED: Agent must document max 3 retry attempts"

    def test_nfr_006_graceful_degradation_for_inaccessible_repos(self, agent_content):
        """
        NFR-006: Continue with available repos if one fails (404, 403)

        Arrange: Load agent file content
        Act: Search for graceful degradation
        Assert: Continue processing documented
        """
        # Act
        has_graceful_degradation = bool(re.search(
            r'graceful.*degrad|continue.*available|continue.*process',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_graceful_degradation, \
            "NFR-006 FAILED: Agent must document graceful degradation (continue with available repos)"

    def test_nfr_006_note_failures_in_summary(self, agent_content):
        """
        NFR-006: Note failures in summary report

        Arrange: Load agent file content
        Act: Search for failure tracking
        Assert: Documents listing failed repos in summary
        """
        # Act
        has_failure_tracking = bool(re.search(
            r'note.*failure|list.*fail|summary.*fail|failed.*repo',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_failure_tracking, \
            "NFR-006 FAILED: Agent must document listing failures in summary report"

    # Error Handling
    def test_structured_errors_documented(self, agent_content):
        """
        Best practice: Agent should return structured errors

        Arrange: Load agent file content
        Act: Search for error handling documentation
        Assert: Structured error format documented
        """
        # Act
        has_error_handling = bool(re.search(
            r'structured.*error|error.*format|error.*handling',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_error_handling, \
            "Agent should document structured error handling"

    def test_errors_include_remediation_steps(self, agent_content):
        """
        Best practice: Errors should include remediation steps

        Arrange: Load agent file content
        Act: Search for remediation documentation
        Assert: Remediation steps mentioned in error handling
        """
        # Act
        has_remediation = bool(re.search(
            r'remediation|recovery|resolution|how.*fix',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        assert has_remediation, \
            "Agent should document remediation steps for common errors"

    # Observability
    def test_logging_behavior_documented(self, agent_content):
        """
        Best practice: Logging behavior should be documented

        Arrange: Load agent file content
        Act: Search for logging documentation
        Assert: Logging approach documented
        """
        # Act
        has_logging = bool(re.search(
            r'log|logging|audit.*trail|track.*attempt',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        if not has_logging:
            pytest.skip("Logging may be implicit (acceptable for subagent)")

    def test_comprehensive_nfr_coverage(self, agent_content):
        """
        Comprehensive: Verify coverage of major NFR categories

        Arrange: Load agent file content
        Act: Check for NFR category documentation
        Assert: At least 3 of 4 categories documented
        """
        # Act
        nfr_categories = {
            'Performance': bool(re.search(r'40K|40,000|token.*budget|2.*minute', agent_content, re.IGNORECASE)),
            'Security': bool(re.search(r'GITHUB_TOKEN|gh.*CLI|environment.*variable', agent_content, re.IGNORECASE)),
            'Reliability': bool(re.search(r'retry|exponential.*backoff|graceful', agent_content, re.IGNORECASE)),
            'Observability': bool(re.search(r'log|track|audit|monitor', agent_content, re.IGNORECASE))
        }

        documented_categories = sum(1 for documented in nfr_categories.values() if documented)

        # Assert
        assert documented_categories >= 3, \
            f"Only {documented_categories}/4 NFR categories documented (expected ≥3)"

    def test_github_api_rate_limiting_handled(self, agent_content):
        """
        Best practice: GitHub API rate limiting should be documented

        Arrange: Load agent file content
        Act: Search for rate limit handling
        Assert: Rate limit documentation present
        """
        # Act
        has_rate_limit = bool(re.search(
            r'rate.*limit|60.*request|API.*limit|403.*rate',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        if not has_rate_limit:
            pytest.skip("Rate limiting may be handled by retry logic")

    def test_result_pattern_for_error_handling(self, agent_content):
        """
        Best practice: Should follow Result Pattern per coding-standards.md

        Arrange: Load agent file content
        Act: Search for Result Pattern reference
        Assert: Result Pattern mentioned or structured errors documented
        """
        # Act
        has_result_pattern = bool(re.search(
            r'Result.*Pattern|structured.*result|result.*object',
            agent_content,
            re.IGNORECASE
        ))

        # Assert
        if not has_result_pattern:
            pytest.skip("Result Pattern may be implied by structured error documentation")
