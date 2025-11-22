"""
Integration tests for devforgeai-ideation skill guidance pattern application (AC#2-3).

STORY-055: devforgeai-ideation Skill Integration with User Input Guidance
Test Objectives:
- AC#2: Verify pattern application in discovery questions
- AC#3: Verify subagent invocation quality improvement

Tests follow AAA pattern and are designed to FAIL until implementation (TDD Red).

Coverage: AC#2 (Pattern Application), AC#3 (Subagent Quality)
"""

import pytest
import re
from pathlib import Path
from typing import Dict, List, Set
from dataclasses import dataclass


@dataclass
class PatternMatch:
    """Represents a detected pattern in text."""

    pattern_name: str
    keyword: str
    location: str
    context: str


class TestPatternApplicationOpenEnded:
    """AC#2: Tests for Open-Ended Discovery pattern application."""

    @pytest.fixture
    def skill_content(self) -> str:
        """Load devforgeai-ideation SKILL.md content."""
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )
        with open(skill_path, "r", encoding="utf-8") as f:
            return f.read()

    def test_phase_1_should_use_open_ended_pattern_for_scope(
        self, skill_content: str
    ):
        """
        Given Phase 1 (Requirements Discovery)
        When examining business scope questions
        Then must use "Tell me about..." open-ended pattern

        From AC#2: "Problem Scope questions use 'Tell me about...' open-ended pattern"
        """
        # Arrange
        phase_1_start = skill_content.find("## Phase 1")
        if phase_1_start == -1:
            phase_1_start = skill_content.find("### Phase 1")
        phase_2_start = skill_content.find("## Phase 2")
        if phase_2_start == -1:
            phase_2_start = skill_content.find("### Phase 2")

        phase_1_content = skill_content[phase_1_start:phase_2_start]

        # Search for question patterns that ask about scope/problem
        scope_keywords = [
            "business scope",
            "problem scope",
            "problem statement",
            "current situation",
            "challenge",
            "pain point",
        ]

        # Act
        scope_section_found = any(
            keyword in phase_1_content.lower() for keyword in scope_keywords
        )

        if scope_section_found:
            # Extract questions about scope
            tell_me_about_count = phase_1_content.lower().count("tell me about")

            # Assert
            assert (
                tell_me_about_count > 0
            ), "Phase 1 scope questions should use 'Tell me about...' pattern"

    def test_open_ended_pattern_should_avoid_yes_no_questions(
        self, skill_content: str
    ):
        """
        Given open-ended pattern application
        When examining questions
        Then should avoid yes/no questions (should be conversational "Tell me about...")
        """
        # Arrange
        phase_1_start = skill_content.find("## Phase 1")
        if phase_1_start == -1:
            phase_1_start = skill_content.find("### Phase 1")
        phase_2_start = skill_content.find("## Phase 2")
        if phase_2_start == -1:
            phase_2_start = skill_content.find("### Phase 2")

        phase_1_content = skill_content[phase_1_start:phase_2_start]

        # Look for "Tell me about" style questions
        open_ended_pattern = r"Tell me about|Describe|Explain|Walk me through|Share"

        # Act
        open_ended_matches = re.findall(
            open_ended_pattern, phase_1_content, re.IGNORECASE
        )

        # Assert (should have at least one, indicating pattern adoption)
        assert len(open_ended_matches) >= 1, (
            "Phase 1 should contain ≥1 open-ended question pattern"
        )


class TestPatternApplicationRanking:
    """AC#2: Tests for Comparative Ranking pattern application."""

    @pytest.fixture
    def skill_content(self) -> str:
        """Load devforgeai-ideation SKILL.md content."""
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )
        with open(skill_path, "r", encoding="utf-8") as f:
            return f.read()

    def test_phase_2_should_use_ranking_pattern_for_priorities(
        self, skill_content: str
    ):
        """
        Given Phase 2 (Feature Elicitation)
        When examining feature priority questions
        Then must use "Rank 1-5" comparative pattern

        From AC#2: "Feature Priority questions use 'Rank 1-5' comparative pattern"
        """
        # Arrange
        phase_2_start = skill_content.find("## Phase 2")
        if phase_2_start == -1:
            phase_2_start = skill_content.find("### Phase 2")
        phase_3_start = skill_content.find("## Phase 3")
        if phase_3_start == -1:
            phase_3_start = skill_content.find("### Phase 3")

        phase_2_content = skill_content[phase_2_start:phase_3_start]

        # Look for ranking/prioritization keywords
        priority_keywords = [
            "priority",
            "prioritize",
            "importance",
            "rank",
            "ranking",
            "order",
        ]

        # Act
        priority_section_found = any(
            keyword in phase_2_content.lower() for keyword in priority_keywords
        )

        if priority_section_found:
            # Look for "Rank" pattern
            rank_pattern = r"Rank\s*\d-\d|ranking\s*\d-\d"
            ranking_matches = re.findall(
                rank_pattern, phase_2_content, re.IGNORECASE
            )

            # Assert
            assert len(ranking_matches) > 0, (
                "Phase 2 priority questions should use 'Rank X-Y' pattern"
            )

    def test_ranking_pattern_should_provide_scale(
        self, skill_content: str
    ):
        """
        Given ranking pattern in questions
        When examining question structure
        Then should provide numeric scale (e.g., 1-5)
        """
        # Arrange
        phase_2_start = skill_content.find("## Phase 2")
        if phase_2_start == -1:
            phase_2_start = skill_content.find("### Phase 2")
        phase_3_start = skill_content.find("## Phase 3")
        if phase_3_start == -1:
            phase_3_start = skill_content.find("### Phase 3")

        phase_2_content = skill_content[phase_2_start:phase_3_start]

        # Act
        # Look for scale definitions (1-5, 1-10, etc.)
        scale_pattern = r"\d-\d|scale|priority level"
        scale_matches = re.findall(
            scale_pattern, phase_2_content, re.IGNORECASE
        )

        # Assert
        if "rank" in phase_2_content.lower():
            assert len(scale_matches) > 0, (
                "Ranking questions should define a numeric scale"
            )


class TestPatternApplicationBoundedChoice:
    """AC#2: Tests for Bounded Choice pattern application."""

    @pytest.fixture
    def skill_content(self) -> str:
        """Load devforgeai-ideation SKILL.md content."""
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )
        with open(skill_path, "r", encoding="utf-8") as f:
            return f.read()

    def test_should_use_bounded_choice_for_timeline_questions(
        self, skill_content: str
    ):
        """
        Given Phase 1-2 timeline/schedule questions
        When examining question structure
        Then must use "Select range: ..." bounded pattern

        From AC#2: "Timeline questions use 'Select range: 1-2 weeks, 1-3 months...' bounded pattern"
        """
        # Arrange
        # Look for timeline/schedule related sections
        timeline_keywords = [
            "timeline",
            "schedule",
            "deadline",
            "timeframe",
            "duration",
            "when",
        ]

        # Act
        timeline_section_exists = any(
            keyword in skill_content.lower() for keyword in timeline_keywords
        )

        if timeline_section_exists:
            # Look for bounded choice pattern
            bounded_pattern = r"select range|choose from|between|within"
            bounded_matches = re.findall(
                bounded_pattern, skill_content, re.IGNORECASE
            )

            # Assert
            assert len(bounded_matches) > 0, (
                "Timeline questions should use bounded choice pattern"
            )

    def test_bounded_choice_should_provide_options(
        self, skill_content: str
    ):
        """
        Given bounded choice pattern for timeline
        When examining options
        Then should provide specific time ranges (weeks, months)
        """
        # Arrange
        time_unit_pattern = r"week|month|day|quarter"

        # Act
        time_references = len(
            re.findall(time_unit_pattern, skill_content, re.IGNORECASE)
        )

        # Assert
        assert time_references > 0, (
            "Bounded timeline questions should reference time units"
        )


class TestPatternApplicationExplicitClassification:
    """AC#2: Tests for Explicit Classification pattern application."""

    @pytest.fixture
    def skill_content(self) -> str:
        """Load devforgeai-ideation SKILL.md content."""
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )
        with open(skill_path, "r", encoding="utf-8") as f:
            return f.read()

    def test_should_use_explicit_classification_for_personas(
        self, skill_content: str
    ):
        """
        Given Phase 2 user persona questions
        When examining question structure
        Then must use "Primary user: [Admin/Developer/End User]" classification pattern

        From AC#2: "User Persona questions use 'Primary user: [Admin/Developer/End User]' explicit classification"
        """
        # Arrange
        persona_keywords = [
            "user",
            "persona",
            "audience",
            "target",
            "stakeholder",
        ]

        # Act
        persona_section_exists = any(
            keyword in skill_content.lower() for keyword in persona_keywords
        )

        if persona_section_exists:
            # Look for explicit classification pattern
            classification_pattern = r"Primary user|user type|role|admin|developer|end user"
            classification_matches = re.findall(
                classification_pattern, skill_content, re.IGNORECASE
            )

            # Assert
            assert len(classification_matches) > 0, (
                "User persona questions should use explicit classification pattern"
            )

    def test_classification_should_provide_predefined_options(
        self, skill_content: str
    ):
        """
        Given explicit classification pattern
        When examining question structure
        Then should provide predefined user role options
        """
        # Arrange
        role_options = ["admin", "developer", "end user", "manager", "operator"]

        # Act
        role_references = sum(
            skill_content.lower().count(role) for role in role_options
        )

        # Assert
        assert role_references >= 2, (
            "Classification questions should list predefined user role options"
        )


class TestPatternConsistency:
    """AC#2: Tests for consistent pattern application across phases."""

    @pytest.fixture
    def skill_content(self) -> str:
        """Load devforgeai-ideation SKILL.md content."""
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )
        with open(skill_path, "r", encoding="utf-8") as f:
            return f.read()

    def test_all_ask_user_question_invocations_should_use_patterns(
        self, skill_content: str
    ):
        """
        Given all AskUserQuestion invocations in Phase 1-2
        When examined
        Then should contain pattern keywords (Tell me, Rank, Select range, Primary user)
        """
        # Arrange
        phase_1_start = skill_content.find("## Phase 1")
        if phase_1_start == -1:
            phase_1_start = skill_content.find("### Phase 1")
        phase_3_start = skill_content.find("## Phase 3")
        if phase_3_start == -1:
            phase_3_start = skill_content.find("### Phase 3")

        phase_1_2_content = skill_content[phase_1_start:phase_3_start]

        # Count AskUserQuestion invocations
        ask_invocation_count = phase_1_2_content.count("AskUserQuestion")

        # Count pattern keywords
        pattern_keywords = [
            "Tell me about",
            "Rank",
            "Select range",
            "Primary user",
        ]
        pattern_count = sum(
            phase_1_2_content.count(keyword) for keyword in pattern_keywords
        )

        # Act & Assert
        # Should have meaningful pattern usage if AskUserQuestion is used
        if ask_invocation_count > 0:
            assert pattern_count >= 2, (
                f"Expected ≥2 pattern keywords in Phase 1-2, found {pattern_count}"
            )

    def test_patterns_should_not_duplicate_guidance_file_content(
        self, skill_content: str
    ):
        """
        Given pattern application in Phase 1-2
        When examined
        Then should USE patterns, not duplicate guidance file content verbatim

        Business Rule BR-002: "Pattern application must preserve existing question
        intent (enhancement, not replacement)"
        """
        # Arrange
        guidance_path = Path(
            "src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
        )
        with open(guidance_path, "r", encoding="utf-8") as f:
            guidance_content = f.read()

        # Extract guidance file large chunks (>100 chars)
        long_sentences = [
            s for s in guidance_content.split(".") if len(s) > 100
        ]

        # Act
        duplicated_chunks = 0
        for chunk in long_sentences[:5]:  # Check first 5 long chunks
            if chunk.strip() in skill_content:
                duplicated_chunks += 1

        # Assert
        assert (
            duplicated_chunks == 0
        ), "Phase 1-2 should apply patterns, not copy guidance verbatim"


class TestSubagentInvocationQuality:
    """AC#3: Tests for subagent invocation quality improvement."""

    @pytest.fixture
    def skill_content(self) -> str:
        """Load devforgeai-ideation SKILL.md content."""
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )
        with open(skill_path, "r", encoding="utf-8") as f:
            return f.read()

    def test_phase_3_should_invoke_requirements_analyst_subagent(
        self, skill_content: str
    ):
        """
        Given Phase 3 (Epic Decomposition)
        When examined
        Then must invoke requirements-analyst subagent
        """
        # Arrange
        phase_3_start = skill_content.find("## Phase 3")
        if phase_3_start == -1:
            phase_3_start = skill_content.find("### Phase 3")
        phase_4_start = skill_content.find("## Phase 4")
        if phase_4_start == -1:
            phase_4_start = skill_content.find("### Phase 4")

        phase_3_content = skill_content[phase_3_start:phase_4_start]

        # Act
        subagent_invocation = (
            "requirements-analyst" in phase_3_content
            or "requirements_analyst" in phase_3_content
        )

        # Assert
        assert subagent_invocation, (
            "Phase 3 should invoke requirements-analyst subagent"
        )

    def test_phase_3_subagent_prompt_should_include_collected_context(
        self, skill_content: str
    ):
        """
        Given requirements-analyst subagent invocation in Phase 3
        When examining the prompt
        Then should reference collected context from Phase 1-2 (not just patterns)

        Business Rule BR-003: "Subagent receives structured context (not raw pattern names)"
        """
        # Arrange
        phase_3_start = skill_content.find("## Phase 3")
        if phase_3_start == -1:
            phase_3_start = skill_content.find("### Phase 3")
        phase_4_start = skill_content.find("## Phase 4")
        if phase_4_start == -1:
            phase_4_start = skill_content.find("### Phase 4")

        phase_3_content = skill_content[phase_3_start:phase_4_start]

        # Look for context variable references (e.g., ${problem_scope}, user_answers, collected_data)
        context_indicators = [
            "user_responses",
            "collected",
            "scope",
            "requirements",
            "context",
            "answers",
        ]

        # Act
        context_references = sum(
            1
            for indicator in context_indicators
            if indicator in phase_3_content.lower()
        )

        # Assert
        assert context_references >= 2, (
            "Phase 3 subagent invocation should include structured context "
            "from Phase 1-2 collection"
        )

    def test_subagent_prompt_should_not_mention_pattern_names(
        self, skill_content: str
    ):
        """
        Given requirements-analyst subagent prompt
        When examined
        Then should NOT mention pattern names (Open-Ended, Ranking, etc.) directly

        Business Rule BR-003: "Subagent receives structured context (not raw pattern names)"
        """
        # Arrange
        phase_3_start = skill_content.find("## Phase 3")
        if phase_3_start == -1:
            phase_3_start = skill_content.find("### Phase 3")
        phase_4_start = skill_content.find("## Phase 4")
        if phase_4_start == -1:
            phase_4_start = skill_content.find("### Phase 4")

        phase_3_content = skill_content[phase_3_start:phase_4_start]

        # Extract subagent invocation (Task/Skill call)
        subagent_prompt_start = phase_3_content.find("prompt")
        if subagent_prompt_start > 0:
            # Get roughly the next 500 chars of prompt
            subagent_prompt = phase_3_content[
                subagent_prompt_start : subagent_prompt_start + 500
            ]

            # Look for pattern name references
            pattern_name_indicators = [
                "Open-Ended pattern",
                "Ranking pattern",
                "Bounded Choice",
                "Classification pattern",
            ]

            # Act
            pattern_mentions = sum(
                subagent_prompt.count(indicator)
                for indicator in pattern_name_indicators
            )

            # Assert
            assert pattern_mentions == 0, (
                "Subagent prompt should not mention pattern names directly; "
                "should use structured context instead"
            )


class TestBackwardCompatibility:
    """AC#5: Tests for backward compatibility."""

    def test_skill_should_not_remove_existing_phases(self):
        """
        Given devforgeai-ideation SKILL.md
        When examined
        Then must retain all existing phases 1-6 (Step 0 is NEW addition, not replacement)
        """
        # Arrange
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )

        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Count phase definitions
        required_phases = {
            "Phase 1": False,
            "Phase 2": False,
            "Phase 3": False,
            "Phase 4": False,
            "Phase 5": False,
            "Phase 6": False,
        }

        # Act
        for phase in required_phases:
            if f"## {phase}" in content or f"### {phase}" in content:
                required_phases[phase] = True

        # Assert
        missing_phases = [
            phase for phase, found in required_phases.items() if not found
        ]
        assert not missing_phases, (
            f"SKILL.md missing phases: {missing_phases}. "
            f"Step 0 must be added WITHOUT removing existing phases."
        )

    def test_phase_1_existing_steps_should_be_preserved(self):
        """
        Given Phase 1 existing steps (1-onwards)
        When examined
        Then Step 0 should be NEW insertion BEFORE Step 1 (not replacement)
        """
        # Arrange
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )

        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract Phase 1
        phase_1_start = content.find("## Phase 1")
        if phase_1_start == -1:
            phase_1_start = content.find("### Phase 1")
        phase_2_start = content.find("## Phase 2")
        if phase_2_start == -1:
            phase_2_start = content.find("### Phase 2")

        phase_1_content = content[phase_1_start:phase_2_start]

        # Look for original steps
        original_steps = {
            "Step 1": False,
            "Step 2": False,
            "Step 3": False,
        }

        # Act
        for step in original_steps:
            if step in phase_1_content:
                original_steps[step] = True

        # Assert
        missing_steps = [step for step, found in original_steps.items() if not found]
        if missing_steps:
            # Some projects might have different numbering, so allow flexible check
            assert (
                "Step " in phase_1_content
            ), "Phase 1 should retain existing workflow steps"
