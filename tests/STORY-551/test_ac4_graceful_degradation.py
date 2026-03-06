"""
Test: AC#4 - Graceful Degradation When Profile Is Unavailable
Story: STORY-551
Generated: 2026-03-05

Verifies SKILL.md has fallback to "intermediate" defaults when profile
is unavailable, issues a non-blocking warning, and completes workflow
without error.
"""

import re


class TestIntermediateDefault:
    """Verify SKILL.md defaults to intermediate when profile absent."""

    def test_should_default_to_intermediate_pacing(self, skill_content):
        """SKILL.md must default to intermediate when no profile exists."""
        assert re.search(
            r'(?i)default.*intermediate',
            skill_content
        ), (
            "SKILL.md does not specify default to 'intermediate' pacing. "
            "AC#4: Must default to intermediate when profile unavailable."
        )

    def test_should_document_fallback_behavior(self, skill_content):
        """SKILL.md must document fallback/degradation behavior."""
        assert re.search(
            r'(?i)(graceful\s+degradation|fall\s*back|profile\s+unavailable|profile\s+absent)',
            skill_content
        ), (
            "SKILL.md missing graceful degradation documentation. "
            "AC#4: Must document behavior when profile is absent."
        )


class TestNonBlockingWarning:
    """Verify SKILL.md specifies non-blocking warning when profile absent."""

    def test_should_log_non_blocking_warning(self, skill_content):
        """SKILL.md must log a non-blocking warning when profile not found."""
        assert re.search(
            r'(?i)(non.blocking\s+warning|warning.*(?:not|without)\s+(?:halt|block|stop))',
            skill_content
        ), (
            "SKILL.md does not specify non-blocking warning for missing profile. "
            "AC#4: Must log warning without halting workflow."
        )

    def test_should_not_halt_on_missing_profile(self, skill_content):
        """SKILL.md must explicitly state no HALT for missing profile."""
        assert re.search(
            r'(?i)(do\s+not\s+halt|(?:not|never|no)\s+.*halt.*profile|continue.*without.*profile)',
            skill_content
        ), (
            "SKILL.md does not explicitly state that missing profile should not HALT."
        )


class TestWorkflowCompletion:
    """Verify SKILL.md confirms workflow completes without error when no profile."""

    def test_should_complete_workflow_without_profile(self, skill_content):
        """SKILL.md must confirm full workflow completes without profile."""
        assert re.search(
            r'(?i)(complete.*workflow|workflow.*complete|full.*projection).*(?:without|absent|missing)',
            skill_content,
            re.DOTALL
        ), (
            "SKILL.md does not confirm workflow completes when profile is absent. "
            "AC#4: Full financial projection workflow must complete without error."
        )


class TestEdgeCaseEC002IncompleteProjection:
    """EC-002: Incomplete/truncated projection data surfaces structured error."""

    def test_should_handle_incomplete_projection_data(self, skill_content):
        """SKILL.md must document behavior for incomplete projection data."""
        assert re.search(
            r'(?i)(incomplete|truncated|partial).*(?:projection|data|response)',
            skill_content
        ), (
            "EC-002: SKILL.md does not document handling of incomplete projection data."
        )

    def test_should_surface_structured_error(self, skill_content):
        """Incomplete data should surface a structured error, not partial results."""
        assert re.search(
            r'(?i)(structured\s+error|error.*structured|(?:not|never)\s+.*partial\s+data)',
            skill_content
        ), (
            "EC-002: Must surface structured error, not present partial data as complete."
        )


class TestEdgeCaseEC005NegativeInputs:
    """EC-005: Negative financial input values are rejected."""

    def test_should_validate_financial_inputs(self, skill_content):
        """SKILL.md must document input validation for financial values."""
        assert re.search(
            r'(?i)(validat|reject|negative).*(?:input|value|revenue|cost)',
            skill_content
        ), (
            "EC-005: SKILL.md does not document validation of financial inputs."
        )

    def test_should_reject_negative_values(self, skill_content):
        """Negative values must be rejected with AskUserQuestion."""
        assert re.search(
            r'(?i)(negative|zero\s+or\s+negative|less\s+than\s+zero).*(?:reject|invalid|AskUserQuestion)',
            skill_content,
            re.DOTALL
        ), (
            "EC-005: Negative financial values must be rejected via AskUserQuestion."
        )
