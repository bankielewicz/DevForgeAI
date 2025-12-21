---
id: EPIC-018
title: ast-grep Foundation & Core Rules
business-value: Improve code analysis accuracy from 60-75% to 90-95%+ through semantic AST-based analysis
status: Planning
priority: High
complexity-score: 21
architecture-tier: Tier 2
created: 2025-12-08
estimated-points: 30
target-sprints: 3-4
---

# EPIC-018: ast-grep Foundation & Core Rules

## Business Goal

Integrate ast-grep as a semantic code analysis engine into DevForgeAI framework to replace grep-based pattern matching with AST-aware queries, improving detection accuracy by 15-30%.

**Success Metrics:**
- Security detection accuracy: 70% → 95% (+25%)
- False positive rate: 30% → <10% (-20%)
- Rule coverage: 20 patterns → 25+ rules (+5 initially, 100+ total across all epics)
- Analysis performance: <10s for 1000 files (accuracy priority, performance secondary)

## Features

### Feature 1: CLI Validator Foundation
**Description:** Create DevForgeAI CLI validator that wraps ast-grep, handles installation detection, and provides graceful fallback to grep-based analysis when ast-grep unavailable.

**User Stories (high-level):**
1. As a DevForgeAI user, I want ast-grep automatically installed via PyPI so that I don't need manual setup
2. As a DevForgeAI user, I want interactive prompts when ast-grep is missing so that I can choose install/fallback/skip
3. As a DevForgeAI developer, I want graceful fallback to grep so that workflows continue even without ast-grep

**Estimated Effort:** Medium (8-10 story points)

### Feature 2: Configuration Infrastructure
**Description:** Establish ast-grep rule storage, sgconfig.yml configuration, language mappings, and directory structure following DevForgeAI conventions.

**User Stories (high-level):**
1. As a DevForgeAI maintainer, I want rules stored in `devforgeai/ast-grep/rules/` so that they are project-scoped
2. As a rule author, I want language-specific directories (python/, csharp/, typescript/) so that rules are organized
3. As a DevForgeAI user, I want sgconfig.yml auto-generated so that configuration is consistent

**Estimated Effort:** Small (5-7 story points)

### Feature 3: Core Security Rules
**Description:** Create 5 CRITICAL severity security rules covering SQL injection, XSS, hardcoded secrets, eval usage, and insecure deserialization for Python, C#, and TypeScript.

**User Stories (high-level):**
1. As a developer, I want SQL injection detection so that parameterized queries are enforced
2. As a security engineer, I want hardcoded secrets detected so that environment variables are used
3. As a developer, I want XSS vulnerabilities flagged so that innerHTML usage is validated

**Estimated Effort:** Medium (7-9 story points)

### Feature 4: Core Anti-pattern Rules
**Description:** Create 10 HIGH/MEDIUM severity anti-pattern rules covering god objects, async void, console.log in production, magic numbers, long methods, and nested conditionals.

**User Stories (high-level):**
1. As a code reviewer, I want god objects detected so that classes stay focused (<500 lines)
2. As a .NET developer, I want async void violations flagged so that proper async Task is used
3. As a maintainer, I want console.log in production code detected so that proper logging is enforced

**Estimated Effort:** Medium (7-9 story points)

### Feature 5: Output Format
**Description:** Implement JSON, text, and markdown output formats for ast-grep violations compatible with DevForgeAI QA reporting and severity mapping (CRITICAL/HIGH/MEDIUM/LOW).

**User Stories (high-level):**
1. As a QA skill, I want JSON output so that I can parse violations programmatically
2. As a CLI user, I want human-readable text output so that I can review violations quickly
3. As a documentation generator, I want markdown reports so that violations integrate with QA reports

**Estimated Effort:** Small (3-5 story points)

## Stories

| Story ID | Feature # | Title | Points | Status |
|----------|-----------|-------|--------|--------|
| STORY-115 | 1 | CLI Validator Foundation - ast-grep Integration | 8 | Backlog |
| STORY-116 | 2 | Configuration Infrastructure - ast-grep Rule Storage | 5 | Backlog |
| STORY-117 | 3 | Core Security Rules - CRITICAL Severity Detection | 8 | Backlog |
| STORY-118 | 4 | Core Anti-pattern Rules - Code Quality Detection | 8 | Backlog |
| STORY-119 | 5 | Output Format - JSON, Text, and Markdown Reports | 3 | Backlog |

**Total Points:** 32

## Requirements Summary

### Functional Requirements

**CLI Integration:**
- `devforgeai ast-grep scan --path src/` command
- `--category` filter (security, anti-patterns, complexity, architecture)
- `--language` filter (python, csharp, typescript, javascript)
- `--format` output (text, json, markdown)
- Installation via multi-package manager (PyPI first, fallback to system binary detection)
- Interactive prompts for missing ast-grep (install now? fallback to grep? skip?)

**Rule Categories (Phase 1):**
1. **Security (5 rules):** SQL injection, XSS, hardcoded secrets, eval, insecure deserialization
2. **Anti-patterns (10 rules):** God objects, async void, console.log, magic numbers, long methods, nested conditionals, unused imports, parameter count, method complexity, duplicate code patterns
3. **Output:** JSON (automation), text (CLI), markdown (reports)

### Data Model

**Entities:**
- **Rule:** YAML configuration (id, language, severity, message, pattern, fix)
- **Configuration:** sgconfig.yml (rule directories, language globs, test directories)
- **Violation:** Detection result (file, line, column, rule_id, severity, evidence, remediation)
- **Report:** Aggregated violations by severity (critical_count, high_count, violations array)

**Relationships:**
- Configuration → Rules: One-to-many (one config references many rule files)
- Scan → Violations: One-to-many (one scan produces many violations)
- Report → Violations: One-to-many (one report aggregates violations by severity)

### Integration Points

1. **ast-grep CLI:** REST-like invocation via subprocess (`sg scan --config ... --json`)
2. **devforgeai-validate CLI:** New subcommand `ast-grep scan` in `.claude/scripts/devforgeai_cli/validators/ast_grep_validator.py`
3. **setup.py:** Add dependency `ast-grep-cli>=0.40.0,<1.0.0`

### Non-Functional Requirements

**Performance:**
- No specific target (accuracy is priority over speed)
- Acceptable: <10s for 1000 files
- Benchmark current grep approach (~5s) for comparison

**Security:**
- Rules validate security practices (OWASP Top 10 coverage)
- No execution of analyzed code (static analysis only)
- Rule definitions reviewed for false positives

**Scalability:**
- Support projects with 1000+ files
- Incremental scanning (future enhancement)
- Caching (future enhancement)

**Availability:**
- Graceful fallback to grep when ast-grep unavailable
- Clear error messages for installation issues
- Multi-platform support (Linux, macOS, Windows/WSL)

## Architecture Considerations

**Complexity Tier:** 2 (Moderate Application)

**Recommended Architecture:**
- Pattern: Modular integration following DevForgeAI 3-layer architecture (Skills → Subagents → Commands)
- Layers: CLI validator (Layer 3), validation logic (Layer 2), ast-grep wrapper (utility)
- Database: File-based rule storage (`devforgeai/ast-grep/rules/`)
- Deployment: Installed via pip as part of DevForgeAI CLI tools

**Technology Recommendations:**
- Backend: Python 3.10+ (matches existing devforgeai-validate CLI)
- CLI Framework: argparse (consistency with existing CLI)
- Dependencies: ast-grep-cli (PyPI), PyYAML (existing dependency)
- Testing: pytest (existing test framework)

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| ast-grep not installed | Medium | Multi-package manager installation + interactive prompts + graceful fallback to grep |
| Markdown support gap | Medium | Hybrid approach: extract code blocks from Markdown → analyze with ast-grep |
| False positives | Medium | Extensive rule testing with test fixtures + constraint refinement |
| ast-grep API changes | Low | Pin version >=0.40.0,<1.0.0, monitor changelog |
| Performance degradation | Low | Benchmarking + optimization if needed (accuracy priority) |

## Dependencies

**Prerequisites:**
- DevForgeAI context files exist (tech-stack.md, source-tree.md, etc.)
- Python 3.10+ installed
- pip package manager available

**Dependents:**
- EPIC-019: Framework Integration (requires CLI validator and core rules)
- EPIC-020: Self-Validation & Dogfooding (requires complete rule infrastructure)

## Next Steps

1. **Story Creation:** Break features into implementable stories via `/create-story`
   - STORY: CLI Validator Foundation (Feature 1)
   - STORY: Configuration Infrastructure (Feature 2)
   - STORY: Core Security Rules (Feature 3)
   - STORY: Core Anti-pattern Rules (Feature 4)
   - STORY: Output Format (Feature 5)

2. **Architecture Validation:** Validate against DevForgeAI constraints
   - Check tech-stack.md for compatibility
   - Verify 3-layer architecture compliance
   - Validate token budget constraints

3. **Sprint Planning:** Assign stories to Sprint 1-3 via `/create-sprint`
   - Sprint 1: CLI validator + configuration (Stories 1-2)
   - Sprint 2: Security rules (Story 3)
   - Sprint 3: Anti-pattern rules + output format (Stories 4-5)
