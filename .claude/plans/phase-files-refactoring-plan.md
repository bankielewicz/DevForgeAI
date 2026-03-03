# Phase Files Progressive Task Disclosure Refactoring Plan

## Objective
Standardize the "Progressive Task Disclosure" sections across all 12 implementing-stories phase files (phase-01 through phase-10, including phase-04.5 and phase-05.5) for consistency, DRY principle compliance, and readability.

## Current Issues Identified

### 1. Missing/Inconsistent "Phase Completion Display" Sections
- **Present in:** Phase-03, Phase-04, Phase-10
- **Missing in:** Phase-01, Phase-02, Phase-04.5, Phase-05, Phase-05.5, Phase-06, Phase-07, Phase-08, Phase-09
- **Impact:** Users can't see consistent visual feedback on mandatory step completion

### 2. Missing/Inconsistent "Reflection" Subsections
- **Present in:** Phase-01, Phase-02, Phase-03, Phase-04, Phase-06, Phase-07 (6 phases)
- **Missing in:** Phase-04.5, Phase-05, Phase-05.5, Phase-08, Phase-09, Phase-10 (6 phases)
- **Impact:** Inconsistent observation capture behavior across phases

### 3. Missing Session Memory Update Sections
- **Missing in:** Phase-04.5, Phase-05.5 (2 phases)
- **Present in:** All other phases
- **Impact:** Session memory not updated for AC verification phases

### 4. Redundant Observation Capture Structure
- **Duplication:** All phases repeat nearly identical observation capture workflow
  - Steps 1-3 are identical: "Collect Explicit Observations" → "Invoke Observation Extractor" → "Append to Phase State"
  - Only differences: subagent names and category descriptions
- **Opportunity:** Extract to reusable reference template

### 5. File Size Inconsistency
- **Oversized:** Phase-01 (452 lines), Phase-04 (461 lines), Phase-09 (352 lines)
- **Optimal target:** ~200-250 lines per file
- **Issue:** Large files reduce readability; optional sections should be brief or referenced

## Refactoring Strategy

### Phase 1: Standardize Optional Captures Section Order
**All 12 files should have identical section order:**
1. **Phase Completion Display** (new/standardized)
2. **Observation Capture** (already exists, standardize template)
3. **Session Memory Update** (already exists, add to 04.5/05.5)
4. **Reflection** (optional reflection questions, standardize)
5. **Exit Gate** (already exists)

### Phase 2: Create Reusable Observation Capture Template
**Extract common workflow to:** `.claude/skills/implementing-stories/references/observation-capture-template.md`

**Template structure:**
```markdown
### Observation Capture (EPIC-051)

1. **Collect Explicit Observations:**
   - Extract observations from {SUBAGENT_LIST}
   - Set source: "explicit"

2. **Invoke Observation Extractor:**
   ```
   Task(subagent_type="observation-extractor",
        prompt="Extract implicit observations from {PHASE_CONTEXT}")
   ```

3. **Append to Phase State:**
   - Generate ID: "OBS-{PHASE}-{timestamp}"
   - Append to phase-state.json observations[]

Error Handling: Non-blocking per BR-001
```

**Usage in phase files:**
- Phase-01, 02, 06, 07: Use full template (have relevant subagents)
- Phase-03, 04, 05: Use template with specific subagent names
- Phase-04.5, 05.5, 08, 09, 10: Use minimal template (fewer subagents)

### Phase 3: Add Missing Session Memory Update Sections
**Add to Phase-04.5 and Phase-05.5:**
```markdown
### Session Memory Update (STORY-341)

Before exiting this phase, append observations to the session memory file:

[Standard template from other phases, adapted for phase number]
```

### Phase 4: Standardize Phase Completion Display
**Template for all phases:**
```markdown
### Phase Completion Display

**Before marking Phase {N} complete, display:**

[Display template with phase-specific details]
```

**Required fields:**
- Phase number and name (X/10)
- TDD Iteration counter (if applicable)
- Observation count
- Checklist of mandatory steps completed
- Status message

### Phase 5: Address File Size Issues

**Phase-01 (452 lines → target 300 lines):**
- Extract "Technical Debt Threshold Evaluation" (Step 10) to separate reference file
- Reference: `references/preflight/01.10-debt-threshold.md` (already exists)
- Reduce inline detail; link to reference

**Phase-04 (461 lines → target 280 lines):**
- Extract "Early Coverage Validation" (Step 2a) to separate reference file
- Reference: `references/tdd-refactor-phase-coverage-validation.md` (new)
- Reduce inline detail; link to reference

**Phase-09 (352 lines → target 250 lines):**
- Extract "AI Analysis Validation" (Step 2.3-2.7) to separate reference file
- Reference: `references/phase-09-ai-analysis-validation.md` (new)
- Keep mandatory steps summary in main file

## Implementation Steps

### Step 1: Create Reusable Templates (Reference Files)
- Create: `references/observation-capture-template.md`
- Create: `references/phase-completion-display-template.md`
- Create: `references/session-memory-update-template.md`
- Create: `references/reflection-template.md`

### Step 2: Refactor Phase Files (Standardize)
**For each phase file (order matters):**

**Phase-01:** Extract debt threshold to reference → Standardize optional captures order
**Phase-02:** Standardize optional captures order → Add Phase Completion Display
**Phase-03:** Standardize optional captures order (already complete, fix minor issues)
**Phase-04:** Extract coverage validation → Standardize optional captures order
**Phase-04.5:** Add Session Memory Update + Phase Completion Display
**Phase-05:** Standardize optional captures order → Add Phase Completion Display
**Phase-05.5:** Add Session Memory Update + Phase Completion Display
**Phase-06:** Add Phase Completion Display → Standardize optional captures order
**Phase-07:** Add Phase Completion Display → Standardize optional captures order
**Phase-08:** Add Phase Completion Display + Reflection → Standardize optional captures order
**Phase-09:** Extract AI analysis validation → Add Reflection → Standardize optional captures order
**Phase-10:** Standardize optional captures order (add missing sections)

### Step 3: Verify Consistency
- All 12 files have identical section order in "Optional Captures"
- All files reference appropriate templates vs. inline details
- File sizes within 200-300 line range
- All DRY violations eliminated

## Success Criteria
- [ ] All 12 phase files have consistent "Progressive Task Disclosure" section structure
- [ ] Each file has sections in order: Validation Checkpoint → Pre-Exit Checklist → Optional Captures (with sub-sections) → Exit Gate
- [ ] "Optional Captures" contains: Phase Completion Display → Observation Capture → Session Memory Update → Reflection (where applicable)
- [ ] File sizes: Phase-01/04/09 reduced to 250-300 lines; others 200-250 lines
- [ ] Zero code duplication in observation capture workflow
- [ ] All references to templates are consistent and accurate
- [ ] No behavior changes to phase execution logic

## DRY Improvements
- **Before:** ~2,700 lines of observation capture boilerplate across 12 files (75 lines × 12 × 3 subagent patterns)
- **After:** Single template (~20 lines) referenced 12 times + 3 adapter variants (~10 lines each)
- **Savings:** ~2,550 lines (~95% reduction in duplication)

## Files to Modify
1. `/mnt/c/Projects/DevForgeAI2/.claude/skills/implementing-stories/phases/phase-01-preflight.md`
2. `/mnt/c/Projects/DevForgeAI2/.claude/skills/implementing-stories/phases/phase-02-test-first.md`
3. `/mnt/c/Projects/DevForgeAI2/.claude/skills/implementing-stories/phases/phase-03-implementation.md`
4. `/mnt/c/Projects/DevForgeAI2/.claude/skills/implementing-stories/phases/phase-04-refactoring.md`
5. `/mnt/c/Projects/DevForgeAI2/.claude/skills/implementing-stories/phases/phase-04.5-ac-verification.md`
6. `/mnt/c/Projects/DevForgeAI2/.claude/skills/implementing-stories/phases/phase-05-integration.md`
7. `/mnt/c/Projects/DevForgeAI2/.claude/skills/implementing-stories/phases/phase-05.5-ac-verification.md`
8. `/mnt/c/Projects/DevForgeAI2/.claude/skills/implementing-stories/phases/phase-06-deferral.md`
9. `/mnt/c/Projects/DevForgeAI2/.claude/skills/implementing-stories/phases/phase-07-dod-update.md`
10. `/mnt/c/Projects/DevForgeAI2/.claude/skills/implementing-stories/phases/phase-08-git-workflow.md`
11. `/mnt/c/Projects/DevForgeAI2/.claude/skills/implementing-stories/phases/phase-09-feedback.md`
12. `/mnt/c/Projects/DevForgeAI2/.claude/skills/implementing-stories/phases/phase-10-result.md`

## Reference Files to Create
1. `.claude/skills/implementing-stories/references/progressive-disclosure-template.md` (master template)
2. `.claude/skills/implementing-stories/references/observation-capture-template.md` (specialized)
3. `.claude/skills/implementing-stories/references/phase-completion-display-template.md` (template variants)

## Timeline
- Total refactoring: ~2 hours
- Per-file time: 5-10 minutes (standardization + verification)
