---
id: SPRINT-7
name: Sprint 7 - AST-Grep
epic: EPIC-018
start_date: 2025-12-22
end_date: 2026-01-05
duration_days: 14
status: Active
total_points: 32
completed_points: 0
stories:
  - STORY-115
  - STORY-116
  - STORY-117
  - STORY-118
  - STORY-119
created: 2025-12-20 14:30:00
---

# Sprint 7: AST-Grep

## Overview

**Duration:** 2025-12-22 to 2026-01-05 (14 days)
**Capacity:** 32 story points
**Epic:** EPIC-018 - ast-grep Foundation & Core Rules
**Status:** Active

## Sprint Goals

Complete the foundation and core rules layer for ast-grep integration into DevForgeAI, enabling semantic code analysis with 90%+ accuracy for security vulnerabilities and code anti-patterns. This sprint delivers:

1. **CLI Foundation:** Auto-install wrapper, dependency validation, graceful fallback
2. **Rule Infrastructure:** Project-scoped storage, sgconfig.yml configuration, language organization
3. **Security Analysis:** CRITICAL severity rules for SQL injection, XSS, secrets, eval, deserialization
4. **Quality Rules:** HIGH/MEDIUM severity anti-pattern detection (god objects, async void, console.log, etc.)
5. **Output Formatting:** JSON, text, and markdown formats compatible with DevForgeAI QA reporting

**Expected Business Impact:** Improve code analysis accuracy from 60-75% to 90-95%+ through AST-aware pattern matching, reducing false positives and enabling stricter quality gates.

## Stories

### In Progress (0 points)

[None - Sprint just starting]

### Ready for Dev (32 points)

#### STORY-115: CLI Validator Foundation - ast-grep Integration
- **Points:** 8
- **Priority:** Medium
- **Epic:** EPIC-018
- **Acceptance Criteria:** 4 criteria
- **Status:** Ready for Dev
- **Dependencies:** None
- **Description:** Create CLI validator that wraps ast-grep with auto-install via PyPI, version compatibility checking, and graceful fallback to grep-based analysis.

#### STORY-116: Configuration Infrastructure - ast-grep Rule Storage
- **Points:** 5
- **Priority:** Medium
- **Epic:** EPIC-018
- **Acceptance Criteria:** 4 criteria
- **Status:** Ready for Dev
- **Dependencies:** STORY-115
- **Description:** Establish rule storage structure (.devforgeai/ast-grep/rules/), language-specific directories (python/, csharp/, typescript/, javascript/), and auto-generated sgconfig.yml configuration.

#### STORY-117: Core Security Rules - CRITICAL Severity Detection
- **Points:** 8
- **Priority:** Medium
- **Epic:** EPIC-018
- **Acceptance Criteria:** 5 criteria
- **Status:** Ready for Dev
- **Dependencies:** STORY-115, STORY-116
- **Description:** Create 5 CRITICAL severity security rules covering SQL injection, XSS, hardcoded secrets, eval usage, and insecure deserialization for Python, C#, and TypeScript.

#### STORY-118: Core Anti-pattern Rules - Code Quality Detection
- **Points:** 8
- **Priority:** Medium
- **Epic:** EPIC-018
- **Acceptance Criteria:** 7 criteria
- **Status:** Ready for Dev
- **Dependencies:** STORY-115, STORY-116
- **Description:** Create 10 HIGH/MEDIUM severity anti-pattern rules covering god objects, async void, console.log in production, magic numbers, long methods, nested conditionals, and more.

#### STORY-119: Output Format - JSON, Text, and Markdown Reports
- **Points:** 3
- **Priority:** Medium
- **Epic:** EPIC-018
- **Acceptance Criteria:** 5 criteria
- **Status:** Ready for Dev
- **Dependencies:** STORY-115, STORY-117, STORY-118
- **Description:** Implement JSON, text, and markdown output formatters for ast-grep violations with severity mapping and DevForgeAI QA report integration.

### Completed (0 points)

[None - Sprint in progress]

## Sprint Metrics

- **Planned Velocity:** 32 points
- **Current Velocity:** 0 points (0%)
- **Stories Planned:** 5
- **Stories Completed:** 0
- **Days Remaining:** 14
- **Capacity Status:** Optimal (32 points for 14-day sprint, target 20-40 range)

**Capacity Analysis:** Sprint carries optimal load with balanced story mix across CLI infrastructure (8 pts), configuration (5 pts), security rules (8 pts), anti-pattern rules (8 pts), and output formatting (3 pts). All work aligns with EPIC-018 goals to improve code analysis accuracy from 60-75% to 90-95%+.

## Story Dependencies

```
STORY-115 (CLI Foundation)
  ├─> STORY-116 (Configuration Infrastructure)
  │   ├─> STORY-117 (Security Rules)
  │   └─> STORY-118 (Anti-pattern Rules)
  │       └─> STORY-119 (Output Format)
  └─> STORY-119 (Output Format)
```

**Recommended Development Order:**
1. **STORY-115** (Foundation) - Days 1-3
2. **STORY-116** (Configuration) - Days 4-5
3. **STORY-117** (Security Rules) - Days 6-8 (parallel with STORY-118)
4. **STORY-118** (Anti-pattern Rules) - Days 6-8 (parallel with STORY-117)
5. **STORY-119** (Output Format) - Days 9-10 (depends on both rules)
6. **Integration & Testing** - Days 11-14

## Technical Context

**Technology Stack:**
- **Language:** Python 3.10+
- **Code Analysis Engine:** ast-grep >=0.40.0,<1.0.0
- **Configuration Format:** YAML (PyYAML existing dependency)
- **CLI Framework:** argparse (consistent with existing devforgeai-validate)

**Architecture Alignment:**
- **Pattern:** Modular integration following DevForgeAI 3-layer architecture
- **Layers:** CLI validator (Layer 3) → Validation logic (Layer 2) → ast-grep wrapper (utility)
- **Storage:** File-based rule storage (`.devforgeai/ast-grep/rules/`)
- **Scope:** Project-scoped integration, no shared infrastructure

**Integration Points:**
1. CLI Command: `devforgeai ast-grep scan --path <dir> --category <category> --language <lang> --format <format>`
2. DevForgeAI QA Skill: Markdown output appends directly to QA reports
3. Quality Gates: CRITICAL violations (security rules) block approval

## Daily Progress

### Week 1 (Dec 22-26)

#### Monday, Dec 22
- [ ] Day 1 Start: STORY-115 foundation setup
  - Create AstGrepValidator class structure
  - Implement detection logic (shutil.which, subprocess)
  - Setup unit tests (Red phase)

#### Tuesday, Dec 23
- [ ] Day 2: STORY-115 auto-install and fallback
  - Implement pip install integration
  - Create GrepFallbackAnalyzer
  - Add version compatibility checks

#### Wednesday, Dec 24
- [ ] Day 3: STORY-115 completion and testing
  - Complete all acceptance criteria tests
  - Performance validation (<500ms detection)
  - Integration testing with CLI

#### Thursday, Dec 25
- [ ] Holiday

#### Friday, Dec 26
- [ ] Day 4: STORY-116 configuration infrastructure
  - Create ConfigurationInitializer
  - Generate directory structure
  - Auto-generate sgconfig.yml

### Week 2 (Dec 29-Jan 2)

#### Monday, Dec 29
- [ ] Day 5: STORY-116 validation and testing
  - Implement ConfigurationValidator
  - Validate YAML, directory structure
  - Complete AC tests

#### Tuesday, Dec 30
- [ ] Day 6-8: STORY-117 & STORY-118 (parallel development)
  - Security rules: SQL injection, XSS, secrets, eval, deserialization
  - Anti-pattern rules: God objects, async void, console.log, magic numbers, etc.
  - Language-specific implementations (Python, C#, TypeScript)

#### Wednesday, Dec 31
- [ ] Day 6-8 continued: Security & anti-pattern rules development

#### Thursday, Jan 1
- [ ] Holiday

#### Friday, Jan 2
- [ ] Day 6-8 continued: Security & anti-pattern rules completion

### Week 3 (Jan 5)

#### Sunday, Jan 5
- [ ] Day 9-10: STORY-119 output formatting
  - JSON formatter with schema
  - Text formatter with ANSI colors
  - Markdown formatter with emoji severity mapping
  - DevForgeAI QA report integration

- [ ] Day 11-14: Integration, testing, and documentation
  - End-to-end testing across all stories
  - Cross-platform validation (Linux, macOS, Windows/WSL)
  - Performance benchmarking
  - Documentation and README updates

## Retrospective Notes

[To be filled at sprint end - 2026-01-05]

- [ ] What went well?
- [ ] What could be improved?
- [ ] Action items for next sprint
- [ ] Velocity assessment

## Next Steps

1. **Start Development**
   - Begin with STORY-115 using `/dev STORY-115`
   - Follow TDD workflow (Red → Green → Refactor)
   - Target completion by 2025-12-24

2. **Dependency Management**
   - STORY-116 cannot start until STORY-115 foundation is solid
   - STORY-117 and STORY-118 can develop in parallel after STORY-116
   - STORY-119 depends on output from STORY-117 and STORY-118

3. **Quality Gates**
   - Each story requires 95%+ code coverage for business logic
   - All acceptance criteria must have passing tests before moving to QA
   - Security rules require ≥95% true positive rate validation

4. **Integration Testing**
   - After STORY-116, validate configuration with real ast-grep installation
   - After STORY-117 and STORY-118, test rules detection with fixtures
   - After STORY-119, validate output formats against DevForgeAI QA expectations

5. **Release Preparation**
   - Documentation updates for new CLI commands
   - Update dependencies.md with ast-grep-cli >=0.40.0,<1.0.0
   - Create migration guide if upgrading existing DevForgeAI installations

## References

- **EPIC:** [EPIC-018: ast-grep Foundation & Core Rules](../Epics/EPIC-018-astgrep-foundation-core-rules.epic.md)
- **Stories:** STORY-115, STORY-116, STORY-117, STORY-118, STORY-119
- **Framework Docs:** [DevForgeAI Architecture](../../context/architecture-constraints.md)
- **External Docs:** [ast-grep Documentation](https://ast-grep.github.io/)

---

**Sprint Template Version:** 2.1
**Created:** 2025-12-20
**Status:** Active
