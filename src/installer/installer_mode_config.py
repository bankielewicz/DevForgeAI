"""
STORY-243: Installer Mode Configuration Module

This module provides installer mode configuration for different installation
experiences: CLI, Wizard, Silent, and GUI.

Implements:
- InstallerStep: Single step in wizard installation flow
- InstallableComponent: Component available for selective installation
- InstallerModeResult: Holds generated installer mode configuration
- InstallerModeConfig: Service for generating mode-specific configurations
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import platform
import yaml


@dataclass
class InstallerStep:
    """
    Single step in wizard installation flow.

    Technical Spec fields:
    - id: String (Required, unique)
    - title: String (Required)
    - type: String (Enum: info, license, path_select, component_select, progress, complete)
    - validation: Optional[String]
    - can_skip: Bool (Default: false)
    """
    id: str
    title: str
    type: str
    validation: Optional[str] = None
    can_skip: bool = False


@dataclass
class InstallableComponent:
    """
    Component available for selective installation.

    Technical Spec fields:
    - id: String (Required, unique)
    - name: String (Required)
    - description: String (Required)
    - size_bytes: Int (Positive)
    - required: Bool (Default: false)
    - default_selected: Bool (Default: true)
    - files: List[String] (Glob patterns)
    """
    id: str
    name: str
    description: str
    size_bytes: int
    required: bool = False
    default_selected: bool = True
    files: List[str] = field(default_factory=list)


@dataclass
class InstallerModeResult:
    """
    Holds generated installer mode configuration.

    Technical Spec fields:
    - mode: String (Required, Enum: cli, wizard, gui, silent)
    - config_path: String (Required, path to generated installer-config.yaml)
    - steps: List[InstallerStep] (For wizard mode)
    - prompts: List (For cli mode)
    - silent_config_schema: Dict[str, Any] (For silent mode)
    - gui_layout: Dict[str, Any] (For gui mode)
    - post_install_actions: List (Optional)
    - components: List[InstallableComponent] (Required)
    """
    mode: str
    config_path: str
    steps: List[InstallerStep] = field(default_factory=list)
    prompts: List[Dict[str, Any]] = field(default_factory=list)
    silent_config_schema: Dict[str, Any] = field(default_factory=dict)
    gui_layout: Dict[str, Any] = field(default_factory=dict)
    post_install_actions: List[Dict[str, Any]] = field(default_factory=list)
    components: List[InstallableComponent] = field(default_factory=list)


class InstallerModeConfig:
    """
    Service for generating installer mode configurations.

    Supports 4 installation modes:
    - cli: Interactive command-line installation
    - wizard: Step-by-step guided installation
    - silent: Automated CI/CD installation
    - gui: Graphical desktop installation

    Usage:
        config = InstallerModeConfig(Path("/path/to/project"))
        result = config.configure(mode="wizard")
    """

    # Valid installation modes
    VALID_MODES = {"cli", "wizard", "silent", "gui"}

    # Standard 6 wizard steps (BR-001)
    WIZARD_STEPS = [
        InstallerStep(id="welcome", title="Welcome", type="info", validation=None, can_skip=False),
        InstallerStep(id="license", title="License Agreement", type="license", validation="accept_required", can_skip=False),
        InstallerStep(id="path", title="Installation Path", type="path_select", validation="path_writable", can_skip=False),
        InstallerStep(id="components", title="Component Selection", type="component_select", validation=None, can_skip=True),
        InstallerStep(id="install", title="Installing", type="progress", validation=None, can_skip=False),
        InstallerStep(id="complete", title="Complete", type="complete", validation=None, can_skip=False),
    ]

    # Default components per story Notes
    DEFAULT_COMPONENTS = [
        InstallableComponent(
            id="core",
            name="Core Framework",
            description="Essential .claude/ and devforgeai/ files",
            size_bytes=1024000,
            required=True,  # BR-003: Core is always required
            default_selected=True,
            files=[".claude/**/*", "devforgeai/**/*"]
        ),
        InstallableComponent(
            id="cli",
            name="CLI Tools",
            description="Command-line utilities",
            size_bytes=512000,
            required=False,
            default_selected=True,
            files=["bin/*", "scripts/*"]
        ),
        InstallableComponent(
            id="templates",
            name="Templates",
            description="Project templates and examples",
            size_bytes=256000,
            required=False,
            default_selected=False,
            files=["templates/**/*"]
        ),
        InstallableComponent(
            id="examples",
            name="Examples",
            description="Sample projects",
            size_bytes=128000,
            required=False,
            default_selected=False,
            files=["examples/**/*"]
        ),
    ]

    def __init__(self, project_dir: Path):
        """
        Initialize InstallerModeConfig.

        Args:
            project_dir: Path to the project directory
        """
        self.project_dir = Path(project_dir)
        self._config_path: Optional[Path] = None

    def configure(
        self,
        mode: str,
        post_install_actions: Optional[List[Dict[str, Any]]] = None
    ) -> InstallerModeResult:
        """
        Generate installer configuration for the specified mode.

        Args:
            mode: Installation mode (cli, wizard, silent, gui)
            post_install_actions: Optional list of post-installation actions

        Returns:
            InstallerModeResult with mode-specific configuration

        Raises:
            ValueError: If mode is not valid
            KeyError: If mode is not recognized
        """
        if mode not in self.VALID_MODES:
            raise ValueError(f"Invalid mode: {mode}. Valid modes: {self.VALID_MODES}")

        # Initialize result with common fields
        components = self._get_components()
        actions = self._process_post_install_actions(post_install_actions or [])

        # Generate config file
        config_path = self._generate_config_file(mode, components, actions)

        # Build mode-specific result
        if mode == "cli":
            return self._configure_cli_mode(config_path, components, actions)
        elif mode == "wizard":
            return self._configure_wizard_mode(config_path, components, actions)
        elif mode == "silent":
            return self._configure_silent_mode(config_path, components, actions)
        elif mode == "gui":
            return self._configure_gui_mode(config_path, components, actions)
        else:
            raise KeyError(f"Unhandled mode: {mode}")

    def _get_components(self) -> List[InstallableComponent]:
        """Get default components, ensuring core is always required (BR-003)."""
        components = []
        for comp in self.DEFAULT_COMPONENTS:
            # Create new instance to avoid modifying class defaults
            new_comp = InstallableComponent(
                id=comp.id,
                name=comp.name,
                description=comp.description,
                size_bytes=comp.size_bytes,
                required=comp.required,
                default_selected=comp.default_selected,
                files=list(comp.files)
            )
            # BR-003: Core component must always be required
            if new_comp.id == "core":
                new_comp.required = True
                new_comp.default_selected = True
            components.append(new_comp)
        return components

    def _process_post_install_actions(
        self,
        actions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Process and validate post-install actions (BR-004: preserve order)."""
        processed = []
        for action in actions:
            if isinstance(action, dict):
                # Keep original order (BR-004)
                processed.append(action)
        return processed

    def _get_default_install_path(self) -> str:
        """Get platform-specific default installation path."""
        system = platform.system().lower()
        if system == "windows":
            return "C:\\Program Files\\DevForgeAI"
        elif system == "darwin":
            return "/usr/local/devforgeai"
        else:
            return "/opt/devforgeai"

    def _generate_config_file(
        self,
        mode: str,
        components: List[InstallableComponent],
        post_install_actions: List[Dict[str, Any]]
    ) -> str:
        """
        Generate installer-config.yaml file (SVC-007).

        The generated YAML includes documentation comments (NFR-004).
        """
        config_path = self.project_dir / "installer-config.yaml"

        # Build config dict
        config = {
            "installation": {
                "mode": mode,
                "target": {
                    "path": self._get_default_install_path(),
                    "create_if_missing": True
                },
                "components": [comp.id for comp in components if comp.default_selected],
                "post_install": post_install_actions
            }
        }

        # Add mode-specific sections
        if mode == "cli":
            config["cli"] = {
                "progress": {"type": "spinner", "color": True},
                "colors": {"enabled": True, "success": "green", "error": "red", "warning": "yellow"},
                "help": {"enabled": True, "usage_examples": True}
            }
        elif mode == "wizard":
            config["wizard"] = {
                "navigation": {"next": True, "back": True, "cancel": True},
                "progress": {"show_step_count": True, "show_percentage": True},
                "buttons": {"next": "Next >", "back": "< Back", "cancel": "Cancel", "finish": "Finish"}
            }
        elif mode == "silent":
            config["silent"] = {
                "exit_codes": {"success": 0, "error": 1, "validation_failed": 2, "cancelled": 3},
                "logging": {"enabled": True, "file": "install.log", "level": "INFO"}
            }
        elif mode == "gui":
            config["gui"] = {
                "window": {"width": 800, "height": 600, "resizable": True},
                "components": {"checkboxes": True, "component_selection": True},
                "browse": {"dialog": True, "path_selection": True},
                "progress": {"bar": True, "cancel_button": True}
            }

        # Generate YAML with comments (NFR-004)
        yaml_content = self._generate_yaml_with_comments(config, mode)

        # Write to file
        config_path.write_text(yaml_content, encoding="utf-8")

        return str(config_path)

    def _generate_yaml_with_comments(self, config: Dict, mode: str) -> str:
        """Generate YAML content with documentation comments."""
        lines = [
            "# DevForgeAI Installer Configuration",
            f"# Mode: {mode}",
            "# Generated by InstallerModeConfig (STORY-243)",
            "#",
            "# This file configures the installation behavior.",
            "# Edit settings below to customize the installation process.",
            "",
        ]

        # Add mode-specific header comments
        if mode == "wizard":
            lines.extend([
                "# Wizard Mode: Step-by-step guided installation",
                "# Steps: Welcome -> License -> Path -> Components -> Install -> Complete",
                "",
            ])
        elif mode == "cli":
            lines.extend([
                "# CLI Mode: Interactive command-line installation",
                "# Features: Progress spinner, colored output, help text",
                "",
            ])
        elif mode == "silent":
            lines.extend([
                "# Silent Mode: Automated CI/CD installation",
                "# No prompts - all settings from this config file",
                "# Exit codes indicate success/failure",
                "",
            ])
        elif mode == "gui":
            lines.extend([
                "# GUI Mode: Graphical desktop installation",
                "# Features: Browse dialog, component checkboxes, progress bar",
                "",
            ])

        # Dump YAML
        yaml_content = yaml.dump(config, default_flow_style=False, sort_keys=False)
        lines.append(yaml_content)

        return "\n".join(lines)

    def _configure_cli_mode(
        self,
        config_path: str,
        components: List[InstallableComponent],
        post_install_actions: List[Dict[str, Any]]
    ) -> InstallerModeResult:
        """Configure CLI mode with prompts and progress indicators (AC#1)."""
        prompts = [
            {"name": "install_path", "prompt": "Enter installation path:", "type": "text", "default": self._get_default_install_path()},
            {"name": "components", "prompt": "Select components to install:", "type": "multiselect", "help": "Use arrow keys to select"},
            {"name": "confirm", "prompt": "Proceed with installation?", "type": "confirm", "default": True}
        ]

        return InstallerModeResult(
            mode="cli",
            config_path=config_path,
            steps=[],  # CLI doesn't use steps
            prompts=prompts,
            silent_config_schema={},
            gui_layout={},
            post_install_actions=post_install_actions,
            components=components
        )

    def _configure_wizard_mode(
        self,
        config_path: str,
        components: List[InstallableComponent],
        post_install_actions: List[Dict[str, Any]]
    ) -> InstallerModeResult:
        """Configure Wizard mode with 6 standard steps (AC#2, BR-001)."""
        # BR-001: Wizard mode must have exactly 6 standard steps
        # Reuse WIZARD_STEPS class constant (DRY principle)
        steps = list(self.WIZARD_STEPS)

        return InstallerModeResult(
            mode="wizard",
            config_path=config_path,
            steps=steps,
            prompts=[],  # Wizard uses steps, not prompts
            silent_config_schema={},
            gui_layout={},
            post_install_actions=post_install_actions,
            components=components
        )

    def _configure_silent_mode(
        self,
        config_path: str,
        components: List[InstallableComponent],
        post_install_actions: List[Dict[str, Any]]
    ) -> InstallerModeResult:
        """Configure Silent mode with schema and exit codes (AC#3, BR-002)."""
        # BR-002: Silent mode must not prompt for any input
        silent_config_schema = {
            "install_path": {
                "type": "string",
                "required": True,
                "description": "Installation directory path"
            },
            "components": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of component IDs to install"
            },
            "post_install": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Post-installation actions to execute"
            },
            "logging": {
                "type": "object",
                "properties": {
                    "level": {"type": "string", "enum": ["DEBUG", "INFO", "WARNING", "ERROR"]},
                    "file": {"type": "string"}
                }
            }
        }

        return InstallerModeResult(
            mode="silent",
            config_path=config_path,
            steps=[],
            prompts=[],  # BR-002: No prompts in silent mode
            silent_config_schema=silent_config_schema,
            gui_layout={},
            post_install_actions=post_install_actions,
            components=components
        )

    def _configure_gui_mode(
        self,
        config_path: str,
        components: List[InstallableComponent],
        post_install_actions: List[Dict[str, Any]]
    ) -> InstallerModeResult:
        """Configure GUI mode with window layout and controls (AC#4)."""
        gui_layout = {
            "window": {
                "width": 800,
                "height": 600,
                "title": "DevForgeAI Installer",
                "resizable": True,
                "centered": True
            },
            "component_selection": {
                "type": "checkbox_list",
                "checkboxes": True,
                "show_size": True,
                "show_description": True
            },
            "path_selection": {
                "type": "input_with_browse",
                "browse_button": True,
                "dialog": "folder_select"
            },
            "progress": {
                "type": "progress_bar",
                "bar": True,
                "percentage": True,
                "cancel_button": True
            },
            "buttons": {
                "install": {"text": "Install", "style": "primary"},
                "cancel": {"text": "Cancel", "style": "secondary"},
                "browse": {"text": "Browse...", "style": "default"}
            }
        }

        return InstallerModeResult(
            mode="gui",
            config_path=config_path,
            steps=[],
            prompts=[],
            silent_config_schema={},
            gui_layout=gui_layout,
            post_install_actions=post_install_actions,
            components=components
        )
