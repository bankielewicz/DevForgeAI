# Fix Actions Catalog

Classification matrix and fix procedures for each audit finding type. This file is the SSOT for how findings are classified and remediated.

---

## Table of Contents

1. [Classification Matrix](#classification-matrix)
2. [Safety Rules](#automated-fix-safety-rules)
3. [Automated Fix Procedures](#automated-fix-procedures)
4. [Interactive Fix Procedures](#interactive-fix-procedures)
5. [Batch Fix Strategy](#batch-fix-strategy)
6. [Multishot Examples](#multishot-examples)

---

## Classification Matrix

| Finding Type | Classification | Risk Level | Description |
|---|---|---|---|
| `quality/broken_file_reference` | automated | safe | String replace in single file using evidence old/new values |
| `provenance/missing_brainstorm_frontmatter` | automated | safe | Append YAML field to epic/story frontmatter |
| `provenance/missing_frontmatter` | automated | safe | Insert YAML field into frontmatter block |
| `quality/stale_status_label` | automated | safe | Update frontmatter status field |
| `context/invalid_path` | interactive | structural | Multi-file OR context-file change — user must choose approach |
| `adr/implicit_adr_need` | interactive | structural | Requires reading ADR and making judgment |
| `provenance/broken_brainstorm_ref` | interactive | structural | May require brainstorm file creation |
| `dependency/circular` | interactive | structural | Dependency graph restructure needed |
| `dependency/missing_story` | interactive | structural | Story may need to be created first |
| `quality/refactor_missing_preservation_ac` | interactive | structural | Read source files, generate content-preservation ACs, user confirms |
| `quality/refactor_nfr_without_ac` | interactive | structural | Parse NFRs, generate enforcement ACs, user confirms |
| `quality/refactor_askuser_placement_missing` | interactive | structural | Generate lean orchestration compliance AC, user confirms |
| `quality/refactor_missing_golden_capture` | interactive | structural | Generate golden output DoD items, user confirms |
| `coherence/schema_mismatch` | interactive | structural | Cross-story schema alignment — read plan for canonical schema, update divergent story |
| `coherence/api_contract_error` | automated | safe | Replace wrong API field name with correct field name (deterministic, single-file) |
| `coherence/plan_story_drift` | interactive | structural | Diff plan vs story — user chooses which values to align |
| `coherence/naming_inconsistency` | automated | safe | Rename artifacts to match plan naming convention (deterministic, single-file) |
| `coherence/format_inconsistency` | interactive | structural | Replace format pattern across multiple ACs — user confirms canonical format |
| `coherence/instruction_contradiction` | interactive | structural | Resolve by reading plan for authoritative instruction |
| `coherence/dependency_assumption_mismatch` | interactive | structural | Update dependent story's assumptions to match dependency's actual spec |
| `template/missing_section` (Required) | automated | safe | Insert section header + scaffold from template-upgrade-snippets.md + AUDIT-DEFERRED marker. See template-upgrade-procedures.md P1. |
| `template/missing_section` (Conditional) | automated | safe | Insert section header + empty scaffold (no marker). See template-upgrade-procedures.md P2. |
| `template/missing_frontmatter_field` (derivable) | automated | safe | Insert frontmatter field with derivable default value. See template-upgrade-procedures.md P3. |
| `template/missing_frontmatter_field` (ambiguous) | interactive | structural | User chooses value via AskUserQuestion. See template-upgrade-procedures.md P4. |
| `template/legacy_workflow_status` | automated | safe | Rename section to '## Change Log' and convert checkpoint list to table. See template-upgrade-procedures.md P5. |
| `template/legacy_format` | interactive | structural | Markdown→XML AC conversion; user supplies source_files per AC. See template-upgrade-procedures.md P6. |
| `template/informal_dependency_detected` | interactive | structural | Promote prose 'Depends on STORY-NNN' to formal depends_on array. See template-upgrade-procedures.md P7. |
| `template/version_drift` | automated | safe (gated) | Bump format_version field; GATED by all sibling findings resolving to applied or deferred. See template-upgrade-procedures.md P8. |
| `template/cross_story_drift` | advisory | none | Report-only; addressed by upgrading each story individually. |
| `quality/non_deterministic_AC` | interactive | structural | AC references content (format, schema, structure) whose definition lives in an unresolved Open Question. User supplies the format via AskUserQuestion (3-option: embed inline / move to Implementation Guide § Architecture Decisions / spike). Procedure patches AC `<then>`, removes the Open Question item, and updates dependent DoD items. See template-upgrade-procedures.md P9. |
| `dependency/undeclared_dependency` | interactive | structural | Story references `{dep_id}` in ACs/spec but `{dep_id}` is absent from `depends_on`. Covers both in-scope-pairs detection (Sub-Phase 3b Pass 1) and archived-deps detection (Pass 2). Procedure patches `depends_on` array + adds Dependencies-section entry. Reuses pattern from P7 (`template/informal_dependency_detected`). See template-upgrade-procedures.md P10. |

---

## Automated Fix Safety Rules

An automated fix is ONLY classified as "automated" when ALL three conditions hold:

1. **Deterministic:** Old value and new value are exactly derivable from the finding's `Evidence` and `Remediation` fields — no judgment needed
2. **Single-file scope:** Only one file is affected (or a batch of identical single-file edits to non-context files)
3. **Not a context file:** Target file is NOT one of the 6 constitutional context files in `devforgeai/specs/context/` (context files are LOCKED — interactive path required)

IF any condition fails → classify as "interactive" instead.

---

## Automated Fix Procedures

### fix_broken_file_reference

**Applies to:** `quality/broken_file_reference`

**Extraction logic:**
```
old_string = finding.Evidence → extract the incorrect path/filename
new_string = finding.Remediation → extract the correct path/filename

IF remediation contains "change X → Y" or "X should be Y":
    Parse old_string and new_string from arrow notation
ELIF evidence contains backtick-quoted strings:
    old_string = first backtick string, new_string = second backtick string
```

**Execution:**
```
Edit(
    file_path = resolve_story_path(finding.Affected),
    old_string = old_string,
    new_string = new_string
)
```

### fix_missing_frontmatter_field

**Applies to:** `provenance/missing_brainstorm_frontmatter`, `provenance/missing_frontmatter`

**Extraction logic:**
```
field_name = extract from finding.Remediation (e.g., "brainstorm")
field_value = extract from finding.Remediation (e.g., "BRAINSTORM-010")
```

**Execution:**
```
content = Read(file_path = target_file)

Find the YAML frontmatter closing delimiter "---" (the second occurrence).
Insert the new field BEFORE the closing "---".

Edit(
    file_path = target_file,
    old_string = last_field_line + "\n---",
    new_string = last_field_line + "\n" + field_name + ": " + field_value + "\n---"
)
```

**Safety:** Only adds a field — does not modify existing fields.

### fix_stale_status_label

**Applies to:** `quality/stale_status_label`

**Extraction logic:**
```
old_status = finding.Evidence → current status value
new_status = finding.Remediation → correct status value
```

**Execution:**
```
Edit(
    file_path = target_file,
    old_string = "status: " + old_status,
    new_string = "status: " + new_status
)
```

---

## Interactive Fix Procedures

### fix_invalid_path

**Applies to:** `context/invalid_path`

**Risk:** Structural — a legitimate new location may require amending the
source-tree governance ruleset (a constitutional change, LOCKED — requires an ADR).

**Resolution options to present:**

```
AskUserQuestion:
    Question: "Path '{path}' is not valid per the source-tree/ artifact. How to resolve?"
    Header: "Path Fix"
    Options:
        - label: "Redirect outputs to a documented directory (Recommended)"
          description: "Change all story output paths to an existing valid directory"
        - label: "Amend source-tree governance + regenerate"
          description: "The location is a legitimate new framework directory — amend the governance ruleset (constitutional change, requires ADR) and regenerate the source-tree/ artifact"
        - label: "Defer"
          description: "Mark as AUDIT-DEFERRED for later resolution"
```

**IF "Redirect outputs":**
```
AskUserQuestion: "Which existing directory should outputs go to?"
    Options: [valid directories from `devforgeai-validate query-source-tree --governance`]

FOR each affected story:
    Edit(file_path=story_file, old_string=old_path, new_string=new_path)
```

**IF "Amend source-tree governance + regenerate":**
```
HALT — this is a constitutional change. Per ADR-071 / ADR-072 the source-tree/
artifact is GENERATED, never hand-edited. Amending it requires:
  1. An ADR authorising the new governance rule.
  2. Editing the canonical governance source data (governance-source.json,
     carried as devforgeai_cli package data).
  3. Regenerating: env DEVFORGEAI_ALLOW_CONTEXT_EDIT=1 devforgeai-validate generate-source-tree
Route this to the architect workflow — do NOT hand-edit the source-tree/ folder.
```

### fix_implicit_adr_need

**Applies to:** `adr/implicit_adr_need`

**Risk:** Requires reading an ADR and making a judgment call.

**Procedure:**
```
IF finding.Evidence references an ADR ID (e.g., ADR-017):
    adr_content = Read(file_path="devforgeai/specs/adrs/ADR-{NNN}-*.md")

    AskUserQuestion:
        Question: "Does ADR-{NNN} cover this case? [Summary of ADR shown above]"
        Header: "ADR Review"
        Options:
            - label: "Yes — cite ADR-{NNN}"
              description: "Update the note to reference this ADR explicitly"
            - label: "No — create new ADR"
              description: "Defer fix, run /create-story to create ADR"
            - label: "Defer"
              description: "Mark as AUDIT-DEFERRED"

    IF "Yes":
        Edit the story note to reference the ADR explicitly
    IF "No":
        Display: "Run: /create-story 'ADR for {description}'"
        Mark finding as deferred pending ADR creation
```

### fix_broken_brainstorm_ref

**Applies to:** `provenance/broken_brainstorm_ref`

**Procedure:**
```
brainstorm_id = extract from finding.Evidence
brainstorm_path = Glob(pattern="devforgeai/specs/brainstorms/BRAINSTORM-{NNN}*.md")

IF brainstorm file exists:
    Edit target file to reference correct brainstorm path
ELSE:
    AskUserQuestion: "Brainstorm file not found. Create or skip?"
    IF create: Display "Run: /brainstorm to create the brainstorm document"
    IF skip: Mark as deferred
```

### fix_refactor_preservation_ac

**Applies to:** `quality/refactor_missing_preservation_ac`

**Risk:** Structural — generates new acceptance criteria from source file analysis.

**Procedure:**
```
1. Read story's provenance section → extract epic feature reference
2. Read epic feature description → extract target file paths
3. Read each target file → inventory:
   - Display statement count (Grep pattern: "Display:")
   - AskUserQuestion call count (Grep pattern: "AskUserQuestion")
   - Error handling block count (Grep pattern: "^### Error")
   - Governance section count and names (Architecture, Hook Integration, etc.)
   - Help text section count (Grep pattern: "^## |^### ")
4. Generate preservation ACs using templates from acceptance-criteria-patterns.md
   "Refactor Story Patterns" section (Templates 1-5)
5. Present generated ACs to user via AskUserQuestion:
   Question: "Add these content-preservation ACs to {story_id}?"
   Header: "Refactor ACs"
   Options:
     - "Add all" / Description: "Insert all generated preservation ACs"
     - "Review individually" / Description: "Approve each AC separately"
     - "Skip" / Description: "Do not add preservation ACs"
6. If approved: Insert ACs after last existing AC in story file
7. Update AC Verification Checklist with new checklist items
8. Update DoD with golden output capture items (Template 6)
```

**User decision required:** Approve/modify generated ACs before insertion.

### fix_nfr_enforcement_ac

**Applies to:** `quality/refactor_nfr_without_ac`

**Risk:** Structural — generates backward-compatibility enforcement AC.

**Procedure:**
```
1. Read NFR section → extract NFR-002 backward compatibility requirement
2. Read story's target files → extract invocation modes from Quick Reference sections
3. Generate backward-compatible output AC using Template 2 (AC_BACKWARD_COMPAT)
   from acceptance-criteria-patterns.md "Refactor Story Patterns" section
4. Present to user via AskUserQuestion:
   Question: "Add this backward-compatibility AC to {story_id}?"
   Header: "NFR AC"
   Options:
     - "Add AC" / Description: "Insert backward-compatibility enforcement AC"
     - "Modify first" / Description: "Edit the generated AC before inserting"
     - "Skip" / Description: "Do not add enforcement AC"
5. If approved: Insert AC, update checklist and DoD
```

**User decision required:** Approve/modify generated AC.

### fix_askuser_placement_ac

**Applies to:** `quality/refactor_askuser_placement_missing`

**Risk:** Structural — generates lean orchestration compliance ACs.

**Procedure:**
```
1. Read target files → count AskUserQuestion calls per file
2. Generate AskUserQuestion Placement AC using Template 3 (AC_ASKUSER_PLACEMENT)
   from acceptance-criteria-patterns.md "Refactor Story Patterns" section
3. Generate Interactive Prompt Completeness AC using Template 5 (AC_PROMPT_COMPLETE)
4. Present to user via AskUserQuestion:
   Question: "Add these AskUserQuestion placement ACs to {story_id}?"
   Header: "AskUser ACs"
   Options:
     - "Add both" / Description: "Insert placement + completeness ACs"
     - "Review individually" / Description: "Approve each AC separately"
     - "Skip" / Description: "Do not add AskUserQuestion ACs"
5. If approved: Insert ACs, update checklist
```

**User decision required:** Approve/modify generated ACs.

---

## Coherence Fix Procedures

Fix procedures for findings from Sub-Phase 3e (Plan-Story Coherence Validation).

### fix_api_contract_error

**Applies to:** `coherence/api_contract_error`
**Classification:** automated

**Extraction logic:**
```
old_field = finding.Evidence → extract quoted incorrect field name (e.g., 'subagent_type')
new_field = finding.Evidence → extract quoted correct API field name (e.g., 'agent_type')
# Evidence format: "Story references 'X' but API uses 'Y'"
```

**Execution:**
```
Edit(
    file_path = resolve_story_path(finding.Affected[0]),
    old_string = old_field,
    new_string = new_field,
    replace_all = true  # Fix ALL occurrences in story
)
```

**Example:**
```
Finding: "Story references 'subagent_type' but SubagentStop API uses 'agent_type'"
→ Edit(file_path="...STORY-526...story.md", old_string="subagent_type", new_string="agent_type", replace_all=true)
```

### fix_naming_inconsistency

**Applies to:** `coherence/naming_inconsistency`
**Classification:** automated

**Extraction logic:**
```
old_name = finding.Evidence → extract current script/file name from "Generic" list
new_name = finding.Remediation → extract plan's canonical name

# If plan file available, derive canonical names from plan
# If not, use the descriptive-naming variants as canonical
```

**Execution:**
```
FOR each affected story:
  Edit(
      file_path = resolve_story_path(story_id),
      old_string = old_name,
      new_string = new_name,
      replace_all = true
  )
```

### fix_schema_mismatch (interactive)

**Applies to:** `coherence/schema_mismatch`
**Classification:** interactive

**Risk:** Structural — requires choosing which story's schema is canonical.

**Procedure:**
```
1. Display: "Schema mismatch detected between {story_A} and {story_B} for '{target_file}'"
2. Display both field lists side-by-side
3. IF plan_file exists:
     Display plan's canonical schema
     AskUserQuestion:
       Question: "Which schema to use for '{target_file}'?"
       Header: "Schema Fix"
       Options:
         - "Use plan schema (Recommended)" / Description: "Align both stories to plan"
         - "Use {story_A}'s schema" / Description: "Update {story_B} to match"
         - "Use {story_B}'s schema" / Description: "Update {story_A} to match"
         - "Skip" / Description: "Defer to manual review"
4. Apply chosen schema:
   - For field name changes: Edit(replace_all=true) on the non-canonical story
   - For type changes: Edit specific type annotations
5. Verify: Re-run validate_cross_story_schema on affected stories
```

### fix_plan_story_drift (interactive)

**Applies to:** `coherence/plan_story_drift`
**Classification:** interactive

**Risk:** Structural — plan may be outdated, or story may have intentional divergence.

**Procedure:**
```
1. Display: "Specification drift detected"
   Show: "Plan: '{plan_value}'"
   Show: "Story: '{story_value}'"
2. AskUserQuestion:
   Question: "How to resolve drift for '{spec_category}'?"
   Header: "Drift Fix"
   Options:
     - "Update story to match plan (Recommended)" / Description: "Plan is authoritative"
     - "Update plan to match story" / Description: "Story has intentional change"
     - "Skip" / Description: "Defer"
3. IF update story:
     Edit(file_path=story_path, old_string=story_value, new_string=plan_value, replace_all=true)
   ELIF update plan:
     Edit(file_path=plan_path, old_string=plan_value, new_string=story_value, replace_all=true)
```

### fix_format_inconsistency (interactive)

**Applies to:** `coherence/format_inconsistency`
**Classification:** interactive

**Risk:** Structural — format change ripples through ACs, tech spec, and DoD.

**Procedure:**
```
1. Display: "Format inconsistency for '{format_type}'"
   List all stories using each variant with examples
2. IF plan_file exists: Display plan's format as recommendation
3. AskUserQuestion:
   Question: "Which format to standardize on for '{format_type}'?"
   Header: "Format Fix"
   Options:
     - "Use '{variant_A}' (from plan)" / Description: "Recommended by plan"
     - "Use '{variant_B}'" / Description: "Used by {story_ids}"
     - "Skip" / Description: "Defer"
4. FOR each story using the non-canonical format:
     Edit(file_path=story_path, old_string=old_format_example, new_string=new_format_example, replace_all=true)
     # Note: replace_all needed because format appears in ACs, tech spec, and DoD
5. Verify: Re-run validate_format_consistency
```

### fix_instruction_contradiction (interactive)

**Applies to:** `coherence/instruction_contradiction`
**Classification:** interactive

**Procedure:**
```
1. Display: "Contradictory instruction for '{subject}'"
   Show: "{story_A} says '{placement_A}'"
   Show: "{story_B} says '{placement_B}'"
   IF plan_file: Show: "Plan says '{plan_placement}'"
2. AskUserQuestion:
   Question: "Which placement is correct for '{subject}'?"
   Header: "Contradiction"
   Options:
     - "Use plan placement (Recommended)" / Description: "'{plan_placement}'"
     - "Use {story_A}'s placement" / Description: "'{placement_A}'"
     - "Use {story_B}'s placement" / Description: "'{placement_B}'"
     - "Skip" / Description: "Defer"
3. Update the non-canonical story's Design Decisions section
```

### fix_dependency_assumption_mismatch (interactive)

**Applies to:** `coherence/dependency_assumption_mismatch`
**Classification:** interactive

**Risk:** Structural — must decide which story to change (dependent or dependency).

**Procedure:**
```
1. Display: "{story_B} assumes {dep_A} outputs '{assumed_value}'"
   Display: "But {dep_A} actually specifies '{actual_value}'"
2. AskUserQuestion:
   Question: "How to resolve assumption mismatch?"
   Header: "Dep Fix"
   Options:
     - "Update {story_B} to match {dep_A} (Recommended)" / Description: "Align consumer to producer"
     - "Update {dep_A} to match {story_B}" / Description: "Align producer to consumer"
     - "Skip" / Description: "Defer"
3. Apply chosen alignment with Edit(replace_all=true)
4. Verify: Re-run validate_dependency_assumptions
```

---

## Template Upgrade Fix Procedures

See `template-upgrade-procedures.md` for the authoritative SSOT of procedures P1-P8 covering all `template/*` finding types. Each procedure documents:

- **Trigger** — which finding type and `_section_status` / `_field_derivability` / `_dependency_direction` discriminator invokes it
- **Classification** — automated, interactive, or advisory
- **Inputs** — required fields from the finding object plus any reads from `template-upgrade-snippets.md`
- **Execution** — exact `Edit()` and `AskUserQuestion` patterns
- **Verification** — Grep checks consumed by Phase 04

Procedure index:

| Finding type | Procedure | Classification |
|---|---|---|
| `template/missing_section` (Required) | P1 | automated |
| `template/missing_section` (Conditional) | P2 | automated |
| `template/missing_frontmatter_field` (derivable) | P3 | automated |
| `template/missing_frontmatter_field` (ambiguous) | P4 | interactive |
| `template/legacy_workflow_status` | P5 | automated |
| `template/legacy_format` | P6 | interactive (per-AC) |
| `template/informal_dependency_detected` | P7 | interactive |
| `template/version_drift` | P8 | automated (gated) |
| `template/cross_story_drift` | none | advisory |

**Critical ordering:** P8 (version-bump) MUST run LAST for each story. The detection reference emits the version_drift finding with `finding_id` prefix `TPL-ZZZ-` to ensure alphabetical sort places it last in the audit table; Phase 03 Step 1 processes findings in audit order; therefore P8 runs after all sibling fixes for the same story. P8 gates on sibling status — any sibling with `status: failed` causes P8 itself to defer.

---

## Batch Fix Strategy

When a single finding affects many files (>3 files, e.g., F-001 affecting 12 stories):

1. **Confirm resolution once:**
   ```
   AskUserQuestion:
       Question: "Finding {finding_id} affects {N} files. Apply same resolution to all?"
       Header: "Batch Fix"
       Options:
           - label: "Yes — apply uniformly"
             description: "Same change across all {N} files"
           - label: "No — review each file"
             description: "Walk through files individually"
   ```

2. **Apply sequentially:** FOR each affected file, apply the same edit

3. **Verify each:** Confirm each edit succeeded (fail-fast on first error)

4. **Report batch summary:** Display single summary line, not per-file noise:
   ```
   "✓ Batch fixed {finding_id}: {N}/{N} files updated"
   ```

---

## Multishot Examples

Three complete finding → fix → verify cycles demonstrating the full workflow:

<examples>

<example name="automated-broken-file-reference">
**Finding (from audit):**

| Field | Value |
|-------|-------|
| **Finding ID** | F-002 |
| **Severity** | MEDIUM |
| **Type** | quality/broken_file_reference |
| **Affected** | STORY-414 |
| **Evidence** | `use=xml-tags.md` — actual file is `use-xml-tags.md` (typo: `=` should be `-`) |
| **Remediation** | Edit STORY-414: change `use=xml-tags.md` → `use-xml-tags.md` |
| **Verification** | `Glob(pattern=".claude/skills/.../use-xml-tags.md")` |

**Classification:** automated (deterministic, single file, not context file)

**Fix:**
```
Edit(
    file_path="devforgeai/specs/Stories/STORY-414-scoring-rubric-extraction.story.md",
    old_string="use=xml-tags.md",
    new_string="use-xml-tags.md"
)
```

**Verify:**
```
Glob(pattern=".claude/skills/spec-driven-cc-guide/references/prompt-engineering/use-xml-tags.md")
→ Match found → PASS ✓
```
</example>

<example name="automated-missing-frontmatter">
**Finding (from audit):**

| Field | Value |
|-------|-------|
| **Finding ID** | F-003 |
| **Severity** | MEDIUM |
| **Type** | provenance/missing_brainstorm_frontmatter |
| **Affected** | EPIC-066 |
| **Evidence** | EPIC-066 frontmatter has no `brainstorm:` field |
| **Remediation** | Add `brainstorm: BRAINSTORM-010` to EPIC-066 YAML frontmatter |
| **Verification** | `Grep(pattern="brainstorm:", path="EPIC-066...")` |

**Classification:** automated (deterministic, single file, not context file)

**Fix:**
```
Read EPIC-066 → locate last field before closing "---"
Edit(
    file_path="devforgeai/specs/Epics/EPIC-066-dev-command-anthropic-conformance-analysis.epic.md",
    old_string="team: AI Architecture\n---",
    new_string="team: AI Architecture\nbrainstorm: BRAINSTORM-010\n---"
)
```

**Verify:**
```
Grep(pattern="brainstorm:", path="devforgeai/specs/Epics/EPIC-066-dev-command-anthropic-conformance-analysis.epic.md")
→ Match found → PASS ✓
```
</example>

<example name="interactive-context-file-path">
**Finding (from audit):**

| Field | Value |
|-------|-------|
| **Finding ID** | F-001 |
| **Severity** | MEDIUM |
| **Type** | context/invalid_path |
| **Affected** | STORY-413 through STORY-424 (12 stories) |
| **Evidence** | `devforgeai/specs/requirements/dev-analysis/` is not valid per `query-source-tree --validate-path` |
| **Remediation** | Option A: redirect outputs to the documented `analysis/` directory. Option B: amend the source-tree governance ruleset (requires ADR) |

**Classification:** interactive (multi-file batch OR constitutional change)

**Fix:**
```
AskUserQuestion: "How to resolve the invalid path?"
→ User selects: "Redirect outputs to a documented directory"

FOR each affected story (STORY-413 … STORY-424):
    Edit(
        file_path=story_file,
        old_string="devforgeai/specs/requirements/dev-analysis/",
        new_string="devforgeai/specs/analysis/"
    )
```

**Verify:**
```
devforgeai-validate query-source-tree --validate-path devforgeai/specs/analysis/
→ exit 0 (valid) → PASS ✓
```
</example>

</examples>
