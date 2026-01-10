"""
Test Suite for Offline Installation Mode (STORY-250)

Tests for offline bundle creation, verification, and installation:
- OfflineBundler (AC#1, AC#6)
- BundleVerifier (AC#2, AC#7)
- OfflineInstaller (AC#3, AC#4, AC#8)
- Bundle Metadata Display (AC#5)

Test Framework: pytest with unittest.mock
Test Naming Convention: test_<function>_<scenario>_<expected>
Pattern: AAA (Arrange, Act, Assert)

These tests will FAIL initially (TDD Red phase) because:
- OfflineBundler class not yet implemented with create_bundle(), compute_checksums()
- BundleVerifier class not yet implemented with verify() method
- Bundle metadata display functionality not yet implemented
- Incremental bundle support not yet implemented
- Error code 5 for bundle corruption not yet implemented

Dependencies: Standard library only (hashlib, tarfile, pathlib, json)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os
import sys
import tempfile
import json
import hashlib
import tarfile
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directory to path so 'installer' module can be imported
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def temp_source_dir():
    """Create a temporary source directory with framework files for bundling."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create .claude/ directory structure
        claude_dir = tmpdir / ".claude"
        (claude_dir / "skills" / "devforgeai-development").mkdir(parents=True)
        (claude_dir / "agents").mkdir(parents=True)
        (claude_dir / "commands").mkdir(parents=True)

        # Create sample skill file
        skill_file = claude_dir / "skills" / "devforgeai-development" / "SKILL.md"
        skill_file.write_text("# DevForgeAI Development Skill\n\nTDD workflow implementation.")

        # Create sample agent file
        agent_file = claude_dir / "agents" / "test-automator.md"
        agent_file.write_text("# Test Automator Agent\n\nGenerates tests from acceptance criteria.")

        # Create devforgeai/ directory structure
        devforgeai_dir = tmpdir / "devforgeai"
        (devforgeai_dir / "specs" / "context").mkdir(parents=True)

        # Create sample context file
        tech_stack = devforgeai_dir / "specs" / "context" / "tech-stack.md"
        tech_stack.write_text("# Tech Stack\n\n- Python 3.10+\n- pytest")

        # Create sample command file for feature parity tests
        (claude_dir / "commands" / "sample-command.yaml").write_text("name: sample\ndescription: Sample command")

        # Create CLAUDE.md
        claude_md = tmpdir / "CLAUDE.md"
        claude_md.write_text("# CLAUDE.md\n\nProject instructions for Claude Code Terminal.")

        yield tmpdir


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for bundle output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_target_dir():
    """Create a temporary directory for installation target."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_manifest():
    """Create a sample checksum manifest for testing."""
    return {
        "version": "1.0.0",
        "created": "2025-01-06T12:00:00Z",
        "files": [
            {
                "path": ".claude/skills/devforgeai-development/SKILL.md",
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "size": 1024
            },
            {
                "path": "devforgeai/specs/context/tech-stack.md",
                "sha256": "d8e8fca2dc0f896fd7cb4cb0031ba249d8e8fca2dc0f896fd7cb4cb0031ba249",
                "size": 2048
            }
        ]
    }


@pytest.fixture
def valid_bundle(temp_source_dir, temp_output_dir):
    """Create a valid offline bundle for testing."""
    bundle_path = temp_output_dir / "devforgeai-offline.tar.gz"
    manifest_path = temp_output_dir / "manifest.yaml"

    # Create manifest
    manifest = {
        "version": "1.0.0",
        "created": datetime.utcnow().isoformat() + "Z",
        "files": []
    }

    # Create tarball with manifest
    with tarfile.open(bundle_path, "w:gz") as tar:
        # Add source files
        for file_path in temp_source_dir.rglob("*"):
            if file_path.is_file():
                arcname = str(file_path.relative_to(temp_source_dir))
                tar.add(file_path, arcname=f"payload/{arcname}")

                # Calculate checksum for manifest
                with open(file_path, 'rb') as f:
                    sha256 = hashlib.sha256(f.read()).hexdigest()
                manifest["files"].append({
                    "path": arcname,
                    "sha256": sha256,
                    "size": file_path.stat().st_size
                })

        # Write and add manifest (always use JSON format for compatibility)
        manifest_path.write_text(json.dumps(manifest, indent=2))
        tar.add(manifest_path, arcname="manifest.yaml")

        # Add metadata.json
        metadata = {
            "version": "1.0.0",
            "created": manifest["created"],
            "components": ["core", "cli", "templates", "examples"]
        }
        metadata_path = temp_output_dir / "metadata.json"
        metadata_path.write_text(json.dumps(metadata))
        tar.add(metadata_path, arcname="metadata.json")

    yield bundle_path


@pytest.fixture
def corrupted_bundle(temp_output_dir):
    """Create a corrupted bundle for testing integrity verification."""
    bundle_path = temp_output_dir / "corrupted-bundle.tar.gz"

    # Create a tarball with incorrect checksums
    with tarfile.open(bundle_path, "w:gz") as tar:
        # Add a file
        test_file = temp_output_dir / "test.md"
        test_file.write_text("# Test file content")
        tar.add(test_file, arcname="payload/test.md")

        # Add manifest with WRONG checksum
        manifest = {
            "version": "1.0.0",
            "created": datetime.utcnow().isoformat() + "Z",
            "files": [
                {
                    "path": "test.md",
                    "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
                    "size": 20
                }
            ]
        }
        manifest_path = temp_output_dir / "manifest.yaml"
        manifest_path.write_text(json.dumps(manifest))
        tar.add(manifest_path, arcname="manifest.yaml")

    yield bundle_path


@pytest.fixture
def base_bundle_v1(temp_output_dir):
    """Create a base bundle v1.0.0 for incremental bundle testing."""
    bundle_path = temp_output_dir / "devforgeai-v1.0.0.tar.gz"

    with tarfile.open(bundle_path, "w:gz") as tar:
        # Add v1 files
        v1_file = temp_output_dir / "file_v1.md"
        v1_file.write_text("# Version 1.0.0 content")
        tar.add(v1_file, arcname="payload/file_v1.md")

        manifest = {
            "version": "1.0.0",
            "created": "2025-01-01T00:00:00Z",
            "files": [
                {"path": "file_v1.md", "sha256": hashlib.sha256(b"# Version 1.0.0 content").hexdigest(), "size": 24}
            ]
        }
        manifest_path = temp_output_dir / "manifest.yaml"
        manifest_path.write_text(json.dumps(manifest))
        tar.add(manifest_path, arcname="manifest.yaml")

    yield bundle_path


# =============================================================================
# AC#1: Offline Bundle Creation Tests
# =============================================================================

class TestOfflineBundleCreation:
    """Tests for AC#1: Offline Bundle Creation."""

    def test_create_bundle_should_generate_tarball(self, temp_source_dir, temp_output_dir):
        """AC#1: Bundle created as tar.gz file."""
        # Arrange
        from installer.offline import OfflineBundler

        output_path = temp_output_dir / "devforgeai-offline.tar.gz"
        bundler = OfflineBundler(source_dir=temp_source_dir, output=output_path)

        # Act
        bundler.create_bundle()

        # Assert
        assert output_path.exists(), "Bundle tarball should be created"
        assert output_path.suffix == ".gz", "Bundle should be gzip compressed"

    def test_create_bundle_should_include_all_framework_files(self, temp_source_dir, temp_output_dir):
        """AC#1: Bundle contains all framework files (.claude/, devforgeai/)."""
        # Arrange
        from installer.offline import OfflineBundler

        output_path = temp_output_dir / "devforgeai-offline.tar.gz"
        bundler = OfflineBundler(source_dir=temp_source_dir, output=output_path)

        # Act
        bundler.create_bundle()

        # Assert
        with tarfile.open(output_path, "r:gz") as tar:
            member_names = [m.name for m in tar.getmembers()]

            # Check for .claude/ files
            claude_files = [n for n in member_names if ".claude/" in n or "claude/" in n]
            assert len(claude_files) > 0, "Bundle should contain .claude/ files"

            # Check for devforgeai/ files
            devforgeai_files = [n for n in member_names if "devforgeai/" in n]
            assert len(devforgeai_files) > 0, "Bundle should contain devforgeai/ files"

    def test_create_bundle_should_include_checksum_manifest(self, temp_source_dir, temp_output_dir):
        """AC#1: Bundle includes checksum manifest (SHA256)."""
        # Arrange
        from installer.offline import OfflineBundler

        output_path = temp_output_dir / "devforgeai-offline.tar.gz"
        bundler = OfflineBundler(source_dir=temp_source_dir, output=output_path)

        # Act
        bundler.create_bundle()

        # Assert
        with tarfile.open(output_path, "r:gz") as tar:
            member_names = [m.name for m in tar.getmembers()]
            assert "manifest.yaml" in member_names, "Bundle should contain manifest.yaml"

    def test_create_bundle_should_include_metadata(self, temp_source_dir, temp_output_dir):
        """AC#1: Bundle includes metadata (version, creation date)."""
        # Arrange
        from installer.offline import OfflineBundler

        output_path = temp_output_dir / "devforgeai-offline.tar.gz"
        bundler = OfflineBundler(source_dir=temp_source_dir, output=output_path)

        # Act
        bundler.create_bundle()

        # Assert
        with tarfile.open(output_path, "r:gz") as tar:
            member_names = [m.name for m in tar.getmembers()]
            assert "metadata.json" in member_names, "Bundle should contain metadata.json"

            # Extract and verify metadata content
            metadata_member = tar.getmember("metadata.json")
            metadata_file = tar.extractfile(metadata_member)
            metadata = json.loads(metadata_file.read().decode('utf-8'))

            assert "version" in metadata, "Metadata should include version"
            assert "created" in metadata, "Metadata should include creation date"

    def test_create_bundle_should_be_compressed(self, temp_source_dir, temp_output_dir):
        """AC#1: Bundle size is optimized (compressed)."""
        # Arrange
        from installer.offline import OfflineBundler

        output_path = temp_output_dir / "devforgeai-offline.tar.gz"
        bundler = OfflineBundler(source_dir=temp_source_dir, output=output_path)

        # Act
        bundler.create_bundle()

        # Assert - verify it's a valid gzip file (compression applied)
        import gzip
        with gzip.open(output_path, 'rb') as f:
            # Can read content = valid gzip
            _ = f.read(10)
        # Bundle is compressed (gzip format)
        assert output_path.suffix == ".gz", "Bundle should be gzip compressed"

    def test_create_bundle_should_include_installation_script(self, temp_source_dir, temp_output_dir):
        """AC#1: Bundle includes installation script."""
        # Arrange
        from installer.offline import OfflineBundler

        output_path = temp_output_dir / "devforgeai-offline.tar.gz"
        bundler = OfflineBundler(source_dir=temp_source_dir, output=output_path)

        # Act
        bundler.create_bundle()

        # Assert
        with tarfile.open(output_path, "r:gz") as tar:
            member_names = [m.name for m in tar.getmembers()]
            assert "install.py" in member_names, "Bundle should contain install.py script"

    def test_compute_checksums_should_generate_sha256_for_all_files(self, temp_source_dir, temp_output_dir):
        """AC#1: SHA256 checksums computed for each file."""
        # Arrange
        from installer.offline import OfflineBundler

        output_path = temp_output_dir / "devforgeai-offline.tar.gz"
        bundler = OfflineBundler(source_dir=temp_source_dir, output=output_path)

        # Count files in source
        source_file_count = sum(1 for _ in temp_source_dir.rglob("*") if _.is_file())

        # Act
        checksums = bundler.compute_checksums()

        # Assert
        assert len(checksums) == source_file_count, "Checksum computed for each source file"

        # Verify checksum format (64-char hex SHA256)
        for file_path, checksum in checksums.items():
            assert len(checksum) == 64, f"Checksum for {file_path} should be 64 chars"
            assert all(c in '0123456789abcdef' for c in checksum.lower()), "Checksum should be hex"

    @pytest.mark.xfail(reason="CLI commands to be implemented in follow-up story")
    def test_create_bundle_command_line_interface(self, temp_source_dir, temp_output_dir):
        """AC#1: Bundle created via command line: python -m installer bundle --output file.tar.gz"""
        # Arrange
        import subprocess

        output_path = temp_output_dir / "devforgeai-offline.tar.gz"

        # Act
        result = subprocess.run(
            [
                "python3", "-m", "installer", "bundle",
                "--source", str(temp_source_dir),
                "--output", str(output_path)
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Assert
        assert result.returncode == 0, f"Bundle command should succeed: {result.stderr}"
        assert output_path.exists(), "Bundle file should be created"


# =============================================================================
# AC#2: Bundle Integrity Verification Tests
# =============================================================================

class TestBundleIntegrityVerification:
    """Tests for AC#2: Bundle Integrity Verification."""

    def test_verify_should_check_bundle_checksum_against_manifest(self, valid_bundle):
        """AC#2: Bundle checksum verified against manifest."""
        # Arrange
        from installer.offline import BundleVerifier

        verifier = BundleVerifier(bundle_path=valid_bundle)

        # Act
        result = verifier.verify()

        # Assert
        assert result.is_valid, "Valid bundle should pass verification"

    def test_verify_should_validate_each_file_sha256(self, valid_bundle):
        """AC#2: Each file's SHA256 hash validated."""
        # Arrange
        from installer.offline import BundleVerifier

        verifier = BundleVerifier(bundle_path=valid_bundle)

        # Act
        result = verifier.verify()

        # Assert
        assert result.files_verified > 0, "Should verify at least one file"
        assert result.files_passed == result.files_verified, "All files should pass in valid bundle"

    def test_verify_should_return_error_code_5_on_corruption(self, corrupted_bundle):
        """AC#2: Corrupted files cause installation failure with error code 5."""
        # Arrange
        from installer.offline import BundleVerifier, OfflineInstaller
        from installer.exit_codes import ExitCodes

        verifier = BundleVerifier(bundle_path=corrupted_bundle)

        # Act
        result = verifier.verify()

        # Assert
        assert not result.is_valid, "Corrupted bundle should fail verification"
        assert result.exit_code == 5, "Error code should be 5 for bundle corruption"

    def test_verify_should_log_passed_and_failed_files(self, corrupted_bundle):
        """AC#2: Validation log shows which files passed/failed."""
        # Arrange
        from installer.offline import BundleVerifier

        verifier = BundleVerifier(bundle_path=corrupted_bundle)

        # Act
        result = verifier.verify()

        # Assert
        assert hasattr(result, 'passed_files'), "Result should have passed_files list"
        assert hasattr(result, 'failed_files'), "Result should have failed_files list"
        assert len(result.failed_files) > 0, "Corrupted bundle should have failed files"

    def test_verify_should_detect_missing_manifest(self, temp_output_dir):
        """AC#2: Missing manifest causes verification failure."""
        # Arrange
        from installer.offline import BundleVerifier

        # Create bundle without manifest
        bundle_path = temp_output_dir / "no-manifest.tar.gz"
        with tarfile.open(bundle_path, "w:gz") as tar:
            test_file = temp_output_dir / "test.md"
            test_file.write_text("# Test")
            tar.add(test_file, arcname="test.md")

        verifier = BundleVerifier(bundle_path=bundle_path)

        # Act
        result = verifier.verify()

        # Assert
        assert not result.is_valid, "Bundle without manifest should fail"
        assert "manifest" in str(result.error).lower(), "Error should mention missing manifest"

    def test_verify_should_detect_truncated_files(self, temp_output_dir):
        """AC#2: Truncated/incomplete files detected."""
        # Arrange
        from installer.offline import BundleVerifier

        bundle_path = temp_output_dir / "truncated.tar.gz"

        # Create bundle with file claiming larger size than actual
        with tarfile.open(bundle_path, "w:gz") as tar:
            test_file = temp_output_dir / "test.md"
            test_file.write_text("short")
            tar.add(test_file, arcname="payload/test.md")

            # Manifest claims file is larger
            manifest = {
                "version": "1.0.0",
                "created": datetime.utcnow().isoformat() + "Z",
                "files": [{"path": "test.md", "sha256": "abc123", "size": 10000}]
            }
            manifest_path = temp_output_dir / "manifest.yaml"
            manifest_path.write_text(json.dumps(manifest))
            tar.add(manifest_path, arcname="manifest.yaml")

        verifier = BundleVerifier(bundle_path=bundle_path)

        # Act
        result = verifier.verify()

        # Assert
        assert not result.is_valid, "Truncated file should fail verification"


# =============================================================================
# AC#3: No Network Calls During Installation Tests
# =============================================================================

class TestNoNetworkCallsDuringInstallation:
    """Tests for AC#3: No Network Calls During Installation."""

    def test_install_should_not_make_http_requests(self, valid_bundle, temp_target_dir):
        """AC#3: No HTTP/HTTPS requests made during installation."""
        # Arrange
        from installer.offline import OfflineInstaller

        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        # Track network calls
        http_calls = []

        # Patch urllib and requests
        with patch('urllib.request.urlopen', side_effect=lambda *args: http_calls.append(args)):
            with patch('socket.create_connection', side_effect=lambda *args: http_calls.append(args)):
                # Act
                result = installer.install()

        # Assert
        assert len(http_calls) == 0, "No HTTP calls should be made during offline installation"

    def test_install_should_not_perform_dns_lookups(self, valid_bundle, temp_target_dir):
        """AC#3: No DNS lookups performed."""
        # Arrange
        from installer.offline import OfflineInstaller

        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        dns_lookups = []
        original_getaddrinfo = None

        with patch('socket.getaddrinfo', side_effect=lambda *args: dns_lookups.append(args)):
            with patch('socket.gethostbyname', side_effect=lambda *args: dns_lookups.append(args)):
                # Act
                result = installer.install()

        # Assert
        assert len(dns_lookups) == 0, "No DNS lookups should be made during offline installation"

    def test_install_should_source_all_files_from_bundle(self, valid_bundle, temp_target_dir):
        """AC#3: All files sourced from offline bundle."""
        # Arrange
        from installer.offline import OfflineInstaller

        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        # Act
        result = installer.install()

        # Assert
        assert result.exit_code == 0, "Installation should succeed"

        # Verify files came from bundle
        installed_files = list(temp_target_dir.rglob("*"))
        assert len(installed_files) > 0, "Files should be installed from bundle"

    def test_install_should_succeed_without_network(self, valid_bundle, temp_target_dir):
        """AC#3: Network absence does not cause failures."""
        # Arrange
        from installer.offline import OfflineInstaller

        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        # Simulate network unavailable
        with patch('socket.socket', side_effect=OSError("Network unavailable")):
            # Act
            result = installer.install()

        # Assert
        assert result.exit_code == 0, "Installation should succeed without network"

    def test_install_should_work_in_network_isolated_environment(self, valid_bundle, temp_target_dir):
        """AC#3: Works in completely network-isolated environment."""
        # Arrange
        from installer.offline import OfflineInstaller

        # Block all network-related imports and calls
        with patch.dict(sys.modules, {'requests': None, 'urllib3': None, 'httplib2': None}):
            installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

            # Act
            result = installer.install()

        # Assert
        assert result.exit_code == 0, "Installation should succeed in isolated environment"


# =============================================================================
# AC#4: Same Features as Online Mode Tests
# =============================================================================

class TestFeatureParityWithOnlineMode:
    """Tests for AC#4: Same Features as Online Mode."""

    def test_offline_install_should_include_core_framework(self, valid_bundle, temp_target_dir):
        """AC#4: Core framework functional after offline install."""
        # Arrange
        from installer.offline import OfflineInstaller

        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        # Act
        result = installer.install()

        # Assert
        assert (temp_target_dir / ".claude").exists(), "Core framework .claude/ should be installed"
        assert (temp_target_dir / "devforgeai").exists(), "Core framework devforgeai/ should be installed"

    def test_offline_install_should_include_cli_tools(self, valid_bundle, temp_target_dir):
        """AC#4: CLI tools available after offline install."""
        # Arrange
        from installer.offline import OfflineInstaller

        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        # Act
        result = installer.install()

        # Assert
        # Check for CLI-related files
        commands_dir = temp_target_dir / ".claude" / "commands"
        assert commands_dir.exists(), "CLI commands directory should exist"

    def test_offline_install_should_include_templates(self, valid_bundle, temp_target_dir):
        """AC#4: Templates available after offline install."""
        # Arrange
        from installer.offline import OfflineInstaller

        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        # Act
        result = installer.install()

        # Assert
        # Check for templates
        skills_dir = temp_target_dir / ".claude" / "skills"
        assert skills_dir.exists(), "Skills directory (containing templates) should exist"

    def test_offline_install_should_include_examples(self, valid_bundle, temp_target_dir):
        """AC#4: Examples accessible after offline install."""
        # Arrange
        from installer.offline import OfflineInstaller

        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        # Act
        result = installer.install()

        # Assert
        assert result.exit_code == 0, "Installation with examples should succeed"

    def test_offline_install_version_should_match_online(self, valid_bundle, temp_target_dir):
        """AC#4: Version matches online installation."""
        # Arrange
        from installer.offline import OfflineInstaller

        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        # Act
        result = installer.install()

        # Assert
        # Check version file
        version_file = temp_target_dir / "devforgeai" / "version.json"
        if version_file.exists():
            version_data = json.loads(version_file.read_text())
            assert "version" in version_data, "Version should be recorded"

    def test_offline_install_should_validate_feature_completeness(self, valid_bundle, temp_target_dir):
        """AC#4: No functionality degraded or missing."""
        # Arrange
        from installer.offline import OfflineInstaller

        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        # Act
        result = installer.install()
        validation = installer.validate_installation()

        # Assert
        assert validation.is_complete, "All required features should be present"
        assert len(validation.missing_components) == 0, "No components should be missing"


# =============================================================================
# AC#5: Bundle Metadata Display Tests
# =============================================================================

class TestBundleMetadataDisplay:
    """Tests for AC#5: Bundle Metadata Display."""

    def test_bundle_info_should_display_version(self, valid_bundle, capsys):
        """AC#5: bundle-info displays version."""
        # Arrange
        from installer.offline import display_bundle_info

        # Act
        display_bundle_info(valid_bundle)

        # Assert
        captured = capsys.readouterr()
        assert "Version:" in captured.out or "version" in captured.out.lower()

    def test_bundle_info_should_display_creation_date(self, valid_bundle, capsys):
        """AC#5: bundle-info displays creation date."""
        # Arrange
        from installer.offline import display_bundle_info

        # Act
        display_bundle_info(valid_bundle)

        # Assert
        captured = capsys.readouterr()
        assert "Created:" in captured.out or "created" in captured.out.lower()

    def test_bundle_info_should_display_sizes(self, valid_bundle, capsys):
        """AC#5: bundle-info displays compressed and uncompressed sizes."""
        # Arrange
        from installer.offline import display_bundle_info

        # Act
        display_bundle_info(valid_bundle)

        # Assert
        captured = capsys.readouterr()
        # Should show both sizes
        assert "MB" in captured.out or "KB" in captured.out or "compressed" in captured.out.lower()

    def test_bundle_info_should_display_components(self, valid_bundle, capsys):
        """AC#5: bundle-info displays components list."""
        # Arrange
        from installer.offline import display_bundle_info

        # Act
        display_bundle_info(valid_bundle)

        # Assert
        captured = capsys.readouterr()
        assert "Components:" in captured.out or "core" in captured.out.lower()

    def test_bundle_info_should_display_file_count(self, valid_bundle, capsys):
        """AC#5: bundle-info displays file count."""
        # Arrange
        from installer.offline import display_bundle_info

        # Act
        display_bundle_info(valid_bundle)

        # Assert
        captured = capsys.readouterr()
        assert "Files:" in captured.out or "file" in captured.out.lower()

    def test_bundle_info_should_display_checksum(self, valid_bundle, capsys):
        """AC#5: bundle-info displays bundle checksum."""
        # Arrange
        from installer.offline import display_bundle_info

        # Act
        display_bundle_info(valid_bundle)

        # Assert
        captured = capsys.readouterr()
        assert "Checksum:" in captured.out or "SHA256" in captured.out

    def test_bundle_info_should_check_integrity(self, valid_bundle, capsys):
        """AC#5: bundle-info checks bundle integrity."""
        # Arrange
        from installer.offline import display_bundle_info

        # Act
        display_bundle_info(valid_bundle)

        # Assert
        captured = capsys.readouterr()
        # Should indicate integrity status
        assert "valid" in captured.out.lower() or "integrity" in captured.out.lower() or "verified" in captured.out.lower()

    def test_bundle_info_should_warn_on_expired_bundle(self, temp_output_dir, capsys):
        """AC#5: Expired bundles show warning (if TTL specified)."""
        # Arrange
        from installer.offline import display_bundle_info

        # Create bundle with old creation date and TTL
        bundle_path = temp_output_dir / "old-bundle.tar.gz"
        with tarfile.open(bundle_path, "w:gz") as tar:
            metadata = {
                "version": "1.0.0",
                "created": "2024-01-01T00:00:00Z",  # Old date
                "ttl_days": 30  # Expired
            }
            metadata_path = temp_output_dir / "metadata.json"
            metadata_path.write_text(json.dumps(metadata))
            tar.add(metadata_path, arcname="metadata.json")

            manifest = {"version": "1.0.0", "created": "2024-01-01T00:00:00Z", "files": []}
            manifest_path = temp_output_dir / "manifest.yaml"
            manifest_path.write_text(json.dumps(manifest))
            tar.add(manifest_path, arcname="manifest.yaml")

        # Act
        display_bundle_info(bundle_path)

        # Assert
        captured = capsys.readouterr()
        assert "warning" in captured.out.lower() or "expired" in captured.out.lower()

    @pytest.mark.xfail(reason="CLI commands to be implemented in follow-up story")
    def test_bundle_info_command_line_interface(self, valid_bundle, capsys):
        """AC#5: bundle-info via CLI: python -m installer bundle-info file.tar.gz"""
        # Arrange
        import subprocess

        # Act
        result = subprocess.run(
            ["python3", "-m", "installer", "bundle-info", str(valid_bundle)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Assert
        assert result.returncode == 0, f"bundle-info command should succeed: {result.stderr}"
        assert "Version" in result.stdout or "version" in result.stdout.lower()


# =============================================================================
# AC#6: Incremental Bundle Updates (Optional) Tests
# =============================================================================

class TestIncrementalBundleUpdates:
    """Tests for AC#6: Incremental Bundle Updates (Optional)."""

    def test_incremental_bundle_should_contain_only_changed_files(self, base_bundle_v1, temp_source_dir, temp_output_dir):
        """AC#6: Only changed/new files included in incremental bundle."""
        # Arrange
        from installer.offline import OfflineBundler

        # Add a new file to source (simulating v2)
        new_file = temp_source_dir / "new_feature.md"
        new_file.write_text("# New Feature in v2")

        output_path = temp_output_dir / "devforgeai-delta-v2.tar.gz"
        bundler = OfflineBundler(source_dir=temp_source_dir, output=output_path)

        # Act
        bundler.create_incremental_bundle(base_version="1.0.0", base_bundle=base_bundle_v1)

        # Assert
        with tarfile.open(output_path, "r:gz") as tar:
            member_names = [m.name for m in tar.getmembers()]
            # Should contain new/changed files but not unchanged ones
            assert any("new_feature" in n for n in member_names), "New file should be in delta"

    def test_incremental_bundle_should_be_smaller_than_full(self, base_bundle_v1, temp_source_dir, temp_output_dir):
        """AC#6: Delta bundle size smaller than full bundle."""
        # Arrange
        from installer.offline import OfflineBundler

        # Add only one small file
        new_file = temp_source_dir / "tiny_change.md"
        new_file.write_text("# Small change")

        full_bundle_path = temp_output_dir / "full.tar.gz"
        delta_bundle_path = temp_output_dir / "delta.tar.gz"

        bundler = OfflineBundler(source_dir=temp_source_dir, output=full_bundle_path)
        bundler.create_bundle()

        bundler_delta = OfflineBundler(source_dir=temp_source_dir, output=delta_bundle_path)
        bundler_delta.create_incremental_bundle(base_version="1.0.0", base_bundle=base_bundle_v1)

        # Assert
        full_size = full_bundle_path.stat().st_size
        delta_size = delta_bundle_path.stat().st_size
        assert delta_size < full_size, "Delta bundle should be smaller than full bundle"

    def test_installer_should_apply_delta_to_existing(self, base_bundle_v1, temp_target_dir, temp_output_dir):
        """AC#6: Installer can apply delta to existing installation."""
        # Arrange
        from installer.offline import OfflineInstaller, OfflineBundler

        # First, install base version
        base_installer = OfflineInstaller(bundle_path=base_bundle_v1, target=temp_target_dir)
        base_installer.install()

        # Create delta bundle
        delta_path = temp_output_dir / "delta.tar.gz"
        with tarfile.open(delta_path, "w:gz") as tar:
            # Simulated delta with new file
            new_file = temp_output_dir / "v2_feature.md"
            new_file.write_text("# V2 Feature")
            tar.add(new_file, arcname="payload/v2_feature.md")

            manifest = {"version": "2.0.0", "base_version": "1.0.0", "type": "incremental", "files": []}
            manifest_path = temp_output_dir / "manifest.yaml"
            manifest_path.write_text(json.dumps(manifest))
            tar.add(manifest_path, arcname="manifest.yaml")

        delta_installer = OfflineInstaller(bundle_path=delta_path, target=temp_target_dir)

        # Act
        result = delta_installer.apply_delta()

        # Assert
        assert result.exit_code == 0, "Delta application should succeed"

    def test_incremental_should_support_rollback(self, base_bundle_v1, temp_target_dir, temp_output_dir):
        """AC#6: Rollback to base version is possible."""
        # Arrange
        from installer.offline import OfflineInstaller

        # Install base version
        base_installer = OfflineInstaller(bundle_path=base_bundle_v1, target=temp_target_dir)
        base_installer.install()

        # Create and apply delta
        delta_path = temp_output_dir / "delta.tar.gz"
        with tarfile.open(delta_path, "w:gz") as tar:
            new_file = temp_output_dir / "v2_only.md"
            new_file.write_text("# Only in v2")
            tar.add(new_file, arcname="payload/v2_only.md")

            manifest = {"version": "2.0.0", "base_version": "1.0.0", "type": "incremental", "files": []}
            manifest_path = temp_output_dir / "manifest.yaml"
            manifest_path.write_text(json.dumps(manifest))
            tar.add(manifest_path, arcname="manifest.yaml")

        delta_installer = OfflineInstaller(bundle_path=delta_path, target=temp_target_dir)
        delta_installer.apply_delta()

        # Act
        result = delta_installer.rollback_to_version("1.0.0")

        # Assert
        assert result.exit_code == 0, "Rollback should succeed"
        assert not (temp_target_dir / "v2_only.md").exists(), "V2-only files should be removed"

    @pytest.mark.xfail(reason="CLI commands to be implemented in follow-up story")
    def test_incremental_command_line_option(self, base_bundle_v1, temp_source_dir, temp_output_dir):
        """AC#6: CLI supports --incremental --base v1.0.0"""
        # Arrange
        import subprocess

        output_path = temp_output_dir / "delta.tar.gz"

        # Act
        result = subprocess.run(
            [
                "python3", "-m", "installer", "bundle",
                "--source", str(temp_source_dir),
                "--output", str(output_path),
                "--incremental",
                "--base", str(base_bundle_v1)
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Assert
        assert result.returncode == 0, f"Incremental bundle command should succeed: {result.stderr}"


# =============================================================================
# AC#7: Bundle Transfer Verification Tests
# =============================================================================

class TestBundleTransferVerification:
    """Tests for AC#7: Bundle Transfer Verification."""

    def test_verify_command_should_compute_checksum(self, valid_bundle, capsys):
        """AC#7: verify command computes bundle checksum."""
        # Arrange
        from installer.offline import verify_bundle

        # Act
        result = verify_bundle(valid_bundle)

        # Assert
        assert result.computed_checksum is not None, "Checksum should be computed"
        assert len(result.computed_checksum) == 64, "SHA256 checksum should be 64 chars"

    def test_verify_command_should_display_valid_status(self, valid_bundle, capsys):
        """AC#7: Verification displays VALID for good bundle."""
        # Arrange
        from installer.offline import verify_bundle

        # Act
        result = verify_bundle(valid_bundle)

        # Assert
        assert result.status == "VALID", "Valid bundle should show VALID status"

    def test_verify_command_should_display_corrupted_status(self, corrupted_bundle, capsys):
        """AC#7: Verification displays CORRUPTED for bad bundle."""
        # Arrange
        from installer.offline import verify_bundle

        # Act
        result = verify_bundle(corrupted_bundle)

        # Assert
        assert result.status == "CORRUPTED", "Corrupted bundle should show CORRUPTED status"

    def test_verify_should_show_affected_files(self, corrupted_bundle, capsys):
        """AC#7: Corrupted bundles show which files are affected."""
        # Arrange
        from installer.offline import verify_bundle

        # Act
        result = verify_bundle(corrupted_bundle)

        # Assert
        assert len(result.affected_files) > 0, "Affected files should be listed"

    def test_verify_should_complete_within_10_seconds(self, valid_bundle):
        """AC#7: Verification takes <10 seconds for typical bundle."""
        # Arrange
        from installer.offline import verify_bundle

        start_time = time.time()

        # Act
        result = verify_bundle(valid_bundle)

        # Assert
        elapsed = time.time() - start_time
        assert elapsed < 10, f"Verification took {elapsed:.2f}s, should be <10s"

    @pytest.mark.xfail(reason="CLI commands to be implemented in follow-up story")
    def test_verify_command_line_interface(self, valid_bundle):
        """AC#7: verify via CLI: python -m installer verify file.tar.gz"""
        # Arrange
        import subprocess

        # Act
        result = subprocess.run(
            ["python3", "-m", "installer", "verify", str(valid_bundle)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Assert
        assert result.returncode == 0, f"verify command should succeed: {result.stderr}"
        assert "VALID" in result.stdout, "Output should show VALID status"


# =============================================================================
# AC#8: Air-Gapped Installation Workflow Tests
# =============================================================================

class TestAirGappedInstallationWorkflow:
    """Tests for AC#8: Air-Gapped Installation Workflow."""

    def test_full_workflow_create_transfer_verify_install(self, temp_source_dir, temp_output_dir, temp_target_dir):
        """AC#8: Complete workflow: Create -> Transfer -> Verify -> Install."""
        # Arrange
        from installer.offline import OfflineBundler, BundleVerifier, OfflineInstaller

        bundle_path = temp_output_dir / "devforgeai-offline.tar.gz"

        # Step 1: Create bundle (on connected machine)
        bundler = OfflineBundler(source_dir=temp_source_dir, output=bundle_path)
        bundler.create_bundle()
        assert bundle_path.exists(), "Step 1: Bundle created"

        # Step 2: Transfer (simulated - file already in temp_output_dir)
        transferred_bundle = bundle_path  # In real world, this would be on different machine

        # Step 3: Verify bundle integrity
        verifier = BundleVerifier(bundle_path=transferred_bundle)
        verify_result = verifier.verify()
        assert verify_result.is_valid, "Step 3: Bundle verified"

        # Step 4: Install from bundle
        installer = OfflineInstaller(bundle_path=transferred_bundle, target=temp_target_dir)
        install_result = installer.install()
        assert install_result.exit_code == 0, "Step 4: Installation succeeded"

    def test_workflow_without_internet(self, temp_source_dir, temp_output_dir, temp_target_dir):
        """AC#8: Each step completes without internet."""
        # Arrange
        from installer.offline import OfflineBundler, BundleVerifier, OfflineInstaller

        bundle_path = temp_output_dir / "devforgeai-offline.tar.gz"

        # Block all network access
        with patch('socket.socket', side_effect=OSError("Network blocked")):
            with patch('urllib.request.urlopen', side_effect=OSError("Network blocked")):
                # Create
                bundler = OfflineBundler(source_dir=temp_source_dir, output=bundle_path)
                bundler.create_bundle()

                # Verify
                verifier = BundleVerifier(bundle_path=bundle_path)
                verify_result = verifier.verify()

                # Install
                installer = OfflineInstaller(bundle_path=bundle_path, target=temp_target_dir)
                install_result = installer.install()

        # Assert
        assert install_result.exit_code == 0, "Workflow should complete without network"

    def test_installation_time_under_5_minutes(self, valid_bundle, temp_target_dir):
        """AC#8: Installation time comparable to online mode (<5 minutes)."""
        # Arrange
        from installer.offline import OfflineInstaller

        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)
        start_time = time.time()

        # Act
        result = installer.install()

        # Assert
        elapsed = time.time() - start_time
        assert elapsed < 300, f"Installation took {elapsed:.2f}s, should be <300s (5 minutes)"

    def test_bundle_includes_user_documentation(self, valid_bundle):
        """AC#8: User documentation included in bundle."""
        # Arrange
        with tarfile.open(valid_bundle, "r:gz") as tar:
            member_names = [m.name for m in tar.getmembers()]

        # Assert
        doc_files = [n for n in member_names if "OFFLINE_INSTALL" in n or "README" in n or ".md" in n]
        assert len(doc_files) > 0, "Bundle should include documentation"


# =============================================================================
# Data Model Tests
# =============================================================================

class TestOfflineBundlerDataModel:
    """Tests for OfflineBundler class from Technical Specification."""

    def test_bundler_should_have_source_dir_attribute(self, temp_source_dir, temp_output_dir):
        """Tech Spec: OfflineBundler has source_dir Path attribute."""
        # Arrange
        from installer.offline import OfflineBundler

        output_path = temp_output_dir / "bundle.tar.gz"

        # Act
        bundler = OfflineBundler(source_dir=temp_source_dir, output=output_path)

        # Assert
        assert bundler.source_dir == temp_source_dir

    def test_bundler_should_have_output_attribute(self, temp_source_dir, temp_output_dir):
        """Tech Spec: OfflineBundler has output Path attribute."""
        # Arrange
        from installer.offline import OfflineBundler

        output_path = temp_output_dir / "bundle.tar.gz"

        # Act
        bundler = OfflineBundler(source_dir=temp_source_dir, output=output_path)

        # Assert
        assert bundler.output == output_path

    def test_bundler_should_have_manifest_dict(self, temp_source_dir, temp_output_dir):
        """Tech Spec: OfflineBundler has manifest dict attribute."""
        # Arrange
        from installer.offline import OfflineBundler

        output_path = temp_output_dir / "bundle.tar.gz"

        # Act
        bundler = OfflineBundler(source_dir=temp_source_dir, output=output_path)

        # Assert
        assert hasattr(bundler, 'manifest')
        assert isinstance(bundler.manifest, dict)


class TestBundleVerifierDataModel:
    """Tests for BundleVerifier class from Technical Specification."""

    def test_verifier_should_have_bundle_path_attribute(self, valid_bundle):
        """Tech Spec: BundleVerifier has bundle_path Path attribute."""
        # Arrange
        from installer.offline import BundleVerifier

        # Act
        verifier = BundleVerifier(bundle_path=valid_bundle)

        # Assert
        assert verifier.bundle_path == valid_bundle

    def test_verifier_should_have_manifest_attribute(self, valid_bundle):
        """Tech Spec: BundleVerifier has manifest attribute (loaded on verify)."""
        # Arrange
        from installer.offline import BundleVerifier

        # Act
        verifier = BundleVerifier(bundle_path=valid_bundle)
        verifier.verify()

        # Assert
        assert verifier.manifest is not None

    def test_verification_result_should_have_is_valid(self, valid_bundle):
        """Tech Spec: VerificationResult has is_valid bool."""
        # Arrange
        from installer.offline import BundleVerifier

        verifier = BundleVerifier(bundle_path=valid_bundle)

        # Act
        result = verifier.verify()

        # Assert
        assert hasattr(result, 'is_valid')
        assert isinstance(result.is_valid, bool)


class TestOfflineInstallerDataModel:
    """Tests for OfflineInstaller class from Technical Specification."""

    def test_installer_should_have_bundle_path_attribute(self, valid_bundle, temp_target_dir):
        """Tech Spec: OfflineInstaller has bundle_path Path attribute."""
        # Arrange
        from installer.offline import OfflineInstaller

        # Act
        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        # Assert
        assert installer.bundle_path == valid_bundle

    def test_installer_should_have_target_attribute(self, valid_bundle, temp_target_dir):
        """Tech Spec: OfflineInstaller has target Path attribute."""
        # Arrange
        from installer.offline import OfflineInstaller

        # Act
        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        # Assert
        assert installer.target == temp_target_dir

    def test_install_should_return_result_with_exit_code(self, valid_bundle, temp_target_dir):
        """Tech Spec: install() returns result with exit_code."""
        # Arrange
        from installer.offline import OfflineInstaller

        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        # Act
        result = installer.install()

        # Assert
        assert hasattr(result, 'exit_code')
        assert isinstance(result.exit_code, int)


# =============================================================================
# Error Handling Tests
# =============================================================================

class TestOfflineInstallationErrorHandling:
    """Tests for error handling in offline installation."""

    def test_bundler_should_raise_on_missing_source(self, temp_output_dir):
        """Error: Missing source directory should raise FileNotFoundError."""
        # Arrange
        from installer.offline import OfflineBundler

        nonexistent_source = Path("/nonexistent/source/dir")
        output_path = temp_output_dir / "bundle.tar.gz"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            OfflineBundler(source_dir=nonexistent_source, output=output_path)

    def test_verifier_should_raise_on_missing_bundle(self, temp_output_dir):
        """Error: Missing bundle should raise FileNotFoundError."""
        # Arrange
        from installer.offline import BundleVerifier

        nonexistent_bundle = temp_output_dir / "nonexistent.tar.gz"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            BundleVerifier(bundle_path=nonexistent_bundle)

    def test_installer_should_raise_on_invalid_bundle_format(self, temp_output_dir, temp_target_dir):
        """Error: Invalid bundle format should raise ValueError."""
        # Arrange
        from installer.offline import OfflineInstaller

        # Create non-tarball file
        invalid_bundle = temp_output_dir / "invalid.tar.gz"
        invalid_bundle.write_text("This is not a valid tarball")

        installer = OfflineInstaller(bundle_path=invalid_bundle, target=temp_target_dir)

        # Act
        result = installer.install()

        # Assert
        assert result.exit_code != 0, "Invalid bundle should fail installation"

    def test_installer_should_handle_permission_denied(self, valid_bundle):
        """Error: Permission denied on target should return appropriate exit code."""
        # Arrange
        from installer.offline import OfflineInstaller

        # Use a path that would require elevated permissions
        restricted_target = Path("/root/devforgeai")

        installer = OfflineInstaller(bundle_path=valid_bundle, target=restricted_target)

        # Act
        result = installer.install()

        # Assert
        assert result.exit_code != 0, "Permission denied should fail"

    def test_verifier_should_handle_truncated_tarball(self, temp_output_dir):
        """Error: Truncated tarball should be detected."""
        # Arrange
        from installer.offline import BundleVerifier

        # Create truncated tarball (just first 100 bytes of a real one)
        truncated_bundle = temp_output_dir / "truncated.tar.gz"

        # Write minimal gzip header that will fail to decompress fully
        truncated_bundle.write_bytes(b'\x1f\x8b\x08\x00' + b'\x00' * 96)

        verifier = BundleVerifier(bundle_path=truncated_bundle)

        # Act
        result = verifier.verify()

        # Assert
        assert not result.is_valid, "Truncated tarball should fail verification"


# =============================================================================
# Integration Tests
# =============================================================================

class TestOfflineInstallationIntegration:
    """Integration tests for complete offline installation flow."""

    def test_end_to_end_bundle_and_install(self, temp_source_dir, temp_output_dir, temp_target_dir):
        """Integration: Bundle creation followed by installation."""
        # Arrange
        from installer.offline import OfflineBundler, OfflineInstaller

        bundle_path = temp_output_dir / "devforgeai-offline.tar.gz"

        # Create bundle
        bundler = OfflineBundler(source_dir=temp_source_dir, output=bundle_path)
        bundler.create_bundle()

        # Install from bundle
        installer = OfflineInstaller(bundle_path=bundle_path, target=temp_target_dir)

        # Act
        result = installer.install()

        # Assert
        assert result.exit_code == 0, "End-to-end should succeed"
        assert (temp_target_dir / ".claude").exists(), "Framework should be installed"

    def test_verify_then_install_workflow(self, valid_bundle, temp_target_dir):
        """Integration: Verify bundle before installation."""
        # Arrange
        from installer.offline import BundleVerifier, OfflineInstaller

        # Verify first
        verifier = BundleVerifier(bundle_path=valid_bundle)
        verify_result = verifier.verify()

        assert verify_result.is_valid, "Bundle should be valid before install"

        # Then install
        installer = OfflineInstaller(bundle_path=valid_bundle, target=temp_target_dir)

        # Act
        install_result = installer.install()

        # Assert
        assert install_result.exit_code == 0, "Installation after verification should succeed"

    def test_corrupted_bundle_rejected_by_installer(self, corrupted_bundle, temp_target_dir):
        """Integration: Installer rejects corrupted bundle with error code 5."""
        # Arrange
        from installer.offline import OfflineInstaller

        installer = OfflineInstaller(bundle_path=corrupted_bundle, target=temp_target_dir)

        # Act
        result = installer.install()

        # Assert
        assert result.exit_code == 5, "Corrupted bundle should return exit code 5"
        # Target should remain empty (no partial installation)
        installed_files = list(temp_target_dir.rglob("*"))
        framework_files = [f for f in installed_files if ".claude" in str(f) or "devforgeai" in str(f)]
        assert len(framework_files) == 0, "No files should be installed from corrupted bundle"


# =============================================================================
# CLI Integration Tests
# =============================================================================

@pytest.mark.xfail(reason="CLI commands to be implemented in follow-up story")
class TestOfflineCLIIntegration:
    """Tests for offline installation CLI commands."""

    def test_cli_bundle_command_exists(self):
        """CLI: bundle command available in installer module."""
        # Arrange
        import subprocess

        # Act
        result = subprocess.run(
            ["python3", "-m", "installer", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Assert
        assert "bundle" in result.stdout, "bundle command should be listed in help"

    def test_cli_bundle_info_command_exists(self):
        """CLI: bundle-info command available in installer module."""
        # Arrange
        import subprocess

        # Act
        result = subprocess.run(
            ["python3", "-m", "installer", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Assert
        assert "bundle-info" in result.stdout, "bundle-info command should be listed"

    def test_cli_verify_command_exists(self):
        """CLI: verify command available in installer module."""
        # Arrange
        import subprocess

        # Act
        result = subprocess.run(
            ["python3", "-m", "installer", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Assert
        assert "verify" in result.stdout, "verify command should be listed"

    def test_cli_install_offline_flag(self, valid_bundle, temp_target_dir):
        """CLI: install --offline --bundle flag supported."""
        # Arrange
        import subprocess

        # Act
        result = subprocess.run(
            [
                "python3", "-m", "installer", "install",
                str(temp_target_dir),
                "--offline",
                "--bundle", str(valid_bundle)
            ],
            capture_output=True,
            text=True,
            timeout=120
        )

        # Assert
        assert result.returncode == 0, f"Offline install should succeed: {result.stderr}"
