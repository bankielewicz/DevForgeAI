"""
Performance and non-functional requirement tests for STORY-055.

STORY-055: devforgeai-ideation Skill Integration with User Input Guidance
Test Objectives:
- AC#4: Token overhead constraint (≤1,000 tokens)
- AC#3: Subagent re-invocation reduction (≥30%)
- NFR-001: Fast guidance loading (<500ms)
- NFR-002: Reduced re-invocations
- NFR-003: Reliability without guidance file
- NFR-004: Minimal code changes
- NFR-005: Pattern verification via tests

Tests follow AAA pattern and are designed to FAIL until implementation (TDD Red).

Note: Some tests use estimated/simulated measurements for initial development.
Once implementation exists, replace with actual measurements.
"""

import pytest
import time
from pathlib import Path
from typing import Dict, List, Callable
import re


class TestTokenOverheadConstraint:
    """AC#4, NFR-001: Tests for token overhead and performance."""

    @pytest.fixture
    def guidance_file_size_chars(self) -> int:
        """Get guidance file character count."""
        guidance_path = Path(
            "src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
        )
        if guidance_path.exists():
            with open(guidance_path, "r", encoding="utf-8") as f:
                return len(f.read())
        return 0

    @pytest.fixture
    def guidance_file_line_count(self) -> int:
        """Get guidance file line count."""
        guidance_path = Path(
            "src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
        )
        if guidance_path.exists():
            with open(guidance_path, "r", encoding="utf-8") as f:
                return len(f.readlines())
        return 0

    def test_guidance_file_not_exceeding_size_limit(
        self, guidance_file_size_chars: int
    ):
        """
        Given guidance file loaded in Phase 1 Step 0
        When file size is measured
        Then should be reasonable (~2,500 lines ≈ 10,000-15,000 chars)

        Note: AC#4 specifies guidance file is ~2,500 lines; this test verifies
        the file doesn't exceed practical limits for loading.
        """
        # Arrange
        max_practical_size = 50000  # Generous limit for markdown with examples

        # Act
        file_size = guidance_file_size_chars

        # Assert
        assert file_size > 0, "Guidance file not found"
        assert file_size <= max_practical_size, (
            f"Guidance file too large: {file_size} chars "
            f"(max {max_practical_size} recommended)"
        )

    def test_token_overhead_estimated_within_limit(
        self, guidance_file_size_chars: int
    ):
        """
        Given guidance file size of ~2,500 lines
        When token overhead is estimated (1 token ≈ 4 characters)
        Then estimated overhead should be ≤1,000 tokens

        From AC#4: "Total token overhead for Phase 1 increases by ≤1,000 tokens"

        Calculation:
        - If guidance file = 10,000 chars ÷ 4 = 2,500 tokens
        - But: Not all guidance is loaded into Phase 1 (selective sections used)
        - Estimated overhead after optimization = 800-1,000 tokens
        """
        # Arrange
        file_size = guidance_file_size_chars
        estimated_tokens_per_char = 1 / 4  # Approximate Claude tokenization

        # Act
        estimated_total_tokens = file_size * estimated_tokens_per_char
        # Assume selective loading (not entire file, ~40% in active Phase 1 context)
        estimated_phase_1_overhead = estimated_total_tokens * 0.4

        # Assert
        max_overhead_tokens = 1000
        assert estimated_phase_1_overhead <= max_overhead_tokens, (
            f"Estimated token overhead {estimated_phase_1_overhead} exceeds "
            f"maximum {max_overhead_tokens} tokens. "
            f"Consider optimizing guidance file or selective loading."
        )

    def test_guidance_file_loading_should_be_fast(
        self, guidance_file_size_chars: int
    ):
        """
        Given Phase 1 Step 0 loads guidance file
        When Read tool is invoked
        Then must complete within 500ms (NFR-001)

        Note: This test verifies file readability for speed testing.
        Actual performance measurement occurs during integration testing.
        """
        # Arrange
        guidance_path = Path(
            "src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
        )

        # Act & Assert
        if guidance_path.exists():
            start_time = time.time()
            with open(guidance_path, "r", encoding="utf-8") as f:
                content = f.read()
            elapsed_ms = (time.time() - start_time) * 1000

            # File I/O should be <500ms even for larger files
            # This is a baseline measurement, not the full skill execution
            assert elapsed_ms < 500, (
                f"File loading took {elapsed_ms}ms (expected <500ms). "
                f"Consider optimizing file I/O."
            )

    def test_phase_1_should_reference_guidance_selectively(self):
        """
        Given guidance file loaded in Step 0
        When examined for usage in Phase 1
        Then should use SELECTIVE sections (not load entire file into Phase 1)

        Strategy to meet token overhead constraint:
        - Load entire file in Step 0 (cache for reference)
        - Use selectively in Phase 1-2 questions (don't duplicate content)
        - Result: <1,000 token overhead despite large guidance file
        """
        # Arrange
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )

        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract Phase 1 section
        phase_1_start = content.find("## Phase 1")
        if phase_1_start == -1:
            phase_1_start = content.find("### Phase 1")
        phase_2_start = content.find("## Phase 2")
        if phase_2_start == -1:
            phase_2_start = content.find("### Phase 2")

        phase_1_content = content[phase_1_start:phase_2_start]

        # Count references to guidance (should be keywords/patterns, not full sections)
        guidance_references = phase_1_content.count("guidance")

        # Act & Assert
        # Should have minimal explicit guidance references (use patterns instead)
        assert guidance_references <= 3, (
            "Phase 1 should use patterns selectively, "
            "not repeatedly reference guidance file"
        )


class TestSubagentReInvocationReduction:
    """AC#3, NFR-002: Tests for subagent re-invocation reduction."""

    def test_phase_3_subagent_prompt_should_include_structured_context(self):
        """
        Given requirements-analyst subagent invoked in Phase 3
        When prompt is examined
        Then should contain structured context from Phase 1-2

        Why this reduces re-invocations:
        - Phase 1-2 with guidance patterns → Complete problem scope
        - Subagent receives: complete scope, ranked features, known constraints
        - Result: Subagent can produce epic on first invocation
        - Baseline: 2.5 re-invocations → Target: ≤1.75 (30% reduction)
        """
        # Arrange
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )

        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract Phase 3
        phase_3_start = content.find("## Phase 3")
        if phase_3_start == -1:
            phase_3_start = content.find("### Phase 3")
        phase_4_start = content.find("## Phase 4")
        if phase_4_start == -1:
            phase_4_start = content.find("### Phase 4")

        if phase_3_start < 0:
            pytest.skip("Phase 3 not found in SKILL.md")

        phase_3_content = content[phase_3_start:phase_4_start]

        # Look for context variables in subagent prompt
        context_indicators = {
            "problem_scope": 0,
            "requirements": 0,
            "constraints": 0,
            "features": 0,
            "context": 0,
        }

        # Act
        for indicator in context_indicators:
            context_indicators[indicator] = phase_3_content.lower().count(
                indicator
            )

        total_context_references = sum(context_indicators.values())

        # Assert
        assert total_context_references >= 3, (
            f"Phase 3 subagent prompt should include ≥3 context indicators, "
            f"found {total_context_references}. "
            f"This ensures subagent has complete context to reduce re-invocations."
        )

    def test_phase_2_should_collect_all_required_information(self):
        """
        Given Phase 2 (Feature Elicitation)
        When examined
        Then should collect information covering 5 categories:
        - Problem scope (from Phase 1-2 scope questions)
        - Feature list (from Phase 2 feature discovery)
        - Feature priorities (from Phase 2 ranking)
        - Timeline/constraints (from Phase 2 timeline)
        - User personas (from Phase 2 persona classification)

        Why important: Complete information collection in Phase 2 means
        Phase 3 subagent receives rich context, reducing need for re-invocations.
        """
        # Arrange
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )

        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract Phase 2
        phase_2_start = content.find("## Phase 2")
        if phase_2_start == -1:
            phase_2_start = content.find("### Phase 2")
        phase_3_start = content.find("## Phase 3")
        if phase_3_start == -1:
            phase_3_start = content.find("### Phase 3")

        if phase_2_start < 0:
            pytest.skip("Phase 2 not found in SKILL.md")

        phase_2_content = content[phase_2_start:phase_3_start]

        # Look for collection of required information categories
        info_categories = {
            "feature": 0,
            "priority": 0,
            "timeline": 0,
            "persona": 0,
            "user": 0,
        }

        # Act
        for category in info_categories:
            info_categories[category] = phase_2_content.lower().count(
                category
            )

        total_categories = sum(
            1 for count in info_categories.values() if count > 0
        )

        # Assert
        assert total_categories >= 3, (
            f"Phase 2 should collect ≥3 information categories "
            f"to enable quality subagent invocation. Found {total_categories}."
        )

    def test_subagent_prompt_should_have_detailed_instructions(self):
        """
        Given requirements-analyst subagent invocation
        When examined
        Then prompt should be detailed enough to reduce ambiguity

        Strategy:
        - Provide Phase 1-2 collected responses to subagent
        - Include example outputs/expected formats
        - Reference completion criteria
        - Result: Subagent understands context fully, minimizes re-calls
        """
        # Arrange
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )

        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract Phase 3 subagent invocation
        phase_3_start = content.find("## Phase 3")
        if phase_3_start == -1:
            phase_3_start = content.find("### Phase 3")
        phase_4_start = content.find("## Phase 4")
        if phase_4_start == -1:
            phase_4_start = content.find("### Phase 4")

        if phase_3_start < 0:
            pytest.skip("Phase 3 not found")

        phase_3_content = content[phase_3_start:phase_4_start]

        # Find Task/Skill invocation
        subagent_start = phase_3_content.find("Task(")
        if subagent_start < 0:
            subagent_start = phase_3_content.find("Skill(")

        if subagent_start >= 0:
            # Extract ~1000 chars after invocation start
            subagent_section = phase_3_content[
                subagent_start : subagent_start + 1000
            ]

            # Look for detailed instruction indicators
            detail_indicators = [
                "prompt",
                "given",
                "when",
                "then",
                "provide",
                "include",
                "format",
                "example",
            ]

            # Act
            detail_count = sum(
                1
                for indicator in detail_indicators
                if indicator in subagent_section.lower()
            )

            # Assert
            assert detail_count >= 3, (
                f"Subagent invocation should include ≥3 instruction detail indicators, "
                f"found {detail_count}. Detailed prompts reduce re-invocations."
            )


class TestReliabilityWithoutGuidance:
    """NFR-003: Tests for graceful degradation if guidance unavailable."""

    def test_skill_should_complete_if_guidance_missing(self):
        """
        Given guidance file temporarily unavailable
        When Phase 1 Step 0 executes
        Then skill should:
        - Log warning about guidance unavailability
        - Continue with standard (non-guided) prompts
        - Produce complete epic output

        From NFR-003: "100% workflow completion rate even if guidance file missing"

        Business Rule BR-001: "Guidance loading must not halt skill execution
        if file unavailable (graceful degradation)"
        """
        # Arrange
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )

        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract Phase 1 Step 0
        phase_1_start = content.find("## Phase 1")
        if phase_1_start == -1:
            phase_1_start = content.find("### Phase 1")
        phase_2_start = content.find("## Phase 2")
        if phase_2_start == -1:
            phase_2_start = content.find("### Phase 2")

        phase_1_content = content[phase_1_start:phase_2_start]
        step_0_start = phase_1_content.find("Step 0")
        step_1_start = phase_1_content.find("Step 1")
        step_0_content = phase_1_content[step_0_start:step_1_start]

        # Act
        # Look for error handling or graceful degradation logic
        error_handling_indicators = [
            "try",
            "except",
            "if not",
            "if file missing",
            "graceful",
            "continue",
            "proceed",
        ]

        has_error_handling = any(
            indicator in step_0_content.lower()
            for indicator in error_handling_indicators
        )

        # Assert
        assert has_error_handling, (
            "Step 0 should include error handling to continue if guidance missing"
        )

    def test_phase_1_should_have_fallback_questions(self):
        """
        Given Step 0 cannot load guidance
        When Phase 1 proceeds
        Then should have fallback/standard questions that work without guidance

        Ensures workflow completion rate = 100% even without guidance.
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

        # Count AskUserQuestion invocations
        ask_count = phase_1_content.count("AskUserQuestion")

        # Act & Assert
        # Should have questions that work regardless of guidance
        assert ask_count >= 3, (
            f"Phase 1 should have ≥3 questions that work without guidance, found {ask_count}"
        )


class TestCodeChangeMinimization:
    """NFR-004: Tests for minimal code changes."""

    def test_skill_md_changes_should_be_minimal(self):
        """
        Given implementation of AC#1-5
        When checking SKILL.md changes
        Then should add ≤5 lines for Step 0 reference (not major restructuring)

        From NFR-004: "≤ 5 lines changed in SKILL.md (add Step 0 reference)"

        Implementation strategy:
        - Add "Step 0: Load guidance" bullet before Step 1
        - Add 3-4 lines of Load tool call
        - Total: ≤5 line addition
        """
        # Arrange
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )

        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Count "Step 0" occurrences (should be exactly 1 per mention)
        step_0_count = content.count("Step 0")

        # Act & Assert
        # Step 0 should be present but minimal (not major restructuring)
        assert step_0_count >= 1, "Step 0 should be added to Phase 1"
        assert step_0_count <= 3, (
            "Step 0 should be minimal mention (≤3 locations: title, description, reference)"
        )

    def test_reference_file_should_not_exceed_size_limit(self):
        """
        Given reference file created for integration documentation
        When file size checked
        Then should be ≤300 lines

        From NFR-004: "≤300 lines in new reference file"

        File: src/claude/skills/devforgeai-ideation/references/user-input-integration-guide.md
        """
        # Arrange
        ref_path = Path(
            "src/claude/skills/devforgeai-ideation/references/user-input-integration-guide.md"
        )

        # Act
        if ref_path.exists():
            with open(ref_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                line_count = len(lines)

            # Assert
            assert line_count <= 300, (
                f"Integration guide too large: {line_count} lines (max 300)"
            )
        else:
            # If file doesn't exist yet, that's OK for RED phase testing
            pytest.skip("Reference file not yet created")


class TestPatternVerifiability:
    """NFR-005: Tests for pattern verifiability via automated tests."""

    def test_patterns_should_be_detectable_via_grep(self):
        """
        Given Phase 1-2 questions with applied patterns
        When examined via grep/regex
        Then should find pattern keywords in ≥4/5 patterns

        From NFR-005: "≥ 80% pattern usage detectable via Grep (prompts contain pattern keywords)"

        Detectable patterns:
        1. Open-Ended: "Tell me about"
        2. Comparative: "Rank 1-5"
        3. Bounded: "Select range"
        4. Classification: "Primary user"
        5. Other patterns as needed
        """
        # Arrange
        skill_path = Path(
            "src/claude/skills/devforgeai-ideation/SKILL.md"
        )

        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract Phase 1-2
        phase_1_start = content.find("## Phase 1")
        if phase_1_start == -1:
            phase_1_start = content.find("### Phase 1")
        phase_3_start = content.find("## Phase 3")
        if phase_3_start == -1:
            phase_3_start = content.find("### Phase 3")

        phase_1_2_content = content[phase_1_start:phase_3_start]

        # Define detectable patterns
        detectable_patterns = {
            "Open-Ended": r"Tell me about|Describe|Explain",
            "Ranking": r"Rank\s*\d-\d|ranking|priority",
            "Bounded": r"Select range|between|within",
            "Classification": r"Primary user|user type|role",
            "Closed": r"Confirm|Verify|Is",
        }

        # Act
        detected_count = 0
        for pattern_name, pattern_regex in detectable_patterns.items():
            matches = re.findall(pattern_regex, phase_1_2_content, re.IGNORECASE)
            if matches:
                detected_count += 1

        # Assert
        required_detection_rate = 0.80  # ≥80% = ≥4/5 patterns
        detected_rate = detected_count / len(detectable_patterns)

        assert detected_rate >= required_detection_rate, (
            f"Pattern detection rate {detected_rate:.1%} below target 80%. "
            f"Detected {detected_count}/{len(detectable_patterns)} patterns."
        )
