"""
STORY-069: Offline Installation Support - Python Tests
Unit and integration tests for offline installation capabilities.

Tests validate 8 acceptance criteria:
AC#1: Complete Framework Bundle in NPM Package
AC#2: No External Downloads During Installation
AC#3: Python CLI Bundled Installation
AC#4: Graceful Degradation for Optional Dependencies
AC#5: Pre-Installation Network Check
AC#6: Offline Mode Validation
AC#7: Clear Error Messages for Network-Dependent Features
AC#8: Bundle Integrity Verification

Technical Specification Coverage:
- SVC-001: Network detection with timeout
- SVC-002: No HTTP requests during offline install
- SVC-003: Checksum verification detects corrupted files
- CONF-001: All bundled files have checksums
- DM-001: Framework directories bundled (.claude/, .devforgeai/)
- DM-002: Python wheel files bundled
- DM-003: Compressed package ≤ 60MB

Expected Result: ALL TESTS SHOULD FAIL (TDD Red Phase)
Implementation: Offline installation functionality does not exist yet
"""

import pytest
import json
import time
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open, call
from urllib.error import URLError
import socket
import hashlib


class TestNetworkDetection:
    """
    AC#5: Pre-Installation Network Check
    SVC-001: Network detection with timeout
    """

    def test_network_detection_online_success(self):
        """
        AC#5: Installer detects online mode when network available.

        Given: Network connection is available
        When: Installer performs pre-flight validation
        Then: Network status = "Online"
        """
        # Arrange
        from installer.install import check_network_availability

        # Mock socket connection success
        with patch('socket.create_connection') as mock_socket:
            mock_socket.return_value = MagicMock()

            # Act
            is_online = check_network_availability(timeout=2)

            # Assert
            assert is_online is True
            mock_socket.assert_called_once()

    def test_network_detection_offline_timeout(self):
        """
        AC#5: Installer detects offline mode when network unavailable.
        SVC-001: Network timeout triggers offline mode.

        Given: Network connection times out after 2 seconds
        When: Installer performs pre-flight validation
        Then: Network status = "Offline - Air-gapped mode"
        """
        # Arrange
        from installer.install import check_network_availability

        # Mock socket timeout
        with patch('socket.create_connection') as mock_socket:
            mock_socket.side_effect = socket.timeout("Connection timed out")

            # Act
            is_online = check_network_availability(timeout=2)

            # Assert
            assert is_online is False

    def test_network_detection_timeout_within_2_seconds(self):
        """
        AC#5: Network detection completes within 2-second timeout.

        Given: Network check is initiated
        When: Timeout is set to 2 seconds
        Then: Detection completes in ≤ 2.1 seconds (allow 100ms tolerance)
        """
        # Arrange
        from installer.install import check_network_availability

        with patch('socket.create_connection') as mock_socket:
            # Simulate slow network (1.5 second delay)
            def slow_connect(*args, **kwargs):
                time.sleep(1.5)
                raise socket.timeout()

            mock_socket.side_effect = slow_connect

            # Act
            start_time = time.time()
            is_online = check_network_availability(timeout=2)
            elapsed = time.time() - start_time

            # Assert
            assert elapsed < 2.1  # 2s timeout + 100ms tolerance
            assert is_online is False

    def test_network_detection_displays_status_message(self, capsys):
        """
        AC#5: Installer displays network status to user.

        Given: Network detection completes
        When: Status is determined
        Then: Display "Online" or "Offline - Air-gapped mode"
        """
        # Arrange
        from installer.install import display_network_status

        # Act - Online
        display_network_status(is_online=True)
        captured_online = capsys.readouterr()

        # Act - Offline
        display_network_status(is_online=False)
        captured_offline = capsys.readouterr()

        # Assert
        assert "Online" in captured_online.out
        assert "Offline" in captured_offline.out
        assert "Air-gapped mode" in captured_offline.out


class TestNoExternalDownloads:
    """
    AC#2: No External Downloads During Installation
    SVC-002: No HTTP requests during offline install
    """

    def test_offline_install_makes_zero_http_requests(self):
        """
        AC#2: Offline installation makes zero HTTP/HTTPS requests.
        SVC-002: No HTTP requests during offline install.

        Given: Installer runs in offline mode
        When: Installation executes all phases
        Then: Zero HTTP/HTTPS requests made
        """
        # Arrange
        from installer.install import run_offline_installation

        http_request_count = 0

        # Mock all HTTP libraries
        with patch('urllib.request.urlopen') as mock_urllib, \
             patch('requests.get') as mock_requests_get, \
             patch('requests.post') as mock_requests_post:

            # Configure mocks to count calls
            mock_urllib.side_effect = lambda *args: http_request_count.__add__(1)
            mock_requests_get.side_effect = lambda *args: http_request_count.__add__(1)
            mock_requests_post.side_effect = lambda *args: http_request_count.__add__(1)

            # Act
            run_offline_installation(mode='offline')

            # Assert
            assert mock_urllib.call_count == 0, "urllib made HTTP requests"
            assert mock_requests_get.call_count == 0, "requests.get made HTTP calls"
            assert mock_requests_post.call_count == 0, "requests.post made HTTP calls"

    def test_offline_install_no_cdn_dependencies(self):
        """
        AC#2: No CDN dependencies during offline install.

        Given: Installer runs in offline mode
        When: Framework files are loaded
        Then: Zero CDN URLs accessed (jsdelivr, unpkg, cdnjs, etc.)
        """
        # Arrange
        from installer.install import run_offline_installation

        cdn_patterns = [
            'cdn.jsdelivr.net',
            'unpkg.com',
            'cdnjs.cloudflare.com',
            'cdn.skypack.dev'
        ]

        with patch('urllib.request.urlopen') as mock_urllib:
            # Act
            run_offline_installation(mode='offline')

            # Assert
            for call_args in mock_urllib.call_args_list:
                url = str(call_args[0][0]) if call_args[0] else ""
                for cdn in cdn_patterns:
                    assert cdn not in url, f"CDN dependency detected: {cdn}"

    def test_offline_install_no_github_api_calls(self):
        """
        AC#2: No GitHub API calls during offline install.

        Given: Installer runs in offline mode
        When: Installation executes
        Then: Zero requests to api.github.com
        """
        # Arrange
        from installer.install import run_offline_installation

        with patch('urllib.request.urlopen') as mock_urllib:
            # Act
            run_offline_installation(mode='offline')

            # Assert
            github_api_calls = [
                call_args for call_args in mock_urllib.call_args_list
                if 'api.github.com' in str(call_args[0][0])
            ]
            assert len(github_api_calls) == 0, "GitHub API calls detected"

    def test_offline_install_no_npm_registry_lookups(self):
        """
        AC#2: No NPM registry lookups during offline install.

        Given: Installer runs in offline mode
        When: Dependencies are resolved
        Then: Zero requests to registry.npmjs.org
        """
        # Arrange
        from installer.install import run_offline_installation

        with patch('urllib.request.urlopen') as mock_urllib:
            # Act
            run_offline_installation(mode='offline')

            # Assert
            npm_registry_calls = [
                call_args for call_args in mock_urllib.call_args_list
                if 'registry.npmjs.org' in str(call_args[0][0])
            ]
            assert len(npm_registry_calls) == 0, "NPM registry calls detected"


class TestBundleStructure:
    """
    AC#1: Complete Framework Bundle in NPM Package
    DM-001: Framework directories bundled
    """

    def test_bundled_claude_directory_exists(self, tmp_path):
        """
        AC#1, DM-001: .claude/ directory bundled in package.

        Given: NPM package extracted
        When: Installer checks bundle structure
        Then: bundled/claude/ directory exists
        """
        # Arrange
        from installer.install import verify_bundle_structure

        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Act & Assert (should fail - directory doesn't exist yet)
        with pytest.raises(FileNotFoundError, match="bundled/claude"):
            verify_bundle_structure(bundle_root)

    def test_bundled_devforgeai_directory_exists(self, tmp_path):
        """
        AC#1, DM-001: .devforgeai/ directory bundled in package.

        Given: NPM package extracted
        When: Installer checks bundle structure
        Then: bundled/devforgeai/ directory exists
        """
        # Arrange
        from installer.install import verify_bundle_structure

        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Act & Assert (should fail - directory doesn't exist yet)
        with pytest.raises(FileNotFoundError, match="bundled/devforgeai"):
            verify_bundle_structure(bundle_root)

    def test_bundle_contains_all_required_files(self, tmp_path):
        """
        AC#1: Bundle contains 200+ framework files.
        AC#6: File existence checks pass.

        Given: NPM package extracted
        When: Installer counts bundled files
        Then: File count ≥ 200 (framework complete)
        """
        # Arrange
        from installer.install import count_bundled_files

        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Act
        file_count = count_bundled_files(bundle_root)

        # Assert (should fail - no files bundled yet)
        assert file_count >= 200, f"Only {file_count} files bundled (expected ≥200)"

    def test_bundle_size_within_limits(self, tmp_path):
        """
        AC#1, DM-003: Compressed package ≤ 60MB, uncompressed ≤ 150MB.

        Given: NPM package created
        When: Package size is measured
        Then: Compressed ≤ 60MB, Uncompressed ≤ 150MB
        """
        # Arrange
        from installer.install import measure_bundle_size

        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Act
        sizes = measure_bundle_size(bundle_root)

        # Assert
        compressed_mb = sizes['compressed'] / (1024 * 1024)
        uncompressed_mb = sizes['uncompressed'] / (1024 * 1024)

        assert compressed_mb <= 60, f"Compressed size {compressed_mb:.1f}MB exceeds 60MB limit"
        assert uncompressed_mb <= 150, f"Uncompressed size {uncompressed_mb:.1f}MB exceeds 150MB limit"


class TestPythonCliBundled:
    """
    AC#3: Python CLI Bundled Installation
    DM-002: Python wheel files bundled
    """

    def test_python_wheel_files_bundled(self, tmp_path):
        """
        AC#3, DM-002: Python wheel files included in bundle.

        Given: NPM package extracted
        When: Installer checks for Python CLI wheels
        Then: bundled/python-cli/wheels/*.whl files exist
        """
        # Arrange
        from installer.install import find_bundled_wheels

        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Act
        wheel_files = find_bundled_wheels(bundle_root)

        # Assert (should fail - no wheel files exist yet)
        assert len(wheel_files) > 0, "No Python wheel files found in bundle"

    def test_python_cli_installs_from_local_wheels(self, tmp_path):
        """
        AC#3: Python CLI installs from bundled wheel files when Python 3.8+ available.

        Given: Python 3.8+ is available, bundled wheel files exist
        When: Installer runs Python CLI installation
        Then: pip install uses local wheel files (no network)
        """
        # Arrange
        from installer.install import install_python_cli_offline

        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        with patch('subprocess.run') as mock_subprocess:
            mock_subprocess.return_value = MagicMock(returncode=0)

            # Act
            install_python_cli_offline(bundle_root)

            # Assert
            # Should call pip install with --no-index --find-links bundled/python-cli/wheels/
            pip_call = mock_subprocess.call_args[0][0]
            assert '--no-index' in pip_call, "pip should use --no-index for offline install"
            assert '--find-links' in pip_call, "pip should use --find-links for local wheels"
            assert 'bundled/python-cli/wheels' in ' '.join(pip_call), "pip should use bundled wheels"

    def test_python_cli_installation_detects_python_version(self):
        """
        AC#3: Installer detects Python 3.8+ before attempting CLI install.

        Given: Installer runs
        When: Python version is checked
        Then: Python 3.8+ detection succeeds or gracefully fails
        """
        # Arrange
        from installer.install import detect_python_version

        # Act - Mock Python 3.10 available
        with patch('subprocess.run') as mock_subprocess:
            mock_subprocess.return_value = MagicMock(
                returncode=0,
                stdout="Python 3.10.11"
            )
            version = detect_python_version()

        # Assert
        assert version >= (3, 8), f"Python {version} below minimum 3.8"


class TestGracefulDegradation:
    """
    AC#4: Graceful Degradation for Optional Dependencies
    BR-002: Optional features degrade gracefully
    """

    def test_install_continues_without_python(self, capsys):
        """
        AC#4: Installation continues when Python unavailable.
        BR-002: Missing Python = warning, not error.

        Given: Python is not installed
        When: Installer runs
        Then:
        - Displays warning about skipped Python CLI
        - Completes with core framework files
        - Exit code = 0 (success)
        """
        # Arrange
        from installer.install import run_installation

        with patch('installer.install.detect_python_version') as mock_python:
            mock_python.return_value = None  # Python not available

            # Act
            exit_code = run_installation(mode='offline')
            captured = capsys.readouterr()

            # Assert
            assert "Python CLI skipped" in captured.out or "warning" in captured.out.lower()
            assert exit_code == 0, "Installation should succeed without Python"

    def test_install_creates_missing_features_note(self, tmp_path):
        """
        AC#4: Installer documents missing optional features.

        Given: Python unavailable
        When: Installation completes
        Then: Creates MISSING_FEATURES.md documenting optional features
        """
        # Arrange
        from installer.install import run_installation

        with patch('installer.install.detect_python_version') as mock_python:
            mock_python.return_value = None

            # Act
            run_installation(mode='offline', target_dir=tmp_path)

            # Assert
            missing_features_file = tmp_path / ".devforgeai" / "MISSING_FEATURES.md"
            assert missing_features_file.exists(), "MISSING_FEATURES.md not created"
            content = missing_features_file.read_text()
            assert "Python CLI" in content, "Missing features note incomplete"

    def test_graceful_degradation_clear_warning_message(self, capsys):
        """
        AC#4: Clear warning message when Python unavailable.

        Given: Python not installed
        When: Installer attempts Python CLI installation
        Then: Warning message includes:
        - Feature name: "Python CLI"
        - Impact: "CLI validation commands unavailable"
        - Mitigation: "Install Python 3.8+ and re-run"
        """
        # Arrange
        from installer.install import warn_missing_dependency

        # Act
        warn_missing_dependency('python', reason='Python 3.8+ not found')
        captured = capsys.readouterr()

        # Assert
        assert "Python CLI" in captured.out
        assert "unavailable" in captured.out.lower() or "skipped" in captured.out.lower()
        assert "Python 3.8+" in captured.out, "Missing mitigation guidance"


class TestOfflineModeValidation:
    """
    AC#6: Offline Mode Validation
    """

    def test_offline_validation_checks_200_files(self, tmp_path):
        """
        AC#6: Offline validation checks 200+ framework files exist.

        Given: Installation completed in offline mode
        When: Installer runs final verification
        Then: File existence checks validate ≥200 files present
        """
        # Arrange
        from installer.install import validate_offline_installation

        project_root = tmp_path / "project"
        project_root.mkdir()

        # Act
        validation_result = validate_offline_installation(project_root)

        # Assert
        assert validation_result['files_checked'] >= 200
        assert validation_result['files_present'] >= 200
        assert validation_result['success'] is True

    def test_offline_validation_git_initialization_no_remote(self, tmp_path):
        """
        AC#6: Git repository initialized without remote operations.

        Given: Installation completed offline
        When: Validation checks git repository
        Then:
        - git init completed
        - No remote configured (offline mode)
        - Working directory clean
        """
        # Arrange
        from installer.install import validate_git_initialization

        project_root = tmp_path / "project"
        project_root.mkdir()

        # Act
        git_status = validate_git_initialization(project_root)

        # Assert
        assert git_status['initialized'] is True, "Git not initialized"
        assert git_status['has_remote'] is False, "Remote configured in offline mode"
        assert git_status['clean_working_dir'] is True, "Working directory not clean"

    def test_offline_validation_claude_md_merge(self, tmp_path):
        """
        AC#6: CLAUDE.md merge validation using local resources only.

        Given: Installation completed offline
        When: Validation checks CLAUDE.md
        Then: Merge validation uses only local template (no downloads)
        """
        # Arrange
        from installer.install import validate_claude_md_merge

        project_root = tmp_path / "project"
        project_root.mkdir()

        with patch('urllib.request.urlopen') as mock_http:
            # Act
            merge_result = validate_claude_md_merge(project_root)

            # Assert
            assert mock_http.call_count == 0, "CLAUDE.md validation made HTTP requests"
            assert merge_result['success'] is True
            assert merge_result['used_local_template'] is True


class TestNetworkDependentFeatureErrors:
    """
    AC#7: Clear Error Messages for Network-Dependent Features
    """

    def test_network_feature_error_displays_feature_name(self, capsys):
        """
        AC#7: Error message includes feature name.

        Given: Network-dependent feature cannot run offline
        When: Installer displays error
        Then: Message includes feature name ("Update Check", "Template Download", etc.)
        """
        # Arrange
        from installer.install import warn_network_feature_unavailable

        # Act
        warn_network_feature_unavailable(
            feature_name="Update Check",
            reason="Requires GitHub API access"
        )
        captured = capsys.readouterr()

        # Assert
        assert "Update Check" in captured.out, "Feature name missing from error"

    def test_network_feature_error_explains_why_network_required(self, capsys):
        """
        AC#7: Error message explains why feature requires network.

        Given: Network-dependent feature skipped
        When: Error displayed
        Then: Message explains reason (e.g., "Requires GitHub API access")
        """
        # Arrange
        from installer.install import warn_network_feature_unavailable

        # Act
        warn_network_feature_unavailable(
            feature_name="Template Download",
            reason="Requires CDN access for latest templates"
        )
        captured = capsys.readouterr()

        # Assert
        assert "CDN access" in captured.out or "Requires" in captured.out

    def test_network_feature_error_shows_impact_of_skipping(self, capsys):
        """
        AC#7: Error message shows impact of skipping feature.

        Given: Optional network feature skipped
        When: Warning displayed
        Then: Impact documented (e.g., "You won't receive update notifications")
        """
        # Arrange
        from installer.install import warn_network_feature_unavailable

        # Act
        warn_network_feature_unavailable(
            feature_name="Update Check",
            reason="Requires network",
            impact="You won't receive update notifications"
        )
        captured = capsys.readouterr()

        # Assert
        assert "update notifications" in captured.out.lower() or "impact" in captured.out.lower()

    def test_network_feature_error_provides_enable_command(self, capsys):
        """
        AC#7: Error message provides command to enable later when online.

        Given: Network feature skipped
        When: Warning displayed
        Then: Message includes command (e.g., "devforgeai update --check")
        """
        # Arrange
        from installer.install import warn_network_feature_unavailable

        # Act
        warn_network_feature_unavailable(
            feature_name="Update Check",
            reason="Requires network",
            enable_command="devforgeai update --check"
        )
        captured = capsys.readouterr()

        # Assert
        assert "devforgeai update --check" in captured.out, "Enable command missing"

    def test_network_feature_error_does_not_halt_installation(self):
        """
        AC#7: Network feature errors do NOT halt installation.

        Given: Network-dependent feature fails
        When: Installer continues
        Then: Installation proceeds (exit code 0)
        """
        # Arrange
        from installer.install import run_installation

        with patch('installer.install.check_network_availability') as mock_network:
            mock_network.return_value = False

            # Act
            exit_code = run_installation(mode='offline')

            # Assert
            assert exit_code == 0, "Installation halted on network feature failure"


class TestBundleIntegrityVerification:
    """
    AC#8: Bundle Integrity Verification
    SVC-003: Checksum verification detects corrupted files
    CONF-001: All bundled files have checksums
    """

    def test_checksums_json_exists_in_bundle(self, tmp_path):
        """
        AC#8, CONF-001: bundled/checksums.json file exists.

        Given: NPM package extracted
        When: Installer checks bundle structure
        Then: bundled/checksums.json exists and is valid JSON
        """
        # Arrange
        from installer.install import load_checksums

        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Act & Assert (should fail - file doesn't exist yet)
        with pytest.raises(FileNotFoundError, match="checksums.json"):
            load_checksums(bundle_root)

    def test_all_bundled_files_have_checksum_entries(self, tmp_path):
        """
        AC#8, CONF-001: Every bundled file has SHA256 checksum entry.

        Given: Bundle contains 200+ files
        When: Installer loads checksums.json
        Then: Every file has corresponding checksum entry
        """
        # Arrange
        from installer.install import verify_all_files_have_checksums

        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Create mock checksums.json
        checksums_file = bundle_root / "checksums.json"
        checksums_file.write_text(json.dumps({
            "claude/agents/test.md": "abc123",
            "devforgeai/context/tech-stack.md": "def456"
        }))

        # Create actual files (more files than checksums)
        (bundle_root / "claude").mkdir()
        (bundle_root / "claude" / "agents").mkdir()
        (bundle_root / "claude" / "agents" / "test.md").write_text("content")
        (bundle_root / "claude" / "agents" / "missing_checksum.md").write_text("no checksum")

        # Act & Assert
        with pytest.raises(ValueError, match="Files missing checksums"):
            verify_all_files_have_checksums(bundle_root)

    def test_checksum_verification_calculates_sha256(self, tmp_path):
        """
        AC#8: Installer verifies SHA256 checksums for all files.

        Given: Checksums.json contains expected SHA256 hashes
        When: Installer verifies bundle integrity
        Then: Actual file SHA256 matches expected checksum
        """
        # Arrange
        from installer.install import verify_file_checksum

        test_file = tmp_path / "test.txt"
        content = "Test content for checksum"
        test_file.write_text(content)

        # Calculate expected SHA256
        expected_sha256 = hashlib.sha256(content.encode()).hexdigest()

        # Act
        is_valid = verify_file_checksum(test_file, expected_sha256)

        # Assert
        assert is_valid is True

    def test_checksum_mismatch_detected(self, tmp_path):
        """
        AC#8, SVC-003: Corrupted file detected via checksum mismatch.
        BR-003: Checksum mismatches block installation.

        Given: File content differs from expected checksum
        When: Installer verifies integrity
        Then: Mismatch reported, installation halted
        """
        # Arrange
        from installer.install import verify_bundle_integrity

        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Create file
        test_file = bundle_root / "test.txt"
        test_file.write_text("Original content")

        # Create checksums with DIFFERENT hash
        checksums = {
            "test.txt": "0000000000000000000000000000000000000000000000000000000000000000"  # Wrong hash
        }
        (bundle_root / "checksums.json").write_text(json.dumps(checksums))

        # Act & Assert
        with pytest.raises(ValueError, match="Checksum mismatch"):
            verify_bundle_integrity(bundle_root)

    def test_checksum_verification_reports_mismatches(self, capsys):
        """
        AC#8: Installer reports all checksum mismatches.

        Given: Multiple files with checksum mismatches
        When: Verification runs
        Then: Report lists all mismatched files
        """
        # Arrange
        from installer.install import verify_bundle_integrity

        bundle_root = Path("/fake/bundle")

        with patch('pathlib.Path.exists') as mock_exists, \
             patch('pathlib.Path.read_text') as mock_read:

            mock_exists.return_value = True
            mock_read.return_value = json.dumps({
                "file1.txt": "wrong_hash_1",
                "file2.txt": "wrong_hash_2"
            })

            # Act
            try:
                verify_bundle_integrity(bundle_root)
            except ValueError:
                pass

            captured = capsys.readouterr()

            # Assert
            assert "file1.txt" in captured.out or "Checksum mismatch" in captured.out
            assert "file2.txt" in captured.out or "2 mismatches" in captured.out


class TestPerformanceRequirements:
    """
    NFR-001: Installation performance targets
    """

    def test_offline_installation_time_under_60_seconds_hdd(self, tmp_path):
        """
        NFR-001: Offline installation completes in < 60 seconds on HDD.

        Given: Installer runs on HDD storage
        When: Full offline installation executes
        Then: Total time < 60 seconds
        """
        # Arrange
        from installer.install import run_offline_installation

        # Act
        start_time = time.time()
        run_offline_installation(mode='offline', target_dir=tmp_path)
        elapsed = time.time() - start_time

        # Assert
        assert elapsed < 60, f"Installation took {elapsed:.1f}s (expected <60s on HDD)"

    def test_offline_installation_time_under_30_seconds_ssd(self, tmp_path):
        """
        NFR-001: Offline installation completes in < 30 seconds on SSD.

        Given: Installer runs on SSD storage
        When: Full offline installation executes
        Then: Total time < 30 seconds (best case)
        """
        # Arrange
        from installer.install import run_offline_installation

        # Act
        start_time = time.time()
        run_offline_installation(mode='offline', target_dir=tmp_path)
        elapsed = time.time() - start_time

        # Assert
        # Note: This test may PASS on SSD, FAIL on HDD (storage-dependent)
        # CI/CD should run on SSD to validate best-case performance
        assert elapsed < 30, f"Installation took {elapsed:.1f}s (expected <30s on SSD)"


class TestSecurityRequirements:
    """
    NFR-003: Bundle integrity security
    """

    def test_sha256_checksum_validation_for_all_files(self, tmp_path):
        """
        NFR-003: SHA256 validation for all bundled files.

        Given: Bundle contains 200+ files
        When: Integrity check runs
        Then: All 200+ files validated with SHA256
        """
        # Arrange
        from installer.install import verify_bundle_integrity

        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Create 200 files with checksums
        checksums = {}
        for i in range(200):
            file_path = bundle_root / f"file_{i:03d}.txt"
            content = f"File {i} content"
            file_path.write_text(content)
            checksums[f"file_{i:03d}.txt"] = hashlib.sha256(content.encode()).hexdigest()

        (bundle_root / "checksums.json").write_text(json.dumps(checksums))

        # Act
        result = verify_bundle_integrity(bundle_root)

        # Assert
        assert result['files_verified'] >= 200
        assert result['all_valid'] is True

    def test_halt_on_3_checksum_failures(self, tmp_path):
        """
        NFR-003: Installation halts after 3 checksum failures (tamper detection).

        Given: Bundle has >3 corrupted files
        When: Verification detects 3rd failure
        Then: Installation halts immediately with tamper warning
        """
        # Arrange
        from installer.install import verify_bundle_integrity

        bundle_root = tmp_path / "bundled"
        bundle_root.mkdir()

        # Create 5 corrupted files
        checksums = {}
        for i in range(5):
            file_path = bundle_root / f"corrupted_{i}.txt"
            file_path.write_text(f"Corrupted content {i}")
            checksums[f"corrupted_{i}.txt"] = "0" * 64  # Wrong hash

        (bundle_root / "checksums.json").write_text(json.dumps(checksums))

        # Act & Assert
        with pytest.raises(ValueError, match="3 checksum failures|tamper"):
            verify_bundle_integrity(bundle_root)


class TestReliabilityRequirements:
    """
    NFR-004: Graceful degradation reliability
    """

    def test_core_install_succeeds_without_python(self, tmp_path):
        """
        NFR-004: Core installation succeeds even if Python unavailable.

        Given: Python not installed
        When: Installer runs
        Then: Core framework files installed successfully (exit code 0)
        """
        # Arrange
        from installer.install import run_installation

        with patch('installer.install.detect_python_version') as mock_python:
            mock_python.return_value = None

            # Act
            result = run_installation(mode='offline', target_dir=tmp_path)

            # Assert
            assert result['exit_code'] == 0
            assert (tmp_path / ".claude").exists()
            assert (tmp_path / ".devforgeai").exists()


class TestEdgeCases:
    """
    Edge cases from story specification
    """

    def test_partial_network_access_treated_as_offline(self):
        """
        Edge Case 1: Partial network access (corporate proxy) treated as offline.

        Given: Network connection exists but is restricted
        When: Installer detects partial connectivity
        Then: Installer uses offline mode (skips update checks)
        """
        # Arrange
        from installer.install import check_network_availability

        with patch('socket.create_connection') as mock_socket:
            # Simulate corporate proxy (connection succeeds but HTTP fails)
            mock_socket.return_value = MagicMock()

            with patch('urllib.request.urlopen') as mock_http:
                mock_http.side_effect = URLError("Proxy authentication required")

                # Act
                is_online = check_network_availability(timeout=2)

                # Assert
                assert is_online is False, "Partial network should be treated as offline"

    def test_disk_space_check_before_extraction(self, tmp_path):
        """
        Edge Case 4: Disk space insufficient - check before extraction.

        Given: Available disk space < 200MB
        When: Installer checks prerequisites
        Then: Installation halted with clear error (before extraction starts)
        """
        # Arrange
        from installer.install import check_disk_space

        # Act
        with patch('shutil.disk_usage') as mock_disk:
            # Simulate 100MB free (< 200MB required)
            mock_disk.return_value = MagicMock(free=100 * 1024 * 1024)

            # Assert
            with pytest.raises(RuntimeError, match="Insufficient disk space"):
                check_disk_space(tmp_path, required_mb=200)

    def test_git_not_installed_halts_with_clear_error(self):
        """
        Edge Case 5: Git not installed - halt with clear error.

        Given: Git is not available in PATH
        When: Installer checks prerequisites
        Then: Installation halted with error: "Git is required"
        """
        # Arrange
        from installer.install import check_git_available

        with patch('shutil.which') as mock_which:
            mock_which.return_value = None  # Git not found

            # Act & Assert
            with pytest.raises(RuntimeError, match="Git is required|Git not found"):
                check_git_available()
