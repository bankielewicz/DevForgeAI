"""Registry Publisher for STORY-244 - publishes packages to language-specific registries."""
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from installer.credential_masker import CredentialMasker


@dataclass
class RegistryConfig:
    """Configuration for package registry publishing (AC#6)."""
    npm_enabled: bool = False
    pypi_enabled: bool = False
    nuget_enabled: bool = False
    docker_enabled: bool = False
    github_enabled: bool = False
    crates_enabled: bool = False
    package_name: str = ""
    version: str = ""


@dataclass
class RegistryResult:
    """Result of a registry publish operation (AC#6)."""
    registry: str
    success: bool
    version: str
    url: Optional[str] = None
    error: Optional[str] = None
    skipped_reason: Optional[str] = None


@dataclass
class PublishResult:
    """Result of publish_all operation (AC#6)."""
    success: bool
    registry_results: Dict[str, RegistryResult]
    masked_logs: List[str]
    dry_run: bool


class RegistryPublisher:
    """
    Publishes packages to language-specific registries (AC#6).

    Supports npm, PyPI, NuGet, Docker, GitHub Packages, and crates.io.
    Implements business rules BR-001 through BR-005.
    """

    def __init__(self, masker: Optional[CredentialMasker] = None):
        """
        Initialize registry publisher.

        Args:
            masker: Credential masker for sanitizing output. If None, creates one.
        """
        self._masker = masker or CredentialMasker()
        self._logs: List[str] = []

    def _log(self, message: str) -> None:
        """Add a log message, masking any credentials."""
        masked = self._masker.mask_output(message)
        self._logs.append(masked)

    def _run_command(
        self,
        cmd: List[str],
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None,
        input_data: Optional[str] = None,
    ) -> Tuple[int, str, str]:
        """
        Run a command and return sanitized output (BR-004).

        Args:
            cmd: Command to run as list of strings.
            env: Environment variables to set.
            cwd: Working directory.
            input_data: Input to send to stdin.

        Returns:
            Tuple of (return_code, sanitized_stdout, sanitized_stderr).
        """
        process_env = os.environ.copy()
        if env:
            process_env.update(env)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=process_env,
                cwd=cwd,
                input=input_data,
                timeout=300  # 5 minute timeout
            )

            # Sanitize output (BR-004)
            stdout = self._masker.mask_output(result.stdout)
            stderr = self._masker.mask_output(result.stderr)

            return result.returncode, stdout, stderr
        except subprocess.TimeoutExpired:
            return -1, "", "timeout: Command timed out after 300 seconds"
        except Exception as e:
            return -1, "", self._masker.mask_output(str(e))

    def publish_npm(
        self,
        package_path: str,
        registry: str,
        token: str,
        dry_run: bool = False,
    ) -> bool:
        """
        Publish to npm registry (AC#1).

        Args:
            package_path: Path to the npm package directory.
            registry: Registry URL (e.g., https://registry.npmjs.org).
            token: NPM authentication token.
            dry_run: If True, validate but don't publish.

        Returns:
            True if successful or skipped (version exists), raises ValueError if invalid.

        Raises:
            ValueError: If token is empty (BR-004).
            RuntimeError: If a timeout or other critical error occurs.
        """
        if not token:
            raise ValueError("NPM_TOKEN environment variable is required")

        if dry_run:
            self._log(f"DRY RUN: would publish to npm registry {registry}")
            return True

        # Set up npmrc with token
        cmd = ["npm", "publish", "--registry", registry]

        # Set token in environment
        env = {"NPM_TOKEN": token}

        returncode, stdout, stderr = self._run_command(cmd, env=env, cwd=package_path)
        self._log(stdout)

        if returncode == 0:
            return True

        # Check for timeout error
        if "timeout" in stderr.lower():
            raise RuntimeError(f"timeout: {stderr}")

        # Check for version conflict (BR-003)
        if "E403" in stderr or "cannot publish over" in stderr.lower():
            self._log(f"npm: Version already exists, skipping")
            return True

        self._log(f"npm publish failed: {stderr}")
        return False

    def publish_pypi(
        self,
        dist_path: str,
        repository: str,
        credentials: Tuple[str, str],
        dry_run: bool = False,
    ) -> bool:
        """
        Publish to PyPI registry (AC#2).

        Args:
            dist_path: Path to the dist directory with packages.
            repository: Repository name (pypi or testpypi).
            credentials: Tuple of (username, password).
            dry_run: If True, validate but don't publish.

        Returns:
            True if successful or skipped (version exists), raises ValueError if invalid.

        Raises:
            ValueError: If credentials are empty (BR-004).
        """
        username, password = credentials
        if not username or not password:
            raise ValueError("TWINE_USERNAME and TWINE_PASSWORD are required")

        if dry_run:
            self._log(f"DRY RUN: would publish to PyPI repository {repository}")
            return True

        cmd = [
            "python", "-m", "twine", "upload",
            "--repository", repository,
            "--skip-existing",
            f"{dist_path}/*",
        ]

        env = {
            "TWINE_USERNAME": username,
            "TWINE_PASSWORD": password,
        }

        returncode, stdout, stderr = self._run_command(cmd, env=env)
        self._log(stdout)

        if returncode == 0:
            return True

        self._log(f"PyPI publish failed: {stderr}")
        return False

    def publish_nuget(
        self,
        nupkg_path: str,
        source: str,
        api_key: str,
        dry_run: bool = False,
    ) -> bool:
        """
        Publish to NuGet registry (AC#3).

        Args:
            nupkg_path: Path to the .nupkg file.
            source: NuGet source URL.
            api_key: NuGet API key.
            dry_run: If True, validate but don't publish.

        Returns:
            True if successful or skipped (version exists), raises ValueError if invalid.

        Raises:
            ValueError: If api_key is empty (BR-004).
        """
        if not api_key:
            raise ValueError("NUGET_API_KEY environment variable is required")

        if dry_run:
            self._log(f"DRY RUN: would publish to NuGet source {source}")
            return True

        cmd = [
            "dotnet", "nuget", "push",
            nupkg_path,
            "--source", source,
            "--api-key", api_key,
            "--skip-duplicate",
        ]

        returncode, stdout, stderr = self._run_command(cmd)
        self._log(stdout)

        if returncode == 0:
            return True

        self._log(f"NuGet publish failed: {stderr}")
        return False

    def publish_docker(
        self,
        image: str,
        tags: List[str],
        registry: str,
        credentials: Tuple[str, str],
        dry_run: bool = False,
    ) -> bool:
        """
        Publish to Docker registry (AC#4).

        Args:
            image: Docker image name.
            tags: List of tags to push.
            registry: Docker registry URL.
            credentials: Tuple of (username, password).
            dry_run: If True, validate but don't publish.

        Returns:
            True if successful, raises ValueError if invalid.

        Raises:
            ValueError: If credentials are empty (BR-004).
        """
        username, password = credentials
        if not username or not password:
            raise ValueError("DOCKER_USERNAME and DOCKER_PASSWORD are required")

        if dry_run:
            self._log(f"DRY RUN: would publish to Docker registry {registry}")
            return True

        # Login to registry
        login_cmd = ["docker", "login", registry, "-u", username, "--password-stdin"]
        returncode, _, stderr = self._run_command(login_cmd, input_data=password)

        if returncode != 0:
            self._log(f"Docker login failed: {stderr}")
            return False

        # Push each tag
        all_success = True
        for tag in tags:
            image_tag = f"{registry}/{image}:{tag}" if registry != "docker.io" else f"{image}:{tag}"

            # Tag the image
            tag_cmd = ["docker", "tag", f"{image}:latest", image_tag]
            returncode, _, stderr = self._run_command(tag_cmd)
            if returncode != 0:
                self._log(f"Docker tag failed for {tag}: {stderr}")
                all_success = False
                continue

            # Push the image
            push_cmd = ["docker", "push", image_tag]
            returncode, stdout, stderr = self._run_command(push_cmd)
            self._log(stdout)

            if returncode != 0:
                self._log(f"Docker push failed for {tag}: {stderr}")
                all_success = False

        # Logout (cleanup)
        logout_cmd = ["docker", "logout", registry]
        self._run_command(logout_cmd)

        return all_success

    def publish_github(
        self,
        package_type: str,
        package_path: str,
        token: str,
        owner: str,
        dry_run: bool = False,
    ) -> bool:
        """
        Publish to GitHub Packages (AC#5).

        Args:
            package_type: Type of package (npm, container, etc.).
            package_path: Path to the package.
            token: GitHub token.
            owner: GitHub owner/organization.
            dry_run: If True, validate but don't publish.

        Returns:
            True if successful, raises ValueError if invalid.

        Raises:
            ValueError: If token is empty (BR-004).
        """
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable is required")

        if dry_run:
            self._log(f"DRY RUN: would publish to GitHub Packages")
            return True

        if package_type == "npm":
            registry = f"https://npm.pkg.github.com"
            cmd = ["npm", "publish", "--registry", registry, f"--@{owner}:registry={registry}"]
            env = {"GITHUB_TOKEN": token, "NPM_TOKEN": token}
            returncode, stdout, stderr = self._run_command(cmd, env=env, cwd=package_path)

        elif package_type == "container":
            registry = "ghcr.io"
            # Login to ghcr.io
            login_cmd = ["docker", "login", registry, "-u", owner, "--password-stdin"]
            returncode, _, stderr = self._run_command(login_cmd, input_data=token)

            if returncode != 0:
                self._log(f"GitHub container login failed: {stderr}")
                return False

            # Push image
            image_tag = f"{registry}/{package_path}"
            push_cmd = ["docker", "push", image_tag]
            returncode, stdout, stderr = self._run_command(push_cmd)
        else:
            self._log(f"Unsupported GitHub package type: {package_type}")
            return False

        self._log(stdout if returncode == 0 else stderr)
        return returncode == 0

    def publish_crates(
        self,
        crate_path: str,
        token: str,
        dry_run: bool = False,
    ) -> bool:
        """
        Publish to crates.io (AC#6).

        Args:
            crate_path: Path to the Cargo crate.
            token: Cargo registry token.
            dry_run: If True, validate but don't publish.

        Returns:
            True if successful or skipped (version exists), raises ValueError if invalid.

        Raises:
            ValueError: If token is empty (BR-004).
        """
        if not token:
            raise ValueError("CARGO_REGISTRY_TOKEN environment variable is required")

        if dry_run:
            self._log(f"DRY RUN: would publish to crates.io")
            return True

        cmd = ["cargo", "publish", "--token", token]
        env = {"CARGO_REGISTRY_TOKEN": token}

        returncode, stdout, stderr = self._run_command(cmd, env=env, cwd=crate_path)
        self._log(stdout)

        if returncode == 0:
            return True

        # Check for version conflict (BR-003)
        if "already uploaded" in stderr.lower():
            self._log(f"crates.io: Version already exists, skipping")
            return True

        self._log(f"Cargo publish failed: {stderr}")
        return False

    def _handle_registry_publish(
        self,
        registry_name: str,
        publish_func: callable,
        version: str,
        success_url: Optional[str],
    ) -> Tuple[RegistryResult, bool]:
        """
        Execute a registry publish with standardized error handling.

        Args:
            registry_name: Name of the registry (npm, pypi, etc.).
            publish_func: Callable that performs the publish, returns bool.
            version: Package version being published.
            success_url: URL to include on success, or None.

        Returns:
            Tuple of (RegistryResult, success_flag).
        """
        try:
            success = publish_func()
            return RegistryResult(
                registry=registry_name,
                success=success,
                version=version,
                url=success_url if success else None,
            ), success
        except ValueError as e:
            return RegistryResult(
                registry=registry_name,
                success=False,
                version=version,
                error=str(e),
            ), False
        except subprocess.TimeoutExpired as e:
            return RegistryResult(
                registry=registry_name,
                success=False,
                version=version,
                error=f"timeout: {str(e)}",
            ), False
        except Exception as e:
            error_msg = str(e).lower()
            error_text = f"timeout: {str(e)}" if "timeout" in error_msg else str(e)
            return RegistryResult(
                registry=registry_name,
                success=False,
                version=version,
                error=error_text,
            ), False

    def publish_all(
        self,
        config: RegistryConfig,
        dry_run: bool = False,
    ) -> PublishResult:
        """
        Publish to all enabled registries (AC#8 for dry-run mode).

        Args:
            config: Registry configuration.
            dry_run: If True, validate but don't publish.

        Returns:
            PublishResult with results from all registries.

        Raises:
            ValueError: If package_name is empty.
        """
        self._logs = []  # Reset logs

        if not config.package_name:
            raise ValueError("package_name is required")

        registry_results: Dict[str, RegistryResult] = {}
        overall_success = True

        # npm
        if config.npm_enabled:
            result, success = self._handle_registry_publish(
                registry_name="npm",
                publish_func=lambda: self.publish_npm(
                    package_path="/dist",
                    registry="https://registry.npmjs.org",
                    token=os.environ.get("NPM_TOKEN", ""),
                    dry_run=dry_run,
                ),
                version=config.version,
                success_url=f"https://npmjs.com/package/{config.package_name}",
            )
            registry_results["npm"] = result
            if not success:
                overall_success = False

        # PyPI
        if config.pypi_enabled:
            result, success = self._handle_registry_publish(
                registry_name="pypi",
                publish_func=lambda: self.publish_pypi(
                    dist_path="/dist",
                    repository="pypi",
                    credentials=(
                        os.environ.get("TWINE_USERNAME", ""),
                        os.environ.get("TWINE_PASSWORD", ""),
                    ),
                    dry_run=dry_run,
                ),
                version=config.version,
                success_url=f"https://pypi.org/project/{config.package_name}/",
            )
            registry_results["pypi"] = result
            if not success:
                overall_success = False

        # NuGet
        if config.nuget_enabled:
            result, success = self._handle_registry_publish(
                registry_name="nuget",
                publish_func=lambda: self.publish_nuget(
                    nupkg_path=f"/output/{config.package_name}.{config.version}.nupkg",
                    source="https://api.nuget.org/v3/index.json",
                    api_key=os.environ.get("NUGET_API_KEY", ""),
                    dry_run=dry_run,
                ),
                version=config.version,
                success_url=f"https://nuget.org/packages/{config.package_name}/",
            )
            registry_results["nuget"] = result
            if not success:
                overall_success = False

        # Docker
        if config.docker_enabled:
            result, success = self._handle_registry_publish(
                registry_name="docker",
                publish_func=lambda: self.publish_docker(
                    image=config.package_name,
                    tags=[config.version, "latest"],
                    registry="docker.io",
                    credentials=(
                        os.environ.get("DOCKER_USERNAME", ""),
                        os.environ.get("DOCKER_PASSWORD", ""),
                    ),
                    dry_run=dry_run,
                ),
                version=config.version,
                success_url=f"https://hub.docker.com/r/{config.package_name}",
            )
            registry_results["docker"] = result
            if not success:
                overall_success = False

        # GitHub Packages
        if config.github_enabled:
            result, success = self._handle_registry_publish(
                registry_name="github",
                publish_func=lambda: self.publish_github(
                    package_type="npm",
                    package_path="/dist",
                    token=os.environ.get("GITHUB_TOKEN", ""),
                    owner="devforgeai",
                    dry_run=dry_run,
                ),
                version=config.version,
                success_url=f"https://github.com/devforgeai/{config.package_name}/packages",
            )
            registry_results["github"] = result
            if not success:
                overall_success = False

        # crates.io (special case: skip if no token)
        if config.crates_enabled:
            token = os.environ.get("CARGO_REGISTRY_TOKEN", "")
            if not token:
                registry_results["crates"] = RegistryResult(
                    registry="crates",
                    success=True,
                    version=config.version,
                    skipped_reason="CARGO_REGISTRY_TOKEN not set",
                )
            else:
                result, success = self._handle_registry_publish(
                    registry_name="crates",
                    publish_func=lambda: self.publish_crates(
                        crate_path="/crate",
                        token=token,
                        dry_run=dry_run,
                    ),
                    version=config.version,
                    success_url=f"https://crates.io/crates/{config.package_name}",
                )
                registry_results["crates"] = result
                if not success:
                    overall_success = False

        # Add dry-run prefix to logs
        if dry_run:
            self._logs.insert(0, "DRY RUN: Validating publish configuration")

        return PublishResult(
            success=overall_success,
            registry_results=registry_results,
            masked_logs=self._logs,
            dry_run=dry_run,
        )
