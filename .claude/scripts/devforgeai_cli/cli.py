#!/usr/bin/env python3
"""
DevForgeAI CLI - Main Entry Point

Command-line interface for DevForgeAI workflow validators.

Commands:
  validate-dod     Validate Definition of Done completion
  check-git        Check Git repository availability
  validate-context Validate context files exist
  check-hooks      Check if hooks should trigger for an operation
  invoke-hooks     Invoke devforgeai-feedback skill for operation
  ast-grep scan    Semantic code analysis with ast-grep or grep fallback

Based on industry research (SpecDriven AI, pre-commit patterns, DoD checkers).
"""

import sys
import argparse
from pathlib import Path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='devforgeai',
        description='DevForgeAI Workflow Validators',
        epilog='For detailed help: devforgeai <command> --help'
    )

    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # ======================================================================
    # validate-dod command
    # ======================================================================
    dod_parser = subparsers.add_parser(
        'validate-dod',
        help='Validate Definition of Done completion',
        description='Detects autonomous deferrals and validates user approval markers'
    )
    dod_parser.add_argument(
        'story_file',
        help='Path to story file (.story.md)'
    )
    dod_parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    dod_parser.add_argument(
        '--project-root',
        default='.',
        help='Project root directory (default: current directory)'
    )

    # ======================================================================
    # check-git command
    # ======================================================================
    git_parser = subparsers.add_parser(
        'check-git',
        help='Check if directory is a Git repository',
        description='Validates Git availability for DevForgeAI workflows'
    )
    git_parser.add_argument(
        '--directory',
        default='.',
        help='Directory to check (default: current directory)'
    )
    git_parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    # ======================================================================
    # validate-context command
    # ======================================================================
    context_parser = subparsers.add_parser(
        'validate-context',
        help='Validate context files exist',
        description='Checks all 6 DevForgeAI context files are present and non-empty'
    )
    context_parser.add_argument(
        '--directory',
        default='.',
        help='Project root directory (default: current directory)'
    )
    context_parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    # ======================================================================
    # check-hooks command
    # ======================================================================
    hooks_parser = subparsers.add_parser(
        'check-hooks',
        help='Check if hooks should trigger for an operation',
        description='Validates hook configuration and determines trigger status'
    )
    hooks_parser.add_argument(
        '--operation',
        required=True,
        help='Operation name (e.g., dev, qa, release)'
    )
    hooks_parser.add_argument(
        '--status',
        required=True,
        choices=['success', 'failure', 'partial'],
        help='Operation status'
    )
    hooks_parser.add_argument(
        '--config',
        default=None,
        help='Path to hooks.yaml config file (default: devforgeai/config/hooks.yaml)'
    )

    # ======================================================================
    # invoke-hooks command
    # ======================================================================
    invoke_hooks_parser = subparsers.add_parser(
        'invoke-hooks',
        help='Invoke devforgeai-feedback skill for operation',
        description='Extracts operation context and invokes devforgeai-feedback skill for retrospective feedback'
    )
    invoke_hooks_parser.add_argument(
        '--operation',
        required=True,
        help='Operation name (e.g., dev, qa, release)'
    )
    invoke_hooks_parser.add_argument(
        '--story',
        default=None,
        help='Story ID (format: STORY-NNN)'
    )
    invoke_hooks_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    # ======================================================================
    # ast-grep command (STORY-115)
    # ======================================================================
    astgrep_parser = subparsers.add_parser(
        'ast-grep',
        help='Semantic code analysis with ast-grep',
        description='Analyze code using ast-grep patterns or grep fallback'
    )
    astgrep_subparsers = astgrep_parser.add_subparsers(dest='ast_grep_subcommand')

    # ast-grep scan subcommand
    scan_parser = astgrep_subparsers.add_parser(
        'scan',
        help='Scan directory for code violations'
    )
    scan_parser.add_argument(
        'path',
        help='Directory to scan'
    )
    scan_parser.add_argument(
        '--category',
        choices=['security', 'anti-patterns', 'complexity', 'architecture'],
        help='Filter by rule category'
    )
    scan_parser.add_argument(
        '--language',
        choices=['python', 'csharp', 'typescript', 'javascript'],
        help='Filter by language'
    )
    scan_parser.add_argument(
        '--format',
        choices=['text', 'json', 'markdown'],
        default='text',
        help='Output format (default: text)'
    )
    scan_parser.add_argument(
        '--fallback',
        action='store_true',
        help='Force grep fallback mode (skip ast-grep)'
    )

    # Parse arguments
    args = parser.parse_args()

    # Show help if no command specified
    if not args.command:
        parser.print_help()
        return 0

    # Execute command
    try:
        if args.command == 'validate-dod':
            from .validators.dod_validator import validate_dod
            return validate_dod(args.story_file, args.format, args.project_root)

        elif args.command == 'check-git':
            from .validators.git_validator import validate_git
            return validate_git(args.directory, args.format)

        elif args.command == 'validate-context':
            from .validators.context_validator import validate_context
            return validate_context(args.directory, args.format)

        elif args.command == 'check-hooks':
            from .commands.check_hooks import check_hooks_command
            return check_hooks_command(
                operation=args.operation,
                status=args.status,
                config_path=args.config
            )

        elif args.command == 'invoke-hooks':
            from .commands.invoke_hooks import invoke_hooks_command
            return invoke_hooks_command(
                operation=args.operation,
                story_id=args.story,
                verbose=args.verbose
            )

        elif args.command == 'ast-grep':
            if args.ast_grep_subcommand == 'scan':
                from .validators.ast_grep_validator import AstGrepValidator
                from .validators.grep_fallback import GrepFallbackAnalyzer, log_fallback_warning

                validator = AstGrepValidator()

                # Check if we should use fallback mode
                use_fallback = args.fallback or validator.config.get('fallback_mode', False)

                if use_fallback or not validator.is_installed():
                    # Use grep fallback
                    log_fallback_warning()
                    analyzer = GrepFallbackAnalyzer()
                    violations = analyzer.analyze_directory(
                        args.path,
                        category=args.category,
                        language=args.language
                    )
                    output = analyzer.format_results(violations, format=args.format)
                    print(output)
                    return 0 if not violations else 1
                else:
                    # Validate installation and version
                    is_valid, violations = validator.validate(args.path)

                    # For now, just report validation status
                    # Full ast-grep integration will be in future stories
                    if args.format == 'json':
                        import json
                        print(json.dumps({"valid": is_valid, "violations": violations}, indent=2))
                    else:
                        if is_valid:
                            print("✓ ast-grep available and compatible")
                        else:
                            print("✗ ast-grep validation failed:")
                            for v in violations:
                                print(f"  {v['severity']}: {v['error']}")

                    return 0 if is_valid else 1
            else:
                print(f"Unknown ast-grep subcommand: {args.ast_grep_subcommand}", file=sys.stderr)
                return 2

        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 2

    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
