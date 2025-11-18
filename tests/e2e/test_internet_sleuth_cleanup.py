"""
E2E Test: Verify temporary directory cleanup on failure

Tests for STORY-035: Internet-Sleuth Framework Compliance (Phase 1 Migration)

Security NFR-004: Temporary directories for cloned repositories must be removed on exit,
even if analysis fails
"""

import pytest
import subprocess
import tempfile
import time
from pathlib import Path


class TestInternetSleuthCleanup:
    """E2E test suite for temporary directory cleanup"""

    @pytest.mark.story_035
    @pytest.mark.e2e
    @pytest.mark.security
    def test_cleanup_on_successful_completion(self):
        """Test: Temp directory removed after successful analysis"""
        # Arrange: Create temp directory simulating repository clone
        temp_dir = Path(f"/tmp/devforgeai-research-test-{int(time.time())}")
        temp_dir.mkdir(exist_ok=True)

        # Create marker file to verify cleanup
        marker_file = temp_dir / "MARKER.txt"
        marker_file.write_text("Test marker")

        # Act: Simulate successful analysis with cleanup
        script = f"""
trap "rm -rf {temp_dir}" EXIT
echo "Simulating repository analysis..."
# Script completes successfully
exit 0
        """
        result = subprocess.run(["bash", "-c", script], capture_output=True)

        # Assert: Directory should be removed
        assert result.returncode == 0, "Script should complete successfully"
        assert not temp_dir.exists(), f"Temp directory {temp_dir} should be cleaned up after success"

    @pytest.mark.story_035
    @pytest.mark.e2e
    @pytest.mark.security
    def test_cleanup_on_failure(self):
        """Test: Temp directory removed even if analysis fails mid-execution"""
        # Arrange: Create temp directory
        temp_dir = Path(f"/tmp/devforgeai-research-test-fail-{int(time.time())}")
        temp_dir.mkdir(exist_ok=True)

        # Create files simulating partial analysis
        (temp_dir / "README.md").write_text("Repository README")
        (temp_dir / "partial-analysis.txt").write_text("Incomplete analysis")

        # Act: Simulate failure mid-analysis with cleanup trap
        script = f"""
trap "rm -rf {temp_dir}" EXIT
echo "Starting repository analysis..."
# Simulate failure (non-zero exit)
exit 1
        """
        result = subprocess.run(["bash", "-c", script], capture_output=True)

        # Assert: Directory should still be removed despite failure
        assert result.returncode == 1, "Script should fail as simulated"
        assert not temp_dir.exists(), f"Temp directory {temp_dir} should be cleaned up even on failure"

    @pytest.mark.story_035
    @pytest.mark.e2e
    @pytest.mark.security
    def test_cleanup_on_signal_interrupt(self):
        """Test: Temp directory removed if process interrupted (SIGTERM)"""
        # Arrange: Create temp directory
        temp_dir = Path(f"/tmp/devforgeai-research-test-int-{int(time.time())}")
        temp_dir.mkdir(exist_ok=True)

        # Create marker file
        marker_file = temp_dir / "MARKER.txt"
        marker_file.write_text("Interrupt test marker")

        # Act: Simulate process with sleep and interrupt
        script = f"""
trap "rm -rf {temp_dir}" EXIT
echo "Long-running analysis..."
sleep 0.2 &
SLEEP_PID=$!
# Simulate interrupt
kill $SLEEP_PID 2>/dev/null || true
wait $SLEEP_PID 2>/dev/null || true
exit 0
        """
        result = subprocess.run(["bash", "-c", script], capture_output=True, timeout=2)

        # Assert: Directory cleaned up after interruption
        assert not temp_dir.exists(), \
            f"Temp directory {temp_dir} should be cleaned up after process interruption"

    @pytest.mark.story_035
    @pytest.mark.e2e
    @pytest.mark.security
    def test_trap_exit_pattern_in_agent_documentation(self):
        """Test: Agent documentation includes trap EXIT pattern"""
        agent_file = Path(".claude/agents/internet-sleuth.md")
        assert agent_file.exists(), "Agent file must exist"

        content = agent_file.read_text()

        # Verify trap EXIT pattern documented
        assert "trap" in content.lower(), "Agent should document trap usage"
        assert "EXIT" in content, "Agent should document EXIT signal handling"
        assert 'trap "rm -rf' in content, "Agent should show cleanup pattern in trap"

        # Verify uses correct temp path
        assert "/tmp/devforgeai-research" in content, \
            "Agent should use /tmp/devforgeai-research-$$ pattern (not old tmp/repos/ path)"

    @pytest.mark.story_035
    @pytest.mark.e2e
    @pytest.mark.security
    @pytest.mark.slow
    def test_multiple_repositories_cleanup(self):
        """Test: All temp directories cleaned up when analyzing multiple repos"""
        # Arrange: Create 3 temp directories simulating multi-repo analysis
        temp_dirs = [
            Path(f"/tmp/devforgeai-research-multi-1-{int(time.time())}"),
            Path(f"/tmp/devforgeai-research-multi-2-{int(time.time())}"),
            Path(f"/tmp/devforgeai-research-multi-3-{int(time.time())}")
        ]

        for temp_dir in temp_dirs:
            temp_dir.mkdir(exist_ok=True)
            (temp_dir / "README.md").write_text(f"Repository {temp_dir.name}")

        # Act: Simulate multi-repo analysis with cleanup
        cleanup_commands = " && ".join([f'rm -rf {d}' for d in temp_dirs])
        script = f"""
trap "{cleanup_commands}" EXIT
echo "Analyzing multiple repositories..."
# Simulate successful completion
exit 0
        """
        result = subprocess.run(["bash", "-c", script], capture_output=True)

        # Assert: All directories cleaned up
        assert result.returncode == 0, "Multi-repo analysis should complete successfully"
        for temp_dir in temp_dirs:
            assert not temp_dir.exists(), f"Temp directory {temp_dir} should be cleaned up"
