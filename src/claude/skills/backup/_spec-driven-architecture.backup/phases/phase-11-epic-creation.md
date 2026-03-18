# Phase 11: Epic Creation

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Create epic documents from structured requirements. CONDITIONAL phase — only executes when invoked via `/create-epic` command (COMMAND_MODE == "epic-creation") |
| **REFERENCES** | `.claude/skills/designing-systems/references/epic-management.md`, `feature-decomposition.md`, `feature-analyzer.md`, `complexity-assessment-workflow.md`, `complexity-assessment-matrix.md`, `artifact-generation.md`, `epic-validation-checklist.md`, `epic-validation-hook.md`, `technical-assessment-guide.md` |
| **STEP COUNT** | 8 mandatory steps |
| **SUBAGENTS** | `requirements-analyst` (BLOCKING), `architect-reviewer` (BLOCKING) |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:
- [ ] COMMAND_MODE verified as "epic-creation" (or phase skipped)
- [ ] All 6 context files confirmed present
- [ ] Requirements parsed into structured feature list
- [ ] Feature decomposition reviewed and approved by user
- [ ] Technical assessment completed by `architect-reviewer`
- [ ] Epic document written to `devforgeai/specs/Epics/EPIC-NNN-*.epic.md`
- [ ] Epic validated against `epic-validation-checklist.md`
- [ ] Epic file verified to exist via Glob

**IF any criterion is unmet: HALT. Do NOT declare epic creation complete.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/designing-systems/references/epic-management.md")
Read(file_path=".claude/skills/designing-systems/references/feature-decomposition.md")
Read(file_path=".claude/skills/designing-systems/references/feature-analyzer.md")
Read(file_path=".claude/skills/designing-systems/references/complexity-assessment-workflow.md")
Read(file_path=".claude/skills/designing-systems/references/complexity-assessment-matrix.md")
Read(file_path=".claude/skills/designing-systems/references/artifact-generation.md")
Read(file_path=".claude/skills/designing-systems/references/epic-validation-checklist.md")
Read(file_path=".claude/skills/designing-systems/references/epic-validation-hook.md")
Read(file_path=".claude/skills/designing-systems/references/technical-assessment-guide.md")
```

All 9 reads may be issued in parallel. Do NOT rely on memory of previous reads. Load fresh every time.

---

## Mandatory Steps

### Step 11.0: Command Mode Check (GATE)

**EXECUTE:**
Check the value of `$COMMAND_MODE` from the skill invocation context.

Decision logic:
- If `COMMAND_MODE == "context-creation"`: This phase does not apply. Display skip message and halt workflow.
- If `COMMAND_MODE == "epic-creation"`: Proceed to Step 11.1.

If skipping, display:
```
"Phase 11 skipped — not in epic-creation mode. Architecture context creation workflow complete."
```

**VERIFY:**
- `$COMMAND_MODE` value was checked (not assumed)
- Decision is unambiguous: either "context-creation" or "epic-creation"
- If neither value matches: HALT and AskUserQuestion for clarification

**RECORD:**
```json
checkpoint.phase_11.step_11_0 = {
  "command_mode": "<context-creation|epic-creation>",
  "gate_decision": "<proceed|skip>"
}
```

If `gate_decision` is "skip":
```json
checkpoint.phase_11.status = "skipped-auto",
checkpoint.phases_skipped = [...existing, "11"]
```
STOP. Workflow complete for context creation mode.

---

### Step 11.1: Discovery & Context Loading

**EXECUTE:**
Verify all 6 context files exist:
```
Glob(pattern="devforgeai/specs/context/*.md")
```
Confirm at least 6 files returned. Read `EPIC_NAME` from conversation context markers or skill arguments.

Load epic management reference (already loaded in Reference Loading, but confirm available):
```
Read(file_path=".claude/skills/designing-systems/references/epic-management.md")
```

**VERIFY:**
- Glob returned at least 6 context files
- `EPIC_NAME` is non-empty and non-null
- Epic management reference loaded successfully

**RECORD:**
```json
checkpoint.phase_11.step_11_1 = {
  "context_files_count": "<N>",
  "epic_name": "<EPIC_NAME>",
  "context_loaded": true
}
```

---

### Step 11.2: Requirements Input Parsing

**EXECUTE:**
Check if ideation output (YAML-structured requirements) is available in conversation context from a prior `/ideate` or `/brainstorm` session.

If structured requirements found: Parse into feature list with names, descriptions, and acceptance criteria.

If no structured requirements available:
```
AskUserQuestion:
  Question: "No ideation output found in context. Please describe the requirements for this epic."
  Header: "Epic Requirements Input"
  Options:
    - label: "Describe features"
      description: "List the features and capabilities this epic should deliver"
    - label: "Paste requirements document"
      description: "Paste structured requirements (YAML, markdown list, or free text)"
  multiSelect: false
```

**VERIFY:**
- Requirements source identified (ideation output or user input)
- At least 1 feature extracted from requirements
- Each feature has at minimum: name and description

**RECORD:**
```json
checkpoint.phase_11.step_11_2 = {
  "requirements_source": "<ideation_output|user_input>",
  "feature_count": "<N>",
  "features": [{ "name": "<feature name>", "description": "<brief>" }],
  "requirements_parsed": true
}
```

---

### Step 11.3: Feature Decomposition

**EXECUTE:**
```
Task(
  subagent_type="requirements-analyst",
  prompt="Decompose the following requirements into discrete features for epic '${EPIC_NAME}'.

  Requirements:
  ${parsed_requirements}

  Context files are at devforgeai/specs/context/. Read tech-stack.md and architecture-constraints.md to inform decomposition.

  For each feature provide:
  1. Feature name
  2. Description (2-3 sentences)
  3. Acceptance criteria (testable, specific)
  4. Estimated complexity (Low/Medium/High)
  5. Dependencies on other features (if any)

  Return structured JSON array of features."
)
```
This is a BLOCKING task. Wait for result before proceeding.

Present decomposed features to user for review:
```
AskUserQuestion:
  Question: "Review the decomposed features for epic '${EPIC_NAME}':\n\n${formatted_feature_list}\n\nApprove, modify, or add features?"
  Header: "Feature Decomposition Review"
  Options:
    - label: "Approve as-is"
      description: "Accept the feature decomposition"
    - label: "Modify features"
      description: "Adjust feature descriptions, split, or merge features"
    - label: "Add more features"
      description: "Include additional features not captured"
  multiSelect: false
```

**VERIFY:**
- Subagent returned structured result (not error or timeout)
- Each feature has all 5 required fields (name, description, AC, complexity, dependencies)
- User reviewed and approved (or modifications applied)

**RECORD:**
```json
checkpoint.phase_11.step_11_3 = {
  "subagent_invoked": "requirements-analyst",
  "features_decomposed": "<N>",
  "user_review": "<approved|modified|added>",
  "final_features": [{ "name": "<name>", "complexity": "<Low|Medium|High>" }]
}
```

---

### Step 11.4: Technical Assessment

**EXECUTE:**
```
Task(
  subagent_type="architect-reviewer",
  prompt="Assess technical feasibility of the following features for epic '${EPIC_NAME}' against project context files.

  Features:
  ${final_feature_list}

  Read and validate against:
  - devforgeai/specs/context/tech-stack.md (technology compatibility)
  - devforgeai/specs/context/architecture-constraints.md (architectural fit)
  - devforgeai/specs/context/dependencies.md (dependency availability)
  - devforgeai/specs/context/anti-patterns.md (anti-pattern risk)

  For each feature return:
  1. Feasibility: FEASIBLE / NEEDS_ADR / INFEASIBLE
  2. Risk level: LOW / MEDIUM / HIGH
  3. Technical notes (constraints, required patterns, concerns)
  4. If NEEDS_ADR: what decision needs an ADR

  Return structured JSON."
)
```
This is a BLOCKING task. Wait for result before proceeding.

**VERIFY:**
- Subagent returned structured result for every feature
- No feature marked INFEASIBLE without escalation to user
- If any feature is INFEASIBLE: AskUserQuestion to decide (remove, redesign, or override)
- If any feature NEEDS_ADR: note for epic document (ADR creation is a separate workflow)

**RECORD:**
```json
checkpoint.phase_11.step_11_4 = {
  "subagent_invoked": "architect-reviewer",
  "feasibility_results": {
    "feasible": "<count>",
    "needs_adr": "<count>",
    "infeasible": "<count>"
  },
  "risk_summary": { "low": "<N>", "medium": "<N>", "high": "<N>" },
  "assessment_complete": true
}
```

---

### Step 11.5: Epic Document Generation

**EXECUTE:**
Load the epic template:
```
Read(file_path=".claude/skills/designing-systems/assets/templates/epic-template.md")
```

Generate sequential EPIC number:
```
Glob(pattern="devforgeai/specs/Epics/EPIC-*.epic.md")
```
Count existing epics. New epic number = highest existing + 1 (zero-padded to 3 digits).

Populate the template with:
- **Title:** `${EPIC_NAME}`
- **Description:** Synthesized from requirements and assessment
- **Features list:** From Step 11.3 final features
- **Acceptance criteria:** Aggregated from feature-level AC
- **Technical notes:** From Step 11.4 assessment
- **Dependencies:** Cross-feature dependencies from decomposition
- **Complexity assessment:** From Step 11.4 risk summary
- **ADR requirements:** Features flagged NEEDS_ADR

**VERIFY:**
- Template loaded successfully
- Epic number is unique (not duplicating existing epic)
- All template sections populated (no empty required sections)
- Feature count in document matches Step 11.3 final count

**RECORD:**
```json
checkpoint.phase_11.step_11_5 = {
  "template_loaded": true,
  "epic_number": "<NNN>",
  "epic_title": "<EPIC_NAME>",
  "feature_count": "<N>",
  "document_generated": true
}
```

---

### Step 11.6: Validation & Self-Healing

**EXECUTE:**
Validate the generated epic document against the validation checklist:
```
Read(file_path=".claude/skills/designing-systems/references/epic-validation-checklist.md")
```

Check each validation criterion against the generated document:
- Title present and descriptive
- Description section non-empty
- Features list has at least 1 feature
- Each feature has acceptance criteria
- Technical notes section present
- Dependencies documented (or "None" explicitly stated)
- Complexity assessment included

If validation fails on minor issues (missing optional sections, formatting): Auto-fix via Edit.

If validation fails on major issues (missing required sections, conflicting AC):
```
AskUserQuestion:
  Question: "Epic validation found major issue: {issue_description}\nHow should this be resolved?"
  Header: "Epic Validation Issue"
  Options:
    - label: "Fix now"
      description: "Provide corrected content for the failing section"
    - label: "Accept and continue"
      description: "Proceed with the epic as-is (issue documented)"
  multiSelect: false
```

Re-validate after fixes (one round only — if second validation fails, proceed with warnings).

**VERIFY:**
- Validation checklist was loaded and applied
- All major issues either fixed or explicitly accepted by user
- Minor auto-fixes applied without error
- Re-validation executed if fixes were applied

**RECORD:**
```json
checkpoint.phase_11.step_11_6 = {
  "validation_run": true,
  "issues_found": "<count>",
  "major_issues": "<count>",
  "minor_auto_fixed": "<count>",
  "user_resolved": "<count>",
  "revalidation_passed": "<true|false|not_needed>",
  "validation_complete": true
}
```

---

### Step 11.7: Epic File Creation & Report

**EXECUTE:**
Write the validated epic document:
```
Write(file_path="devforgeai/specs/Epics/EPIC-<NNN>-<title-slug>.epic.md", content=<epic_document>)
```

Verify the file was created:
```
Glob(pattern="devforgeai/specs/Epics/EPIC-<NNN>-*.epic.md")
```

Invoke epic validation hook (non-blocking):
```
Read(file_path=".claude/skills/designing-systems/references/epic-validation-hook.md")
```
Execute any post-creation hooks defined in the reference.

Display success report:
```
============================================================
  EPIC CREATED SUCCESSFULLY
============================================================
  Epic:       EPIC-<NNN>: <EPIC_NAME>
  Path:       devforgeai/specs/Epics/EPIC-<NNN>-<title-slug>.epic.md
  Features:   <N> features defined
  Complexity: <LOW|MEDIUM|HIGH> overall
  ADRs needed: <N> (for features requiring architecture decisions)
------------------------------------------------------------
  Next Steps:
    /create-story  → Create stories from this epic's features
    /create-sprint → Plan sprint with epic stories
    /dev           → Begin story development (TDD)
============================================================
```

**VERIFY:**
- Epic file exists at target path (Glob returned exactly 1 match)
- File content length > 500 characters (substantial document, not stub)
- Success report displayed with all fields populated

**RECORD:**
```json
checkpoint.phase_11.step_11_7 = {
  "epic_file": "devforgeai/specs/Epics/EPIC-<NNN>-<title-slug>.epic.md",
  "file_verified": true,
  "content_length": "<character count>",
  "validation_hook_invoked": true,
  "report_displayed": true,
  "epic_created": true
}
checkpoint.phase_11.status = "completed"
```

---

## Phase Transition Display

```
============================================================
  PHASE 11 COMPLETE: Epic Creation
============================================================
  Epic:                EPIC-<NNN>: <EPIC_NAME>
  Features:            <N> defined
  Technical assessment: <N> feasible, <N> need ADR
  Validation:          [PASSED / PASSED WITH WARNINGS]
------------------------------------------------------------
  Epic creation workflow complete.
============================================================
```
