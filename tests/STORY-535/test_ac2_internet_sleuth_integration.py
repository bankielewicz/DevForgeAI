"""
Test: AC#2 - Internet-Sleuth Integration for Market Data
Story: STORY-535
Generated: 2026-03-04

Validates that the skill invokes internet-sleuth subagent for market data
and incorporates at least 2 external data points with source attribution.

Tests target src/ tree per CLAUDE.md.
"""
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = PROJECT_ROOT / "src" / "claude" / "skills" / "researching-market"
SKILL_FILE = SKILL_DIR / "SKILL.md"


class TestInternetSleuthInvocation:
    """Tests that SKILL.md invokes internet-sleuth subagent."""

    def test_should_reference_internet_sleuth_subagent(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: internet-sleuth referenced."""
        content = SKILL_FILE.read_text()
        assert "internet-sleuth" in content.lower(), (
            "SKILL.md must reference the internet-sleuth subagent for market data gathering."
        )

    def test_should_invoke_internet_sleuth_via_task(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Task invocation pattern present."""
        content = SKILL_FILE.read_text()
        assert re.search(r"Task\s*\(|subagent.*internet-sleuth|internet-sleuth.*subagent", content, re.IGNORECASE), (
            "SKILL.md must invoke internet-sleuth via Task() subagent pattern."
        )


class TestExternalDataPoints:
    """Tests that at least 2 external data points are incorporated."""

    def test_should_require_minimum_two_data_points(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Minimum 2 data points required."""
        content = SKILL_FILE.read_text()
        assert re.search(r"(at least|minimum|>=?\s*)2.*data\s*point|2.*external.*source", content, re.IGNORECASE), (
            "SKILL.md must require at least 2 external data points from internet-sleuth."
        )


class TestSourceAttributionForExternalData:
    """Tests that external data points include source attribution."""

    def test_should_require_attribution_for_external_data(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Attribution requirement."""
        content = SKILL_FILE.read_text()
        assert re.search(r"source.*attribution|cite.*source|URL|report.*name", content, re.IGNORECASE), (
            "SKILL.md must require source attribution (URL, report name) for external data."
        )


class TestFermiFallback:
    """BR-003: Fallback to Fermi estimation when internet-sleuth fails."""

    def test_should_define_fermi_fallback_path(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Fermi fallback documented."""
        content = SKILL_FILE.read_text()
        assert re.search(r"fermi.*fallback|fallback.*fermi", content, re.IGNORECASE), (
            "SKILL.md must define Fermi estimation fallback when internet-sleuth fails (BR-003)."
        )

    def test_should_mark_low_confidence_on_fallback(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Low confidence on fallback."""
        content = SKILL_FILE.read_text()
        assert re.search(r"Low.*confidence|confidence.*Low", content, re.IGNORECASE), (
            "SKILL.md must mark confidence as Low when using Fermi fallback."
        )

    def test_should_have_fermi_estimation_reference_file(self):
        """Arrange: Skill directory exists. Act: Check path. Assert: fermi-estimation.md exists."""
        fermi_ref = SKILL_DIR / "references" / "fermi-estimation.md"
        assert fermi_ref.exists(), (
            f"references/fermi-estimation.md not found at {fermi_ref}. "
            "Fermi estimation guidance must be in a reference file."
        )


class TestMaxInternetSleuthInvocations:
    """NFR-002: Maximum 3 internet-sleuth invocations per workflow run."""

    def test_should_limit_internet_sleuth_calls(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Call limit documented."""
        content = SKILL_FILE.read_text()
        assert re.search(r"(max|maximum|limit|<=?\s*)3.*internet-sleuth|3.*invocation|3.*call", content, re.IGNORECASE), (
            "SKILL.md must limit internet-sleuth to maximum 3 invocations per run (NFR-002)."
        )
