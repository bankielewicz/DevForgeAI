# Requirements Specification: EPIC-007 Lean Orchestration Compliance

**Epic ID:** EPIC-007
**Created:** 2025-11-14
**Status:** Draft
**Owner:** Framework Maintainers

---

## Executive Summary

This epic establishes lean orchestration pattern compliance across all 11 DevForgeAI slash commands by refactoring commands to delegate business logic to skills, ensuring sustainable framework architecture.

**Problem:** Commands contain business logic violating "commands orchestrate, skills validate" pattern
**Solution:** Systematic refactoring to move logic from commands to skills
**Impact:** 100% pattern compliance, 50%+ token efficiency, zero technical debt accumulation

---

## Functional Requirements

### FR-001: Command Character Budget Compliance
**Priority:** Critical
**Description:** All commands must remain under 15K character limit

**Acceptance Criteria:**
- All 11 commands <15K characters
- Target range: 6K-12K characters (optimal)
- Automated validation via `/audit-budget`

**Success Metric:** 100% compliance (11/11 commands)

---

### FR-002: Lean Pattern Compliance
**Priority:** Critical
**Description:** All commands follow 5-responsibility checklist

**Command Responsibilities (ONLY):**
1. Parse arguments
2. Load context
3. Set markers
4. Invoke skill
5. Display results

**Command Prohibitions:**
- Business logic
- Complex parsing
- Template generation
- Decision-making
- Error recovery

**Acceptance Criteria:**
- Manual checklist validation per command
- Zero violations detected

**Success Metric:** 100% compliance (11/11 commands pass)

---

### FR-003: Business Logic in Skills
**Priority:** Critical
**Description:** Skills contain ALL business logic, commands contain NONE

**Acceptance Criteria:**
- No if-then logic in commands (except argument validation)
- No calculations/algorithms in commands
- No report generation in commands
- Skills have comprehensive workflows (5-7 phases typical)

**Success Metric:** Zero business logic detected in commands

---

### FR-004: Token Efficiency Improvement
**Priority:** High
**Description:** Achieve 50%+ token usage reduction through lean refactoring

**Baseline Measurement:**
- Measure current token usage per command
- Record main conversation token consumption

**Target:**
- 50%+ reduction in main conversation tokens
- Skill logic in isolated contexts

**Acceptance Criteria:**
- Before/after token measurements documented
- Efficiency improvement ≥50%

**Success Metric:** 50%+ average improvement across refactored commands

---

### FR-005: Zero Functional Regressions
**Priority:** Critical
**Description:** All refactorings preserve existing behavior

**Acceptance Criteria:**
- All existing tests pass (e.g., 75/75 for /qa)
- Command behavior identical before/after
- Performance overhead <100ms per command

**Success Metric:** 100% test pass rate (no regressions)

---

## Non-Functional Requirements

### NFR-001: Maintainability
**Priority:** High
**Description:** Commands easier to understand and modify

**Metrics:**
- Line count reduction ≥30%
- Phase count reduced to 3-5
- Documentation clarity improved

---

### NFR-002: Scalability
**Priority:** Medium
**Description:** Pattern supports adding new commands without bloat

**Metrics:**
- Template includes lean pattern checklist
- New commands follow pattern by default

---

### NFR-003: Reliability
**Priority:** Critical
**Description:** Refactoring does not introduce instability

**Metrics:**
- Zero production incidents post-refactoring
- Rollback procedures documented

---

## Feature Requirements

### Feature 1: Refactor /qa Command (STORY-034)

**Current State:**
- 509 lines
- Phases 4 & 5 contain 167 lines of business logic
- Violates lean pattern (RCA-009)

**Target State:**
- ~340 lines (33% reduction)
- 3 phases only (Phase 0, 1, 2)
- Business logic in skill (Phases 6 & 7)

**Deliverables:**
- Refactored .claude/commands/qa.md
- Enhanced .claude/skills/devforgeai-qa/SKILL.md (add Phases 6 & 7)
- 2 reference files (feedback-hooks-workflow.md, story-update-workflow.md)

**Story:** STORY-034

---

### Feature 2: Audit All Commands

**Objectives:**
- Document current state of all 11 commands
- Identify violations and severity
- Create refactoring backlog

**Deliverables:**
- Command compliance audit report
- Violation documentation by severity
- Prioritized refactoring backlog stories

**Tool:** `/audit-budget` automation

---

### Feature 3: Refactor /create-ui Command

**Current State:**
- 19K characters (126% over budget)
- Complex UI generation logic in command

**Target State:**
- <12K characters (within budget)
- UI logic in devforgeai-ui-generator skill

**Risk:** High complexity due to size

---

### Feature 4: Refactor /release Command

**Current State:**
- 18K characters (121% over budget)
- Complex deployment logic in command

**Target State:**
- <12K characters (within budget)
- Deployment logic in devforgeai-release skill

**Risk:** High due to production deployment impact

---

### Feature 5: Update Framework Documentation

**Objectives:**
- Document lean pattern as framework standard
- Provide templates with pattern built-in
- Create troubleshooting guidance

**Deliverables:**
- Updated lean-orchestration-pattern.md
- Updated command-budget-reference.md
- Updated .claude/memory/commands-reference.md
- Command creation template with lean checklist
- Pattern violation troubleshooting guide

---

## Implementation Strategy

### Phase 1: Prove Pattern (Sprint 1)
- Refactor /qa (STORY-034)
- Audit all commands
- Validate approach works

### Phase 2: Scale Pattern (Sprints 2-3)
- Refactor /create-ui
- Refactor /release
- Update documentation

### Phase 3: Sustain Pattern (Ongoing)
- Monthly compliance audits
- Track trends
- Prevent regressions

---

## Success Criteria Summary

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Commands under budget | 11/11 (100%) | `/audit-budget` |
| Lean pattern compliance | 11/11 (100%) | Manual checklist |
| Business logic in commands | 0 violations | Code review |
| Token efficiency | ≥50% improvement | Before/after measurement |
| Test pass rate | 100% | Test suite execution |
| Documentation complete | 100% | Manual review |

---

## Risks and Mitigations

**Risk 1: Functional Regressions**
- Mitigation: Backup commands, run tests, measure behavior
- Probability: Medium
- Impact: High
- Owner: Framework Maintainers

**Risk 2: Pattern Misapplication**
- Mitigation: Follow proven examples, reference protocol
- Probability: Low
- Impact: Medium
- Owner: Framework Maintainers

**Risk 3: Token Budget Regression**
- Mitigation: Measure baseline, target 50%+ improvement
- Probability: Low
- Impact: Medium
- Owner: AI Development Team

---

## Dependencies

- RCA-009 analysis ✅
- lean-orchestration-pattern.md ✅
- Refactoring examples ✅
- Test suites for commands ✅

---

## Timeline

**Sprint 1:** Features 1-2 (11 points)
**Sprint 2:** Feature 3 (13 points)
**Sprint 3:** Features 4-5 (16 points)

**Total:** 40 points, 2-3 sprints (4-6 weeks)

---

## Stakeholders

- **Framework Maintainers:** Implementation, validation
- **AI Development Team:** Pattern guidance, validation

---

**Requirements Status:** APPROVED FOR IMPLEMENTATION
**Next Step:** Sprint planning - assign features to Sprint-3
