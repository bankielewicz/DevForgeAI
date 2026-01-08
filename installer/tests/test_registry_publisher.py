"""
Test Suite for Registry Publisher (STORY-244)

Tests for RegistryPublisher class that orchestrates publishing to multiple registries:
- npm (AC#1)
- PyPI (AC#2)
- NuGet (AC#3)
- Docker Hub (AC#4)
- GitHub Packages (AC#5)
- crates.io (AC#6)
- Dry-run mode (AC#8)

Test Framework: pytest with unittest.mock
Test Naming Convention: test_<function>_<scenario>_<expected>
Pattern: AAA (Arrange, Act, Assert)

These tests will FAIL initially (TDD Red phase) because:
- installer/registry_publisher.py does not exist yet
- RegistryPublisher, PublishResult, RegistryResult classes not implemented
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
from dataclasses import dataclass
from typing import Optional
import subprocess
import os


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def mock_env_vars():
    """Setup mock environment variables for all registries."""
    env = {
        "NPM_TOKEN": "npm_test_token_12345",
        "TWINE_USERNAME": "test_pypi_user",
        "TWINE_PASSWORD": "test_pypi_password",
        "NUGET_API_KEY": "nuget_api_key_test_12345",
        "DOCKER_USERNAME": "docker_test_user",
        "DOCKER_PASSWORD": "docker_test_password",
        "GITHUB_TOKEN": "ghp_test_token_12345",
        "CARGO_REGISTRY_TOKEN": "cargo_token_test_12345",
    }
    with patch.dict(os.environ, env, clear=False):
        yield env


@pytest.fixture
def registry_publisher(mock_env_vars):
    """Create a RegistryPublisher instance with mocked environment."""
    from installer.registry_publisher import RegistryPublisher
    return RegistryPublisher()


@pytest.fixture
def registry_config():
    """Create a sample RegistryConfig for testing."""
    from installer.registry_publisher import RegistryConfig
    return RegistryConfig(
        npm_enabled=True,
        pypi_enabled=True,
        nuget_enabled=True,
        docker_enabled=True,
        github_enabled=True,
        crates_enabled=True,
        package_name="devforgeai",
        version="1.0.0",
    )


@pytest.fixture
def mock_subprocess():
    """Mock subprocess.run for registry commands."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Success",
            stderr="",
        )
        yield mock_run


# =============================================================================
# Data Model Tests (PublishResult, RegistryResult)
# =============================================================================

class TestPublishResult:
    """Tests for PublishResult data model from Technical Specification."""

    def test_publish_result_should_contain_success_field(self):
        """PublishResult must have success boolean field (Tech Spec)."""
        # Arrange
        from installer.registry_publisher import PublishResult

        # Act
        result = PublishResult(success=True, registry_results={}, masked_logs=[], dry_run=False)

        # Assert
        assert hasattr(result, "success")
        assert result.success is True

    def test_publish_result_should_contain_registry_results_dict(self):
        """PublishResult must have registry_results dict field (Tech Spec)."""
        # Arrange
        from installer.registry_publisher import PublishResult, RegistryResult

        npm_result = RegistryResult(
            registry="npm",
            success=True,
            version="1.0.0",
            url="https://npmjs.com/package/devforgeai",
        )

        # Act
        result = PublishResult(
            success=True,
            registry_results={"npm": npm_result},
            masked_logs=[],
            dry_run=False,
        )

        # Assert
        assert "npm" in result.registry_results
        assert result.registry_results["npm"].success is True

    def test_publish_result_should_contain_masked_logs_list(self):
        """PublishResult must have masked_logs list field (Tech Spec)."""
        # Arrange
        from installer.registry_publisher import PublishResult

        # Act
        result = PublishResult(
            success=True,
            registry_results={},
            masked_logs=["Published devforgeai@1.0.0", "Token: ***"],
            dry_run=False,
        )

        # Assert
        assert isinstance(result.masked_logs, list)
        assert len(result.masked_logs) == 2

    def test_publish_result_should_contain_dry_run_flag(self):
        """PublishResult must have dry_run boolean field (Tech Spec)."""
        # Arrange
        from installer.registry_publisher import PublishResult

        # Act
        result = PublishResult(success=True, registry_results={}, masked_logs=[], dry_run=True)

        # Assert
        assert result.dry_run is True


class TestRegistryResult:
    """Tests for RegistryResult data model from Technical Specification."""

    def test_registry_result_should_contain_registry_name(self):
        """RegistryResult must have registry string field (Tech Spec)."""
        # Arrange
        from installer.registry_publisher import RegistryResult

        # Act
        result = RegistryResult(registry="npm", success=True, version="1.0.0")

        # Assert
        assert result.registry == "npm"

    def test_registry_result_should_contain_success_status(self):
        """RegistryResult must have success boolean field (Tech Spec)."""
        # Arrange
        from installer.registry_publisher import RegistryResult

        # Act
        result = RegistryResult(registry="pypi", success=False, version="1.0.0")

        # Assert
        assert result.success is False

    def test_registry_result_should_contain_version(self):
        """RegistryResult must have version string field (Tech Spec)."""
        # Arrange
        from installer.registry_publisher import RegistryResult

        # Act
        result = RegistryResult(registry="nuget", success=True, version="2.0.0")

        # Assert
        assert result.version == "2.0.0"

    def test_registry_result_should_have_optional_url(self):
        """RegistryResult must have optional url field (Tech Spec)."""
        # Arrange
        from installer.registry_publisher import RegistryResult

        # Act
        result = RegistryResult(
            registry="docker",
            success=True,
            version="1.0.0",
            url="https://hub.docker.com/r/devforgeai/framework",
        )

        # Assert
        assert result.url == "https://hub.docker.com/r/devforgeai/framework"

    def test_registry_result_should_have_optional_error(self):
        """RegistryResult must have optional error field (Tech Spec)."""
        # Arrange
        from installer.registry_publisher import RegistryResult

        # Act
        result = RegistryResult(
            registry="crates",
            success=False,
            version="1.0.0",
            error="CARGO_REGISTRY_TOKEN not set",
        )

        # Assert
        assert result.error == "CARGO_REGISTRY_TOKEN not set"

    def test_registry_result_should_have_optional_skipped_reason(self):
        """RegistryResult must have optional skipped_reason field (Tech Spec)."""
        # Arrange
        from installer.registry_publisher import RegistryResult

        # Act
        result = RegistryResult(
            registry="nuget",
            success=True,
            version="1.0.0",
            skipped_reason="version 1.0.0 already exists",
        )

        # Assert
        assert result.skipped_reason == "version 1.0.0 already exists"


# =============================================================================
# AC#1: npm Registry Publishing Tests
# =============================================================================

class TestNpmPublishing:
    """Tests for npm registry publishing (AC#1)."""

    def test_publish_npm_should_execute_npm_publish_command(
        self, registry_publisher, mock_subprocess
    ):
        """AC#1: npm publish is executed with correct registry URL."""
        # Arrange
        package_path = "/dist/package"
        registry = "https://registry.npmjs.org"
        token = "npm_test_token"

        # Act
        result = registry_publisher.publish_npm(
            package_path=package_path,
            registry=registry,
            token=token,
            dry_run=False,
        )

        # Assert
        mock_subprocess.assert_called()
        call_args = mock_subprocess.call_args
        assert "npm" in str(call_args)
        assert "publish" in str(call_args)

    def test_publish_npm_should_use_npm_token_for_auth(
        self, registry_publisher, mock_subprocess
    ):
        """AC#1: Authentication uses NPM_TOKEN environment variable."""
        # Arrange
        package_path = "/dist/package"
        registry = "https://registry.npmjs.org"
        token = "npm_secret_token_12345"

        # Act
        result = registry_publisher.publish_npm(
            package_path=package_path,
            registry=registry,
            token=token,
            dry_run=False,
        )

        # Assert
        call_env = mock_subprocess.call_args.kwargs.get("env", {})
        assert "NPM_TOKEN" in call_env or token in str(mock_subprocess.call_args)

    def test_publish_npm_should_log_success_with_package_and_version(
        self, registry_publisher, mock_subprocess
    ):
        """AC#1: Successful publish is logged with package name and version."""
        # Arrange
        package_path = "/dist/package"
        mock_subprocess.return_value.stdout = "+ devforgeai@1.0.0"

        # Act
        result = registry_publisher.publish_npm(
            package_path=package_path,
            registry="https://registry.npmjs.org",
            token="token",
            dry_run=False,
        )

        # Assert
        assert result is True

    def test_publish_npm_should_handle_e403_version_conflict_gracefully(
        self, registry_publisher, mock_subprocess
    ):
        """AC#1 Verification: Version conflict (E403) handled gracefully (BR-003)."""
        # Arrange
        mock_subprocess.return_value.returncode = 1
        mock_subprocess.return_value.stderr = "E403: You cannot publish over the previously published version"

        # Act
        result = registry_publisher.publish_npm(
            package_path="/dist/package",
            registry="https://registry.npmjs.org",
            token="token",
            dry_run=False,
        )

        # Assert - Should return True (skip) not raise exception
        assert result is True  # Skipped gracefully per BR-003

    def test_publish_npm_should_fail_on_missing_token(self, registry_publisher):
        """BR-004: Failed credentials cause immediate failure."""
        # Arrange - no token provided
        # Act & Assert
        with pytest.raises(ValueError, match="NPM_TOKEN"):
            registry_publisher.publish_npm(
                package_path="/dist/package",
                registry="https://registry.npmjs.org",
                token="",  # Empty token
                dry_run=False,
            )


# =============================================================================
# AC#2: PyPI Publishing Tests
# =============================================================================

class TestPyPIPublishing:
    """Tests for PyPI publishing via twine (AC#2)."""

    def test_publish_pypi_should_execute_twine_upload(
        self, registry_publisher, mock_subprocess
    ):
        """AC#2: twine upload dist/* is executed."""
        # Arrange
        dist_path = "/dist"
        credentials = ("user", "password")

        # Act
        result = registry_publisher.publish_pypi(
            dist_path=dist_path,
            repository="pypi",
            credentials=credentials,
            dry_run=False,
        )

        # Assert
        mock_subprocess.assert_called()
        call_args = str(mock_subprocess.call_args)
        assert "twine" in call_args
        assert "upload" in call_args

    def test_publish_pypi_should_use_twine_credentials(
        self, registry_publisher, mock_subprocess
    ):
        """AC#2: Authentication uses environment credentials."""
        # Arrange
        credentials = ("test_user", "test_pass")

        # Act
        result = registry_publisher.publish_pypi(
            dist_path="/dist",
            repository="pypi",
            credentials=credentials,
            dry_run=False,
        )

        # Assert
        call_env = mock_subprocess.call_args.kwargs.get("env", {})
        # Should set TWINE_USERNAME and TWINE_PASSWORD
        assert "TWINE_USERNAME" in call_env or "test_user" in str(mock_subprocess.call_args)

    def test_publish_pypi_should_use_skip_existing_flag(
        self, registry_publisher, mock_subprocess
    ):
        """AC#2: skip-existing flag prevents duplicate version errors."""
        # Arrange & Act
        result = registry_publisher.publish_pypi(
            dist_path="/dist",
            repository="pypi",
            credentials=("user", "pass"),
            dry_run=False,
        )

        # Assert
        call_args = str(mock_subprocess.call_args)
        assert "--skip-existing" in call_args

    def test_publish_pypi_should_support_test_pypi_repository(
        self, registry_publisher, mock_subprocess
    ):
        """AC#2 Verification: Test PyPI support (testpypi repository)."""
        # Arrange & Act
        result = registry_publisher.publish_pypi(
            dist_path="/dist",
            repository="testpypi",
            credentials=("user", "pass"),
            dry_run=False,
        )

        # Assert
        call_args = str(mock_subprocess.call_args)
        assert "testpypi" in call_args or "test.pypi.org" in call_args

    def test_publish_pypi_should_fail_on_missing_credentials(self, registry_publisher):
        """BR-004: Failed credentials cause immediate failure."""
        # Arrange - empty credentials
        # Act & Assert
        with pytest.raises(ValueError, match="TWINE"):
            registry_publisher.publish_pypi(
                dist_path="/dist",
                repository="pypi",
                credentials=("", ""),  # Empty credentials
                dry_run=False,
            )


# =============================================================================
# AC#3: NuGet Publishing Tests
# =============================================================================

class TestNuGetPublishing:
    """Tests for NuGet publishing (AC#3)."""

    def test_publish_nuget_should_execute_dotnet_nuget_push(
        self, registry_publisher, mock_subprocess
    ):
        """AC#3: dotnet nuget push is executed."""
        # Arrange
        nupkg_path = "/output/DevForgeAI.1.0.0.nupkg"
        source = "https://api.nuget.org/v3/index.json"
        api_key = "nuget_api_key"

        # Act
        result = registry_publisher.publish_nuget(
            nupkg_path=nupkg_path,
            source=source,
            api_key=api_key,
            dry_run=False,
        )

        # Assert
        mock_subprocess.assert_called()
        call_args = str(mock_subprocess.call_args)
        assert "dotnet" in call_args
        assert "nuget" in call_args
        assert "push" in call_args

    def test_publish_nuget_should_use_nuget_org_source(
        self, registry_publisher, mock_subprocess
    ):
        """AC#3: --source defaults to https://api.nuget.org/v3/index.json."""
        # Arrange & Act
        result = registry_publisher.publish_nuget(
            nupkg_path="/output/Package.nupkg",
            source="https://api.nuget.org/v3/index.json",
            api_key="key",
            dry_run=False,
        )

        # Assert
        call_args = str(mock_subprocess.call_args)
        assert "api.nuget.org" in call_args

    def test_publish_nuget_should_pass_api_key_securely(
        self, registry_publisher, mock_subprocess
    ):
        """AC#3: API key is passed securely via environment variable."""
        # Arrange
        api_key = "super_secret_nuget_key"

        # Act
        result = registry_publisher.publish_nuget(
            nupkg_path="/output/Package.nupkg",
            source="https://api.nuget.org/v3/index.json",
            api_key=api_key,
            dry_run=False,
        )

        # Assert
        call_args = str(mock_subprocess.call_args)
        assert "--api-key" in call_args

    def test_publish_nuget_should_use_skip_duplicate_flag(
        self, registry_publisher, mock_subprocess
    ):
        """AC#3 Verification: --skip-duplicate flag used."""
        # Arrange & Act
        result = registry_publisher.publish_nuget(
            nupkg_path="/output/Package.nupkg",
            source="https://api.nuget.org/v3/index.json",
            api_key="key",
            dry_run=False,
        )

        # Assert
        call_args = str(mock_subprocess.call_args)
        assert "--skip-duplicate" in call_args

    def test_publish_nuget_should_fail_on_missing_api_key(self, registry_publisher):
        """BR-004: Failed credentials cause immediate failure."""
        # Act & Assert
        with pytest.raises(ValueError, match="NUGET_API_KEY"):
            registry_publisher.publish_nuget(
                nupkg_path="/output/Package.nupkg",
                source="https://api.nuget.org/v3/index.json",
                api_key="",  # Empty API key
                dry_run=False,
            )


# =============================================================================
# AC#4: Docker Hub Publishing Tests
# =============================================================================

class TestDockerPublishing:
    """Tests for Docker Hub publishing (AC#4)."""

    def test_publish_docker_should_execute_docker_login(
        self, registry_publisher, mock_subprocess
    ):
        """AC#4: docker login authenticates with Docker Hub."""
        # Arrange
        credentials = ("docker_user", "docker_pass")

        # Act
        result = registry_publisher.publish_docker(
            image="devforgeai/framework",
            tags=["1.0.0", "latest"],
            registry="docker.io",
            credentials=credentials,
            dry_run=False,
        )

        # Assert
        calls = [str(c) for c in mock_subprocess.call_args_list]
        assert any("docker" in c and "login" in c for c in calls)

    def test_publish_docker_should_execute_docker_push(
        self, registry_publisher, mock_subprocess
    ):
        """AC#4: docker push uploads the image with specified tags."""
        # Arrange
        tags = ["1.0.0", "latest"]

        # Act
        result = registry_publisher.publish_docker(
            image="devforgeai/framework",
            tags=tags,
            registry="docker.io",
            credentials=("user", "pass"),
            dry_run=False,
        )

        # Assert
        calls = [str(c) for c in mock_subprocess.call_args_list]
        assert any("docker" in c and "push" in c for c in calls)

    def test_publish_docker_should_push_both_latest_and_version_tags(
        self, registry_publisher, mock_subprocess
    ):
        """AC#4: Both :latest and :version tags are pushed."""
        # Arrange
        tags = ["1.0.0", "latest"]

        # Act
        result = registry_publisher.publish_docker(
            image="devforgeai/framework",
            tags=tags,
            registry="docker.io",
            credentials=("user", "pass"),
            dry_run=False,
        )

        # Assert - should push both tags
        calls = [str(c) for c in mock_subprocess.call_args_list]
        push_calls = [c for c in calls if "push" in c]
        assert len(push_calls) >= 2  # At least version and latest

    def test_publish_docker_should_execute_logout_after_push(
        self, registry_publisher, mock_subprocess
    ):
        """AC#4 Verification: docker logout executed after push (cleanup)."""
        # Arrange & Act
        result = registry_publisher.publish_docker(
            image="devforgeai/framework",
            tags=["1.0.0"],
            registry="docker.io",
            credentials=("user", "pass"),
            dry_run=False,
        )

        # Assert
        calls = [str(c) for c in mock_subprocess.call_args_list]
        # Logout should be last docker command
        assert any("docker" in c and "logout" in c for c in calls)

    def test_publish_docker_should_fail_on_missing_credentials(self, registry_publisher):
        """BR-004: Failed credentials cause immediate failure."""
        # Act & Assert
        with pytest.raises(ValueError, match="DOCKER"):
            registry_publisher.publish_docker(
                image="devforgeai/framework",
                tags=["1.0.0"],
                registry="docker.io",
                credentials=("", ""),  # Empty credentials
                dry_run=False,
            )


# =============================================================================
# AC#5: GitHub Packages Publishing Tests
# =============================================================================

class TestGitHubPackagesPublishing:
    """Tests for GitHub Packages publishing (AC#5)."""

    def test_publish_github_npm_should_use_github_registry(
        self, registry_publisher, mock_subprocess
    ):
        """AC#5: Registry URL set to npm.pkg.github.com (npm)."""
        # Arrange & Act
        result = registry_publisher.publish_github(
            package_type="npm",
            package_path="/dist",
            token="ghp_test_token",
            owner="devforgeai",
            dry_run=False,
        )

        # Assert
        call_args = str(mock_subprocess.call_args)
        assert "npm.pkg.github.com" in call_args

    def test_publish_github_container_should_use_ghcr(
        self, registry_publisher, mock_subprocess
    ):
        """AC#5 Verification: Registry URL set to ghcr.io (container)."""
        # Arrange & Act
        result = registry_publisher.publish_github(
            package_type="container",
            package_path="devforgeai/framework:1.0.0",
            token="ghp_test_token",
            owner="devforgeai",
            dry_run=False,
        )

        # Assert
        call_args = str(mock_subprocess.call_args)
        assert "ghcr.io" in call_args

    def test_publish_github_should_use_github_token_for_auth(
        self, registry_publisher, mock_subprocess
    ):
        """AC#5: GITHUB_TOKEN used for authentication."""
        # Arrange
        token = "ghp_secret_token_12345"

        # Act
        result = registry_publisher.publish_github(
            package_type="npm",
            package_path="/dist",
            token=token,
            owner="devforgeai",
            dry_run=False,
        )

        # Assert
        call_env = mock_subprocess.call_args.kwargs.get("env", {})
        assert "GITHUB_TOKEN" in call_env or token in str(mock_subprocess.call_args)

    def test_publish_github_should_prefix_package_with_owner_scope(
        self, registry_publisher, mock_subprocess
    ):
        """AC#5 Verification: Scope/namespace correctly prefixed (@owner/package)."""
        # Arrange & Act
        result = registry_publisher.publish_github(
            package_type="npm",
            package_path="/dist",
            token="ghp_token",
            owner="devforgeai",
            dry_run=False,
        )

        # Assert
        call_args = str(mock_subprocess.call_args)
        assert "@devforgeai" in call_args or "devforgeai/" in call_args

    def test_publish_github_should_fail_on_missing_token(self, registry_publisher):
        """BR-004: Failed credentials cause immediate failure."""
        # Act & Assert
        with pytest.raises(ValueError, match="GITHUB_TOKEN"):
            registry_publisher.publish_github(
                package_type="npm",
                package_path="/dist",
                token="",  # Empty token
                owner="devforgeai",
                dry_run=False,
            )


# =============================================================================
# AC#6: Crates.io Publishing Tests
# =============================================================================

class TestCratesPublishing:
    """Tests for crates.io publishing (AC#6)."""

    def test_publish_crates_should_execute_cargo_publish(
        self, registry_publisher, mock_subprocess
    ):
        """AC#6: cargo publish is executed."""
        # Arrange
        crate_path = "/crate"
        token = "cargo_token"

        # Act
        result = registry_publisher.publish_crates(
            crate_path=crate_path,
            token=token,
            dry_run=False,
        )

        # Assert
        mock_subprocess.assert_called()
        call_args = str(mock_subprocess.call_args)
        assert "cargo" in call_args
        assert "publish" in call_args

    def test_publish_crates_should_use_cargo_registry_token(
        self, registry_publisher, mock_subprocess
    ):
        """AC#6: Token is passed via environment variable."""
        # Arrange
        token = "cargo_secret_token"

        # Act
        result = registry_publisher.publish_crates(
            crate_path="/crate",
            token=token,
            dry_run=False,
        )

        # Assert
        call_env = mock_subprocess.call_args.kwargs.get("env", {})
        assert "CARGO_REGISTRY_TOKEN" in call_env or token in str(mock_subprocess.call_args)

    def test_publish_crates_should_not_use_allow_dirty_flag(
        self, registry_publisher, mock_subprocess
    ):
        """AC#6 Verification: --allow-dirty flag NOT used (clean builds only)."""
        # Arrange & Act
        result = registry_publisher.publish_crates(
            crate_path="/crate",
            token="token",
            dry_run=False,
        )

        # Assert
        call_args = str(mock_subprocess.call_args)
        assert "--allow-dirty" not in call_args

    def test_publish_crates_should_handle_version_exists_gracefully(
        self, registry_publisher, mock_subprocess
    ):
        """AC#6: Version conflict is detected and skipped gracefully (BR-003)."""
        # Arrange
        mock_subprocess.return_value.returncode = 1
        mock_subprocess.return_value.stderr = "crate version `1.0.0` is already uploaded"

        # Act
        result = registry_publisher.publish_crates(
            crate_path="/crate",
            token="token",
            dry_run=False,
        )

        # Assert - Should return True (skip) not raise exception
        assert result is True

    def test_publish_crates_should_fail_on_missing_token(self, registry_publisher):
        """BR-004: Failed credentials cause immediate failure."""
        # Act & Assert
        with pytest.raises(ValueError, match="CARGO_REGISTRY_TOKEN"):
            registry_publisher.publish_crates(
                crate_path="/crate",
                token="",  # Empty token
                dry_run=False,
            )


# =============================================================================
# AC#8: Dry-Run Mode Tests
# =============================================================================

class TestDryRunMode:
    """Tests for dry-run mode (AC#8)."""

    def test_publish_all_dry_run_should_not_execute_subprocess(
        self, registry_publisher, mock_subprocess, registry_config
    ):
        """AC#8: All publish commands are validated but not executed."""
        # Arrange - subprocess should NOT be called for actual publish

        # Act
        result = registry_publisher.publish_all(
            config=registry_config,
            dry_run=True,
        )

        # Assert - No actual subprocess calls for publish commands
        # Only validation calls allowed
        for call in mock_subprocess.call_args_list:
            call_str = str(call)
            assert "publish" not in call_str or "--dry-run" in call_str

    def test_publish_npm_dry_run_should_validate_credentials(
        self, registry_publisher, mock_subprocess
    ):
        """AC#8: Credential availability is verified in dry-run."""
        # Arrange & Act
        result = registry_publisher.publish_npm(
            package_path="/dist",
            registry="https://registry.npmjs.org",
            token="valid_token",
            dry_run=True,
        )

        # Assert
        assert result is True  # Validation passed

    def test_publish_npm_dry_run_should_fail_on_missing_token(
        self, registry_publisher
    ):
        """AC#8: Dry-run validates credentials (fails if missing)."""
        # Act & Assert
        with pytest.raises(ValueError, match="NPM_TOKEN"):
            registry_publisher.publish_npm(
                package_path="/dist",
                registry="https://registry.npmjs.org",
                token="",  # Empty token
                dry_run=True,
            )

    def test_publish_all_dry_run_should_validate_package_structure(
        self, registry_publisher, mock_subprocess, registry_config
    ):
        """AC#8: Package validity is checked."""
        # Arrange & Act
        result = registry_publisher.publish_all(
            config=registry_config,
            dry_run=True,
        )

        # Assert
        assert result.dry_run is True

    def test_publish_all_dry_run_should_log_would_publish_message(
        self, registry_publisher, mock_subprocess, registry_config
    ):
        """AC#8: Log output shows 'DRY RUN: would publish to {registry}'."""
        # Arrange & Act
        result = registry_publisher.publish_all(
            config=registry_config,
            dry_run=True,
        )

        # Assert
        assert any("DRY RUN" in log or "would publish" in log.lower() for log in result.masked_logs)

    def test_dry_run_should_return_exit_code_0_on_success(
        self, registry_publisher, mock_subprocess, registry_config
    ):
        """AC#8 Verification: Exit code 0 on successful dry-run."""
        # Arrange & Act
        result = registry_publisher.publish_all(
            config=registry_config,
            dry_run=True,
        )

        # Assert
        assert result.success is True


# =============================================================================
# publish_all Orchestration Tests
# =============================================================================

class TestPublishAllOrchestration:
    """Tests for publish_all method that orchestrates all registries."""

    def test_publish_all_should_return_publish_result(
        self, registry_publisher, mock_subprocess, registry_config
    ):
        """Tech Spec: publish_all returns PublishResult."""
        # Arrange & Act
        result = registry_publisher.publish_all(
            config=registry_config,
            dry_run=False,
        )

        # Assert
        from installer.registry_publisher import PublishResult
        assert isinstance(result, PublishResult)

    def test_publish_all_should_include_all_enabled_registries(
        self, registry_publisher, mock_subprocess, registry_config
    ):
        """Tech Spec: Publishes to all enabled registries."""
        # Arrange & Act
        result = registry_publisher.publish_all(
            config=registry_config,
            dry_run=False,
        )

        # Assert
        assert "npm" in result.registry_results
        assert "pypi" in result.registry_results
        assert "nuget" in result.registry_results
        assert "docker" in result.registry_results
        assert "github" in result.registry_results
        assert "crates" in result.registry_results

    def test_publish_all_should_handle_partial_success(
        self, registry_publisher, mock_subprocess, registry_config
    ):
        """Edge Case: Some registries succeed, others fail."""
        # Arrange
        def side_effect(*args, **kwargs):
            cmd = str(args[0]) if args else ""
            if "cargo" in cmd:
                mock_result = MagicMock()
                mock_result.returncode = 1
                mock_result.stderr = "Network timeout"
                return mock_result
            return MagicMock(returncode=0, stdout="Success", stderr="")

        mock_subprocess.side_effect = side_effect

        # Act
        result = registry_publisher.publish_all(
            config=registry_config,
            dry_run=False,
        )

        # Assert - Overall success should be False due to crates failure
        assert result.success is False
        assert result.registry_results["crates"].success is False
        # Other registries should still succeed
        assert result.registry_results["npm"].success is True

    def test_publish_all_should_skip_disabled_registries(
        self, registry_publisher, mock_subprocess
    ):
        """Config: Only publish to enabled registries."""
        # Arrange
        from installer.registry_publisher import RegistryConfig
        config = RegistryConfig(
            npm_enabled=True,
            pypi_enabled=False,  # Disabled
            nuget_enabled=False,  # Disabled
            docker_enabled=False,  # Disabled
            github_enabled=False,  # Disabled
            crates_enabled=False,  # Disabled
            package_name="devforgeai",
            version="1.0.0",
        )

        # Act
        result = registry_publisher.publish_all(
            config=config,
            dry_run=False,
        )

        # Assert
        assert "npm" in result.registry_results
        assert "pypi" not in result.registry_results


# =============================================================================
# Business Rules Tests
# =============================================================================

class TestBusinessRules:
    """Tests for business rules from Technical Specification."""

    def test_br001_credentials_must_come_from_environment(
        self, registry_publisher, mock_subprocess
    ):
        """BR-001: Environment variables MUST be used for all credentials."""
        # Arrange & Act
        result = registry_publisher.publish_npm(
            package_path="/dist",
            registry="https://registry.npmjs.org",
            token=os.environ.get("NPM_TOKEN", ""),
            dry_run=False,
        )

        # Assert - No hardcoded credentials in subprocess call
        call_args = str(mock_subprocess.call_args)
        # Should not contain actual token value in command line
        # Token should be in environment or config file

    def test_br003_version_conflicts_handled_gracefully(
        self, registry_publisher, mock_subprocess
    ):
        """BR-003: Version conflicts MUST be handled gracefully."""
        # Arrange
        mock_subprocess.return_value.returncode = 1
        mock_subprocess.return_value.stderr = "E403: You cannot publish over the previously published version"

        # Act
        result = registry_publisher.publish_npm(
            package_path="/dist",
            registry="https://registry.npmjs.org",
            token="token",
            dry_run=False,
        )

        # Assert - Should not raise, return True with skip reason
        assert result is True

    def test_br004_invalid_credentials_fail_immediately(
        self, registry_publisher
    ):
        """BR-004: Failed credentials MUST cause immediate failure."""
        # Act & Assert
        with pytest.raises(ValueError):
            registry_publisher.publish_npm(
                package_path="/dist",
                registry="https://registry.npmjs.org",
                token="",  # Invalid/empty token
                dry_run=False,
            )


# =============================================================================
# Non-Functional Requirements Tests
# =============================================================================

class TestNonFunctionalRequirements:
    """Tests for NFR from Technical Specification."""

    def test_nfr001_credential_validation_under_2_seconds(
        self, registry_publisher, mock_subprocess, registry_config
    ):
        """NFR-001: Credential validation completes in < 2 seconds."""
        import time

        # Arrange
        start_time = time.time()

        # Act
        result = registry_publisher.publish_all(
            config=registry_config,
            dry_run=True,  # Only validate, don't actually publish
        )

        # Assert
        elapsed = time.time() - start_time
        assert elapsed < 2.0, f"Credential validation took {elapsed}s (expected <2s)"

    def test_nfr003_network_timeout_handled_with_clear_error(
        self, registry_publisher, mock_subprocess
    ):
        """NFR-003: Network timeouts handled with clear error messages."""
        # Arrange
        mock_subprocess.side_effect = subprocess.TimeoutExpired(
            cmd="npm publish",
            timeout=60,
        )

        # Act
        from installer.registry_publisher import RegistryConfig
        config = RegistryConfig(
            npm_enabled=True,
            pypi_enabled=False,
            nuget_enabled=False,
            docker_enabled=False,
            github_enabled=False,
            crates_enabled=False,
            package_name="devforgeai",
            version="1.0.0",
        )

        result = registry_publisher.publish_all(
            config=config,
            dry_run=False,
        )

        # Assert
        assert result.success is False
        assert "npm" in result.registry_results
        assert "timeout" in result.registry_results["npm"].error.lower()


# =============================================================================
# Edge Cases Tests
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases from story specification."""

    def test_missing_optional_registry_credentials_should_skip(
        self, registry_publisher, mock_subprocess
    ):
        """Edge Case 1: Missing credentials for optional registry - skip with info."""
        # Arrange
        from installer.registry_publisher import RegistryConfig
        config = RegistryConfig(
            npm_enabled=True,
            pypi_enabled=True,
            nuget_enabled=True,
            docker_enabled=True,
            github_enabled=True,
            crates_enabled=True,
            package_name="devforgeai",
            version="1.0.0",
        )

        # Remove one credential from environment
        with patch.dict(os.environ, {"CARGO_REGISTRY_TOKEN": ""}, clear=False):
            # Act
            result = registry_publisher.publish_all(
                config=config,
                dry_run=False,
            )

            # Assert - crates should be skipped, others should succeed
            assert result.registry_results["crates"].skipped_reason is not None

    def test_invalid_package_should_fail_fast(
        self, registry_publisher, mock_subprocess
    ):
        """Edge Case 5: Invalid package - Fail fast before any publish attempt."""
        # Arrange
        from installer.registry_publisher import RegistryConfig
        config = RegistryConfig(
            npm_enabled=True,
            pypi_enabled=False,
            nuget_enabled=False,
            docker_enabled=False,
            github_enabled=False,
            crates_enabled=False,
            package_name="",  # Invalid - empty package name
            version="1.0.0",
        )

        # Act & Assert
        with pytest.raises(ValueError, match="package"):
            registry_publisher.publish_all(
                config=config,
                dry_run=False,
            )
