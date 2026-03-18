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
Read(file_path="src/claude/skills/spec-driven-stories/references/ui-specification-creation.md")
Read(file_path="src/claude/skills/spec-driven-stories/references/ui-specification-guide.md")
```

IF any Read fails: HALT -- "Phase 04 reference files not loaded."

Do NOT rely on memory of previous reads. Load ALL references fresh.

---

## Mandatory Steps (3)

### Step 4.1: Detect UI Needs

**EXECUTE:**
```
# Analyze requirements and tech spec for UI indicators
ui_indicators = ["form", "page", "button", "component", "screen", "view", "modal",
                 "dialog", "input", "display", "dashboard", "table", "list", "panel",
                 "UI", "frontend", "user interface"]
ui_detected = false

FOR each indicator in ui_indicators:
  IF indicator found in $REQUIREMENTS_OUTPUT or $TECH_SPEC (case-insensitive):
    ui_detected = true
    break

IF NOT ui_detected:
  Display: "No UI components detected. Marking UI specification as N/A."
  $UI_SPEC = "N/A - This story does not require UI components."
  Skip to Step 4.3

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

  Display: "UI specification generated:"
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

## Phase Transition Display

```
Display: "Phase 04 complete. UI specification {ui_detected ? 'generated' : 'marked N/A'}."
Display: "Proceeding to Phase 05: Story File Creation..."
```
