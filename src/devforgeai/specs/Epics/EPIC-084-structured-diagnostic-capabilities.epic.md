---
id: EPIC-084
title: Structured Diagnostic Capabilities
status: Planning
start_date: 2026-02-23
target_date: 2026-03-15
total_points: 6
completed_points: 0
created: 2026-02-23
owner: Bryan
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
---

# Epic: Structured Diagnostic Capabilities

## Business Goal

Eliminate shotgun debugging from the DevForgeAI development workflow by introducing a structured "investigate before fixing" discipline. Currently, when tests fail, AC verification fails, QA gates block, or commits are rejected, the framework either HALTs or defers to manual recovery guides — there is no unified diagnostic methodology. This leads to agents retrying implementations without understanding why they failed, wasting development cycles and tokens.

This epic introduces three new framework artifacts and integrates them into the existing `/dev` and `/qa` workflows:

1. A **diagnostic skill** that enforces a 4-phase investigation methodology
2. A **read-only subagent** that cross-references implementation against constitutional context files to detect spec drift
3. A **workflow rule** that prevents fix attempts before diagnosis completes
4. **Integration hooks** into the existing TDD and QA workflows so diagnosis triggers automatically on failure

**Inspiration:** The [Superpowers framework](https://github.com/obra/superpowers) by Jesse Vincent includes a "systematic-debugging" skill. This epic adapts that concept into a DevForgeAI-native implementation with deeper integration — specifically constitutional context file awareness for spec drift detection, which Superpowers lacks entirely.

## Success Metrics

- **Metric 1:** Reduce average retry cycles on Green phase failures from 3+ to 1-2 (measured by comparing pre/post phase state files)
- **Metric 2:** 100% of workflow failures trigger structured diagnosis before fix attempts (measured by rule compliance in `/dev` logs)
- **Metric 3:** Spec drift detected as root cause category in applicable failures (measured by `<spec_violation>` presence in diagnostic output)
- **Metric 4:** Zero increase in successful workflow completion time (diagnosis only adds time on failure paths, not success paths)

**Measurement Plan:**
- Track via `devforgeai/feedback/ai-analysis/` post-dev hooks
- Baseline: Current retry behavior (no structured diagnosis)
- Review frequency: After first 5 stories developed with diagnostic capabilities active

## Scope

### In Scope

#### Feature 1: `root-cause-diagnosis` Skill (4-Phase Diagnostic Methodology)

A new skill at `.claude/skills/root-cause-diagnosis/SKILL.md` that enforces a strict 4-phase investigation sequence before any fix attempt is made. The skill is invoked as an **interrupt handler** — called when an existing workflow phase detects a failure, runs diagnosis, then returns control to the calling phase.

**4-Phase Methodology:**

| Phase | Name | Purpose | Output |
|-------|------|---------|--------|
| 1 | CAPTURE | Collect all failure evidence (error messages, exit codes, stack traces, failing test names, phase context) | `<diagnosis>` XML block |
| 2 | INVESTIGATE | Trace failure to origin. **Step 2a:** Check implementation against constitutional context files (spec drift detection). **Step 2b:** If specs pass, trace code execution path. | `<thinking>` block with investigation reasoning |
| 3 | HYPOTHESIZE | State a specific, falsifiable theory: "The failure occurs because [X] causes [Y], as evidenced by [Z]" | Hypothesis statement |
| 4 | PRESCRIBE | Recommend smallest possible fix targeting root cause. If fix fails → return to Phase 2. If 3+ failures → escalate as architectural issue. | `<prescription>` XML block |

**Critical Rule:** NO FIX ATTEMPTS UNTIL PHASE 2 (INVESTIGATE) COMPLETES. This is the core principle that prevents shotgun debugging.

**Skill Structure (Anthropic Agent Skills Spec compliant):**
```
.claude/skills/root-cause-diagnosis/
├── SKILL.md                              # Core methodology (~200 lines, <500 line limit)
└── references/
    ├── investigation-patterns.md         # Categorized failure patterns by type
    └── workflow-integration.md           # How skill integrates with /dev and /qa
```

**YAML Frontmatter:**
```yaml
---
name: root-cause-diagnosis
description: |
  Structured diagnostic methodology for investigating test failures, validation
  errors, and workflow blocks within DevForgeAI development phases. Use when
  tests fail unexpectedly, Green phase implementation doesn't pass tests,
  integration tests break, QA coverage falls below thresholds, AC verification
  fails, or commit hooks block. Enforces investigate-before-fix discipline
  to prevent shotgun debugging.
license: MIT
metadata:
  author: DevForgeAI
  version: "1.0.0"
  category: workflow-automation
  last-updated: "2026-02-23"
allowed-tools: Read Grep Glob Task
---
```

**Trigger Conditions (when skill is invoked):**

| Trigger | Calling Phase | Current Behavior | With Diagnosis |
|---------|--------------|------------------|----------------|
| Tests pass when they should fail | Phase 02 (Red) | Manual investigation | Diagnose: wrong assertions? stale mocks? |
| Tests still fail after implementation | Phase 03 (Green) | Re-invoke backend-architect | Diagnose root cause BEFORE retrying |
| Integration tests fail | Phase 05 | Integration-tester reports | Diagnose: contract mismatch? environment? |
| AC verification fails | Phase 04.5/05.5 | HALT immediately | Diagnose which AC failed and why |
| Coverage below threshold | QA Phase 2 | gaps.json created | Diagnose: which paths uncovered? why? |
| Pre-commit hook blocks | Phase 08 | Read recovery guide | Existing recovery guide preferred |

**`references/investigation-patterns.md` contents — 6 failure categories:**

1. **Spec Drift (CHECK FIRST):** Technology violation (not in tech-stack.md), source tree violation (wrong directory per source-tree.md), dependency violation (per dependencies.md), coding standard violation (per coding-standards.md), architecture violation (per architecture-constraints.md), anti-pattern match (per anti-patterns.md)
2. **Test Assertion Failures:** Wrong expected value, stale snapshot, missing mock, type mismatch
3. **Import/Dependency Failures:** Module not found, version mismatch, circular dependency
4. **Coverage Gaps:** Uncovered branches, untested error paths, layer misclassification
5. **Anti-Pattern Violations:** God object (>500 lines), direct instantiation, hardcoded values
6. **DoD/Commit Validation Failures:** Subsection nesting, text mismatch, missing items

**`references/workflow-integration.md` contents — exact integration pseudocode:**

Phase 03 (Green) integration:
```
AFTER backend-architect/frontend-developer produces implementation:
  Run test suite
  IF tests still fail (exit code != 0):
    BEFORE retrying implementation:
      Invoke Skill("root-cause-diagnosis")
      Pass: test output, implementation files, story context
      Receive: <prescription> with targeted fix
      Apply fix based on diagnosis
    Do NOT re-invoke backend-architect without diagnosis first
```

Phase 05 (Integration) integration:
```
AFTER integration-tester runs:
  IF integration tests fail:
    Invoke Task(subagent_type="diagnostic-analyst")
    Pass: integration test output, component boundaries
    Receive: root cause analysis
```

QA Phase 2 integration:
```
AFTER coverage-analyzer AND anti-pattern-scanner complete:
  IF coverage below threshold (95/85/80) OR critical anti-patterns found:
    Invoke Task(subagent_type="diagnostic-analyst")
    Attach diagnosis to gaps.json for richer remediation context
```

---

#### Feature 2: `diagnostic-analyst` Read-Only Subagent with Constitutional Context File Awareness

A new subagent at `.claude/agents/diagnostic-analyst.md` that can be delegated diagnostic work via `Task(subagent_type="diagnostic-analyst")`. This subagent is **read-only by design** — it has tools `[Read, Grep, Glob]` only (no Write, Edit, or Bash) to ensure diagnosis never accidentally modifies code.

**Key differentiator — Constitutional Context File Awareness:**

The subagent's Phase 2 (INVESTIGATE) starts with **Step 2a: Spec Compliance Check** — before tracing code, it loads the relevant constitutional context files and compares implementation against spec. This catches **spec drift** (implementation diverging from specs) as the #1 hidden root cause category.

| Context File | What It Catches |
|---|---|
| `devforgeai/specs/context/tech-stack.md` | Wrong technology used, prohibited library imported |
| `devforgeai/specs/context/source-tree.md` | File in wrong location, test path mismatch |
| `devforgeai/specs/context/dependencies.md` | Missing or conflicting dependency |
| `devforgeai/specs/context/coding-standards.md` | Pattern violation causing test failure |
| `devforgeai/specs/context/architecture-constraints.md` | Layer violation, SRP breach, wrong pattern |
| `devforgeai/specs/context/anti-patterns.md` | Known anti-pattern causing the failure |

**Subagent output format — structured XML:**
```xml
<diagnosis>
  <phase>Phase where failure occurred</phase>
  <error>Exact error message</error>
  <exit_code>Exit code</exit_code>
  <failing_tests>List of failing test names</failing_tests>
  <context>Story ID, file paths involved</context>
</diagnosis>

<prescription>
  <hypothesis>Specific theory with evidence</hypothesis>
  <spec_violation>Context file and rule violated, if any</spec_violation>
  <fix>Specific change (file, line, what to change)</fix>
  <expected_result>Which tests should pass after fix</expected_result>
  <confidence>high|medium|low</confidence>
</prescription>
```

**Complete subagent definition (to be written to `.claude/agents/diagnostic-analyst.md`):**

```yaml
---
name: diagnostic-analyst
description: >
  Read-only failure investigation specialist following structured diagnosis
  methodology with constitutional context file awareness. Use when test
  failures, validation errors, or quality gate blocks need root cause analysis
  before fix attempts. Cross-references implementation against the 6
  DevForgeAI context files (tech-stack, source-tree, dependencies,
  coding-standards, architecture-constraints, anti-patterns) to detect
  spec drift as a root cause. Never modifies code — diagnosis only.
tools:
  - Read
  - Grep
  - Glob
---
```

**Subagent methodology sections:**
1. Role definition: "You are a diagnostic analyst investigating a software failure"
2. Constitutional Context Files section listing all 6 files with their purposes
3. 4-phase methodology (CAPTURE → INVESTIGATE with Step 2a/2b → HYPOTHESIZE → PRESCRIBE)
4. Critical rules (never modify code, never suggest fixes before Phase 2, always check context files first, cite sources)

**CLAUDE.md registry entries:**
- Subagent table: `| diagnostic-analyst | Read-only failure investigation specialist... | [Read, Grep, Glob] |`
- Proactive triggers:
  - `when Phase 03 tests fail after implementation → diagnostic-analyst`
  - `when Phase 05 integration tests fail → diagnostic-analyst`
  - `when QA Phase 2 detects coverage gaps or critical anti-patterns → diagnostic-analyst`
  - `when AC verification fails in Phase 04.5/05.5 → diagnostic-analyst`

---

#### Feature 3: `diagnosis-before-fix` Workflow Rule

A new rule at `.claude/rules/workflow/diagnosis-before-fix.md` that establishes the principle: **when a failure occurs, diagnose before retrying**.

**Rule content:**
1. When a test, validation, or quality gate fails: Do NOT immediately retry or modify code
2. First invoke the `root-cause-diagnosis` skill or `diagnostic-analyst` subagent
3. Understand WHY the failure occurred before attempting a fix
4. If 3+ fix attempts fail without diagnosis, HALT and escalate to user

**Applies to:** Phase 02 (Red), Phase 03 (Green), Phase 05 (Integration), Phase 04.5/05.5 (AC Verification), QA Phase 2

**Exceptions:**
- Phase 08 commit failures: Use existing `commit-failure-recovery.md` guide first (already has structured DoD diagnosis)
- Trivial failures with obvious cause (e.g., typo in import path): Fix directly, document rationale

**References within the rule:** Links to `.claude/skills/root-cause-diagnosis/SKILL.md`, `.claude/agents/diagnostic-analyst.md`, and `.claude/rules/workflow/commit-failure-recovery.md`

---

#### Feature 4: Integration Hooks into Existing Workflows

Modify two existing skills to invoke diagnosis on failure:

**File 1: `.claude/skills/implementing-stories/SKILL.md`**
- **Phase 03 (Green):** After test execution, if tests still fail → invoke `Skill("root-cause-diagnosis")` before retrying implementation. Do NOT re-invoke backend-architect without diagnosis.
- **Phase 05 (Integration):** After integration-tester reports failures → invoke `Task(subagent_type="diagnostic-analyst")` to categorize failure (contract mismatch / environment / mock vs real).

**File 2: `.claude/skills/devforgeai-qa/SKILL.md`**
- **Phase 2 (Analysis):** After coverage-analyzer and anti-pattern-scanner report failures → invoke `Task(subagent_type="diagnostic-analyst")` and attach diagnosis to gaps.json entries.

**File 3: `CLAUDE.md`**
- Add `diagnostic-analyst` to subagent registry table and proactive trigger mapping.

**Non-regression requirement:** Diagnosis only triggers on failure paths. When no failures occur, the `/dev` and `/qa` workflows complete with zero additional overhead.

### Out of Scope

- ❌ Automated fix application (diagnosis prescribes, human/agent applies — separation of concerns)
- ❌ Persistent diagnostic history across sessions (stateless per invocation)
- ❌ Integration with Phase 08 commit failures (already covered by `commit-failure-recovery.md`)
- ❌ RCA document generation (existing `/rca` command handles post-mortem documentation)
- ❌ QA remediation story creation (existing `/review-qa-reports` handles gap-to-story conversion)

## Target Sprints

### Sprint 1: Foundation (Features 1-3)

**Goal:** Create the core diagnostic artifacts — skill, subagent, and rule
**Estimated Points:** 3
**Stories:**
- STORY-491: Create root-cause-diagnosis skill, diagnostic-analyst subagent, and diagnosis-before-fix rule

**Key Deliverables:**
- `.claude/skills/root-cause-diagnosis/SKILL.md` with 4-phase methodology
- `.claude/skills/root-cause-diagnosis/references/investigation-patterns.md`
- `.claude/skills/root-cause-diagnosis/references/workflow-integration.md`
- `.claude/agents/diagnostic-analyst.md` with read-only tools and context file awareness
- `.claude/rules/workflow/diagnosis-before-fix.md`

### Sprint 2: Integration (Feature 4)

**Goal:** Wire diagnostic hooks into existing workflows
**Estimated Points:** 3
**Stories:**
- STORY-496: Integrate diagnostic hooks into implementing-stories and devforgeai-qa skills

**Key Deliverables:**
- Modified `.claude/skills/implementing-stories/SKILL.md` (Phase 03, Phase 05 hooks)
- Modified `.claude/skills/devforgeai-qa/SKILL.md` (Phase 2 hooks)
- Updated `CLAUDE.md` subagent registry

**Dependency:** STORY-491 must complete first (Sprint 1)

## User Stories

1. **As a** DevForgeAI framework agent executing the Green phase, **I want** a structured diagnostic methodology to trigger automatically when my tests fail after implementation, **so that** I identify the root cause before retrying rather than blindly re-invoking the backend-architect.

2. **As a** DevForgeAI framework agent running QA validation, **I want** the diagnostic-analyst subagent to cross-reference my implementation against the 6 constitutional context files, **so that** spec drift is detected as a root cause category with cited evidence from the violated context file.

3. **As a** DevForgeAI developer, **I want** a workflow rule that prevents fix attempts before root cause investigation completes, **so that** shotgun debugging is eliminated from the framework's behavior.

## Technical Considerations

### Architecture Impact

- **New skill directory:** `.claude/skills/root-cause-diagnosis/` (3 files)
- **New subagent:** `.claude/agents/diagnostic-analyst.md` (1 file)
- **New rule:** `.claude/rules/workflow/diagnosis-before-fix.md` (1 file)
- **Modified skills:** `implementing-stories/SKILL.md` (+20 lines), `devforgeai-qa/SKILL.md` (+10 lines)
- **Modified registry:** `CLAUDE.md` (+5 lines for subagent table + trigger mapping)
- **No new dependencies or technology additions** — all artifacts are markdown/YAML configuration files

### Technology Decisions

- **Skill follows Anthropic Agent Skills Specification v1.0** — kebab-case name, ≤1024 char description, SKILL.md <500 lines, progressive disclosure via references/
- **Subagent is read-only by design** — tools restricted to `[Read, Grep, Glob]` per least-privilege principle in `architecture-constraints.md`
- **XML output format** — `<diagnosis>` and `<prescription>` blocks for structured, parseable diagnostic output (per Anthropic prompt engineering best practices for XML tags)

### Performance Requirements

- Diagnosis adds zero overhead on success paths (only triggers on failure)
- Skill SKILL.md under 500 lines (progressive disclosure compliance)
- Subagent under 500 lines (source-tree.md limit)
- Rule under 200 lines (conditional rule budget)

## Dependencies

### Internal Dependencies

- [x] **6 constitutional context files exist** in `devforgeai/specs/context/`
  - **Status:** Complete (all 6 present)
  - **Impact if missing:** Spec drift detection degrades gracefully (skips missing files)

- [x] **implementing-stories skill exists** at `.claude/skills/implementing-stories/SKILL.md`
  - **Status:** Complete
  - **Impact if missing:** Feature 4 integration cannot proceed

- [x] **devforgeai-qa skill exists** at `.claude/skills/devforgeai-qa/SKILL.md`
  - **Status:** Complete
  - **Impact if missing:** Feature 4 QA integration cannot proceed

### External Dependencies

- None (all artifacts are framework-internal configuration files)

## Risks & Mitigation

### Risk 1: Diagnosis adds latency to failure recovery

- **Probability:** Medium
- **Impact:** Low (only affects failure paths, not success paths)
- **Mitigation:** Skill is lightweight (~200 lines). Subagent reads are parallelizable. Phase 1 (CAPTURE) uses only in-context data (no file I/O).
- **Contingency:** If latency is unacceptable, make diagnosis opt-in via a flag rather than automatic.

### Risk 2: Skill prompt too verbose, dilutes context window

- **Probability:** Low
- **Impact:** Medium (could affect subsequent phase execution quality)
- **Mitigation:** Progressive disclosure — SKILL.md under 500 lines, detailed patterns in references/ loaded only when needed. Anthropic best practices followed (conciseness, only add context Claude doesn't have).
- **Contingency:** Trim SKILL.md further, move more content to references.

### Risk 3: Spec drift detection produces false positives

- **Probability:** Medium
- **Impact:** Low (false positive means unnecessary investigation, not incorrect code changes)
- **Mitigation:** Subagent must cite exact file path and line numbers from context files. Confidence level (high/medium/low) in prescription helps agents calibrate trust.
- **Contingency:** Add a "skip spec check" override for known false-positive patterns.

## What This Epic Does NOT Replace

| Existing Mechanism | Relationship to This Epic |
|---|---|
| **RCA process** (`/rca` command) | RCA = post-mortem documentation after a failure is resolved. Diagnosis = in-the-moment troubleshooting during the failure. Complementary, not overlapping. |
| **QA remediation** (`/review-qa-reports`) | Remediation creates stories from QA gaps. Diagnosis identifies root causes before/during gap creation. Complementary. |
| **Commit failure recovery** (`.claude/rules/workflow/commit-failure-recovery.md`) | Recovery guide stays unchanged. The diagnosis-before-fix rule explicitly defers to it for Phase 08 DoD validation issues. |

## Anthropic Agent Skills Guidelines Compliance

All skill artifacts comply with Anthropic's Agent Skills Specification v1.0:

| Guideline | Compliance |
|-----------|------------|
| Name: kebab-case, ≤64 chars, no reserved words | `root-cause-diagnosis` (21 chars) ✅ |
| Description: WHAT + WHEN + triggers, ≤1024 chars, third person, no XML | 388 chars, plain text ✅ |
| Progressive disclosure: SKILL.md <500 lines | ~200 lines, references for details ✅ |
| Folder: kebab-case, matches name | `root-cause-diagnosis/` ✅ |
| File: exact SKILL.md | `SKILL.md` ✅ |
| No README.md in skill folder | All docs in SKILL.md + references/ ✅ |
| One-level-deep references | SKILL.md → references/*.md directly ✅ |

**Reference documents consulted:**
- `.claude/skills/claude-code-terminal-expert/references/skills/agent-skills-spec.md`
- `.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md`
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/The-Complete-Guide-to-Building-Skills-for-Claude.md`

## Files Created/Modified by This Epic

| Action | File Path | Feature | Story |
|--------|-----------|---------|-------|
| CREATE | `.claude/skills/root-cause-diagnosis/SKILL.md` | F1 | STORY-491 |
| CREATE | `.claude/skills/root-cause-diagnosis/references/investigation-patterns.md` | F1 | STORY-491 |
| CREATE | `.claude/skills/root-cause-diagnosis/references/workflow-integration.md` | F1 | STORY-491 |
| CREATE | `.claude/agents/diagnostic-analyst.md` | F2 | STORY-491 |
| CREATE | `.claude/rules/workflow/diagnosis-before-fix.md` | F3 | STORY-491 |
| MODIFY | `.claude/skills/implementing-stories/SKILL.md` | F4 | STORY-496 |
| MODIFY | `.claude/skills/devforgeai-qa/SKILL.md` | F4 | STORY-496 |
| MODIFY | `CLAUDE.md` | F4 | STORY-496 |

## Plan Reference

**Detailed plan with complete artifact specifications, exact file content drafts, and Anthropic compliance matrix:**
`.claude/plans/atomic-wishing-dragon.md`

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1: Foundation | Not Started | 3 | 1 (STORY-491) | 0 | 0 | 0 |
| Sprint 2: Integration | Not Started | 3 | 1 (STORY-496) | 0 | 0 | 0 |
| **Total** | **0%** | **6** | **2** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 6
- **Completed:** 0
- **Remaining:** 6

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════
Week 1:  Sprint 1 - Foundation (skill, subagent, rule)
Week 2:  Sprint 2 - Integration (workflow hooks)
════════════════════════════════════════════════════
Total Duration: 2 weeks
Target Release: 2026-03-15
```

### Key Milestones
- [ ] **Milestone 1:** STORY-491 complete — core artifacts created and validated
- [ ] **Milestone 2:** STORY-496 complete — integration hooks active in /dev and /qa
- [ ] **Milestone 3:** First real-world diagnosis triggered during a /dev workflow failure

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-23
