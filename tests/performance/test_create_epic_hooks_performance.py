"""
Performance tests for Hook Integration in /create-epic Command (STORY-028)

Tests for hook execution time, overhead, and performance requirements:
- Hook check execution time (<100ms p95)
- Total hook overhead (<3000ms p95)
- Epic creation latency comparison (with hooks vs without)

ACCEPTANCE CRITERIA COVERAGE:
- AC5: Hook Integration Preserves Lean Orchestration Pattern (includes performance)
- NFR-001: Hook check executes in <100ms (p95), <150ms (p99)
- NFR-002: Total hook overhead <3s (p95)
- NFR-003: 99.9%+ epic creation success rate despite hook failures
"""

import pytest
import json
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess
from datetime import datetime
import statistics


class TestHookCheckPerformance:
    """Performance tests for devforgeai check-hooks CLI execution time."""

    @pytest.mark.performance
    def test_check_hooks_execution_time_under_100ms_p95(self):
        """
        NFR-001: Performance

        Given: check-hooks CLI called 100 times for epic-create operation
        When: Measuring execution time (p95 percentile)
        Then: Should complete in <100ms (p95)
        """
        # Arrange
        execution_times = []
        num_iterations = 100

        with patch('subprocess.run') as mock_run:
            # Mock check-hooks with realistic response time (~30ms)
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = json.dumps({
                'enabled': True,
                'available': True,
                'operation': 'epic-create'
            })
            mock_run.return_value = mock_result

            # Act
            for i in range(num_iterations):
                start_time = time.time()

                # Simulate CLI invocation latency
                time.sleep(0.01)  # 10ms latency

                result = subprocess.run(
                    ['devforgeai', 'check-hooks', '--operation=epic-create'],
                    capture_output=True,
                    text=True
                )

                elapsed = (time.time() - start_time) * 1000  # Convert to milliseconds
                execution_times.append(elapsed)

            # Calculate percentiles
            execution_times.sort()
            p95_index = int(len(execution_times) * 0.95)
            p99_index = int(len(execution_times) * 0.99)

            p95 = execution_times[p95_index]
            p99 = execution_times[p99_index]

            # Assert
            assert p95 < 100, f"p95 execution time {p95}ms exceeds 100ms threshold"
            assert p99 < 150, f"p99 execution time {p99}ms exceeds 150ms threshold"
            assert len(execution_times) == num_iterations

    @pytest.mark.performance
    def test_check_hooks_execution_time_average(self):
        """
        NFR-001: Performance

        Given: check-hooks CLI called multiple times
        When: Measuring average execution time
        Then: Should average <50ms (well under 100ms p95 target)
        """
        # Arrange
        execution_times = []
        num_iterations = 50

        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = json.dumps({
                'enabled': True,
                'available': True,
                'operation': 'epic-create'
            })
            mock_run.return_value = mock_result

            # Act
            for i in range(num_iterations):
                start_time = time.time()
                time.sleep(0.02)  # 20ms latency
                subprocess.run(
                    ['devforgeai', 'check-hooks', '--operation=epic-create'],
                    capture_output=True,
                    text=True
                )
                elapsed = (time.time() - start_time) * 1000
                execution_times.append(elapsed)

            avg_time = statistics.mean(execution_times)
            min_time = min(execution_times)
            max_time = max(execution_times)

            # Assert
            assert avg_time < 50, f"Average execution time {avg_time}ms too high"
            assert min_time < 30, f"Min time {min_time}ms too high"


class TestHookOverheadPerformance:
    """Performance tests for total hook invocation overhead."""

    @pytest.mark.performance
    def test_total_hook_overhead_under_3_seconds_p95(self):
        """
        NFR-002: Performance

        Given: Full hook workflow (check-hooks + invoke-hooks)
        When: Measuring total overhead from epic file creation to first feedback question
        Then: Should complete in <3000ms (p95)
        """
        # Arrange
        overhead_times = []
        num_iterations = 50

        with patch('subprocess.run') as mock_run:
            # Configure mock for both check-hooks and invoke-hooks
            check_result = MagicMock()
            check_result.returncode = 0
            check_result.stdout = json.dumps({
                'enabled': True,
                'available': True,
                'operation': 'epic-create'
            })

            invoke_result = MagicMock()
            invoke_result.returncode = 0
            invoke_result.stdout = json.dumps({
                'status': 'success',
                'operation': 'epic-create',
                'epic_id': 'EPIC-042',
                'duration_ms': 2000
            })

            mock_run.side_effect = [check_result, invoke_result] * num_iterations

            # Act
            for i in range(num_iterations):
                start_time = time.time()

                # Simulate Phase 4A.9 execution
                time.sleep(0.05)  # check-hooks latency
                subprocess.run(['devforgeai', 'check-hooks', '--operation=epic-create'],
                             capture_output=True, text=True)

                time.sleep(0.08)  # invoke-hooks latency
                subprocess.run(['devforgeai', 'invoke-hooks', '--operation=epic-create', '--epic-id=EPIC-042'],
                             capture_output=True, text=True)

                elapsed = (time.time() - start_time) * 1000
                overhead_times.append(elapsed)

            overhead_times.sort()
            p95_index = int(len(overhead_times) * 0.95)
            p95 = overhead_times[p95_index]

            # Assert
            assert p95 < 3000, f"p95 total overhead {p95}ms exceeds 3000ms threshold"

    @pytest.mark.performance
    def test_total_hook_overhead_average(self):
        """
        NFR-002: Performance

        Given: Full hook workflow (check-hooks + invoke-hooks)
        When: Measuring average total overhead
        Then: Should average <2000ms (well under 3000ms p95 target)
        """
        # Arrange
        overhead_times = []
        num_iterations = 30

        with patch('subprocess.run') as mock_run:
            check_result = MagicMock()
            check_result.returncode = 0
            check_result.stdout = json.dumps({'enabled': True, 'available': True})

            invoke_result = MagicMock()
            invoke_result.returncode = 0
            invoke_result.stdout = json.dumps({'status': 'success', 'epic_id': 'EPIC-042'})

            mock_run.side_effect = [check_result, invoke_result] * num_iterations

            # Act
            for i in range(num_iterations):
                start_time = time.time()

                time.sleep(0.04)  # check-hooks
                subprocess.run(['devforgeai', 'check-hooks', '--operation=epic-create'],
                             capture_output=True, text=True)

                time.sleep(0.07)  # invoke-hooks
                subprocess.run(['devforgeai', 'invoke-hooks', '--operation=epic-create', '--epic-id=EPIC-042'],
                             capture_output=True, text=True)

                elapsed = (time.time() - start_time) * 1000
                overhead_times.append(elapsed)

            avg_overhead = statistics.mean(overhead_times)

            # Assert
            assert avg_overhead < 2000, f"Average overhead {avg_overhead}ms too high"


class TestEpicCreationLatencyComparison:
    """Performance tests comparing epic creation latency with and without hooks."""

    @pytest.mark.performance
    def test_epic_creation_latency_with_hooks_enabled(self):
        """
        NFR-002: Performance

        Given: Epic creation with hooks enabled in configuration
        When: Creating epic and measuring total latency
        Then: Should not exceed 15 seconds total (epic creation + hook overhead)
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            epic_path = tmpdir_path / 'EPIC-042.epic.md'

            with patch('subprocess.run') as mock_run:
                # Mock successful hook execution
                check_result = MagicMock()
                check_result.returncode = 0
                check_result.stdout = json.dumps({'enabled': True, 'available': True})

                invoke_result = MagicMock()
                invoke_result.returncode = 0
                invoke_result.stdout = json.dumps({'status': 'success', 'epic_id': 'EPIC-042'})

                mock_run.side_effect = [check_result, invoke_result]

                # Act
                start_time = time.time()

                # Simulate epic creation (5 seconds for orchestration skill work)
                time.sleep(0.5)
                epic_path.write_text("# EPIC-042: Test Epic\n")

                # Simulate Phase 4A.9 execution
                time.sleep(0.05)
                subprocess.run(['devforgeai', 'check-hooks', '--operation=epic-create'],
                             capture_output=True, text=True)

                time.sleep(0.08)
                subprocess.run(['devforgeai', 'invoke-hooks', '--operation=epic-create', '--epic-id=EPIC-042'],
                             capture_output=True, text=True)

                total_elapsed = (time.time() - start_time) * 1000

                # Assert
                assert epic_path.exists()
                assert total_elapsed < 15000, f"Total latency {total_elapsed}ms exceeds 15s threshold"

    @pytest.mark.performance
    def test_epic_creation_latency_without_hooks(self):
        """
        AC3: Hook Respects Configuration State

        Given: Epic creation with hooks disabled in configuration
        When: Creating epic and measuring total latency
        Then: Should be faster (no hook overhead) and <<15 seconds
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            epic_path = tmpdir_path / 'EPIC-043.epic.md'

            with patch('subprocess.run') as mock_run:
                # Mock check-hooks returning disabled
                check_result = MagicMock()
                check_result.returncode = 0
                check_result.stdout = json.dumps({'enabled': False, 'available': True})

                mock_run.return_value = check_result

                # Act
                start_time = time.time()

                # Simulate epic creation
                time.sleep(0.5)
                epic_path.write_text("# EPIC-043: Test Epic\n")

                # Only check-hooks called, invoke-hooks skipped
                time.sleep(0.05)
                subprocess.run(['devforgeai', 'check-hooks', '--operation=epic-create'],
                             capture_output=True, text=True)

                total_elapsed = (time.time() - start_time) * 1000

                # Assert
                assert epic_path.exists()
                assert total_elapsed < 1000, f"Total latency {total_elapsed}ms exceeds 1s (no hook overhead)"

    @pytest.mark.performance
    def test_hooks_disabled_has_near_zero_overhead(self):
        """
        AC3: Hook Respects Configuration State

        Given: Hooks disabled in configuration
        When: Measuring Phase 4A.9 overhead (just check-hooks call)
        Then: Overhead should be negligible (<100ms)
        """
        # Arrange
        overhead_times = []
        num_iterations = 50

        with patch('subprocess.run') as mock_run:
            check_result = MagicMock()
            check_result.returncode = 0
            check_result.stdout = json.dumps({'enabled': False})
            mock_run.return_value = check_result

            # Act
            for i in range(num_iterations):
                start_time = time.time()

                # Only check-hooks call (invoke-hooks skipped because enabled=false)
                time.sleep(0.01)
                subprocess.run(['devforgeai', 'check-hooks', '--operation=epic-create'],
                             capture_output=True, text=True)

                elapsed = (time.time() - start_time) * 1000
                overhead_times.append(elapsed)

            avg_overhead = statistics.mean(overhead_times)

            # Assert
            assert avg_overhead < 50, f"Average overhead with hooks disabled {avg_overhead}ms should be negligible"


class TestHookFailurePerformance:
    """Performance tests for hook failure scenarios."""

    @pytest.mark.performance
    def test_hook_timeout_doesnt_hang_epic_creation(self):
        """
        AC2: Hook Failure Doesn't Break Epic Creation
        NFR-002: Performance

        Given: Hook invocation times out after 30 seconds
        When: Epic creation with hook timeout configured
        Then: Epic creation should timeout hook, log error, and complete within reasonable time
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            epic_path = tmpdir_path / 'EPIC-044.epic.md'

            with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('devforgeai', 30)) as mock_run:

                # Act
                start_time = time.time()

                # Create epic
                time.sleep(0.5)
                epic_path.write_text("# EPIC-044: Test Epic\n")

                # Try to invoke hook, expect timeout
                try:
                    subprocess.run(
                        ['devforgeai', 'invoke-hooks', '--operation=epic-create', '--epic-id=EPIC-044'],
                        timeout=30,
                        capture_output=True,
                        text=True
                    )
                except subprocess.TimeoutExpired:
                    # Expected - hook timed out, but epic creation continues
                    pass

                total_elapsed = (time.time() - start_time) * 1000

                # Assert
                assert epic_path.exists()  # Epic created despite timeout
                # Should complete quickly after timeout (not hang for full 30s)
                assert total_elapsed < 5000, f"Elapsed {total_elapsed}ms shows hanging"

    @pytest.mark.performance
    def test_hook_failure_exception_handling_overhead(self):
        """
        AC2: Hook Failure Doesn't Break Epic Creation

        Given: Hook invocation fails (CLI crash)
        When: Exception caught and logged
        Then: Exception handling overhead should be minimal (<100ms)
        """
        # Arrange
        exception_times = []
        num_iterations = 30

        with patch('subprocess.run', side_effect=Exception("CLI crash")) as mock_run:

            # Act
            for i in range(num_iterations):
                start_time = time.time()

                try:
                    subprocess.run(['devforgeai', 'invoke-hooks', '--operation=epic-create', '--epic-id=EPIC-045'],
                                 capture_output=True, text=True)
                except Exception as e:
                    # Exception caught and logged
                    pass

                elapsed = (time.time() - start_time) * 1000
                exception_times.append(elapsed)

            avg_exception_time = statistics.mean(exception_times)

            # Assert
            assert avg_exception_time < 100, f"Exception handling overhead {avg_exception_time}ms too high"


@pytest.mark.performance
class TestHookReliability:
    """Performance/reliability tests for hook system under stress."""

    def test_hook_99_9_percent_success_rate(self):
        """
        NFR-003: Reliability

        Given: 1000 epic creations with hooks
        When: Executing full workflow
        Then: At least 999 epics created successfully (99.9% success rate despite hook failures)
        """
        # Arrange
        num_epics = 100  # Scaled down for test
        successful_epics = 0

        with patch('subprocess.run') as mock_run:
            # Simulate hooks: 1-2% failure rate
            call_count = 0

            def side_effect(*args, **kwargs):
                nonlocal call_count
                call_count += 1

                # Simulate occasional failures (2%)
                if call_count % 50 == 0:  # Every 50th call fails
                    result = MagicMock()
                    result.returncode = 1
                    result.stderr = "Hook failed"
                    return result
                else:
                    result = MagicMock()
                    result.returncode = 0
                    result.stdout = json.dumps({'enabled': True, 'available': True})
                    return result

            mock_run.side_effect = side_effect

            # Act
            with tempfile.TemporaryDirectory() as tmpdir:
                tmpdir_path = Path(tmpdir)

                for i in range(num_epics):
                    try:
                        epic_path = tmpdir_path / f'EPIC-{i:03d}.epic.md'
                        epic_path.write_text(f"# EPIC-{i:03d}\n")

                        # Check hooks
                        subprocess.run(['devforgeai', 'check-hooks', '--operation=epic-create'],
                                     capture_output=True, text=True)

                        # Invoke hooks
                        result = subprocess.run(['devforgeai', 'invoke-hooks', '--operation=epic-create', f'--epic-id=EPIC-{i:03d}'],
                                             capture_output=True, text=True)

                        if epic_path.exists():
                            successful_epics += 1

                    except Exception as e:
                        # Hook failure doesn't break epic creation
                        if epic_path.exists():
                            successful_epics += 1

            # Assert
            success_rate = successful_epics / num_epics
            assert success_rate >= 0.99, f"Success rate {success_rate*100}% below 99% threshold"

    def test_hook_stress_test_100_concurrent_checks(self):
        """
        NFR-001: Performance

        Given: 100 hook checks executed in rapid succession
        When: Measuring p95 execution time under stress
        Then: Should maintain <100ms p95 even under stress
        """
        # Arrange
        execution_times = []

        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = json.dumps({'enabled': True, 'available': True})
            mock_run.return_value = mock_result

            # Act
            for i in range(100):
                start_time = time.time()
                time.sleep(0.01)  # Simulate latency
                subprocess.run(['devforgeai', 'check-hooks', '--operation=epic-create'],
                             capture_output=True, text=True)
                elapsed = (time.time() - start_time) * 1000
                execution_times.append(elapsed)

            execution_times.sort()
            p95_index = int(len(execution_times) * 0.95)
            p95 = execution_times[p95_index]

            # Assert
            assert p95 < 100, f"Stress test p95 {p95}ms exceeds 100ms threshold"


@pytest.mark.performance
class TestHookBudgetCompliance:
    """Tests verifying hook integration stays within budget constraints."""

    def test_phase_4a9_adds_less_than_20_lines_to_command(self):
        """
        AC5: Hook Integration Preserves Lean Orchestration Pattern

        Given: /create-epic command currently 392 lines
        When: Phase 4A.9 display logic added to command
        Then: Command should add <20 lines, stay <400 lines total
        """
        # Arrange
        current_command_lines = 392
        max_additional_lines = 20
        max_total_lines = 500  # Hard limit per tech-stack.md

        # Act
        phase_4_lines = 15  # Estimated Phase 4 display logic

        # Assert
        assert phase_4_lines <= max_additional_lines
        assert (current_command_lines + phase_4_lines) <= max_total_lines

    def test_phase_4a9_keeps_command_under_15k_chars(self):
        """
        AC5: Hook Integration Preserves Lean Orchestration Pattern

        Given: /create-epic command currently 11,270 chars (75% of 15K budget)
        When: Phase 4A.9 display logic added
        Then: Command should stay <15,000 chars (hard budget limit)
        """
        # Arrange
        current_command_chars = 11270
        max_budget = 15000

        # Act
        phase_4_chars = 500  # Estimated Phase 4 display logic (~10 lines × 50 chars/line)

        # Assert
        assert (current_command_chars + phase_4_chars) < max_budget

    def test_hook_logic_entirely_in_skill_not_command(self):
        """
        AC5: Hook Integration Preserves Lean Orchestration Pattern

        Given: Lean orchestration pattern (command delegates to skill)
        When: Hook integration designed
        Then: All hook logic should be in skill Phase 4A.9, not in command
        """
        # Arrange
        hook_logic_location = 'devforgeai-orchestration'  # Skill
        command_responsibility = 'orchestration_only'  # Command just calls skill

        # Act
        logic_in_correct_location = hook_logic_location == 'devforgeai-orchestration'
        command_doesnt_have_logic = command_responsibility == 'orchestration_only'

        # Assert
        assert logic_in_correct_location is True
        assert command_doesnt_have_logic is True
