"""
Test: AC#5 - Partial Progress Persistence
Story: STORY-542
Generated: 2026-03-06

Validates:
- Contains discovery-state file save mechanism
- Detects partial state on re-invocation
- Offers resume from last step or restart
- NFR-001: Corrupted state file falls back to clean start
"""
import os
import re

import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCE_FILE = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "marketing-business",
    "references", "customer-discovery-workflow.md"
)


@pytest.fixture
def source_content():
    """Arrange: Read source file content."""
    assert os.path.isfile(SOURCE_FILE), f"Source file not found: {SOURCE_FILE}"
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        return f.read()


class TestStateSaveMechanism:
    """Tests for discovery-state file save."""

    def test_should_contain_state_file_reference(self, source_content):
        """Act & Assert: File must reference a discovery-state file."""
        content_lower = source_content.lower()
        has_state_file = (
            "discovery-state" in content_lower
            or "discovery_state" in content_lower
            or "state file" in content_lower
        )
        assert has_state_file, (
            "Source file must reference a discovery-state file for persistence"
        )

    def test_should_describe_save_on_exit(self, source_content):
        """Act & Assert: File must describe saving state on workflow exit."""
        content_lower = source_content.lower()
        has_save = (
            "save" in content_lower
            and ("exit" in content_lower or "partial" in content_lower or "progress" in content_lower)
        )
        assert has_save, (
            "Source file must describe saving state on exit"
        )


class TestPartialStateDetection:
    """Tests for detecting partial state on re-invocation."""

    def test_should_detect_partial_state(self, source_content):
        """Act & Assert: File must detect existing partial state on re-invocation."""
        content_lower = source_content.lower()
        has_detect = (
            "detect" in content_lower or "check" in content_lower or "exists" in content_lower
        ) and (
            "state" in content_lower or "progress" in content_lower
        )
        assert has_detect, (
            "Source file must detect partial state on re-invocation"
        )

    def test_should_offer_resume_option(self, source_content):
        """Act & Assert: File must offer resume from last step."""
        content_lower = source_content.lower()
        has_resume = "resume" in content_lower
        assert has_resume, (
            "Source file must offer resume from last step"
        )

    def test_should_offer_restart_option(self, source_content):
        """Act & Assert: File must offer restart from beginning."""
        content_lower = source_content.lower()
        has_restart = "restart" in content_lower or "start over" in content_lower or "fresh start" in content_lower
        assert has_restart, (
            "Source file must offer restart from beginning"
        )


class TestCorruptedStateFallback:
    """Tests for NFR-001: Corrupted state file falls back to clean start."""

    def test_should_handle_corrupted_state_nfr001(self, source_content):
        """Act & Assert: NFR-001 - Corrupted state file must fall back to clean start."""
        content_lower = source_content.lower()
        has_corrupt_handling = (
            "corrupt" in content_lower
            and ("clean" in content_lower or "fresh" in content_lower or "fallback" in content_lower)
        )
        assert has_corrupt_handling, (
            "Source file must handle corrupted state file with clean start fallback (NFR-001)"
        )

    def test_should_warn_on_corrupted_state_nfr001(self, source_content):
        """Act & Assert: NFR-001 - Corrupted state must produce a warning."""
        content_lower = source_content.lower()
        has_warning = (
            "corrupt" in content_lower
            and ("warn" in content_lower or "log" in content_lower or "message" in content_lower)
        )
        assert has_warning, (
            "Source file must warn/log when corrupted state detected (NFR-001)"
        )
