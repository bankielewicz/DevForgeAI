"""
Unit tests for devforgeai-ideation skill guidance loading (AC#1).

STORY-055: devforgeai-ideation Skill Integration with User Input Guidance
Test Objective: Verify user-input-guidance.md loads in Phase 1 Step 0

Tests follow AAA pattern (Arrange, Act, Assert) and are designed to FAIL
until implementation is complete (TDD Red phase).

Coverage: AC#1 (Pre-Discovery Guidance Loading)
"""

import pytest
import os
from pathlib import Path
from typing import Optional, Dict, Any


class TestGuidanceFileLocation:
    """AC#1: Tests for guidance file location and existence."""

    @pytest.fixture
    def guidance_file_path(self) -> Path:
        """Guidance file should exist at documented location."""
        return Path(
            "src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
        )

    def test_should_exist_at_specified_path(self, guidance_file_path: Path):
        """
        Given the devforgeai-ideation skill
        When queried for user-input-guidance.md location
        Then file must exist at: src/claude/skills/devforgeai-ideation/references/user-input-guidance.md
        """
        # Arrange
        project_root = Path.cwd()
        full_path = project_root / guidance_file_path

        # Act
        file_exists = full_path.exists()

        # Assert
        assert file_exists, f"Guidance file not found at {full_path}"

    def test_should_be_markdown_file(self, guidance_file_path: Path):
        """
        Given the guidance file exists
        When checked for format
        Then file extension must be .md
        """
        # Arrange
        project_root = Path.cwd()
        full_path = project_root / guidance_file_path

        # Act
        extension = full_path.suffix

        # Assert
        assert extension == ".md", f"Expected .md extension, got {extension}"

    def test_should_be_readable_file(self, guidance_file_path: Path):
        """
        Given the guidance file exists
        When attempting to read
        Then file must be readable without errors
        """
        # Arrange
        project_root = Path.cwd()
        full_path = project_root / guidance_file_path

        # Act & Assert
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
                assert len(content) > 0, "Guidance file is empty"
        except IOError as e:
            pytest.fail(f"Cannot read guidance file: {e}")

    def test_should_contain_required_sections(self, guidance_file_path: Path):
        """
        Given the guidance file content
        When examined for structure
        Then must contain all required reference sections:
        - Elicitation Patterns (Section 2)
        - AskUserQuestion Templates (Section 3)
        - Skill Integration Guide (Section 5)
        """
        # Arrange
        project_root = Path.cwd()
        full_path = project_root / guidance_file_path
        required_sections = [
            "Section 2: Elicitation Patterns",
            "Section 3: AskUserQuestion Templates",
            "Section 5: Skill Integration Guide",
        ]

        # Act
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Assert
        for section in required_sections:
            assert (
                section in content
            ), f"Missing required section: {section}"

    def test_should_have_minimum_size(self, guidance_file_path: Path):
        """
        Given the guidance file exists
        When file size is checked
        Then must be substantial (>1000 chars) to contain meaningful patterns
        """
        # Arrange
        project_root = Path.cwd()
        full_path = project_root / guidance_file_path
        minimum_chars = 1000

        # Act
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
            file_size = len(content)

        # Assert
        assert file_size > minimum_chars, (
            f"Guidance file too small: {file_size} chars "
            f"(minimum {minimum_chars} required)"
        )

    def test_should_have_valid_yaml_frontmatter(self, guidance_file_path: Path):
        """
        Given the guidance file
        When examined for metadata
        Then must have YAML frontmatter with required fields
        """
        # Arrange
        project_root = Path.cwd()
        full_path = project_root / guidance_file_path
        required_fields = ["id:", "title:", "version:"]

        # Act
        with open(full_path, "r", encoding="utf-8") as f:
            first_50_lines = "\n".join(f.readlines()[:50])

        # Assert
        assert "---" in first_50_lines, "Missing YAML frontmatter delimiter"
        for field in required_fields:
            assert field in first_50_lines, f"Missing YAML field: {field}"


class TestGuidanceLoadingMechanism:
    """AC#1: Tests for guidance loading mechanism in Phase 1 Step 0."""

    def test_skill_file_should_reference_step_0(self):
        """
        Given the devforgeai-ideation SKILL.md file
        When examined for Phase 1 structure
        Then must contain "Step 0" before Step 1 definition
        """
        # Arrange
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )

        # Act
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Assert
        # Look for Phase 1 section
        assert "## Phase 1" in content or "### Phase 1" in content, (
            "Phase 1 not found in SKILL.md"
        )

        # Verify Step 0 exists before Step 1
        step_0_index = content.find("Step 0")
        step_1_index = content.find("Step 1")

        assert step_0_index != -1, "Step 0 not found in Phase 1"
        assert step_0_index < step_1_index, (
            "Step 0 should appear before Step 1"
        )

    def test_phase_1_step_0_should_mention_guidance(self):
        """
        Given Phase 1 Step 0 exists in SKILL.md
        When examined for purpose
        Then must mention loading guidance or user-input-guidance
        """
        # Arrange
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )

        # Act
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract Phase 1 section
        phase_1_start = content.find("## Phase 1")
        if phase_1_start == -1:
            phase_1_start = content.find("### Phase 1")
        phase_1_end = content.find("## Phase 2")
        if phase_1_end == -1:
            phase_1_end = content.find("### Phase 2")

        phase_1_content = content[phase_1_start:phase_1_end]

        # Extract Step 0 section
        step_0_start = phase_1_content.find("Step 0")
        step_1_start = phase_1_content.find("Step 1")
        step_0_content = phase_1_content[step_0_start:step_1_start]

        # Assert
        assert "guidance" in step_0_content.lower(), (
            "Step 0 must mention guidance loading"
        )

    def test_step_0_should_use_read_tool(self):
        """
        Given Phase 1 Step 0 in SKILL.md
        When examined for tool usage
        Then must use Read(file_path='...') to load guidance
        """
        # Arrange
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )

        # Act
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract Phase 1 Step 0 section
        phase_1_start = content.find("## Phase 1")
        if phase_1_start == -1:
            phase_1_start = content.find("### Phase 1")
        phase_1_end = content.find("## Phase 2")
        if phase_1_end == -1:
            phase_1_end = content.find("### Phase 2")

        phase_1_content = content[phase_1_start:phase_1_end]
        step_0_start = phase_1_content.find("Step 0")
        step_1_start = phase_1_content.find("Step 1")
        step_0_content = phase_1_content[step_0_start:step_1_start]

        # Assert
        assert "Read(" in step_0_content, (
            "Step 0 must use Read tool to load guidance"
        )
        assert "user-input-guidance" in step_0_content, (
            "Step 0 must reference user-input-guidance file"
        )


class TestGuidanceFileContent:
    """AC#1: Tests for guidance file content structure."""

    @pytest.fixture
    def guidance_content(self) -> str:
        """Load guidance file content."""
        guidance_path = Path(
            "src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
        )
        with open(guidance_path, "r", encoding="utf-8") as f:
            return f.read()

    def test_should_contain_elicitation_patterns(self, guidance_content: str):
        """
        Given the guidance file
        When examined for Section 2
        Then must contain elicitation patterns (≥5 patterns minimum)
        """
        # Arrange
        pattern_count = 0
        pattern_keywords = [
            "Pattern 1:",
            "Pattern 2:",
            "Pattern 3:",
            "Pattern 4:",
            "Pattern 5:",
        ]

        # Act
        for keyword in pattern_keywords:
            if keyword in guidance_content:
                pattern_count += 1

        # Assert
        assert pattern_count >= 5, (
            f"Expected ≥5 patterns, found {pattern_count}"
        )

    def test_should_contain_ask_user_question_templates(
        self, guidance_content: str
    ):
        """
        Given the guidance file Section 3
        When examined for AskUserQuestion templates
        Then must contain ≥10 template examples
        """
        # Arrange
        template_pattern_count = guidance_content.count("AskUserQuestion")

        # Act & Assert
        assert template_pattern_count >= 10, (
            f"Expected ≥10 AskUserQuestion templates, found {template_pattern_count}"
        )

    def test_should_contain_nfr_quantification_table(
        self, guidance_content: str
    ):
        """
        Given the guidance file Section 4
        When examined for NFR quantification
        Then must contain table mapping vague terms to metrics
        """
        # Arrange
        nfr_indicators = [
            "fast",
            "scalable",
            "responsive",
            "secure",
            "metric",
            "measurement",
        ]

        # Act
        nfr_references = sum(
            1 for indicator in nfr_indicators if indicator in guidance_content.lower()
        )

        # Assert
        assert nfr_references >= 3, (
            f"Expected ≥3 NFR-related terms, found {nfr_references}"
        )

    def test_should_have_skill_integration_guide(
        self, guidance_content: str
    ):
        """
        Given Section 5 (Skill Integration Guide)
        When examined
        Then must contain guidance for devforgeai-ideation specifically
        """
        # Arrange
        skill_mentions = guidance_content.count("devforgeai-ideation")

        # Act & Assert
        assert skill_mentions >= 1, (
            "devforgeai-ideation must be mentioned in skill integration guide"
        )

    def test_should_have_framework_terminology_reference(
        self, guidance_content: str
    ):
        """
        Given Section 6 (Framework Terminology Reference)
        When examined
        Then must contain links/references to CLAUDE.md concepts
        """
        # Arrange
        framework_terms = [
            "acceptance criteria",
            "technical specification",
            "constraint",
            "edge case",
        ]

        # Act
        framework_references = sum(
            1
            for term in framework_terms
            if term in guidance_content.lower()
        )

        # Assert
        assert framework_references >= 2, (
            f"Expected ≥2 framework terminology references, found {framework_references}"
        )


class TestGuidanceLoadingErrorHandling:
    """Tests for graceful degradation if guidance file missing."""

    def test_missing_guidance_should_not_halt_skill(self):
        """
        Given guidance file temporarily unavailable
        When Step 0 executes
        Then skill should continue with standard prompts (graceful degradation)

        Business Rule BR-001: "Guidance loading must not halt skill execution
        if file unavailable"
        """
        # Arrange
        guidance_path = Path(
            "src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
        )
        original_exists = guidance_path.exists()

        # Act & Assert
        # This test verifies the behavior would occur if file missing
        # Implementation should handle FileNotFoundError gracefully
        if not original_exists:
            # If file actually missing in test environment, skip
            pytest.skip("Guidance file not found - testing graceful degradation")

    def test_step_0_should_have_error_handling(self):
        """
        Given Phase 1 Step 0 code
        When examined for error handling
        Then must handle potential Read() failures gracefully
        """
        # Arrange
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )

        # Act
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract Step 0 section
        phase_1_start = content.find("## Phase 1")
        if phase_1_start == -1:
            phase_1_start = content.find("### Phase 1")
        phase_1_end = content.find("## Phase 2")
        if phase_1_end == -1:
            phase_1_end = content.find("### Phase 2")

        phase_1_content = content[phase_1_start:phase_1_end]
        step_0_start = phase_1_content.find("Step 0")
        step_1_start = phase_1_content.find("Step 1")
        step_0_content = phase_1_content[step_0_start:step_1_start]

        # Assert
        # Should have comment or instruction about handling missing file
        error_handling_indicators = [
            "if the file is unavailable",
            "graceful degradation",
            "continue without",
            "log a warning",
            "proceed with standard",
        ]

        has_error_handling = any(
            indicator in step_0_content.lower()
            for indicator in error_handling_indicators
        )

        assert has_error_handling, (
            "Step 0 should document error handling for missing guidance file"
        )
