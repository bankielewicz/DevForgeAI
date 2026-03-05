"""
Test: AC#4 - Overwrite Existing Output
Story: STORY-540
TDD Phase: Red (tests must FAIL before implementation)

Validates that positioning-strategy.md documents:
- Overwrite (not append) behavior for existing positioning.md
- Timestamp display for previous and new version
"""
import re
import pytest


class TestOverwriteBehavior:
    """Verify the reference documents overwrite-not-append semantics."""

    def test_should_document_overwrite_not_append(self, strategy_content):
        assert re.search(
            r"(?i)(overwrite|replac.*exist|not\s+append)",
            strategy_content,
        ), "Reference must document that existing positioning.md is overwritten, not appended"

    def test_should_document_full_content_replacement(self, strategy_content):
        assert re.search(
            r"(?i)(replac.*content|full.*replac|new.*content.*overwrit)",
            strategy_content,
        ), "Reference must document full content replacement on re-run"


class TestTimestampDisplay:
    """Verify the reference documents timestamp display for overwrite."""

    def test_should_document_previous_version_timestamp(self, strategy_content):
        assert re.search(
            r"(?i)(previous.*timestamp|old.*timestamp|prior.*version.*time|timestamp.*previous)",
            strategy_content,
        ), "Reference must document showing timestamp of previous version"

    def test_should_document_new_version_timestamp(self, strategy_content):
        assert re.search(
            r"(?i)(new.*timestamp|updated.*timestamp|current.*version.*time|timestamp.*new)",
            strategy_content,
        ), "Reference must document showing timestamp of new version"

    def test_should_document_user_notification_on_overwrite(self, strategy_content):
        assert re.search(
            r"(?i)(user.*shown.*message|notif.*update|confirm.*overwrite|message.*indicat.*update)",
            strategy_content,
        ), "Reference must document user notification message on overwrite"
