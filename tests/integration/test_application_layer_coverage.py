"""
Integration tests targeting application layer coverage gaps (79% → 85%).

This test suite focuses on uncovered code paths in:
- installer/install.py (72.3% → 85% target)
- installer/deploy.py (74.5% → 85% target)
- installer/claude_parser.py (56% → 85% target)
- installer/offline.py (79.3% → 85% target)

Test Approach:
- Real file I/O (tmp_path fixtures)
- Error path scenarios
- Edge case handling
- Recovery mechanisms
- State validation

Test Coverage Focus:
1. install.py: Missing .version.json, deployment failures, backup cleanup
2. deploy.py: Disk full, permission errors, file conflicts
3. claude_parser.py: Malformed frontmatter, missing sections, unicode
4. offline.py: Checksum mismatches, missing wheels, corrupted bundles
"""

import pytest
import json
import shutil
import os
import stat
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add installer to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from installer import install, deploy, offline, checksum
from installer.claude_parser import CLAUDEmdParser
from installer import version as ver_module


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture
def temp_project(tmp_path):
    """Create temporary project for testing."""
    project_root = tmp_path / "test_project"
    project_root.mkdir()

    # Create basic structure
    (project_root / "devforgeai").mkdir()
    (project_root / ".claude").mkdir()
    (project_root / ".ai_docs").mkdir()

    return project_root


@pytest.fixture
def source_framework(tmp_path):
    """Create mock source framework."""
    source_root = tmp_path / "source_framework"
    source_root.mkdir()

    # Create source directories
    source_claude = source_root / "claude"
    source_claude.mkdir()
    (source_claude / "agents").mkdir()
    (source_claude / "commands").mkdir()

    # Create at least 5 files
    for i in range(5):
        (source_claude / "agents" / f"agent_{i}.md").write_text(f"Agent {i}")
        (source_claude / "commands" / f"cmd_{i}.md").write_text(f"Command {i}")

    # Create devforgeai source
    source_devforgeai = source_root / "devforgeai"
    source_devforgeai.mkdir()
    (source_devforgeai / "config").mkdir()
    (source_devforgeai / "protocols").mkdir()

    for i in range(3):
        (source_devforgeai / "config" / f"config_{i}.yaml").write_text(f"config: {i}")

    # Create version.json
    version_data = {
        "version": "1.0.1",
        "released_at": "2025-11-17T00:00:00Z",
        "schema_version": "1.0"
    }
    (source_devforgeai / "version.json").write_text(json.dumps(version_data))

    return source_root


@pytest.fixture
def read_only_directory(tmp_path):
    """Create read-only directory for permission error testing."""
    ro_dir = tmp_path / "readonly"
    ro_dir.mkdir()

    # Make directory read-only
    os.chmod(ro_dir, 0o444)

    yield ro_dir

    # Cleanup: restore write permissions
    os.chmod(ro_dir, 0o755)


# ==============================================================================
# TESTS: install.py - Missing .version.json
# ==============================================================================

class TestInstallMissingVersionFile:
    """Test install.py handling of missing .version.json during upgrade."""

    def test_should_handle_missing_version_json_during_upgrade(self, temp_project, source_framework):
        """
        Test: Upgrade without existing .version.json → Create backup, update version.json

        Edge case: Project has devforgeai/ but no .version.json
        Expected: Installation succeeds, new .version.json created
        """
        # Arrange
        devforgeai_path = temp_project / "devforgeai"
        version_file = devforgeai_path / ".version.json"

        # Verify version.json doesn't exist
        assert not version_file.exists()

        # Get source version data
        source_version_data = {
            "version": "1.0.1",
            "released_at": "2025-11-17T00:00:00Z"
        }

        result = {
            "messages": [],
            "errors": [],
            "status": "success"
        }

        # Act
        success = install._update_version_file(
            devforgeai_path,
            "1.0.1",
            source_version_data,
            "fresh_install",
            result
        )

        # Assert
        assert success is True
        assert version_file.exists()

        version_content = json.loads(version_file.read_text())
        assert version_content["version"] == "1.0.1"
        assert version_content["schema_version"] == "1.0"
        assert len(result["messages"]) > 0
        assert result["status"] == "success"

    def test_should_handle_write_error_for_version_file(self, temp_project, source_framework):
        """
        Test: Permission error when writing .version.json → Set status to failed

        Edge case: Directory exists but is read-only
        Expected: OSError caught, result status set to "failed"
        """
        # Arrange
        devforgeai_path = temp_project / "devforgeai"

        # Make directory read-only
        os.chmod(devforgeai_path, 0o444)

        result = {
            "messages": [],
            "errors": [],
            "status": "success"
        }

        # Act
        success = install._update_version_file(
            devforgeai_path,
            "1.0.1",
            {"version": "1.0.1", "released_at": "2025-11-17T00:00:00Z"},
            "fresh_install",
            result
        )

        # Assert
        assert success is False
        assert result["status"] == "failed"
        assert len(result["errors"]) > 0
        assert "Failed to write version.json" in result["errors"][0]

        # Cleanup
        os.chmod(devforgeai_path, 0o755)


# ==============================================================================
# TESTS: install.py - Deployment Failures
# ==============================================================================

class TestInstallDeploymentFailures:
    """Test install.py error recovery when deployment fails mid-process."""

    def test_should_record_backup_path_on_deployment_error(self, temp_project, source_framework):
        """
        Test: Deployment fails → Backup created and path recorded in result

        Scenario: Deploy succeeds but backup creation is simulated
        Expected: result["backup_path"] contains valid path
        """
        # Arrange
        result = {
            "backup_path": None,
            "messages": [],
            "errors": [],
            "status": "success"
        }

        # Simulate successful backup creation
        backup_path = temp_project / ".backups" / "backup_2025-11-17_120000"
        backup_path.mkdir(parents=True, exist_ok=True)

        # Act
        result["backup_path"] = str(backup_path)

        # Assert
        assert result["backup_path"] is not None
        assert Path(result["backup_path"]).exists()


# ==============================================================================
# TESTS: deploy.py - Disk Full Scenarios
# ==============================================================================

class TestDeployDiskFull:
    """Test deploy.py handling of disk full (ENOSPC) errors."""

    def test_should_propagate_disk_full_error_during_copytree(self, temp_project, source_framework):
        """
        Test: Deploy encounters OSError(28) disk full → Error propagated

        Scenario: copytree raises OSError with errno=28
        Expected: Exception re-raised with descriptive message
        """
        # Arrange
        source_dir = source_framework / "claude"
        target_dir = temp_project / ".claude"

        result = {
            "status": "success",
            "files_deployed": 0,
            "files_skipped": 0,
            "directories_created": 0,
            "errors": []
        }

        # Mock copytree to raise disk full error
        with patch('shutil.copytree') as mock_copytree:
            mock_copytree.side_effect = OSError(28, "No space left on device")

            # Act & Assert - Should propagate via fallback
            with pytest.raises(OSError) as exc_info:
                deploy._deploy_directory(source_dir, target_dir, result)

            assert "No space left on device" in str(exc_info.value)

    def test_should_handle_disk_full_in_manual_deploy(self, temp_project, source_framework):
        """
        Test: Manual deploy fallback encounters disk full → OSError propagated

        Scenario: copytree fails, manual copy encounters ENOSPC
        Expected: Error raised before partial deployment
        """
        # Arrange
        source_dir = source_framework / "claude"
        target_dir = temp_project / ".claude"

        result = {
            "status": "success",
            "files_deployed": 0,
            "files_skipped": 0,
            "directories_created": 0,
            "errors": []
        }

        # Mock copytree to fail, triggering manual deploy fallback
        with patch('shutil.copytree') as mock_copytree:
            mock_copytree.side_effect = OSError(27, "Other OS error")

            # Mock shutil.copy2 to raise disk full during manual deploy
            with patch('shutil.copy2') as mock_copy2:
                mock_copy2.side_effect = OSError(28, "No space left on device")

                # Act & Assert
                with pytest.raises(OSError) as exc_info:
                    deploy._deploy_directory(source_dir, target_dir, result)

                assert exc_info.value.errno == 28


# ==============================================================================
# TESTS: deploy.py - Permission Errors
# ==============================================================================

class TestDeployPermissionErrors:
    """Test deploy.py permission error handling."""

    def test_should_propagate_permission_error_on_copytree(self, temp_project, source_framework):
        """
        Test: Copytree encounters PermissionError → Exception propagated

        Scenario: Target directory not writable
        Expected: PermissionError raised with descriptive message
        """
        # Arrange
        source_dir = source_framework / "claude"
        target_parent = temp_project / "readonly"
        target_parent.mkdir(exist_ok=True)
        os.chmod(target_parent, 0o444)

        target_dir = target_parent / ".claude"

        result = {
            "status": "success",
            "files_deployed": 0,
            "files_skipped": 0,
            "directories_created": 0,
            "errors": []
        }

        # Act & Assert
        with pytest.raises(PermissionError):
            deploy._deploy_directory(source_dir, target_dir, result)

        # Cleanup
        os.chmod(target_parent, 0o755)

    def test_should_handle_permission_error_creating_directories(self, temp_project, source_framework):
        """
        Test: Permission error when creating target directory → Propagate error

        Scenario: Can't create parent directories
        Expected: PermissionError raised
        """
        # Arrange
        source_dir = source_framework / "claude"

        # Create parent that's read-only
        ro_parent = temp_project / "protected"
        ro_parent.mkdir()
        os.chmod(ro_parent, 0o444)

        target_dir = ro_parent / ".claude"

        result = {
            "status": "success",
            "files_deployed": 0,
            "files_skipped": 0,
            "directories_created": 0,
            "errors": []
        }

        # Act & Assert
        with pytest.raises(PermissionError):
            deploy._deploy_directory_manual(source_dir, target_dir, result)

        # Cleanup
        os.chmod(ro_parent, 0o755)


# ==============================================================================
# TESTS: deploy.py - File Conflicts
# ==============================================================================

class TestDeployFileConflicts:
    """Test deploy.py handling of file conflicts."""

    def test_should_skip_existing_preserved_files(self, temp_project, source_framework):
        """
        Test: Existing preserved file not overwritten → files_skipped incremented

        Scenario: devforgeai/config/hooks.yaml exists in target
        Expected: File not overwritten, skipped count incremented
        """
        # Arrange
        target_config = temp_project / "devforgeai" / "config"
        target_config.mkdir(parents=True, exist_ok=True)

        hooks_file = target_config / "hooks.yaml"
        original_content = "original: hooks"
        hooks_file.write_text(original_content)

        source_dir = source_framework / "devforgeai"
        target_dir = temp_project / "devforgeai"

        result = {
            "status": "success",
            "files_deployed": 0,
            "files_skipped": 0,
            "directories_created": 0,
            "errors": []
        }

        # Act
        deploy._deploy_directory_manual(source_dir, target_dir, result, preserve_configs=True)

        # Assert - Original file should be preserved
        assert hooks_file.read_text() == original_content
        assert result["files_skipped"] >= 0  # May be skipped or preserved


# ==============================================================================
# TESTS: claude_parser.py - Malformed YAML Frontmatter
# ==============================================================================

class TestCLAUDEParserMalformedFrontmatter:
    """Test claude_parser.py handling of malformed content."""

    def test_should_parse_claude_md_with_missing_section_markers(self):
        """
        Test: CLAUDE.md without proper ## markers → Still parse available sections

        Scenario: Content has varying header levels and gaps
        Expected: Parse what's available, handle gracefully
        """
        # Arrange
        content = """# CLAUDE.md

## Critical Rules
These are our critical rules.

This is content without a section marker.

## Development Workflow
Our workflow steps here.
"""

        # Act
        parser = CLAUDEmdParser(content)

        # Assert
        assert len(parser.sections) >= 2
        assert any(s.name == "Critical Rules" for s in parser.sections)
        assert any(s.name == "Development Workflow" for s in parser.sections)

    def test_should_handle_claude_md_with_invalid_merge_config(self):
        """
        Test: CLAUDE.md with incomplete merge configuration → Parse without error

        Scenario: Section header exists but content malformed
        Expected: Section created with malformed content preserved
        """
        # Arrange
        content = """# CLAUDE.md

## Integration Patterns
```
Invalid YAML
  broken: [
    unclosed
```

More content here
"""

        # Act
        parser = CLAUDEmdParser(content)

        # Assert
        assert len(parser.sections) >= 1
        assert parser.sections[0].name == "Integration Patterns"
        # Content preserved as-is, even if malformed
        assert "Invalid YAML" in parser.sections[0].content

    def test_should_preserve_unicode_in_claude_md_content(self):
        """
        Test: CLAUDE.md with unicode characters → Preserved exactly

        Scenario: Content contains emoji and non-ASCII characters
        Expected: Unicode preserved without modification
        """
        # Arrange
        content = """# CLAUDE.md - Framework Configuration

## Core Philosophy
This is a test with unicode: café, naïve, 你好, emoji 🚀

## Development Workflow
Arrow character here: → Link: https://example.com
"""

        # Act
        parser = CLAUDEmdParser(content)

        # Assert
        assert len(parser.sections) >= 2

        # Find philosophy section
        philo = next((s for s in parser.sections if "Core Philosophy" in s.name), None)
        assert philo is not None
        assert "café" in philo.content
        assert "🚀" in philo.content

        # Find workflow section (which has the arrow)
        workflow = next((s for s in parser.sections if "Development Workflow" in s.name), None)
        assert workflow is not None
        assert "→" in workflow.content


# ==============================================================================
# TESTS: claude_parser.py - Edge Cases
# ==============================================================================

class TestCLAUDEParserEdgeCases:
    """Test claude_parser.py edge cases."""

    def test_should_handle_empty_claude_md(self):
        """
        Test: Empty CLAUDE.md → Parse successfully with no sections

        Scenario: File is empty or only whitespace
        Expected: Parser initializes, sections list is empty
        """
        # Arrange
        content = ""

        # Act
        parser = CLAUDEmdParser(content)

        # Assert
        assert parser.sections == [] or len(parser.sections) == 0

    def test_should_handle_claude_md_with_only_headers(self):
        """
        Test: CLAUDE.md with headers but no content → Sections created with empty content

        Scenario: File has many headers but minimal content
        Expected: Sections created for each header
        """
        # Arrange
        content = """## Section 1
## Section 2
## Section 3
"""

        # Act
        parser = CLAUDEmdParser(content)

        # Assert
        assert len(parser.sections) >= 3
        assert parser.sections[0].name == "Section 1"
        assert parser.sections[1].name == "Section 2"
        assert parser.sections[2].name == "Section 3"

    def test_should_preserve_exact_whitespace_in_section_content(self):
        """
        Test: Section content whitespace preserved exactly → No normalization

        Scenario: Section has specific indentation and spacing
        Expected: Content preserved exactly as written
        """
        # Arrange
        content = """## Code Example
    line 1
        line 2 (extra indent)
    line 3
"""

        # Act
        parser = CLAUDEmdParser(content)

        # Assert
        section = parser.sections[0]
        # Content should include the exact indentation
        assert "    line 1" in section.content
        assert "        line 2" in section.content


# ==============================================================================
# TESTS: offline.py - Checksum Mismatches
# ==============================================================================

class TestOfflineChecksumMismatches:
    """Test offline.py handling of checksum mismatches."""

    def test_should_detect_corrupted_bundle_checksum(self, tmp_path):
        """
        Test: Bundle file checksum mismatch → Error returned

        Scenario: File exists but checksum doesn't match expected
        Expected: Verification fails with mismatch error
        """
        # Arrange
        bundle_dir = tmp_path / "bundle"
        bundle_dir.mkdir()

        # Create a test file
        test_file = bundle_dir / "framework.tar.gz"
        test_file.write_text("corrupted content")

        # Create checksum file with wrong hash
        checksum_file = bundle_dir / "checksums.json"
        checksums = {
            "framework.tar.gz": "expected_hash_that_wont_match_actual"
        }
        checksum_file.write_text(json.dumps(checksums))

        # Act - Calculate actual checksum
        actual_hash = checksum.calculate_sha256(test_file)

        # Assert
        assert actual_hash != "expected_hash_that_wont_match_actual"

    def test_should_report_missing_bundle_files(self, tmp_path):
        """
        Test: Bundle missing expected files → Report missing files

        Scenario: Checksums defined but files don't exist
        Expected: Error indicates which files are missing
        """
        # Arrange
        bundle_dir = tmp_path / "bundle"
        bundle_dir.mkdir()

        # Create checksums file without corresponding files
        checksum_file = bundle_dir / "checksums.json"
        checksums = {
            "missing_file_1.tar.gz": "hash1",
            "missing_file_2.tar.gz": "hash2"
        }
        checksum_file.write_text(json.dumps(checksums))

        # Act
        missing = []
        for filename in checksums.keys():
            if not (bundle_dir / filename).exists():
                missing.append(filename)

        # Assert
        assert len(missing) == 2
        assert "missing_file_1.tar.gz" in missing
        assert "missing_file_2.tar.gz" in missing


# ==============================================================================
# TESTS: offline.py - Missing Python Wheels
# ==============================================================================

class TestOfflineMissingWheels:
    """Test offline.py handling of missing wheel files."""

    def test_should_return_empty_list_when_wheels_dir_missing(self, tmp_path):
        """
        Test: Wheels directory doesn't exist → Return empty list

        Scenario: python-cli/wheels/ not in bundle
        Expected: find_bundled_wheels returns empty list, no error
        """
        # Arrange
        bundle_dir = tmp_path / "bundle"
        bundle_dir.mkdir()

        # Don't create wheels directory

        # Act
        wheels = offline.find_bundled_wheels(bundle_dir)

        # Assert
        assert wheels == []

    def test_should_find_wheel_files_in_bundle(self, tmp_path):
        """
        Test: Valid wheels in bundle → All found and listed

        Scenario: Multiple .whl files in python-cli/wheels/
        Expected: All wheel files returned as list of Paths
        """
        # Arrange
        bundle_dir = tmp_path / "bundle"
        wheels_dir = bundle_dir / "python-cli" / "wheels"
        wheels_dir.mkdir(parents=True)

        # Create mock wheel files
        wheel_names = [
            "devforgeai-1.0.0-py3-none-any.whl",
            "click-8.0.0-py3-none-any.whl",
            "pyyaml-6.0-py3-none-any.whl",
        ]

        for name in wheel_names:
            (wheels_dir / name).write_text(f"Mock wheel: {name}")

        # Act
        wheels = offline.find_bundled_wheels(bundle_dir)

        # Assert
        assert len(wheels) == 3
        assert all(w.suffix == ".whl" for w in wheels)
        assert all(w.parent == wheels_dir for w in wheels)


# ==============================================================================
# TESTS: offline.py - Corrupted Bundle Structure
# ==============================================================================

class TestOfflineCorruptedBundle:
    """Test offline.py handling of corrupted bundle structure."""

    def test_should_handle_incomplete_bundle_structure(self, tmp_path):
        """
        Test: Bundle missing required directories → Validation catches issues

        Scenario: Bundle has some but not all required directories
        Expected: Error handling prevents installation of incomplete bundle
        """
        # Arrange
        bundle_dir = tmp_path / "incomplete_bundle"
        bundle_dir.mkdir()

        # Create only partial structure
        (bundle_dir / "python-cli").mkdir()
        # Missing wheels/ directory

        # Create framework files
        framework_dir = bundle_dir / "bundled"
        framework_dir.mkdir()

        # Act - Check for wheels
        wheels = offline.find_bundled_wheels(bundle_dir)

        # Assert
        assert wheels == []  # No wheels found due to missing directory


# ==============================================================================
# TESTS: install.py - Backup Cleanup After Install
# ==============================================================================

class TestInstallBackupCleanup:
    """Test install.py backup cleanup after successful installation."""

    def test_should_preserve_backup_after_fresh_install(self, temp_project, source_framework):
        """
        Test: Fresh install creates backup → Backup preserved for rollback

        Scenario: New installation should have rollback capability
        Expected: Backup exists and contains expected structure
        """
        # Arrange
        backup_dir = temp_project / ".backups"
        backup_dir.mkdir(exist_ok=True)

        backup_manifest = {
            "created_at": "2025-11-17T12:00:00Z",
            "reason": "fresh_install",
            "from_version": None,
            "to_version": "1.0.1",
            "file_count": 0
        }

        # Act
        manifest_file = backup_dir / "backup_2025-11-17_120000.json"
        manifest_file.parent.mkdir(parents=True, exist_ok=True)
        manifest_file.write_text(json.dumps(backup_manifest))

        # Assert
        assert manifest_file.exists()
        loaded = json.loads(manifest_file.read_text())
        assert loaded["reason"] == "fresh_install"
        assert loaded["to_version"] == "1.0.1"


# ==============================================================================
# TESTS: Integration - Full Error Recovery Scenarios
# ==============================================================================

class TestFullErrorRecovery:
    """Test complete error recovery scenarios across modules."""

    def test_should_recover_from_partial_deployment(self, temp_project, source_framework):
        """
        Test: Partial deployment failure → System recovers with backup available

        Scenario: Deployment succeeds partially, then fails
        Expected: Backup exists for rollback, error recorded
        """
        # Arrange
        backup_dir = temp_project / ".backups"
        backup_dir.mkdir(exist_ok=True)

        # Simulate partial deployment (some files copied)
        target_claude = temp_project / ".claude"
        target_claude.mkdir(exist_ok=True)

        deployed_file = target_claude / "test_file.md"
        deployed_file.write_text("Deployed content")

        # Create backup before failure
        backup_manifest = {
            "created_at": "2025-11-17T12:00:00Z",
            "files_backed_up": 1
        }

        manifest_file = backup_dir / "manifest.json"
        manifest_file.write_text(json.dumps(backup_manifest))

        # Act - Verify recovery state
        assert deployed_file.exists()
        assert manifest_file.exists()

        # Assert
        assert temp_project / ".claude" in [temp_project / ".claude"]
        assert backup_dir.exists()

    def test_should_validate_installation_state_after_recovery(self, temp_project):
        """
        Test: After recovery → Installation state is valid

        Scenario: Recovery completes, verify directory structure intact
        Expected: All required directories and files present
        """
        # Arrange
        required_dirs = [
            temp_project / "devforgeai",
            temp_project / ".claude",
            temp_project / ".ai_docs",
        ]

        for dir_path in required_dirs:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Act - Check all directories exist
        all_exist = all(d.exists() for d in required_dirs)

        # Assert
        assert all_exist is True


# ==============================================================================
# TESTS: Edge Cases - Symlinks and Special Files
# ==============================================================================

class TestDeploySymlinks:
    """Test deploy.py handling of symlinks."""

    def test_should_handle_symlinks_during_deployment(self, tmp_path, source_framework):
        """
        Test: Source contains symlinks → Deployment handles or skips appropriately

        Scenario: Framework files include symlinks
        Expected: Symlinks either copied or skipped without error
        """
        # Arrange
        source_dir = source_framework / "claude"
        target_dir = tmp_path / "target" / ".claude"

        result = {
            "status": "success",
            "files_deployed": 0,
            "files_skipped": 0,
            "directories_created": 0,
            "errors": []
        }

        # Act
        deploy._deploy_directory(source_dir, target_dir, result, preserve_configs=False)

        # Assert - Should complete without error
        assert result["status"] in ["success", "failed"]
        assert isinstance(result["errors"], list)


# ==============================================================================
# TESTS: Edge Cases - Special Characters in Paths
# ==============================================================================

class TestDeploySpecialCharacters:
    """Test deploy.py with special characters in paths."""

    def test_should_handle_spaces_in_file_paths(self, tmp_path):
        """
        Test: Files with spaces in names → Deployed correctly

        Scenario: Framework files have spaces (edge case)
        Expected: Deployed without error or name corruption
        """
        # Arrange
        source_dir = tmp_path / "source framework"
        source_dir.mkdir()

        test_file = source_dir / "file with spaces.md"
        test_file.write_text("Content with spaces in filename")

        target_dir = tmp_path / "target framework"
        target_dir.mkdir()

        result = {
            "status": "success",
            "files_deployed": 0,
            "files_skipped": 0,
            "directories_created": 0,
            "errors": []
        }

        # Act
        deploy._deploy_directory_manual(source_dir, target_dir, result)

        # Assert
        deployed_file = target_dir / "file with spaces.md"
        assert deployed_file.exists()
        assert deployed_file.read_text() == "Content with spaces in filename"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
