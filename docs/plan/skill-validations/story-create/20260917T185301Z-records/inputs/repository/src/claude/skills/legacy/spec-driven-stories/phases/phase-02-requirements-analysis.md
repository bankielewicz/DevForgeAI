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
- **STEP COUNT:** 4 (2.1, 2.2, 2.3, 2.4) + 1 substep (2.3.5)
- **REFERENCE FILES:**
  - `references/requirements-analysis.md`
  - `references/acceptance-criteria-core.md` (always)
  - `references/acceptance-criteria-domains.md` (always)
  - `references/acceptance-criteria-refactor.md` (ONLY when `type: refactor`)
  - `contracts/requirements-analyst-contract.yaml`

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-stories/references/requirements-analysis.md")

# AC patterns split into 3 focused files (was single 1,387-line file that exceeded Read budget)
Read(file_path=".claude/skills/spec-driven-stories/references/acceptance-criteria-core.md")     # Always: core principles, GWT, error handling, edge cases, testing
Read(file_path=".claude/skills/spec-driven-stories/references/acceptance-criteria-domains.md")  # Always: 13 domain libraries (CRUD, Auth, etc.)

# Refactor patterns — load ONLY if story type is "refactor"
IF story frontmatter has `type: refactor`:
    Read(file_path=".claude/skills/spec-driven-stories/references/acceptance-criteria-refactor.md")

Read(file_path=".claude/skills/spec-driven-stories/contracts/requirements-analyst-contract.yaml")

# Validator-traps awareness (added per /create-story remediation 2026-04-26): pre-load
# known-validator-trap reference so the orchestrator can pre-emptively avoid the traps
# (e.g., paraphrase stakeholder quotes, choose Configuration over DataModel for in-memory
# schemas, etc.) BEFORE Phase 07 fires regression-slot-consuming HALTs.
Read(file_path=".claude/skills/spec-driven-stories/references/validator-traps.md")
```

IF any Read fails: HALT -- "Phase 02 reference files not loaded."

---

## Mandatory Steps (4)

### Step 2.1: Confirm Subagent File-Creation Impossibility (RCA-007)

**EXECUTE:**
```
Display: "Pre-invocation check: subagent has no Write/Edit tools — file creation blocked by design (RCA-007)"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=02 --step=2.1 --project-root=.
```
Update checkpoint: `phases["02"].steps_completed.append("2.1")`

---

### Step 2.2: Invoke story-requirements-analyst Subagent

The subagent owns all codebase research for Phase 02 (its tool whitelist is `Read, Grep, Glob`). Pass the feature description + metadata and delegate — abstract feature descriptions are the subagent's Baseline Research Protocol's problem, not the orchestrator's. Pre-research from the orchestrator pollutes context and duplicates work the subagent redoes anyway.

**EXECUTE:**
```
Invoke Agent(subagent_type="story-requirements-analyst") with prompt containing:
  - Feature description: $FEATURE_DESCRIPTION
  - Story ID: $STORY_ID
  - Story type: $TYPE
  - Epic context: $EPIC_ID (if available, read epic file for context)
  - Priority: $PRIORITY
  - Baseline research mandate: If the feature description is abstract (vague scope, no concrete file paths, no specific code patterns named), use your Read/Grep/Glob tools to research the codebase BEFORE generating ACs. Follow the Baseline Research Protocol in your agent definition. Ground every AC in file:line references where possible.
  - Instructions: Generate CONTENT ONLY (no file creation)
    - User Story (As a / I want / So that)
    - 3+ Acceptance Criteria (Given/When/Then)
    - Edge Cases
    - Non-Functional Requirements

  - **Verbatim-AC extraction mandate (FM-1 remediation, 2026-04-26):** IF an Epic ID is provided AND the epic file contains a `## Feature Specifications` section with `**Acceptance criteria:**` blocks for the mapped feature, EXTRACT VERBATIM the full acceptance-criteria array from the matching feature block. Do NOT synthesize new ACs. Do NOT summarize, paraphrase, or omit items. If a feature has 6 ACs in the epic, the story MUST list all 6 (plus any CC-N cross-cutting items referenced by that feature). Preserve exact wording — copy each AC string character-for-character. ONLY synthesize new ACs when no epic AC source exists (greenfield/recommendation-driven story OR epic uses pre-template-v2 format with no `**Acceptance criteria:**` blocks).

  - **Split-feature detection mandate (FM-2 remediation, 2026-04-26):** Scan the feature description for split signals: literal phrases "two-part", "three-part", "Part 1 of", numbered subitems formatted as "1. (a) ... 2. (b) ..." or "1. **(verification)** ... 2. **(amendment)** ...", or explicit `Stories: 1-2` / `Stories: 2-3` metadata in the epic Scope table. IF a split signal is detected AND the current $POINTS value is less than the epic's stated `Points:` value for the feature: emit a `<split_feature_signal>` block in the output containing: (a) `detected_pattern` (verbatim quote of the signal text), (b) `suggested_part` (e.g., "This story is Part 1 of N for Feature F-NN"), (c) `sibling_story_topics` (one-line description of what each remaining part should cover). The orchestrator will surface this signal to the user via AskUserQuestion before Phase 05 writes the story file, allowing the user to confirm split-story scoping or merge into a single multi-pt story.

  - per-AC implementation hint elements (optional — trivial ACs may omit the implementation element):
    For each acceptance_criteria, generate an optional <implementation> block containing:
      - <approach>: 1-3 sentence implementation approach summary
      - <pseudocode>: optional code sketch (language-appropriate per tech-stack.md)
      - <rationale>: optional decision rationale referencing context files
      - <task_hint>: optional prompt fragment for subagent delegation

    XML format example:
    ```xml
    <acceptance_criteria id="AC1">
      <given>...</given>
      <when>...</when>
      <then>...</then>
      <implementation>
        <approach>Use repository pattern to fetch user by email, validate password hash</approach>
        <pseudocode><![CDATA[
          user = repo.find_by_email(email)
          if not user or not verify(password, user.hash):
              raise AuthError
        ]]></pseudocode>
        <rationale>Repository pattern per coding-standards.md; DI per architecture-constraints.md</rationale>
        <task_hint>backend-architect: implement login endpoint with DI</task_hint>
      </implementation>
    </acceptance_criteria>
    ```

IF story-requirements-analyst not available:
  Fallback to Agent(subagent_type="requirements-analyst") with enhanced constraints:
    - "Return CONTENT ONLY. Do NOT create files."
    - "Output must include all 4 sections."
    - "If possible, include per-AC <implementation> elements with at least <approach> for non-trivial ACs."

# ---------------------------------------------------------------------------
# FROM_RECOMMENDATIONS mode: authoritative-REC instructions
# ---------------------------------------------------------------------------
IF conversation contains "**From Recommendations:** true":
  Append to the subagent prompt (BEFORE "Capture subagent output"):
    """
    FROM_RECOMMENDATIONS mode — authoritative constraints:

    The $FEATURE_DESCRIPTION contains ${N} REC entries sourced from
    ${Source Recommendations File}. Each REC entry is AUTHORITATIVE.

    For every REC entry, produce EXACTLY ONE <acceptance_criteria> where:
      - <given> quotes the target file:lines verbatim (from the REC's file/lines fields)
      - <when> paraphrases the condition described in REC.description
      - <then> quotes REC.verification.expected CHARACTER-FOR-CHARACTER
        (do not soften, summarize, or paraphrase the expected output)
      - <implementation><pseudocode> contains either:
          * the REC's before_code → after_code diff (when both non-null), OR
          * a numbered list of REC.remediation_steps (when before/after are null)
      - <implementation><rationale> cites the source REC-ID and severity
        (e.g., "Per REC-STORY-648-M-001 (MEDIUM, security)")

    Do NOT invent ACs outside the provided REC set. The total AC count
    MUST equal the number of REC entries in $FEATURE_DESCRIPTION.

    Do NOT soften severity descriptions. Do NOT substitute generic
    remediation text for the REC's specific before_code/after_code or
    remediation_steps.
    """

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
# Sprint A (STORY-646): CLI replaces inline required_sections loop with full contract validation
# Write $REQUIREMENTS_OUTPUT to disk first (per operational-safety.md Rule 2)
scratch_path = "tmp/${SESSION_ID}/phase-outputs/phase-02-requirements.txt"
Bash("mkdir -p tmp/${SESSION_ID}/phase-outputs")
Write(file_path=scratch_path, content=$REQUIREMENTS_OUTPUT)

cli_result = Bash(f"devforgeai-validate validate-subagent-contract --output-file={scratch_path} --contract-file=src/claude/skills/spec-driven-stories/contracts/requirements-analyst-contract.yaml --format=json")

IF cli_result.exit_code == 0:
  Display: "Subagent output validated against full YAML contract — no violations (STORY-646)"
ELSE IF cli_result.exit_code == 1:
  cli_parsed = json_parse(cli_result.stdout)
  critical_high = [v for v in cli_parsed.violations if v.severity in ["CRITICAL", "HIGH"]]
  IF len(critical_high) > 0:
    Display: f"Subagent output has {len(cli_parsed.violations)} violation(s) — re-invoking story-requirements-analyst"
    Re-invoke story-requirements-analyst with violation details
ELSE IF cli_result.exit_code == 127:
  # CLI not installed — fall back to legacy section-name check
  Display: "WARNING: validate-subagent-contract CLI not installed — using legacy section check (exit 127)"
  required_sections = ["User Story", "Acceptance Criteria", "Edge Cases", "Non-Functional Requirements"]
  missing_sections = [s for s in required_sections if f"## {s}" not in $REQUIREMENTS_OUTPUT]
  IF missing_sections:
    Display: f"Subagent output missing sections: {missing_sections}"
    Re-invoke subagent with emphasis on missing sections

# Post-invocation file diff: NOT needed (RCA-007 Phase 3 — subagent has no Write/Edit tools)
```

**VERIFY:** All 4 required sections present in `$REQUIREMENTS_OUTPUT`.

#### Step 2.3.5: Canonical user-story format check (Sprint 4 patch — closes Sprint 4 Checkpoint #3 wiring gap)

The existing Step 2.3 check (above) verifies only that the literal section heading `"User Story"` appears in `$REQUIREMENTS_OUTPUT`. It does NOT verify that the section body matches the canonical `"As a <role>, I want <goal>, So that <reason>"` format. A subagent could emit a "User Story" section containing prose that bypasses the canonical pattern and the rest of Phase 02 would pass.

This substep invokes the `validate-user-story` CLI validator (implemented in Sprint 4 core, commit `f0307b8c`) which regex-checks the format per `src/claude/scripts/devforgeai_cli/validators/user_story.py`. PRIMARY path uses the CLI; exit-127 falls back to the section-name-only check already completed in Step 2.3 above.

**EXECUTE:**
```
# $REQUIREMENTS_OUTPUT is in-memory subagent output; CLI reads from disk.
# Write to project-scoped tmp per operational-safety.md Rule 2.
scratch_path = "tmp/${SESSION_ID}/phase-outputs/phase-02-requirements.txt"
Bash("mkdir -p tmp/${SESSION_ID}/phase-outputs")
Write(file_path=scratch_path, content=$REQUIREMENTS_OUTPUT)

cli_result = Bash(f"devforgeai-validate validate-user-story --story-file={scratch_path} --format=json")

IF cli_result.exit_code == 0:
  Display: "User story format: canonical 'As a / I want / So that' present (Sprint 4 patch)"

ELSE IF cli_result.exit_code == 1:
  parsed = json_parse(cli_result.stdout)
  IF parsed.user_story_count == 0:
    Display: "Subagent output missing canonical user story — re-invoking with format emphasis..."
    Re-invoke story-requirements-analyst with emphasis:
      "Include EXACTLY ONE 'As a <role>, I want <goal>, So that <reason>' block in the User Story section. The entire sentence must be in this form; no prose alternatives."
    # After re-invocation, re-run this Step 2.3.5. On still-zero result:
    HALT: "Phase 02 user-story format check failed after re-invocation. Subagent produced no canonical user story."
  ELSE IF parsed.user_story_count > 1:
    HALT: f"Subagent produced {parsed.user_story_count} user stories; expected exactly 1. Prompt/template issue — re-invocation will not fix. See {cli_result.stdout}."

ELSE IF cli_result.exit_code == 127:
  # CLI not installed. Step 2.3 section-name check above is the fallback scope;
  # no additional work here. This is a documented degradation per master plan §4.3.
  Display: "validate-user-story CLI not installed — using section-name-only check from Step 2.3 (deprecated fallback)"

ELSE:
  HALT: f"validate-user-story CLI unexpected exit {cli_result.exit_code}: {cli_result.stdout}"
```

**VERIFY:** Exactly ONE canonical user story block present in `$REQUIREMENTS_OUTPUT` (or CLI unavailable — fallback to Step 2.3 section-name check already verified).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=02 --step=2.3.5 --project-root=.
```
Update checkpoint: `phases["02"].steps_completed.append("2.3.5")`

#### Per-AC implementation element validation (HALT — Sprint 2.2, USER MANDATE)

This is a **BLOCKING** check. Every acceptance criterion MUST have an
`<implementation>` block with at least an `<approach>` child. Without it, a
fresh `/dev` Claude session has nothing to feed `test-automator` and
`backend-architect` — the "new session without context" failure mode this
sprint exists to eliminate.

The previous policy (non-blocking warning when ac_count >= 3 AND
implementation_count == 0) was insufficient. It is replaced below.

```
# Scan subagent output for <implementation> elements
implementation_count = count occurrences of "<implementation>" in $REQUIREMENTS_OUTPUT
ac_count             = count Given/When/Then blocks in $REQUIREMENTS_OUTPUT

# === Sprint 2.2 — full-fidelity HALT (was WARN) ============================
IF ac_count > 0 AND implementation_count < ac_count:

  # Identify exactly which ACs are missing the <implementation> block.
  missing_acs = []
  FOR each AC in $REQUIREMENTS_OUTPUT:
    IF AC does not contain "<implementation>":
      missing_acs.append(AC.id)

  Display: "Missing <implementation> blocks for ACs: {missing_acs}"
  Display: "Re-invoking story-requirements-analyst with targeted prompt..."

  # Single re-invocation chance. Targeted prompt — do NOT regenerate the
  # entire requirements output, only fill in the missing implementation
  # blocks.
  re_invoke story-requirements-analyst with prompt:
    "For each AC listed ({missing_acs}), generate an <implementation> block
     containing AT MINIMUM an <approach> child. Preserve all other ACs and
     Given/When/Then content unchanged. Output the full updated
     <acceptance_criteria> set."

  # Recount after re-invocation.
  implementation_count = count occurrences of "<implementation>" in $REQUIREMENTS_OUTPUT

  IF implementation_count < ac_count:
    HALT: "Story creation BLOCKED — story-requirements-analyst could not
           produce <implementation> blocks for every AC after retargeted
           re-invocation. A full-fidelity story file requires every AC to
           carry implementation guidance. Aborting Phase 02; do not
           proceed to Phase 03."
# ===========================================================================
```

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

### Step 2.5: Sizing Sanity Check (FM-3 remediation, 2026-04-26)

**Purpose:** Detect undersized stories before Phase 05 commits the story file. STORY-655 (1pt with 10 ACs / 22 checklist items / 6 BRs / 7 NFRs) is the documented case this step prevents.

**EXECUTE:**

After Step 2.4 (Refine if Incomplete) completes, perform a structural-budget reality-check on the subagent output:

```python
ac_count = count("<acceptance_criteria " in $REQUIREMENTS_OUTPUT)
edge_case_count = count(non-empty bullet items under "Edge Cases" section in $REQUIREMENTS_OUTPUT)
nfr_count = count(non-empty entries under "Non-Functional Requirements" in $REQUIREMENTS_OUTPUT)

# Heuristic budget per points value (DERIVED — calibrated against typical DevForgeAI sizing patterns)
budget = {
  1: { "ac_max": 4,  "nfr_max": 3  },
  2: { "ac_max": 6,  "nfr_max": 5  },
  3: { "ac_max": 8,  "nfr_max": 7  },
  5: { "ac_max": 12, "nfr_max": 10 },
  8: { "ac_max": 18, "nfr_max": 14 }
}

current_points = $POINTS  # from Phase 01 context markers (story frontmatter)
budget_for_points = budget.get(int(current_points), { "ac_max": 999, "nfr_max": 999 })

IF ac_count > budget_for_points.ac_max OR nfr_count > budget_for_points.nfr_max:
  AskUserQuestion:
    Question: f"Sizing reality check: this story has {ac_count} ACs and {nfr_count} NFRs but is sized {current_points}pt. Typical {current_points}pt budget is ≤{budget_for_points.ac_max} ACs / ≤{budget_for_points.nfr_max} NFRs. How should this be resolved?"
    Header: "Sizing"
    Options:
      - label: "Re-size to match scope"
        description: "Update story points field to better reflect documented scope (orchestrator will prompt for new value)"
      - label: "Trim to fit current sizing"
        description: "Re-invoke story-requirements-analyst to reduce AC/NFR scope to fit the {current_points}pt budget"
      - label: "Accept oversized scope"
        description: "Proceed as-is; document deviation in story Notes section under '## Sizing Deviation'"
    multiSelect: false

  IF user selects "Re-size to match scope":
    Prompt user for new points value (1, 2, 3, 5, 8)
    Update context marker $POINTS = new value
    Continue to Phase 03 with updated sizing
  ELIF user selects "Trim to fit current sizing":
    Re-invoke story-requirements-analyst with prompt:
      "Current AC count {ac_count} and NFR count {nfr_count} exceed the {current_points}pt budget (max {budget_for_points.ac_max} ACs / {budget_for_points.nfr_max} NFRs). Reduce scope to fit budget while preserving the highest-priority requirements. Output the trimmed <acceptance_criteria> set and revised NFR list."
    Re-run Step 2.5 once after re-invocation
  ELIF user selects "Accept oversized scope":
    Append to $REQUIREMENTS_OUTPUT a "## Sizing Deviation" section noting the budget breach with timestamp and rationale
    Continue
```

**VERIFY:** User response captured (when prompted) OR budget check passed without prompt; `$REQUIREMENTS_OUTPUT` matches the sizing decision.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=02 --step=2.5 --project-root=.
```
Update checkpoint: `phases["02"].steps_completed.append("2.5")`

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
- [ ] Implementation hints present for every AC (BLOCKING per Sprint 2.2 USER MANDATE — HALT if implementation_count < ac_count)

**Gate Check (formerly Phase 2-3 Gate):**
```
required_sections = ["User Story", "Acceptance Criteria", "Edge Cases", "Non-Functional Requirements"]
FOR each section in required_sections:
  IF section NOT in $REQUIREMENTS_OUTPUT:
    HALT: "Phase 2-3 Gate FAILED: Missing {section}"
Display: "Phase 2-3 Gate PASSED: All 4 required sections present"
```

IF any unchecked: HALT -- "Phase 02 exit criteria not met"

### Persist Phase 02 Output Cache (Sprint 3.6)

Contract: `contracts/phase-output-schema.json` (`phase02Output`).
Readers: Phase 05 (AC embedding), Phase 07 (AC fidelity).

```bash
mkdir -p tmp/${SESSION_ID}/phase-outputs
```

```
# Best-effort extraction. Cache is derivative; user_story.py validator remains
# authoritative. Empty strings / empty arrays on extraction failure are allowed.
user_story        = first match of "As an?\s+.+?\bSo that\s+.+?(?=\n\n|\Z)" (dotall) in $REQUIREMENTS_OUTPUT
acceptance_arr    = all <acceptance_criteria[^>]*>.*?</acceptance_criteria> blocks, parsed to {id,given,when,then}
impl_xml_blocks   = all <implementation>.*?</implementation> blocks verbatim (CDATA preserved)
ac_count          = value from Step 2.3 counter
edge_cases        = bullet list under "## Edge Cases"; [] on extraction failure
nfrs              = items under "## Non-Functional Requirements"; [] on extraction failure

Write(file_path="tmp/${SESSION_ID}/phase-outputs/phase-02.json",
      content=json_serialize({
        "schema_version": "1.0",
        "phase_id": "02",
        "user_story": user_story,
        "acceptance_criteria": acceptance_arr,
        "edge_cases": edge_cases,
        "nfrs": nfrs,
        "implementation_xml_blocks": impl_xml_blocks,
        "ac_count": ac_count
      }))
```

## Phase Transition Display

```
Display: "Phase 02 complete. Requirements analysis validated."
Display: "Proceeding to Phase 03: Technical Specification..."
```

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.
