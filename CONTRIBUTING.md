# Contributing to DevForgeAI

Thank you for your interest in contributing to DevForgeAI! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

1. Check [existing issues](https://github.com/bankielewicz/DevForgeAI/issues) to avoid duplicates
2. Open a new issue with:
   - Clear title describing the problem
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (OS, Node.js version, Python version)

### Requesting Features

1. Open an issue with the `enhancement` label
2. Describe the problem the feature solves
3. Explain which framework layer it affects (skills, subagents, rules, CLI, or constitutional files)

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Follow the DevForgeAI workflow (see Development Workflow below)
4. Commit changes (pre-commit hooks validate DoD compliance)
5. Push to your branch (`git push origin feature/your-feature`)
6. Open a Pull Request with a clear description

---

## Development Setup

```bash
# Clone the repository
git clone https://github.com/bankielewicz/DevForgeAI.git
cd DevForgeAI

# Install Node.js dependencies
npm install

# Install Python CLI in development mode
pip install -e .claude/scripts/

# Verify installation
devforgeai-validate --help

# Run tests
npm test                                        # Node.js tests (Jest)
pytest .claude/scripts/devforgeai_cli/tests/    # Python tests
```

### Prerequisites

- **Node.js** >= 18.0.0
- **npm** >= 8.0.0
- **Python** >= 3.10
- **Git**
- **Claude Code Terminal** (for running skills and commands)

---

## Development Workflow

DevForgeAI uses its own framework for development. When contributing:

### 1. Create a Story

```
/create-story [feature-description]
```

This generates a story file with acceptance criteria and technical specifications.

### 2. Develop with TDD

```
/dev STORY-XXX
```

The `/dev` command enforces a 10-phase TDD cycle: Pre-Flight, Red (write failing tests), Green (implement), Refactor, AC Verify, Integration, AC Verify, Deferral, DoD Update, Git, Feedback, Result.

### 3. Validate Quality

```
/qa STORY-XXX deep
```

Quality gates enforce strict coverage thresholds:
- Business Logic: 95%
- Application: 85%
- Infrastructure: 80%

### 4. Commit

Pre-commit hooks validate Definition of Done compliance. Do **not** use `--no-verify` to bypass validation -- fix the issues instead.

---

## Rules for Contributors

- **Context files are immutable** -- The 6 files in `devforgeai/specs/context/` cannot be edited directly. Propose changes via Architecture Decision Records (ADRs) in `devforgeai/specs/adrs/`.
- **TDD is mandatory** -- Write tests before implementation. No exceptions.
- **No `--no-verify` commits** -- Fix validation errors, do not bypass them.
- **No `/tmp/` usage** -- Use `{project-root}/tmp/{story-id}/` for temporary files.
- **Native tools over Bash** -- Use Read/Write/Edit/Glob/Grep instead of cat/echo/sed when working within Claude Code Terminal.

---

## Pull Request Process

1. Ensure all tests pass (`npm test` and `pytest`)
2. Update documentation if your change affects APIs or workflows
3. Fill out the PR template with a clear description of changes
4. Link to the relevant story or issue
5. A maintainer will review your PR and may request changes

---

## Deep Dive

For comprehensive framework internals, architecture details, and advanced contribution patterns, see [DEVELOPER.md](DEVELOPER.md).

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.
