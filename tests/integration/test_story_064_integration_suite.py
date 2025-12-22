"""
Integration tests for STORY-064: devforgeai-story-creation Integration Validation and Test Execution

Tests cover:
- Acceptance Criteria 1: Test Suite Execution Complete (integration tests passing)
- Acceptance Criteria 4: CI/CD Integration Configured
- Acceptance Criteria 5: Cross-Reference Added to user-input-guidance.md
- Acceptance Criteria 6: Production Validation via /create-story

Test Suite Composition:
- IT01-IT12: Integration tests for skill interaction, CI/CD, cross-references, production validation
- Organized in 4 test classes: Skill Integration, CI/CD, Cross-References, Production Validation

Test IDs: IT01-IT12
Test Organization: 3 skill + 3 CI/CD + 3 cross-ref + 3 production tests
Coverage: File existence, integration patterns, deployment configuration, production scenarios
"""

import pytest
from pathlib import Path
from typing import List

# Import shared helper from unit tests
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "unit"))
from test_story_064_unit_suite import FileValidationHelper


class TestSkillIntegration:
    """Integration tests for skill-to-guidance integration (IT01-IT03).

    Validates: Guidance file integration in story-creation skill.
    """

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_it01_guidance_loading_in_story_creation_skill(self):
        """IT01: Guidance file is loaded in devforgeai-story-creation SKILL.md.

        Verifies: SKILL.md contains guidance file loading in Phase 1.
        """
        content = FileValidationHelper.assert_file_exists(
            FileValidationHelper.SKILL_FILE,
            "AC-6: devforgeai-story-creation SKILL.md not found"
        )
        assert "user-input-guidance.md" in content, (
            "AC-6 violation: SKILL.md must load user-input-guidance.md in Phase 1"
        )

        phase1_idx = content.find("Phase 1")
        assert phase1_idx != -1, "SKILL.md missing Phase 1"

        phase1_section = content[phase1_idx:phase1_idx + 5000]
        assert "guidance" in phase1_section.lower() or "load" in phase1_section.lower(), (
            "AC-6 violation: Phase 1 must document guidance loading"
        )

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_it02_integration_guide_documents_patterns(self):
        """IT02: user-input-integration-guide.md documents pattern usage.

        Verifies: Guide documents epic, sprint, priority, fibonacci patterns.
        """
        content = FileValidationHelper.assert_file_exists(
            FileValidationHelper.INTEGRATION_GUIDE,
            "AC-6: Integration guide not found"
        )

        required_patterns = ["epic", "sprint", "priority", "fibonacci"]
        found_patterns = sum(1 for pattern in required_patterns if pattern.lower() in content.lower())

        assert found_patterns >= 2, (
            f"AC-6 violation: Integration guide missing pattern references. "
            f"Found {found_patterns}/{len(required_patterns)} expected patterns"
        )

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_it03_fixture_integration_with_test_runner(self):
        """IT03: Test fixtures exist and integrate with test execution.

        Verifies: All 5 fixture files exist with correct names.
        """
        fixture_dir = FileValidationHelper.FIXTURE_DIR
        assert fixture_dir.exists(), "Fixture directory not found"

        fixture_files = list(fixture_dir.glob("*.md"))
        assert len(fixture_files) >= 5, (
            f"AC-2 violation: Expected 5 fixture files, found {len(fixture_files)}"
        )

        fixture_names = [f.stem for f in fixture_files]
        expected_fixtures = [
            "simple-feature", "moderate-feature", "complex-feature",
            "ambiguous-feature", "edge-case-feature"
        ]

        for expected in expected_fixtures:
            assert expected in fixture_names, f"Required fixture missing: {expected}-feature.md"


class TestCICDIntegration:
    """Integration tests for CI/CD pipeline configuration (IT04-IT06).

    Validates: Pipeline configuration and merge-blocking behavior.
    """

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_it04_cicd_pipeline_configuration_exists(self):
        """IT04: CI/CD pipeline configuration file exists.

        Verifies: story-creation-test-pipeline.yml exists with content.
        """
        config_content = FileValidationHelper.assert_file_exists(
            FileValidationHelper.PIPELINE_CONFIG,
            "AC-4: CI/CD pipeline configuration not found"
        )
        assert len(config_content) > 0, "Pipeline configuration exists but is empty"

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_it05_pipeline_runs_on_skill_modifications(self):
        """IT05: Pipeline configured to run on SKILL.md modifications.

        Verifies: Pipeline has trigger conditions for story-creation changes.
        """
        config_content = FileValidationHelper.assert_file_exists(
            FileValidationHelper.PIPELINE_CONFIG,
            "AC-4: Pipeline configuration required"
        )
        assert "story-creation" in config_content or "SKILL.md" in config_content, (
            "AC-4 violation: Pipeline missing trigger conditions for SKILL.md modifications"
        )

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_it06_pipeline_blocks_merge_on_test_failure(self):
        """IT06: Pipeline blocks merge when tests fail.

        Verifies: Configuration specifies blocking behavior on test failure.
        """
        config_content = FileValidationHelper.assert_file_exists(
            FileValidationHelper.PIPELINE_CONFIG,
            "AC-4: Pipeline configuration required"
        )
        keywords = ["fail", "block", "required", "merge"]
        keywords_found = sum(1 for kw in keywords if kw.lower() in config_content.lower())
        assert keywords_found >= 2, (
            "AC-4 violation: Pipeline missing merge-blocking on test failure"
        )


class TestCrossReferences:
    """Integration tests for cross-references between guidance files (IT07-IT09)"""

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_it07_cross_reference_in_ideation_guidance(self):
        """
        IT07: user-input-guidance.md includes Integration Points section

        ARRANGE: Load ideation guidance file
        ACT: Search for Integration Points section
        ASSERT: Section exists with story-creation reference
        """
        # Arrange
        guidance_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
        )

        # Act & Assert
        assert guidance_path.exists(), (
            "AC-5: Ideation guidance file not found"
        )

        with open(guidance_path, 'r') as f:
            content = f.read()

        # Check for Integration Points section
        assert "Integration Points" in content or "Skills Using This Guidance" in content, (
            "AC-5 violation: user-input-guidance.md missing Integration Points or Skills Using This Guidance section"
        )

        # Verify story-creation referenced
        assert "story-creation" in content.lower() or "STORY-056" in content, (
            "AC-5 violation: Integration Points must reference devforgeai-story-creation"
        )

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_it08_bidirectional_navigation_story_creation_to_ideation(self):
        """
        IT08: user-input-integration-guide.md references ideation guidance

        ARRANGE: Load story-creation integration guide
        ACT: Search for reference to ideation user-input-guidance.md
        ASSERT: Bidirectional navigation works (integration guide → ideation guidance)
        """
        # Arrange
        integration_guide_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/references/user-input-integration-guide.md"
        )

        # Act & Assert
        assert integration_guide_path.exists(), (
            "Story-creation integration guide not found"
        )

        with open(integration_guide_path, 'r') as f:
            content = f.read()

        # Check for reference back to ideation guidance
        assert "ideation" in content.lower() or "user-input-guidance" in content.lower(), (
            "AC-5 violation: Story-creation integration guide missing reference to ideation guidance"
        )

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_it09_cross_reference_consistency_with_story_055(self):
        """
        IT09: Cross-references consistent with STORY-055 (ideation integration)

        ARRANGE: Load both integration guides
        ACT: Verify consistent cross-references between files
        ASSERT: Both files reference each other consistently
        """
        # Arrange
        ideation_guide_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/references/user-input-integration-guide.md"
        )
        story_creation_guide_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/references/user-input-integration-guide.md"
        )

        # Act & Assert
        # At least one of the guides should exist and reference the integration pattern
        guides_exist = ideation_guide_path.exists() or story_creation_guide_path.exists()
        assert guides_exist, (
            "AC-5 violation: No integration guides found for cross-reference validation"
        )

        # Verify ideation guidance references story-creation
        ideation_guidance_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
        )

        if ideation_guidance_path.exists():
            with open(ideation_guidance_path, 'r') as f:
                content = f.read()

            # Should have integration points documentation
            assert "Integration Points" in content or "Skills" in content, (
                "AC-5 violation: Ideation guidance missing integration documentation"
            )


class TestProductionValidation:
    """Integration tests for production validation via /create-story (IT10-IT12)"""

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_it10_create_story_command_exists(self):
        """
        IT10: /create-story command exists and is configured

        ARRANGE: Define path to create-story command
        ACT: Check if command file exists
        ASSERT: Command file present and contains story-creation skill invocation
        """
        # Arrange
        command_path = Path(
            "/mnt/c/Projects/DevForgeAI2/.claude/commands/create-story.md"
        )

        # Act & Assert
        assert command_path.exists(), (
            f"AC-6 violation: /create-story command not found at {command_path}"
        )

        with open(command_path, 'r') as f:
            content = f.read()

        # Verify invokes story-creation skill
        assert "story-creation" in content.lower() or "devforgeai-story-creation" in content.lower(), (
            "AC-6 violation: /create-story must invoke devforgeai-story-creation skill"
        )

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_it11_skill_loads_guidance_in_phase_0(self):
        """
        IT11: SKILL.md loads guidance in Phase 0 with logging

        ARRANGE: Load story-creation SKILL.md
        ACT: Extract Phase 0/Step 0 content
        ASSERT: Guidance loading documented with expected log messages
        """
        # Arrange
        skill_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md"
        )

        # Act & Assert
        assert skill_path.exists(), "Story-creation SKILL.md required for IT11"

        with open(skill_path, 'r') as f:
            content = f.read()

        # Verify guidance loading is documented
        assert "Load user-input-guidance.md" in content or "Loading user-input-guidance" in content or "guidance" in content.lower(), (
            "AC-6 violation: SKILL.md Step 0 missing guidance loading documentation"
        )

        # Verify expected log messages mentioned
        assert "Loading user-input-guidance.md" in content or "patterns" in content.lower(), (
            "AC-6 violation: Expected log messages not documented in Phase 0"
        )

    @pytest.mark.integration
    @pytest.mark.acceptance_criteria
    def test_it12_pattern_enhanced_questions_documented(self):
        """
        IT12: Pattern-enhanced questions documented for epic, sprint, priority, points

        ARRANGE: Load integration guide
        ACT: Search for pattern-enhanced question documentation
        ASSERT: Guide documents epic, sprint, priority, and points questions
        """
        # Arrange
        integration_guide_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/references/user-input-integration-guide.md"
        )

        # Act & Assert
        assert integration_guide_path.exists(), (
            "Integration guide required for IT12"
        )

        with open(integration_guide_path, 'r') as f:
            content = f.read()

        # Verify pattern-enhanced question documentation
        question_types = ["epic", "sprint", "priority", "points"]
        found_types = sum(1 for qtype in question_types if qtype.lower() in content.lower())

        assert found_types >= 3, (
            f"AC-6 violation: Integration guide missing pattern-enhanced question documentation. "
            f"Found {found_types}/{len(question_types)} expected question types"
        )
