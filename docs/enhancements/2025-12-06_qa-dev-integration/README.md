# QA-Dev Integration Enhancement

**Date:** 2025-12-06
**Triggered by:** STORY-078 repeated rollbacks (2-3 times)
**Status:** ✅ Implemented

---

## Problem Statement

STORY-078 (Upgrade Mode Migration Scripts) failed QA multiple times due to coverage gaps. Claude kept failing to complete the story because:

1. **QA generated human-readable markdown** - No machine-readable output
2. **`/dev` couldn't parse specific gaps** - Only knew "QA failed", not "which files"
3. **Test-automator wrote generic tests** - Not targeted at uncovered lines
4. **Cycle repeated** - Fix, fail, fix, fail

### Root Cause

The QA → Dev feedback loop was **broken at the integration layer**:

```
Before (Broken):
  /qa → Markdown report (human reads) → /dev → "increase coverage" (generic)

After (Fixed):
  /qa → gaps.json (structured) → /dev → "cover rollback.py lines X-Y" (targeted)
```

---

## Solution Implemented

### Part 1: QA Skill Enhancement (Producer)

**File:** `.claude/skills/devforgeai-qa/references/report-generation.md`

**Changes:**
- Added Step 3.5: Generate Structured Gap Export (`gaps.json`)
- Added Step 3.6: Archive Resolved Gaps (move to `resolved/` on QA pass)

**New output format:**
```json
{
  "story_id": "STORY-078",
  "qa_result": "FAILED",
  "coverage_gaps": [
    {
      "file": "installer/rollback.py",
      "current_coverage": 63.6,
      "target_coverage": 95.0,
      "suggested_tests": ["Test rollback on corrupted backup", ...]
    }
  ]
}
```

### Part 2: Dev Skill Enhancement (Consumer)

**File:** `.claude/skills/devforgeai-development/references/preflight-validation.md`

**Changes:**
- Added Step 0.8.5: Load Structured Gap Data (gaps.json)
- Sets `$REMEDIATION_MODE = true` when gaps.json exists
- Builds `$QA_COVERAGE_GAPS` array for targeted remediation

### Part 3: New Reference File

**File:** `.claude/skills/devforgeai-development/references/qa-remediation-workflow.md`

**Purpose:** Complete remediation mode workflow
- Phase 1R: Targeted test generation
- Phase 2R: Targeted implementation
- Phase 3R: Anti-pattern resolution
- Phase 4R: Coverage verification
- Phase 4.5R: Deferral resolution
- Phase 5R: Commit and complete

### Part 4: Test-Automator Enhancement

**File:** `.claude/agents/test-automator.md`

**Changes:**
- Added Remediation Mode section
- Detects `MODE: REMEDIATION` in prompt
- Parses `coverage_gaps` array
- Generates targeted tests from `suggested_tests`
- Converts natural language to test functions

---

## Files Modified

| File | Change Type | Lines Added |
|------|-------------|-------------|
| `.claude/skills/devforgeai-qa/references/report-generation.md` | Edit | ~150 |
| `.claude/skills/devforgeai-development/references/preflight-validation.md` | Edit | ~120 |
| `.claude/skills/devforgeai-development/references/qa-remediation-workflow.md` | Create | ~400 |
| `.claude/skills/devforgeai-development/SKILL.md` | Edit | ~50 (remediation mode decision point) |
| `.claude/skills/devforgeai-development/references/tdd-red-phase.md` | Edit | ~35 (remediation mode check) |
| `.claude/skills/devforgeai-development/references/tdd-green-phase.md` | Edit | ~35 (remediation mode check) |
| `.claude/agents/test-automator.md` | Edit | ~170 |
| `devforgeai/context/source-tree.md` | Edit | ~10 |

### Integration Points (Silo Prevention)

The remediation workflow is integrated at multiple levels:

1. **Detection Layer** (`preflight-validation.md` Step 0.8.5):
   - Detects gaps.json
   - Sets `$REMEDIATION_MODE = true`
   - Loads gap data into variables

2. **Decision Layer** (`SKILL.md` after Phase 0):
   - Checks `$REMEDIATION_MODE` flag
   - Branches to remediation workflow OR normal TDD

3. **Execution Layer** (Phase reference files):
   - `tdd-red-phase.md`: Checks mode before Phase 1
   - `tdd-green-phase.md`: Checks mode before Phase 2
   - Each redirects to `qa-remediation-workflow.md` if in remediation mode

4. **Workflow Map** (`SKILL.md` execution map):
   - Visual diagram shows remediation branch
   - Clear flow: Phase 0 → Decision → (Remediation OR Normal)

**New directories created:**
- `devforgeai/qa/resolved/` - Archive for resolved gap files
- `src/devforgeai/qa/resolved/` - Distribution copy

---

## Lifecycle

```
QA FAILS:
  → Generate: devforgeai/qa/reports/{STORY-ID}-gaps.json

/dev RUNS:
  → Step 0.8.5 detects gaps.json
  → Sets $REMEDIATION_MODE = true
  → Enters remediation workflow (targeted)
  → test-automator receives coverage_gaps
  → Generates targeted tests

QA PASSES:
  → Move gaps.json → devforgeai/qa/resolved/{STORY-ID}-gaps.json
  → Update story Implementation Notes
```

---

## Expected Impact

| Metric | Before | After |
|--------|--------|-------|
| Coverage gap detection | Generic | Specific (file:line) |
| Test generation scope | Full story | Gaps only |
| Token usage for remediation | ~40K | ~15K (62% savings) |
| Rollback cycles | 2-3 per story | 0-1 expected |

---

## Validation

To validate this enhancement:

1. **Run `/qa STORY-078`**
   - Should generate `STORY-078-qa-report.md`
   - Should generate `STORY-078-gaps.json`

2. **Run `/dev STORY-078`**
   - Should display "STRUCTURED GAP DATA DETECTED"
   - Should show coverage gaps with suggested tests
   - Should enter remediation mode

3. **Verify targeted tests**
   - test-automator should receive gaps array
   - Tests should target rollback.py and migration_discovery.py

4. **Re-run `/qa STORY-078`**
   - Should pass after remediation
   - gaps.json should move to resolved/

---

## Backup and Rollback

**Backups created at:** `devforgeai/backups/2025-12-06_qa-dev-integration/`

**Files backed up:**
- `report-generation.md.bak`
- `preflight-validation.md.bak`
- `test-automator.md.bak`

**To rollback:**
```bash
cp devforgeai/backups/2025-12-06_qa-dev-integration/report-generation.md.bak \
   .claude/skills/devforgeai-qa/references/report-generation.md

cp devforgeai/backups/2025-12-06_qa-dev-integration/preflight-validation.md.bak \
   .claude/skills/devforgeai-development/references/preflight-validation.md

cp devforgeai/backups/2025-12-06_qa-dev-integration/test-automator.md.bak \
   .claude/agents/test-automator.md

rm .claude/skills/devforgeai-development/references/qa-remediation-workflow.md
```

---

## Related

- **STORY-078:** Trigger story that exposed the gap
- **Plan file:** `/home/bryan/.claude/plans/ticklish-spinning-canyon.md`
- **Source tree:** Updated with `resolved/` folder
