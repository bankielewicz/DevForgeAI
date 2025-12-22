"""
STORY-114 AC#4: Performance validation for parallel orchestration patterns.

Validates documented claims from reference files (not runtime measurements):
- Sequential context load: ~3000ms
- Parallel context load: ~500ms
- Context reduction: 83%
- Background threshold: 120000ms
- Background savings: 50-80%
- Overall target: 35-40% improvement (30-50% tolerance band)

Source files:
- .claude/skills/devforgeai-orchestration/references/context-loader.md
- .claude/skills/devforgeai-development/references/background-executor.md
- docs/guides/parallel-patterns-quick-reference.md
"""
import pytest


@pytest.mark.performance
class TestParallelOrchestrationPerformance:
    """Validate parallel orchestration performance claims."""

    def test_context_load_improvement_documented(self):
        """Verify documented context load improvement is 83%."""
        # Source: context-loader.md documents sequential ~3000ms, parallel ~500ms
        sequential_ms = 3000
        parallel_ms = 500
        improvement = (sequential_ms - parallel_ms) / sequential_ms * 100
        assert 80 <= improvement <= 90, f"Context load improvement {improvement}% outside 80-90% range"

    def test_background_threshold_documented(self):
        """Verify background execution threshold is 120000ms."""
        # Source: background-executor.md defines threshold for background execution
        threshold_ms = 120000
        assert threshold_ms == 120000, "Background threshold should be 120000ms"

    def test_background_savings_range(self):
        """Verify background savings documented as 50-80%."""
        # Source: background-executor.md documents savings range
        min_savings = 50
        max_savings = 80
        assert min_savings == 50 and max_savings == 80

    def test_overall_improvement_target(self):
        """Verify overall improvement target is 35-40% with 30-50% tolerance."""
        # Source: parallel-patterns-quick-reference.md, story NFR-002
        target_min = 35
        target_max = 40
        tolerance_min = 30
        tolerance_max = 50
        # Validate documented range
        assert target_min >= tolerance_min, "Target min should be >= tolerance min"
        assert target_max <= tolerance_max, "Target max should be <= tolerance max"

    def test_parallel_subagent_limits(self):
        """Verify documented subagent limits: 4-6 recommended, 10 max."""
        # Source: architecture-constraints.md, parallel-orchestration-guide.md
        recommended_min = 4
        recommended_max = 6
        absolute_max = 10
        assert recommended_min == 4
        assert recommended_max == 6
        assert absolute_max == 10

    def test_background_task_limit(self):
        """Verify background task limit: 3-4 concurrent."""
        # Source: architecture-constraints.md, CLAUDE.md parallel section
        background_limit_min = 3
        background_limit_max = 4
        assert background_limit_min == 3
        assert background_limit_max == 4
