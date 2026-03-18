# Phase 02: Requirements Analysis

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from=01 --to=02 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 01 incomplete. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Generate user story (As a/I want/So that), 3+ acceptance criteria (Given/When/Then), edge cases, and non-functional requirements via subagent delegation
- **REQUIRED SUBAGENTS:** story-requirements-analyst (BLOCKING)
- **REQUIRED ARTIFACTS:** User story text, 3+ ACs, edge cases list, NFR list
- **STEP COUNT:** 4
- **REFERENCE FILES:**
  - `references/requirements-analysis.md`
  - `references/acceptance-criteria-patterns.md`
  - `contracts/requirements-analyst-contract.yaml`

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-stories/references/requirements-analysis.md")
Read(file_path="src/claude/skills/spec-driven-stories/references/acceptance-criteria-patterns.md")
Read(file_path="src/claude/skills/spec-driven-stories/contracts/requirements-analyst-contract.yaml")
```

IF any Read fails: HALT -- "Phase 02 reference files not loaded."

Do NOT rely on memory of previous reads. Load ALL references fresh.

---

## Mandatory Steps (4)

### Step 2.1: Pre-Invocation File System Snapshot (RCA-007)

**EXECUTE:**
```
# Capture file system state before subagent invocation
pre_snapshot = Glob(pattern="devforgeai/specs/Stories/STORY-*.story.md")
pre_file_count = len(pre_snapshot)
Display: "Pre-invocation snapshot: {pre_file_count} story files"
```

**VERIFY:** `pre_file_count` is a non-negative integer.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=02 --step=2.1 --project-root=.
```
Update checkpoint: `phases["02"].steps_completed.append("2.1")`

---

### Step 2.2: Invoke story-requirements-analyst Subagent

**EXECUTE:**
```
Invoke Agent(subagent_type="story-requirements-analyst") with prompt containing:
  - Feature description: $FEATURE_DESCRIPTION
  - Story ID: $STORY_ID
  - Story type: $TYPE
  - Epic context: $EPIC_ID (if available, read epic file for context)
  - Priority: $PRIORITY
  - Instructions: Generate CONTENT ONLY (no file creation)
    - User Story (As a / I want / So that)
    - 3+ Acceptance Criteria (Given/When/Then)
    - Edge Cases
    - Non-Functional Requirements

IF story-requirements-analyst not available:
  Fallback to Agent(subagent_type="requirements-analyst") with enhanced constraints:
    - "Return CONTENT ONLY. Do NOT create files."
    - "Output must include all 4 sections."

Capture subagent output as $REQUIREMENTS_OUTPUT
```

**VERIFY:** `$REQUIREMENTS_OUTPUT` is non-empty and contains text.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=02 --step=2.2 --project-root=.
```
Update checkpoint: `phases["02"].steps_completed.append("2.2")`

---

### Step 2.3: Validate Subagent Output & File System Diff (RCA-007)

**EXECUTE:**
```
# Contract-based validation
required_sections = ["User Story", "Acceptance Criteria", "Edge Cases", "Non-Functional Requirements"]
missing_sections = []

FOR each section in required_sections:
  IF section NOT found in $REQUIREMENTS_OUTPUT:
    missing_sections.append(section)

IF missing_sections is NOT empty:
  Display: "Subagent output missing sections: {missing_sections}"
  Display: "Re-invoking subagent with explicit section requirements..."
  Re-invoke subagent with emphasis on missing sections

# Post-invocation file system diff (RCA-007)
post_snapshot = Glob(pattern="devforgeai/specs/Stories/STORY-*.story.md")
post_file_count = len(post_snapshot)

IF post_file_count > pre_file_count:
  new_files = post_snapshot - pre_snapshot
  Display: "WARNING: Subagent created unauthorized files: {new_files}"
  # Delete unauthorized files
  FOR each unauthorized_file in new_files:
    Display: "Removing unauthorized file: {unauthorized_file}"
```

**VERIFY:** All 4 required sections present in `$REQUIREMENTS_OUTPUT`. File count unchanged.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=02 --step=2.3 --project-root=.
```
Update checkpoint: `phases["02"].steps_completed.append("2.3")`

---

### Step 2.4: Refine if Incomplete

**EXECUTE:**
```
# Validate AC quality
ac_count = count Given/When/Then blocks in $REQUIREMENTS_OUTPUT

IF ac_count < 3:
  Display: "Only {ac_count} ACs found. Minimum 3 required."
  Supplement with additional ACs based on edge cases and feature description

# Validate NFR quality
nfr_items = extract NFR items from $REQUIREMENTS_OUTPUT
FOR each nfr in nfr_items:
  IF nfr contains vague terms ("fast", "scalable", "reliable") without metrics:
    Replace with measurable version (e.g., "< 200ms response time")

Display: "Requirements analysis complete:"
Display: "  - User Story: present"
Display: "  - Acceptance Criteria: {ac_count}"
Display: "  - Edge Cases: {edge_case_count}"
Display: "  - NFRs: {nfr_count}"
```

**VERIFY:** AC count >= 3, all NFRs have measurable metrics.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=02 --step=2.4 --project-root=.
```
Update checkpoint: `phases["02"].steps_completed.append("2.4")`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=02 --checkpoint-passed --project-root=.
```

## Exit Verification Checklist (absorbs Phase 2-3 Gate)

- [ ] User Story present (As a / I want / So that format)
- [ ] 3+ Acceptance Criteria present (Given/When/Then format)
- [ ] Edge Cases section present and non-empty
- [ ] Non-Functional Requirements section present with measurable metrics
- [ ] No unauthorized files created (file count unchanged from pre-snapshot)

**Gate Check (formerly Phase 2-3 Gate):**
```
required_sections = ["User Story", "Acceptance Criteria", "Edge Cases", "Non-Functional Requirements"]
FOR each section in required_sections:
  IF section NOT in $REQUIREMENTS_OUTPUT:
    HALT: "Phase 2-3 Gate FAILED: Missing {section}"
Display: "Phase 2-3 Gate PASSED: All 4 required sections present"
```

IF any unchecked: HALT -- "Phase 02 exit criteria not met"

## Phase Transition Display

```
Display: "Phase 02 complete. Requirements analysis validated."
Display: "Proceeding to Phase 03: Technical Specification..."
```
