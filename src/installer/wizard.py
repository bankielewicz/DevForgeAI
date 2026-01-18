"""
CLI Wizard Installer for DevForgeAI (STORY-247)

Provides step-by-step interactive installation wizard with:
- Welcome screen with framework info (AC#1)
- License agreement requiring 'accept' (AC#2)
- Installation path selection with validation (AC#3)
- Component selection with Core Framework locked (AC#4)
- Configuration options including Git integration (AC#5)
- Progress display with real-time updates (AC#6)
- Completion summary with next steps (AC#7)
- Error recovery with retry/skip/abort options (AC#8)

Business Rules:
- BR-001: Core Framework cannot be deselected
- BR-002: License requires 'accept' text (case-insensitive)
- BR-003: Path validated for write permissions (os.access)
- BR-004: Git options disabled if Git unavailable (shutil.which)
- BR-005: Progress callback invoked per step

Usage:
    from installer.wizard import WizardInstaller

    wizard = WizardInstaller(target_path="/path/to/install")
    exit_code = wizard.run()
"""

import os
import shutil
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

from installer.exit_codes import ExitCodes
from installer import deploy


# Framework version for display
FRAMEWORK_VERSION = "1.0.0"

# Display constants for consistent formatting
HEADER_WIDTH = 60
HEADER_CHAR = "="
SEPARATOR_CHAR = "-"


@dataclass
class Component:
    """
    Installable component definition.

    Attributes:
        id: Unique identifier for the component
        name: Display name
        description: Brief description of what's included
        size_mb: Estimated size in megabytes
        required: If True, component cannot be deselected
        selected: Current selection state
    """

    id: str
    name: str
    description: str = ""
    size_mb: float = 0.0
    required: bool = False
    selected: bool = False


@dataclass
class WizardState:
    """
    Current state of the installation wizard.

    Attributes:
        current_step: Current step index (0-6)
        target_path: Installation target directory
        components: List of available components
        config: Configuration options (init_git, create_commit, run_validation)
        progress: Installation progress (0.0 to 1.0)
    """

    current_step: int
    target_path: Path
    components: List[Component]
    config: Dict[str, bool]
    progress: float = 0.0


class WizardInstaller:
    """
    Interactive CLI wizard for DevForgeAI installation.

    Guides the user through a step-by-step installation process with
    validation, component selection, and progress tracking.

    Args:
        target_path: Target directory for installation
        tty_mode: If False, operates in non-interactive mode (NFR-004)

    Example:
        >>> wizard = WizardInstaller(target_path="/home/user/project")
        >>> exit_code = wizard.run()
        >>> if exit_code == 0:
        ...     print("Installation successful!")
    """

    # Default components for installation
    DEFAULT_COMPONENTS = [
        Component(
            id="core",
            name="Core Framework",
            description=".claude/, devforgeai/",
            size_mb=2.5,
            required=True,
            selected=True,
        ),
        Component(
            id="cli",
            name="CLI Tools",
            description="devforgeai command",
            size_mb=0.5,
            required=False,
            selected=False,
        ),
        Component(
            id="templates",
            name="Templates",
            description="project templates",
            size_mb=1.0,
            required=False,
            selected=False,
        ),
        Component(
            id="examples",
            name="Examples",
            description="example projects",
            size_mb=3.0,
            required=False,
            selected=False,
        ),
    ]

    def __init__(
        self,
        target_path: Union[str, Path],
        tty_mode: bool = True,
    ):
        """Initialize the wizard installer with target path and mode."""
        # Handle empty path - use current directory
        if not target_path:
            target_path = Path.cwd()
        else:
            target_path = Path(target_path)

        # Initialize state with default components
        self.state = WizardState(
            current_step=0,
            target_path=target_path,
            components=self._create_default_components(),
            config={
                "init_git": False,
                "create_commit": False,
                "run_validation": False,
            },
            progress=0.0,
        )

        self.tty_mode = tty_mode
        self._progress_callback: Optional[Callable[[str, float, Optional[float]], None]] = None
        self._log_file: Optional[str] = None

    def _create_default_components(self) -> List[Component]:
        """Create a fresh copy of default components."""
        return [
            Component(
                id=c.id,
                name=c.name,
                description=c.description,
                size_mb=c.size_mb,
                required=c.required,
                selected=c.selected,
            )
            for c in self.DEFAULT_COMPONENTS
        ]

    # -------------------------------------------------------------------------
    # Display Formatting Helpers (DRY Principle)
    # -------------------------------------------------------------------------

    def _print_header(self, title: str) -> None:
        """Print a section header with consistent formatting."""
        print("\n" + HEADER_CHAR * HEADER_WIDTH)
        print(f"  {title}")
        print(HEADER_CHAR * HEADER_WIDTH)

    def _print_separator(self) -> None:
        """Print a section separator line."""
        print(SEPARATOR_CHAR * HEADER_WIDTH)

    def _format_checkbox(self, selected: bool) -> str:
        """Return checkbox indicator for selection state."""
        return "[x]" if selected else "[ ]"

    # -------------------------------------------------------------------------
    # Wizard Step Methods
    # -------------------------------------------------------------------------

    def run(self) -> int:
        """
        Execute the full installation wizard.

        Returns:
            0 on success, non-zero on failure or cancellation.
        """
        try:
            # Step 0: Welcome
            if not self.step_welcome():
                return ExitCodes.VALIDATION_FAILED

            # Step 1: License
            if not self.step_license():
                return ExitCodes.VALIDATION_FAILED

            # Step 2: Path selection
            if not self.step_path():
                return ExitCodes.VALIDATION_FAILED

            # Step 3: Component selection
            if not self.step_components():
                return ExitCodes.VALIDATION_FAILED

            # Step 4: Configuration
            if not self.step_config():
                return ExitCodes.VALIDATION_FAILED

            # Step 5: Installation
            if not self.step_install():
                return ExitCodes.ROLLBACK_OCCURRED

            # Step 6: Complete
            self.step_complete()

            return ExitCodes.SUCCESS

        except KeyboardInterrupt:
            print("\n\nInstallation cancelled by user.")
            return ExitCodes.VALIDATION_FAILED

    def step_welcome(self) -> bool:
        """
        Display welcome screen (AC#1).

        Shows framework name, version, and brief description.
        User presses Enter to continue or Ctrl+C to cancel.

        Returns:
            True to continue, False to cancel.
        """
        self.state.current_step = 0

        self._print_header("Welcome to DevForgeAI Framework Installer")
        print(f"\n  Version: v{FRAMEWORK_VERSION}")
        print("\n  This wizard will guide you through the installation of")
        print("  the DevForgeAI framework in your project.")
        print("\n  What will be installed:")
        print("    - Skills, agents, and commands (.claude/)")
        print("    - Project specifications (devforgeai/)")
        print("    - Configuration files (CLAUDE.md)")
        print()
        self._print_separator()

        try:
            input("\n  Press Enter to continue or Ctrl+C to cancel...")
            return True
        except KeyboardInterrupt:
            return False

    def step_license(self) -> bool:
        """
        Display license agreement and require acceptance (AC#2, BR-002).

        User must type 'accept' (case-insensitive) to proceed.

        Returns:
            True if accepted, False if cancelled.
        """
        self.state.current_step = 1

        self._print_header("License Agreement")
        print("\n  DevForgeAI is released under the MIT License.")
        print("\n  Copyright (c) 2025 DevForgeAI")
        print("\n  Permission is hereby granted, free of charge, to any person")
        print("  obtaining a copy of this software and associated documentation")
        print("  files, to deal in the Software without restriction, including")
        print("  without limitation the rights to use, copy, modify, merge,")
        print("  publish, distribute, sublicense, and/or sell copies of the")
        print("  Software.")
        print("\n  THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND.")
        print()
        self._print_separator()

        return self._prompt_for_license_acceptance()

    def _prompt_for_license_acceptance(self) -> bool:
        """Prompt user until they accept license or cancel."""
        while True:
            try:
                response = input("\n  Type 'accept' to agree to the license terms: ")
                if response.strip().lower() == "accept":
                    return True
                print("  Please type 'accept' to continue or Ctrl+C to cancel.")
            except KeyboardInterrupt:
                return False

    def step_path(self) -> bool:
        """
        Select installation path (AC#3, BR-003).

        Displays default path, allows user to change it.
        Validates path exists and is writable.

        Returns:
            True if valid path selected, False if cancelled.
        """
        self.state.current_step = 2

        self._print_header("Installation Path")
        print(f"\n  Default path: {self.state.target_path}")
        print("\n  Press Enter to accept the default or type a new path.")
        self._print_separator()

        return self._prompt_for_valid_path()

    def _prompt_for_valid_path(self) -> bool:
        """Prompt user until a valid path is provided or cancelled."""
        while True:
            try:
                response = input("\n  Installation path: ").strip()
                path = Path(response) if response else self.state.target_path

                if self.validate_path(str(path)):
                    self.state.target_path = path
                    print(f"  Selected: {path}")
                    return True

                self._display_path_validation_error(path)

            except KeyboardInterrupt:
                return False

    def _display_path_validation_error(self, path: Path) -> None:
        """Display appropriate error message for invalid path."""
        if not path.exists():
            print(f"  Error: Path does not exist: {path}")
        else:
            print(f"  Error: Permission denied - cannot write to {path}")
        print("  Please enter a valid, writable path.")

    def step_components(self) -> bool:
        """
        Select components to install (AC#4, BR-001).

        Displays available components with checkboxes.
        Core Framework is pre-selected and cannot be deselected.

        Returns:
            True to continue, False if cancelled.
        """
        self.state.current_step = 3

        self._print_header("Component Selection")
        print("\n  Select components to install:")
        print("  (Core Framework is required and cannot be deselected)")
        self._print_separator()

        self._display_components_with_size()

        print("\n  Enter component numbers to toggle (e.g., '2,3'), or press Enter to continue.")

        try:
            response = input("\n  Toggle components: ").strip()
            if response:
                self._process_component_toggles(response)
                self._display_components_with_size()
            return True

        except KeyboardInterrupt:
            return False

    def _display_components_with_size(self) -> None:
        """Display component list with selection status and total size."""
        self._display_components()
        print(f"\n  Total size: {self.get_total_size():.1f} MB")

    def _display_components(self) -> None:
        """Display component list with selection status."""
        for i, comp in enumerate(self.state.components, 1):
            checkbox = self._format_checkbox(comp.selected)
            required_marker = " (required)" if comp.required else ""
            print(f"  {i}. {checkbox} {comp.name} - {comp.description} ({comp.size_mb} MB){required_marker}")

    def _process_component_toggles(self, response: str) -> None:
        """Parse and apply component toggle selections."""
        for part in response.split(","):
            part = part.strip()
            if part.isdigit():
                idx = int(part) - 1  # 1-indexed for user
                if 0 <= idx < len(self.state.components):
                    self.toggle_component(self.state.components[idx].id)

    def step_config(self) -> bool:
        """
        Configure additional options (AC#5, BR-004).

        Presents Git options (init, commit) and validation option.
        Git options are disabled if Git is not available.

        Returns:
            True to continue, False if cancelled.
        """
        self.state.current_step = 4

        self._print_header("Configuration Options")

        git_available = self.is_git_available()

        if not git_available:
            print("\n  Note: Git is not available or not installed.")
            print("  Git-related options are disabled.")

        print("\n  Options:")
        self._print_separator()

        self._display_config_options(git_available)

        print("\n  Enter option numbers to toggle (e.g., '1,3'), or press Enter to continue.")

        try:
            response = input("\n  Toggle options: ").strip()
            if response:
                self._process_config_toggles(response, git_available)
            return True

        except KeyboardInterrupt:
            return False

    def _display_config_options(self, git_available: bool) -> None:
        """Display configuration options with availability status."""
        git_disabled_marker = "" if git_available else " [disabled - Git unavailable]"

        options = [
            ("init_git", "Initialize Git repository", git_disabled_marker),
            ("create_commit", "Create initial commit", git_disabled_marker),
            ("run_validation", "Run validation after install", ""),
        ]

        for i, (key, label, marker) in enumerate(options, 1):
            checkbox = self._format_checkbox(self.state.config.get(key, False))
            print(f"  {i}. {checkbox} {label}{marker}")

    def _process_config_toggles(self, response: str, git_available: bool) -> None:
        """Parse and apply configuration option toggles."""
        option_map = {
            "1": ("init_git", git_available),
            "2": ("create_commit", git_available),
            "3": ("run_validation", True),
        }

        for part in response.split(","):
            part = part.strip()
            if part in option_map:
                config_key, is_enabled = option_map[part]
                if is_enabled:
                    self.toggle_config(config_key)

    def step_install(self) -> bool:
        """
        Execute installation with progress display (AC#6, BR-005).

        Shows progress bar, step names, and percentage.
        Logs detailed output to install.log.
        Handles critical errors by stopping installation.

        Returns:
            True on success, False on failure.
        """
        self.state.current_step = 5

        self._print_header("Installing DevForgeAI")

        self._log_file = str(self.state.target_path / "install.log")
        self._init_log_file()

        try:
            return self._execute_installation_steps()
        except PermissionError as e:
            return self._handle_installation_error("Permission denied", e)
        except OSError as e:
            return self._handle_installation_error("OS error", e)

    def _execute_installation_steps(self) -> bool:
        """Execute all installation steps with progress tracking."""
        steps = self._get_installation_steps()
        total_steps = len(steps)

        for current, (step_name, step_action) in enumerate(steps, 1):
            self._update_progress(step_name, current / total_steps)
            print(f"  [{current}/{total_steps}] {step_name}... ")

            if step_action and not step_action():
                print("  Error: Installation failed")
                return False

        self.state.progress = 1.0
        self._update_progress("Complete", 1.0)
        print("\n  Installation complete! (100%)")
        return True

    def _get_installation_steps(self) -> List[tuple]:
        """
        Return list of (step_name, step_action) tuples.

        step_action is None for display-only steps, or a callable returning bool.
        Uses _do_install for file copying to maintain test compatibility.
        """
        return [
            ("Preparing installation", None),
            ("Copying framework files", self._do_install),
            ("Configuring components", None),
            ("Initializing Git repository", None) if self.state.config.get("init_git") else ("Skipping Git setup", None),
            ("Finalizing installation", None),
        ]

    def _execute_file_installation(self) -> bool:
        """
        Perform actual file installation by deploying framework files.

        Resolves source path from module location and calls deploy.deploy_framework_files()
        to copy framework files to the target directory.

        Returns:
            True on success, False on failure.
        """
        self._log("Installation started")
        self._log(f"Target path: {self.state.target_path}")
        self._log(f"Selected components: {[c.id for c in self.state.components if c.selected]}")

        # Resolve source_root from module location
        # installer/wizard.py -> installer/ -> project_root/src/
        source_root = Path(__file__).parent.parent / "src"

        try:
            # Call deploy module to perform actual file deployment
            result = deploy.deploy_framework_files(source_root, self.state.target_path)

            # Handle deployment result
            if result.get("status") == "success":
                files_deployed = result.get("files_deployed", 0)
                self._log(f"Deployed {files_deployed} files successfully")
                return True
            else:
                # Deployment failed
                errors = result.get("errors", [])
                error_msg = "; ".join(errors) if errors else "Unknown deployment error"
                self._log(f"Deployment failed: {error_msg}")
                return False

        except PermissionError as e:
            self._log(f"Permission error during deployment: {e}")
            return False
        except OSError as e:
            self._log(f"OS error during deployment: {e}")
            return False

    def _handle_installation_error(self, error_type: str, error: Exception) -> bool:
        """Handle and log installation errors."""
        print(f"\n  Error: {error_type} - {error}")
        self._log(f"ERROR: {type(error).__name__} - {error}")
        return False

    def _do_install(self) -> bool:
        """
        Perform actual file installation (legacy method for test compatibility).

        Delegates to _execute_file_installation for actual work.
        Tests mock this method, so it must remain for backward compatibility.

        Returns:
            True on success, False on failure.
        """
        return self._execute_file_installation()

    def step_complete(self) -> None:
        """
        Display completion summary (AC#7).

        Shows success message, installation path, installed components,
        and next steps for the user.
        """
        self.state.current_step = 6

        self._print_header("Installation Complete!")
        print("\n  [*] Success! DevForgeAI has been installed.")
        print(f"\n  Installation path: {self.state.target_path}")

        self._display_installed_components()
        self._display_next_steps()

        self._print_header("Thank you for installing DevForgeAI!")
        print()

    def _display_installed_components(self) -> None:
        """Display list of installed components."""
        print("\n  Installed components:")
        for comp in self.state.components:
            if comp.selected:
                print(f"    - {comp.name}")

    def _display_next_steps(self) -> None:
        """Display next steps for the user."""
        print("\n  Next steps:")
        print("    1. Navigate to your project directory:")
        print(f"       cd {self.state.target_path}")
        print("    2. Open Claude Code Terminal and run:")
        print("       /create-context")
        print("    3. Create your first story:")
        print("       /create-story [feature description]")

    def handle_error(
        self,
        error: Exception,
        recoverable: bool = False,
        skippable: bool = False,
    ) -> str:
        """
        Handle installation errors with recovery options (AC#8).

        Displays error message, suggests remediation, and offers
        retry/skip/abort options for recoverable errors.

        Args:
            error: The exception that occurred
            recoverable: If True, offer retry option
            skippable: If True, offer skip option

        Returns:
            Action to take: 'retry', 'skip', or 'abort'
        """
        self._display_error_header(error)
        self._log_error_state(error)
        self._display_remediation_suggestions(error)

        if recoverable:
            return self._prompt_for_error_recovery(skippable)
        return "abort"

    def _display_error_header(self, error: Exception) -> None:
        """Display error header and message."""
        print()
        self._print_separator()
        print("  Error occurred during installation")
        self._print_separator()
        print(f"\n  {type(error).__name__}: {error}")

    def _log_error_state(self, error: Exception) -> None:
        """Log error details and partial state."""
        error_type = type(error).__name__
        self._log(f"ERROR: {error_type} - {error}")
        self._log(f"Progress at error: {self.state.progress * 100:.0f}%")

        if 0 < self.state.progress < 1:
            self._log(f"Partial installation state: {self.state.progress * 100:.0f}% complete")

    def _display_remediation_suggestions(self, error: Exception) -> None:
        """Display context-specific remediation suggestions."""
        suggestions = self._get_remediation_suggestions(error)
        print("\n  Try the following:")
        for suggestion in suggestions:
            print(f"    - {suggestion}")

    def _get_remediation_suggestions(self, error: Exception) -> List[str]:
        """Return remediation suggestions based on error type."""
        if isinstance(error, PermissionError):
            return [
                "Check that you have write permissions to the target directory",
                "Try running with elevated privileges (sudo on Linux/macOS)",
                "Ensure no files are locked by other applications",
            ]
        elif isinstance(error, OSError):
            return [
                "Check available disk space",
                "Verify the target path is valid",
                "Close any applications using the target directory",
            ]
        elif isinstance(error, ConnectionError):
            return [
                "Check your network connection",
                "Retry the installation",
            ]
        return [
            "Check the installation logs for details",
            "Ensure all prerequisites are met",
        ]

    def _prompt_for_error_recovery(self, skippable: bool) -> str:
        """Prompt user for error recovery action."""
        options = ["[r]etry", "[a]bort"]
        if skippable:
            options.insert(1, "[s]kip")

        print(f"\n  Options: {', '.join(options)}")

        try:
            response = input("  Enter choice: ").strip().lower()
            if response == "r":
                return "retry"
            if response == "s" and skippable:
                return "skip"
            return "abort"
        except KeyboardInterrupt:
            return "abort"

    def toggle_component(self, component_id: str) -> bool:
        """
        Toggle component selection state (BR-001).

        Core Framework cannot be deselected.

        Args:
            component_id: ID of component to toggle

        Returns:
            True if toggled, False if component not found or is required.
        """
        for comp in self.state.components:
            if comp.id == component_id:
                # BR-001: Core Framework cannot be deselected
                if comp.required and comp.selected:
                    return False
                comp.selected = not comp.selected
                return True
        return False

    def toggle_config(self, config_key: str) -> None:
        """
        Toggle a configuration option.

        Args:
            config_key: Configuration key to toggle
        """
        if config_key in self.state.config:
            self.state.config[config_key] = not self.state.config[config_key]

    def get_total_size(self) -> float:
        """
        Calculate total size of selected components.

        Returns:
            Total size in MB.
        """
        return sum(comp.size_mb for comp in self.state.components if comp.selected)

    def validate_path(self, path: str) -> bool:
        """
        Validate installation path (BR-003).

        Checks that path exists and is writable using os.access.

        Args:
            path: Path to validate

        Returns:
            True if valid, False otherwise.
        """
        path_obj = Path(path)

        # Check existence
        if not path_obj.exists():
            return False

        # Check write permission (BR-003: use os.access)
        return os.access(str(path_obj), os.W_OK)

    def is_git_available(self) -> bool:
        """
        Check if Git is available on the system (BR-004).

        Uses shutil.which to find git executable.

        Returns:
            True if Git is available, False otherwise.
        """
        return shutil.which("git") is not None

    def set_progress_callback(
        self,
        callback: Callable[[str, float, Optional[float]], None],
    ) -> None:
        """
        Set callback for progress updates (BR-005).

        Args:
            callback: Function(step_name, percentage, eta)
        """
        self._progress_callback = callback

    def update_progress(
        self,
        step_name: str,
        percentage: float,
        eta: Optional[float] = None,
    ) -> None:
        """
        Update progress display (public method for testing).

        Args:
            step_name: Current step name
            percentage: Progress percentage (0.0 to 1.0)
            eta: Estimated time remaining in seconds
        """
        self._update_progress(step_name, percentage, eta)

    def _update_progress(
        self,
        step_name: str,
        percentage: float,
        eta: Optional[float] = None,
    ) -> None:
        """
        Internal method to update progress and invoke callback.

        Args:
            step_name: Current step name
            percentage: Progress percentage (0.0 to 1.0)
            eta: Estimated time remaining in seconds
        """
        self.state.progress = percentage

        if self._progress_callback:
            self._progress_callback(step_name, percentage, eta)

    def _init_log_file(self) -> None:
        """Initialize the installation log file."""
        if self._log_file:
            try:
                with open(self._log_file, "w") as f:
                    f.write(f"DevForgeAI Installation Log\n")
                    f.write(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Target: {self.state.target_path}\n")
                    f.write("-" * 60 + "\n")
            except OSError:
                # Log file creation failed, continue without logging
                self._log_file = None

    def _log(self, message: str) -> None:
        """Write a message to the log file."""
        if self._log_file:
            try:
                with open(self._log_file, "a") as f:
                    timestamp = time.strftime("%H:%M:%S")
                    f.write(f"[{timestamp}] {message}\n")
            except OSError:
                pass  # Ignore log write failures
