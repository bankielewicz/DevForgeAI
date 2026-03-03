# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-03

### Added

- **Core Framework**
  - 44 specialized subagents for architecture, testing, QA, security, documentation, and more
  - 26 inline skills covering the full software development lifecycle
  - 46 slash commands from `/brainstorm` through `/release`
  - 6 constitutional context files (tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns)
  - 4 sequential quality gates blocking progression until standards are met

- **TDD Workflow (`/dev`)**
  - 10-phase development cycle with mandatory Red-Green-Refactor
  - Phase 04.5 and 05.5 AC compliance verification
  - Test folder write protection (only authorized agents in designated phases)
  - Coverage thresholds: 95% business logic, 85% application, 80% infrastructure

- **Configuration Layer Alignment Protocol (CLAP)**
  - 15 validation checks across contradiction, completeness, and ADR propagation categories
  - `/audit-alignment` command for on-demand validation

- **Hook-Based Phase Enforcement (EPIC-086, Sprint 22)**
  - STORY-525: Phase Steps Registry with 72 steps across 12 phases
  - STORY-526: SubagentStop hook for automatic invocation tracking
  - STORY-527: TaskCompleted hook for step validation gates
  - Eliminates undetected phase skipping through automated validation

- **Root Cause Analysis System**
  - `/rca` command with 5 Whys methodology
  - diagnostic-analyst subagent for cross-reference investigation
  - `/create-stories-from-rca` for converting findings into actionable stories

- **Feedback System**
  - 7 commands for capture, search, export, import, and reindex
  - AI analysis and observation extraction from subagent outputs

- **Sprint Planning**
  - `/create-sprint` with automated story selection and capacity planning
  - Dependency graph analysis with cycle detection

- **Cross-AI Collaboration**
  - `/collaborate` generates portable documents for sharing with external LLMs

- **CLI Validation Tools**
  - `devforgeai-validate` Python CLI for phase management, DoD validation, and story checks
  - Pre-commit hook integration for commit-time validation

- **Documentation**
  - API reference (docs/api/API.md)
  - Architecture guide (docs/architecture/ARCHITECTURE.md)
  - Troubleshooting guide (docs/guides/TROUBLESHOOTING.md)
  - Developer guide (DEVELOPER.md)

[1.0.0]: https://github.com/bankielewicz/DevForgeAI/releases/tag/v1.0.0
