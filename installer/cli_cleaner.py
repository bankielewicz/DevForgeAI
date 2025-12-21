"""CLICleaner service for STORY-081.

Handles cleanup of CLI binaries and shell integrations:
- Remove local binaries (~/bin/, ~/.local/bin/)
- Detect binaries in system PATH
- Clean shell integrations (bash, zsh, fish)
- Provide manual cleanup instructions when needed
"""

import os
import shutil
from pathlib import Path
from typing import Any, List, Optional

from installer.uninstall_models import CLICleanupResult


class CLICleaner:
    """Cleans up CLI binaries and shell integrations."""

    # CLI binary names to remove
    CLI_BINARIES = ["devforgeai", "devforgeai-validate"]

    # Local binary directories (user-writable)
    LOCAL_BIN_DIRS = [
        Path.home() / "bin",
        Path.home() / ".local" / "bin",
        Path.home() / "devforgeai" / "bin",
    ]

    # Shell config files for integration cleanup
    SHELL_CONFIGS = {
        "bash": [".bashrc", ".bash_profile", ".profile"],
        "zsh": [".zshrc", ".zprofile"],
        "fish": [".config/fish/config.fish"],
    }

    def __init__(self, file_system: Any = None, logger: Any = None):
        """Initialize CLI cleaner.

        Args:
            file_system: File system abstraction (optional)
            logger: Logger for messages
        """
        self.file_system = file_system
        self.logger = logger

    def remove_local_binary(self, binary_name: str) -> CLICleanupResult:
        """Remove a local binary from user directories.

        Args:
            binary_name: Name of binary to remove

        Returns:
            CLICleanupResult with status
        """
        result = CLICleanupResult()

        for bin_dir in self.LOCAL_BIN_DIRS:
            self._remove_binary_from_dir(bin_dir, binary_name, result)

        self._check_system_path_binary(binary_name, result)
        return result

    def _remove_binary_from_dir(self, bin_dir: Path, binary_name: str, result: CLICleanupResult) -> None:
        """Remove binary from a specific directory.

        Args:
            bin_dir: Directory to search
            binary_name: Name of binary to remove
            result: CLICleanupResult to update
        """
        binary_path = bin_dir / binary_name

        if self.file_system:
            self._remove_binary_mocked(binary_path, result)
        else:
            self._remove_binary_real(binary_path, result)

    def _remove_binary_mocked(self, binary_path: Path, result: CLICleanupResult) -> None:
        """Remove binary using mocked file system.

        Args:
            binary_path: Path to binary
            result: CLICleanupResult to update
        """
        if self.file_system.exists(str(binary_path)):
            if self.file_system.is_file(str(binary_path)):
                try:
                    self.file_system.remove_file(str(binary_path))
                    result.binaries_removed.append(str(binary_path))
                    result.removed = True
                except Exception as e:
                    result.warnings.append(f"Failed to remove {binary_path}: {e}")

    def _remove_binary_real(self, binary_path: Path, result: CLICleanupResult) -> None:
        """Remove binary using real file system.

        Args:
            binary_path: Path to binary
            result: CLICleanupResult to update
        """
        if binary_path.exists() and binary_path.is_file():
            try:
                binary_path.unlink()
                result.binaries_removed.append(str(binary_path))
                result.removed = True
            except PermissionError:
                result.warnings.append(
                    f"Permission denied: {binary_path}. "
                    "May require sudo to remove."
                )

    def _check_system_path_binary(self, binary_name: str, result: CLICleanupResult) -> None:
        """Check if binary exists in system PATH.

        Args:
            binary_name: Name of binary to check
            result: CLICleanupResult to update
        """
        system_path = shutil.which(binary_name)
        if system_path and not any(str(d) in system_path for d in self.LOCAL_BIN_DIRS):
            result.warnings.append(
                f"Binary found in system PATH: {system_path}. "
                "Manual removal required."
            )
            result.requires_manual_cleanup = True

    def remove_wrapper_scripts(self) -> CLICleanupResult:
        """Remove wrapper scripts for all CLI binaries.

        Returns:
            CLICleanupResult with status
        """
        result = CLICleanupResult()

        for binary_name in self.CLI_BINARIES:
            binary_result = self.remove_local_binary(binary_name)
            result.binaries_removed.extend(binary_result.binaries_removed)
            result.warnings.extend(binary_result.warnings)
            if binary_result.removed:
                result.removed = True
            if binary_result.requires_manual_cleanup:
                result.requires_manual_cleanup = True

        return result

    def is_binary_in_path(self, binary_name: str) -> bool:
        """Check if binary is in system PATH.

        Args:
            binary_name: Name of binary to check

        Returns:
            True if binary found in PATH
        """
        return shutil.which(binary_name) is not None

    def cleanup_shell_aliases(self, shell: str) -> CLICleanupResult:
        """Clean up shell aliases for a specific shell.

        Args:
            shell: Shell name (bash, zsh, fish)

        Returns:
            CLICleanupResult with status
        """
        result = CLICleanupResult()

        config_files = self.SHELL_CONFIGS.get(shell, [])
        for config_file in config_files:
            config_path = Path.home() / config_file

            if config_path.exists():
                try:
                    # Read config and filter out devforgeai lines
                    content = config_path.read_text()
                    lines = content.splitlines()
                    filtered = [
                        line for line in lines
                        if "devforgeai" not in line.lower()
                    ]

                    if len(filtered) < len(lines):
                        config_path.write_text("\n".join(filtered) + "\n")
                        result.removed = True

                except PermissionError:
                    result.warnings.append(f"Cannot modify {config_path}")

        return result

    def cleanup_shell_integrations(self, shell: str) -> CLICleanupResult:
        """Clean up shell integrations (aliases + completions).

        Args:
            shell: Shell name (bash, zsh, fish)

        Returns:
            CLICleanupResult with status
        """
        result = self.cleanup_shell_aliases(shell)

        # Also check for completion files
        if shell == "bash":
            completion_dir = Path.home() / ".bash_completion.d"
        elif shell == "zsh":
            completion_dir = Path.home() / ".zsh" / "completions"
        elif shell == "fish":
            completion_dir = Path.home() / ".config" / "fish" / "completions"
        else:
            completion_dir = None

        if completion_dir and completion_dir.exists():
            for binary in self.CLI_BINARIES:
                completion_file = completion_dir / f"_{binary}"
                if completion_file.exists():
                    try:
                        completion_file.unlink()
                        result.removed = True
                    except PermissionError:
                        result.warnings.append(f"Cannot remove {completion_file}")

        return result

    def cleanup_all_shell_integrations(self) -> CLICleanupResult:
        """Clean up integrations for all shells.

        Returns:
            CLICleanupResult with combined status
        """
        result = CLICleanupResult()

        for shell in self.SHELL_CONFIGS.keys():
            shell_result = self.cleanup_shell_integrations(shell)
            result.warnings.extend(shell_result.warnings)
            if shell_result.removed:
                result.removed = True

        return result

    def check_npm_global_install(self) -> CLICleanupResult:
        """Check for npm global installation.

        Returns:
            CLICleanupResult with warnings if npm global found
        """
        result = CLICleanupResult()

        for binary in self.CLI_BINARIES:
            binary_path = shutil.which(binary)
            if binary_path and "node_modules" in binary_path:
                result.warnings.append(
                    f"Found npm global installation: {binary_path}. "
                    "Run 'npm uninstall -g devforgeai' to remove."
                )
                result.requires_manual_cleanup = True

        return result

    def detect_homebrew_installation(self) -> CLICleanupResult:
        """Detect if devforgeai was installed via Homebrew on macOS.

        Returns:
            CLICleanupResult with Homebrew detection info
        """
        result = CLICleanupResult()

        try:
            homebrew_path = Path("/usr/local/opt/devforgeai")
            if homebrew_path.exists():
                result.warnings.append(
                    "Detected Homebrew installation at /usr/local/opt/devforgeai. "
                    "Run 'brew uninstall devforgeai' to remove."
                )
                result.requires_manual_cleanup = True
        except Exception:
            pass

        return result

    def remove_homebrew_installation(self) -> CLICleanupResult:
        """Remove Homebrew-installed devforgeai.

        Returns:
            CLICleanupResult with removal status
        """
        result = CLICleanupResult()

        try:
            import subprocess
            # Try to uninstall via brew
            subprocess.run(["brew", "uninstall", "devforgeai"], check=False)
            result.removed = True
        except (FileNotFoundError, Exception):
            result.warnings.append("Homebrew uninstall failed. Please run: brew uninstall devforgeai")

        return result

    def cleanup_fish_completions(self) -> CLICleanupResult:
        """Remove devforgeai completions from Fish shell.

        Returns:
            CLICleanupResult with cleanup status
        """
        result = CLICleanupResult()

        fish_completions = Path.home() / ".config" / "fish" / "conf.d" / "devforgeai.fish"
        if fish_completions.exists():
            try:
                fish_completions.unlink()
                result.removed = True
            except PermissionError:
                result.warnings.append(f"Cannot remove {fish_completions}")

        return result

    def read_config_file(self, config_path: str) -> str:
        """Read shell configuration file.

        Args:
            config_path: Path to config file

        Returns:
            File content or empty string if not found
        """
        config = Path(config_path)
        if config.exists():
            return config.read_text()
        return ""

    def cleanup_fish_functions(self) -> CLICleanupResult:
        """Remove devforgeai function definitions from Fish shell.

        Returns:
            CLICleanupResult with cleanup status
        """
        result = CLICleanupResult()

        fish_config = Path.home() / ".config" / "fish" / "config.fish"
        if fish_config.exists():
            try:
                content = fish_config.read_text()
                filtered = [
                    line for line in content.splitlines()
                    if "devforgeai" not in line.lower() and "function devforgeai" not in line
                ]
                if len(filtered) < len(content.splitlines()):
                    fish_config.write_text("\n".join(filtered) + "\n")
                    result.removed = True
            except PermissionError:
                result.warnings.append(f"Cannot modify {fish_config}")

        return result

    def cleanup_for_docker_environment(self) -> CLICleanupResult:
        """Handle Docker-specific cleanup.

        Returns:
            CLICleanupResult with Docker-aware cleanup status
        """
        result = CLICleanupResult()

        import os
        if "DOCKER_HOST" in os.environ or Path("/.dockerenv").exists():
            result.warnings.append(
                "Docker environment detected. Skipping system PATH cleanup. "
                "Only container-local paths will be cleaned."
            )

        return result

    def detect_kubernetes_environment(self) -> CLICleanupResult:
        """Detect Kubernetes environment and handle mounted paths.

        Returns:
            CLICleanupResult with Kubernetes detection info
        """
        result = CLICleanupResult()

        import os
        if "KUBERNETES_SERVICE_HOST" in os.environ:
            result.warnings.append(
                "Kubernetes environment detected. Be careful with mounted volume cleanup."
            )
            result.requires_manual_cleanup = True

        return result

    def cleanup_venv_installation(self) -> CLICleanupResult:
        """Handle Python virtual environment cleanup.

        Returns:
            CLICleanupResult with venv cleanup status
        """
        result = CLICleanupResult()

        import os
        if "VIRTUAL_ENV" in os.environ:
            venv_path = Path(os.environ["VIRTUAL_ENV"]) / "bin" / "devforgeai"
            if venv_path.exists():
                try:
                    venv_path.unlink()
                    result.removed = True
                except PermissionError:
                    result.warnings.append(f"Cannot remove {venv_path}")

        return result

    def hard_reset_bash_config(self) -> CLICleanupResult:
        """Hard reset corrupted bash configuration.

        Returns:
            CLICleanupResult with reset status
        """
        result = CLICleanupResult()

        bashrc = Path.home() / ".bashrc"
        if bashrc.exists():
            try:
                content = bashrc.read_text()
                # Remove devforgeai lines
                filtered = [
                    line for line in content.splitlines()
                    if "devforgeai" not in line.lower()
                ]
                bashrc.write_text("\n".join(filtered) + "\n")
                result.removed = True
            except PermissionError:
                result.warnings.append(f"Cannot modify {bashrc}")

        return result

    def validate_config_integrity(self) -> bool:
        """Validate shell config file syntax integrity.

        Returns:
            True if config is valid, False otherwise
        """
        import subprocess

        bashrc = Path.home() / ".bashrc"
        if bashrc.exists():
            try:
                # Check bash syntax
                result = subprocess.run(
                    ["bash", "-n", str(bashrc)],
                    capture_output=True,
                    timeout=5
                )
                return result.returncode == 0
            except (subprocess.TimeoutExpired, FileNotFoundError):
                return False

        return True

    def backup_and_reset_config(self) -> CLICleanupResult:
        """Backup corrupted config before hard reset.

        Returns:
            CLICleanupResult with backup and reset status
        """
        result = CLICleanupResult()

        bashrc = Path.home() / ".bashrc"
        if bashrc.exists():
            try:
                # Create backup
                backup_path = bashrc.with_suffix(".bashrc.backup")
                if not backup_path.exists():
                    import shutil
                    shutil.copy2(bashrc, backup_path)
                    result.warnings.append(f"Backup created at {backup_path}")

                # Then reset
                reset_result = self.hard_reset_bash_config()
                result.removed = reset_result.removed
                result.warnings.extend(reset_result.warnings)
            except Exception as e:
                result.warnings.append(f"Error during backup/reset: {e}")

        return result

    def get_manual_cleanup_instructions(self) -> str:
        """Get instructions for manual PATH cleanup.

        Returns:
            Instructions string
        """
        return """
Manual CLI Cleanup Instructions:
================================

1. NPM Global Installation:
   npm uninstall -g devforgeai

2. System PATH Binary:
   sudo rm /usr/local/bin/devforgeai
   sudo rm /usr/local/bin/devforgeai-validate

3. Shell Integrations:
   Remove any lines containing 'devforgeai' from:
   - ~/.bashrc
   - ~/.zshrc
   - ~/.config/fish/config.fish

4. Shell Completions:
   rm ~/.bash_completion.d/_devforgeai
   rm ~/.zsh/completions/_devforgeai
   rm ~/.config/fish/completions/devforgeai.fish

After cleanup, restart your shell or run:
   source ~/.bashrc  # or ~/.zshrc
"""
