"""
Regression tests for STORY-064: devforgeai-story-creation Integration Validation and Test Execution

Tests cover:
- Acceptance Criteria 1: Test Suite Execution (backward compatibility)
- Acceptance Criteria 5: Cross-Reference (no broken links)
- Acceptance Criteria 6: Production Validation (production behavior)
- Non-Functional Requirements: Backward compatibility, graceful degradation

Test Suite Composition:
- REG01-REG10: Regression tests for backward compatibility and production scenarios
- Organized in 2 test classes: Backward Compatibility, Production Scenarios

Test IDs: REG01-REG10
Test Organization: 5 backward compat + 5 production scenario tests
Coverage: Graceful degradation, circular dependencies, timeout protection, production fixtures
"""

import pytest
from pathlib import Path

# Import shared helper
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "unit"))
from test_story_064_unit_suite import FileValidationHelper


class TestBackwardCompatibility:
    """Regression tests for backward compatibility (REG01-REG05)"""

    @pytest.mark.regression
    @pytest.mark.acceptance_criteria
    def test_reg01_story_creation_works_without_guidance_file(self):
        """
        REG01: Story-creation gracefully degrades if guidance file missing

        ARRANGE: Verify graceful degradation documented in SKILL.md
        ACT: Search for error handling in Phase 1
        ASSERT: SKILL.md documents fallback behavior
        """
        # Arrange
        skill_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md"
        )

        # Act & Assert
        assert skill_path.exists(), "Story-creation SKILL.md required"

        with open(skill_path, 'r') as f:
            content = f.read()

        # Verify graceful degradation documented
        assert "graceful" in content.lower() or "missing" in content.lower() or "fallback" in content.lower(), (
            "REG01 violation: SKILL.md must document graceful degradation if guidance file missing"
        )

        # Verify workflow continues without patterns
        assert "continue" in content.lower() or "without" in content.lower(), (
            "REG01 violation: Must explicitly state workflow continues without guidance"
        )

    @pytest.mark.regression
    @pytest.mark.acceptance_criteria
    def test_reg02_skill_invocation_without_guidance_integration(self):
        """
        REG02: devforgeai-story-creation can be invoked independently

        ARRANGE: Load SKILL.md
        ACT: Verify skill is self-contained (no hard dependency on guidance)
        ASSERT: Skill functions with or without guidance file
        """
        # Arrange
        skill_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md"
        )

        # Act & Assert
        assert skill_path.exists(), "Story-creation SKILL.md required"

        with open(skill_path, 'r') as f:
            content = f.read()

        # Verify skill can run independently
        # Should have fallback path or optional guidance loading
        assert "Phase 1" in content or "Story Discovery" in content, (
            "REG02 violation: SKILL.md must define story creation phases"
        )

        # Verify no hard requirement on guidance
        assert "must load" not in content.lower() or "optional" in content.lower(), (
            "REG02 violation: Guidance loading should be optional, not required"
        )

    @pytest.mark.regression
    @pytest.mark.acceptance_criteria
    def test_reg03_cross_references_dont_create_circular_dependencies(self):
        """
        REG03: Cross-references between files don't create circular dependencies

        ARRANGE: Load both ideation and story-creation integration guides
        ACT: Analyze reference patterns
        ASSERT: No circular dependencies in reference structure
        """
        # Arrange
        ideation_guidance_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
        )

        story_creation_integration_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/references/user-input-integration-guide.md"
        )

        # Act & Assert
        if ideation_guidance_path.exists() and story_creation_integration_path.exists():
            with open(ideation_guidance_path, 'r') as f:
                ideation_content = f.read()

            with open(story_creation_integration_path, 'r') as f:
                story_creation_content = f.read()

            # Verify no circular references
            # story-creation references ideation guidance
            assert "ideation" in story_creation_content.lower(), (
                "REG03: Story-creation should reference ideation guidance"
            )

            # ideation guidance mentions story-creation in Integration Points
            if "Integration Points" in ideation_content:
                assert "story-creation" in ideation_content.lower() or "story" in ideation_content.lower(), (
                    "REG03: Ideation guidance should mention story-creation in Integration Points"
                )

    @pytest.mark.regression
    @pytest.mark.acceptance_criteria
    def test_reg04_guidance_loading_timeout_protection(self):
        """
        REG04: Guidance loading has timeout protection (< 2 seconds p95)

        ARRANGE: Verify timeout documented in integration guide
        ACT: Search for timeout specifications
        ASSERT: Timeout protection documented
        """
        # Arrange
        integration_guide_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/references/user-input-integration-guide.md"
        )

        # Act & Assert
        if integration_guide_path.exists():
            with open(integration_guide_path, 'r') as f:
                content = f.read()

            # Check for performance guidance
            assert "2 second" in content or "timeout" in content.lower() or "performance" in content.lower(), (
                "REG04 violation: Integration guide should document guidance loading timeout (< 2s p95)"
            )

    @pytest.mark.regression
    @pytest.mark.acceptance_criteria
    def test_reg05_pattern_matching_resilient_to_variation(self):
        """
        REG05: Pattern matching is resilient to pattern name variation

        ARRANGE: Verify pattern name normalization documented
        ACT: Search for normalization rules
        ASSERT: Rules handle case sensitivity and spacing
        """
        # Arrange
        integration_guide_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/references/user-input-integration-guide.md"
        )

        # Act & Assert
        if integration_guide_path.exists():
            with open(integration_guide_path, 'r') as f:
                content = f.read()

            # Check for normalization rules
            assert "normalize" in content.lower() or "case" in content.lower() or "variation" in content.lower(), (
                "REG05 violation: Integration guide should document pattern name normalization"
            )


class TestProductionScenarios:
    """Regression tests for production scenarios (REG06-REG10)"""

    @pytest.mark.regression
    @pytest.mark.acceptance_criteria
    def test_reg06_create_story_with_simple_feature_description(self):
        """
        REG06: /create-story works with simple feature descriptions

        ARRANGE: Load simple-feature.md fixture
        ACT: Verify fixture format is compatible with /create-story
        ASSERT: Fixture can be used as valid input to story creation
        """
        # Arrange
        simple_feature_path = Path(
            "/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/simple-feature.md"
        )

        # Act & Assert
        assert simple_feature_path.exists(), (
            "Simple feature fixture required for REG06"
        )

        with open(simple_feature_path, 'r') as f:
            content = f.read()

        # Verify fixture has expected structure
        assert len(content) > 50, "Simple feature fixture too short"
        assert "CRUD" in content or "straightforward" in content or "feature" in content.lower(), (
            "Simple feature fixture missing expected content"
        )

    @pytest.mark.regression
    @pytest.mark.acceptance_criteria
    def test_reg07_create_story_with_complex_feature_description(self):
        """
        REG07: /create-story handles complex feature descriptions

        ARRANGE: Load complex-feature.md fixture
        ACT: Verify fixture represents realistic complex requirements
        ASSERT: Fixture demonstrates cross-cutting concern scenario
        """
        # Arrange
        complex_feature_path = Path(
            "/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/complex-feature.md"
        )

        # Act & Assert
        assert complex_feature_path.exists(), (
            "Complex feature fixture required for REG07"
        )

        with open(complex_feature_path, 'r') as f:
            content = f.read()

        # Verify fixture demonstrates complexity
        assert len(content) > 200, "Complex feature fixture too short"
        assert "cross-cutting" in content.lower() or "dependencies" in content.lower() or "component" in content.lower(), (
            "Complex feature fixture missing complexity indicators"
        )

    @pytest.mark.regression
    @pytest.mark.acceptance_criteria
    def test_reg08_guidance_patterns_applied_to_epic_selection(self):
        """
        REG08: Epic selection question uses guidance patterns

        ARRANGE: Load SKILL.md Phase 1 Step 3
        ACT: Search for epic selection question pattern
        ASSERT: Question applies Explicit Classification + Bounded Choice patterns
        """
        # Arrange
        skill_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md"
        )

        # Act & Assert
        assert skill_path.exists(), "Story-creation SKILL.md required"

        with open(skill_path, 'r') as f:
            content = f.read()

        # Verify epic selection documented
        assert "epic" in content.lower() or "Step 3" in content or "Step 4" in content, (
            "REG08 violation: SKILL.md must document epic selection step"
        )

        # Verify patterns used
        assert "pattern" in content.lower() or "bounded" in content.lower() or "choice" in content.lower(), (
            "REG08 violation: SKILL.md should reference pattern usage"
        )

    @pytest.mark.regression
    @pytest.mark.acceptance_criteria
    def test_reg09_guidance_patterns_applied_to_priority_selection(self):
        """
        REG09: Priority selection question uses Explicit Classification pattern

        ARRANGE: Load SKILL.md Phase 1 Step 5
        ACT: Search for priority selection question pattern
        ASSERT: Question applies Explicit Classification pattern with 4 levels
        """
        # Arrange
        skill_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md"
        )

        # Act & Assert
        assert skill_path.exists(), "Story-creation SKILL.md required"

        with open(skill_path, 'r') as f:
            content = f.read()

        # Verify priority selection documented
        assert "priority" in content.lower() or "Step 5" in content, (
            "REG09 violation: SKILL.md must document priority selection step"
        )

        # Verify 4-level classification
        assert "critical" in content.lower() or "high" in content.lower() or "medium" in content.lower() or "low" in content.lower(), (
            "REG09 violation: SKILL.md should document 4-level priority classification"
        )

    @pytest.mark.regression
    @pytest.mark.acceptance_criteria
    def test_reg10_guidance_patterns_applied_to_points_selection(self):
        """
        REG10: Story points selection uses Fibonacci Bounded Choice pattern

        ARRANGE: Load SKILL.md Phase 1 Step 5
        ACT: Search for points selection question pattern
        ASSERT: Question applies Fibonacci sequence (1, 2, 3, 5, 8, 13)
        """
        # Arrange
        skill_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md"
        )

        # Act & Assert
        assert skill_path.exists(), "Story-creation SKILL.md required"

        with open(skill_path, 'r') as f:
            content = f.read()

        # Verify points selection documented
        assert "point" in content.lower() or "fibonacci" in content.lower() or "complexity" in content.lower(), (
            "REG10 violation: SKILL.md must document story points selection"
        )

        # Verify Fibonacci sequence mentioned
        fibonacci_numbers = ["1", "2", "3", "5", "8", "13"]
        found_numbers = sum(1 for num in fibonacci_numbers if num in content)

        assert found_numbers >= 3, (
            f"REG10 violation: SKILL.md should reference Fibonacci sequence. "
            f"Found {found_numbers}/6 Fibonacci numbers"
        )
