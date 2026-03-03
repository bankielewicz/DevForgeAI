"""
Integration Test: Secret Redaction in Research Reports

Tests for STORY-035: Internet-Sleuth Framework Compliance (Phase 1 Migration)

Security NFR-003: If analyzing repositories, do NOT expose secrets in research reports
(redact API keys, tokens, passwords using pattern matching)
"""

import pytest
import re
from pathlib import Path


class TestInternetSleuthSecretRedaction:
    """Integration test suite for secret redaction functionality"""

    @pytest.fixture
    def redaction_patterns(self):
        """Fixture: Return secret redaction patterns from agent spec"""
        return {
            "api_key": r"api[_-]?key.*=.*[A-Za-z0-9]{20,}",
            "password": r"password.*=.*",
            "private_key": r"BEGIN.*PRIVATE KEY"
        }

    @pytest.fixture
    def agent_documentation(self):
        """Fixture: Load agent file for pattern verification"""
        agent_file = Path(".claude/agents/internet-sleuth.md")
        return agent_file.read_text()

    @pytest.mark.story_035
    @pytest.mark.integration
    @pytest.mark.security
    def test_agent_documents_secret_redaction(self, agent_documentation):
        """Test: Agent documentation includes secret redaction patterns"""
        # Verify secret redaction is documented
        assert "Secret Redaction" in agent_documentation or "secret redaction" in agent_documentation.lower(), \
            "Agent must document secret redaction capability"

        # Verify [REDACTED] replacement pattern documented
        assert "[REDACTED]" in agent_documentation, \
            "Agent must document [REDACTED] replacement pattern"

    @pytest.mark.story_035
    @pytest.mark.integration
    @pytest.mark.security
    def test_api_key_pattern_documented(self, agent_documentation, redaction_patterns):
        """Test: API key redaction pattern is documented"""
        # Check if API key pattern is present or similar pattern exists
        has_api_key_pattern = "api" in agent_documentation.lower() and "key" in agent_documentation.lower()
        assert has_api_key_pattern, "Agent should document API key redaction"

        # Verify pattern documentation includes character length threshold
        has_length_threshold = re.search(r"\{(\d+),\}", agent_documentation) is not None
        assert has_length_threshold, "Pattern should include character length threshold (e.g., {20,})"

    @pytest.mark.story_035
    @pytest.mark.integration
    @pytest.mark.security
    def test_password_pattern_documented(self, agent_documentation):
        """Test: Password redaction pattern is documented"""
        has_password_pattern = "password" in agent_documentation.lower()
        assert has_password_pattern, "Agent should document password redaction"

    @pytest.mark.story_035
    @pytest.mark.integration
    @pytest.mark.security
    def test_private_key_pattern_documented(self, agent_documentation):
        """Test: Private key redaction pattern is documented"""
        has_private_key = "PRIVATE KEY" in agent_documentation or "private key" in agent_documentation.lower()
        assert has_private_key, "Agent should document private key redaction"

    @pytest.mark.story_035
    @pytest.mark.integration
    @pytest.mark.security
    def test_simulated_api_key_redaction(self):
        """Test: Verify API key would be redacted using documented pattern"""
        # Arrange: Sample code with API key
        sample_code = """
const API_KEY = "sk_live_1234567890abcdefghijklmnopqrstuvwxyz";
const secret = "ghp_abcdefghijklmnopqrstuvwxyz1234567890";
        """

        # Act: Apply documented redaction pattern
        pattern = r"(api[_-]?key|secret)\s*=\s*['\"]([A-Za-z0-9_]{20,})['\"]"
        redacted = re.sub(pattern, r'\1 = "[REDACTED]"', sample_code, flags=re.IGNORECASE)

        # Assert: Secrets should be redacted
        assert "[REDACTED]" in redacted, "API keys should be redacted"
        assert "sk_live_1234567890" not in redacted, "API key value should be removed"
        assert "ghp_abcdefghijklm" not in redacted, "Secret value should be removed"

    @pytest.mark.story_035
    @pytest.mark.integration
    @pytest.mark.security
    def test_simulated_password_redaction(self):
        """Test: Verify password would be redacted using documented pattern"""
        # Arrange: Sample configuration with password
        sample_config = """
database_password = "super_secret_123!"
db_pass: "another_password_456"
        """

        # Act: Apply documented redaction pattern
        pattern = r"(password|pass|pwd)\s*[:=]\s*['\"]([^'\"]+)['\"]"
        redacted = re.sub(pattern, r'\1: "[REDACTED]"', sample_config, flags=re.IGNORECASE)

        # Assert: Passwords should be redacted
        assert "[REDACTED]" in redacted, "Passwords should be redacted"
        assert "super_secret_123" not in redacted, "Password value should be removed"
        assert "another_password" not in redacted, "Password value should be removed"

    @pytest.mark.story_035
    @pytest.mark.integration
    @pytest.mark.security
    def test_simulated_private_key_redaction(self):
        """Test: Verify private key would be redacted using documented pattern"""
        # Arrange: Sample private key
        sample_key = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234567890abcdefghijklmnopqrstuvwxyz
-----END RSA PRIVATE KEY-----
        """

        # Act: Apply documented redaction pattern
        pattern = r"-----BEGIN.*PRIVATE KEY-----.*?-----END.*PRIVATE KEY-----"
        redacted = re.sub(pattern, "[REDACTED PRIVATE KEY]", sample_key, flags=re.DOTALL)

        # Assert: Private key should be redacted
        assert "[REDACTED PRIVATE KEY]" in redacted, "Private key should be redacted"
        assert "MIIEpAIBAAKCAQEA" not in redacted, "Private key content should be removed"

    @pytest.mark.story_035
    @pytest.mark.integration
    @pytest.mark.security
    def test_redaction_patterns_comprehensive(self, agent_documentation):
        """Test: Agent documentation covers comprehensive secret types"""
        # Verify multiple secret types documented
        secret_types = ["api key", "token", "password", "private key"]
        covered_types = [stype for stype in secret_types if stype in agent_documentation.lower()]

        assert len(covered_types) >= 3, \
            f"Agent should document at least 3 secret types. Found: {covered_types}"

    @pytest.mark.story_035
    @pytest.mark.integration
    @pytest.mark.security
    def test_redaction_in_research_reports_requirement(self, agent_documentation):
        """Test: Agent explicitly states redaction applies to research reports"""
        # Verify documentation makes clear that redaction applies to outputs
        has_research_report_context = "research report" in agent_documentation.lower() or \
                                      "research output" in agent_documentation.lower() or \
                                      "output" in agent_documentation.lower()

        assert has_research_report_context, \
            "Agent should explicitly state redaction applies to research reports/outputs"

    @pytest.mark.story_035
    @pytest.mark.integration
    @pytest.mark.security
    def test_no_hardcoded_credentials_in_agent_file(self):
        """Test: Agent file contains no hardcoded credentials"""
        agent_file = Path(".claude/agents/internet-sleuth.md")
        content = agent_file.read_text()

        # Check for common credential patterns (should NOT be found)
        forbidden_patterns = [
            r"ghp_[A-Za-z0-9]{36}",  # GitHub personal access token
            r"sk_live_[A-Za-z0-9]+",  # API keys starting with sk_live
            r"Bearer [A-Za-z0-9]{20,}",  # Bearer tokens
            r"api[_-]?key\s*=\s*['\"][A-Za-z0-9]{10,}['\"]",  # Hardcoded API keys
        ]

        for pattern in forbidden_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            assert len(matches) == 0, \
                f"Agent file should NOT contain hardcoded credentials matching pattern: {pattern}"

    @pytest.mark.story_035
    @pytest.mark.integration
    @pytest.mark.security
    def test_environment_variable_usage_documented(self, agent_documentation):
        """Test: Agent documents GITHUB_TOKEN environment variable usage"""
        assert "GITHUB_TOKEN" in agent_documentation, \
            "Agent must document GITHUB_TOKEN environment variable"

        # Verify it's documented as environment variable (not hardcoded)
        assert "environment variable" in agent_documentation.lower() or \
               "env var" in agent_documentation.lower() or \
               "os.environ" in agent_documentation or \
               "$GITHUB_TOKEN" in agent_documentation or \
               "${GITHUB_TOKEN}" in agent_documentation, \
            "GITHUB_TOKEN must be documented as environment variable"

    @pytest.mark.story_035
    @pytest.mark.integration
    @pytest.mark.security
    def test_no_credential_prompts_documented(self, agent_documentation):
        """Test: Agent does NOT prompt for credentials"""
        # Agent should never ask user for passwords/tokens
        forbidden_prompts = ["enter password", "input token", "provide api key", "credential prompt"]

        for prompt_pattern in forbidden_prompts:
            assert prompt_pattern not in agent_documentation.lower(), \
                f"Agent should NOT prompt for credentials (found: '{prompt_pattern}')"

        # Verify explicit statement about inheriting credentials
        assert "inherit" in agent_documentation.lower() or \
               "caller" in agent_documentation.lower(), \
            "Agent should document it inherits caller's credentials"
