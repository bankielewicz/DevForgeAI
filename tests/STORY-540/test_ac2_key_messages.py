"""
Test: AC#2 - Key Messages Generation
Story: STORY-540
TDD Phase: Red (tests must FAIL before implementation)

Validates that positioning-strategy.md documents key message generation
rules: 3-5 messages, <=50 words each, mapped to named audience segments.
"""
import re
import pytest


# ---------------------------------------------------------------------------
# BR-002: Key messages count 3-5, each <= 50 words
# ---------------------------------------------------------------------------

class TestKeyMessageCountRules:
    """Verify the reference file documents message count constraints."""

    def test_should_document_minimum_3_messages_rule(self, strategy_content):
        # Must mention the minimum of 3 messages
        assert re.search(r"(?i)(3\s*(to|-)\s*5|minimum.*3|at\s+least\s+3)", strategy_content), (
            "Reference must document minimum of 3 key messages"
        )

    def test_should_document_maximum_5_messages_rule(self, strategy_content):
        assert re.search(r"(?i)(3\s*(to|-)\s*5|maximum.*5|up\s+to\s+5|no\s+more\s+than\s+5)", strategy_content), (
            "Reference must document maximum of 5 key messages"
        )

    def test_should_document_50_word_limit_per_message(self, strategy_content):
        assert re.search(r"(?i)(50\s*word|<=\s*50|50\s*-?\s*word\s*limit)", strategy_content), (
            "Reference must document 50-word limit per key message"
        )


# ---------------------------------------------------------------------------
# Audience segment mapping
# ---------------------------------------------------------------------------

class TestAudienceSegmentMapping:
    """Verify messages are mapped to named audience segments."""

    def test_should_document_segment_subsection_format(self, strategy_content):
        # AC says: ### Segment: [Name]
        assert re.search(
            r"###\s+Segment:\s*\[", strategy_content
        ), "Reference must document '### Segment: [Name]' subsection format"

    def test_should_reference_key_messages_section_header(self, strategy_content):
        assert re.search(
            r"##\s+Key\s+Messages", strategy_content
        ), "Reference must document '## Key Messages' output section"


# ---------------------------------------------------------------------------
# BR-003: Empty audience input blocks workflow
# ---------------------------------------------------------------------------

class TestEmptyAudienceValidation:
    """Verify the reference documents empty audience input validation."""

    def test_should_document_empty_audience_validation_error(self, strategy_content):
        assert re.search(
            r"(?i)(empty.*audience.*error|audience.*empty.*block|validation.*error.*audience)",
            strategy_content,
        ), "Reference must document that empty audience input produces a validation error"

    def test_should_document_no_partial_output_on_empty_audience(self, strategy_content):
        assert re.search(
            r"(?i)(no\s+partial\s+output|no\s+output.*written|block.*workflow)",
            strategy_content,
        ), "Reference must document that no output is written when audience is empty"


# ---------------------------------------------------------------------------
# BR-004: >5 audience segments truncated to first 5 alphabetically
# ---------------------------------------------------------------------------

class TestSegmentTruncation:
    """Verify the reference documents truncation rules."""

    def test_should_document_truncation_to_5_segments(self, strategy_content):
        assert re.search(
            r"(?i)(truncat.*5|first\s+5\s+alphabetically|limit.*5\s+segment)",
            strategy_content,
        ), "Reference must document truncation to first 5 segments alphabetically"

    def test_should_document_truncation_notification(self, strategy_content):
        assert re.search(
            r"(?i)(notif.*omit|warn.*truncat|user.*notif.*segment)",
            strategy_content,
        ), "Reference must document user notification of truncated segments"


# ---------------------------------------------------------------------------
# BR-005: Duplicate segment names (case-insensitive) deduplicated
# ---------------------------------------------------------------------------

class TestSegmentDeduplication:
    """Verify the reference documents deduplication rules."""

    def test_should_document_case_insensitive_deduplication(self, strategy_content):
        assert re.search(
            r"(?i)(case.insensitive.*dedup|dedup.*case.insensitive|duplicate.*segment)",
            strategy_content,
        ), "Reference must document case-insensitive deduplication of segment names"

    def test_should_document_first_occurrence_retention(self, strategy_content):
        assert re.search(
            r"(?i)(first\s+occurrence|retain.*first|keep.*first)",
            strategy_content,
        ), "Reference must document that first occurrence is retained on deduplication"
