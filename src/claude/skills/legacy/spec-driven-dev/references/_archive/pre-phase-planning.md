# Pre-Phase Planning Integration

**Source:** STORY-FEEDBACK-005
**Purpose:** Execute optional planning steps before phases 02-05 to enable course correction based on prior phase observations.

---

## Config Loading (Phase 01)

After context file loading in Phase 01:

```
Glob(pattern="devforgeai/config/pre-phase-planning.yaml")

IF file exists:
    Read(file_path="devforgeai/config/pre-phase-planning.yaml")
    $PRE_PHASE_CONFIG = parse_yaml(content)
ELSE:
    $PRE_PHASE_CONFIG = {enabled: false}
```

**Story Override:** If story frontmatter contains `pre_phase_planning:`, merge with global config (story overrides global).

---

## Execution Pattern

Before each phase (02, 03, 04, 05):

```
IF $PRE_PHASE_CONFIG.enabled AND $PRE_PHASE_CONFIG.phases[phase_id].enabled:
    Display: "━━━ Pre-Phase {phase_id}: {description} ━━━"
    Read(file_path=pre_phase_file)
    Execute pre-phase workflow
    $PRE_PHASE_OUTPUT = result  # Pass to main phase
    Display: "Pre-Phase {phase_id} complete → {output_file}"
```

---

## Pre-Phase Files

| Phase | File | Output |
|-------|------|--------|
| 02 | `phases/pre-02-planning.md` | pre-02-api-spec.json |
| 03 | `phases/pre-03-planning.md` | pre-03-impl-plan.json |
| 04 | `phases/pre-04-planning.md` | pre-04-refactor-plan.json |
| 05 | `phases/pre-05-planning.md` | pre-05-integration-plan.json |

**Config:** `devforgeai/config/pre-phase-planning.yaml`
**Schema:** `devforgeai/config/pre-phase-planning.schema.json`
