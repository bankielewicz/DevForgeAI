# Recovery Prompt: QA Skill Framework Improvements

**Use this prompt when:** Context window was cleared/crashed during implementation of QA skill improvements.

**Copy everything below the line and paste into new Claude session:**

---

## RECOVERY PROMPT - PASTE THIS INTO NEW SESSION

```
You are Opus, the architectural advisor for DevForgeAI. A previous session was working on framework improvements but the context window was cleared or the session crashed.

## CRITICAL: Check for In-Flight Work

Before proceeding, you MUST check if work was partially completed:

1. **Check for uncommitted changes:**
   ```bash
   git status
   git diff --name-only
   ```

2. **If uncommitted changes exist in these files, READ them first:**
   - `.claude/skills/devforgeai-qa/SKILL.md`
   - `.claude/skills/devforgeai-qa/references/*.md`
   - `.claude/skills/devforgeai-development/SKILL.md`
   - `devforgeai/templates/story-template.md`

3. **If changes exist, ask user:**
   "I found uncommitted changes in [files]. Should I:
   a) Continue from where the previous session left off
   b) Stash changes and start fresh
   c) Review changes before deciding"

## Context: What Was Being Implemented

This work stems from an architectural review after executing `/qa STORY-118 deep`. The review identified 5 framework improvements to implement.

**Source Document:** Read `/home/bryan/.claude/plans/frolicking-stirring-lecun.md` for full context.

**Architectural Review:** Read `devforgeai/specs/enhancements/QA-SKILL-IMPROVEMENT-RECOVERY-PROMPT.md` (this file).

## The 5 Improvements to Implement

### 1. Phase Complexity - Consolidate QA Phases (HIGH, 2h)
**Issue:** QA skill has 11+ phases with fractional numbers (0.0, 0.5, 0.6, 0.7, 0.9, 1, 2, 2.5, 3, 4, 5, 6, 7)
**File:** `.claude/skills/devforgeai-qa/SKILL.md`
**Action:** Consolidate to 5 logical groups:
  - Phase 0: Setup (CWD validation, test isolation, lock acquisition)
  - Phase 1: Validation (test execution, coverage analysis, traceability)
  - Phase 2: Analysis (anti-patterns, parallel validators, spec compliance, quality metrics)
  - Phase 3: Reporting (report generation, gaps.json, story update)
  - Phase 4: Cleanup (lock release, hooks invocation)

### 2. Reference File Overhead - Merge References (MEDIUM, 1h)
**Issue:** Each phase loads its own reference file (~500 tokens each, 6+ files)
**Files:** `.claude/skills/devforgeai-qa/references/`
**Action:** Create single consolidated file for deep mode:
  - Create `references/deep-validation-workflow.md` with all steps
  - Update SKILL.md to load once at start, not per-phase

### 3. Fixture/Rule Mismatch - Pre-flight Validation (HIGH, 1h)
**Issue:** ast-grep rule patterns not matching fixtures discovered at QA time
**File:** `.claude/skills/devforgeai-development/SKILL.md`
**Action:** Add validation step to Phase 2 (Test Writing):
  ```
  FOR each rule_file in ast-grep/rules/**/*.yml:
      fixture = find_matching_fixture(rule_file)
      IF NOT fixture.exists():
          WARN: "Rule {rule_file} has no matching test fixture"
      IF ast_grep_scan(fixture, rule_file).violations == 0:
          WARN: "Rule {rule_file} detected 0 violations - pattern may be wrong"
  ```

### 4. Technical Limitations - Story Template Field (LOW, 1h)
**Issue:** Tool limitations (e.g., ast-grep can't do semantic duplication) discovered at QA time
**File:** `devforgeai/templates/story-template.md`
**Action:** Add section after Technical Specification:
  ```yaml
  technical_limitations:
    - id: TL-001
      component: "Component name"
      limitation: "Description of limitation"
      decision: "pending|defer:STORY-XXX|descope:ADR-XXX"
      discovered_phase: "Architecture|Development|QA"
  ```

### 5. Implementation Notes - Enforce in /dev (MEDIUM, 30m)
**Issue:** STORY-118 missing Implementation Notes section
**File:** `.claude/skills/devforgeai-development/SKILL.md`
**Action:** Add enforcement to Phase 4 (Story Update):
  ```
  IF story lacks "## Implementation Notes":
      HALT: "Story file incomplete - add Implementation Notes before Phase 5"
      Required subsections:
      - Definition of Done Status
      - Test Results
      - Acceptance Criteria Verification
      - Files Created/Modified
  ```

## Progress Checkpoints

Check these off as you complete each:

- [ ] Checked for uncommitted changes from previous session
- [ ] Read plan file: `/home/bryan/.claude/plans/frolicking-stirring-lecun.md`
- [ ] **Improvement 1:** QA phases consolidated (0→4 instead of 0.0→7)
- [ ] **Improvement 2:** Reference files merged to single deep-mode file
- [ ] **Improvement 3:** Rule/fixture validation added to /dev Phase 2
- [ ] **Improvement 4:** Technical Limitations field added to story template
- [ ] **Improvement 5:** Implementation Notes enforcement added to /dev Phase 4
- [ ] All changes tested (validate skills still work)
- [ ] Changes committed with descriptive message

## Key Files to Read First

Execute these reads to understand current state:

```bash
# Current QA skill structure
Read .claude/skills/devforgeai-qa/SKILL.md

# Current reference files
Glob .claude/skills/devforgeai-qa/references/*.md

# Current dev skill (for improvements 3 and 5)
Read .claude/skills/devforgeai-development/SKILL.md

# Story template (for improvement 4)
Read devforgeai/templates/story-template.md
```

## Constraints

All changes must be implementable within Claude Code Terminal using only:
- Native tools: Read, Write, Edit, Glob, Grep, Bash, Task
- No external dependencies
- No aspirational features - only grounded improvements

## When Complete

1. Run validation: `/qa` on a test story to verify QA skill still works
2. Create commit:
   ```bash
   git add .claude/skills/devforgeai-qa/ .claude/skills/devforgeai-development/ devforgeai/templates/
   git commit -m "refactor(qa): consolidate phases and improve framework robustness

   - Consolidate 11 QA phases to 5 logical groups
   - Merge reference files for deep mode
   - Add rule/fixture pre-flight validation in /dev
   - Add Technical Limitations field to story template
   - Enforce Implementation Notes section in /dev Phase 4

   Implements recommendations from architectural review of STORY-118 QA execution."
   ```
3. Update this recovery prompt with completion status

## If Blocked

- **Phase consolidation unclear:** Read `.claude/skills/devforgeai-qa/references/` for current phase logic
- **Reference merge complex:** Start with just coverage + anti-pattern workflows
- **Rule validation scope:** Focus on `devforgeai/ast-grep/rules/` patterns only
- **Template changes break things:** Add field as optional, not required

## Do NOT

- ❌ Work on STORY-118 (that's separate remediation work)
- ❌ Make aspirational changes not in the 5 improvements
- ❌ Add external dependencies
- ❌ Skip checking for uncommitted changes
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-21 | Initial recovery prompt created from architectural review |

## Source References

- Architectural Review: `/home/bryan/.claude/plans/frolicking-stirring-lecun.md`
- QA Report: `devforgeai/qa/reports/STORY-118-qa-report.md`
- Gaps Analysis: `devforgeai/qa/reports/STORY-118-gaps.json`
