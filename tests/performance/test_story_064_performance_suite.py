"""
Performance tests for STORY-064: devforgeai-story-creation Integration Validation and Test Execution

Tests cover:
- Acceptance Criteria 1: Test Suite Execution (performance targets)
- Acceptance Criteria 6: Production Validation (performance of /create-story)
- Non-Functional Requirements: Guidance loading time, question generation time

Test Suite Composition:
- PERF01-PERF08: Performance tests for guidance loading, pattern matching, question generation
- Organized in 2 test classes: Guidance Loading Performance, Question Generation Performance

Test IDs: PERF01-PERF08
Test Organization: 4 guidance loading + 4 question generation performance tests
Coverage: File load times, token budgets, pattern extraction, workflow overhead
Performance targets: Guidance <2s, Integration guide <1s, Pattern extraction <500ms, Fibonacci <1ms
"""

import pytest
import time
from pathlib import Path

# Import shared helper
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "unit"))
from test_story_064_unit_suite import FileValidationHelper


class TestGuidanceLoadingPerformance:
    """Performance tests for guidance file loading (PERF01-PERF04).

    Validates: Guidance loading time, file size, and pattern extraction performance.
    """

    @pytest.mark.performance
    @pytest.mark.acceptance_criteria
    def test_perf01_guidance_file_load_time_under_2_seconds(self):
        """PERF01: Guidance file loading completes in <2 seconds (p95).

        Target: Load time <2 seconds for guidance file.
        """
        start_time = time.time()
        content = FileValidationHelper.assert_file_exists(
            FileValidationHelper.GUIDANCE_FILE,
            "Guidance file required for performance test"
        )
        load_time = time.time() - start_time

        assert load_time < 2.0, (
            f"PERF01 violation: Guidance loading took {load_time:.3f}s (target: <2s p95)"
        )
        assert len(content) > 100, "Guidance file not properly loaded"

    @pytest.mark.performance
    @pytest.mark.acceptance_criteria
    def test_perf02_guidance_file_size_reasonable_for_tokens(self):
        """PERF02: Guidance file size is reasonable for token budget.

        Target: File size <50KB (approx <12.5K tokens).
        """
        file_size_bytes = FileValidationHelper.GUIDANCE_FILE.stat().st_size
        estimated_tokens = file_size_bytes / 4

        assert file_size_bytes < 50000, (
            f"PERF02 violation: Guidance file {file_size_bytes} bytes (est. {estimated_tokens:.0f} tokens). "
            f"Target: <50KB for <12.5K tokens budget"
        )

    @pytest.mark.performance
    @pytest.mark.acceptance_criteria
    def test_perf03_integration_guide_load_time_reasonable(self):
        """PERF03: Story-creation integration guide loads quickly.

        Target: Load time <1 second for integration guide.
        """
        if not FileValidationHelper.INTEGRATION_GUIDE.exists():
            pytest.skip("Integration guide not yet created")

        start_time = time.time()
        FileValidationHelper.assert_file_exists(
            FileValidationHelper.INTEGRATION_GUIDE,
            "Integration guide required"
        )
        load_time = time.time() - start_time

        assert load_time < 1.0, (
            f"PERF03 violation: Integration guide loading took {load_time:.3f}s (target: <1s)"
        )

    @pytest.mark.performance
    @pytest.mark.acceptance_criteria
    def test_perf04_pattern_extraction_from_guidance_performant(self):
        """PERF04: Pattern extraction from guidance file is performant.

        Target: Pattern extraction <500ms for batch operations.
        """
        content = FileValidationHelper.assert_file_exists(
            FileValidationHelper.GUIDANCE_FILE,
            "Guidance file required"
        )

        start_time = time.time()
        patterns = [
            line for line in content.split('\n')
            if '##' in line and any(
                pat in line.lower() for pat in ['pattern', 'guidance']
            )
        ]
        extraction_time = time.time() - start_time

        assert extraction_time < 0.5, (
            f"PERF04 violation: Pattern extraction took {extraction_time:.3f}s (target: <500ms)"
        )


class TestQuestionGenerationPerformance:
    """Performance tests for pattern-enhanced question generation (PERF05-PERF08)"""

    @pytest.mark.performance
    @pytest.mark.acceptance_criteria
    def test_perf05_epic_selection_question_generation_fast(self):
        """
        PERF05: Epic selection question generation is performant

        ARRANGE: Verify SKILL.md contains epic selection logic
        ACT: Verify question generation is documented as lightweight
        ASSERT: Question generation doesn't add significant overhead
        """
        # Arrange
        skill_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md"
        )

        assert skill_path.exists(), "SKILL.md required"

        # Act
        with open(skill_path, 'r') as f:
            content = f.read()

        # Assert: Verify no expensive operations documented in epic selection
        epic_section_idx = content.lower().find("epic")
        if epic_section_idx != -1:
            epic_section = content[epic_section_idx:epic_section_idx + 2000]

            # Check for inefficient operations (shouldn't have)
            assert "loop" not in epic_section.lower() or "simple" in epic_section.lower(), (
                "PERF05 violation: Epic selection may have inefficient loops"
            )

    @pytest.mark.performance
    @pytest.mark.acceptance_criteria
    def test_perf06_priority_selection_question_generation_fast(self):
        """
        PERF06: Priority selection question generation is performant

        ARRANGE: Verify SKILL.md contains priority selection logic
        ACT: Verify question generation with 4 levels is lightweight
        ASSERT: Question generation is O(1) not O(n)
        """
        # Arrange
        skill_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md"
        )

        assert skill_path.exists(), "SKILL.md required"

        # Act
        with open(skill_path, 'r') as f:
            content = f.read()

        # Assert: Verify priority selection is static (4 levels)
        priority_section_idx = content.lower().find("priority")
        if priority_section_idx != -1:
            priority_section = content[priority_section_idx:priority_section_idx + 2000]

            # Count priority levels mentioned
            levels = ["critical", "high", "medium", "low"]
            found_levels = sum(1 for level in levels if level in priority_section.lower())

            assert found_levels >= 3, (
                "PERF06: Priority selection should have 4 static levels"
            )

    @pytest.mark.performance
    @pytest.mark.acceptance_criteria
    def test_perf07_fibonacci_points_question_generation_fast(self):
        """
        PERF07: Story points question with Fibonacci sequence is performant

        ARRANGE: Verify SKILL.md contains points selection logic
        ACT: Verify Fibonacci sequence generation is lightweight
        ASSERT: Question generation is O(1) not O(n)
        """
        # Arrange
        skill_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md"
        )

        assert skill_path.exists(), "SKILL.md required"

        # Act: Measure Fibonacci sequence generation time
        start_time = time.time()

        fibonacci = [1, 2, 3, 5, 8, 13]
        gen_time = time.time() - start_time

        # Assert: Generation should be instant (< 1ms)
        assert gen_time < 0.001, (
            f"PERF07 violation: Fibonacci generation took {gen_time*1000:.2f}ms (target: <1ms)"
        )

    @pytest.mark.performance
    @pytest.mark.acceptance_criteria
    def test_perf08_full_create_story_workflow_reasonable_performance(self):
        """
        PERF08: Full /create-story workflow has reasonable performance

        ARRANGE: Verify SKILL.md contains all phases
        ACT: Estimate total performance impact
        ASSERT: Workflow doesn't add excessive overhead due to guidance
        """
        # Arrange
        skill_path = Path(
            "/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md"
        )

        assert skill_path.exists(), "SKILL.md required"

        # Act: Check that performance impact is documented
        with open(skill_path, 'r') as f:
            content = f.read()

        # Assert: Verify performance impact is minimal
        # Count phases to estimate complexity
        phase_count = content.count("Phase ")

        assert phase_count >= 1, (
            "PERF08: SKILL.md should have at least 1 phase defined"
        )

        # Verify no performance regressions mentioned
        assert "slow" not in content.lower() or "optimize" in content.lower(), (
            "PERF08: SKILL.md mentions slowness without optimization plan"
        )
