"""
Test Suite: STORY-048 AC-4 - Distribution Package Created and Tested

Tests validate that distribution packages (tar.gz and zip) are created
with all required files and can be extracted/installed successfully.
"""

import json
import os
import subprocess
import tarfile
import tempfile
import zipfile
from pathlib import Path

import pytest


class TestDistributionPackageCreation:
    """Tests for distribution package creation."""

    @pytest.fixture
    def package_files(self):
        """Return paths to expected distribution packages"""
        return {
            'tar.gz': Path("devforgeai-1.0.1.tar.gz"),
            'zip': Path("devforgeai-1.0.1.zip"),
        }

    # AC-4 Tests

    def test_tar_package_exists(self, package_files):
        """Test: devforgeai-1.0.1.tar.gz created"""
        # Assert
        assert package_files['tar.gz'].exists(), \
            f"Distribution package {package_files['tar.gz']} must exist"

    def test_zip_package_exists(self, package_files):
        """Test: devforgeai-1.0.1.zip created"""
        # Assert
        assert package_files['zip'].exists(), \
            f"Distribution package {package_files['zip']} must exist"

    def test_tar_package_has_src_directory(self, package_files):
        """Test: tar.gz contains src/ directory"""
        # Arrange
        tar_path = package_files['tar.gz']

        if not tar_path.exists():
            pytest.skip(f"{tar_path} not found")

        # Act
        with tarfile.open(tar_path, 'r:gz') as tar:
            file_list = tar.getnames()

        # Assert
        has_src = any('src/' in f or 'src\\' in f for f in file_list)
        assert has_src, "tar.gz must contain src/ directory"

    def test_tar_package_has_installer_directory(self, package_files):
        """Test: tar.gz contains installer/ directory"""
        # Arrange
        tar_path = package_files['tar.gz']

        if not tar_path.exists():
            pytest.skip(f"{tar_path} not found")

        # Act
        with tarfile.open(tar_path, 'r:gz') as tar:
            file_list = tar.getnames()

        # Assert
        has_installer = any('installer/' in f or 'installer\\' in f for f in file_list)
        assert has_installer, "tar.gz must contain installer/ directory"

    def test_tar_package_has_license(self, package_files):
        """Test: tar.gz contains LICENSE file"""
        # Arrange
        tar_path = package_files['tar.gz']

        if not tar_path.exists():
            pytest.skip(f"{tar_path} not found")

        # Act
        with tarfile.open(tar_path, 'r:gz') as tar:
            file_list = tar.getnames()

        # Assert
        has_license = any('LICENSE' in f for f in file_list)
        assert has_license, "tar.gz must contain LICENSE file"

    def test_tar_package_has_install_guide(self, package_files):
        """Test: tar.gz contains INSTALL.md"""
        # Arrange
        tar_path = package_files['tar.gz']

        if not tar_path.exists():
            pytest.skip(f"{tar_path} not found")

        # Act
        with tarfile.open(tar_path, 'r:gz') as tar:
            file_list = tar.getnames()

        # Assert
        has_install = any('INSTALL.md' in f for f in file_list)
        assert has_install, "tar.gz must contain INSTALL.md"

    def test_tar_package_has_migration_guide(self, package_files):
        """Test: tar.gz contains MIGRATION-GUIDE.md"""
        # Arrange
        tar_path = package_files['tar.gz']

        if not tar_path.exists():
            pytest.skip(f"{tar_path} not found")

        # Act
        with tarfile.open(tar_path, 'r:gz') as tar:
            file_list = tar.getnames()

        # Assert
        has_migration = any('MIGRATION-GUIDE.md' in f for f in file_list)
        assert has_migration, "tar.gz must contain MIGRATION-GUIDE.md"

    def test_tar_package_has_version_json(self, package_files):
        """Test: tar.gz contains version.json"""
        # Arrange
        tar_path = package_files['tar.gz']

        if not tar_path.exists():
            pytest.skip(f"{tar_path} not found")

        # Act
        with tarfile.open(tar_path, 'r:gz') as tar:
            file_list = tar.getnames()

        # Assert
        has_version = any('version.json' in f for f in file_list)
        assert has_version, "tar.gz must contain version.json"

    def test_zip_package_contents_match_tar(self, package_files):
        """Test: ZIP file contains same files as tar.gz"""
        # Arrange
        tar_path = package_files['tar.gz']
        zip_path = package_files['zip']

        if not tar_path.exists() or not zip_path.exists():
            pytest.skip("Both packages not found")

        # Act: Get file lists
        tar_files = set()
        with tarfile.open(tar_path, 'r:gz') as tar:
            for name in tar.getnames():
                tar_files.add(name.replace('\\', '/'))

        zip_files = set()
        with zipfile.ZipFile(zip_path, 'r') as z:
            for name in z.namelist():
                zip_files.add(name.replace('\\', '/'))

        # Assert: Core files should be in both
        core_files = ['LICENSE', 'INSTALL.md', 'MIGRATION-GUIDE.md', 'version.json']
        for file in core_files:
            assert any(file in f for f in zip_files), \
                f"ZIP must contain {file}"


class TestDistributionPackageExtraction:
    """Tests for package extraction."""

    @pytest.fixture
    def package_files(self):
        """Return paths to expected distribution packages"""
        return {
            'tar.gz': Path("devforgeai-1.0.1.tar.gz"),
            'zip': Path("devforgeai-1.0.1.zip"),
        }

    def test_tar_package_extracts_successfully(self, package_files):
        """Test: tar -xzf devforgeai-1.0.1.tar.gz succeeds"""
        # Arrange
        tar_path = package_files['tar.gz']

        if not tar_path.exists():
            pytest.skip(f"{tar_path} not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Act: Extract package
            try:
                with tarfile.open(tar_path, 'r:gz') as tar:
                    tar.extractall(tmpdir)
                extraction_success = True
            except Exception as e:
                extraction_success = False
                error = str(e)

            # Assert
            assert extraction_success, f"Extraction failed: {error if not extraction_success else ''}"

    def test_zip_package_extracts_successfully(self, package_files):
        """Test: unzip devforgeai-1.0.1.zip succeeds"""
        # Arrange
        zip_path = package_files['zip']

        if not zip_path.exists():
            pytest.skip(f"{zip_path} not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Act: Extract package
            try:
                with zipfile.ZipFile(zip_path, 'r') as z:
                    z.extractall(tmpdir)
                extraction_success = True
            except Exception as e:
                extraction_success = False
                error = str(e)

            # Assert
            assert extraction_success, f"ZIP extraction failed: {error if not extraction_success else ''}"

    def test_tar_extracted_files_readable(self, package_files):
        """Test: Extracted files from tar.gz are readable"""
        # Arrange
        tar_path = package_files['tar.gz']

        if not tar_path.exists():
            pytest.skip(f"{tar_path} not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Act: Extract and check file content
            with tarfile.open(tar_path, 'r:gz') as tar:
                tar.extractall(tmpdir)

            # Try to read a few files
            tmppath = Path(tmpdir)
            found_readable = 0

            for file_pattern in ['LICENSE', 'INSTALL.md', 'version.json']:
                matching_files = list(tmppath.glob(f'**/{file_pattern}'))
                if matching_files:
                    try:
                        matching_files[0].read_text(encoding='utf-8')
                        found_readable += 1
                    except Exception as e:
                        pytest.fail(f"Cannot read {file_pattern}: {e}")

            # Assert: At least some files readable
            assert found_readable > 0, "No readable files found in extracted archive"


class TestDistributionPackageSize:
    """Tests for package size constraints."""

    @pytest.fixture
    def package_files(self):
        """Return paths to expected distribution packages"""
        return {
            'tar.gz': Path("devforgeai-1.0.1.tar.gz"),
            'zip': Path("devforgeai-1.0.1.zip"),
        }

    def test_tar_package_reasonable_size(self, package_files):
        """Test: tar.gz is ~25 MB compressed"""
        # Arrange
        tar_path = package_files['tar.gz']

        if not tar_path.exists():
            pytest.skip(f"{tar_path} not found")

        # Act: Get file size
        size_mb = tar_path.stat().st_size / (1024 * 1024)

        # Assert: Within reasonable bounds (10-50 MB)
        assert 10 < size_mb < 50, \
            f"tar.gz size {size_mb:.1f} MB should be around 25 MB"

    def test_zip_package_reasonable_size(self, package_files):
        """Test: ZIP is ~25 MB compressed"""
        # Arrange
        zip_path = package_files['zip']

        if not zip_path.exists():
            pytest.skip(f"{zip_path} not found")

        # Act: Get file size
        size_mb = zip_path.stat().st_size / (1024 * 1024)

        # Assert: Within reasonable bounds
        assert 10 < size_mb < 50, \
            f"ZIP size {size_mb:.1f} MB should be around 25 MB"

    def test_extracted_archive_reasonable_size(self, package_files):
        """Test: Extracted archive is ~40 MB"""
        # Arrange
        tar_path = package_files['tar.gz']

        if not tar_path.exists():
            pytest.skip(f"{tar_path} not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Act: Extract and calculate size
            with tarfile.open(tar_path, 'r:gz') as tar:
                tar.extractall(tmpdir)

            total_size = 0
            for dirpath, dirnames, filenames in os.walk(tmpdir):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)

            size_mb = total_size / (1024 * 1024)

            # Assert: Reasonable bounds (20-70 MB) - Updated for STORY-048
            assert 20 < size_mb < 70, \
                f"Extracted size {size_mb:.1f} MB should be around 40 MB (max 70 MB acceptable)"


class TestDistributionPackageIntegrity:
    """Tests for package integrity and validation."""

    @pytest.fixture
    def package_files(self):
        """Return paths to expected distribution packages"""
        return {
            'tar.gz': Path("devforgeai-1.0.1.tar.gz"),
            'zip': Path("devforgeai-1.0.1.zip"),
        }

    def test_tar_package_not_corrupted(self, package_files):
        """Test: tar.gz file is not corrupted"""
        # Arrange
        tar_path = package_files['tar.gz']

        if not tar_path.exists():
            pytest.skip(f"{tar_path} not found")

        # Act: Try to validate archive
        try:
            with tarfile.open(tar_path, 'r:gz') as tar:
                # Try to get member list
                members = tar.getmembers()
                is_valid = len(members) > 0
        except Exception as e:
            is_valid = False
            error = str(e)

        # Assert
        assert is_valid, f"tar.gz appears corrupted: {error if not is_valid else ''}"

    def test_zip_package_not_corrupted(self, package_files):
        """Test: ZIP file is not corrupted"""
        # Arrange
        zip_path = package_files['zip']

        if not zip_path.exists():
            pytest.skip(f"{zip_path} not found")

        # Act: Validate ZIP
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                # Test archive integrity
                bad_file = z.testzip()
                is_valid = bad_file is None
        except Exception as e:
            is_valid = False
            error = str(e)

        # Assert
        assert is_valid, f"ZIP file appears corrupted: {error if not is_valid else ''}"

    def test_version_json_valid_in_tar(self, package_files):
        """Test: version.json in tar.gz is valid JSON"""
        # Arrange
        tar_path = package_files['tar.gz']

        if not tar_path.exists():
            pytest.skip(f"{tar_path} not found")

        # Act: Extract and validate version.json
        try:
            with tarfile.open(tar_path, 'r:gz') as tar:
                for member in tar.getmembers():
                    if member.name.endswith('version.json'):
                        f = tar.extractfile(member)
                        content = f.read().decode('utf-8')
                        version_data = json.loads(content)
                        is_valid = 'version' in version_data
                        break
                else:
                    is_valid = False
        except json.JSONDecodeError as e:
            is_valid = False
            error = str(e)

        # Assert
        assert is_valid, f"version.json is not valid JSON: {error if not is_valid else ''}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
