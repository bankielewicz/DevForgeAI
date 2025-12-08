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
        Path.home() / ".devforgeai" / "bin",
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
            binary_path = bin_dir / binary_name

            if self.file_system:
                # Use mocked file system
                if self.file_system.exists(str(binary_path)):
                    if self.file_system.is_file(str(binary_path)):
                        try:
                            self.file_system.remove_file(str(binary_path))
                            result.binaries_removed.append(str(binary_path))
                            result.removed = True
                        except Exception as e:
                            result.warnings.append(f"Failed to remove {binary_path}: {e}")
            else:
                # Use real file system
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

        # Check if binary is in system PATH (requires manual cleanup)
        system_path = shutil.which(binary_name)
        if system_path and not any(str(d) in system_path for d in self.LOCAL_BIN_DIRS):
            result.warnings.append(
                f"Binary found in system PATH: {system_path}. "
                "Manual removal required."
            )
            result.requires_manual_cleanup = True

        return result

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
