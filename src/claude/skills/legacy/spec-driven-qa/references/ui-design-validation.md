# UI Design Source of Truth Validation

**Purpose:** Validate that implemented UI components match the design.md specification during QA.
**Version:** 1.0
**Loaded by:** Phase 2 (Deep Analysis), during spec compliance validation

---

## Detection

During QA Phase 1 or Phase 2 setup:

```
design_doc = Glob(pattern="devforgeai/specs/ui/design.md")

IF design_doc found:
  Read(file_path="devforgeai/specs/ui/design.md")
  ui_validation_enabled = true
  Display: "Design Source of Truth detected. UI validation will be performed."
ELSE:
  ui_validation_enabled = false
  Display: "No design.md found. Skipping UI design validation."
```

---

## Validation Checks (when ui_validation_enabled == true)

### Check 1: Component Name Compliance

```
FOR each COMP-NNN in design.md.components:
  IF COMP-NNN is referenced in the story being validated:
    Search implemented code for component matching COMP-NNN.name

    IF component found:
      Verify: Component name matches design.md exactly (PascalCase)
      Status: PASS
    ELSE:
      Status: WARNING — "Component ${COMP-NNN.name} from design.md not found in implementation"
```

**Severity:** WARNING (component may be in a different story)

### Check 2: Props Interface Compliance

```
FOR each component matching design.md:
  Extract props interface from implemented code

  FOR each prop in design.md.data.props:
    IF prop.name exists in implemented props:
      Verify: Type matches
      Verify: Required flag matches
      Status: PASS
    ELSE:
      IF prop.required == true:
        Status: HIGH — "Required prop '${prop.name}' missing from ${component.name}"
      ELSE:
        Status: LOW — "Optional prop '${prop.name}' not implemented"
```

**Severity:** HIGH for missing required props, LOW for missing optional props

### Check 3: Accessibility Compliance

```
FOR each component matching design.md:
  Extract accessibility attributes from implemented code

  Verify: ARIA role matches design.md.accessibility.role
  Verify: aria-label present if design.md.accessibility.label specified
  Verify: Keyboard handlers present for design.md.accessibility.keyboard.key_handlers
  Verify: tabIndex or focus management if design.md specifies tab_order

  IF any required accessibility attribute missing:
    Status: HIGH — "Missing accessibility: ${missing_attribute} on ${component.name}"
```

**Severity:** HIGH (accessibility is mandatory per WCAG AA)

### Check 4: Design Token Usage

```
# Check that implemented code uses design tokens, not arbitrary values
FOR each implemented UI file:
  Search for hardcoded color values (#hex, rgb(), etc.)
  Search for hardcoded spacing values (margin: 15px, etc.)
  Search for hardcoded font sizes

  IF hardcoded values found that don't match design.md tokens:
    Status: MEDIUM — "Hardcoded value '${value}' found instead of design token"
```

**Severity:** MEDIUM (token drift reduces design consistency)

### Check 5: State Coverage

```
FOR each component matching design.md:
  IF design.md lists states: [default, hover, focused, disabled, loading, error]

  FOR each required state:
    Search implemented code for state handling:
      - hover: className containing "hover:" or onMouseEnter/onMouseLeave
      - focused: className containing "focus:" or onFocus/onBlur
      - disabled: disabled prop handling or aria-disabled
      - loading: isLoading/loading state handling
      - error: error state handling

    IF state not implemented:
      Status: LOW — "State '${state}' from design.md not implemented on ${component.name}"
```

**Severity:** LOW (states can be added iteratively)

---

## Reporting

UI design validation results are included in the QA report under a dedicated section:

```markdown
### UI Design Source of Truth Compliance

**design.md:** devforgeai/specs/ui/design.md
**Status:** ${PASSED|WARNING|FAILED}

| Check | Result | Details |
|-------|--------|---------|
| Component Names | ${PASS/WARN} | ${N} of ${M} components found |
| Props Interfaces | ${PASS/HIGH} | ${N} missing required props |
| Accessibility | ${PASS/HIGH} | ${N} missing attributes |
| Design Tokens | ${PASS/MEDIUM} | ${N} hardcoded values |
| State Coverage | ${PASS/LOW} | ${N} missing states |
```

**Overall Status:**
- PASSED: All checks pass or only LOW severity issues
- WARNING: MEDIUM severity issues present
- FAILED: HIGH severity issues present (missing required props, missing accessibility)

---

## Check 6: Visual Baseline Comparison (when screenshots exist)

```
screenshots = Glob(pattern="devforgeai/specs/ui/visual-capture/desktop.png")

IF screenshots found:
  # Read baseline screenshot (Claude is multimodal — can analyze PNG files)
  Read(file_path="devforgeai/specs/ui/visual-capture/desktop.png")

  # Compare against implemented UI:
  # - Does the layout match the baseline screenshot?
  # - Are brand colors (#00d4aa or whatever tokens.colors.primary is) visible?
  # - Is the component hierarchy consistent with the screenshot?
  # - Are responsive breakpoints handled (check tablet.png, mobile.png)?

  # Report visual fidelity
  visual_fidelity = "HIGH" | "MEDIUM" | "LOW"
  IF visual drift detected:
    Report: "MEDIUM: Visual drift detected between baseline and implementation"
    List specific differences observed
  ELSE:
    Report: "Visual baseline comparison: PASS"

ELSE:
  # No screenshots — skip visual comparison
  # This is not an error — screenshots are only created when --url is used
```

**Severity:** MEDIUM (visual drift doesn't block but should be investigated)

**Reporting:**
```markdown
| Visual Baseline | ${PASS/MEDIUM} | ${fidelity_assessment} |
```

---

## Backward Compatibility

When design.md does not exist:
- All UI design validation checks are SKIPPED
- QA report does not include "UI Design Source of Truth Compliance" section
- No impact on existing QA workflow

When visual-capture/ does not exist:
- Check 6 (Visual Baseline) is SKIPPED
- No impact on existing QA workflow
