---
id: EPIC-020
title: Self-Validation & Dogfooding
business-value: DevForgeAI framework validates its own code quality using ast-grep rules, demonstrating framework maturity and preventing framework-level technical debt
status: Planning
priority: Medium
complexity-score: 21
architecture-tier: Tier 2
created: 2025-12-08
estimated-points: 20
target-sprints: 2-3
---

# EPIC-020: Self-Validation & Dogfooding

## Business Goal

Enable DevForgeAI framework to validate its own codebase using ast-grep rules, creating framework-specific rules that enforce best practices, prevent anti-patterns, and ensure the framework itself follows the principles it advocates.

**Success Metrics:**
- 100+ total rules across all 4 languages (Python, C#, TypeScript, JavaScript)
- DevForgeAI framework passes own validation (zero CRITICAL/HIGH violations)
- Pre-commit hook prevents framework violations from being committed
- Framework code quality measurably improved (complexity, duplication, coverage)

## Features

### Feature 1: DevForgeAI-Specific Rules
**Description:** Create custom ast-grep rules that enforce DevForgeAI framework conventions such as "use native tools over Bash", "no missing frontmatter", "skills under 1000 lines", and "progressive disclosure pattern".

**User Stories (high-level):**
1. As a framework maintainer, I want bash-for-files violations detected so that native tools (Read/Write/Glob/Grep) are enforced
2. As a skill author, I want missing YAML frontmatter detected so that all skills/subagents/commands follow template
3. As a framework reviewer, I want skill size violations detected so that components stay under 1000 lines (token budget)

**Estimated Effort:** Medium (7-9 story points)

### Feature 2: Pre-commit Integration
**Description:** Integrate ast-grep validation into Git pre-commit hooks so that framework code is automatically validated before commits, blocking commits with CRITICAL/HIGH violations.

**User Stories (high-level):**
1. As a developer, I want pre-commit validation so that framework violations are caught before commit
2. As a reviewer, I want violations blocked at commit time so that PRs are higher quality
3. As a CI/CD engineer, I want pre-commit hook installable so that all contributors use validation

**Estimated Effort:** Small (4-6 story points)

### Feature 3: Complete Rule Coverage
**Description:** Expand rule coverage to 100+ rules total across Python, C#, TypeScript, JavaScript covering all categories (Security, Anti-patterns, Complexity, Architecture).

**User Stories (high-level):**
1. As a framework user, I want comprehensive Python rules so that Python projects are fully validated
2. As a .NET developer, I want complete C# rules so that .NET projects follow best practices
3. As a web developer, I want TypeScript/JavaScript rules so that web projects are validated

**Estimated Effort:** Large (5-7 story points per language = 20-28 total, split across iterations)

**Rule Breakdown:**
- Python: 30 rules (10 security, 10 anti-patterns, 5 complexity, 5 architecture)
- C#: 30 rules (10 security, 10 anti-patterns, 5 complexity, 5 architecture)
- TypeScript: 25 rules (8 security, 10 anti-patterns, 4 complexity, 3 architecture)
- JavaScript: 25 rules (8 security, 10 anti-patterns, 4 complexity, 3 architecture)
- Universal: 10 rules (TODOs, FIXMEs, hardcoded URLs, etc.)

**Total: 120 rules** (exceeds 100+ goal)

### Feature 4: Documentation & Guides
**Description:** Create comprehensive documentation for ast-grep integration including rule authoring guide, troubleshooting guide, custom rule creation workflow, and migration guide for projects.

**User Stories (high-level):**
1. As a rule author, I want a rule creation guide so that I can write custom rules
2. As a user, I want troubleshooting documentation so that I can resolve ast-grep issues
3. As a project lead, I want migration guide so that I can adopt ast-grep in my project

**Estimated Effort:** Small (4-6 story points)

## Requirements Summary

### Functional Requirements

**DevForgeAI-Specific Rules (Priority):**
1. **bash-for-files:** Detect Bash usage for file operations (cat, echo, find, grep, sed) - suggest native tools
2. **missing-frontmatter:** Detect skills/subagents/commands without YAML frontmatter
3. **skill-size-violation:** Detect skills exceeding 1000 lines (token budget)
4. **missing-progressive-disclosure:** Detect skills not using "see references/" pattern
5. **circular-skill-dependencies:** Detect Skill A → Skill B → Skill A cycles
6. **prohibited-tools:** Detect skills using prohibited tool combinations
7. **ambiguity-without-askuserquestion:** Detect skills making assumptions without asking
8. **hardcoded-paths:** Detect hardcoded file paths (should be configurable)
9. **missing-error-handling:** Detect skills without error recovery procedures
10. **language-specific-examples:** Detect framework docs with language-specific code (should be agnostic)

**Pre-commit Hook:**
- Install script: `.claude/scripts/install_ast_grep_hooks.sh`
- Hook location: `.git/hooks/pre-commit`
- Validation: Run `devforgeai ast-grep scan --path .claude/ --category devforgeai --format text`
- Blocking: Exit code 1 if CRITICAL/HIGH violations found
- Bypass: Allow `git commit --no-verify` (but log warning)

**Documentation:**
- Rule Authoring Guide: `.devforgeai/ast-grep/docs/rule-authoring-guide.md`
- Troubleshooting Guide: `.devforgeai/ast-grep/docs/troubleshooting.md`
- Custom Rule Workflow: `.devforgeai/ast-grep/docs/custom-rule-workflow.md`
- Migration Guide: `.devforgeai/ast-grep/docs/migration-guide.md`

### Data Model

**Entities:**
- **DevForgeAI Rule:** Custom rule for framework validation (extends base Rule entity)
- **Pre-commit Hook:** Shell script configuration (hook path, validation command, exit codes)
- **Rule Test Fixture:** Test cases for rule validation (valid code, invalid code, expected violations)
- **Documentation:** Markdown files (guides, examples, troubleshooting)

**Relationships:**
- DevForgeAI Rule → Test Fixtures: One-to-many (one rule has many test cases)
- Pre-commit Hook → Rules: One-to-many (hook validates all rules)
- Documentation → Rules: One-to-many (one guide documents many rules)

### Integration Points

1. **Git Pre-commit Hook:** `.git/hooks/pre-commit` invokes `devforgeai ast-grep scan`
2. **CI/CD Pipeline:** GitHub Actions (future) runs ast-grep validation on PRs
3. **Framework Self-Validation:** DevForgeAI codebase scanned with own rules

### Non-Functional Requirements

**Performance:**
- Pre-commit validation: <5s for framework codebase (~200 files)
- Rule execution: <1s per rule category
- Documentation build: <2s (Markdown generation)

**Maintainability:**
- Rule tests: 100% coverage (all rules have test fixtures)
- Documentation: 100% rule coverage (all rules documented)
- Examples: All rules have valid/invalid code examples

**Usability:**
- Clear violation messages with remediation guidance
- Rule test fixtures demonstrate correct/incorrect usage
- Documentation searchable and indexed

## Architecture Considerations

**Complexity Tier:** 2 (Moderate Application)

**Recommended Architecture:**
- Pattern: Extension of existing ast-grep infrastructure (no new architecture needed)
- Layers: DevForgeAI rules stored in `.devforgeai/ast-grep/rules/devforgeai/`
- Pre-commit: Standard Git hook pattern (shell script)
- Testing: pytest with rule test fixtures

**Technology Recommendations:**
- Rules: YAML (ast-grep standard format)
- Pre-commit: Bash script (Git hooks requirement)
- Documentation: Markdown (DevForgeAI standard)
- Testing: pytest + sh (test rule fixtures + hook installation)

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Pre-commit hook slows down commits | Low | Optimize rule execution, provide `--no-verify` escape hatch |
| False positives in framework code | Medium | Extensive testing with framework codebase, refine rules iteratively |
| Rule maintenance burden | Medium | Document rule intent, provide test fixtures, automate testing |
| DevForgeAI framework violations found | Medium | Fix violations discovered, update framework to follow own rules |
| Documentation becomes stale | Low | Automated doc generation from rule metadata, version with rules |

## Dependencies

**Prerequisites:**
- EPIC-018 complete (CLI validator, core rules, configuration)
- EPIC-019 complete (subagents enhanced, QA integrated)
- Git repository initialized (for pre-commit hooks)

**Dependents:**
- None (final epic in ast-grep integration series)

## Next Steps

1. **Story Creation:** Break features into implementable stories via `/create-story`
   - STORY: DevForgeAI-Specific Rules (Feature 1)
   - STORY: Pre-commit Integration (Feature 2)
   - STORY: Complete Rule Coverage - Python (Feature 3a)
   - STORY: Complete Rule Coverage - C# (Feature 3b)
   - STORY: Complete Rule Coverage - TypeScript/JavaScript (Feature 3c)
   - STORY: Documentation & Guides (Feature 4)

2. **Architecture Validation:** Validate against DevForgeAI constraints
   - Verify rule storage location (`.devforgeai/ast-grep/rules/devforgeai/`)
   - Check pre-commit hook follows Git standards
   - Validate documentation format (Markdown with frontmatter)

3. **Sprint Planning:** Assign stories to Sprint 8-10 via `/create-sprint`
   - Sprint 8: DevForgeAI rules + pre-commit (Stories 1-2)
   - Sprint 9: Complete rule coverage (Stories 3a-3c)
   - Sprint 10: Documentation + polish (Story 4)

4. **Framework Self-Validation:** Run ast-grep on DevForgeAI codebase
   - Scan `.claude/skills/`, `.claude/agents/`, `.claude/commands/`
   - Fix violations discovered
   - Document as dogfooding success story
