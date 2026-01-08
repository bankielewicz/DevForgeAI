"""
STORY-243: Installer Mode Configuration Module - Test Configuration

Pytest configuration for the installer_mode_config test suite.
"""

import sys
from pathlib import Path

# Add project root to Python path for installer module imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
