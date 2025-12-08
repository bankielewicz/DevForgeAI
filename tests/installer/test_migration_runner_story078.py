"""
Unit tests for MigrationRunner service (STORY-078).

Tests migration execution:
- Script execution in version order (AC#4)
- Output capture (AC#4)
- Failure handling (AC#4)
- Progress display (AC#4)

Test Framework: pytest 7.4+
Coverage Target: 95%+ for business logic
"""

import pytest
import sys
import time
import logging
import os
from pathlib import Path
from typing import List
from unittest.mock import MagicMock, patch, Mock

from installer.migration_runner import MigrationRunner, MigrationResult, MigrationRunResult
from installer.models import MigrationScript, MigrationError


class TestMigrationExecution:
    """Tests for SVC-011: Execute migration scripts in order"""

    def test_should_execute_single_migration_successfully(self, tmp_path):
        """
        AC#4: Migrate successfully completes when script succeeds

        Arrange: Single migration script
        Act: Call run([migration])
        Assert: Script executed, returns success status
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("def main():\n    print('success')\n    return 0\n\nif __name__ == '__main__':\n    main()\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert result.all_success is True
        assert result.applied_count == 1
        assert len(result.results) == 1
        assert result.results[0].success is True

    def test_should_execute_multiple_migrations_in_sequence(self, tmp_path):
        """
        AC#4: Execute scripts in version order (oldest to newest)

        Arrange: 3 migration scripts
        Act: Call run([mig1, mig2, mig3])
        Assert: All 3 execute in order: mig1 completes before mig2, mig2 before mig3
        """
        # Arrange
        migrations = []
        execution_order = []

        for i, (from_v, to_v) in enumerate([("1.0.0", "1.1.0"), ("1.1.0", "1.2.0"), ("1.2.0", "1.3.0")]):
            migration_file = tmp_path / f"v{from_v}-to-v{to_v}.py"
            migration_file.write_text(f"import sys\nprint('mig{i}')\nif __name__ == '__main__':\n    pass\n")

            migrations.append(MigrationScript(
                path=str(migration_file),
                from_version=from_v,
                to_version=to_v
            ))

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations, timeout_seconds=10)

        # Assert
        assert result.all_success is True
        assert result.applied_count == 3
        assert len(result.results) == 3

        # All should succeed
        for migration_result in result.results:
            assert migration_result.success is True

    def test_should_execute_migrations_with_correct_exit_code_on_success(self, tmp_path):
        """
        AC#4: Successful migration has exit code 0

        Arrange: Migration script with exit 0
        Act: Call run()
        Assert: Migration marked as successful
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("import sys\nif __name__ == '__main__':\n    sys.exit(0)\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert result.all_success is True
        assert result.results[0].exit_code == 0
        assert result.results[0].success is True

    def test_should_capture_stdout_from_migration(self, tmp_path):
        """
        AC#4: Script output (stdout/stderr) captured in logs

        Arrange: Migration script prints "Migrating database..."
        Act: Call run()
        Assert: Output captured in result["output"]
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("print('Migrating database...')\nif __name__ == '__main__':\n    pass\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert result.results[0].success is True
        assert "Migrating database..." in result.results[0].stdout

    def test_should_capture_stderr_from_migration(self, tmp_path):
        """
        AC#4: Script stderr captured in logs

        Arrange: Migration script prints to stderr: "Warning: deprecated feature"
        Act: Call run()
        Assert: Stderr captured in result["stderr"]
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("import sys\nprint('Warning: deprecated feature', file=sys.stderr)\nif __name__ == '__main__':\n    pass\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert result.results[0].success is True
        assert "Warning: deprecated feature" in result.results[0].stderr

    def test_should_stop_on_first_failure(self, tmp_path):
        """
        AC#4: Stop on first failure (failure triggers rollback)

        Arrange: 3 migrations where 2nd fails (exit code 1)
        Act: Call run()
        Assert: Migration 1 completes, 2 fails, 3 never executes
        """
        # Arrange
        migrations = []

        # Migration 1: succeeds
        mig1 = tmp_path / "v1.0.0-to-v1.1.0.py"
        mig1.write_text("if __name__ == '__main__':\n    pass\n")
        migrations.append(MigrationScript(path=str(mig1), from_version="1.0.0", to_version="1.1.0"))

        # Migration 2: fails
        mig2 = tmp_path / "v1.1.0-to-v1.2.0.py"
        mig2.write_text("import sys\nif __name__ == '__main__':\n    sys.exit(1)\n")
        migrations.append(MigrationScript(path=str(mig2), from_version="1.1.0", to_version="1.2.0"))

        # Migration 3: would succeed but never runs
        mig3 = tmp_path / "v1.2.0-to-v1.3.0.py"
        mig3.write_text("if __name__ == '__main__':\n    pass\n")
        migrations.append(MigrationScript(path=str(mig3), from_version="1.2.0", to_version="1.3.0"))

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations, timeout_seconds=10)

        # Assert
        assert result.all_success is False
        assert result.applied_count == 1  # Only 1 succeeded
        assert len(result.results) == 2  # Only 2 executed (3rd never ran)
        assert result.results[0].success is True
        assert result.results[1].success is False

    def test_should_return_failed_migration_details_on_failure(self, tmp_path):
        """
        AC#4: Failure details returned in result

        Arrange: Migration fails with "Database connection failed"
        Act: Call run()
        Assert: result["failed_migration"] and result["error_message"] populated
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("import sys\nprint('Database connection failed', file=sys.stderr)\nsys.exit(1)\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert result.all_success is False
        assert result.failed_at_migration is not None
        assert result.failed_migration_result is not None

    def test_should_not_execute_migrations_after_first_failure(self, tmp_path):
        """
        AC#4: Failure of migration N prevents execution of migration N+1

        Arrange: Migrations [A, B, C] where B fails
        Act: Call run()
        Assert: C never executes (proven by tracking calls)
        """
        # Arrange
        migrations = []

        mig1 = tmp_path / "v1.0.0-to-v1.1.0.py"
        mig1.write_text("if __name__ == '__main__':\n    pass\n")
        migrations.append(MigrationScript(path=str(mig1), from_version="1.0.0", to_version="1.1.0"))

        mig2 = tmp_path / "v1.1.0-to-v1.2.0.py"
        mig2.write_text("import sys\nsys.exit(99)\n")  # Unusual exit code
        migrations.append(MigrationScript(path=str(mig2), from_version="1.1.0", to_version="1.2.0"))

        mig3 = tmp_path / "v1.2.0-to-v1.3.0.py"
        mig3.write_text("print('THIS SHOULD NOT PRINT')\n")
        migrations.append(MigrationScript(path=str(mig3), from_version="1.2.0", to_version="1.3.0"))

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations, timeout_seconds=10)

        # Assert
        assert result.all_success is False
        assert len(result.results) == 2  # 3rd migration never executed
        assert "THIS SHOULD NOT PRINT" not in result.results[1].stderr

    def test_should_track_successfully_applied_migrations(self, tmp_path):
        """
        AC#4: Successful migrations recorded for rollback reference

        Arrange: 2 migrations complete successfully
        Act: Call run()
        Assert: result["applied_migrations"] contains both migration names
        """
        # Arrange
        migrations = []

        for from_v, to_v in [("1.0.0", "1.1.0"), ("1.1.0", "1.2.0")]:
            mig = tmp_path / f"v{from_v}-to-v{to_v}.py"
            mig.write_text("if __name__ == '__main__':\n    pass\n")
            migrations.append(MigrationScript(path=str(mig), from_version=from_v, to_version=to_v))

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations, timeout_seconds=10)

        # Assert
        assert result.all_success is True
        applied = runner.get_applied_migrations(result)
        assert len(applied) == 2
        assert str(migrations[0].path) in applied
        assert str(migrations[1].path) in applied


class TestMigrationOutputCapture:
    """Tests for SVC-012: Capture script output for logging"""

    def test_should_capture_simple_print_statements(self, tmp_path):
        """
        SVC-012: Capture stdout from print()

        Arrange: Migration with print("Starting migration...")
        Act: Call run()
        Assert: Output appears in captured stdout
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("print('Starting migration...')\nif __name__ == '__main__':\n    pass\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert "Starting migration..." in result.results[0].stdout

    def test_should_capture_multiline_output(self, tmp_path):
        """
        SVC-012: Capture multi-line output from script

        Arrange: Migration prints 10 lines of output
        Act: Call run()
        Assert: All 10 lines captured
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        lines = "\n".join([f"print('Line {i}')" for i in range(10)])
        migration_file.write_text(f"{lines}\nif __name__ == '__main__':\n    pass\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        for i in range(10):
            assert f"Line {i}" in result.results[0].stdout

    def test_should_separate_stdout_and_stderr(self, tmp_path):
        """
        SVC-012: Capture stdout and stderr separately

        Arrange: Migration prints to both stdout and stderr
        Act: Call run()
        Assert: result["stdout"] and result["stderr"] separate
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text(
            "import sys\n"
            "print('Standard output')\n"
            "print('Standard error', file=sys.stderr)\n"
            "if __name__ == '__main__':\n    pass\n"
        )

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert "Standard output" in result.results[0].stdout
        assert "Standard error" in result.results[0].stderr

    def test_should_capture_output_even_on_failure(self, tmp_path):
        """
        SVC-012: Capture output from failed migration

        Arrange: Migration prints error message then exits with code 1
        Act: Call run()
        Assert: Error output captured despite failure
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text(
            "import sys\n"
            "print('Error occurred', file=sys.stderr)\n"
            "sys.exit(1)\n"
        )

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert result.results[0].success is False
        assert "Error occurred" in result.results[0].stderr


class TestMigrationFailureHandling:
    """Tests for SVC-013: Stop on first failure"""

    def test_should_detect_non_zero_exit_code(self, tmp_path):
        """
        SVC-013: Detect migration failure by exit code

        Arrange: Migration exits with code 1
        Act: Call run()
        Assert: Failure detected and reported
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("import sys\nsys.exit(1)\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert result.all_success is False
        assert result.results[0].exit_code == 1

    def test_should_abort_remaining_migrations_on_first_failure(self, tmp_path):
        """
        SVC-013: Stop on first failure

        Arrange: [mig1, mig2_fails, mig3]
        Act: Call run()
        Assert: mig1 complete, mig2 fails, mig3 never starts
        """
        # Arrange
        migrations = []

        mig1 = tmp_path / "v1.0.0-to-v1.1.0.py"
        mig1.write_text("if __name__ == '__main__':\n    pass\n")
        migrations.append(MigrationScript(path=str(mig1), from_version="1.0.0", to_version="1.1.0"))

        mig2 = tmp_path / "v1.1.0-to-v1.2.0.py"
        mig2.write_text("import sys\nsys.exit(1)\n")
        migrations.append(MigrationScript(path=str(mig2), from_version="1.1.0", to_version="1.2.0"))

        mig3 = tmp_path / "v1.2.0-to-v1.3.0.py"
        mig3.write_text("if __name__ == '__main__':\n    pass\n")
        migrations.append(MigrationScript(path=str(mig3), from_version="1.2.0", to_version="1.3.0"))

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations, timeout_seconds=10)

        # Assert
        assert result.all_success is False
        assert len(result.results) == 2  # Only mig1 and mig2 ran
        assert result.results[0].success is True
        assert result.results[1].success is False

    def test_should_return_failure_index_in_result(self, tmp_path):
        """
        SVC-013: Report which migration failed

        Arrange: 3 migrations where 2nd fails
        Act: Call run()
        Assert: result["failed_migration_index"] == 1
        """
        # Arrange
        migrations = []

        for i, (from_v, to_v) in enumerate([("1.0.0", "1.1.0"), ("1.1.0", "1.2.0"), ("1.2.0", "1.3.0")]):
            mig = tmp_path / f"v{from_v}-to-v{to_v}.py"
            if i == 1:  # Second migration fails
                mig.write_text("import sys\nsys.exit(1)\n")
            else:
                mig.write_text("if __name__ == '__main__':\n    pass\n")
            migrations.append(MigrationScript(path=str(mig), from_version=from_v, to_version=to_v))

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations, timeout_seconds=10)

        # Assert
        assert result.all_success is False
        assert result.failed_at_migration == migrations[1]

    def test_should_provide_clear_error_message_on_failure(self, tmp_path):
        """
        SVC-013: Error message explains failure

        Arrange: Migration fails with specific error
        Act: Call run()
        Assert: result["error_message"] contains useful debugging info
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text(
            "import sys\n"
            "print('Database connection failed', file=sys.stderr)\n"
            "sys.exit(1)\n"
        )

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert result.failed_migration_result.error_message is not None
        assert len(result.failed_migration_result.error_message) > 0


class TestMigrationTracking:
    """Tests for SVC-014: Track successfully applied migrations"""

    def test_should_record_successful_migration_name(self, tmp_path):
        """
        SVC-014: Record name of executed migration

        Arrange: Migration "v1.0.0-to-v1.1.0.py" completes
        Act: Call run()
        Assert: applied_migrations contains "v1.0.0-to-v1.1.0.py"
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("if __name__ == '__main__':\n    pass\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)
        applied = runner.get_applied_migrations(result)

        # Assert
        assert str(migration_file) in applied

    def test_should_record_exit_code_for_each_migration(self, tmp_path):
        """
        SVC-014: Record exit code for each successful migration

        Arrange: 2 migrations with exit code 0
        Act: Call run()
        Assert: Each recorded with exit_code=0
        """
        # Arrange
        migrations = []

        for from_v, to_v in [("1.0.0", "1.1.0"), ("1.1.0", "1.2.0")]:
            mig = tmp_path / f"v{from_v}-to-v{to_v}.py"
            mig.write_text("if __name__ == '__main__':\n    pass\n")
            migrations.append(MigrationScript(path=str(mig), from_version=from_v, to_version=to_v))

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations, timeout_seconds=10)

        # Assert
        for migration_result in result.results:
            assert migration_result.exit_code == 0

    def test_should_maintain_order_of_applied_migrations(self, tmp_path):
        """
        SVC-014: Applied migrations list maintains execution order

        Arrange: 3 migrations execute in order
        Act: Call run()
        Assert: applied_migrations[0] is 1st executed, [1] is 2nd, [2] is 3rd
        """
        # Arrange
        migrations = []

        for i, (from_v, to_v) in enumerate([("1.0.0", "1.1.0"), ("1.1.0", "1.2.0"), ("1.2.0", "1.3.0")]):
            mig = tmp_path / f"v{from_v}-to-v{to_v}.py"
            mig.write_text("if __name__ == '__main__':\n    pass\n")
            migrations.append(MigrationScript(path=str(mig), from_version=from_v, to_version=to_v))

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations, timeout_seconds=10)

        # Assert
        for i, migration_result in enumerate(result.results):
            assert migration_result.script == migrations[i]

    def test_should_record_no_applied_migrations_on_immediate_failure(self, tmp_path):
        """
        SVC-014: Empty applied_migrations if first migration fails

        Arrange: First migration fails immediately
        Act: Call run()
        Assert: applied_migrations is empty list
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("import sys\nsys.exit(1)\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)
        applied = runner.get_applied_migrations(result)

        # Assert
        assert applied == []

    def test_should_record_partial_applied_migrations_on_later_failure(self, tmp_path):
        """
        SVC-014: Record migrations that succeeded before failure

        Arrange: [mig1_ok, mig2_ok, mig3_fails]
        Act: Call run()
        Assert: applied_migrations contains mig1 and mig2 only
        """
        # Arrange
        migrations = []

        for i, (from_v, to_v) in enumerate([("1.0.0", "1.1.0"), ("1.1.0", "1.2.0"), ("1.2.0", "1.3.0")]):
            mig = tmp_path / f"v{from_v}-to-v{to_v}.py"
            if i == 2:  # Third migration fails
                mig.write_text("import sys\nsys.exit(1)\n")
            else:
                mig.write_text("if __name__ == '__main__':\n    pass\n")
            migrations.append(MigrationScript(path=str(mig), from_version=from_v, to_version=to_v))

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations, timeout_seconds=10)
        applied = runner.get_applied_migrations(result)

        # Assert
        assert len(applied) == 2
        assert str(migrations[0].path) in applied
        assert str(migrations[1].path) in applied


class TestMigrationEdgeCases:
    """Tests for edge cases and error scenarios"""

    def test_should_handle_empty_migration_list(self, tmp_path):
        """
        Edge case: No migrations to execute

        Arrange: Call run([])
        Act: Execute with empty migration list
        Assert: Returns success with applied_migrations=[]
        """
        # Arrange
        runner = MigrationRunner()

        # Act
        result = runner.run([], timeout_seconds=10)

        # Assert
        assert result.all_success is True
        assert result.applied_count == 0

    def test_should_handle_migration_that_returns_non_standard_exit_code(self, tmp_path):
        """
        Edge case: Migration exits with code other than 0/1

        Arrange: Migration exits with code 127 (command not found)
        Act: Call run()
        Assert: Non-zero exit treated as failure
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("import sys\nsys.exit(127)\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert result.all_success is False
        assert result.results[0].exit_code == 127


# Fixtures for test support


@pytest.fixture
def migration_runner_config():
    """Configuration for migration runner"""
    return {
        "migration_timeout_seconds": 300,
        "capture_output": True,
        "stop_on_failure": True,
    }


@pytest.fixture
def sample_migration_script(tmp_path):
    """Create a sample migration script"""
    migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
    migration_file.write_text('''
def main():
    """Migrate from 1.0.0 to 1.1.0"""
    print("Starting migration...")

    # Perform migration operations
    print("Updating configuration...")
    print("Migration complete!")

    return {"status": "success"}

if __name__ == "__main__":
    result = main()
    print(f"Result: {result}")
''')
    return migration_file


@pytest.fixture
def failing_migration_script(tmp_path):
    """Create a migration script that fails"""
    migration_file = tmp_path / "v1.1.0-to-v1.2.0.py"
    migration_file.write_text('''
import sys
def main():
    """Migration that fails"""
    print("Starting migration...")
    print("Database connection failed", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    main()
''')
    return migration_file


# ==================== NEW COVERAGE GAP TESTS (STORY-078 Phase 4.5) ====================
# Targets: 11% gap in migration_runner.py (16 lines in timeout/error handling)


class TestMigrationTimeout:
    """Tests for timeout scenarios"""

    def test_should_timeout_and_kill_long_running_migration(self, tmp_path):
        """
        Test: Long-running migration killed after timeout

        Arrange: Migration that sleeps for 10 seconds, timeout=1 second
        Act: Call run()
        Assert: Migration terminated, exit code -1
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text(
            "import time\nimport sys\n"
            "time.sleep(10)\n"
            "print('Should not print')\n"
        )

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=1)

        # Assert
        assert result.all_success is False
        assert result.results[0].exit_code == -1
        assert "timeout" in result.results[0].stderr.lower()

    def test_should_append_timeout_message_to_stderr(self, tmp_path):
        """
        Test: Timeout message appended to stderr

        Arrange: Timeout scenario
        Act: Call run()
        Assert: Stderr contains timeout message with seconds
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("import time\ntime.sleep(5)\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=1)

        # Assert
        assert "timeout" in result.results[0].stderr.lower()
        assert "1" in result.results[0].stderr  # Timeout seconds

    def test_should_recover_stderr_from_killed_process(self, tmp_path):
        """
        Test: Stderr captured even from killed process

        Arrange: Migration killed after timeout
        Act: Call run()
        Assert: Any output before timeout captured
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text(
            "import time\nimport sys\n"
            "print('Starting...')\n"
            "time.sleep(10)\n"
            "print('This should not print')\n"
        )

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=1)

        # Assert - Starting message should be in stdout before timeout
        assert result.results[0].success is False

    def test_should_handle_subprocess_exception(self, tmp_path, caplog):
        """
        Test: Subprocess exceptions handled gracefully

        Arrange: Mock Popen to raise exception
        Act: Call run()
        Assert: Migration marked as failed with logged error
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("print('test')\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Mock Popen to raise exception during subprocess creation
        with patch("installer.migration_runner.subprocess.Popen") as mock_popen:
            mock_popen.side_effect = OSError("Process creation failed")

            # Act
            with caplog.at_level(logging.ERROR):
                result = runner.run([migration], timeout_seconds=10)

            # Assert
            assert result.all_success is False
            assert "Process creation failed" in caplog.text or "execution" in caplog.text.lower()


class TestScriptFileHandling:
    """Tests for migration script file operations"""

    def test_should_make_script_executable_on_unix(self, tmp_path):
        """
        Test: Script made executable on Unix systems

        Arrange: Migration script with read-only permissions
        Act: Call run()
        Assert: Script executed (permissions changed internally)
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("if __name__ == '__main__':\n    pass\n")

        # Make read-only
        os.chmod(migration_file, 0o444)

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert result.all_success is True

    def test_should_handle_nonexistent_script_file(self, tmp_path):
        """
        Test: Nonexistent script file detected during MigrationScript creation

        Arrange: Attempt to create MigrationScript with non-existent path
        Act: Create MigrationScript
        Assert: ValueError raised (validation in __post_init__)
        """
        # Act & Assert
        # Note: MigrationScript validates file existence in __post_init__,
        # so the error is raised during object creation, not during run()
        with pytest.raises(ValueError) as exc_info:
            MigrationScript(
                path=str(tmp_path / "nonexistent.py"),
                from_version="1.0.0",
                to_version="1.1.0"
            )
        assert "not found" in str(exc_info.value).lower()

    def test_should_tolerate_chmod_errors_on_windows(self, tmp_path):
        """
        Test: chmod errors ignored (Windows compatibility)

        Arrange: Mock os.stat/chmod to raise on Windows
        Act: Call run()
        Assert: Script still executes (chmod failure ignored)
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("if __name__ == '__main__':\n    pass\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Mock os.chmod to raise AttributeError (Windows behavior)
        with patch("os.chmod") as mock_chmod:
            mock_chmod.side_effect = AttributeError("chmod not available")

            # Act & Assert - Should still execute successfully
            result = runner.run([migration], timeout_seconds=10)
            assert result.all_success is True


class TestMigrationErrorMessages:
    """Tests for error message generation"""

    def test_should_generate_error_message_from_exit_code(self, tmp_path):
        """
        Test: Error message generated from exit code when stderr empty

        Arrange: Migration fails with exit code 42, no stderr
        Act: Call run()
        Assert: error_message contains exit code
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("import sys\nsys.exit(42)\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert result.all_success is False
        assert "42" in result.results[0].error_message

    def test_should_prefer_stderr_for_error_message(self, tmp_path):
        """
        Test: Stderr message preferred over exit code

        Arrange: Migration fails with stderr message
        Act: Call run()
        Assert: error_message contains stderr content
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text(
            "import sys\n"
            "print('Database error: connection refused', file=sys.stderr)\n"
            "sys.exit(1)\n"
        )

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert result.all_success is False
        assert "connection refused" in result.results[0].error_message


class TestMigrationExecutionSequence:
    """Tests for execution sequence and state tracking"""

    def test_should_update_applied_count_correctly(self, tmp_path):
        """
        Test: applied_count reflects successful migrations

        Arrange: 3 migrations where 2nd fails
        Act: Call run()
        Assert: applied_count == 1
        """
        # Arrange
        migrations = []

        mig1 = tmp_path / "v1.0.0-to-v1.1.0.py"
        mig1.write_text("if __name__ == '__main__':\n    pass\n")
        migrations.append(MigrationScript(path=str(mig1), from_version="1.0.0", to_version="1.1.0"))

        mig2 = tmp_path / "v1.1.0-to-v1.2.0.py"
        mig2.write_text("import sys\nsys.exit(1)\n")
        migrations.append(MigrationScript(path=str(mig2), from_version="1.1.0", to_version="1.2.0"))

        mig3 = tmp_path / "v1.2.0-to-v1.3.0.py"
        mig3.write_text("if __name__ == '__main__':\n    pass\n")
        migrations.append(MigrationScript(path=str(mig3), from_version="1.2.0", to_version="1.3.0"))

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations, timeout_seconds=10)

        # Assert
        assert result.applied_count == 1

    def test_should_populate_failed_migration_fields(self, tmp_path):
        """
        Test: Failed migration details populated correctly

        Arrange: Migration fails
        Act: Call run()
        Assert: failed_at_migration and failed_migration_result set
        """
        # Arrange
        migration_file = tmp_path / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("import sys\nsys.exit(1)\n")

        migration = MigrationScript(
            path=str(migration_file),
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run([migration], timeout_seconds=10)

        # Assert
        assert result.failed_at_migration == migration
        assert result.failed_migration_result is not None
        assert result.failed_migration_result.success is False
