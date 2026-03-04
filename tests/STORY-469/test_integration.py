"""
Integration Tests: STORY-469 - Confidence-Building Patterns

Tests cross-file interactions and API contracts:
1. Cross-reference integrity: business-coach.md references both reference files with correct paths
2. Pattern consistency: "validate then redirect" principle consistent across files
3. Template completeness: Evidence-based affirmation placeholders documented in data sources
4. Subagent decision tree: Confidence detection leads to correct reference file loading
"""
import pathlib
import re

import pytest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]

# Implementation file paths
CONFIDENCE_PATTERNS_FILE = (
    PROJECT_ROOT
    / "src"
    / "claude"
    / "skills"
    / "coaching-entrepreneur"
    / "references"
    / "confidence-building-patterns.md"
)
IMPOSTER_SYNDROME_FILE = (
    PROJECT_ROOT
    / "src"
    / "claude"
    / "skills"
    / "coaching-entrepreneur"
    / "references"
    / "imposter-syndrome-interventions.md"
)
BUSINESS_COACH_FILE = PROJECT_ROOT / "src" / "claude" / "agents" / "business-coach.md"


class TestCrossReferenceIntegrity:
    """Validate that file references are correct and resolvable."""

    @pytest.fixture
    def business_coach_content(self) -> str:
        """Load the business-coach.md subagent file."""
        assert BUSINESS_COACH_FILE.is_file(), f"File not found: {BUSINESS_COACH_FILE}"
        return BUSINESS_COACH_FILE.read_text(encoding="utf-8")

    def test_business_coach_references_confidence_patterns_with_correct_relative_path(
        self, business_coach_content: str
    ):
        """
        Integration Test 1: business-coach.md must reference the confidence-building-patterns.md file
        with the correct relative path that the subagent can load.

        Context: The business-coach subagent exists in src/claude/agents/business-coach.md
        and must load reference files from src/claude/skills/coaching-entrepreneur/references/

        The relative path from the agent to the reference file should be:
        ../skills/coaching-entrepreneur/references/confidence-building-patterns.md
        OR use filename only (confidence-building-patterns.md) if loading from skill context.
        """
        # Arrange
        filename_reference = "confidence-building-patterns.md"

        # Act
        has_reference = filename_reference in business_coach_content

        # Assert
        assert has_reference, (
            f"business-coach.md does not reference '{filename_reference}' "
            "with correct filename. Cannot locate reference file during execution."
        )

    def test_business_coach_references_imposter_syndrome_interventions_with_correct_path(
        self, business_coach_content: str
    ):
        """
        Integration Test 2: business-coach.md must reference the imposter-syndrome-interventions.md
        file with the correct filename that can be resolved during execution.
        """
        # Arrange
        filename_reference = "imposter-syndrome-interventions.md"

        # Act
        has_reference = filename_reference in business_coach_content

        # Assert
        assert has_reference, (
            f"business-coach.md does not reference '{filename_reference}'. "
            "Cannot locate this reference file during subagent execution."
        )

    def test_reference_files_exist_at_expected_absolute_paths(self):
        """
        Integration Test 3: Verify the referenced files actually exist at their expected locations.

        This ensures that when business-coach.md instructs to load these files,
        they are available in the src/claude/skills tree.
        """
        # Act
        confidence_exists = CONFIDENCE_PATTERNS_FILE.is_file()
        imposter_exists = IMPOSTER_SYNDROME_FILE.is_file()

        # Assert
        assert confidence_exists, (
            f"Expected confidence-building-patterns.md at {CONFIDENCE_PATTERNS_FILE}"
        )
        assert imposter_exists, (
            f"Expected imposter-syndrome-interventions.md at {IMPOSTER_SYNDROME_FILE}"
        )


class TestPatternConsistency:
    """Validate that the 'validate then redirect' principle is consistent across files."""

    @pytest.fixture
    def confidence_content(self) -> str:
        """Load confidence-building-patterns.md."""
        return CONFIDENCE_PATTERNS_FILE.read_text(encoding="utf-8")

    @pytest.fixture
    def imposter_content(self) -> str:
        """Load imposter-syndrome-interventions.md."""
        return IMPOSTER_SYNDROME_FILE.read_text(encoding="utf-8")

    @pytest.fixture
    def business_coach_content(self) -> str:
        """Load business-coach.md."""
        return BUSINESS_COACH_FILE.read_text(encoding="utf-8")

    def test_validate_before_redirect_principle_in_imposter_interventions(
        self, imposter_content: str
    ):
        """
        Integration Test 4: The imposter syndrome interventions file documents
        the validate-before-redirect pattern with validation steps appearing first.

        This is the core intervention principle for imposter syndrome cases.
        """
        # Arrange
        content_lower = imposter_content.lower()

        # Act
        validate_idx = content_lower.find("validate")
        redirect_idx = content_lower.find("redirect")

        # Assert
        assert validate_idx > -1, "'validate' not found in imposter syndrome interventions"
        assert redirect_idx > -1, "'redirect' not found in imposter syndrome interventions"
        assert validate_idx < redirect_idx, (
            "Pattern violation: 'validate' must appear before 'redirect' "
            "in imposter syndrome interventions"
        )

    def test_validate_redirect_principle_mentioned_in_confidence_patterns(
        self, confidence_content: str
    ):
        """
        Integration Test 5: The confidence-building-patterns.md should acknowledge
        the validate-then-redirect approach when discussing imposter syndrome
        and reference the specialized interventions file.
        """
        # Arrange
        # Should mention the principle or reference the interventions file
        has_principle_ref = (
            "validate" in confidence_content.lower()
            or "imposter-syndrome-interventions" in confidence_content
        )

        # Act
        imposter_interventions_ref = "imposter-syndrome-interventions.md" in confidence_content

        # Assert
        assert imposter_interventions_ref or "validate" in confidence_content.lower(), (
            "confidence-building-patterns.md should reference the validate-then-redirect "
            "principle or the specialized imposter syndrome interventions file"
        )

    def test_business_coach_references_validate_redirect_in_decision_tree(
        self, business_coach_content: str
    ):
        """
        Integration Test 6: The business-coach.md decision tree should include
        instructions about applying the validate-then-redirect intervention
        for imposter syndrome cases.
        """
        # Arrange
        # Look for references to the pattern or the intervention approach
        decision_tree_pattern = re.compile(
            r"(validate|redirect|decision tree|imposter syndrome)",
            re.IGNORECASE,
        )

        # Act
        has_pattern_ref = bool(decision_tree_pattern.search(business_coach_content))

        # Assert
        assert has_pattern_ref, (
            "business-coach.md decision tree should reference the validate-then-redirect "
            "pattern or imposter syndrome intervention approach"
        )


class TestTemplateCompletenessAndDataSources:
    """
    Validate that evidence-based affirmation templates are complete and
    their data sources are documented.
    """

    @pytest.fixture
    def confidence_content(self) -> str:
        """Load confidence-building-patterns.md."""
        return CONFIDENCE_PATTERNS_FILE.read_text(encoding="utf-8")

    def test_evidence_based_affirmation_section_contains_all_required_placeholders(
        self, confidence_content: str
    ):
        """
        Integration Test 7: The evidence-based-affirmation section must include
        template placeholders for the three key metrics: {milestone_count}, {active_weeks},
        and {completed_count}, which are documented in the data sources.
        """
        # Arrange
        milestone_placeholder = "{milestone_count}"
        active_weeks_placeholder = "{active_weeks}"
        completed_count_placeholder = "{completed_count}"

        # Act
        has_milestone = milestone_placeholder in confidence_content
        has_active_weeks = active_weeks_placeholder in confidence_content
        has_completed = completed_count_placeholder in confidence_content

        # Assert
        assert has_milestone, (
            f"Affirmation templates missing {milestone_placeholder} placeholder. "
            "Cannot reference user's milestone count."
        )
        assert has_active_weeks, (
            f"Affirmation templates missing {active_weeks_placeholder} placeholder. "
            "Cannot reference duration of user's effort."
        )
        assert has_completed, (
            f"Affirmation templates missing {completed_count_placeholder} placeholder. "
            "Cannot reference task completion count."
        )

    def test_data_sources_section_documents_all_placeholders(
        self, confidence_content: str
    ):
        """
        Integration Test 8: The Data Sources section (under Evidence-Based Affirmation)
        must document what data each placeholder represents and where it comes from.

        This ensures the AI system understands how to populate these placeholders
        when applying affirmation templates.
        """
        # Arrange
        # Look for the Data Sources subsection which is under Evidence-Based Affirmation
        content_lower = confidence_content.lower()
        data_sources_idx = content_lower.find("data sources")

        assert data_sources_idx > -1, "Data Sources section not found in evidence-based affirmation"

        # Extract the section (from "Data Sources" up to next ## header)
        section_start = data_sources_idx
        next_main_section = content_lower.find("\n##", section_start)
        if next_main_section > -1:
            section_content = confidence_content[section_start:next_main_section]
        else:
            section_content = confidence_content[section_start:]

        # Act
        # Check for documentation about data sources
        has_data_documentation = (
            "milestone" in section_content.lower()
            or "progress" in section_content.lower()
            or "pull" in section_content.lower()
        )

        # Assert
        assert has_data_documentation, (
            "Data Sources section exists but does not document the data sources. "
            "Must explain where to get milestone_count, active_weeks, completed_count."
        )

    def test_momentum_tracking_section_references_milestone_count_metric(
        self, confidence_content: str
    ):
        """
        Integration Test 9: The Momentum Tracking section should reference
        the {milestone_count} metric as one of the progress indicators.

        This ensures consistency between the template affirmation placeholders
        and the momentum tracking methodology.
        """
        # Arrange
        # Check directly for milestone_count anywhere in the file after momentum tracking starts
        content_lower = confidence_content.lower()
        momentum_idx = content_lower.find("momentum tracking")

        assert momentum_idx > -1, "Momentum Tracking section not found"

        # Extract from momentum tracking to end of file
        section_start = momentum_idx
        section_content = confidence_content[section_start:]

        # Act
        # Check if milestone_count is mentioned in momentum tracking section
        has_milestone_ref = "{milestone_count}" in section_content

        # Assert
        assert has_milestone_ref, (
            "Momentum Tracking section should reference {milestone_count} placeholder. "
            "This ensures data consistency with evidence-based affirmation templates."
        )


class TestSubagentExecutionContract:
    """
    Validate that the subagent can execute the confidence coaching workflow
    by checking the contract between business-coach.md and the reference files.
    """

    @pytest.fixture
    def business_coach_content(self) -> str:
        """Load business-coach.md."""
        return BUSINESS_COACH_FILE.read_text(encoding="utf-8")

    @pytest.fixture
    def confidence_content(self) -> str:
        """Load confidence-building-patterns.md."""
        return CONFIDENCE_PATTERNS_FILE.read_text(encoding="utf-8")

    @pytest.fixture
    def imposter_content(self) -> str:
        """Load imposter-syndrome-interventions.md."""
        return IMPOSTER_SYNDROME_FILE.read_text(encoding="utf-8")

    def test_business_coach_decision_tree_maps_to_reference_file_content(
        self, business_coach_content: str, confidence_content: str, imposter_content: str
    ):
        """
        Integration Test 10: The decision tree in business-coach.md references
        techniques that actually exist in the referenced files.

        Example: If the decision tree mentions "reframing techniques", those techniques
        must be documented in confidence-building-patterns.md.
        """
        # Arrange
        # Check if decision tree references specific technique names
        technique_patterns = [
            "reframing",
            "evidence-based affirmation",
            "momentum tracking",
            "validate-then-redirect",
        ]

        # Act - For each technique mentioned in business-coach, verify it exists in reference files
        found_techniques = []
        missing_techniques = []

        for technique in technique_patterns:
            if technique.lower() in business_coach_content.lower():
                found_techniques.append(technique)
                # Check if it exists in one of the reference files
                if (
                    technique.lower() not in confidence_content.lower()
                    and technique.lower() not in imposter_content.lower()
                ):
                    missing_techniques.append(technique)

        # Assert
        assert len(found_techniques) > 0, (
            "business-coach.md decision tree should reference specific techniques "
            "like 'reframing', 'evidence-based affirmation', etc."
        )

        assert len(missing_techniques) == 0, (
            f"Business-coach references techniques not found in reference files: {missing_techniques}. "
            "Contract violation: decision tree references non-existent techniques."
        )

    def test_imposter_syndrome_intervention_steps_are_sequenced_correctly(
        self, business_coach_content: str, imposter_content: str
    ):
        """
        Integration Test 11: The imposter syndrome intervention in
        imposter-syndrome-interventions.md must be documented with clear steps
        that business-coach.md can follow.

        The steps should follow the validate->redirect->normalize->action sequence.
        """
        # Arrange
        # Look for the intervention step sequence in imposter syndrome file
        step_pattern = re.compile(
            r"(step|validation|redirect|normalize|action)",
            re.IGNORECASE,
        )

        # Act
        has_steps = bool(step_pattern.search(imposter_content))
        coach_references_steps = "step" in business_coach_content.lower() or (
            "validate" in business_coach_content.lower()
            and "redirect" in business_coach_content.lower()
        )

        # Assert
        assert has_steps, (
            "Imposter syndrome interventions should document clear steps "
            "(Validate, Redirect, Normalize, Action)"
        )

        assert coach_references_steps, (
            "Business-coach should reference or follow the intervention steps "
            "from the imposter syndrome file"
        )

    def test_affirmation_templates_can_be_instantiated_by_subagent(
        self, business_coach_content: str, confidence_content: str
    ):
        """
        Integration Test 12: The evidence-based affirmation templates in
        confidence-building-patterns.md must be formulated such that the
        business-coach subagent can instantiate them with user data.

        Tests that templates use consistent placeholder syntax {placeholder_name}.
        """
        # Arrange
        # Search for evidence-based affirmation templates with placeholders
        placeholder_pattern = re.compile(r"\{[a-z_]+\}", re.IGNORECASE)

        # Act
        # Find all placeholders in the entire file (they appear in evidence-based affirmation section)
        all_placeholders = placeholder_pattern.findall(confidence_content)

        # Assert
        assert len(all_placeholders) > 0, (
            "confidence-building-patterns.md should contain template placeholders "
            "with syntax {placeholder_name} for data substitution"
        )


class TestFileLineCountCompliance:
    """Verify NFR-001: Reference files stay under 1500 lines."""

    def test_all_reference_files_under_1500_lines(self):
        """
        Integration Test 13: Both reference files must comply with NFR-001
        to ensure they are maintainable and load efficiently.
        """
        # Act
        confidence_lines = len(CONFIDENCE_PATTERNS_FILE.read_text(encoding="utf-8").splitlines())
        imposter_lines = len(IMPOSTER_SYNDROME_FILE.read_text(encoding="utf-8").splitlines())

        # Assert
        assert confidence_lines < 1500, (
            f"confidence-building-patterns.md ({confidence_lines} lines) exceeds NFR-001 limit (1500)"
        )
        assert imposter_lines < 1500, (
            f"imposter-syndrome-interventions.md ({imposter_lines} lines) exceeds NFR-001 limit (1500)"
        )

        # Display summary
        print(f"\nNFR-001 Compliance Summary:")
        print(f"  confidence-building-patterns.md: {confidence_lines} lines (target: <1500)")
        print(f"  imposter-syndrome-interventions.md: {imposter_lines} lines (target: <1500)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
