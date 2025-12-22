"""
DevForgeAI Installer CLI Entry Point.

This module enables running the installer as a Python module:
    python -m installer install /path/to/project

This solves the relative import issue when running install.py directly.
"""

import sys
import json
from pathlib import Path

from . import install as install_module


def main():
    """
    Parse CLI arguments and invoke the installer.

    Usage:
        python -m installer install <target_path> [--force]
        python -m installer validate <target_path>
        python -m installer rollback <target_path>
        python -m installer uninstall <target_path>
    """
    args = sys.argv[1:]

    if not args or args[0] in ('--help', '-h'):
        print("""DevForgeAI Installer

Usage:
    python -m installer install <target_path> [--force]
    python -m installer validate <target_path>
    python -m installer rollback <target_path>
    python -m installer uninstall <target_path>

Commands:
    install     Install or upgrade DevForgeAI to target directory
    validate    Validate existing installation
    rollback    Restore previous version from backup
    uninstall   Remove DevForgeAI from target directory

Options:
    --force     Skip confirmation prompts
    --help, -h  Show this help message

Examples:
    python -m installer install .
    python -m installer install /path/to/project --force
    python -m installer validate .
""")
        sys.exit(0)

    # Parse command
    command = args[0]

    # Check for valid command
    valid_commands = ['install', 'validate', 'rollback', 'uninstall']
    if command not in valid_commands:
        print(f"Error: Unknown command '{command}'")
        print(f"Valid commands: {', '.join(valid_commands)}")
        print("Run 'python -m installer --help' for usage.")
        sys.exit(1)

    # Parse target path (required for all commands)
    if len(args) < 2:
        print(f"Error: {command} requires a target path")
        print(f"Usage: python -m installer {command} <target_path>")
        sys.exit(1)

    target_path = Path(args[1]).resolve()

    # Parse options
    force = '--force' in args

    # Execute command
    try:
        if command == 'install':
            result = install_module.install(target_path, force=force)
        elif command == 'validate':
            result = install_module.install(target_path, mode='validate')
        elif command == 'rollback':
            result = install_module.install(target_path, mode='rollback')
        elif command == 'uninstall':
            result = install_module.install(target_path, mode='uninstall')

        # Display result
        status = result.get('status', 'unknown')

        # Print messages
        for msg in result.get('messages', []):
            print(msg)

        # Print warnings
        for warn in result.get('warnings', []):
            print(f"⚠️  {warn}")

        # Print errors
        for err in result.get('errors', []):
            print(f"❌ {err}")

        # Exit code based on status
        if status == 'success':
            sys.exit(0)
        elif status == 'rollback':
            print("Installation was rolled back due to errors.")
            sys.exit(2)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"❌ Installer error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
