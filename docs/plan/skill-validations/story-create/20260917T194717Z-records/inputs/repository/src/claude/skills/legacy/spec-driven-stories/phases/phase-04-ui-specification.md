# Phase 04: UI Specification

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from=03 --to=04 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 03 incomplete. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Document UI components, create ASCII mockups, specify accessibility requirements, define interaction flows (if applicable to this story)
- **REQUIRED SUBAGENTS:** none
- **REQUIRED ARTIFACTS:** UI specification section (or explicit "N/A - no UI" determination)
- **STEP COUNT:** 3
- **REFERENCE FILES:**
  - `references/ui-specification-creation.md`
  - `references/ui-specification-guide.md`

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-stories/references/ui-specification-creation.md")
Read(file_path=".claude/skills/spec-driven-stories/references/ui-specification-guide.md")
```

IF any Read fails: HALT -- "Phase 04 reference files not loaded."

---

## Mandatory Steps (4)

### Step 4.0.5: Design Source of Truth Detection

**EXECUTE:**
```
# Check if a Design Source of Truth (design.md) exists
design_doc = Glob(pattern="devforgeai/specs/ui/design.md")

IF design_doc found:
  Read(file_path="devforgeai/specs/ui/design.md")

  # Extract component inventory from YAML frontmatter
  # Parse components section: extract all COMP-NNN entries
  # Parse interactions section: extract all FLOW-NNN entries
  # Parse layouts section: extract all LAYOUT-NNN entries
  # Parse tokens section: extract design intent and aesthetic vibe

  design_available = true

  # Match story's feature to relevant components from design.md
  # Use story description and AC text to identify which COMP-IDs are relevant
  relevant_components = []
  FOR each component in design.md.components:
    IF component.description matches any keyword from $REQUIREMENTS_OUTPUT:
      relevant_components.append(component)

  # Also check if any AC references UI elements
  FOR each AC in $REQUIREMENTS_OUTPUT:
    FOR each component in design.md.components:
      IF component.name mentioned in AC.given or AC.when or AC.then:
        IF component not in relevant_components:
          relevant_components.append(component)

  Display: "Design Source of Truth found: devforgeai/specs/ui/design.md"
  Display: "  Total components in design: {total_count}"
  Display: "  Components relevant to this story: {len(relevant_components)}"

  # Check for visual capture screenshots
  screenshots_exist = Glob(pattern="devforgeai/specs/ui/visual-capture/desktop.png")
  IF screenshots_exist:
    Display: "  Visual capture screenshots available (desktop, tablet, mobile)"

ELSE:
  design_available = false
  screenshots_exist = false
  Display: "No design.md found. Will use standard UI detection and ASCII mockup generation."
```

**VERIFY:** `design_available` is boolean. If true, `relevant_components` list is populated.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=04 --step=4.0.5 --project-root=.
```
Update checkpoint: `phases["04"].steps_completed.append("4.0.5")`

---

### Step 4.1: Detect UI Needs

**EXECUTE:**
```
# Sprint 4.2 — PRIMARY path: CLI validator replaces inline keyword-scan loop.
# Contract: src/claude/scripts/devforgeai_cli/validators/indicators.py (Sprint 4.1).
# Exit codes: 0 = scan completed, 2 = IO, 127 = CLI absent.
# Concatenate requirements and tech spec to a scratch file the CLI can read.
scratch_path = "tmp/${SESSION_ID}/phase-outputs/phase-04-ui-scan.txt"
Write(file_path=scratch_path, content=$REQUIREMENTS_OUTPUT + "\n\n" + $TECH_SPEC)

cli_result = Bash(f"devforgeai-validate detect-indicators --story-file={scratch_path} --format=json")

IF cli_result.exit_code == 0:
  parsed = json_parse(cli_result.stdout)
  detect_indicators_hint = parsed            # retain raw scanner output as an auditable HINT (never the routing authority)
  raw_ui_detected = parsed.ui_detected
  Display: f"UI keyword hint (raw): {raw_ui_detected} (indicators: {parsed.ui_indicators_found}, Sprint 4.2)"
ELSE IF cli_result.exit_code == 127:
  # CLI absent — inline fallback (deprecated).
  ui_indicators = ["form", "page", "button", "component", "screen", "view", "modal",
                   "dialog", "input", "display", "dashboard", "table", "list", "panel",
                   "UI", "frontend", "user interface"]
  raw_ui_detected = false

  FOR each indicator in ui_indicators:
    IF indicator found in $REQUIREMENTS_OUTPUT or $TECH_SPEC (case-insensitive):
      raw_ui_detected = true
      break

  detect_indicators_hint = {"ui_detected": raw_ui_detected, "source": "inline-fallback"}
ELSE:
  HALT: f"detect-indicators CLI unexpected exit {cli_result.exit_code}: {cli_result.stdout}"

# === CROSS-CHECK (Issue-719): route UI generation on tech-spec component TYPES + design.md, not the raw keyword hint. ===
# Unlike Phase 03, the FULL $TECH_SPEC already exists here (built in Phase 03 Step 3.4), so its component types are the
# authoritative routing source. The keyword scanner false-positives on prose ("form"/"component"/"list" in non-UI text)
# for pure-backend stories (incident SEED-002 / COMP-001). COMPOUND GUARD: there is NO `type: UI` in the 7-type enum, so
# "all components are backend types" is an inference from ABSENCE — it must NOT override a POSITIVE design.md signal.
# design.md is the only positive UI evidence available; a relevant-component match there forces UI required.
backend_only_types = {"Service", "Worker", "Configuration", "Logging", "Repository", "DataModel"}   # the 6 non-API, non-UI types
tech_spec_types = extract component `type` values from $TECH_SPEC
design_match_detected = (design_available == true) AND (len(relevant_components) > 0)   # positive UI signal from the Design Source of Truth

# Reconcile: design.md match forces UI; else suppress when every tech-spec component is a backend-only type.
# `all_backend` is the named suppression condition (the non-empty guard avoids the all([]) == true vacuous-truth trap).
all_backend = (tech_spec_types is non-empty) AND all(t in backend_only_types for t in tech_spec_types)
ui_detected = design_match_detected OR (raw_ui_detected AND NOT all_backend)

IF raw_ui_detected AND NOT ui_detected:
  ui_override_reason = "raw detect-indicators ui_detected=true but the tech-spec has zero UI-surface components (all types are backend-only) and no design.md component match — UI marked N/A"
  Display: f"CROSS-CHECK: {ui_override_reason}"
  Write(file_path="tmp/${SESSION_ID}/phase-outputs/phase-04-cross-check.json", content={"detect_indicators_hint": detect_indicators_hint, "ui_override_reason": ui_override_reason, "tech_spec_component_types": tech_spec_types, "design_match_detected": design_match_detected})
ELSE:
  ui_override_reason = null
  Write(file_path="tmp/${SESSION_ID}/phase-outputs/phase-04-cross-check.json", content={"detect_indicators_hint": detect_indicators_hint, "ui_override_reason": null, "tech_spec_component_types": tech_spec_types, "design_match_detected": design_match_detected})

IF NOT ui_detected:
  Display: "No UI components detected. Marking UI specification as N/A."
  $UI_SPEC = "N/A - This story does not require UI components."
  # Record Step 4.2 as the N/A determination before proceeding to Step 4.3.
  devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=04 --step=4.2 --project-root=.
  Update checkpoint: phases["04"].steps_completed.append("4.2")
  Proceed to Step 4.3.

Display: "UI components detected. Generating UI specification..."
```

**VERIFY:** `ui_detected` is boolean. If false, `$UI_SPEC` is set to N/A string.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=04 --step=4.1 --project-root=.
```
Update checkpoint: `phases["04"].steps_completed.append("4.1")`

---

### Step 4.2: Generate UI Specification

**EXECUTE:**
```
IF ui_detected == true:

  IF design_available == true AND len(relevant_components) > 0:
    # === DESIGN.MD PATH: Populate from Source of Truth ===
    # Full fidelity — use component specs, interactions, and accessibility from design.md

    $UI_SPEC = generate from design.md:
      1. Component list — from relevant_components (COMP-ID, name, type, classification)
         Include: description, props, state, events from design.md data contract
      2. Layout reference — from design.md layouts section
         Include: ASCII layout diagram and responsive behavior
      3. Component interfaces — from design.md data.props specification
         Include: exact prop names, types, required flags, defaults
      4. Interaction flows — from design.md interactions section
         Filter: only flows involving relevant_components
         Include: step-by-step with state changes and visual feedback
      5. Accessibility requirements — from design.md accessibility specs
         Include: roles, labels, keyboard handlers, contrast ratios
      6. Design tokens reference — from design.md tokens section
         Include: colors, spacing, typography used by these components
      7. Source of Truth reference:
         "Full specification: devforgeai/specs/ui/design.md"
         "Components: [list of COMP-NNN IDs for this story]"
      8. Visual Reference (if screenshots exist):
         IF screenshots_exist:
           "### Visual Reference
            Target screenshots for this story's UI components:
            - Desktop (1280x800): devforgeai/specs/ui/visual-capture/desktop.png
            - Tablet (768x1024): devforgeai/specs/ui/visual-capture/tablet.png
            - Mobile (375x812): devforgeai/specs/ui/visual-capture/mobile.png
            Implementation MUST match these visual targets."

    Display: "UI specification populated from Design Source of Truth (design.md):"
    Display: "  Components from design.md: {len(relevant_components)}"
    Display: "  Interaction flows: {flow_count}"
    Display: "  Full fidelity: Visual + Behavioral + Accessibility"
    IF screenshots_exist:
      Display: "  Visual references: 3 screenshots included"

  ELSE:
    # === FALLBACK PATH: Generate ASCII mockups from scratch ===
    # Follow ui-specification-creation.md workflow
    $UI_SPEC = generate:
      1. Component list (name, type, purpose)
      2. ASCII layout mockup
      3. Component interfaces (props/state)
      4. Interaction flows (user actions -> system responses)
      5. Accessibility requirements (WCAG AA compliance)
         - Keyboard navigation
         - Screen reader support
         - Color contrast ratios
         - Focus management

    Display: "UI specification generated (ASCII fallback — no design.md available):"
    Display: "  Components: {component_count}"
    Display: "  Mockups: {mockup_count}"
    Display: "  Interaction flows: {flow_count}"
```

**VERIFY:** If `ui_detected`, `$UI_SPEC` contains component list, mockup, and accessibility section.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=04 --step=4.2 --project-root=.
```
Update checkpoint: `phases["04"].steps_completed.append("4.2")`

---

### Step 4.3: Finalize UI Section

**EXECUTE:**
```
Display: "UI Specification: {ui_detected ? 'Generated' : 'N/A'}"
```

**VERIFY:** `$UI_SPEC` is set (either full specification or N/A string).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=04 --step=4.3 --project-root=.
```
Update checkpoint: `phases["04"].steps_completed.append("4.3")`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=04 --checkpoint-passed --project-root=.
```

## Exit Verification Checklist

- [ ] UI needs detection completed (ui_detected is boolean)
- [ ] If UI detected: Component list, mockup, and accessibility section present
- [ ] If no UI: Explicit "N/A" determination recorded
- [ ] $UI_SPEC variable is set (non-null)

IF any unchecked: HALT -- "Phase 04 exit criteria not met"

### Persist Phase 04 Output Cache (Sprint 3.6)

Contract: `contracts/phase-output-schema.json` (`phase04Output`).
Reader: Phase 05 (UI spec embedding).
Write ALWAYS — even when `ui_detected == false` — so Phase 05 has a uniform read path.

```bash
mkdir -p tmp/${SESSION_ID}/phase-outputs
```

```
Write(file_path="tmp/${SESSION_ID}/phase-outputs/phase-04.json",
      content=json_serialize({
        "schema_version": "1.0",
        "phase_id": "04",
        "ui_detected": $ui_detected,
        "ui_spec_content": $UI_SPEC,
        "design_md_used": $design_available,
        "relevant_components": $relevant_components
      }))
```

## Phase Transition Display

```
Display: "Phase 04 complete. UI specification {ui_detected ? 'generated' : 'marked N/A'}."
Display: "Proceeding to Phase 05: Story File Creation..."
```
