"""
STORY-080: Unit tests for BackupRestorer service.

Tests file restoration from backup with user content preservation.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+ business logic
Test Categories: AC#4, AC#5, AC#6
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import hashlib
import json


class TestFileRestoration:
    """Test file restoration from backup (AC#4, SVC-005)."""

    def test_restore_all_files_from_backup(self, tmp_path):
        """
        Test: BackupRestorer restores all files from backup (AC#4, SVC-005).

        Given: Backup contains 100 files
        When: restore() is called
        Then: All 100 files are restored to original locations
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        # Create 100 test files in backup
        for i in range(100):
            file_path = backup_dir / f"file_{i:03d}.txt"
            file_path.write_text(f"content {i}")

        restorer = BackupRestorer(logger=Mock())

        # Act
        result = restorer.restore(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        assert result.files_restored == 100
        for i in range(100):
            assert (target_dir / f"file_{i:03d}.txt").exists()

    def test_restore_creates_parent_directories(self, tmp_path):
        """
        Test: BackupRestorer creates parent directories as needed (AC#4, SVC-005).

        Given: Backup has nested directory structure
        When: restore() is called
        Then: All parent directories are created
        And: Files are restored to correct nested locations
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "level1" / "level2").mkdir(parents=True)
        (backup_dir / "level1" / "level2" / "deep.txt").write_text("deep content")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        restorer = BackupRestorer(logger=Mock())

        # Act
        result = restorer.restore(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        assert (target_dir / "level1" / "level2" / "deep.txt").exists()
        assert (target_dir / "level1" / "level2" / "deep.txt").read_text() == "deep content"


class TestUserContentPreservation:
    """Test user content preservation during restore (AC#5, SVC-006/007)."""

    def test_restore_skips_user_content_paths_by_default(self, tmp_path):
        """
        Test: User content is NOT restored by default (AC#5, SVC-006).

        Given: Backup contains devforgeai/specs/Stories/story.md
        When: restore() called without include_user_content flag
        Then: devforgeai/specs/Stories/ is NOT restored
        And: Files are added to files_preserved count
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / ".ai_docs" / "Stories").mkdir(parents=True)
        (backup_dir / ".ai_docs" / "Stories" / "story.md").write_text("# Story\nContent")
        (backup_dir / "framework_file.txt").write_text("framework")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        restorer = BackupRestorer(logger=Mock())

        # Act
        result = restorer.restore(
            backup_dir=backup_dir,
            target_dir=target_dir,
            include_user_content=False
        )

        # Assert
        assert not (target_dir / ".ai_docs" / "Stories" / "story.md").exists()
        assert (target_dir / "framework_file.txt").exists()
        assert result.files_preserved >= 1

    def test_restore_includes_user_content_when_flag_set(self, tmp_path):
        """
        Test: User content IS restored when --include-user-content flag set (AC#5, SVC-007).

        Given: Backup contains devforgeai/specs/Stories/story.md and flag is True
        When: restore() called with include_user_content=True
        Then: devforgeai/specs/Stories/ IS restored from backup
        And: files_preserved count is 0 for user content paths
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / ".ai_docs" / "Stories").mkdir(parents=True)
        (backup_dir / ".ai_docs" / "Stories" / "story.md").write_text("# Story\nOld content")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / ".ai_docs" / "Stories").mkdir(parents=True)
        (target_dir / ".ai_docs" / "Stories" / "story.md").write_text("# Story\nNew content")

        restorer = BackupRestorer(logger=Mock())

        # Act
        result = restorer.restore(
            backup_dir=backup_dir,
            target_dir=target_dir,
            include_user_content=True
        )

        # Assert
        assert (target_dir / ".ai_docs" / "Stories" / "story.md").exists()
        assert (target_dir / ".ai_docs" / "Stories" / "story.md").read_text() == "# Story\nOld content"

    def test_restore_skips_ai_docs_stories(self, tmp_path):
        """
        Test: devforgeai/specs/Stories/* not restored by default (AC#5, SVC-006).

        Given: Backup contains stories
        When: restore() called without flag
        Then: Stories are preserved (not overwritten)
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / ".ai_docs" / "Stories").mkdir(parents=True)
        (backup_dir / ".ai_docs" / "Stories" / "STORY-001.md").write_text("# Old Story")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / ".ai_docs" / "Stories").mkdir(parents=True)
        (target_dir / ".ai_docs" / "Stories" / "STORY-001.md").write_text("# New Story")

        restorer = BackupRestorer(logger=Mock())

        # Act
        result = restorer.restore(
            backup_dir=backup_dir,
            target_dir=target_dir,
            include_user_content=False
        )

        # Assert
        assert (target_dir / ".ai_docs" / "Stories" / "STORY-001.md").read_text() == "# New Story"

    def test_restore_skips_ai_docs_epics(self, tmp_path):
        """
        Test: devforgeai/specs/Epics/* not restored by default (AC#5, SVC-006).

        Given: Backup contains epics
        When: restore() called without flag
        Then: Epics are preserved (not overwritten)
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / ".ai_docs" / "Epics").mkdir(parents=True)
        (backup_dir / ".ai_docs" / "Epics" / "EPIC-001.md").write_text("# Old Epic")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / ".ai_docs" / "Epics").mkdir(parents=True)
        (target_dir / ".ai_docs" / "Epics" / "EPIC-001.md").write_text("# New Epic")

        restorer = BackupRestorer(logger=Mock())

        # Act
        result = restorer.restore(
            backup_dir=backup_dir,
            target_dir=target_dir,
            include_user_content=False
        )

        # Assert
        assert (target_dir / ".ai_docs" / "Epics" / "EPIC-001.md").read_text() == "# New Epic"

    def test_restore_skips_devforgeai_context(self, tmp_path):
        """
        Test: .devforgeai/context/* not restored by default (AC#5, SVC-006).

        Given: Backup contains context files
        When: restore() called without flag
        Then: Context files are preserved
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / ".devforgeai" / "context").mkdir(parents=True)
        (backup_dir / ".devforgeai" / "context" / "tech-stack.md").write_text("# Old tech-stack")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / ".devforgeai" / "context").mkdir(parents=True)
        (target_dir / ".devforgeai" / "context" / "tech-stack.md").write_text("# New tech-stack")

        restorer = BackupRestorer(logger=Mock())

        # Act
        result = restorer.restore(
            backup_dir=backup_dir,
            target_dir=target_dir,
            include_user_content=False
        )

        # Assert
        assert (target_dir / ".devforgeai" / "context" / "tech-stack.md").read_text() == "# New tech-stack"

    def test_restore_skips_devforgeai_adrs(self, tmp_path):
        """
        Test: .devforgeai/adrs/* not restored by default (AC#5, SVC-006).

        Given: Backup contains ADR files
        When: restore() called without flag
        Then: ADRs are preserved
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / ".devforgeai" / "adrs").mkdir(parents=True)
        (backup_dir / ".devforgeai" / "adrs" / "ADR-001.md").write_text("# Old ADR")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / ".devforgeai" / "adrs").mkdir(parents=True)
        (target_dir / ".devforgeai" / "adrs" / "ADR-001.md").write_text("# New ADR")

        restorer = BackupRestorer(logger=Mock())

        # Act
        result = restorer.restore(
            backup_dir=backup_dir,
            target_dir=target_dir,
            include_user_content=False
        )

        # Assert
        assert (target_dir / ".devforgeai" / "adrs" / "ADR-001.md").read_text() == "# New ADR"


class TestChecksumVerification:
    """Test file checksum verification (AC#6, SVC-008)."""

    def test_restore_verifies_file_checksums(self, tmp_path):
        """
        Test: BackupRestorer verifies file checksums after restore (AC#6, SVC-008).

        Given: Backup contains files with checksums in manifest
        When: restore() is called
        Then: Checksums are calculated and compared
        And: All files match backup checksums
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        # Create file with known content
        file_content = "test content for checksum"
        (backup_dir / "test_file.txt").write_text(file_content)

        # Calculate checksum
        checksum = hashlib.sha256(file_content.encode()).hexdigest()

        # Create manifest with checksum
        manifest = {
            "files": {
                "test_file.txt": {
                    "checksum": checksum,
                    "size": len(file_content)
                }
            }
        }
        (backup_dir / "manifest.json").write_text(json.dumps(manifest))

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        restorer = BackupRestorer(logger=Mock())

        # Act
        result = restorer.restore(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        assert result.checksums_verified is True

    def test_restore_returns_correct_counts(self, tmp_path):
        """
        Test: restore() returns accurate file counts (AC#4).

        Given: 50 framework files and 10 user files in backup
        When: restore() called without include_user_content
        Then: files_restored=50, files_preserved=10
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        # Create 50 framework files
        for i in range(50):
            (backup_dir / f"framework_{i}.txt").write_text(f"content {i}")

        # Create 10 user content files
        (backup_dir / ".ai_docs" / "Stories").mkdir(parents=True)
        for i in range(10):
            (backup_dir / ".ai_docs" / "Stories" / f"STORY-{i:03d}.md").write_text(f"# Story {i}")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        restorer = BackupRestorer(logger=Mock())

        # Act
        result = restorer.restore(
            backup_dir=backup_dir,
            target_dir=target_dir,
            include_user_content=False
        )

        # Assert
        assert result.files_restored == 50
        assert result.files_preserved == 10


class TestRestoreErrorHandling:
    """Test error handling during restore (error cases)."""

    def test_restore_handles_missing_backup(self, tmp_path):
        """
        Test: restore() handles missing backup directory gracefully.

        Given: Backup directory does not exist
        When: restore() is called
        Then: Raises appropriate error
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "nonexistent"
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        restorer = BackupRestorer(logger=Mock())

        # Act & Assert
        with pytest.raises(Exception):
            restorer.restore(backup_dir=backup_dir, target_dir=target_dir)

    def test_restore_handles_checksum_mismatch(self, tmp_path):
        """
        Test: restore() detects checksum mismatches (AC#6).

        Given: Restored file checksum doesn't match manifest
        When: restore() completes verification
        Then: Returns error or sets checksums_verified=False
        """
        # Arrange
        from installer.backup_restorer import BackupRestorer

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        # Create file
        file_content = "test content"
        (backup_dir / "test_file.txt").write_text(file_content)

        # Create manifest with WRONG checksum
        manifest = {
            "files": {
                "test_file.txt": {
                    "checksum": "wrong_checksum_12345",
                    "size": len(file_content)
                }
            }
        }
        (backup_dir / "manifest.json").write_text(json.dumps(manifest))

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        restorer = BackupRestorer(logger=Mock())

        # Act
        result = restorer.restore(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        assert result.checksums_verified is False or result.error is not None
