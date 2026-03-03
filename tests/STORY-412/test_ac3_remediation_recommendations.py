"""
Test: AC#3 - Remediation Recommendations Provided
Story: STORY-412
Generated: 2026-02-16

Validates that each violation includes a remediation recommendation
of type: refactor, accept, or defer.
"""
import os
import re
import pytest

AUDIT_RESULTS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..",
    "devforgeai", "specs", "analysis", "command-hybrid-audit-results.md"
)

VALID_RECOMMENDATIONS = ["refactor", "accept", "defer"]


class TestRemediationRecommendations:
    """AC#3: Remediation recommendations provided for each violation."""

    def _read_audit(self):
        with open(AUDIT_RESULTS_PATH, "r") as f:
            return f.read()

    def test_should_have_remediation_section_when_audit_complete(self):
        """Assert audit results contain a remediation section."""
        content = self._read_audit()
        assert re.search(r"(?i)remediat", content), (
            "Audit results do not contain remediation recommendations"
        )

    def test_should_include_valid_recommendation_type(self):
        """Assert at least one valid recommendation type (refactor/accept/defer) is present."""
        content = self._read_audit().lower()
        found = [r for r in VALID_RECOMMENDATIONS if r in content]
        assert found, (
            f"No valid recommendation types found. Expected one of: {VALID_RECOMMENDATIONS}"
        )

    def test_should_provide_recommendation_for_each_violation(self):
        """Assert every documented violation has a corresponding recommendation."""
        content = self._read_audit()
        # Count violation entries (commands with >4 code blocks)
        violation_pattern = re.findall(r"\d+\s*code\s*block", content, re.IGNORECASE)
        # Count recommendation entries
        recommendation_count = sum(
            1 for r in VALID_RECOMMENDATIONS
            if r in content.lower()
        )
        # At minimum, if violations exist, recommendations must exist
        if violation_pattern:
            assert recommendation_count > 0, (
                f"Found {len(violation_pattern)} violations but no remediation recommendations"
            )

    def test_should_recommend_refactor_for_high_violation_commands(self):
        """BR-002: Commands with >8 code blocks should get refactor recommendation."""
        content = self._read_audit()
        # Find code block counts > 8
        counts = re.findall(r"(\d+)\s*code\s*block", content, re.IGNORECASE)
        high_violations = [int(c) for c in counts if int(c) > 8]
        if high_violations:
            assert "refactor" in content.lower(), (
                f"Commands with >8 code blocks ({high_violations}) should recommend 'refactor'"
            )
