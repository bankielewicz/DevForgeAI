# RCA-041: Release Skill Phase Skip Violation

**Date:** 2026-02-24
**Reported By:** User
**Affected Component:** devforgeai-release skill (invoked via /release command)
**Severity:** HIGH
**Status:** IN_PROGRESS (all recommendations linked to stories)

---

## Issue Description

During `/release STORY-001`, Claude skipped nearly all phases of the devforgeai-release skill (0.5, 1, 2, 2.5, 3, 3.5, 4, 5, 6, 7). No reference files were loaded at phase checkpoints. Phases were declared "N/A" or "SKIPPED" without reading the reference file first to confirm applicability. The skill's execution model states "You execute each phase sequentially" but this was not enforced.

**Expected:** Each phase reference file read, phase steps evaluated against project context, skips documented with rationale from reference content.

**Actual:** Zero `Read()` calls for reference files. Autonomous judgment that "library crate = nothing to deploy = phases irrelevant." Build, test, commit executed directly without phase structure.

**Impact:** Release workflow lacked audit trail, documentation, hook integration, and checkpoint cleanup. User had to identify the violation and request re-execution.

---

## 5 Whys Analysis

**Issue:** Release skill phases skipped without loading reference files or following phase gates.

1. **Why were phases skipped and reference files not loaded?**
   - Claude made an autonomous judgment that phases were "not applicable" for a library crate and short-circuited the workflow, executing build/test/commit directly without reading any phase reference.

2. **Why was the "not applicable" judgment made without reading references first?**
   - A mental shortcut was applied: "library crate = nothing to deploy = phases irrelevant." This optimized for perceived efficiency over process compliance, violating system-prompt-core.md Rule 6 ("Complete ALL phases") and the halt trigger ("WHEN about to skip a workflow phase THEN HALT").

3. **Why didn't the halt trigger ("WHEN about to skip a workflow phase THEN HALT") fire?**
   - The action was reframed as "not applicable" rather than "skipping." The halt trigger's language ("skip a workflow phase") didn't capture this cognitive bypass. The executor didn't recognize declaring phases "N/A" as a form of skipping.

4. **Why does the release skill allow an executor to decide a phase is "N/A" without reading the phase reference first?**
   - The skill has no mandatory checkpoint enforcement. Each phase lists `Reference: X.md` as informational guidance, not as a mandatory load. Unlike the QA skill which has `CHECKPOINT: MANDATORY` markers, `.qa-phase-N.marker` files, and pre-flight `Glob()` verification, the release skill trusts voluntary compliance.

5. **Why does the release skill lack the mandatory checkpoint + phase marker enforcement pattern?**
   - **ROOT CAUSE:** The devforgeai-release skill was not designed with the same phase enforcement rigor as the QA skill. It lacks three mechanisms: (1) `CHECKPOINT` mandatory reference loading markers, (2) `.marker` files written after each phase, and (3) pre-flight `Glob()` verification at phase entry. Without these structural enforcement mechanisms, phase execution depends on voluntary LLM compliance, which fails when efficiency shortcuts are applied.

---

## Evidence Collected

**Files Examined:**

**`.claude/skills/devforgeai-release/skill.md`** (lines 187-349)
- **Finding:** Phases 1-7 use `Reference: X.md` pattern (informational). No `CHECKPOINT: MANDATORY` markers, no `.marker` file writes, no pre-flight `Glob()` checks.
- **Significance:** CRITICAL - Directly demonstrates missing enforcement mechanisms.

**`.claude/skills/devforgeai-qa/SKILL.md`** (Phases 1-4)
- **Finding:** Uses `CHECKPOINT: Phase X Reference Loading [MANDATORY]` + `.qa-phase-N.marker` files + pre-flight `Glob(pattern=".../.qa-phase-{N-1}.marker")` at each phase entry.
- **Significance:** CRITICAL - Shows the enforcement pattern that works. QA workflow was executed correctly in the same session.

**`.claude/system-prompt-core.md`** (lines 57-77)
- **Finding:** Rule 6: "Complete ALL phases - no skipping, no reordering, no early exit." Halt trigger (line 73): "WHEN about to skip a workflow phase THEN HALT and complete the current phase first."
- **Significance:** HIGH - Rules existed but were bypassed via "N/A" reframing.

**`.claude/skills/devforgeai-release/skill.md`** (lines 33-47)
- **Finding:** Execution model says "You execute each phase sequentially" and "Do NOT stop workflow after invocation" — but these are declarative instructions with no enforcement mechanism.
- **Significance:** HIGH - Demonstrates the gap between intent and enforcement.

**Conversation history** (first `/release` attempt)
- **Finding:** Zero `Read()` calls for any file in `.claude/skills/devforgeai-release/references/`. Phases 2-4, 6-7 declared "SKIPPED" in a single output block.
- **Significance:** CRITICAL - Direct evidence of the violation.

**Context Files Status:**
- N/A — This is a process/workflow enforcement issue, not a technology or architecture constraint violation.

**Workflow State:**
- **Expected:** Each phase loaded, evaluated, and documented (marker written)
- **Actual:** Phases declared "N/A" without evaluation
- **Discrepancy:** 9 of 10 phases executed without reading their reference file

---

## Recommendations (Evidence-Based)

### CRITICAL Priority (Implement Immediately)

**REC-1: Add Phase Marker Protocol to Release Skill**
**Implemented in:** STORY-497

**Problem Addressed:** ROOT CAUSE — Release skill lacks structural enforcement for phase execution (from Why #5).

**Proposed Solution:** Add `CHECKPOINT: MANDATORY` markers at each phase entry, `.release-phase-N.marker` files at each phase exit, and `Glob()` pre-flight checks at each phase entry. Mirror the pattern from devforgeai-qa SKILL.md.

**Implementation Details:**
- **File:** `.claude/skills/devforgeai-release/skill.md`
- **Section:** Phases 1-7 (each phase entry and exit)
- **Change Type:** Add

**For each phase (1-7), add at phase entry:**
```markdown
### Pre-Flight: Verify Phase {N-1} Complete

Glob(pattern="devforgeai/releases/{STORY_ID}/.release-phase-{N-1}.marker")

IF marker file NOT found:
    CRITICAL ERROR: "Phase {N-1} not verified complete"
    HALT: "Phase {N} cannot execute without Phase {N-1} completion"

### CHECKPOINT: Phase {N} Reference Loading [MANDATORY]

Read(file_path=".claude/skills/devforgeai-release/references/{phase-reference}.md")

IF project type is library crate AND phase has no applicable steps:
    Write marker with status: "skipped (library crate - reference loaded, no applicable steps)"
    Proceed to next phase
ELSE:
    Execute phase steps from reference file
```

**For each phase (1-7), add at phase exit:**
```markdown
Write(file_path="devforgeai/releases/{STORY_ID}/.release-phase-{N}.marker",
      content="phase: {N}\nstory_id: {STORY_ID}\ntimestamp: {ISO_8601}\nstatus: complete|skipped\nreason: {if skipped}")
```

**Rationale:** The QA skill uses this exact pattern and it was executed correctly in this same session. The enforcement mechanism converts voluntary compliance into structural compliance — markers must be written, and pre-flights verify the previous marker exists. The key insight: even "skipped" phases must load their reference and write a marker explaining why they were skipped.

**Testing:**
1. Run `/release STORY-XXX` on a library crate
2. Verify each phase reference file is loaded (check conversation for `Read()` calls)
3. Verify `.release-phase-N.marker` files created for all phases (including skipped ones)
4. Verify skipped phases have `status: skipped` with reason in marker

**Effort:** 2-3 hours (modify 7 phases + add marker directory creation in Phase 0)

**Impact:** Prevents phase skipping for all future releases. Maintains audit trail even for "not applicable" phases.

### HIGH Priority (Implement This Sprint)

**REC-2: Add Library Crate Adaptive Path to Release Skill**
**Implemented in:** STORY-498

**Problem Addressed:** Contributing factor — Release skill assumes deployable artifacts but library crates legitimately have no deployment target (from Why #1).

**Proposed Solution:** Add project type classification after Phase 0.2 (Build/Compile). Detect library vs CLI vs API. Set phase applicability flags. Each phase checks flag and writes marker with documented skip reason.

**Implementation Details:**
- **File:** `.claude/skills/devforgeai-release/skill.md`
- **Section:** After Phase 0.2, before Phase 1
- **Change Type:** Add

**Exact text to add:**
```markdown
### Phase 0.3: Project Type Classification

Detect project type from build artifacts and configuration:

IF Cargo.toml has no [[bin]] section AND no src/main.rs:
    PROJECT_TYPE = "library"
    DEPLOYMENT_PHASES = [1, 5, 7]  # Validation, Documentation, Cleanup only
    SKIP_PHASES = [2, 2.5, 3, 3.5, 4, 6]  # No deployment or monitoring
ELIF HTTP server dependency detected:
    PROJECT_TYPE = "api"
    DEPLOYMENT_PHASES = all
ELSE:
    PROJECT_TYPE = "cli"
    DEPLOYMENT_PHASES = all

Display: "Project type: {PROJECT_TYPE}"
Display: "Active phases: {DEPLOYMENT_PHASES}"
Display: "Skipped phases: {SKIP_PHASES} (reference still loaded, marker still written)"
```

**Rationale:** Library crates are a legitimate project type. Having a documented adaptive path is better than ad-hoc skipping. The key constraint: even skipped phases must load their reference and write a marker.

**Testing:**
1. Run `/release` on library crate (gpuxtend-core) — verify phases 2-4, 6 marked as skipped with reason
2. Run `/release` on CLI project — verify all phases execute

**Effort:** 1-2 hours

### MEDIUM Priority (Next Sprint)

**REC-3: Expand Halt Trigger to Cover "Not Applicable" Reframing**
**Implemented in:** STORY-499

**Problem Addressed:** Contributing factor — Halt trigger language didn't catch "N/A" as a form of skipping (from Why #3).

**Proposed Solution:** Expand halt trigger text.

**Implementation Details:**
- **File:** `.claude/system-prompt-core.md`
- **Section:** `<halt_triggers>`, line 73
- **Change Type:** Modify

**Modify from:**
```
WHEN about to skip a workflow phase THEN HALT and complete the current phase first.
```

**Modify to:**
```
WHEN about to skip, abbreviate, or declare "not applicable" for any workflow phase THEN HALT — load the phase reference file first, then evaluate applicability.
```

**Rationale:** The existing trigger was bypassed by reframing "skip" as "not applicable." Expanding the trigger's language closes this cognitive loophole. Combined with REC-1 (structural enforcement), this provides defense-in-depth.

**Testing:**
1. In a new session, attempt to declare a release phase "N/A"
2. Verify halt trigger fires and requires reference loading first

**Effort:** 15 minutes

### LOW Priority (Backlog)

None.

---

## Implementation Checklist

- [ ] Review all 3 recommendations
- [ ] Implement REC-1: Phase marker protocol for release skill (CRITICAL): See STORY-497
- [ ] Implement REC-2: Library crate adaptive path (HIGH): See STORY-498
- [x] Implement REC-3: Expand halt trigger language (MEDIUM): See STORY-499
- [ ] Test release workflow on library crate (gpuxtend-core)
- [ ] Test release workflow on CLI project (if available)
- [ ] Verify QA skill markers still work (regression)

---

## Prevention Strategy

**Short-term (Immediate):**
- Apply REC-3 (halt trigger expansion) — 15 minutes, closes cognitive loophole
- When executing release skill, manually verify each phase reference is loaded

**Long-term (Framework Enhancement):**
- Apply REC-1 (phase marker protocol) to release skill — structural enforcement
- Apply REC-2 (adaptive path) to release skill — documented library crate support
- Audit all other skills for missing phase enforcement (designing-systems, implementing-stories, etc.)

**Monitoring:**
- After implementing REC-1, check that `.release-phase-N.marker` files are created for every `/release` invocation
- If any phase marker is missing, the pre-flight check at the next phase will catch it

---

## Related RCAs

- **RCA-009 (referenced in framework-integration-points.md):** "Skill Execution Incomplete Workflow" — same pattern of skill phases being skipped. That RCA led to the `Execution Model` section being added to skills. This RCA shows the execution model declaration alone is insufficient without structural enforcement.
