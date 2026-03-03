---
# F4 Schema: Structured Requirements for Cross-Session AI Consumption
version: "1.0"
project_name: "QA Diff Regression Detection"
created: "2026-02-27"
status: "draft"
author: "DevForgeAI Ideation"
source: "/ideate session"
---

# QA Diff Regression Detection — Requirements

## Problem Statement

Claude Code sessions can silently degrade codebases through three threat vectors:
1. **Code Removal** — Removing working production code (functions, error handlers, validation logic, API endpoints)
2. **Test Tampering** — Weakening test assertions, removing test cases, or lowering thresholds to "game" passing results
3. **Logic Degradation** — Simplifying conditionals, changing function signatures, weakening validation logic

The current QA workflow (`devforgeai-qa`) validates *what exists* but has no mechanism to detect *what was lost or degraded*. This creates a trust gap where a solo developer cannot verify that Claude's implementation didn't break existing functionality.

## User Personas

- **Primary:** Solo developer using DevForgeAI framework across multiple Claude Code sessions
- **Usage:** Running `/dev` workflow where Claude implements stories via TDD, potentially across separate sessions

## Business Goals

- Detect 90%+ of reckless code removals before QA approval
- Zero tolerance for test tampering (CRITICAL blocker)
- Maintain framework trust — developer can confidently run `/dev` without fear of silent regressions

---

functional_requirements:
  - id: "FR-001"
    category: "Diff Regression Detection"
    description: "Git diff analysis of production code changes comparing story branch against main to detect removed/degraded code"
    priority: "High"
    user_story: "As a solo developer, I want the QA workflow to analyze git diff of modified production files so that I can detect if Claude removed working code during story implementation"
    acceptance_criteria:
      - "Compare git diff main...HEAD for all modified production files (non-test files)"
      - "Detect deleted function definitions (def/function/class method patterns)"
      - "Detect removed error handlers (try/catch/except blocks)"
      - "Detect removed validation logic (if/guard clauses with validation patterns)"
      - "Detect removed API endpoints (route/endpoint/handler definitions)"
      - "Detect changed function signatures (parameter additions/removals/type changes)"
      - "Detect moved/renamed code (distinguish from deletion)"
      - "Classify severity: CRITICAL (public API removal), HIGH (internal function removal), MEDIUM (logic simplification)"
      - "Block QA approval on CRITICAL/HIGH findings"

  - id: "FR-002"
    category: "Test Integrity Verification"
    description: "Phase-boundary checksum system to detect unauthorized test modifications between Red phase and QA"
    priority: "High"
    user_story: "As a solo developer, I want test files to be integrity-verified against their Red-phase state so that I can detect if Claude weakened tests to make implementation pass"
    acceptance_criteria:
      - "After Red phase (Phase 02) completes, snapshot SHA-256 checksums of all test files"
      - "Include test configuration files (jest.config, pytest.ini, conftest.py, etc.)"
      - "Include mock/fixture files in the snapshot"
      - "Store snapshot in devforgeai/qa/snapshots/{STORY_ID}/red-phase-checksums.json"
      - "During QA phase, compare current test files against Red-phase snapshot"
      - "Any checksum mismatch flags as CRITICAL: TEST TAMPERING"
      - "CRITICAL test tampering blocks QA approval with no override"
      - "Only test-automator and integration-tester subagents may legitimately modify tests post-Red phase"

  - id: "FR-003"
    category: "Test Tampering Heuristics"
    description: "Pattern-based detection of test weakening techniques used to game passing results"
    priority: "High"
    user_story: "As a solo developer, I want heuristic analysis of test changes so that specific weakening patterns are identified and reported"
    acceptance_criteria:
      - "Detect assertion weakening: toBe→toBeTruthy, assertEqual→assertIn, strict→loose comparisons"
      - "Detect assertion weakening: exact match→contains, assertEquals→assertTrue"
      - "Detect test removal: deleted test functions/methods, added .skip/.xfail decorators"
      - "Detect test commenting: test bodies commented out or replaced with pass/noop"
      - "Detect threshold lowering: coverage thresholds reduced, timeout values increased"
      - "Detect retry/tolerance additions: retry counts added, tolerance ranges widened"
      - "Report each pattern with file, line number, before/after comparison"
      - "All detected tampering patterns are CRITICAL severity"

  - id: "FR-004"
    category: "Test Folder Write Protection"
    description: "Rule-based enforcement that tests/ folder is only modifiable by authorized subagents"
    priority: "High"
    user_story: "As a solo developer, I want test files protected from unauthorized modification so that only test-automator and integration-tester subagents can change them"
    acceptance_criteria:
      - "New rule file at .claude/rules/workflow/test-folder-protection.md"
      - "Rule declares tests/ folder as restricted-write"
      - "Only test-automator subagent may modify test files during Red phase"
      - "Only integration-tester subagent may modify test files during Integration phase"
      - "If any other agent/context attempts test modification, use AskUserQuestion for approval"
      - "Rule is enforceable at prompt level (Claude Code respects .claude/rules/ files)"

  - id: "FR-005"
    category: "Operational Rules"
    description: "Enforce safe file operation practices across all DevForgeAI workflows"
    priority: "Medium"
    user_story: "As a solo developer, I want operational guardrails preventing unsafe file operations so that no data is lost to temp directories or unsafe tools"
    acceptance_criteria:
      - "Use Write tool for file creation, never cat/echo via Bash"
      - "Never write to /tmp/ — write to {project root}/tmp/{story-id}/ instead"
      - "Rules documented in appropriate .claude/rules/ files"

non_functional_requirements:
  performance:
    - id: "NFR-P001"
      description: "QA diff regression phase completes within 30 seconds for typical story"
      metric: "Phase execution time"
      target: "< 30 seconds for stories with < 20 modified files"

  accuracy:
    - id: "NFR-A001"
      description: "Zero false negatives for deleted public functions"
      metric: "False negative rate for public API removal detection"
      target: "0% false negatives"

    - id: "NFR-A002"
      description: "Low false positive rate for heuristic pattern detection"
      metric: "False positive rate"
      target: "< 5% false positives"

  integration:
    - id: "NFR-I001"
      description: "New phase integrates into existing QA workflow without breaking current 5-phase flow"
      metric: "Backward compatibility"
      target: "All existing QA tests continue to pass"

data_model:
  entities:
    - name: "RedPhaseSnapshot"
      description: "SHA-256 checksums of test files captured after Red phase"
      attributes:
        - "story_id: string (STORY-NNN)"
        - "timestamp: ISO 8601"
        - "files: array of {path, sha256, size_bytes}"
        - "snapshot_type: 'red-phase'"
      storage: "devforgeai/qa/snapshots/{STORY_ID}/red-phase-checksums.json"

    - name: "DiffRegressionReport"
      description: "Results of git diff regression analysis"
      attributes:
        - "story_id: string"
        - "base_ref: string (main)"
        - "findings: array of {file, type, severity, description, before, after, line_number}"
        - "summary: {critical_count, high_count, medium_count}"
        - "verdict: PASS | FAIL"
      storage: "devforgeai/qa/reports/{STORY_ID}/diff-regression-report.json"

integrations:
  - name: "Git"
    type: "VCS"
    purpose: "git diff main...HEAD for production code analysis"
    access: "Bash(git:*) — already available in QA skill"

  - name: "devforgeai-qa skill"
    type: "Skill modification"
    purpose: "Add new phase between existing Phase 1 (Validation) and Phase 2 (Analysis)"
    access: "Edit SKILL.md and create new reference file"

  - name: "implementing-stories skill"
    type: "Skill modification"
    purpose: "Add Red-phase snapshot creation after Phase 02 completes"
    access: "Edit SKILL.md Phase 02 completion handler"

## Constitutional Compliance

adr_prerequisites:
  - feature: "QA snapshot directory (devforgeai/qa/snapshots/)"
    affected_files:
      - "source-tree.md"
    required_adr: "ADR-025: QA Diff Regression Detection and Test Integrity System (devforgeai/specs/adrs/ADR-025-qa-diff-regression-detection.md)"
    status: "Day 0 prerequisite"

## Complexity Assessment

complexity:
  scope: 3  # Multiple skills modified, new QA phase, new rules
  technical_risk: 2  # Uses existing tools (git diff, SHA-256, pattern matching)
  integration_surface: 3  # Touches QA skill, dev skill, rules, source-tree
  domain_novelty: 2  # Novel concept but straightforward implementation
  overall: "Standard (Tier 2)"
  estimated_points: "21-34"

## Epic Decomposition (Recommended)

epics:
  - name: "EPIC-085: QA Diff Regression Detection"
    priority: "P0 (Must Have)"
    features:
      - "FR-001: Git diff regression detection phase in QA workflow"
      - "FR-002: Red-phase test integrity checksum system"
      - "FR-003: Test tampering heuristic pattern detection"
      - "FR-004: Test folder write protection rule"
      - "FR-005: Operational safety rules (Write tool, no /tmp/)"
    dependencies:
      - "ADR for source-tree.md update (snapshot directory)"

## Next Action

next_action: "/create-epic qa-diff-regression-detection"
mode: "brownfield"
recommended_workflow: "Create epic → Create stories → Implement via /dev"
