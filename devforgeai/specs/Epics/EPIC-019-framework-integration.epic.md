---
id: EPIC-019
title: Framework Integration (Subagents + QA)
business-value: Replace grep-based analysis with semantic AST queries across DevForgeAI subagents and QA skill
status: Planning
priority: High
complexity-score: 21
architecture-tier: Tier 2
created: 2025-12-08
estimated-points: 35
target-sprints: 4-5
---

# EPIC-019: Framework Integration (Subagents + QA)

## Business Goal

Enhance DevForgeAI's code analysis subagents (anti-pattern-scanner, code-quality-auditor, code-analyzer) and QA skill with ast-grep semantic analysis, replacing grep-based pattern matching for higher accuracy and deeper insights.

**Success Metrics:**
- Duplication detection accuracy: 60% → 92% (+32%)
- Dependency graph accuracy: 75% → 95% (+20%)
- Architecture violation detection: 65% → 88% (+23%)
- Zero regression in existing QA workflows (backward compatible)

## Features

### Feature 1: anti-pattern-scanner Enhancement
**Description:** Replace grep-based anti-pattern detection with ast-grep semantic queries for god objects, layer violations, circular dependencies, and forbidden patterns.

**User Stories (high-level):**
1. As a QA validator, I want semantic anti-pattern detection so that false positives are reduced
2. As a developer, I want layer boundary violations detected so that clean architecture is enforced
3. As a code reviewer, I want circular dependency detection so that architectural violations are caught early

**Estimated Effort:** Medium (8-10 story points)

### Feature 2: code-quality-auditor Enhancement
**Description:** Replace external tools (radon/lizard) with ast-grep for AST-based complexity analysis, duplication detection via AST comparison, and maintainability metrics.

**User Stories (high-level):**
1. As a QA engineer, I want AST-based complexity analysis so that results are language-agnostic
2. As a refactoring specialist, I want semantic duplication detection so that refactored code with different variable names is still detected
3. As a tech lead, I want maintainability metrics based on AST so that code quality is measurable

**Estimated Effort:** Large (10-12 story points)

### Feature 3: code-analyzer Enhancement
**Description:** Replace regex-based API extraction with semantic parsing for function signatures, class definitions, import analysis, and dependency graphs.

**User Stories (high-level):**
1. As a documentation generator, I want accurate function signature extraction so that API docs are complete
2. As an architecture validator, I want semantic dependency graphs so that layer violations are detected
3. As a developer, I want unused import detection so that code stays clean

**Estimated Effort:** Medium (7-9 story points)

### Feature 4: QA Skill Integration
**Description:** Integrate ast-grep into devforgeai-qa Phase 2 (Anti-Pattern Detection) with fallback to existing grep-based analysis, severity mapping, and violation aggregation.

**User Stories (high-level):**
1. As a QA skill, I want ast-grep invocation in Phase 2 so that semantic analysis runs automatically
2. As a developer, I want hybrid validation (ast-grep + grep fallback) so that workflows never fail due to missing tools
3. As a QA reporter, I want ast-grep violations in QA reports so that all issues are visible

**Estimated Effort:** Medium (6-8 story points)

### Feature 5: Severity Mapping & Blocking
**Description:** Map ast-grep severity (error/warning/hint) to DevForgeAI severity (CRITICAL/HIGH/MEDIUM/LOW) and enforce blocking behavior for CRITICAL/HIGH violations in /dev workflow.

**User Stories (high-level):**
1. As a quality gate, I want CRITICAL violations to block /dev workflow so that critical issues are fixed immediately
2. As a developer, I want HIGH violations reported but workflow continues so that I can address them in context
3. As a project lead, I want configurable blocking behavior so that enforcement matches project needs

**Estimated Effort:** Small (4-6 story points)

## Requirements Summary

### Functional Requirements

**Subagent Enhancements:**
1. **anti-pattern-scanner:** Phase 2-6 use `devforgeai ast-grep scan --category anti-patterns --format json` instead of grep
2. **code-quality-auditor:** Replace radon/lizard with ast-grep complexity rules, AST-based duplication detection
3. **code-analyzer:** Replace regex extraction with `sg run --pattern` for semantic parsing

**QA Skill Integration:**
- Phase 2 Step 2.1: Execute ast-grep scan (`devforgeai ast-grep scan --path src/ --format json`)
- Fallback: If ast-grep unavailable, use anti-pattern-scanner subagent (grep-based)
- Violation merging: Combine ast-grep + subagent results
- Severity mapping: ast-grep error→CRITICAL, warning→HIGH/MEDIUM, hint→LOW

**Blocking Enforcement:**
- CRITICAL violations: HALT /dev workflow immediately (strict blocking)
- HIGH violations: Report but continue (advisory)
- MEDIUM/LOW violations: Report in summary (informational)

### Data Model

**Entities:**
- **Violation (enhanced):** Add fields: `rule_id` (ast-grep rule ID), `category` (security/anti-patterns/complexity/architecture), `owasp` (OWASP mapping if security)
- **QA Report (enhanced):** Add section: `ast_grep_violations` (separate from grep-based violations for comparison)
- **Severity Mapping:** ast-grep severity → DevForgeAI severity (error→CRITICAL, warning→HIGH, hint→LOW)

**Relationships:**
- QA Skill → ast-grep CLI: One-to-one (single invocation per QA run)
- Subagent → ast-grep CLI: One-to-many (multiple scans per subagent execution)

### Integration Points

1. **devforgeai-qa SKILL.md:** Phase 2 invokes `devforgeai ast-grep scan`
2. **anti-pattern-scanner.md:** Phases 2-6 invoke ast-grep with category filters
3. **code-quality-auditor.md:** Phase 2 (Complexity) uses ast-grep rules
4. **code-analyzer.md:** Step 3 (Public API Extraction) uses `sg run --pattern`

### Non-Functional Requirements

**Performance:**
- QA Phase 2 execution time: Target <30s for 1000 files (acceptable: <60s)
- Subagent overhead: ast-grep adds <10s vs grep-based analysis

**Backward Compatibility:**
- Existing QA reports unchanged (new ast-grep section added)
- Grep-based subagents still functional (fallback preserved)
- No breaking changes to skill interfaces

**Reliability:**
- Graceful degradation when ast-grep unavailable
- Error handling for ast-grep CLI failures
- Violation parsing resilient to format changes

## Architecture Considerations

**Complexity Tier:** 2 (Moderate Application)

**Recommended Architecture:**
- Pattern: Enhance existing subagents (no new subagents created)
- Layers: Subagents invoke CLI validator (Layer 2 → Layer 3)
- Integration: Skills invoke enhanced subagents (Layer 1 → Layer 2)
- Data Flow: ast-grep CLI → JSON → Subagent → Skill → QA Report

**Technology Recommendations:**
- Enhancement: Python modifications to existing subagent prompts
- CLI Integration: Bash subprocess calls to `devforgeai ast-grep scan`
- Output Parsing: JSON deserialization (standard library)
- Testing: pytest with fixtures for ast-grep output

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Subagent prompt size exceeds limits | Medium | Use progressive disclosure (load ast-grep integration details on-demand) |
| ast-grep CLI changes break parsing | Medium | Pin version >=0.40.0,<1.0.0, validate JSON schema |
| Performance regression in QA | Low | Benchmarking + parallel scans (future optimization) |
| Backward compatibility broken | High | Comprehensive testing of existing QA workflows, fallback preserved |
| False negatives (missed violations) | Medium | Hybrid approach (ast-grep + grep both run, results merged) |

## Dependencies

**Prerequisites:**
- EPIC-018 complete (CLI validator, core rules, configuration infrastructure)
- Existing subagents functional (anti-pattern-scanner, code-quality-auditor, code-analyzer)
- QA skill Phase 2 workflow stable

**Dependents:**
- EPIC-020: Self-Validation & Dogfooding (uses enhanced subagents for framework validation)

## Next Steps

1. **Story Creation:** Break features into implementable stories via `/create-story`
   - STORY: anti-pattern-scanner Enhancement (Feature 1)
   - STORY: code-quality-auditor Enhancement (Feature 2)
   - STORY: code-analyzer Enhancement (Feature 3)
   - STORY: QA Skill Integration (Feature 4)
   - STORY: Severity Mapping & Blocking (Feature 5)

2. **Architecture Validation:** Validate against DevForgeAI constraints
   - Verify subagent prompt size stays within limits (<500 lines)
   - Check tool usage patterns (Bash subprocess invocation)
   - Validate backward compatibility

3. **Sprint Planning:** Assign stories to Sprint 4-7 via `/create-sprint`
   - Sprint 4: anti-pattern-scanner + code-analyzer (Stories 1, 3)
   - Sprint 5: code-quality-auditor (Story 2)
   - Sprint 6: QA Skill Integration (Story 4)
   - Sprint 7: Severity Mapping & Testing (Story 5)
