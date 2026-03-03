---
id: STORY-460
title: Slim Skill-Invoking Commands (qa, create-ui, ideate) to Lean Orchestration Pattern
type: refactor
epic: EPIC-071
sprint: Sprint-14
status: QA Approved
points: 15
depends_on: ["STORY-457", "STORY-458", "STORY-459"]
priority: Critical
advisory: false
assigned_to: DevForgeAI AI Agent
created: 2026-02-20
format_version: "2.9"
---

# Story: Slim Skill-Invoking Commands (qa, create-ui, ideate) to Lean Orchestration Pattern

## Description

**As a** framework maintainer responsible for DevForgeAI's command-skill boundary,
**I want** to slim `qa.md` (344 lines), `create-ui.md` (675 lines), and `ideate.md` (374 lines) by extracting CWD validation, mode inference, context file validation, output verification, brainstorm auto-detection, project mode detection, result interpretation, and hook integration logic into their respective skills' Phase 0,
**so that** all three commands follow the lean orchestration pattern, the main conversation token budget is freed by 40-60% per invocation, and the framework achieves uniform command architecture compliance.

## Provenance

```xml
<provenance>
  <origin document="EPIC-071" section="Feature 4: Skill-Invoking Command Slimming">
    <quote>"Refactor qa.md (344 lines, 8 blocks), create-ui.md (675 lines, 8 blocks), ideate.md (374 lines, 7 blocks). Pattern C (Multi-Phase Slimming). BLOCKING PREREQUISITE: devforgeai-qa SKILL.md is 1,012 lines (12 over maximum)."</quote>
    <line_reference>lines 100-110</line_reference>
    <quantified_impact>Combined 1,393 lines reduced to ~290 lines (79% reduction); prerequisite qa skill size reduction unblocks this work</quantified_impact>
  </origin>

  <decision rationale="pattern-c-multi-phase-slimming">
    <selected>Move mode detection and context probing into skill Phase 0; move result interpretation into skill post-execution phases; add DO NOT guardrail section</selected>
    <rejected alternative="accept-current-overhead">Pre-skill probing consumes main conversation tokens unnecessarily; skills can perform detection in isolated context at zero cost</rejected>
    <trade_off>Skills gain Phase 0 complexity but tokens are isolated; net benefit is 40-60% main conversation savings</trade_off>
  </decision>

  <stakeholder role="Framework Owner" goal="uniform-command-compliance">
    <quote>"Concise is key -- the context window is a public good"</quote>
    <source>Anthropic best-practices.md; REQ-071 decision DR-4</source>
  </stakeholder>
</provenance>
```

## Acceptance Criteria

### AC#1: qa.md reduced to lean orchestration pattern

```xml
<acceptance_criteria id="AC1">
  <given>qa.md is 344 lines with 8 code blocks containing CWD validation and mode inference from story status</given>
  <when>The command is refactored following Pattern C</when>
  <then>qa.md contains <=100 lines, <=3 code blocks before Skill(), Lean Orchestration Enforcement section with >=4 DO NOT items, and CWD validation exists in devforgeai-qa SKILL.md Phase 0</then>
  <verification>
    <source_files>
      <file hint="Refactored command">.claude/commands/qa.md</file>
      <file hint="Extended skill">.claude/skills/devforgeai-qa/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-460/test_ac1_qa_lean.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: create-ui.md reduced to lean orchestration pattern

```xml
<acceptance_criteria id="AC2">
  <given>create-ui.md is 675 lines with 8 code blocks containing context file validation, tech-stack extraction, output verification, and component validation</given>
  <when>The command is refactored following Pattern C</when>
  <then>create-ui.md contains <=100 lines, <=3 code blocks before Skill(), Lean Orchestration Enforcement section, and all extracted logic exists in devforgeai-ui-generator skill phases</then>
  <verification>
    <source_files>
      <file hint="Refactored command">.claude/commands/create-ui.md</file>
      <file hint="Extended skill">.claude/skills/devforgeai-ui-generator/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-460/test_ac2_create_ui_lean.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: ideate.md reduced to lean orchestration pattern

```xml
<acceptance_criteria id="AC3">
  <given>ideate.md is 374 lines with 7 code blocks containing brainstorm auto-detection, project mode detection, result interpretation via Task(), and hook integration via Bash</given>
  <when>The command is refactored following Pattern C</when>
  <then>ideate.md contains <=90 lines, <=3 code blocks before Skill(), Lean Orchestration Enforcement section, brainstorm detection in discovering-requirements SKILL.md Phase 0, and result interpretation in skill completion phase</then>
  <verification>
    <source_files>
      <file hint="Refactored command">.claude/commands/ideate.md</file>
      <file hint="Extended skill">.claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-460/test_ac3_ideate_lean.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: BLOCKING PREREQUISITE — devforgeai-qa SKILL.md size reduction

```xml
<acceptance_criteria id="AC4">
  <given>devforgeai-qa SKILL.md is currently 1,012 lines (12 lines OVER the 1,000-line maximum per tech-stack.md lines 375-379)</given>
  <when>The prerequisite extraction is completed BEFORE absorbing qa.md logic</when>
  <then>devforgeai-qa SKILL.md is <=800 lines, content extracted to new reference files in .claude/skills/devforgeai-qa/references/, and all phase execution behavior preserved through reference loading</then>
  <verification>
    <source_files>
      <file hint="Reduced skill">.claude/skills/devforgeai-qa/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-460/test_ac4_qa_skill_reduced.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Backward compatibility for all three commands

```xml
<acceptance_criteria id="AC5">
  <given>Existing workflows use /qa STORY-001 deep, /qa STORY-001, /create-ui STORY-001, /create-ui "Login form", /ideate "app idea", /ideate (brainstorm auto-detection)</given>
  <when>The refactoring is complete</when>
  <then>All invocation syntaxes produce identical end-to-end behavior: same validation results, same display output, same error messages, same file artifacts</then>
  <verification>
    <source_files>
      <file hint="Command 1">.claude/commands/qa.md</file>
      <file hint="Command 2">.claude/commands/create-ui.md</file>
      <file hint="Command 3">.claude/commands/ideate.md</file>
    </source_files>
    <test_file>tests/STORY-460/test_ac5_backward_compat.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#6: DO NOT guardrail sections in all three commands

```xml
<acceptance_criteria id="AC6">
  <given>The gold standard requires explicit forbidden actions derived from extracted logic</given>
  <when>The refactoring is complete</when>
  <then>Each command contains Lean Orchestration Enforcement section with >=4 command-specific DO NOT items directly derived from the logic being extracted</then>
  <verification>
    <source_files>
      <file hint="All 3 commands">.claude/commands/qa.md, .claude/commands/create-ui.md, .claude/commands/ideate.md</file>
    </source_files>
    <test_file>tests/STORY-460/test_ac6_guardrails.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#7: Skill size compliance after absorption

```xml
<acceptance_criteria id="AC7">
  <given>Architecture-constraints.md limits SKILL.md to <1,000 lines; recommended target is 500 lines</given>
  <when>The refactoring is complete</when>
  <then>devforgeai-qa SKILL.md <=800 lines (after prerequisite + absorption), devforgeai-ui-generator SKILL.md <=500 lines, discovering-requirements SKILL.md <=500 lines (all use references/ for absorbed logic)</then>
  <verification>
    <source_files>
      <file hint="QA skill">.claude/skills/devforgeai-qa/SKILL.md</file>
      <file hint="UI skill">.claude/skills/devforgeai-ui-generator/SKILL.md</file>
      <file hint="Requirements skill">.claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-460/test_ac7_skill_sizes.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#8: Backward-compatible output including help text, error messages, and display formats for all 3 commands

```xml
<acceptance_criteria id="AC8">
  <given>Pre-refactoring output samples captured for all invocation modes: qa.md (344 lines) has Quick Reference with 3 examples, Error Handling with 4 sections (Story ID Invalid, Story File Not Found, Invalid Mode, QA Skill Failed with recovery steps), Success Criteria checklist (10 items), Integration with Framework section (invoked by, invokes, result handling with light/deep modes, quality gates), Related Commands (4 commands), Performance Targets (light: 2min/15K, deep: 5min/70K); create-ui.md (675 lines) has Arguments section, 5 error handling blocks (Story Not Found with available stories list, Context Files Missing with 6-file descriptions, Frontend Stack Not Defined with framework/styling/state options, UI Generator Skill Failed with debug info, Specification Validation Failed with missing/placeholder/violation lists), Success Criteria, Token Efficiency, Integration Points, Feedback Hook Integration (Phase N); ideate.md (374 lines) has brainstorm auto-detection flow (Phase 0), project mode detection with greenfield/brownfield/brainstorm-resume routing (Phase 2.0), result interpretation via Task(subagent_type=ideation-result-interpreter) (Phase 3), hook integration via Bash (Phase N), Error Handling section</given>
  <when>All 3 commands are refactored</when>
  <then>qa.md help text preserves ALL original sections (Quick Reference, Error Handling 4 types, Success Criteria, Integration, Related Commands, Performance Targets); create-ui.md preserves ALL 5 error handling blocks with exact formatted output (emoji + message + Action Required + recovery steps), Success Criteria, Token Efficiency, Integration Points; ideate.md preserves Error Handling section and brainstorm auto-detection UX flow. All error messages use identical emoji+message+action format from originals</then>
  <verification>
    <source_files>
      <file hint="qa.md">.claude/commands/qa.md</file>
      <file hint="create-ui.md">.claude/commands/create-ui.md</file>
      <file hint="ideate.md">.claude/commands/ideate.md</file>
    </source_files>
    <test_file>tests/STORY-460/test_ac8_backward_compat_output.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#9: Governance, integration, and hook sections preserved in skills or references

```xml
<acceptance_criteria id="AC9">
  <given>create-ui.md contains Feedback Hook Integration section (Phase N, lines 349-403) with check-hooks/invoke-hooks workflow; Integration Points section (lines 572-591) documenting prerequisites, invokes, creates, enables, related commands; Token Efficiency section (lines 551-571) with before/after metrics. ideate.md contains Hook Integration section (Phase N, lines 296-326) with devforgeai-validate CLI calls and timing targets; project mode detection docs (Phase 2.0, lines 136-177) with greenfield/brownfield/brainstorm-resume decision tree. qa.md contains Integration with Framework section (lines 283-308) documenting invoked-by/invokes/result-handling/quality-gates</given>
  <when>Business logic extracted to skills</when>
  <then>ALL governance content preserved in skill or skill references: create-ui Feedback Hook Integration in devforgeai-ui-generator skill or reference, create-ui Integration Points in command or skill, ideate Hook Integration in discovering-requirements skill or reference, ideate project mode detection decision tree in discovering-requirements skill Phase 0 or reference, qa Integration with Framework in devforgeai-qa skill or command</then>
  <verification>
    <source_files>
      <file hint="QA skill">.claude/skills/devforgeai-qa/SKILL.md</file>
      <file hint="UI skill">.claude/skills/devforgeai-ui-generator/SKILL.md</file>
      <file hint="Requirements skill">.claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-460/test_ac9_governance_preserved.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#10: All AskUserQuestion prompts and interactive flows functional with original text

```xml
<acceptance_criteria id="AC10">
  <given>qa.md has 7 AskUserQuestion calls (story ID validation, mode selection with Dev Complete/In Development inference, story listing); create-ui.md has 7 AskUserQuestion references (spec validation issue resolution, placeholder resolution, override requests); ideate.md has 3 AskUserQuestion calls (brainstorm resume prompt, business idea capture, mode confirmation)</given>
  <when>Commands are refactored with AskUserQuestion in commands per lean orchestration</when>
  <then>ALL qa.md AskUserQuestion prompts functional with original text/options (story ID prompt, mode inference from status, story listing), ALL create-ui.md interactive validation flows preserved (placeholder resolution, constraint violation overrides), ALL ideate.md prompts preserved (brainstorm resume decision, business idea input, mode confirmation), mode inference logic (Dev Complete→deep, In Development→light) produces identical results</then>
  <verification>
    <source_files>
      <file hint="qa.md">.claude/commands/qa.md</file>
      <file hint="create-ui.md">.claude/commands/create-ui.md</file>
      <file hint="ideate.md">.claude/commands/ideate.md</file>
    </source_files>
    <test_file>tests/STORY-460/test_ac10_interactive_prompts.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#11: AskUserQuestion calls reside in commands per lean orchestration, not in absorbed skill phases

```xml
<acceptance_criteria id="AC11">
  <given>The lean orchestration pattern (lean-orchestration-pattern.md line 104) states "User interaction (AskUserQuestion belongs in commands for UX decisions)"</given>
  <when>All 3 commands and their extended skills are inspected</when>
  <then>No new AskUserQuestion calls added to devforgeai-qa SKILL.md by this story (Phase 0 absorption must not introduce AskUserQuestion), no new AskUserQuestion added to devforgeai-ui-generator SKILL.md by this story, no new AskUserQuestion added to discovering-requirements SKILL.md by this story, all user interaction from extracted logic remains in respective command files, skills receive user decisions via context markers</then>
  <verification>
    <source_files>
      <file hint="QA skill">.claude/skills/devforgeai-qa/SKILL.md</file>
      <file hint="UI skill">.claude/skills/devforgeai-ui-generator/SKILL.md</file>
      <file hint="Requirements skill">.claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-460/test_ac11_askuser_placement.sh</test_file>
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
      name: "qa.md (refactored)"
      file_path: ".claude/commands/qa.md"
      requirements:
        - id: "CMD-001"
          description: "Reduce from 344 to <=100 lines with <=3 code blocks"
          testable: true
          test_requirement: "Test: wc -l <=100; block count <=3; wc -c <=12000"
          priority: "Critical"

    - type: "Configuration"
      name: "create-ui.md (refactored)"
      file_path: ".claude/commands/create-ui.md"
      requirements:
        - id: "CMD-002"
          description: "Reduce from 675 to <=100 lines with <=3 code blocks"
          testable: true
          test_requirement: "Test: wc -l <=100; block count <=3; wc -c <=12000"
          priority: "Critical"

    - type: "Configuration"
      name: "ideate.md (refactored)"
      file_path: ".claude/commands/ideate.md"
      requirements:
        - id: "CMD-003"
          description: "Reduce from 374 to <=90 lines with <=3 code blocks"
          testable: true
          test_requirement: "Test: wc -l <=90; block count <=3; wc -c <=12000"
          priority: "Critical"

    - type: "Service"
      name: "devforgeai-qa SKILL.md (prerequisite reduction + extension)"
      file_path: ".claude/skills/devforgeai-qa/SKILL.md"
      requirements:
        - id: "SVC-001"
          description: "PREREQUISITE: Reduce from 1,012 to <=800 lines via reference extraction BEFORE qa.md absorption"
          testable: true
          test_requirement: "Test: wc -l <=800 after extraction, before absorption"
          priority: "Critical"
        - id: "SVC-002"
          description: "Absorb CWD validation and mode inference from qa.md into Phase 0"
          testable: true
          test_requirement: "Test: Phase 0 contains CWD check and mode inference; qa.md has zero instances"
          priority: "High"

    - type: "Service"
      name: "devforgeai-ui-generator SKILL.md (extended)"
      file_path: ".claude/skills/devforgeai-ui-generator/SKILL.md"
      requirements:
        - id: "SVC-003"
          description: "Absorb context validation and output verification from create-ui.md"
          testable: true
          test_requirement: "Test: Skill Phase 0/7 contain extracted logic; create-ui.md has zero instances"
          priority: "High"

    - type: "Service"
      name: "discovering-requirements SKILL.md (extended)"
      file_path: ".claude/skills/discovering-requirements/SKILL.md"
      requirements:
        - id: "SVC-004"
          description: "Absorb brainstorm detection, project mode detection, result interpretation, hook integration from ideate.md"
          testable: true
          test_requirement: "Test: Skill Phase 0 contains brainstorm/mode detection; ideate.md has zero Task() or Bash() calls"
          priority: "High"
        - id: "SVC-005"
          description: "Content preservation: ALL error handling paths (qa: 4 types, create-ui: 5 types with formatted blocks, ideate: error section), display formatting, hook integration workflows, integration documentation, and token efficiency metrics must be preserved in commands or skill references — not deleted"
          testable: true
          test_requirement: "Test: Grep for all error type headers in command+skill combined; verify qa 4 types, create-ui 5 types, ideate error section all present"
          priority: "Critical"
        - id: "SVC-006"
          description: "AskUserQuestion calls must NOT be added to any of the 3 skills by this story per lean-orchestration-pattern.md line 104; commands handle all user interaction"
          testable: true
          test_requirement: "Test: git diff of 3 SKILL.md files shows zero new AskUserQuestion additions"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "devforgeai-qa prerequisite extraction MUST complete before any qa.md logic absorption"
      trigger: "Story execution start"
      validation: "wc -l SKILL.md <=800 verified before absorption step"
      error_handling: "HALT absorption if prerequisite not met"
      test_requirement: "Test: Verify line count before and after prerequisite step"
      priority: "Critical"
    - id: "BR-002"
      rule: "Zero forbidden patterns in all 3 refactored commands"
      trigger: "Post-refactoring verification"
      validation: "Grep for Task(, Bash(command=, FOR...in returns 0"
      error_handling: "Revert and fix if patterns found"
      test_requirement: "Test: grep forbidden patterns returns 0 for all 3 files"
      priority: "Critical"
    - id: "BR-003"
      rule: "Pattern C consistency: all 3 commands follow same slimming approach"
      trigger: "Code review"
      validation: "Same template structure as create-story.md gold standard"
      error_handling: "Refactor to match pattern"
      test_requirement: "Test: All 3 commands match gold standard section structure"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Token reduction >=40% per command invocation"
      metric: "qa: ~8K to ~2K; create-ui: ~15K to ~3K; ideate: ~8K to ~2K"
      test_requirement: "Test: Compare before/after token consumption"
      priority: "High"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "All invocation syntaxes produce identical behavior"
      metric: "1 smoke test per syntax variant passes"
      test_requirement: "Test: Run all 6 syntax variants, verify output"
      priority: "Critical"
    - id: "NFR-003"
      category: "Maintainability"
      requirement: "All 3 skills remain under documented line limits after absorption"
      metric: "qa <=800, ui-generator <=500, discovering-requirements <=500"
      test_requirement: "Test: wc -l for all 3 SKILL.md files"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "devforgeai-qa SKILL.md"
    limitation: "Currently 1,012 lines (12 over 1,000-line maximum). Must extract to references/ before absorbing qa.md logic. The 800-line post-extraction ceiling is non-negotiable."
    decision: "workaround:Prerequisite extraction (AC4) reduces SKILL.md before absorption"
    discovered_phase: "Architecture"
    impact: "Blocks qa.md refactoring until prerequisite completes; may require splitting AC4 into separate sub-task"

  - id: TL-002
    component: "ideate.md hook integration"
    limitation: "Hook integration uses Bash(command=devforgeai-validate invoke-hooks...) which is a forbidden pattern in commands. Must be absorbed into skill cleanup phase."
    decision: "workaround:Move hook invocation to discovering-requirements skill final phase"
    discovered_phase: "Architecture"
    impact: "Hook behavior preserved but invocation location changes from command to skill"
```

---

## Non-Functional Requirements (NFRs)

### Performance
- qa.md overhead: <=2K tokens (from ~8K)
- create-ui.md overhead: <=3K tokens (from ~15K)
- ideate.md overhead: <=2K tokens (from ~8K)
- No regression in end-to-end execution time (within 10%)

### Security
- Same file access patterns (no new permissions)
- CWD validation uses same Read(file_path="CLAUDE.md") check
- Hook invocation same CLI, same shell injection surface

### Reliability
- All error scenarios preserved (Story Not Found, Invalid Mode, Context Missing, Skill Failed)
- Prerequisite verified before absorption (HALT if not met)

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-457:** Establishes Pattern A precedent
- [ ] **STORY-458:** Establishes Pattern A+C precedent
- [ ] **STORY-459:** Completes critical skill extension (implementing-stories)

---

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+ for extracted skill logic

**Test Scenarios:**
1. **Happy Path:** /qa STORY-001 deep; /create-ui STORY-001; /ideate "idea"
2. **Edge Cases:**
   - qa: unexpected story status (not Dev Complete/In Development)
   - create-ui: standalone mode (no story file)
   - ideate: zero brainstorm files; hook failure
   - qa skill over budget after absorption
3. **Error Cases:**
   - Missing skill files; invalid mode argument

---

## Acceptance Criteria Verification Checklist

### AC#1: qa.md lean
- [ ] Lines <=100 - **Phase:** 3
- [ ] Blocks <=3 - **Phase:** 3
- [ ] DO NOT section - **Phase:** 3

### AC#2: create-ui.md lean
- [ ] Lines <=100 - **Phase:** 3
- [ ] Blocks <=3 - **Phase:** 3
- [ ] DO NOT section - **Phase:** 3

### AC#3: ideate.md lean
- [ ] Lines <=90 - **Phase:** 3
- [ ] Blocks <=3 - **Phase:** 3
- [ ] DO NOT section - **Phase:** 3

### AC#4: QA skill prerequisite
- [ ] SKILL.md <=800 lines after extraction - **Phase:** 2
- [ ] Reference files created - **Phase:** 2

### AC#5: Backward compatibility
- [ ] All 6 syntax variants tested - **Phase:** 5

### AC#6: Guardrails
- [ ] >=4 DO NOT items per command - **Phase:** 3

### AC#7: Skill sizes
- [ ] qa <=800, ui <=500, reqs <=500 - **Phase:** 3

### AC#8: Backward-compatible output

- [ ] qa.md: Quick Reference, 4 error types, Success Criteria, Integration, Related Commands, Performance Targets preserved - **Phase:** 3 - **Evidence:** grep
- [ ] create-ui.md: 5 error blocks with formatted output (emoji+message+Action Required) preserved - **Phase:** 3 - **Evidence:** grep
- [ ] create-ui.md: Success Criteria, Token Efficiency, Integration Points preserved - **Phase:** 3 - **Evidence:** grep
- [ ] ideate.md: Error Handling section, brainstorm auto-detection UX flow preserved - **Phase:** 3 - **Evidence:** grep
- [ ] Golden output diff shows no regressions for all 6 invocation modes - **Phase:** 5 - **Evidence:** diff

### AC#9: Governance preserved

- [ ] create-ui Feedback Hook Integration workflow preserved in skill or reference - **Phase:** 3 - **Evidence:** grep
- [ ] create-ui Integration Points section preserved - **Phase:** 3 - **Evidence:** grep
- [ ] ideate Hook Integration and project mode detection decision tree preserved - **Phase:** 3 - **Evidence:** grep
- [ ] qa Integration with Framework (invoked-by/invokes/result-handling/quality-gates) preserved - **Phase:** 3 - **Evidence:** grep

### AC#10: Interactive prompts functional

- [ ] qa.md 7 AskUserQuestion prompts with original text/options - **Phase:** 3 - **Evidence:** code review
- [ ] create-ui.md 7 interactive validation flows (placeholder resolution, overrides) - **Phase:** 3 - **Evidence:** code review
- [ ] ideate.md 3 prompts (brainstorm resume, idea capture, mode confirm) - **Phase:** 3 - **Evidence:** code review

### AC#11: AskUserQuestion placement

- [ ] Zero new AskUserQuestion in devforgeai-qa SKILL.md (git diff) - **Phase:** 3 - **Evidence:** grep/diff
- [ ] Zero new AskUserQuestion in devforgeai-ui-generator SKILL.md (git diff) - **Phase:** 3 - **Evidence:** grep/diff
- [ ] Zero new AskUserQuestion in discovering-requirements SKILL.md (git diff) - **Phase:** 3 - **Evidence:** grep/diff

---

**Checklist Progress:** 0/28 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
3. The extract_section() validator stops at the first ### header it encounters
4. If DoD items are under a ### subsection, the validator cannot find them → commit blocked
5. The ### Additional Notes subsection is OK because it comes AFTER DoD items
See: src/claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Definition of Done

### Implementation
- [x] devforgeai-qa SKILL.md reduced to <=800 lines (PREREQUISITE before qa.md absorption)
- [x] qa.md reduced to <=100 lines with <=3 code blocks
- [x] create-ui.md reduced to <=100 lines with <=3 code blocks
- [x] ideate.md reduced to <=90 lines with <=3 code blocks
- [x] All 3 commands contain Lean Orchestration Enforcement DO NOT sections (>=4 items each)

### Quality
- [x] All 11 acceptance criteria have passing tests (AC#1-AC#11)
- [x] All 3 skills remain under documented line limits after absorption
- [x] Zero forbidden patterns in any command (Task(, Bash(command=, FOR loops)
- [x] All error handling scenarios preserved: qa (4 types), create-ui (5 types with formatted blocks), ideate (error section) (AC#8)
- [x] Governance sections preserved: create-ui hooks/integration, ideate hooks/mode detection, qa integration/quality gates (AC#9)
- [x] All AskUserQuestion prompts functional: qa (7), create-ui (7 references), ideate (3) (AC#10)
- [x] AskUserQuestion calls ZERO new additions to any of 3 SKILL.md files (AC#11)

### Testing
- [x] All invocation syntaxes tested (6 variants: qa deep/light/auto, create-ui story/standalone, ideate with/without brainstorm)
- [x] Edge cases: unexpected status, standalone mode, zero brainstorms, hook failure
- [x] Dual-path sync: files identical in src/ and .claude/ trees
- [x] /audit-hybrid passes for all 3 commands
- [x] Golden output samples captured BEFORE refactoring for all 6 invocation modes (AC#8)
- [x] Post-refactoring output diffed against golden samples (AC#8)
- [x] Error type count matches original: qa (4), create-ui (5), ideate (1 section) (AC#8)

### Documentation
- [x] Reference files documented in respective skills
- [x] Tests run against src/ tree per CLAUDE.md

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-21

- [x] devforgeai-qa SKILL.md reduced to <=800 lines (PREREQUISITE before qa.md absorption) - Completed: Reduced from 1,349 to 774 lines via extraction of Phase 0, Phase 3, Phase 4, and Marker Protocol to 4 new reference files
- [x] qa.md reduced to <=100 lines with <=3 code blocks - Completed: Reduced from 343 to 93 lines (73% reduction) following lean orchestration pattern
- [x] create-ui.md reduced to <=100 lines with <=3 code blocks - Completed: Reduced from 674 to 87 lines (87% reduction) following lean orchestration pattern
- [x] ideate.md reduced to <=90 lines with <=3 code blocks - Completed: Reduced from 373 to 80 lines (79% reduction) following lean orchestration pattern
- [x] All 3 commands contain Lean Orchestration Enforcement DO NOT sections (>=4 items each) - Completed: qa 5 items, create-ui 5 items, ideate 4 items
- [x] All 11 acceptance criteria have passing tests (AC#1-AC#11) - Completed: 11/11 test suites pass
- [x] All 3 skills remain under documented line limits after absorption - Completed: qa 774, ui 278, reqs 414
- [x] Zero forbidden patterns in any command (Task(, Bash(command=, FOR loops) - Completed: Verified via test suite
- [x] All error handling scenarios preserved: qa (4 types), create-ui (5 types with formatted blocks), ideate (error section) (AC#8) - Completed: All error types preserved in refactored commands
- [x] Governance sections preserved: create-ui hooks/integration, ideate hooks/mode detection, qa integration/quality gates (AC#9) - Completed: Governance in skill files and command integration sections
- [x] All AskUserQuestion prompts functional: qa (7), create-ui (7 references), ideate (3) (AC#10) - Completed: All prompts preserved in command files
- [x] AskUserQuestion calls ZERO new additions to any of 3 SKILL.md files (AC#11) - Completed: Verified via git diff baseline comparison
- [x] All invocation syntaxes tested (6 variants: qa deep/light/auto, create-ui story/standalone, ideate with/without brainstorm) - Completed: Test suite covers all variants
- [x] Dual-path sync: files identical in src/ and .claude/ trees - Completed: All files synced
- [x] Reference files documented in respective skills - Completed: 4 new reference files in devforgeai-qa/references/
- [x] Tests run against src/ tree per CLAUDE.md - Completed: All tests target src/ tree

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | ✅ | Git validated, context files verified, dependencies satisfied |
| 02 Red | ✅ | 12 test files, 11 suites, 7/11 initially failing |
| 03 Green | ✅ | All 11 suites passing (qa 93, create-ui 87, ideate 80, QA skill 774) |
| 04 Refactor | ✅ | Code review + refactoring specialist approved |
| 04.5 AC Verify | ✅ | 11/11 ACs verified PASS |
| 05 Integration | ✅ | Dual-path sync, reference links, full suite pass |
| 05.5 AC Verify | ✅ | No regressions post-integration |
| 06 Deferral | ✅ | No deferrals |
| 07 DoD Update | ✅ | All DoD items marked complete |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| .claude/commands/qa.md | Modified | 343→93 |
| .claude/commands/create-ui.md | Modified | 674→87 |
| .claude/commands/ideate.md | Modified | 373→80 |
| .claude/skills/devforgeai-qa/SKILL.md | Modified | 1349→774 |
| .claude/skills/devforgeai-qa/references/phase-0-setup-workflow.md | Created | 190 |
| .claude/skills/devforgeai-qa/references/phase-3-reporting-workflow.md | Created | 252 |
| .claude/skills/devforgeai-qa/references/phase-4-cleanup-workflow.md | Created | 143 |
| .claude/skills/devforgeai-qa/references/phase-marker-protocol.md | Created | 37 |
| tests/STORY-460/ (12 files) | Created | ~400 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-20 12:00 | devforgeai-story-creation | Created | Story created from EPIC-071 Feature 4 | STORY-460.story.md |
| 2026-02-21 | .claude/qa-result-interpreter | QA Deep | PASS WITH WARNINGS: 11/11 ACs, 0 CRITICAL, 4 HIGH (source-tree registration) | - |

## Notes

**STORY-457 Lessons Learned (Applied to This Story):**
- STORY-457's first implementation was reverted because ACs measured size/structure without measuring content completeness
- Key losses: governance sections dropped, display logic degraded 83%, AskUserQuestion misplaced in skill, help text compressed, features offered but not implemented
- AC#8-11 added to this story to prevent identical problems: backward-compatible output with golden diffing (AC#8), governance/hook/integration preservation (AC#9), interactive prompt completeness (AC#10), AskUserQuestion placement per lean-orchestration-pattern.md line 104 (AC#11)
- EXTRA CAUTION for create-ui.md: This is the LARGEST command (675 lines) with 5 detailed error handling blocks containing multi-line formatted output with emoji, Action Required sections, and debug info. All 5 blocks must survive in command or skill reference.
- EXTRA CAUTION for ideate.md: Contains project mode detection decision tree (greenfield/brownfield/brainstorm-resume) that is behavioral logic driving the user experience — deletion breaks UX flow

**BLOCKING PREREQUISITE:** devforgeai-qa SKILL.md must be reduced from 1,012 to <=800 lines BEFORE qa.md logic absorption. This is AC#4 and must be the first implementation step.

**References:**
- Epic: EPIC-071, Feature 4
- Requirements: REQ-071 (decision DR-4, Pattern C)
- Tech-stack constraint: devforgeai/specs/context/tech-stack.md (lines 375-379, SKILL.md size limits)
- Lean Orchestration Protocol: devforgeai/protocols/lean-orchestration-pattern.md

---

Story Template Version: 2.9
Last Updated: 2026-02-20
