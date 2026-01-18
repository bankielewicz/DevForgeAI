"""
CLAUDE.md Template Variable Detection and Substitution Module

Handles detection and substitution of framework template variables:
- {{PROJECT_NAME}}: Auto-detected from git remote or directory name
- {{PROJECT_PATH}}: Project directory path
- {{PYTHON_VERSION}}: Python version from python3 --version
- {{PYTHON_PATH}}: Path to python3 from which python3
- {{TECH_STACK}}: Detected from package.json, requirements.txt, or *.csproj
- {{INSTALLATION_DATE}}: ISO 8601 format date
- {{FRAMEWORK_VERSION}}: From version.json or hardcoded
"""

import re
import subprocess
import json
from pathlib import Path
from datetime import date
from typing import Dict, Optional


# Constants for subprocess operations
PYTHON_VERSION_TIMEOUT = 5
SUBPROCESS_TIMEOUT = 5
DEFAULT_PYTHON_PATH = "/usr/bin/python3"
DEFAULT_FRAMEWORK_VERSION = "1.0.1"
DEFAULT_PYTHON_VERSION = "Python 3.8+"

# Tech stack detection file patterns
TECH_STACK_PATTERNS = {
    "package.json": "Node.js",
    "requirements.txt": "Python",
}


def _extract_git_repo_name(git_config_path: Path) -> Optional[str]:
    """
    Extract repository name from git config.

    Args:
        git_config_path: Path to .git/config file

    Returns:
        Repository name (without .git), or None if not found
    """
    try:
        config_content = git_config_path.read_text()
        match = re.search(r'url = .*?/([^/]+?)(?:\.git)?$', config_content, re.MULTILINE)
        return match.group(1) if match else None
    except (OSError, IOError):
        return None


def _run_subprocess_command(command: list[str], timeout: int) -> Optional[str]:
    """
    Run a subprocess command safely.

    Args:
        command: List of command arguments
        timeout: Timeout in seconds

    Returns:
        stdout + stderr combined, or None on error

    Raises:
        No exceptions - returns None on any error for robustness
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            output = result.stdout + result.stderr
            return output.strip() if output else None
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return None


class TemplateVariableDetector:
    """Detects and substitutes framework template variables in CLAUDE.md."""

    # Pattern for framework variables (uppercase + underscores only)
    FRAMEWORK_VAR_PATTERN = r'\{\{[A-Z_]+\}\}'

    # List of supported framework variables
    FRAMEWORK_VARIABLES = {
        'PROJECT_NAME',
        'PROJECT_PATH',
        'PYTHON_VERSION',
        'PYTHON_PATH',
        'TECH_STACK',
        'INSTALLATION_DATE',
        'FRAMEWORK_VERSION'
    }

    def __init__(self, project_path: Path):
        """Initialize detector with project path."""
        self.project_path = Path(project_path)
        self.detected_variables = {}
        self.substituted_count = 0

        # Pre-detect and cache variables for property access
        self._project_name = None
        self._python_version = None
        self._python_path = None
        self._tech_stack = None
        self._installation_date = None
        self._framework_version = None

    def detect_variables(self, template_content: str) -> Dict[str, str]:
        """
        Find all framework variables in template content.

        Returns:
            Dictionary mapping variable names (without braces) to detected pattern.
        """
        variables = {}
        matches = re.findall(self.FRAMEWORK_VAR_PATTERN, template_content)

        for match in matches:
            # Extract variable name from {{VAR}} -> VAR
            var_name = match[2:-2]
            if var_name in self.FRAMEWORK_VARIABLES:
                variables[var_name] = match

        # Return unique variables
        return {k: v for k, v in variables.items()}

    def auto_detect_project_name(self) -> str:
        """
        Auto-detect PROJECT_NAME from git remote or directory name.

        Returns:
            Project name (repository name or directory name).
        """
        git_config = self.project_path / ".git" / "config"
        if git_config.exists():
            repo_name = _extract_git_repo_name(git_config)
            if repo_name:
                return repo_name

        # Fallback to directory name
        return self.project_path.name

    def auto_detect_python_version(self) -> str:
        """
        Auto-detect PYTHON_VERSION from 'python3 --version' command.

        Returns:
            Python version string (e.g., "Python 3.10.11").
        """
        version = _run_subprocess_command(['python3', '--version'], PYTHON_VERSION_TIMEOUT)
        return version if version else DEFAULT_PYTHON_VERSION

    def auto_detect_python_path(self) -> str:
        """
        Auto-detect PYTHON_PATH from 'which python3' command.

        Returns:
            Absolute path to python3 executable.
        """
        path = _run_subprocess_command(['which', 'python3'], SUBPROCESS_TIMEOUT)
        return path if path else DEFAULT_PYTHON_PATH

    def auto_detect_tech_stack(self, project_path: Optional[Path] = None) -> str:
        """
        Auto-detect TECH_STACK from presence of config files.

        Checks for:
        - package.json → Node.js
        - requirements.txt → Python
        - *.csproj → .NET

        Returns:
            Tech stack name.
        """
        if project_path is None:
            project_path = self.project_path

        project_path = Path(project_path)

        # Check for known tech stack patterns
        for filename, tech_name in TECH_STACK_PATTERNS.items():
            if (project_path / filename).exists():
                return tech_name

        # Check for .NET
        if list(project_path.glob("*.csproj")):
            return ".NET"

        return "Mixed"

    def auto_detect_installation_date(self) -> str:
        """
        Auto-detect INSTALLATION_DATE in ISO 8601 format.

        Returns:
            Date string (YYYY-MM-DD).
        """
        return date.today().isoformat()

    def auto_detect_framework_version(self) -> str:
        """
        Auto-detect FRAMEWORK_VERSION from version file or hardcoded.

        Returns:
            Version string (e.g., "1.0.1").
        """
        version_file = self.project_path / "devforgeai" / "version.json"
        if not version_file.exists():
            return DEFAULT_FRAMEWORK_VERSION

        try:
            with open(version_file, 'r', encoding='utf-8') as f:
                version_data = json.load(f)
                return version_data.get('version', DEFAULT_FRAMEWORK_VERSION)
        except (json.JSONDecodeError, IOError, OSError):
            return DEFAULT_FRAMEWORK_VERSION

    def get_all_variables(self) -> Dict[str, str]:
        """
        Get all framework variables with auto-detected values.

        Returns:
            Dictionary mapping variable names to their values.
        """
        variables = {
            'PROJECT_NAME': self.auto_detect_project_name(),
            'PROJECT_PATH': str(self.project_path),
            'PYTHON_VERSION': self.auto_detect_python_version(),
            'PYTHON_PATH': self.auto_detect_python_path(),
            'TECH_STACK': self.auto_detect_tech_stack(),
            'INSTALLATION_DATE': self.auto_detect_installation_date(),
            'FRAMEWORK_VERSION': self.auto_detect_framework_version()
        }

        self.detected_variables = variables
        return variables

    def _substitute_variable(self, template: str, var_name: str, var_value: str) -> tuple[str, int]:
        """
        Replace a single framework variable pattern in template.

        Args:
            template: Template content to process
            var_name: Variable name (e.g., 'PROJECT_NAME')
            var_value: Value to substitute

        Returns:
            Tuple of (modified template, count of substitutions)
        """
        var_pattern = f"{{{{{var_name}}}}}"
        occurrences = template.count(var_pattern)

        if occurrences > 0:
            template = template.replace(var_pattern, var_value)

        return template, occurrences

    def substitute_variables(self, template: str, variables: Optional[Dict[str, str]] = None) -> str:
        """
        Replace {{VAR}} patterns with values.

        Substitutes only framework variables. User variables like {{MY_VAR}} are preserved.

        Args:
            template: Template content with {{VAR}} patterns.
            variables: Dictionary mapping variable names to values.
                      If None, auto-detects all variables.

        Returns:
            Template content with substitutions applied.
        """
        if variables is None:
            variables = self.get_all_variables()

        result = template
        self.substituted_count = 0

        # Only substitute framework variables
        for var_name in self.FRAMEWORK_VARIABLES:
            if var_name in variables:
                result, occurrences = self._substitute_variable(result, var_name, variables[var_name])
                self.substituted_count += occurrences

        return result

    def get_substitution_report(self) -> str:
        """
        Get summary report of variable detection and substitution.

        Returns:
            Report string like "7 variables detected, N substituted (X%)".
        """
        detected_count = len(self.detected_variables) or len(self.FRAMEWORK_VARIABLES)
        percentage = (self.substituted_count * 100 // detected_count) if detected_count > 0 else 0

        return f"{detected_count} variables detected, {self.substituted_count} substituted ({percentage}%)"

    # Properties for direct access to detected variables
    @property
    def project_name(self) -> str:
        """Get auto-detected project name."""
        if self._project_name is None:
            self._project_name = self.auto_detect_project_name()
        return self._project_name

    @property
    def python_version(self) -> str:
        """Get auto-detected python version."""
        if self._python_version is None:
            self._python_version = self.auto_detect_python_version()
        return self._python_version

    @property
    def python_path(self) -> str:
        """Get auto-detected python path."""
        if self._python_path is None:
            self._python_path = self.auto_detect_python_path()
        return self._python_path

    @property
    def tech_stack(self) -> str:
        """Get auto-detected tech stack."""
        if self._tech_stack is None:
            self._tech_stack = self.auto_detect_tech_stack()
        return self._tech_stack

    @property
    def installation_date(self) -> str:
        """Get installation date."""
        if self._installation_date is None:
            self._installation_date = self.auto_detect_installation_date()
        return self._installation_date

    @property
    def framework_version(self) -> str:
        """Get auto-detected framework version."""
        if self._framework_version is None:
            self._framework_version = self.auto_detect_framework_version()
        return self._framework_version
