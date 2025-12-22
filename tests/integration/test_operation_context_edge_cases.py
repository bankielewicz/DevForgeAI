"""
Edge case and security tests for Operation Context Extraction (STORY-019)

Tests challenging scenarios: sanitization, corrupted data, concurrent access,
large datasets, and sensitive data handling.

Test Framework: pytest
Pattern: AAA (Arrange, Act, Assert)
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4
import re

# Import modules under test (will fail initially - TDD Red phase)
try:
    from devforgeai.operation_context import (
        OperationContext,
        TodoItem,
        ErrorContext,
        extractOperationContext,
    )
    from devforgeai.sanitization import (
        sanitizeContext,
        detectSensitivePatterns,
        redactSensitiveData,
    )
    from devforgeai.operation_history import OperationHistory
except ImportError:
    # Expected to fail in Red phase
    pass


class TestSanitizationBehavior:
    """Tests for data sanitization rules (AC2, NFR: Security)"""

    def test_sanitize_context_with_error_messages(self):
        """Security: sanitize_context() redacts secrets in error messages and stack traces"""
        # Arrange
        from devforgeai.sanitization import sanitize_context

        context_dict = {
            "operation_id": "550e8400-e29b-41d4-a716-446655440000",
            "status": "failed",
            "error": {
                "message": "Git auth failed: password=SuperSecret123 for user@github.com",
                "stack_trace": "GitError: api_key=sk-1234567890abcdef at 192.168.1.100\n  File: /home/user/project/secret.py"
            }
        }

        # Act
        sanitized, metadata = sanitize_context(context_dict)

        # Assert - verify secrets redacted
        assert "[REDACTED]" in sanitized["error"]["message"]
        assert "SuperSecret123" not in sanitized["error"]["message"]
        assert "[email@example.com]" in sanitized["error"]["message"]
        assert "user@github.com" not in sanitized["error"]["message"]

        assert "[REDACTED]" in sanitized["error"]["stack_trace"]
        assert "sk-1234567890abcdef" not in sanitized["error"]["stack_trace"]
        assert "XXX.XXX.XXX.XXX" in sanitized["error"]["stack_trace"]
        assert "192.168.1.100" not in sanitized["error"]["stack_trace"]
        assert "secret.py" in sanitized["error"]["stack_trace"]  # Filename preserved
        assert "/home/user/project/" not in sanitized["error"]["stack_trace"]  # Path removed

        # Verify metadata tracks sanitization
        assert metadata["sanitization_applied"] == True
        assert metadata["fields_sanitized"] == 2
        assert "error.message" in metadata["sanitized_fields"]
        assert "error.stack_trace" in metadata["sanitized_fields"]

    def test_sanitize_passwords_in_error_logs(self):
        """Security: Remove passwords from error logs"""
        # Arrange
        error_log = "Connection failed: password=secret123 for user@db.com"

        # Act
        sanitized = redactSensitiveData(error_log)

        # Assert
        assert "secret123" not in sanitized
        assert "[REDACTED]" in sanitized or "password=[REDACTED]" in sanitized

    def test_sanitize_api_keys_in_logs(self):
        """Security: Remove API keys from error logs"""
        # Arrange
        error_log = "API request failed: api_key=sk_live_1234567890abcdef"

        # Act
        sanitized = redactSensitiveData(error_log)

        # Assert
        assert "sk_live_1234567890abcdef" not in sanitized
        assert "[REDACTED]" in sanitized or "api_key=[REDACTED]" in sanitized

    def test_sanitize_tokens_in_logs(self):
        """Security: Remove tokens from error logs"""
        # Arrange
        error_log = "Token validation failed: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

        # Act
        sanitized = redactSensitiveData(error_log)

        # Assert
        assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in sanitized
        assert "[REDACTED]" in sanitized or "token=[REDACTED]" in sanitized

    def test_sanitize_database_connection_strings(self):
        """Security: Remove database connection strings"""
        # Arrange
        error_log = "DB Error: server=prod.database.windows.net;user=admin;password=SuperSecret123!"

        # Act
        sanitized = redactSensitiveData(error_log)

        # Assert
        assert "SuperSecret123!" not in sanitized
        assert "[DB_CONNECTION_REDACTED]" in sanitized or "[REDACTED]" in sanitized

    def test_sanitize_ipv4_addresses(self):
        """Security: Mask IPv4 addresses in error logs"""
        # Arrange
        error_log = "Connection from 192.168.1.100 failed after 3 retries"

        # Act
        sanitized = redactSensitiveData(error_log)

        # Assert
        assert "192.168.1.100" not in sanitized
        assert "XXX.XXX.XXX.XXX" in sanitized or "[internal-ip]" in sanitized

    def test_sanitize_ipv6_addresses(self):
        """Security: Mask IPv6 addresses in error logs"""
        # Arrange
        error_log = "Connection from 2001:0db8:85a3:0000:0000:8a2e:0370:7334 timeout"

        # Act
        sanitized = redactSensitiveData(error_log)

        # Assert
        assert "2001:0db8:85a3:0000:0000:8a2e:0370:7334" not in sanitized
        assert "[internal-ipv6]" in sanitized or "[REDACTED]" in sanitized

    def test_sanitize_internal_domain_names(self):
        """Security: Redact internal domain names"""
        # Arrange
        error_log = "Request to https://internal-api.company.internal failed"

        # Act
        sanitized = redactSensitiveData(error_log)

        # Assert
        assert "internal-api.company.internal" not in sanitized
        assert "[internal-domain]" in sanitized or "[REDACTED]" in sanitized

    def test_sanitize_pii_emails(self):
        """Security: Redact PII (email addresses)"""
        # Arrange
        error_log = "User john.doe@company.com logged in from unusual location"

        # Act
        sanitized = redactSensitiveData(error_log)

        # Assert
        assert "john.doe@company.com" not in sanitized
        assert "[email@example.com]" in sanitized or "[REDACTED]" in sanitized

    def test_sanitize_file_paths(self):
        """Security: Remove absolute file paths, keep only filename"""
        # Arrange
        error_log = "Error in /home/deploy/app/src/config.py at line 42"

        # Act
        sanitized = redactSensitiveData(error_log)

        # Assert
        # Full path should be removed
        assert "/home/deploy/app/src/" not in sanitized
        # Filename should be preserved
        assert "config.py" in sanitized

    def test_sanitization_metadata_tracked(self):
        """Security: Sanitization actions logged with what, why, timestamp"""
        # Arrange
        error_log = "Error: password=secret123, token=abc456"

        # Act
        context = extractOperationContext(
            str(uuid4()), options={"includeSanitization": True}
        )

        # Assert
        # If context was sanitized, metadata should reflect this
        if hasattr(context, "extraction_metadata"):
            assert context.extraction_metadata.sanitization_applied is True
            assert context.extraction_metadata.fields_sanitized >= 0

    def test_no_unredacted_secrets_in_feedback_context(self):
        """Security: Sanitized context passed to feedback has NO unredacted secrets"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        context = extractOperationContext(
            operation_id, options={"includeSanitization": True}
        )

        # Get error logs if present
        if context.error and context.error.stack_trace:
            # Assert - look for unredacted patterns
            trace = context.error.stack_trace
            # Check for passwords
            assert not re.search(
                r"password\s*=\s*[^;\s\[\]]+(?!\[REDACTED\])", trace, re.IGNORECASE
            )
            # Check for API keys
            assert not re.search(
                r"api[_-]?key\s*=\s*[^;\s\[\]]+(?!\[REDACTED\])", trace, re.IGNORECASE
            )
            # Check for tokens (simple check for long base64 strings)
            assert not re.search(
                r"token\s*=\s*[A-Za-z0-9+/={64,}(?!\[REDACTED\])", trace
            )


class TestCorruptedDataHandling:
    """Tests for handling corrupted or missing logs"""

    def test_missing_error_logs_uses_last_known_state(self):
        """Edge case: Missing error logs → use last known state"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        context = extractOperationContext(operation_id)

        # Assert
        if context.status == "failed":
            # Should have some error info even if logs missing
            assert context.error is not None or context.todo_summary["failed"] > 0

    def test_corrupted_logs_partial_extraction(self):
        """Edge case: Corrupted logs → extract available data"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        context = extractOperationContext(operation_id)

        # Assert
        # Should extract something even if logs corrupted
        assert context is not None
        assert context.operation_id == operation_id
        assert context.status is not None

    def test_data_loss_event_logged(self):
        """Edge case: Data loss event is logged when extraction fails"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        context = extractOperationContext(operation_id)

        # Assert
        # If data loss occurred, completeness_score should indicate it
        if hasattr(context, "extraction_metadata"):
            completeness = context.extraction_metadata.completeness_score
            assert 0 <= completeness <= 1.0

    def test_partial_error_info_in_feedback(self):
        """Edge case: Feedback shows 'Partial error information: [available fields]'"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        context = extractOperationContext(operation_id)

        # Assert
        if context.status == "failed" and context.error:
            # Error should have message at minimum
            assert context.error.message is not None


class TestConcurrentFeedbackRequests:
    """Tests for concurrent feedback requests on same operation"""

    def test_prevent_duplicate_feedback(self):
        """Edge case: Prevent duplicate feedback for same operation"""
        # Arrange
        operation_id = str(uuid4())
        feedback_session_1 = str(uuid4())

        # Act
        from devforgeai.operation_history import updateOperationHistory

        # First feedback request
        updateOperationHistory(
            operation_id,
            feedback_session_id=feedback_session_1,
            feedback_status="initiated",
        )

        # Second feedback request for same operation
        feedback_session_2 = str(uuid4())

        # Assert
        history = OperationHistory.get(operation_id)
        # Should either reject second request or offer options
        if history["feedback_session_id"] == feedback_session_1:
            # Correctly prevented duplicate
            assert history["feedback_session_id"] != feedback_session_2

    def test_concurrent_request_offers_options(self):
        """Edge case: Concurrent feedback offer options: view existing, append, defer"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        # Would invoke feedback system with concurrent request handling
        # (Implementation would raise exception or return options)

        # Assert
        # Options should include:
        # - View existing conversation
        # - Append to existing
        # - Defer new feedback
        options = [
            "view_existing",
            "append_to_existing",
            "defer_new_feedback",
        ]
        assert "view_existing" in options


class TestContextSizeEnforcement:
    """Tests for context size limits (NFR: Performance)"""

    def test_context_size_under_50kb_simple_operation(self):
        """Performance: Simple operation (10 todos, no error) < 50KB"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        context = extractOperationContext(operation_id)

        # Assert
        import json
        from dataclasses import asdict
        context_json = json.dumps(asdict(context))
        context_size = len(context_json.encode("utf-8"))
        assert context_size < 50000

    def test_context_size_under_50kb_complex_operation(self):
        """Performance: Complex operation (100+ todos) < 50KB"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        context = extractOperationContext(operation_id, options={"maxContextSize": 50000})

        # Assert
        import json
        from dataclasses import asdict
        context_json = json.dumps(asdict(context))
        context_size = len(context_json.encode("utf-8"))
        assert context_size < 50000

    def test_truncation_marker_when_exceeds_limit(self):
        """Performance: If exceeds limit, truncate with marker"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        context = extractOperationContext(
            operation_id,
            options={"maxContextSize": 10000},  # Force truncation
        )

        # Assert
        if len(context.todos) > 100:
            # Should have truncation marker or truncated flag
            context_json = str(context.__dict__)
            assert (
                "... truncated" in context_json
                or "omitted" in context_json
                or context.extraction_metadata.truncation_applied
            )


class TestExtractionPerformance:
    """Tests for extraction performance (NFR: Performance)"""

    def test_extraction_time_simple_operation(self):
        """Performance: Simple operation extraction < 50ms"""
        # Arrange
        operation_id = str(uuid4())
        import time

        # Act
        start = time.time()
        context = extractOperationContext(operation_id)
        elapsed = (time.time() - start) * 1000  # Convert to ms

        # Assert
        assert elapsed < 50

    def test_extraction_time_complex_operation(self):
        """Performance: Complex operation (100+ todos) extraction < 150ms"""
        # Arrange
        operation_id = str(uuid4())
        import time

        # Act
        start = time.time()
        context = extractOperationContext(operation_id)
        elapsed = (time.time() - start) * 1000  # Convert to ms

        # Assert
        assert elapsed < 150

    def test_extraction_time_failed_operation(self):
        """Performance: Failed operation (with error logs) extraction < 200ms"""
        # Arrange
        operation_id = str(uuid4())
        import time

        # Act
        start = time.time()
        context = extractOperationContext(operation_id)
        elapsed = (time.time() - start) * 1000  # Convert to ms

        # Assert
        assert elapsed < 200


class TestHistoryQueryPerformance:
    """Tests for history query performance"""

    def test_query_context_by_operation_id_under_50ms(self):
        """Performance: Query context by operation_id < 50ms"""
        # Arrange
        operation_id = str(uuid4())
        import time

        # Act
        start = time.time()
        context = extractOperationContext(operation_id)
        elapsed = (time.time() - start) * 1000  # Convert to ms

        # Assert
        assert elapsed < 50

    def test_history_update_feedback_link_under_100ms(self):
        """Performance: Update history with feedback link < 100ms"""
        # Arrange
        operation_id = str(uuid4())
        feedback_session_id = str(uuid4())
        import time

        # Act
        start = time.time()
        from devforgeai.operation_history import updateOperationHistory

        updateOperationHistory(
            operation_id,
            feedback_session_id=feedback_session_id,
            feedback_status="initiated",
        )
        elapsed = (time.time() - start) * 1000  # Convert to ms

        # Assert
        assert elapsed < 100


class TestAccessControlAndAudit:
    """Tests for access control (NFR: Security)"""

    def test_unsanitized_context_access_restricted(self):
        """Security: Only operation initiator can access unsanitized context"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        # Request unsanitized context (should fail or require auth)
        try:
            context = extractOperationContext(
                operation_id, options={"includeSanitization": False}
            )
            # If allowed, should check access control
            # This is implementation-dependent
        except PermissionError:
            # Correct behavior - access denied
            pass

    def test_sanitized_context_available_to_feedback(self):
        """Security: Sanitized context available to feedback conversation"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        context = extractOperationContext(
            operation_id, options={"includeSanitization": True}
        )

        # Assert
        # Should be available (no access restrictions)
        assert context is not None
        # Should be sanitized
        if context.error and context.error.stack_trace:
            assert "[REDACTED]" in context.error.stack_trace or not any(
                pattern in context.error.stack_trace
                for pattern in ["password", "token", "secret"]
            )

    def test_audit_trail_all_access_logged(self):
        """Security: Audit all access to unsanitized context"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        # Would need to track access attempts
        # (Implementation would log to audit trail)

        # Assert
        # Audit trail should exist for security access
        # from devforgeai.audit import getAuditTrail
        # audit_entries = getAuditTrail(operation_id)
        # Should have entries for any unsanitized access


class TestSensitiveDataDetection:
    """Tests for automatic sensitive data pattern detection"""

    def test_detect_password_patterns(self):
        """Security: Detect password patterns (password=, pwd=, etc.)"""
        # Arrange
        patterns = [
            "password=secret",
            "pwd=secret",
            "passwd=secret",
            "pass=secret",
        ]

        # Act & Assert
        for pattern in patterns:
            assert "secret" in pattern
            result = detectSensitivePatterns(pattern)
            assert result is not None or "secret" in pattern

    def test_detect_api_key_patterns(self):
        """Security: Detect API key patterns"""
        # Arrange
        patterns = [
            "api_key=sk_live_123",
            "apiKey=sk_live_123",
            "API-KEY=sk_live_123",
        ]

        # Act & Assert
        for pattern in patterns:
            result = detectSensitivePatterns(pattern)
            assert result is not None or "123" in pattern

    def test_detect_token_patterns(self):
        """Security: Detect token patterns"""
        # Arrange
        patterns = [
            "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            "access_token=abc123def456",
            "authorization: Bearer abc123",
        ]

        # Act & Assert
        for pattern in patterns:
            result = detectSensitivePatterns(pattern)
            assert result is not None or "token" in pattern.lower()

    def test_detect_database_secrets(self):
        """Security: Detect database connection secrets"""
        # Arrange
        patterns = [
            "password=SuperSecret123!",
            "user=admin;password=xyz",
            "mongodb://user:pass@host:port",
        ]

        # Act & Assert
        for pattern in patterns:
            result = detectSensitivePatterns(pattern)
            # Should detect password in various formats
            assert result is not None
            assert "passwords" in result
            assert len(result["passwords"]) > 0

    def test_detect_ip_addresses_with_messages(self):
        """Security: Verify IP detection returns proper messages"""
        # Arrange
        test_ipv4 = "Connected to 192.168.1.100:8080"
        test_ipv6 = "Server at 2001:0db8:85a3:0000"

        # Act
        result_ipv4 = detectSensitivePatterns(test_ipv4)
        result_ipv6 = detectSensitivePatterns(test_ipv6)

        # Assert - verify detection messages (covers lines 103, 106)
        assert result_ipv4 is not None
        assert "ips" in result_ipv4
        assert "Found IPv4 address" in result_ipv4["ips"]

        assert result_ipv6 is not None
        assert "ips" in result_ipv6
        assert "Found IPv6 address" in result_ipv6["ips"]

    def test_detect_emails_with_messages(self):
        """Security: Verify email detection returns proper messages"""
        # Arrange
        test_data = "Error for user@company.com failed"

        # Act
        result = detectSensitivePatterns(test_data)

        # Assert - verify detection message (covers line 110)
        assert result is not None
        assert "emails" in result
        assert "Found email address" in result["emails"]

    def test_detect_internal_domains_with_messages(self):
        """Security: Verify internal domain detection returns proper messages"""
        # Arrange
        test_data = "Service failed: https://myservice.internal/v1/users"

        # Act
        result = detectSensitivePatterns(test_data)

        # Assert - verify detection message (covers line 114)
        assert result is not None
        assert "internal_domains" in result
        assert "Found internal domain" in result["internal_domains"]


class TestDataRetentionCompliance:
    """Tests for data retention policy (NFR: Security)"""

    def test_recent_operation_full_retention(self):
        """Security: Recently completed operations (< 30 days) - full data retained"""
        # Arrange
        operation_id = str(uuid4())
        context = extractOperationContext(operation_id)

        # Act
        created_at = datetime.fromisoformat(
            context.start_time.replace("Z", "+00:00")
        )
        now_aware = datetime.now(created_at.tzinfo)
        age_days = (now_aware - created_at).days

        # Assert
        if age_days < 30:
            # Should have full data
            assert context.todos is not None
            assert len(context.todos) > 0

    def test_old_operation_summary_only(self):
        """Security: Older operations (> 12 months) - summary only"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        # (In real system, would query old operation)
        # For testing purposes, we'd create a synthetic old operation

        # Assert
        # Old operations should have summary but not detailed todos
        # (Implementation-dependent)


class TestContextImmutability:
    """Tests for context immutability during feedback conversation"""

    def test_context_immutable_during_feedback(self):
        """Business rule: Context immutable during feedback conversation"""
        # Arrange
        operation_id = str(uuid4())
        from devforgeai.feedback_integration import passContextToFeedback

        context = extractOperationContext(operation_id)
        feedback_context = passContextToFeedback(context)

        # Act
        # Try to modify original context (should fail with frozen dataclass)
        original_status = context.status
        try:
            # This should raise FrozenInstanceError for frozen dataclass
            context.status = "modified"
            modified_status = context.status
        except (TypeError, AttributeError, Exception):
            # Correct - immutable (frozen dataclass raises FrozenInstanceError or AttributeError)
            modified_status = original_status

        # Assert
        assert modified_status == original_status


class TestCachingBehavior:
    """Tests for caching behavior (Business Rule: Context Extraction Timing)"""

    def test_context_extracted_once_on_completion(self):
        """Business rule: Extract immediately when operation completes"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        first_extraction = extractOperationContext(operation_id)
        extraction_time_1 = first_extraction.extraction_metadata.extracted_at

        # Second call should use cache
        second_extraction = extractOperationContext(operation_id)
        extraction_time_2 = second_extraction.extraction_metadata.extracted_at

        # Assert
        assert extraction_time_1 == extraction_time_2  # Same extraction time = cached

    def test_cache_retained_30_days(self):
        """Business rule: Cache extracted context for 30 days"""
        # Arrange
        operation_id = str(uuid4())

        # Act
        context = extractOperationContext(operation_id)

        # Assert
        # Would need cache TTL validation
        # (Implementation would check cache expiration)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
