# RCA-045: QA Workflow Phase Execution Enforcement Gap

**Date:** 2026-02-28
**Reported By:** User
**Affected Component:** devforgeai-qa skill (Phase 1.5, systemic)
**Severity:** HIGH

---

## Issue Description

During `/qa STORY-509 deep` execution, the orchestrator skipped the Test Integrity Verification substep (STORY-502) within Phase 1.5, despite loading the `diff-regression-detection.md` reference file that documents it. The snapshot checksums at `devforgeai/qa/snapshots/STORY-509/red-phase-checksums.json` were never read or compared against current test files. Post-QA manual verification revealed 3 of 4 test files had mismatched checksums (modified after RED phase).

**Expected:** Orchestrator reads snapshot file, computes SHA-256 of current test files, compares, and reports any CRITICAL: TEST TAMPERING findings before declaring Phase 1.5 PASS.
**Actual:** Orchestrator completed diff regression analysis (additive-only → PASS), never reached the Test Integrity Verification section of the reference file.
**Impact:** QA declared PASSED without detecting test file modifications. Story status changed to "QA Approved" despite 3 checksum mismatches that were never investigated. Whether these mismatches represent legitimate modifications (e.g., test corrections during GREEN phase per user approval) or actual tampering is unknown — the point is QA never performed the verification to make that determination. The STORY-502 protocol requires that mismatches be flagged as CRITICAL: TEST TAMPERING findings for investigation; QA skipping the check entirely means the finding was never raised. This is the same class of issue documented in RCA-043 (snapshot not created) but at the QA consumption side.

**Broader Pattern:** The user identified this as a systemic issue — the /dev workflow has a robust `phase-state.json` progress file with CLI-enforced checkpoints (`devforgeai-validate phase-init/phase-complete`), while the QA workflow has only ephemeral self-attested marker files (`.qa-phase-N.marker`). This enforcement asymmetry allows QA sub-steps to be silently skipped.

---

## 5 Whys Analysis

**Issue:** QA Phase 1.5 Test Integrity Verification was skipped during STORY-509 deep validation.

1. **Why was the test integrity snapshot verification skipped?**
   - The orchestrator loaded `diff-regression-detection.md`, completed the diff regression analysis (additive-only → PASS), and declared Phase 1.5 complete — without continuing to the "Test Integrity Verification (STORY-502)" section starting at line 149 of the same reference file.
   - *Evidence: `diff-regression-detection.md` lines 149-226 contain the algorithm. Conversation transcript shows PASS declared after diff analysis with no snapshot file read.*

2. **Why did the orchestrator stop mid-reference-file?**
   - The reference file has two distinct sections: (1) Diff Regression Detection (lines 1-147) and (2) Test Integrity Verification (lines 149-226). The early PASS from diff analysis created a false completion signal — the orchestrator treated "no regressions found" as "phase complete."
   - *Evidence: Orchestrator displayed "Phase 1.5 Result: PASS ✅ (additive-only changes, no regressions detected)" immediately after diff analysis.*

3. **Why did partial reference file execution count as phase completion?**
   - SKILL.md's Phase 1.5 section lists 5 steps focused on diff regression. Test Integrity Verification is embedded in the reference file as supplementary content, not as a separate numbered step in SKILL.md. The orchestrator followed SKILL.md's explicit steps but didn't complete the reference file's additional section.
   - *Evidence: SKILL.md Phase 1.5 steps 1-5 cover diff execution, exclusion, scanning, classification, and result determination. No step says "Execute Test Integrity Verification."*

4. **Why doesn't the QA skill have enforceable sub-step checkpoints?**
   - The QA workflow uses ephemeral `.qa-phase-N.marker` files for inter-phase gating with no intra-phase tracking. Markers record only `phase, story_id, mode, timestamp, status: complete` — no record of which sub-steps or verifications actually executed. Markers are self-attested by the orchestrator with no external validation.
   - *Evidence: `.qa-phase-1.marker` has no `steps_required` or `steps_completed` fields. Contrast: `/dev` workflow's `phase-state.json` records `subagents_required`, `subagents_invoked`, `checkpoint_passed`.*

5. **Why does the QA workflow lack a persistent progress file with CLI-enforced checkpoints?**
   - **ROOT CAUSE:** The /dev workflow was upgraded with a CLI-enforced `phase-state.json` system (via `devforgeai-validate phase-init/phase-complete/phase-ready`) per RCA-018 that records required vs. invoked subagents and checkpoint validation per phase. The QA workflow was never given an equivalent mechanism. It still uses the original marker file approach which: (1) has no CLI validation gate, (2) tracks only phase-level completion not sub-steps, (3) gets deleted on QA PASS destroying audit trail, (4) has no required-vs-actual comparison, (5) cannot enforce mandatory artifact verification like snapshot checking.

---

## Evidence Collected

**Files Examined:**

1. **`devforgeai/workflows/STORY-509-phase-state.json`** (CRITICAL)
   - Full /dev progress file showing all 12 phases with `subagents_required`, `subagents_invoked`, `checkpoint_passed`, timestamps
   - Significance: Proves the enforcement mechanism exists for /dev but not /qa

2. **`.claude/skills/devforgeai-qa/references/diff-regression-detection.md`** (CRITICAL)
   - Lines 149-226: Test Integrity Verification algorithm with SHA-256 comparison
   - Lines 155-157: Graceful degradation for missing snapshots
   - Significance: Proves the step is fully documented but was not executed

3. **`devforgeai/qa/snapshots/STORY-509/red-phase-checksums.json`** (HIGH)
   - Contains checksums for 4 test files created during RED phase
   - Significance: Proves snapshot exists and was available for verification

4. **`.claude/skills/devforgeai-qa/SKILL.md`** (HIGH)
   - Phase 1.5 section: 5 numbered steps for diff regression, no numbered step for test integrity
   - Phase marker protocol: Simple text files with no sub-step tracking
   - Significance: Proves the structural gap — snapshot verification not in SKILL.md steps

5. **`devforgeai/qa/reports/STORY-509/.qa-phase-1.marker`** (created during this QA run, deleted in Step 4.5)
   - Content: `phase: 1\nstory_id: STORY-509\nmode: deep\ntimestamp: ...\nstatus: complete`
   - Significance: No sub-step tracking, self-attested, ephemeral

6. **`devforgeai/RCA/RCA-043-test-integrity-snapshot-skipped.md`** (HIGH)
   - RCA-043 covers the creation side (Phase 02 of /dev not creating snapshots)
   - This RCA-045 covers the consumption side (QA not reading/comparing snapshots)
   - Significance: Shows this is a two-sided gap — both creation and consumption lack enforcement

7. **`devforgeai/RCA/RCA-021-qa-skill-phases-skipped.md`** (HIGH)
   - Documents prior QA phase-skipping incident (STORY-127)
   - REC-1 through REC-5 addressed various enforcement gaps
   - Significance: Pattern recurrence — QA enforcement improved but still insufficient

8. **`devforgeai/RCA/RCA-018-development-skill-phase-completion-skipping.md`** (HIGH)
   - Documents /dev phase-skipping pattern and the CLI gate solution
   - REC-1 (CRITICAL) led to `phase-state.json` + CLI gates
   - Significance: Proves the solution pattern — the same approach should be applied to QA

**Context Files Status:**
- Not directly relevant (this is a workflow enforcement issue)

**Workflow State:**
- STORY-509 was updated to "QA Approved" despite missing test integrity verification
- 3 of 4 test files had checksum mismatches (not investigated — QA never performed the verification, so legitimacy vs. tampering was never determined)

---

## Recommendations (Evidence-Based)

### CRITICAL Priority (Implement Immediately)

**REC-1: Add QA Phase-State Progress File with CLI Gate Enforcement**

- **Problem:** QA workflow uses ephemeral self-attested marker files while /dev has a persistent CLI-enforced `phase-state.json`. This allows QA sub-steps to be silently skipped.
- **Proposed Solution:** Extend the existing `devforgeai-validate` CLI to support QA phase tracking with a `qa-phase-state.json` file, mirroring the /dev mechanism.
- **File (CLI):** `.claude/scripts/devforgeai_cli/commands/phase_commands.py`
- **File (Skill):** `.claude/skills/devforgeai-qa/SKILL.md`
- **File (Output):** `devforgeai/workflows/{STORY_ID}-qa-phase-state.json`
- **Implementation approach:** Extend the *existing* `devforgeai-validate` CLI commands (`phase-init`, `phase-complete`, `phase-ready`) with a `--workflow=qa` flag rather than creating separate `qa-phase-*` commands. This aligns with REC-5's unification goal and avoids maintaining two parallel command sets.
  1. Add `--workflow=dev|qa` parameter to existing `phase-init` command. When `--workflow=qa`, create `{STORY_ID}-qa-phase-state.json` with QA-specific phases (0, 1, 1.5, 2, 3, 4) and their `steps_required` arrays
  2. Add `--workflow=dev|qa` parameter to existing `phase-complete` command. When `--workflow=qa`, validate required steps were executed before marking phase complete. Read step requirements from the qa-phase-state.json file
  3. Add `--workflow=dev|qa` parameter to existing `phase-ready` command. When `--workflow=qa`, check previous QA phase is complete
  4. Replace self-attested `.qa-phase-N.marker` writes in SKILL.md with CLI gate calls: `devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase={N} --checkpoint-passed`
  5. Default `--workflow` to `dev` for backward compatibility (existing /dev invocations unchanged)
- **Schema for QA phase-state.json:**
  The schema below shows ALL 6 QA phases (0, 1, 1.5, 2, 3, 4). Phase keys use the same zero-padded string convention as /dev (`"00"`, `"01"`, `"1.5"`, `"02"`, `"03"`, `"04"`).
  ```json
  {
    "story_id": "STORY-509",
    "workflow": "qa",
    "mode": "deep",
    "current_phase": "02",
    "workflow_started": "2026-02-28T00:00:00Z",
    "phases": {
      "00": {
        "status": "completed",
        "steps_required": ["cwd_validation", "test_isolation", "lock_acquisition", "deep_workflow_load", "story_type_extraction"],
        "steps_completed": ["cwd_validation", "test_isolation", "lock_acquisition", "deep_workflow_load", "story_type_extraction"],
        "checkpoint_passed": true
      },
      "01": {
        "status": "completed",
        "steps_required": ["traceability_validation", "test_execution", "coverage_analysis"],
        "steps_completed": ["traceability_validation", "test_execution", "coverage_analysis"],
        "subagents_required": [],
        "subagents_invoked": [],
        "checkpoint_passed": true
      },
      "1.5": {
        "status": "completed",
        "steps_required": ["diff_regression_detection", "test_integrity_verification"],
        "steps_completed": ["diff_regression_detection", "test_integrity_verification"],
        "checkpoint_passed": true
      },
      "02": {
        "status": "in_progress",
        "steps_required": ["anti_pattern_scan", "parallel_validators", "spec_compliance", "code_quality"],
        "steps_completed": [],
        "subagents_required": ["anti-pattern-scanner", "test-automator", "code-reviewer", "security-auditor"],
        "subagents_invoked": [],
        "checkpoint_passed": false
      },
      "03": {
        "status": "pending",
        "steps_required": ["result_determination", "report_generation", "gaps_json_creation", "story_update", "qa_result_interpreter"],
        "steps_completed": [],
        "subagents_required": ["qa-result-interpreter"],
        "subagents_invoked": [],
        "checkpoint_passed": false
      },
      "04": {
        "status": "pending",
        "steps_required": ["lock_release", "feedback_hooks", "execution_summary", "final_summary"],
        "steps_completed": [],
        "checkpoint_passed": false
      }
    }
  }
  ```
- **Rationale:** The /dev workflow's phase-state.json mechanism eliminated phase-skipping incidents (RCA-018 REC-1). The same mechanism applied to QA would: (1) externally validate phase completion via CLI, (2) track required vs. completed sub-steps, (3) persist audit trail (not deleted on pass), (4) enable resume from interrupted phases.
- **Testing:** Run `/qa STORY-XXX deep`, intentionally skip test integrity verification. Verify: `qa-phase-complete` CLI rejects Phase 1.5 completion because `test_integrity_verification` not in `steps_completed`.
- **Effort:** High (4-6 hours — CLI extension + SKILL.md refactor + testing)

### HIGH Priority (Implement This Sprint)

**REC-2: Add Test Integrity Verification as Explicit Numbered Step in SKILL.md Phase 1.5**

- **Problem:** Test Integrity Verification is buried in the reference file but not listed as a numbered step in SKILL.md's Phase 1.5 section. The orchestrator follows SKILL.md steps, not exhaustive reference file parsing.
- **Proposed Solution:** Add a new numbered step after the existing 5 diff-regression steps in SKILL.md's Phase 1.5 section, explicitly calling out test integrity verification. The existing steps 1-5 use implicit numbering within the "### Steps" subsection; the new step continues that sequence as step 6.
- **File:** `.claude/skills/devforgeai-qa/SKILL.md`
- **Section:** Phase 1.5, within the "### Steps" subsection, after step 5 ("Determine phase result")
- **Change:** Add:
  ```markdown
  6. **Execute Test Integrity Verification (STORY-502):**
     - Read snapshot file: `Glob(pattern="devforgeai/qa/snapshots/{STORY_ID}/red-phase-checksums.json")`
     - If snapshot found:
       - Read the snapshot JSON
       - For each file in snapshot `checksums` object: compute SHA-256 via `Bash(command="sha256sum {file}")`
       - Compare each computed hash to the snapshot's expected hash
       - If ANY mismatch: add CRITICAL finding `TEST TAMPERING` (blocks QA unconditionally — no override)
       - If ALL match: record `test_integrity: PASS`
     - If snapshot NOT found: log WARNING "Test integrity snapshot not found — skipping integrity verification (graceful degradation for pre-STORY-502 stories)" — QA continues without blocking
     - Record verification result in qa-phase-state.json `steps_completed` array
  ```
- **Rationale:** Making the step explicit in SKILL.md (not just in the reference file) prevents the orchestrator from treating it as supplementary content.
- **Effort:** Low (15 min — add step to SKILL.md)

**REC-3: Preserve QA Phase-State on PASS (Don't Delete Markers)**

- **Problem:** Step 4.5 of Phase 4 deletes all `.qa-phase-N.marker` files on QA PASS, destroying the audit trail. This makes post-hoc investigation impossible.
- **Proposed Solution:** Replace marker deletion with archival. The specific behavior depends on whether REC-1 is implemented:
  - **If REC-1 is implemented (qa-phase-state.json exists):** Keep `{STORY_ID}-qa-phase-state.json` in `devforgeai/workflows/` permanently (same location as /dev phase-state files). Delete old-style `.qa-phase-N.marker` files since they are superseded. The qa-phase-state.json IS the audit trail.
  - **If REC-1 is NOT yet implemented (only markers exist):** Move `.qa-phase-N.marker` files from `devforgeai/qa/reports/{STORY_ID}/` to a permanent archive directory `devforgeai/qa/archive/{STORY_ID}/` instead of deleting them.
- **File:** `.claude/skills/devforgeai-qa/SKILL.md` (Step 4.5 in Phase 4) and `references/phase-4-cleanup-workflow.md` (Step 4.5)
- **Change:** In SKILL.md Step 4.5 "Marker Cleanup [CONDITIONAL - QA PASSED ONLY]", replace the `rm` operation with the appropriate archival operation per above.
- **Rationale:** The /dev workflow preserves `phase-state.json` indefinitely (78+ files in `devforgeai/workflows/`). QA should do the same for auditability.
- **Dependency:** REC-3 should be implemented AFTER REC-1. If REC-1 lands first, REC-3 simplifies to "don't delete qa-phase-state.json" (which is the default behavior since it lives in `devforgeai/workflows/`).
- **Effort:** Low (15 min — change cleanup logic)

### MEDIUM Priority (Next Sprint)

**REC-4: Add Validation Checkpoint Checklists Within Phase 1.5 and Phase 2**

- **Problem:** Phase 1 and Phase 2 have "Completion Checklists" but Phase 1.5 has none. Sub-steps within phases lack explicit checklists that force the orchestrator to self-verify before writing the phase marker.
- **Proposed Solution:** Add Phase 1.5 Completion Checklist:
  ```markdown
  ### Phase 1.5 Completion Checklist
  - [ ] Diff regression detection executed (Steps 1-5)
  - [ ] Test integrity snapshot read (if exists)
  - [ ] Checksum comparison completed (if snapshot exists)
  - [ ] All findings classified by severity
  - [ ] Phase result determined (PASS/BLOCKED/WARN)
  ```
- **File:** `.claude/skills/devforgeai-qa/SKILL.md`
- **Rationale:** Checklists create a self-verification step. Combined with REC-1's CLI gates, the checklist items become required steps the CLI validates.
- **Effort:** Low (20 min)

### LOW Priority (Backlog)

**REC-5: Unify /dev and /qa Phase Tracking Under Single CLI Interface**

- **Problem:** /dev and /qa have divergent tracking mechanisms (phase-state.json vs markers). This creates maintenance burden and inconsistent enforcement.
- **Proposed Solution:** Extend `devforgeai-validate` to have a unified phase tracking interface: `phase-init --workflow=dev|qa`, `phase-complete --workflow=dev|qa`, with workflow-specific step requirements loaded from configuration.
- **Rationale:** Single interface reduces code duplication, ensures QA always benefits from /dev enforcement improvements.
- **Effort:** High (8-10 hours — refactor CLI + both skills)

---

## Implementation Checklist

- [ ] Review all recommendations
- [ ] **REC-1 (CRITICAL):** Add `--workflow=dev|qa` flag to existing phase-init/phase-complete/phase-ready CLI commands — **Implemented in:** STORY-517
- [ ] **REC-1:** Create qa-phase-state.json schema with steps_required/steps_completed per phase — **Implemented in:** STORY-517
- [ ] **REC-1:** Replace marker writes in SKILL.md with CLI gate calls — **Implemented in:** STORY-517
- [ ] **REC-2 (HIGH):** Add Test Integrity Verification as Step 6 in SKILL.md Phase 1.5 — **Implemented in:** STORY-518
- [ ] **REC-3 (HIGH):** Change Phase 4 cleanup to archive markers/state instead of delete — **Implemented in:** STORY-519
- [ ] **REC-4 (MEDIUM):** Add Phase 1.5 Completion Checklist to SKILL.md — **Implemented in:** STORY-520
- [x] **REC-5 (LOW):** Design unified phase tracking interface — **Implemented in:** STORY-521
- [ ] Test: Run `/qa` on story with snapshot, verify test integrity verification executes
- [ ] Test: Intentionally skip a sub-step, verify CLI gate blocks phase completion
- [ ] Mark RCA-045 as RESOLVED after REC-1 and REC-2 implemented

---

## Prevention Strategy

**Short-term (Immediate):**
- Add Test Integrity Verification as explicit numbered step in SKILL.md (REC-2) — prevents this specific skip
- Add Phase 1.5 completion checklist (REC-4) — adds self-verification layer

**Long-term (Framework Enhancement):**
- Implement qa-phase-state.json with CLI gates (REC-1) — eliminates the enforcement asymmetry between /dev and /qa
- Unify tracking interfaces (REC-5) — ensures both workflows always have equivalent enforcement
- Archive phase state on pass (REC-3) — enables post-hoc investigation

**Monitoring:**
- During QA execution, verify qa-phase-state.json `steps_completed` array matches `steps_required` before phase marker write
- Flag any QA run where `steps_completed.length < steps_required.length` as enforcement violation
- Track phase-skip incidents per sprint (target: zero)

---

## Related RCAs

- **RCA-043:** Test Integrity Snapshot Skipped (MEDIUM) — Creation side: /dev Phase 02 not creating snapshots. RCA-045 covers consumption side: QA not reading/comparing snapshots. Same feature (STORY-502), both sides lacking enforcement.
- **RCA-021:** QA Skill Phases Skipped (HIGH) — Prior QA phase-skipping incident. REC-1 through REC-5 improved enforcement but didn't add CLI gates equivalent to /dev's mechanism.
- **RCA-018:** Development Skill Phase Completion Skipping (HIGH) — Established the phase-state.json + CLI gate pattern that solved phase-skipping for /dev. RCA-045 recommends applying the same pattern to QA.
- **RCA-022:** Mandatory TDD Phases Skipped (HIGH) — Same root cause family: enforcement gaps in phase execution allowing silent skipping.
- **RCA-019:** Development Skill Phase Skipping Enforcement (HIGH) — Further refinements to /dev enforcement that QA should inherit.

**Pattern Evolution:**
```
RCA-018 → /dev phase-skipping → Fixed with phase-state.json + CLI gates
RCA-021 → /qa phase-skipping → Partially fixed with markers + pre-flight checks
RCA-043 → Snapshot not created in /dev → Fixed with checkpoint reordering
RCA-045 → Snapshot not verified in /qa → ROOT CAUSE: QA lacks /dev's enforcement mechanism
```

**Lesson:** /dev enforcement was upgraded (RCA-018 → CLI gates) but QA was not given the same upgrade. The enforcement asymmetry between the two workflows allows QA-specific steps to be skipped without detection.
