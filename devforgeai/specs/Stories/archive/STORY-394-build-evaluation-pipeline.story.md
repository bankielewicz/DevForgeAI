---
id: STORY-394
title: "Build Before/After Evaluation Pipeline for Agent Migration"
type: feature
epic: EPIC-062
sprint: Backlog
status: QA Approved
points: 8
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: Unassigned
created: 2026-02-06
format_version: "2.8"
---

# Story: Build Before/After Evaluation Pipeline for Agent Migration

## Description

**As a** Framework Owner,
**I want** a before/after evaluation pipeline with a structured scoring rubric that runs entirely within Claude Code Terminal,
**so that** I can objectively measure quality improvements when migrating agents to the unified template, enabling data-driven go/no-go decisions for each rollout wave.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-010" section="problem-statement">
    <quote>"DevForgeAI framework stakeholders experience inconsistent and unreliable results from subagents and skills because prompts were written ad-hoc without a systematic methodology based on proven prompt engineering principles"</quote>
    <line_reference>BRAINSTORM-010, lines 99-100</line_reference>
    <quantified_impact>32+ subagents, 17 skills, 39 commands producing inconsistent quality — evaluation pipeline enables objective measurement of improvement</quantified_impact>
  </origin>

  <decision rationale="claude-code-terminal-only-evaluation">
    <selected>Structured Markdown-based evaluation pipeline using Read/Write/Grep tools within Claude Code Terminal</selected>
    <rejected alternative="external-eval-tools">
      External evaluation frameworks (LangSmith, PromptFoo, etc.) explicitly excluded as Out of Scope per EPIC-062 and brainstorm Won't Have
    </rejected>
    <rejected alternative="automated-optimization">
      Self-improving or automated prompt optimization excluded per brainstorm Won't Have — human review required
    </rejected>
    <trade_off>Manual execution per component trades speed for reliability and human oversight</trade_off>
  </decision>

  <stakeholder role="Framework Owner" goal="objective-quality-measurement">
    <quote>"Evaluation pipeline produces objective quality scores (not subjective assessment)"</quote>
    <source>EPIC-062, Success Metrics, Metric 2</source>
  </stakeholder>

  <hypothesis id="H1" validation="pilot-evaluation" success_criteria="3 pilot agents show measurable quality improvement in before/after scores">
    Applying Anthropic prompt engineering patterns to DevForgeAI agents produces measurably better output quality as scored by a structured rubric
  </hypothesis>
</provenance>
```

## Acceptance Criteria

### AC#1: Scoring Rubric Defined with Objective Quality Dimensions

```xml
<acceptance_criteria id="AC1">
  <given>The need for objective quality measurement across agent migrations</given>
  <when>The scoring rubric document is created at devforgeai/specs/research/evaluation-rubric.md</when>
  <then>The rubric contains at minimum 5 independently scorable quality dimensions, each with: (1) a clear name and definition, (2) a 1-5 numeric scale with explicit descriptors for scores 1, 3, and 5, (3) at least one concrete example per score level, (4) a weighting factor (sum of all weights = 100%), and the rubric is agent-agnostic (not hardcoded to any specific agent). Suggested dimensions include: Task Completion Accuracy, Output Structure Compliance, Edge Case Handling, Instruction Adherence, and Conciseness/Token Efficiency.</then>
  <verification>
    <source_files>
      <file hint="Scoring rubric definition">devforgeai/specs/research/evaluation-rubric.md</file>
    </source_files>
    <test_file>tests/STORY-394/test_ac1_scoring_rubric.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Before-State Capture Mechanism

```xml
<acceptance_criteria id="AC2">
  <given>An agent exists in .claude/agents/ with a current (pre-migration) system prompt</given>
  <when>The before-state capture process is executed for that agent</when>
  <then>A structured before-state snapshot is produced containing: (1) agent name and file path, (2) capture timestamp, (3) full system prompt text (or hash for reference), (4) a set of 3+ standardized evaluation prompts appropriate to the agent's role, (5) the agent's output for each evaluation prompt, (6) rubric scores for each output across all dimensions, and the snapshot is stored in devforgeai/specs/research/evaluation-results.md under a clearly identifiable section for that agent. The capture process works for ANY agent (not hardcoded to pilot agents).</then>
  <verification>
    <source_files>
      <file hint="Evaluation results storage">devforgeai/specs/research/evaluation-results.md</file>
      <file hint="Capture process documentation">devforgeai/specs/research/evaluation-pipeline.md</file>
    </source_files>
    <test_file>tests/STORY-394/test_ac2_before_state_capture.sh</test_file>
    <coverage_threshold>85</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: After-State Comparison with Numeric Scores

```xml
<acceptance_criteria id="AC3">
  <given>A before-state snapshot exists for an agent AND the agent has been migrated to the unified template</given>
  <when>The after-state evaluation is executed using the same evaluation prompts from the before-state</when>
  <then>The pipeline produces: (1) after-state scores for each rubric dimension, (2) a delta (change) for each dimension comparing before vs. after, (3) a weighted composite score for both before and after states, (4) a composite delta showing overall improvement or regression, (5) a pass/fail determination based on a configurable threshold (default: composite delta >= 0, meaning no regression), and all results are appended to the agent's section in devforgeai/specs/research/evaluation-results.md.</then>
  <verification>
    <source_files>
      <file hint="Evaluation results with comparison">devforgeai/specs/research/evaluation-results.md</file>
    </source_files>
    <test_file>tests/STORY-394/test_ac3_after_state_comparison.sh</test_file>
    <coverage_threshold>85</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Evaluation Results Stored in Structured Format

```xml
<acceptance_criteria id="AC4">
  <given>One or more agents have been evaluated (before and/or after state)</given>
  <when>The evaluation results file is examined</when>
  <then>devforgeai/specs/research/evaluation-results.md contains: (1) a summary table listing all evaluated agents with their before score, after score, delta, and pass/fail, (2) per-agent detail sections with dimension-level breakdown, (3) evaluation prompt text and output excerpts (or references) used for scoring, (4) timestamps for each evaluation run, (5) rubric version identifier used for each evaluation, and the file follows Markdown format consistent with devforgeai/specs/ conventions.</then>
  <verification>
    <source_files>
      <file hint="Structured results file">devforgeai/specs/research/evaluation-results.md</file>
    </source_files>
    <test_file>tests/STORY-394/test_ac4_results_format.sh</test_file>
    <coverage_threshold>85</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Pipeline Reusability Across Migration Waves

```xml
<acceptance_criteria id="AC5">
  <given>The evaluation pipeline has been used for 3 pilot agents in Sprint 1</given>
  <when>Wave 1 rollout begins (10 validator/analyzer agents) in Sprint 3</when>
  <then>The same pipeline process, rubric, and results format can be applied to Wave 1 agents without modification to the pipeline itself. Specifically: (1) the evaluation-pipeline.md process document uses agent name as a parameter (not hardcoded agent references), (2) evaluation prompts are categorizable by agent role type (validator, implementor, reviewer, etc.) enabling prompt reuse across agents of the same type, (3) results accumulate in the same evaluation-results.md file with clear wave/sprint identifiers, (4) the rubric dimensions apply equally to all agent types.</then>
  <verification>
    <source_files>
      <file hint="Pipeline process document">devforgeai/specs/research/evaluation-pipeline.md</file>
      <file hint="Rubric document">devforgeai/specs/research/evaluation-rubric.md</file>
    </source_files>
    <test_file>tests/STORY-394/test_ac5_pipeline_reusability.sh</test_file>
    <coverage_threshold>85</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Rollback Decision Support

```xml
<acceptance_criteria id="AC6">
  <given>An after-state evaluation shows regression (composite delta less than 0) for an agent</given>
  <when>The evaluation results are reviewed</when>
  <then>The pipeline output clearly indicates: (1) which specific dimensions regressed and by how much, (2) a ROLLBACK RECOMMENDED flag when composite delta is below the configurable threshold, (3) the specific file path of the agent that should be rolled back, and the evaluation-pipeline.md documents the rollback exercise process (per EPIC-062 requirement: "Rollback exercised for at least 1 component to verify capability").</then>
  <verification>
    <source_files>
      <file hint="Pipeline with rollback guidance">devforgeai/specs/research/evaluation-pipeline.md</file>
      <file hint="Results showing regression handling">devforgeai/specs/research/evaluation-results.md</file>
    </source_files>
    <test_file>tests/STORY-394/test_ac6_rollback_support.sh</test_file>
    <coverage_threshold>85</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "EvaluationRubric"
      file_path: "devforgeai/specs/research/evaluation-rubric.md"
      requirements:
        - id: "RUBRIC-001"
          description: "Define 5+ quality dimensions with 1-5 numeric scales and explicit descriptors for scores 1, 3, and 5"
          testable: true
          test_requirement: "Test: File contains at least 5 dimension headings, each with score descriptors for 1, 3, and 5"
          priority: "Critical"
          implements_ac: ["AC1"]
        - id: "RUBRIC-002"
          description: "Include weighting factors that sum to 100%"
          testable: true
          test_requirement: "Test: Parse weight values from file, verify sum equals 100 (+/- 1%)"
          priority: "Critical"
          implements_ac: ["AC1"]
        - id: "RUBRIC-003"
          description: "Include concrete examples per score level per dimension"
          testable: true
          test_requirement: "Test: Each dimension section contains at least 1 example per score level (1, 3, 5)"
          priority: "High"
          implements_ac: ["AC1"]
        - id: "RUBRIC-004"
          description: "Include version identifier for rubric evolution tracking"
          testable: true
          test_requirement: "Test: File contains version identifier in header (e.g., Rubric Version: 1.0)"
          priority: "High"
          implements_ac: ["AC1"]

    - type: "Configuration"
      name: "EvaluationPipeline"
      file_path: "devforgeai/specs/research/evaluation-pipeline.md"
      dependencies: ["evaluation-rubric.md", "evaluation-results.md"]
      requirements:
        - id: "PIPE-001"
          description: "Document step-by-step before-state capture process with parameterized agent name"
          testable: true
          test_requirement: "Test: Process steps reference {agent_name} as parameter, not hardcoded agent names"
          priority: "Critical"
          implements_ac: ["AC2"]
        - id: "PIPE-002"
          description: "Document after-state comparison process with delta calculation"
          testable: true
          test_requirement: "Test: Process includes explicit delta calculation formula and pass/fail determination"
          priority: "Critical"
          implements_ac: ["AC3"]
        - id: "PIPE-003"
          description: "Document rollback decision criteria and exercise process"
          testable: true
          test_requirement: "Test: Process includes rollback section with threshold-based ROLLBACK RECOMMENDED flag"
          priority: "High"
          implements_ac: ["AC6"]
        - id: "PIPE-004"
          description: "Document evaluation prompt creation guidelines by agent role type"
          testable: true
          test_requirement: "Test: Guidelines cover at least 4 agent role categories with example prompts"
          priority: "High"
          implements_ac: ["AC5"]
        - id: "PIPE-005"
          description: "Document results file format and update procedure"
          testable: true
          test_requirement: "Test: Format specification matches what AC#4 requires in evaluation-results.md"
          priority: "Medium"
          implements_ac: ["AC4"]

    - type: "DataModel"
      name: "EvaluationResults"
      file_path: "devforgeai/specs/research/evaluation-results.md"
      purpose: "Structured storage for before/after evaluation scores across all agent migrations"
      fields:
        - name: "SummaryTable"
          type: "Markdown Table"
          constraints: "Required, columns: Agent | Wave | Before Score | After Score | Delta | Pass/Fail"
          description: "Top-level summary of all evaluated agents"
          test_requirement: "Test: File header contains Markdown table with 6 required columns"
        - name: "AgentDetailSection"
          type: "Markdown Section"
          constraints: "Required per evaluated agent"
          description: "Per-agent breakdown with dimension-level before/after/delta scores"
          test_requirement: "Test: Each evaluated agent has subsection with per-dimension rows"
        - name: "Timestamp"
          type: "ISO 8601 DateTime"
          constraints: "Required per evaluation entry"
          description: "When the evaluation was performed"
          test_requirement: "Test: Each evaluation entry includes ISO 8601 timestamp"
        - name: "RubricVersion"
          type: "String (semver)"
          constraints: "Required per evaluation entry"
          description: "Which rubric version was used for scoring"
          test_requirement: "Test: Each evaluation entry includes rubric version reference"

  business_rules:
    - id: "BR-001"
      rule: "All numeric scores must be integers in range 1-5 inclusive"
      test_requirement: "Test: No score values outside 1-5 range in results file"
      priority: "Critical"
    - id: "BR-002"
      rule: "Dimension weights must sum to exactly 100% (tolerance: +/- 1%)"
      test_requirement: "Test: Sum of weights in rubric equals 100 within tolerance"
      priority: "Critical"
    - id: "BR-003"
      rule: "Composite score = SUM(dimension_score * dimension_weight) for all dimensions"
      test_requirement: "Test: Recalculate composite from per-dimension scores; verify match"
      priority: "Critical"
    - id: "BR-004"
      rule: "Delta = after_score - before_score (positive = improvement, negative = regression)"
      test_requirement: "Test: Verify delta values match difference of before and after scores"
      priority: "High"
    - id: "BR-005"
      rule: "Pass/fail threshold configurable, default >= 0 (no regression)"
      test_requirement: "Test: Pipeline document specifies configurable threshold with default"
      priority: "High"
    - id: "BR-006"
      rule: "Pipeline must use agent name as parameter (not hardcoded to specific agents)"
      test_requirement: "Test: Grep for hardcoded agent names in pipeline; expect 0 matches in process steps"
      priority: "High"
    - id: "BR-007"
      rule: "Minimum 3 evaluation prompts per agent"
      test_requirement: "Test: Each agent evaluation section contains at least 3 evaluation prompt entries"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Single agent evaluation completes within 1 Claude Code session"
      metric: "< 30 minutes wall-clock time per agent evaluation"
      test_requirement: "Test: Pipeline document specifies time target per agent"
      priority: "High"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Partial evaluation recovery: completed scores persist if session ends mid-evaluation"
      metric: "All completed scores written to evaluation-results.md before proceeding to next agent"
      test_requirement: "Test: Pipeline document specifies write-after-each-agent pattern"
      priority: "High"
    - id: "NFR-003"
      category: "Scalability"
      requirement: "Pipeline supports 1 agent (pilot) up to 39 agents (full roster) without structural changes"
      metric: "Same pipeline document, rubric, and results format used for all waves"
      test_requirement: "Test: Pipeline makes no wave-specific structural assumptions"
      priority: "Medium"
    - id: "NFR-004"
      category: "Security"
      requirement: "No external API calls, no sensitive data in evaluation prompts"
      metric: "Zero network requests, zero PII in evaluation artifacts"
      test_requirement: "Test: Pipeline document explicitly prohibits external calls and PII"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Claude Code Terminal"
    limitation: "Cannot run identical prompts through 'old' and 'new' agent versions simultaneously — must evaluate sequentially (before snapshot, then migrate, then after evaluation)"
    decision: "workaround:Sequential evaluation with snapshots stored in Markdown files"
    discovered_phase: "Architecture"
    impact: "Evaluation requires two sessions per agent (before + after), not side-by-side comparison"
  - id: TL-002
    component: "Evaluation consistency"
    limitation: "Claude's outputs are non-deterministic — same prompt may produce different quality outputs on repeated runs"
    decision: "workaround:Document 'best of 1' approach with note about variance; recommend re-run for borderline scores"
    discovered_phase: "Architecture"
    impact: "Scores have inherent variance; pipeline documents this and provides guidance"
  - id: TL-003
    component: "Scoring subjectivity"
    limitation: "Even with rubric, human scoring of LLM output has subjective elements — different evaluators may assign different scores"
    decision: "workaround:Detailed rubric descriptors and examples minimize subjectivity; document that Framework Owner is sole evaluator for consistency"
    discovered_phase: "Architecture"
    impact: "Single evaluator (Framework Owner) ensures consistency; rubric examples reduce variance"
```

---

## Non-Functional Requirements (NFRs)

### Performance
- Single agent evaluation (before OR after state): < 30 minutes wall-clock time
- Rubric scoring for 1 agent across all dimensions: < 5 minutes
- Results file write/update: < 10 seconds per agent entry
- Batch evaluation of 10 agents in a wave: completable within 3 Claude Code sessions

### Security
- No external API calls or network requests required
- No sensitive data in evaluation prompts (no PII, credentials)
- Results stored in version-controlled Markdown (auditable via git)
- No executable code in pipeline artifacts

### Reliability
- Pipeline documented as step-by-step process (not session-dependent)
- Results persist across sessions via Markdown files
- Partial evaluation recovery: completed scores written immediately
- Idempotent scoring: re-run overwrites existing entry

### Scalability
- Supports 1 agent up to 39 agents without structural changes
- Results accumulate across 4+ migration waves
- Evaluation prompts organized by agent role type (7 categories)
- Rubric dimensions universally applicable

---

## Edge Cases

1. **Agent with no clear "output" to evaluate:** Some agents (e.g., `context-validator`, `deferral-validator`) produce pass/fail verdicts rather than rich text output. The rubric must accommodate binary-output agents by weighting "Task Completion Accuracy" higher and "Conciseness/Token Efficiency" lower.

2. **Rubric version changes mid-rollout:** If the rubric is refined after pilot evaluation, previously captured before-state scores become incomparable. Pipeline must version the rubric and record which version was used for each evaluation. Re-evaluation required if rubric changes.

3. **Non-deterministic agent output:** Claude's responses vary between invocations even with identical prompts. Mitigation: document "best of 1" approach with note about variance; recommend re-run for borderline scores.

4. **Agent has no pre-migration state (new agent):** If an agent is created fresh during migration, there is no before-state. Pipeline marks as "NEW — no before-state" and evaluates only after-state.

5. **Evaluation prompts inappropriate for agent role:** Generic prompts may not exercise specialized capabilities. Pipeline must support role-specific evaluation prompt sets categorized by agent type.

6. **Very large evaluation-results.md over multiple waves:** After evaluating 39+ agents, results file grows large. Mitigate by considering per-wave split files while maintaining summary index.

---

## Dependencies

### Prerequisite Stories
None — the evaluation pipeline can be built independently of the pilot migrations.

### External Dependencies
None — all work within Claude Code Terminal.

### Technology Dependencies
None — uses only Markdown files and standard Read/Write/Edit/Grep tools.

---

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** Rubric file contains 5+ dimensions with proper scoring scales
2. **Happy Path:** Pipeline document uses parameterized agent names
3. **Happy Path:** Results file contains summary table with required columns
4. **Edge Cases:** Rubric weights sum exactly to 100%
5. **Edge Cases:** Score validation rejects values outside 1-5 range
6. **Error Cases:** Missing rubric version detected

### Integration Tests
**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **End-to-End:** Complete before-state capture for a mock agent
2. **End-to-End:** After-state comparison produces correct deltas
3. **Regression:** Rollback flag triggered on negative delta
4. **Reusability:** Pipeline works for agents of different role types

---

## Acceptance Criteria Verification Checklist

### AC#1: Scoring Rubric
- [ ] 5+ quality dimensions defined - **Phase:** 3 - **Evidence:** test_ac1_scoring_rubric.sh
- [ ] 1-5 numeric scale with descriptors per dimension - **Phase:** 3 - **Evidence:** test_ac1_scoring_rubric.sh
- [ ] Concrete examples per score level - **Phase:** 3 - **Evidence:** test_ac1_scoring_rubric.sh
- [ ] Weights sum to 100% - **Phase:** 3 - **Evidence:** test_ac1_scoring_rubric.sh
- [ ] Rubric is agent-agnostic - **Phase:** 3 - **Evidence:** test_ac1_scoring_rubric.sh

### AC#2: Before-State Capture
- [ ] Agent name and file path captured - **Phase:** 3 - **Evidence:** test_ac2_before_state_capture.sh
- [ ] Capture timestamp recorded - **Phase:** 3 - **Evidence:** test_ac2_before_state_capture.sh
- [ ] 3+ evaluation prompts per agent - **Phase:** 3 - **Evidence:** test_ac2_before_state_capture.sh
- [ ] Rubric scores for each output - **Phase:** 3 - **Evidence:** test_ac2_before_state_capture.sh
- [ ] Works for ANY agent (not hardcoded) - **Phase:** 5 - **Evidence:** test_ac2_before_state_capture.sh

### AC#3: After-State Comparison
- [ ] After-state scores produced - **Phase:** 3 - **Evidence:** test_ac3_after_state_comparison.sh
- [ ] Delta per dimension calculated - **Phase:** 3 - **Evidence:** test_ac3_after_state_comparison.sh
- [ ] Weighted composite scores - **Phase:** 3 - **Evidence:** test_ac3_after_state_comparison.sh
- [ ] Pass/fail determination - **Phase:** 3 - **Evidence:** test_ac3_after_state_comparison.sh

### AC#4: Results Format
- [ ] Summary table with required columns - **Phase:** 3 - **Evidence:** test_ac4_results_format.sh
- [ ] Per-agent detail sections - **Phase:** 3 - **Evidence:** test_ac4_results_format.sh
- [ ] Timestamps and rubric version - **Phase:** 3 - **Evidence:** test_ac4_results_format.sh

### AC#5: Pipeline Reusability
- [ ] Parameterized agent name (not hardcoded) - **Phase:** 3 - **Evidence:** test_ac5_pipeline_reusability.sh
- [ ] Role-type evaluation prompt categories - **Phase:** 3 - **Evidence:** test_ac5_pipeline_reusability.sh
- [ ] Results accumulate across waves - **Phase:** 5 - **Evidence:** test_ac5_pipeline_reusability.sh
- [ ] Rubric dimensions universal - **Phase:** 3 - **Evidence:** test_ac5_pipeline_reusability.sh

### AC#6: Rollback Decision Support
- [ ] Regression dimensions identified - **Phase:** 3 - **Evidence:** test_ac6_rollback_support.sh
- [ ] ROLLBACK RECOMMENDED flag - **Phase:** 3 - **Evidence:** test_ac6_rollback_support.sh
- [ ] Agent file path for rollback - **Phase:** 3 - **Evidence:** test_ac6_rollback_support.sh
- [ ] Rollback exercise process documented - **Phase:** 3 - **Evidence:** test_ac6_rollback_support.sh

---

**Checklist Progress:** 0/27 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] Evaluation rubric created with 5+ dimensions, 1-5 scales, weights summing to 100%
- [ ] Evaluation pipeline process documented with parameterized agent names
- [ ] Before-state capture process works for any agent
- [ ] After-state comparison produces per-dimension and composite deltas
- [ ] Pass/fail threshold configurable with default >= 0
- [ ] Results file format defined with summary table and per-agent details
- [ ] Rollback decision criteria and exercise process documented
- [ ] Evaluation prompt guidelines by agent role type documented

### Quality
- [ ] All 6 acceptance criteria have passing tests
- [ ] Edge cases handled (binary-output agents, rubric versioning, non-determinism)
- [ ] All data validation rules enforced (score range, weight sum, prompt count)
- [ ] Code coverage > 95% for business logic

### Testing
- [ ] Unit tests for rubric structure validation
- [ ] Unit tests for pipeline parameterization
- [ ] Unit tests for results format validation
- [ ] Integration test for complete before-state capture workflow
- [ ] Integration test for after-state comparison with delta calculation

### Documentation
- [ ] evaluation-rubric.md complete with dimensions, scales, weights, examples
- [ ] evaluation-pipeline.md complete with step-by-step process
- [ ] evaluation-results.md template initialized with summary table header

---

## Implementation Notes

- [x] Evaluation rubric created with 5+ dimensions, 1-5 scales, weights summing to 100% - Completed: devforgeai/specs/research/evaluation-rubric.md with 5 dimensions (Task Completion Accuracy 30%, Output Structure Compliance 20%, Edge Case Handling 20%, Instruction Adherence 15%, Conciseness/Token Efficiency 15%)
- [x] Evaluation pipeline process documented with parameterized agent names - Completed: devforgeai/specs/research/evaluation-pipeline.md uses {agent_name} parameter throughout (13 occurrences)
- [x] Before-state capture process works for any agent - Completed: Pipeline Step 1-6 documents parameterized capture process
- [x] After-state comparison produces per-dimension and composite deltas - Completed: Pipeline lines 101-150 document delta calculation with formula
- [x] Pass/fail threshold configurable with default >= 0 - Completed: Pipeline lines 140-149 document configurable threshold
- [x] Results file format defined with summary table and per-agent details - Completed: devforgeai/specs/research/evaluation-results.md with 3 pilot agents evaluated
- [x] Rollback decision criteria and exercise process documented - Completed: Pipeline lines 153-187 with 5-step rollback exercise process
- [x] Evaluation prompt guidelines by agent role type documented - Completed: Pipeline lines 31-37 with 4 role categories (Validator, Implementor, Reviewer, Analyzer)
- [x] All 6 acceptance criteria have passing tests - Completed: 57/57 tests pass across 6 AC test files
- [x] Edge cases handled (binary-output agents, rubric versioning, non-determinism) - Completed: Documented in story Edge Cases section and rubric
- [x] All data validation rules enforced (score range, weight sum, prompt count) - Completed: Tests verify BR-001 through BR-007
- [x] Unit tests for rubric structure validation - Completed: tests/STORY-394/test_ac1_scoring_rubric.sh (10 tests)
- [x] Unit tests for pipeline parameterization - Completed: tests/STORY-394/test_ac5_pipeline_reusability.sh (8 tests)
- [x] Unit tests for results format validation - Completed: tests/STORY-394/test_ac4_results_format.sh (12 tests)
- [x] Integration test for complete before-state capture workflow - Completed: tests/STORY-394/test_ac2_before_state_capture.sh (9 tests)
- [x] Integration test for after-state comparison with delta calculation - Completed: tests/STORY-394/test_ac3_after_state_comparison.sh (9 tests)
- [x] evaluation-rubric.md complete with dimensions, scales, weights, examples - Completed: 5 dimensions with 1-5 scales and concrete examples per score level
- [x] evaluation-pipeline.md complete with step-by-step process - Completed: Before-state (6 steps), After-state (4 steps), Rollback (5 steps)
- [x] evaluation-results.md template initialized with summary table header - Completed: Contains summary table with 3 pilot agent evaluations

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-13

### TDD Workflow Summary

- **Phase 02 (Red):** test-automator generated 6 AC test files with 57 total tests
- **Phase 03 (Green):** backend-architect created 3 Markdown implementation files (rubric, pipeline, results)
- **Phase 04 (Refactor):** refactoring-specialist and code-reviewer verified documentation quality
- **Phase 4.5:** ac-compliance-verifier identified AC#4 gap (missing prompt text/output references) - fixed
- **Phase 05:** integration-tester identified composite score arithmetic errors (BR-003 violation) - fixed
- **Phase 5.5:** ac-compliance-verifier confirmed all 6 ACs PASS with BR-003 arithmetic verified

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-06 | claude/story-requirements-analyst | Created | Story created from EPIC-062 Feature 4 | STORY-394.story.md |
| 2026-02-13 | .claude/qa-result-interpreter | QA Deep | PASSED: 57/57 tests, 3/3 validators, 0 violations | - |

## Notes

**Design Decisions:**
- Evaluation pipeline designed as a methodology document (not executable code) per tech-stack.md constraints
- Single evaluator (Framework Owner) ensures scoring consistency across all agents
- "Best of 1" evaluation approach chosen over multi-run averaging for practical session time management
- Rubric versioning enables evolution while maintaining comparability within a version

**Open Questions:**
- [ ] Should evaluation prompts be stored alongside the pipeline doc or in a separate prompt library? - **Owner:** Framework Owner - **Due:** Before development starts
- [ ] Should rubric evolution trigger re-evaluation of already-scored agents? - **Owner:** Framework Owner - **Due:** After pilot evaluation

**References:**
- EPIC-062: Pilot Improvement, Evaluation & Rollout
- BRAINSTORM-010: Prompt Engineering from Anthropic Repos
- EPIC-062 Success Metric 2: "Evaluation pipeline produces objective quality scores"
- EPIC-062 User Story 15: "As a Framework Owner, I want a before/after evaluation pipeline"

---

Story Template Version: 2.8
Last Updated: 2026-02-06
