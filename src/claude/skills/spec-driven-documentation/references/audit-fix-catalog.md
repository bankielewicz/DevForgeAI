# Audit Fix Catalog

## Fix Mode Classification

| Fix Mode | Description | User Interaction |
|----------|-------------|------------------|
| `automated` | Deterministic, safe to apply without review | None (applied silently) |
| `interactive` | Requires judgment or user preference | Per-fix approval prompt |

## Fix Actions by Finding Type

### License Fixes

| Finding Type | Fix Action | Fix Mode | Description |
|-------------|------------|----------|-------------|
| `license:missing` | `create_dual_license` | interactive | Create LICENSE-MIT and LICENSE-APACHE files |
| `license:mismatch` | `sync_license` | interactive | Update docs to match manifest license field |

### Community File Fixes

| Finding Type | Fix Action | Fix Mode | Description |
|-------------|------------|----------|-------------|
| `community:contributing` | `create_contributing` | automated | Create CONTRIBUTING.md from template |
| `community:coc` | `create_coc` | interactive | Create CODE_OF_CONDUCT.md (Contributor Covenant) |
| `community:security` | `create_security` | interactive | Create SECURITY.md with disclosure policy |
| `community:issue_templates` | `create_issue_templates` | automated | Create .github/ISSUE_TEMPLATE/ |
| `community:pr_template` | `create_pr_template` | automated | Create .github/PULL_REQUEST_TEMPLATE.md |

### Tone Fixes

| Finding Type | Fix Action | Fix Mode | Description |
|-------------|------------|----------|-------------|
| `tone:no_why` | `rewrite_opening` | interactive | Rewrite README opening with value proposition |
| `tone:no_pronouns` | `add_pronouns` | interactive | Suggest human pronoun replacements |
| `tone:gatekeeping` | `soften_language` | interactive | Suggest welcoming language alternatives |

### Formatting Fixes

| Finding Type | Fix Action | Fix Mode | Description |
|-------------|------------|----------|-------------|
| `formatting:missing_badges` | `insert_badges` | automated | Insert standard badges after first heading |
| `formatting:no_admonitions` | `suggest_admonitions` | interactive | Suggest where to add GFM admonitions |
| `formatting:oversized` | `split_file` | interactive | Recommend splitting oversized file |
| `formatting:no_changelog_cats` | `add_changelog_cats` | automated | Add Keep a Changelog categories |

### Architecture Fixes

| Finding Type | Fix Action | Fix Mode | Description |
|-------------|------------|----------|-------------|
| `architecture:orphan` | `add_cross_reference` | interactive | Add link from related doc to orphaned file |
| `architecture:duplicate` | `merge_duplicates` | interactive | Suggest merging duplicate-named files |
| `architecture:no_index` | `create_docs_index` | automated | Create docs/README.md navigation index |

### Onboarding Fixes

| Finding Type | Fix Action | Fix Mode | Description |
|-------------|------------|----------|-------------|
| `onboarding:no_install` | `add_install_steps` | interactive | Generate install steps from manifest |
| `onboarding:no_quickstart` | `add_quickstart` | interactive | Generate Quick Start section |
| `onboarding:config_mismatch` | `sync_config` | automated | Sync version/MSRV between manifest and docs |

## Template Variables

Templates for file creation use these variables:

| Variable | Resolution Source | Fallback |
|----------|-------------------|----------|
| `{{project_name}}` | package.json name, Cargo.toml [package].name | Directory name |
| `{{version}}` | Manifest version field | "0.1.0" |
| `{{license}}` | Manifest license field | AskUserQuestion |
| `{{repo_url}}` | `git remote get-url origin` | AskUserQuestion |
| `{{test_command}}` | Detect from scripts/Makefile | "npm test" / "cargo test" |
| `{{lint_command}}` | Detect from scripts/Makefile | "npm run lint" |
| `{{format_command}}` | Detect from scripts/Makefile | "npm run format" |
| `{{msrv}}` | rust-toolchain.toml, engines field | AskUserQuestion |
| `{{contact_email}}` | N/A | AskUserQuestion |
| `{{description}}` | Manifest description field | AskUserQuestion |

## Badge Templates

Standard badges for `insert_badges` action:

```markdown
[![CI]({{repo_url}}/actions/workflows/ci.yml/badge.svg)]({{repo_url}}/actions/workflows/ci.yml)
[![License: {{license}}](https://img.shields.io/badge/License-{{license}}-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-{{version}}-green.svg)](CHANGELOG.md)
```

## CONTRIBUTING.md Template

```markdown
# Contributing to {{project_name}}

We welcome contributions! Here's how to get started.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone {{repo_url}}`
3. Create a branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Run tests: `{{test_command}}`
6. Run linting: `{{lint_command}}`
7. Commit and push
8. Open a Pull Request

## Development Setup

```bash
# Install dependencies
{{install_command}}

# Run tests
{{test_command}}

# Run linter
{{lint_command}}
```

## Code Style

- Run `{{format_command}}` before committing
- Follow the existing code style
- Write tests for new features

## Reporting Bugs

Use the [bug report template]({{repo_url}}/issues/new?template=bug_report.md).

## Suggesting Features

Use the [feature request template]({{repo_url}}/issues/new?template=feature_request.md).
```
