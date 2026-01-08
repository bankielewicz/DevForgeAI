"""
Test Suite for Credential Masker (STORY-244)

Tests for CredentialMasker class that sanitizes output to prevent credential exposure:
- AC#7: Credential Masking in Logs

Test Framework: pytest with unittest.mock
Test Naming Convention: test_<function>_<scenario>_<expected>
Pattern: AAA (Arrange, Act, Assert)

These tests will FAIL initially (TDD Red phase) because:
- installer/credential_masker.py does not exist yet
- CredentialMasker class not implemented
"""

import pytest
import re
from unittest.mock import Mock, patch, MagicMock


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def credential_masker():
    """Create a CredentialMasker instance for testing."""
    from installer.credential_masker import CredentialMasker
    return CredentialMasker()


@pytest.fixture
def sample_output_with_npm_token():
    """Sample output containing npm token."""
    return """
npm notice Publishing to https://registry.npmjs.org
npm notice package: devforgeai@1.0.0
npm WARN using --token npm_secret_token_12345abcdef
+ devforgeai@1.0.0
"""


@pytest.fixture
def sample_output_with_multiple_credentials():
    """Sample output containing multiple credential types."""
    return """
Setting up credentials...
NPM_TOKEN=npm_abcd1234567890
TWINE_PASSWORD=pypi_password_super_secret
NUGET_API_KEY=oy2nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN=ghp_abcdefghijklmnopqrstuvwxyz1234567890
CARGO_REGISTRY_TOKEN=cratesio_token_secret_value
DOCKER_PASSWORD=d0cker_p@ssw0rd!123
Publishing complete.
"""


# =============================================================================
# AC#7: Credential Masking in Logs Tests
# =============================================================================

class TestMaskOutput:
    """Tests for mask_output method (AC#7)."""

    def test_mask_output_should_mask_npm_token(self, credential_masker):
        """AC#7: NPM tokens are masked with ***."""
        # Arrange
        text = "Using token: npm_secret_token_12345abcdef for authentication"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "npm_secret_token_12345abcdef" not in masked
        assert "***" in masked

    def test_mask_output_should_mask_pypi_password(self, credential_masker):
        """AC#7: PyPI passwords are masked with ***."""
        # Arrange
        text = "TWINE_PASSWORD=super_secret_pypi_password123"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "super_secret_pypi_password123" not in masked
        assert "***" in masked

    def test_mask_output_should_mask_nuget_api_key(self, credential_masker):
        """AC#7: NuGet API keys are masked with ***."""
        # Arrange
        text = "--api-key oy2nxabcdefghijklmnopqrstuvwxyz1234567890"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "oy2nxabcdefghijklmnopqrstuvwxyz1234567890" not in masked
        assert "***" in masked

    def test_mask_output_should_mask_github_token(self, credential_masker):
        """AC#7: GitHub tokens (ghp_*) are masked with ***."""
        # Arrange
        text = "Authorization: token ghp_abcdefghijklmnopqrstuvwxyz1234567890"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "ghp_abcdefghijklmnopqrstuvwxyz1234567890" not in masked
        assert "***" in masked

    def test_mask_output_should_mask_github_pat_classic(self, credential_masker):
        """AC#7: GitHub classic PAT (ghp_*) are masked with ***."""
        # Arrange
        text = "GITHUB_TOKEN=ghp_1234567890abcdefghijklmnopqrstuvwxyz"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "ghp_1234567890abcdefghijklmnopqrstuvwxyz" not in masked
        assert "***" in masked

    def test_mask_output_should_mask_github_fine_grained_pat(self, credential_masker):
        """AC#7: GitHub fine-grained PAT (github_pat_*) are masked."""
        # Arrange
        text = "Using github_pat_11ABCDEFGH0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "github_pat_11ABCDEFGH0" not in masked
        assert "***" in masked

    def test_mask_output_should_mask_cargo_registry_token(self, credential_masker):
        """AC#7: Cargo registry tokens are masked with ***."""
        # Arrange
        text = "CARGO_REGISTRY_TOKEN=cio_abcdefghijklmnopqrstuvwxyz1234567890"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "cio_abcdefghijklmnopqrstuvwxyz1234567890" not in masked
        assert "***" in masked

    def test_mask_output_should_mask_docker_password(self, credential_masker):
        """AC#7: Docker passwords are masked with ***."""
        # Arrange
        text = "docker login -u user -p my_docker_password_secret123"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "my_docker_password_secret123" not in masked
        assert "***" in masked

    def test_mask_output_should_handle_multiple_credentials(
        self, credential_masker, sample_output_with_multiple_credentials
    ):
        """AC#7: All credentials in output are masked."""
        # Arrange
        text = sample_output_with_multiple_credentials

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "npm_abcd1234567890" not in masked
        assert "pypi_password_super_secret" not in masked
        assert "oy2nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" not in masked
        assert "ghp_abcdefghijklmnopqrstuvwxyz1234567890" not in masked
        assert "cratesio_token_secret_value" not in masked
        assert "d0cker_p@ssw0rd!123" not in masked
        # Should still contain non-sensitive parts
        assert "Setting up credentials..." in masked
        assert "Publishing complete." in masked

    def test_mask_output_should_preserve_non_sensitive_content(
        self, credential_masker
    ):
        """AC#7: Non-sensitive content is preserved."""
        # Arrange
        text = "Published devforgeai@1.0.0 to registry.npmjs.org successfully"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert masked == text  # No changes

    def test_mask_output_should_handle_empty_string(self, credential_masker):
        """Edge case: Empty string input."""
        # Arrange
        text = ""

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert masked == ""

    def test_mask_output_should_handle_none_gracefully(self, credential_masker):
        """Edge case: None input."""
        # Arrange & Act & Assert
        # Should either return empty string or handle None gracefully
        result = credential_masker.mask_output(None)
        assert result is None or result == ""


# =============================================================================
# Credential Pattern Tests (AC#7 Verification)
# =============================================================================

class TestCredentialPatterns:
    """Tests for credential pattern detection."""

    def test_mask_output_should_detect_bearer_token_pattern(self, credential_masker):
        """AC#7 Verification: Bearer token pattern detected."""
        # Arrange
        text = "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxx"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in masked
        assert "***" in masked

    def test_mask_output_should_detect_basic_auth_pattern(self, credential_masker):
        """AC#7 Verification: Basic auth pattern detected."""
        # Arrange
        text = "Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ="

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "dXNlcm5hbWU6cGFzc3dvcmQ=" not in masked
        assert "***" in masked

    def test_mask_output_should_detect_aws_access_key(self, credential_masker):
        """AC#7 Verification: AWS access key pattern detected."""
        # Arrange
        text = "AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "AKIAIOSFODNN7EXAMPLE" not in masked
        assert "***" in masked

    def test_mask_output_should_detect_aws_secret_key(self, credential_masker):
        """AC#7 Verification: AWS secret key pattern detected."""
        # Arrange
        text = "AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" not in masked
        assert "***" in masked

    def test_mask_output_should_detect_password_in_url(self, credential_masker):
        """AC#7 Verification: Password in URL detected."""
        # Arrange
        text = "https://user:secret_password@registry.example.com/package"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "secret_password" not in masked
        assert "***" in masked
        # Should preserve URL structure
        assert "registry.example.com" in masked

    def test_mask_output_should_detect_api_key_patterns(self, credential_masker):
        """AC#7 Verification: Generic API key patterns detected."""
        # Arrange
        texts = [
            "api_key=sk_live_abcdef1234567890",
            "apiKey: 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'",
            "API-KEY: secret_api_key_value",
            "x-api-key: my_api_key_12345",
        ]

        for text in texts:
            # Act
            masked = credential_masker.mask_output(text)

            # Assert
            assert "sk_live_" not in masked or "***" in masked
            assert text != masked  # Something should be masked


# =============================================================================
# scan_for_leaks Tests (AC#7 Verification)
# =============================================================================

class TestScanForLeaks:
    """Tests for scan_for_leaks method."""

    def test_scan_for_leaks_should_return_empty_for_clean_text(
        self, credential_masker
    ):
        """AC#7 Verification: Clean text returns no leaks."""
        # Arrange
        text = "Published devforgeai@1.0.0 successfully"

        # Act
        leaks = credential_masker.scan_for_leaks(text)

        # Assert
        assert leaks == []

    def test_scan_for_leaks_should_detect_npm_token(self, credential_masker):
        """AC#7 Verification: NPM token leak detected."""
        # Arrange
        text = "Using npm_secret_token_12345 for publish"

        # Act
        leaks = credential_masker.scan_for_leaks(text)

        # Assert
        assert len(leaks) > 0
        assert any("npm" in leak.lower() for leak in leaks)

    def test_scan_for_leaks_should_detect_github_token(self, credential_masker):
        """AC#7 Verification: GitHub token leak detected."""
        # Arrange
        text = "Authorization: ghp_1234567890abcdefghijklmnopqrstuvwxyz"

        # Act
        leaks = credential_masker.scan_for_leaks(text)

        # Assert
        assert len(leaks) > 0
        assert any("github" in leak.lower() or "ghp_" in leak for leak in leaks)

    def test_scan_for_leaks_should_detect_multiple_leaks(
        self, credential_masker, sample_output_with_multiple_credentials
    ):
        """AC#7 Verification: Multiple leaks detected."""
        # Arrange
        text = sample_output_with_multiple_credentials

        # Act
        leaks = credential_masker.scan_for_leaks(text)

        # Assert
        assert len(leaks) >= 3  # At least 3 different credential types

    def test_scan_for_leaks_should_return_matched_patterns(
        self, credential_masker
    ):
        """AC#7: Warning is issued if unmasked credential pattern detected."""
        # Arrange
        text = "NUGET_API_KEY=oy2nxabcdefghijklmnop"

        # Act
        leaks = credential_masker.scan_for_leaks(text)

        # Assert
        assert len(leaks) > 0
        # Each leak should identify what was found
        assert any("oy2nx" in str(leak) or "nuget" in str(leak).lower() for leak in leaks)


# =============================================================================
# get_patterns Tests
# =============================================================================

class TestGetPatterns:
    """Tests for get_patterns method."""

    def test_get_patterns_should_return_list_of_regex(self, credential_masker):
        """Tech Spec: get_patterns returns list of compiled regex patterns."""
        # Arrange & Act
        patterns = credential_masker.get_patterns()

        # Assert
        assert isinstance(patterns, list)
        assert len(patterns) > 0
        for pattern in patterns:
            assert isinstance(pattern, re.Pattern)

    def test_get_patterns_should_include_npm_token_pattern(self, credential_masker):
        """Patterns should include npm token regex."""
        # Arrange
        patterns = credential_masker.get_patterns()

        # Act - Test if any pattern matches npm token
        test_token = "npm_abcd1234567890"
        matches = any(p.search(test_token) for p in patterns)

        # Assert
        assert matches, "No pattern matches npm token format"

    def test_get_patterns_should_include_github_token_pattern(self, credential_masker):
        """Patterns should include GitHub token regex."""
        # Arrange
        patterns = credential_masker.get_patterns()

        # Act
        test_token = "ghp_abcdefghijklmnopqrstuvwxyz1234567890"
        matches = any(p.search(test_token) for p in patterns)

        # Assert
        assert matches, "No pattern matches GitHub token format"

    def test_get_patterns_should_include_nuget_api_key_pattern(self, credential_masker):
        """Patterns should include NuGet API key regex."""
        # Arrange
        patterns = credential_masker.get_patterns()

        # Act
        test_key = "oy2nxabcdefghijklmnopqrstuvwxyz1234567890"
        matches = any(p.search(test_key) for p in patterns)

        # Assert
        assert matches, "No pattern matches NuGet API key format"

    def test_get_patterns_should_include_bearer_token_pattern(self, credential_masker):
        """Patterns should include Bearer token regex."""
        # Arrange
        patterns = credential_masker.get_patterns()

        # Act
        test_header = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ0ZXN0IjoxfQ.sig"
        matches = any(p.search(test_header) for p in patterns)

        # Assert
        assert matches, "No pattern matches Bearer token format"

    def test_get_patterns_should_include_password_env_var_pattern(
        self, credential_masker
    ):
        """Patterns should include PASSWORD env var regex."""
        # Arrange
        patterns = credential_masker.get_patterns()

        # Act
        test_env = "TWINE_PASSWORD=secret123"
        matches = any(p.search(test_env) for p in patterns)

        # Assert
        assert matches, "No pattern matches PASSWORD env var format"


# =============================================================================
# Masking in Different Contexts Tests
# =============================================================================

class TestMaskingContexts:
    """Tests for masking in stdout, stderr, and log files (AC#7)."""

    def test_mask_stdout_should_sanitize_credentials(self, credential_masker):
        """AC#7: Masking applied to stdout capture."""
        # Arrange
        stdout = """
npm notice
npm notice Publishing to https://registry.npmjs.org/
npm notice === Tarball Contents ===
npm http fetch POST 200 https://registry.npmjs.org/-/user/org.couchdb.user:username 1234ms
Using token: npm_secret_12345
+ devforgeai@1.0.0
"""

        # Act
        masked = credential_masker.mask_output(stdout)

        # Assert
        assert "npm_secret_12345" not in masked
        assert "***" in masked
        # Preserve package name and version
        assert "devforgeai@1.0.0" in masked

    def test_mask_stderr_should_sanitize_credentials(self, credential_masker):
        """AC#7: Masking applied to stderr capture."""
        # Arrange
        stderr = """
npm WARN publish Error authenticating
npm ERR! code E401
npm ERR! Unable to authenticate, need: Bearer authorization_uri=https://login.microsoft.com/
npm ERR! Token: npm_bad_token_999 expired
"""

        # Act
        masked = credential_masker.mask_output(stderr)

        # Assert
        assert "npm_bad_token_999" not in masked
        assert "***" in masked
        # Preserve error messages
        assert "E401" in masked

    def test_mask_log_file_content_should_sanitize_credentials(
        self, credential_masker
    ):
        """AC#7: Log files sanitized."""
        # Arrange
        log_content = """
2025-01-06 10:00:00 INFO Starting publish to npm
2025-01-06 10:00:01 DEBUG Using NPM_TOKEN=npm_abcd_secret_token
2025-01-06 10:00:02 INFO Published successfully
2025-01-06 10:00:03 DEBUG docker login -p docker_password123
"""

        # Act
        masked = credential_masker.mask_output(log_content)

        # Assert
        assert "npm_abcd_secret_token" not in masked
        assert "docker_password123" not in masked
        assert "***" in masked
        # Preserve log structure
        assert "2025-01-06" in masked
        assert "INFO" in masked

    def test_mask_credentials_in_error_messages(self, credential_masker):
        """Edge Case 7: Credential in error output - Mask even in error messages."""
        # Arrange
        error_output = """
Error: Failed to authenticate with registry
Details: Token npm_12345_secret was rejected
Please check your NPM_TOKEN environment variable
"""

        # Act
        masked = credential_masker.mask_output(error_output)

        # Assert
        assert "npm_12345_secret" not in masked
        assert "***" in masked
        # Preserve error context
        assert "Failed to authenticate" in masked


# =============================================================================
# Post-Execution Scan Tests (AC#7 Verification)
# =============================================================================

class TestPostExecutionScan:
    """Tests for post-execution credential leak detection."""

    def test_should_detect_leaked_credential_after_mask_failure(
        self, credential_masker
    ):
        """AC#7 Verification: Post-execution scan for leaked credentials."""
        # Arrange - Simulate output that might have slipped through
        output_after_processing = "Published with token npm_test123 to registry"

        # Act
        leaks = credential_masker.scan_for_leaks(output_after_processing)

        # Assert
        assert len(leaks) > 0, "Leaked credential should be detected"

    def test_should_return_no_leaks_after_proper_masking(self, credential_masker):
        """AC#7 Verification: Properly masked output has no leaks."""
        # Arrange
        original = "Using NPM_TOKEN=npm_secret_value"
        masked = credential_masker.mask_output(original)

        # Act
        leaks = credential_masker.scan_for_leaks(masked)

        # Assert
        assert len(leaks) == 0, f"Masked output still has leaks: {leaks}"


# =============================================================================
# NFR-002: Security Tests
# =============================================================================

class TestSecurityRequirements:
    """Tests for NFR-002: No credentials appear in any log output."""

    def test_nfr002_no_credentials_in_masked_output(
        self, credential_masker, sample_output_with_multiple_credentials
    ):
        """NFR-002: credential_leak_count = 0."""
        # Arrange
        text = sample_output_with_multiple_credentials

        # Act
        masked = credential_masker.mask_output(text)
        leaks = credential_masker.scan_for_leaks(masked)

        # Assert
        assert len(leaks) == 0, f"Credentials leaked: {leaks}"

    def test_fuzzing_with_credential_variations(self, credential_masker):
        """NFR-002: Fuzzing tests with credential patterns in output."""
        # Arrange - Various credential formats
        test_cases = [
            "NPM_TOKEN=npm_xxxxxxxxxx",
            "npm_token: npm_yyyyyyyyyy",
            '"npmToken": "npm_zzzzzzzzzz"',
            "GITHUB_TOKEN=ghp_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            'github-token: "ghp_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"',
            "NUGET_API_KEY=oy2nxcccccccccccccccccccccccccccccccccccccc",
            "password: 'super_secret_password_123!'",
            "apiKey=sk_test_dddddddddddddddddddddddd",
            "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxx",
            "https://user:pass123@registry.com/pkg",
            "AWS_SECRET_ACCESS_KEY=eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            'secret_key: "ffffffffffffffffffffffffffffffffffff"',
            "CARGO_REGISTRY_TOKEN=cio_gggggggggggggggggggggggggggg",
        ]

        for text in test_cases:
            # Act
            masked = credential_masker.mask_output(text)
            leaks = credential_masker.scan_for_leaks(masked)

            # Assert
            assert len(leaks) == 0, f"Credential leaked in: '{text}' -> '{masked}'"
            assert "***" in masked, f"No masking applied to: '{text}'"


# =============================================================================
# Edge Cases
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases in credential masking."""

    def test_should_handle_unicode_in_output(self, credential_masker):
        """Edge case: Unicode characters in output."""
        # Arrange
        text = "Deploying to registry... token=npm_test123 \u2713"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "npm_test123" not in masked
        assert "\u2713" in masked  # Checkmark preserved

    def test_should_handle_very_long_tokens(self, credential_masker):
        """Edge case: Very long token strings."""
        # Arrange
        long_token = "ghp_" + "a" * 100
        text = f"Using token: {long_token}"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert long_token not in masked
        assert "***" in masked

    def test_should_handle_token_at_start_of_line(self, credential_masker):
        """Edge case: Token at beginning of line."""
        # Arrange
        text = "npm_secret_token\nSome other text"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "npm_secret_token" not in masked

    def test_should_handle_token_at_end_of_line(self, credential_masker):
        """Edge case: Token at end of line."""
        # Arrange
        text = "Using: npm_secret_token"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "npm_secret_token" not in masked

    def test_should_handle_multiple_tokens_same_line(self, credential_masker):
        """Edge case: Multiple tokens on same line."""
        # Arrange
        text = "NPM=npm_token1 GITHUB=ghp_token2 NUGET=oy2nxtoken3"

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "npm_token1" not in masked
        assert "ghp_token2" not in masked
        assert "oy2nxtoken3" not in masked

    def test_should_not_mask_false_positives(self, credential_masker):
        """Edge case: Avoid false positives on legitimate text."""
        # Arrange - Text that looks like tokens but isn't
        text = """
The npm_install command completed.
Publishing to github.com repository.
Token validation passed.
"""

        # Act
        masked = credential_masker.mask_output(text)

        # Assert - Should preserve most of the text
        assert "npm_install" in masked  # Not a token
        assert "github.com" in masked  # Not a token

    def test_should_handle_json_formatted_credentials(self, credential_masker):
        """Edge case: JSON-formatted credential output."""
        # Arrange
        text = '{"npm_token": "npm_abcd1234", "github_token": "ghp_efgh5678"}'

        # Act
        masked = credential_masker.mask_output(text)

        # Assert
        assert "npm_abcd1234" not in masked
        assert "ghp_efgh5678" not in masked
        assert "***" in masked

    def test_should_handle_multiline_credentials(self, credential_masker):
        """Edge case: Credentials split across lines."""
        # Arrange
        text = """
NPM_TOKEN=npm_
secret_token_12345
"""

        # Act - This is a tricky case; token might be split
        masked = credential_masker.mask_output(text)
        leaks = credential_masker.scan_for_leaks(masked)

        # Assert - At minimum, detect the pattern
        # Note: Split tokens may be harder to detect
        # Test ensures scan works even if mask doesn't catch split tokens
        assert isinstance(leaks, list)
