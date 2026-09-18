# Phase 06: Documentation & Formatter

**Purpose:** Create UI specification summary, update story file (if story mode), and invoke ui-spec-formatter subagent.

**Pre-Flight:** Verify Phase 05 completed.

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-design/references/documentation-update.md")
Read(file_path=".claude/skills/spec-driven-design/references/design-source-of-truth-population.md")
Read(file_path=".claude/skills/spec-driven-design/references/design-source-of-truth-schema.md")
Read(file_path=".claude/skills/spec-driven-design/references/component-examples.md")
Read(file_path=".claude/skills/spec-driven-design/references/ui-spec-formatter-integration.md")
Read(file_path=".claude/skills/spec-driven-design/references/ui-result-formatting-guide.md")
```

IF any Read fails: HALT -- "Phase 06 reference files not loaded."

---

## Step 6.1: Load Documentation Update Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-design/references/documentation-update.md")
```

**VERIFY:**
- File content loaded into context
- Content contains documentation procedures

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=06 --step=6.1 --project-root=. 2>&1")
```

---

## Step 6.2: Generate UI Spec Summary

**EXECUTE:**
Create a UI-SPEC-SUMMARY.md file with YAML frontmatter (machine-readable) and markdown body:

**YAML Frontmatter (required for cross-skill consumption):**
```yaml
---
schema_version: "1.0"
mode: "${story|standalone|extract}"
story_id: "${STORY_ID_OR_NULL}"
epic_id: "${EPIC_ID_OR_NULL}"
design_source_of_truth: "devforgeai/specs/ui/design.md"
components_generated:
  - name: "${ComponentName}"
    file: "${file_path}"
    type: "${component_type}"
framework: "${FRAMEWORK}"
styling: "${STYLING}"
theme: "${THEME}"
aesthetic_vibe: "${AESTHETIC_VIBE}"
design_tokens_file: "devforgeai/specs/context/design-system.md"
accessibility_level: "WCAG 2.1 AA"
validation_status: "${PASSED|PARTIAL|FAILED}"
generated_date: "${ISO_DATE}"
---
```

**Markdown Body:**
- Components generated (file path, framework, type)
- Technology stack selected
- Dependencies required
- Integration instructions
- Next steps for development
- **Cross-reference to design.md:** "Full design specification: devforgeai/specs/ui/design.md"

```
Write(file_path="devforgeai/specs/ui/UI-SPEC-SUMMARY.md", content=${SUMMARY_CONTENT})
```

**VERIFY:**
```
Glob(pattern="devforgeai/specs/ui/UI-SPEC-SUMMARY.md")
```
- File exists on disk

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=06 --step=6.2 --project-root=. 2>&1")
```

---

## Step 6.2.5: Generate Design Source of Truth

**EXECUTE:**

1. Load the design source of truth template:
```
Read(file_path=".claude/skills/spec-driven-design/assets/templates/design-source-of-truth-template.md")
```

2. Load the population reference:
```
Read(file_path=".claude/skills/spec-driven-design/references/design-source-of-truth-population.md")
```

3. Load the schema reference:
```
Read(file_path=".claude/skills/spec-driven-design/references/design-source-of-truth-schema.md")
```

4. Populate the template section by section. Each sub-step is mandatory with its own verification.

**Sub-step 6.2.5.1: Populate Metadata**
EXECUTE: Set schema_version="1.1", document_type="ui-design-source-of-truth", project=${PROJECT_NAME}, created/updated=current date, source_skill="spec-driven-design", source_mode="generated"|"extracted"|"hybrid", mode=${MODE}, platform=${PLATFORM}, story_id=${STORY_ID or null}, epic_id=from story frontmatter or null. Use the immutable CLI-owned Phase 03 context binding for platform and design schema; never infer either from framework choice or artifact contents. Extract mode uses the explicit platform recorded in the extracted design metadata and does not create or alter an invocation binding.
VERIFY: All 11 schema-1.1 metadata fields are non-null (except story_id and epic_id which may be null); mode is story, standalone, or extract; platform is web, gui, or tui.

**Sub-step 6.2.5.2: Populate Design Tokens**
EXECUTE: Populate colors (min 8 required tokens), spacing (8-point grid), typography (font family + min 4 scale entries), borders, shadows, motion, responsive breakpoints, z-index. Use design-system-rules.md + Phase 03 selections. Map framework-specific values to concrete CSS values using population reference.
VERIFY: colors section has ≥8 entries. spacing.unit = "8px". typography has font_family.primary and ≥4 scale entries.

**Sub-step 6.2.5.3: Populate Component Inventory**
EXECUTE:
1. Load the component template (structural enforcement):
```
Read(file_path=".claude/skills/spec-driven-design/assets/templates/component-template.md")
```
2. Load the component examples (quality bar):
```
Read(file_path=".claude/skills/spec-driven-design/references/component-examples.md")
```
3. For EACH component from Phase 05 (or Phase 02a extraction), fill in the component template to create a COMP-NNN entry. Every field must be populated — no blank or placeholder values. Match or exceed the quality bar shown in the examples (~80+ lines per component).
   - name, type, classification per component-anatomy.md
   - visual: using token references per Token Normalization rule
   - content: list every visible element (minimum 2 per component)
   - states: default state + interactive states (hover, focused, disabled as applicable)
   - data: props (MUST include children/className per mandatory prop rules), events, internal_state (smart only)
   - accessibility: role, label, keyboard handlers, screen reader, contrast

VERIFY: ≥1 COMP-NNN entry. Every component has visual + data.props + accessibility sections. Every component rendering children has children in data.props.

**Sub-step 6.2.5.4: Populate Layouts**
EXECUTE: Group components into page regions. Generate ASCII layout diagram with COMP-NNN references. Define responsive behavior per breakpoint.
VERIFY: ≥1 LAYOUT-NNN entry. Each layout has regions, ASCII diagram, responsive section. All COMP-NNN refs in regions exist in component inventory.

**Sub-step 6.2.5.5: Populate Interactions**
EXECUTE: Create FLOW-NNN for every category of callback props (navigation, toggle, selection, CRUD, search, responsive, error). Every on* callback prop across all components MUST be covered by at least one FLOW.
VERIFY: ≥1 FLOW-NNN entry. All callback props covered (completeness check).

**Sub-step 6.2.5.6: Populate Animations**
EXECUTE: Create ANIM-NNN entries from transition/animation code. Include @keyframes definitions.
VERIFY: ≥1 ANIM-NNN entry if animations exist in source code.

**Sub-step 6.2.5.7: Populate Global Accessibility**
EXECUTE: Set wcag_level (minimum "AA"), keyboard nav, screen reader, motion preferences, touch targets.
VERIFY: wcag_level is not null/placeholder.

**Sub-step 6.2.5.8: Populate Data Context**
EXECUTE: Document API endpoints, global state (Redux/Zustand/Context), mock data guidance.
VERIFY: Section is present (even if empty for mockups with no backend).

**Sub-step 6.2.5.9: Initialize Design Review Applicability**
EXECUTE: For generated web story/standalone mode, include `design_review` after `data_context` with status `pending` and the fixed lint, render-manifest, screenshot, and review paths that Phase 07 will replace with validated hashes, counts, round, composite, status, and remaining gaps. For GUI, TUI, and extract mode, omit the entire `design_review` group.
VERIFY: Generated web story/standalone has exactly one non-empty `design_review` group after `data_context`; GUI, TUI, and extract have none.

5. Write the populated design.md:
```
Write(file_path="devforgeai/specs/ui/design.md", content=${POPULATED_DESIGN_DOC})
```

6. Verify the file was created:
```
Glob(pattern="devforgeai/specs/ui/design.md")
```

7. Verify no template placeholders remain:
```
Grep(pattern="\\$\\{", path="devforgeai/specs/ui/design.md", output_mode="count")
```
IF count > 0: Report remaining placeholders, attempt to fill from context, or flag for Phase 07 validation.

**--- Step 6.2.5a: Children Integrity Gate (MANDATORY — runs in ALL modes) ---**

This gate ensures design.md is internally self-consistent before validation.

**EXECUTE:**
```
# Re-read the design.md just written
Read(file_path="devforgeai/specs/ui/design.md")

# Build master inventory of all defined COMP-NNN IDs
master_inventory = set of all component.id values in Section 3

# Check children[] arrays for dangling references
dangling = []
FOR each component in Section 3:
  IF component.children is not empty:
    FOR each child_id in component.children:
      IF child_id NOT IN master_inventory:
        dangling.append({ parent: component.id, child: child_id })

# Check parent references
FOR each component in Section 3:
  IF component.parent != "root" AND component.parent NOT IN master_inventory:
    dangling.append({ component: component.id, invalid_parent: component.parent })

IF len(dangling) > 0:
  Display: "Children Integrity Gate: ${len(dangling)} dangling references found"
  FOR each ref in dangling:
    Display: "  - ${ref}"

  # AUTO-FIX: Create stub component definitions for missing children
  FOR each dangling child ref:
    next_id = max(existing COMP-NNN numbers) + 1
    Create stub component:
      id: "COMP-${next_id}"
      name: infer from parent context or use child_id as hint
      type: "composite"
      classification: "dumb"
      description: "Auto-generated stub — verify and complete manually"
      parent: the parent component that referenced it
      visual: { dimensions: { width: "auto", height: "auto" } }
      data: { props: [{ name: "children", type: "ReactNode", required: false }] }
      accessibility: { role: "generic" }

    # Update the children[] array to use the new COMP-NNN ID
    Update parent.children: replace old dangling ID with new COMP-NNN

  # Fix dangling parent references
  FOR each dangling parent ref:
    Set component.parent = "root"

  # RE-WRITE design.md with all fixes applied
  Write(file_path="devforgeai/specs/ui/design.md", content=${FIXED_DESIGN_DOC})
  Display: "Children Integrity Gate: Auto-fixed ${len(dangling)} references. Re-wrote design.md."

ELSE:
  Display: "Children Integrity Gate: PASSED (0 dangling references)"
```

**VERIFY:**
```
# Re-read the fixed design.md
Read(file_path="devforgeai/specs/ui/design.md")

# Re-verify: extract ALL COMP-NNN IDs and ALL references
# Assert: ZERO dangling references remain after fix
re_check = scan all children[] and parent values
IF any dangling refs remain:
  HALT: "Children Integrity Gate FAILED after auto-fix. Manual intervention required."
```

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=06 --step=6.2.5a --project-root=. 2>&1")
```

**--- End Step 6.2.5a ---**

**FINAL VERIFY (Step 6.2.5 overall):**
- File `devforgeai/specs/ui/design.md` exists on disk
- File contains `schema_version: "1.1"`
- File contains `document_type: "ui-design-source-of-truth"`
- All required token sections populated (colors, spacing, typography minimum)
- At least 1 COMP-NNN entry in components section
- Zero `${...}` placeholders remaining
- **Zero dangling children/parent references (Step 6.2.5a passed)**
- **Validation script passes (hard enforcement):**
```
Bash(command="python3 src/claude/skills/spec-driven-design/scripts/validate_design_md.py devforgeai/specs/ui/design.md --expected-components=${COMPONENT_COUNT} --mode=${MODE} 2>&1")
```
IF exit code != 0: Read the JSON output, fix identified failures, re-run until exit code = 0.

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=06 --step=6.2.5 --project-root=. 2>&1")
```

---

## Step 6.3: Update Story File (Story Mode Only)

**EXECUTE:**
```
IF MODE == "story":
    Read the story file
    Edit the story's Technical Specification section to add UI component references:
    - Generated component file path
    - Framework and styling used
    - Integration notes
ELSE:
    SKIP — standalone mode has no story file to update
```

**VERIFY:**
- Story mode: Story file updated with UI references
- Standalone mode: Step marked as skipped (valid)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=06 --step=6.3 --project-root=. 2>&1")
```

---

## Step 6.4: Load Formatter Integration Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-design/references/ui-spec-formatter-integration.md")
```

Also load formatter guardrails:
```
Read(file_path=".claude/skills/spec-driven-design/references/ui-result-formatting-guide.md")
```

**VERIFY:**
- Both files loaded into context
- Integration reference contains invocation protocol

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=06 --step=6.4 --project-root=. 2>&1")
```

---

## Step 6.5: Invoke ui-spec-formatter Subagent

**EXECUTE:**
```
Agent(subagent_type="ui-spec-formatter", prompt="""
Validate and format the UI specification for display.

Input:
- UI Spec file: devforgeai/specs/ui/UI-SPEC-SUMMARY.md
- Generated component: ${OUTPUT_PATH}
- Mode: ${MODE}
- Framework: ${FRAMEWORK}
- UI Type: ${UI_TYPE}
- Styling: ${STYLING}
- Theme: ${THEME}
- Components: ${COMPONENTS}

Validate against context files (tech-stack.md, source-tree/, dependencies.md, coding-standards.md, anti-patterns.md).
Return a `subagent-result-v1` structured JSON object with: status (SUCCESS/PARTIAL/FAILED), display template, component details, validation results, next steps, and `coverage_attestation` in the normal response. The attestation must include `context_pack_consumed: true` and `context_miss: []`. This is OUT-attestation-only; do not create a handoff path.
""")
```

Capture subagent output as FORMATTER_RESULT.

**VERIFY:**
- FORMATTER_RESULT is non-empty
- FORMATTER_RESULT contains a status field (SUCCESS, PARTIAL, or FAILED)
- If FAILED: Record failure reason for Phase 07 handling

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=06 --step=6.5 --project-root=. 2>&1")
```

---

## Phase 06 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate validate-design-phase ${IDENTIFIER} ${WORKFLOW_FLAG} --mode=${MODE} --phase=06 --project-root=. 2>&1")
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=06 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0; any non-zero result blocks completion

**NEXT:** Proceed to Phase 07 (Specification Validation).

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.
